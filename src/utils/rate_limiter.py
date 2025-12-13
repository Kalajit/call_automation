import time
from collections import defaultdict
from typing import Dict, Tuple
from fastapi import HTTPException, Request, status
from src.config.settings import RATE_LIMIT_ENABLED, RATE_LIMIT_CALLS, RATE_LIMIT_PERIOD
from src.utils.logging_config import logger

class RateLimiter:
    """
    In-memory rate limiter (for production, use Redis)
    """
    def __init__(self):
        self.requests: Dict[str, list] = defaultdict(list)
    
    def is_allowed(self, identifier: str) -> Tuple[bool, int]:
        """
        Check if request is allowed under rate limit.
        Returns (is_allowed, remaining_calls)
        """
        if not RATE_LIMIT_ENABLED:
            return True, RATE_LIMIT_CALLS
        
        now = time.time()
        window_start = now - RATE_LIMIT_PERIOD
        
        # Clean old entries
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if req_time > window_start
        ]
        
        # Check limit
        current_count = len(self.requests[identifier])
        if current_count >= RATE_LIMIT_CALLS:
            logger.warning(f"Rate limit exceeded for {identifier}")
            return False, 0
        
        # Add current request
        self.requests[identifier].append(now)
        remaining = RATE_LIMIT_CALLS - current_count - 1
        
        return True, remaining

rate_limiter = RateLimiter()

async def check_rate_limit(request: Request, current_user: Dict):
    """
    FastAPI dependency to check rate limits.
    """
    # Use user_id or company_id as identifier
    identifier = f"user_{current_user.get('user_id')}_{current_user.get('company_id')}"
    
    allowed, remaining = rate_limiter.is_allowed(identifier)
    
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Try again in {RATE_LIMIT_PERIOD} seconds.",
            headers={"Retry-After": str(RATE_LIMIT_PERIOD)}
        )
    
    # Add rate limit info to response headers (handled in middleware)
    request.state.rate_limit_remaining = remaining
    return True