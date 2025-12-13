import re
from typing import Optional


def validate_phone_number(phone: str) -> bool:
    """
    Validate phone number format
    
    Args:
        phone: Phone number string
        
    Returns:
        True if valid, False otherwise
    """
    if not phone:
        return False
    
    # Remove all non-digits
    digits = re.sub(r'\D', '', phone)
    
    # Check if it's a valid length (10-15 digits)
    if len(digits) < 10 or len(digits) > 15:
        return False
    
    return True


def normalize_phone_number(phone: str, default_country_code: str = "+91") -> Optional[str]:
    """
    Normalize phone number to E.164 format
    
    Args:
        phone: Phone number string
        default_country_code: Default country code (default: +91 for India)
        
    Returns:
        Normalized phone number or None if invalid
    """
    if not phone:
        return None
    
    # Remove all non-digits
    digits = re.sub(r'\D', '', phone)
    
    # If 10 digits, add default country code
    if len(digits) == 10:
        return f"{default_country_code}{digits}"
    
    # If already has country code
    if len(digits) > 10:
        if not digits.startswith('+'):
            return f"+{digits}"
        return digits
    
    return None


def validate_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email string
        
    Returns:
        True if valid, False otherwise
    """
    if not email:
        return False
    
    # Basic email validation regex
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_iso_datetime(datetime_str: str) -> bool:
    """
    Validate ISO datetime format
    
    Args:
        datetime_str: DateTime string
        
    Returns:
        True if valid ISO format, False otherwise
    """
    from datetime import datetime
    
    try:
        datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
        return True
    except (ValueError, AttributeError):
        return False