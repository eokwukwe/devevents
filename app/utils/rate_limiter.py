from typing import Callable
from fastapi import HTTPException, Request, status
from limits import RateLimitItemPerMinute, storage, strategies


throttler = strategies.MovingWindowRateLimiter(storage.MemoryStorage())


def _default_identifier(request: Request) -> str:
    """
    Extracts a unique identifier from a request.

    This function uses the client's IP address as the unique identifier,
    which is a common approach for client identification in rate limiting.

    Args:
        request (Request): The incoming request object from FastAPI.

    Returns:
        str: A string representing the unique identifier of the client.
    """
    return request.client.host


class RateLimiter:
    """
    A rate limiting class using the Moving Window strategy.

    This class is designed to be used as a dependency in FastAPI routes
    to enforce rate limits based on the number of requests per minute.

    Attributes:
        rate (int): The number of requests allowed per minute.
        cost (int): The cost of each request. Default is 1.
        identifier (Callable[[Request], str]): A function to identify unique clients.

    Raises:
        HTTPException: A 429 Too Many Requests error if the rate limit is exceeded.

    Examples:
        To use this rate limiter, add an instance of `PerMinuteRateLimit` as a dependency in your FastAPI route:

        @app.get("/some-path")
        async def some_path(request: Request, _=Depends(PerMinuteRateLimit())):
            # Your endpoint logic here
    """

    def __init__(
        self,
        rate: int = 5,
        cost: int = 1,
        identifier: Callable[[Request], str] = _default_identifier,
    ):
        self.rate = rate
        self.cost = cost
        self.identifier = identifier

    def __call__(self, request: Request):
        key = self.identifier(request)
        limit_item = RateLimitItemPerMinute(self.rate)

        if not throttler.hit(limit_item, key, self.cost):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="request limit reached")
