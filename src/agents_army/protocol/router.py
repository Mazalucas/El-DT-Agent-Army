"""Message routing for agent communication."""

import asyncio
from collections import defaultdict
from typing import Callable, Dict, List, Optional

from agents_army.protocol.message import AgentMessage
from agents_army.protocol.types import AgentRole


class MessageRouter:
    """
    Basic message router for agent communication.

    Routes messages to registered handlers based on recipient role(s).
    """

    def __init__(self):
        """Initialize the message router."""
        self._handlers: Dict[AgentRole, List[Callable]] = defaultdict(list)
        self._message_queue: asyncio.Queue = asyncio.Queue()
        self._running: bool = False
        self._task: Optional[asyncio.Task] = None

    def register_handler(
        self, role: AgentRole, handler: Callable[[AgentMessage], None]
    ) -> None:
        """
        Register a message handler for a specific role.

        Args:
            role: The agent role to handle messages for
            handler: Async function that takes an AgentMessage and returns None
        """
        self._handlers[role].append(handler)

    def unregister_handler(
        self, role: AgentRole, handler: Callable[[AgentMessage], None]
    ) -> None:
        """
        Unregister a message handler.

        Args:
            role: The agent role
            handler: The handler to remove
        """
        if role in self._handlers and handler in self._handlers[role]:
            self._handlers[role].remove(handler)

    async def route(self, message: AgentMessage) -> None:
        """
        Route a message to appropriate handlers.

        Args:
            message: The message to route
        """
        # Validate message
        if not self._is_valid_message(message):
            raise ValueError(f"Invalid message: {message.id}")

        # Get recipient roles
        to_roles = message.get_to_roles()

        # Route to all matching handlers
        for role in to_roles:
            if role in self._handlers:
                for handler in self._handlers[role]:
                    try:
                        if asyncio.iscoroutinefunction(handler):
                            await handler(message)
                        else:
                            handler(message)
                    except Exception as e:
                        # Log error but continue routing to other handlers
                        print(f"Error in handler for {role}: {e}")

    async def send(self, message: AgentMessage) -> None:
        """
        Send a message (adds to queue if router is running, otherwise routes immediately).

        Args:
            message: The message to send
        """
        if self._running:
            await self._message_queue.put(message)
        else:
            await self.route(message)

    async def start(self) -> None:
        """Start the message router (begins processing queue)."""
        if self._running:
            return

        self._running = True
        self._task = asyncio.create_task(self._process_queue())

    async def stop(self) -> None:
        """Stop the message router."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    async def _process_queue(self) -> None:
        """Process messages from the queue."""
        while self._running:
            try:
                message = await asyncio.wait_for(
                    self._message_queue.get(), timeout=1.0
                )
                await self.route(message)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f"Error processing message: {e}")

    def _is_valid_message(self, message: AgentMessage) -> bool:
        """
        Validate a message.

        Args:
            message: Message to validate

        Returns:
            True if valid, False otherwise
        """
        # Basic validation
        if not message.id:
            return False
        if not message.from_role:
            return False
        if not message.to_role:
            return False
        if not message.type:
            return False

        return True

    def get_registered_roles(self) -> List[AgentRole]:
        """
        Get list of roles with registered handlers.

        Returns:
            List of agent roles
        """
        return list(self._handlers.keys())

    def get_handler_count(self, role: AgentRole) -> int:
        """
        Get number of handlers for a role.

        Args:
            role: The agent role

        Returns:
            Number of handlers
        """
        return len(self._handlers.get(role, []))
