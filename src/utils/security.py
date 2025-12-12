import os
from fastapi import Request
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


def verify_webhook_signature(request: Request, expected_token: str = None) -> bool:
    """
    Verify webhook came from Twilio/n8n
    """
    # For Twilio webhooks
    if expected_token:
        signature = request.headers.get("X-Twilio-Signature", "")
        url = str(request.url)
        
        # Simple token validation (enhance with HMAC in production)
        if not signature and not expected_token:
            return True  # Skip validation if no token configured
        
        return signature == expected_token
    
    # For n8n webhooks - check API key
    api_key = request.headers.get("Authorization", "").replace("Bearer ", "")
    valid_key = os.getenv("N8N_WEBHOOK_KEY", "your-secret-key")
    
    return api_key == valid_key