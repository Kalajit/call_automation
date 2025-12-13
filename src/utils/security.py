import os
from fastapi import Request, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.utils.logging_config import get_logger
from src.config.settings import (
    JWT_SECRET_KEY, 
    JWT_ALGORITHM, 
    SERVICE_API_KEY,
    TWILIO_AUTH_TOKEN
)
import hmac
import hashlib
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict


logger = get_logger(__name__)

security = HTTPBearer()

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



# ============================================
# JWT TOKEN VALIDATION
# ============================================

def verify_jwt_token(token: str) -> Dict:
    """
    Verify JWT token issued by Node.js server.
    Returns decoded payload if valid, raises HTTPException if invalid.
    """
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
        )
        
        # Check expiration
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        
        # Validate required fields
        if "user_id" not in payload or "company_id" not in payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        logger.info(f"JWT validated for user {payload.get('user_id')}, company {payload.get('company_id')}")
        return payload
        
    except jwt.ExpiredSignatureError:
        logger.warning("Expired JWT token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid JWT token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )

# ============================================
# API KEY VALIDATION (Backup Method)
# ============================================

def verify_api_key(api_key: str) -> bool:
    """
    Verify service-to-service API key.
    Use this for internal services that don't have JWT.
    """
    if not SERVICE_API_KEY:
        logger.error("SERVICE_API_KEY not configured")
        return False
    
    is_valid = hmac.compare_digest(api_key, SERVICE_API_KEY)
    if not is_valid:
        logger.warning("Invalid API key provided")
    return is_valid

# ============================================
# TWILIO WEBHOOK SIGNATURE VALIDATION
# ============================================

def verify_twilio_signature(
    signature: str,
    url: str,
    params: Dict
) -> bool:
    """
    Verify Twilio webhook signature for additional security.
    """
    if not TWILIO_AUTH_TOKEN:
        logger.warning("TWILIO_AUTH_TOKEN not set, skipping signature verification")
        return True
    
    # Create expected signature
    data = url + ''.join([f'{k}{v}' for k, v in sorted(params.items())])
    expected = hmac.new(
        TWILIO_AUTH_TOKEN.encode('utf-8'),
        data.encode('utf-8'),
        hashlib.sha1
    ).digest()
    
    # Compare
    import base64
    expected_b64 = base64.b64encode(expected).decode('utf-8')
    
    is_valid = hmac.compare_digest(signature, expected_b64)
    if not is_valid:
        logger.warning("Invalid Twilio signature")
    return is_valid

# ============================================
# COMBINED AUTHENTICATION DEPENDENCY
# ============================================

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> Dict:
    """
    FastAPI dependency to validate authentication.
    Supports both JWT and API Key.
    """
    token = credentials.credentials
    
    # Try JWT first
    try:
        return verify_jwt_token(token)
    except HTTPException:
        pass
    
    # Fallback to API Key
    if verify_api_key(token):
        return {
            "user_id": "service",
            "company_id": None,
            "role": "service",
            "authenticated_via": "api_key"
        }
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

# ============================================
# OPTIONAL: ROLE-BASED ACCESS CONTROL
# ============================================

def require_role(required_role: str):
    """
    Decorator to require specific role.
    Usage: @require_role("admin")
    """
    async def role_checker(current_user: Dict = Security(get_current_user)):
        user_role = current_user.get("role", "user")
        if user_role != required_role and user_role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires {required_role} role"
            )
        return current_user
    return role_checker

# ============================================
# COMPANY OWNERSHIP VALIDATION
# ============================================

def verify_company_access(current_user: Dict, company_id: int) -> bool:
    """
    Verify user has access to the specified company.
    """
    user_company_id = current_user.get("company_id")
    
    # Service accounts have access to all companies
    if current_user.get("role") == "service":
        return True
    
    # Admins have access to all companies
    if current_user.get("role") == "admin":
        return True
    
    # Regular users can only access their company
    if user_company_id != company_id:
        logger.warning(f"User {current_user.get('user_id')} attempted to access company {company_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this company"
        )
    
    return True