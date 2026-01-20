"""Rate limiting for Agents_Army."""

from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, Optional


class RateLimiter:
    """
    Rate limiter for API and agent actions.

    Prevents abuse by limiting requests per time window.
    """

    def __init__(
        self,
        default_limit: int = 100,
        default_window: timedelta = timedelta(minutes=1),
    ):
        """
        Initialize RateLimiter.

        Args:
            default_limit: Default requests per window
            default_window: Default time window
        """
        self.default_limit = default_limit
        self.default_window = default_window
        self.limits: Dict[str, Dict[str, int]] = defaultdict(
            lambda: {"limit": default_limit, "window_seconds": default_window.total_seconds()}
        )
        self.requests: Dict[str, List[datetime]] = defaultdict(list)

    def set_limit(
        self,
        identifier: str,
        limit: int,
        window: Optional[timedelta] = None,
    ) -> None:
        """
        Set rate limit for an identifier.

        Args:
            identifier: Identifier (agent_id, IP, etc.)
            limit: Requests per window
            window: Time window (uses default if None)
        """
        self.limits[identifier] = {
            "limit": limit,
            "window_seconds": (
                window.total_seconds() if window else self.default_window.total_seconds()
            ),
        }

    def is_allowed(self, identifier: str) -> bool:
        """
        Check if request is allowed.

        Args:
            identifier: Request identifier

        Returns:
            True if allowed, False if rate limited
        """
        now = datetime.now()
        limit_config = self.limits[identifier]
        limit = limit_config["limit"]
        window_seconds = limit_config["window_seconds"]
        window = timedelta(seconds=window_seconds)

        # Clean old requests
        cutoff = now - window
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier] if req_time > cutoff
        ]

        # Check limit
        if len(self.requests[identifier]) >= limit:
            return False

        # Record request
        self.requests[identifier].append(now)
        return True

    def get_remaining(self, identifier: str) -> int:
        """
        Get remaining requests for identifier.

        Args:
            identifier: Request identifier

        Returns:
            Number of remaining requests
        """
        now = datetime.now()
        limit_config = self.limits[identifier]
        limit = limit_config["limit"]
        window_seconds = limit_config["window_seconds"]
        window = timedelta(seconds=window_seconds)

        # Clean old requests
        cutoff = now - window
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier] if req_time > cutoff
        ]

        return max(0, limit - len(self.requests[identifier]))

    def reset(self, identifier: Optional[str] = None) -> None:
        """
        Reset rate limit for identifier or all.

        Args:
            identifier: Optional identifier (resets all if None)
        """
        if identifier:
            self.requests[identifier].clear()
        else:
            self.requests.clear()
