from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.rate_limiter import RateLimiter


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, rate_limiter: RateLimiter):
        super().__init__(app)
        self.rate_limiter = rate_limiter

    async def dispatch(self, request: Request, call_next):
        try:
            # Use the rate limiter here
            self.rate_limiter(request)
        except HTTPException as exc:
            # Return the rate limit exceeded response
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail}
            )

        # Proceed to the next middleware or route handler
        response = await call_next(request)
        return response
