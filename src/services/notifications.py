import asyncio
import aiosmtplib
import httpx
from email.mime.text import MIMEText
from twilio.rest import Client
from typing import Dict
from src.config.settings import (
    EMAIL_SMTP_SERVER,
    EMAIL_SMTP_PORT,
    EMAIL_SENDER,
    EMAIL_PASSWORD,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    CRM_API_URL,
    CRM_API_KEY
)
from src.database.connection import get_db_pool
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


async def send_email_summary(
    to_email: str, 
    subject: str, 
    body: str,
    metrics: Dict
):
    """Send email summary (async)"""
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL_SENDER
        msg['To'] = to_email
        
        await aiosmtplib.send(
            msg,
            hostname=EMAIL_SMTP_SERVER,
            port=EMAIL_SMTP_PORT,
            username=EMAIL_SENDER,
            password=EMAIL_PASSWORD,
            start_tls=True
        )
        logger.info(f"Email sent to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        metrics["errors"]["email_failed"] += 1


async def send_email_with_retry(
    to_email: str, 
    subject: str, 
    body: str, 
    company_id: int,
    metrics: Dict,
    max_retries: int = 3
) -> bool:
    """
    Use company's email config from server.js flow
    """
    try:
        db_pool = get_db_pool()
        
        # Get company email config (same as server.js does)
        if not db_pool:
            logger.error("Database pool not initialized")
            return False
        
        async with db_pool.acquire() as conn:
            email_config = await conn.fetchrow("""
                SELECT 
                    id,
                    email_address,
                    provider,
                    oauth_access_token,
                    oauth_refresh_token,
                    oauth_token_expires_at
                FROM email_configs
                WHERE company_id = $1 AND is_active = TRUE
                ORDER BY created_at DESC
                LIMIT 1
            """, company_id)
        
        if not email_config:
            logger.error(f"No active email config for company {company_id}")
            return False
        
        # Use CRM API to send email (reuses server.js logic)
        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient(timeout=15.0) as client:
                    response = await client.post(
                        f"{CRM_API_URL}/email/send",
                        json={
                            "company_id": company_id,
                            "to_email": to_email,
                            "subject": subject,
                            "body": body,
                            "from_config_id": email_config.get('id')
                        }
                    )
                    
                    if response.status_code == 200:
                        logger.info(f"📧 Email sent successfully to {to_email} via CRM API")
                        return True
                    else:
                        logger.warning(f"Email API returned {response.status_code}: {response.text}")
                        
            except Exception as e:
                logger.error(f"Email attempt {attempt + 1} failed: {e}")
                
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                else:
                    # Log to email_queue for manual retry
                    try:
                        async with db_pool.acquire() as conn:
                            await conn.execute("""
                                INSERT INTO email_queue (
                                    company_id, to_email, subject, body, 
                                    status, error_message, retry_count
                                )
                                VALUES ($1, $2, $3, $4, 'failed', $5, $6)
                            """, company_id, to_email, subject, body, str(e), attempt + 1)
                    except Exception as db_error:
                        logger.error(f"Failed to log email error: {db_error}")
                    
                    metrics["errors"]["email_failed"] += 1
                    return False
        
        return False
        
    except Exception as e:
        logger.error(f"Email sending error: {e}", exc_info=True)
        return False


async def send_whatsapp_summary(to_phone: str, body: str, metrics: Dict):
    """Send WhatsApp summary via Twilio"""
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: client.messages.create(
                from_=f'whatsapp:+19784045213',  # Your WhatsApp number
                body=body,
                to=f'whatsapp:{to_phone}'
            )
        )
        logger.info(f"WhatsApp sent to {to_phone}")
    except Exception as e:
        logger.error(f"Failed to send WhatsApp: {e}")
        metrics["errors"]["whatsapp_failed"] += 1