"""Integration tests for message flows."""

import asyncio
import pytest

from agents_army.protocol.message import AgentMessage
from agents_army.protocol.router import MessageRouter
from agents_army.protocol.types import AgentRole, MessageType


class TestMessageFlow:
    """Test message flows between agents."""

    @pytest.mark.asyncio
    async def test_simple_message_flow(self):
        """Test simple message flow from DT to Researcher."""
        router = MessageRouter()
        received_messages = []

        async def researcher_handler(message: AgentMessage):
            received_messages.append(message)

        router.register_handler(AgentRole.RESEARCHER, researcher_handler)

        message = AgentMessage(
            from_role=AgentRole.DT,
            to_role=AgentRole.RESEARCHER,
            type=MessageType.TASK_REQUEST,
            payload={"task_id": "task_001", "description": "Research X"},
        )

        await router.route(message)

        assert len(received_messages) == 1
        assert received_messages[0].id == message.id
        assert received_messages[0].payload["task_id"] == "task_001"

    @pytest.mark.asyncio
    async def test_broadcast_message(self):
        """Test message broadcast to multiple recipients."""
        router = MessageRouter()
        researcher_messages = []
        writer_messages = []

        async def researcher_handler(message: AgentMessage):
            researcher_messages.append(message)

        async def writer_handler(message: AgentMessage):
            writer_messages.append(message)

        router.register_handler(AgentRole.RESEARCHER, researcher_handler)
        router.register_handler(AgentRole.WRITER, writer_handler)

        message = AgentMessage(
            from_role=AgentRole.DT,
            to_role=[AgentRole.RESEARCHER, AgentRole.WRITER],
            type=MessageType.TASK_REQUEST,
            payload={"task_id": "task_001"},
        )

        await router.route(message)

        assert len(researcher_messages) == 1
        assert len(writer_messages) == 1
        assert researcher_messages[0].id == message.id
        assert writer_messages[0].id == message.id

    @pytest.mark.asyncio
    async def test_message_queue(self):
        """Test message queue processing."""
        router = MessageRouter()
        received_messages = []

        async def handler(message: AgentMessage):
            received_messages.append(message)

        router.register_handler(AgentRole.RESEARCHER, handler)
        await router.start()

        # Send multiple messages
        for i in range(3):
            message = AgentMessage(
                from_role=AgentRole.DT,
                to_role=AgentRole.RESEARCHER,
                type=MessageType.TASK_REQUEST,
                payload={"task_id": f"task_{i:03d}"},
            )
            await router.send(message)

        # Wait for processing
        await asyncio.sleep(0.1)

        await router.stop()

        assert len(received_messages) == 3

    @pytest.mark.asyncio
    async def test_reply_flow(self):
        """Test request-reply flow."""
        router = MessageRouter()
        replies = []

        async def researcher_handler(message: AgentMessage):
            # Researcher responds to task request
            reply = AgentMessage(
                from_role=AgentRole.RESEARCHER,
                to_role=AgentRole.DT,
                type=MessageType.TASK_RESPONSE,
                payload={
                    "task_id": message.payload["task_id"],
                    "status": "completed",
                },
                reply_to=message.id,
            )
            await router.route(reply)

        async def dt_handler(message: AgentMessage):
            replies.append(message)

        router.register_handler(AgentRole.RESEARCHER, researcher_handler)
        router.register_handler(AgentRole.DT, dt_handler)

        request = AgentMessage(
            from_role=AgentRole.DT,
            to_role=AgentRole.RESEARCHER,
            type=MessageType.TASK_REQUEST,
            payload={"task_id": "task_001", "description": "Research X"},
        )

        await router.route(request)

        # Wait a bit for reply
        await asyncio.sleep(0.1)

        assert len(replies) == 1
        assert replies[0].type == MessageType.TASK_RESPONSE
        assert replies[0].is_reply_to(request)

    @pytest.mark.asyncio
    async def test_handler_error_handling(self):
        """Test that handler errors don't break routing."""
        router = MessageRouter()
        successful_messages = []

        async def failing_handler(message: AgentMessage):
            raise ValueError("Handler error")

        async def successful_handler(message: AgentMessage):
            successful_messages.append(message)

        router.register_handler(AgentRole.RESEARCHER, failing_handler)
        router.register_handler(AgentRole.RESEARCHER, successful_handler)

        message = AgentMessage(
            from_role=AgentRole.DT,
            to_role=AgentRole.RESEARCHER,
            type=MessageType.TASK_REQUEST,
            payload={"task_id": "task_001"},
        )

        # Should not raise exception
        await router.route(message)

        # Successful handler should still be called
        assert len(successful_messages) == 1
