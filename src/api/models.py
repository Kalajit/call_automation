import re
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, validator


class OutboundCallRequest(BaseModel):
    """Request model for outbound call"""
    company_id: int
    lead_id: int
    to_phone: str
    name: str
    call_type: str = "qualification"
    prompt_config_key: Optional[str] = None
    
    @validator("to_phone")
    def normalize_phone(cls, v):
        # Remove all non-digits
        digits = re.sub(r'\D', '', v)
        # Add +91 if 10 digits
        if len(digits) == 10:
            return f"+91{digits}"
        elif not digits.startswith('+'):
            return f"+{digits}"
        return v


class ScheduleCallRequest(BaseModel):
    """Request model for scheduling a call"""
    company_id: int
    lead_id: int
    call_type: str
    scheduled_time: str  # ISO format
    
    @validator("scheduled_time")
    def validate_time(cls, v):
        try:
            datetime.fromisoformat(v.replace('Z', '+00:00'))
            return v
        except:
            raise ValueError("Invalid ISO format")