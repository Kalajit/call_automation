import json
import time
from typing import Optional, Dict, List
from datetime import datetime
from src.database.connection import get_db_pool
from src.database.leads import update_lead_status
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


async def save_call_log(
    call_sid: str,
    company_id: int,
    lead_id: int,
    to_phone: str,
    from_phone: str,
    call_type: str,
    call_status: str,
    call_duration: int = None,
    transcript: str = None,
    sentiment: Dict = None,
    summary: Dict = None,
    conversation_history: List = None,
    recording_url: str = None,
    local_audio_path: str = None
):
    """Save or update call log in database"""
    db_pool = get_db_pool()
    
    async with db_pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO call_logs (
                call_sid, company_id, lead_id, to_phone, from_phone,
                call_type, call_status, call_duration, transcript,
                sentiment, summary, conversation_history,
                recording_url, local_audio_path
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
            ON CONFLICT (call_sid) DO UPDATE SET
                call_status = EXCLUDED.call_status,
                call_duration = COALESCE(EXCLUDED.call_duration, call_logs.call_duration),
                transcript = COALESCE(EXCLUDED.transcript, call_logs.transcript),
                sentiment = COALESCE(EXCLUDED.sentiment, call_logs.sentiment),
                summary = COALESCE(EXCLUDED.summary, call_logs.summary),
                conversation_history = COALESCE(EXCLUDED.conversation_history, call_logs.conversation_history),
                recording_url = COALESCE(EXCLUDED.recording_url, call_logs.recording_url),
                local_audio_path = COALESCE(EXCLUDED.local_audio_path, call_logs.local_audio_path),
                updated_at = CURRENT_TIMESTAMP
        """, call_sid, company_id, lead_id, to_phone, from_phone,
            call_type, call_status, call_duration, transcript,
            json.dumps(sentiment) if sentiment else None,
            json.dumps(summary) if summary else None,
            json.dumps(conversation_history) if conversation_history else None,
            recording_url, local_audio_path
        )


async def handle_call_failure(
    company_id: int,
    lead_id: int,
    to_phone: str,
    from_phone: str,
    call_type: str,
    error_message: str,
    metrics: Dict
):
    """
    Handle call initiation failures
    """
    try:
        # Generate a pseudo call_sid for failed calls
        failed_call_sid = f"FAILED_{int(time.time())}_{lead_id}"
        
        # Save failed call log
        await save_call_log(
            call_sid=failed_call_sid,
            company_id=company_id,
            lead_id=lead_id,
            to_phone=to_phone,
            from_phone=from_phone or "unknown",
            call_type=call_type,
            call_status="failed",
            transcript=f"Call failed: {error_message}"
        )
        
        # Update lead status
        await update_lead_status(lead_id, "call_failed")
        
        # Create alert
        db_pool = get_db_pool()
        async with db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO alerts (alert_type, title, message, severity, lead_id)
                VALUES ($1, $2, $3, $4, $5)
            """, 
            "call_failed",
            f"Call Failed - Lead {lead_id}",
            f"Failed to call {to_phone}: {error_message}",
            "high",
            lead_id)
        
        metrics["calls_failed"][call_type] += 1
        logger.error(f"❌ Call failure handled for lead {lead_id}: {error_message}")
        
    except Exception as e:
        logger.error(f"Failed to handle call failure: {e}")