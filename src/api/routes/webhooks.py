from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from src.database.call_logs import save_call_log
from src.services.notifications import send_whatsapp_summary
from src.utils.security import verify_webhook_signature
from src.utils.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter(tags=["webhooks"])


def setup_webhook_routes(conversation_store: dict, metrics: dict):
    """Setup webhook routes with dependencies"""
    
    @router.post("/call_status")
    async def call_status_callback(request: Request):
        """
        Twilio call status callback
        
        Module 1 Requirement: Call status tracking
        """
        try:
            if not verify_webhook_signature(request):
                logger.warning("⚠️ Unauthorized webhook attempt")
                return JSONResponse(status_code=403, content={"error": "Unauthorized"})
            
            form_data = await request.form()
            call_sid = form_data.get("CallSid")
            call_status = form_data.get("CallStatus")
            
            logger.info(f"Call status: {call_sid} -> {call_status}")
            
            # Update database
            if call_sid in conversation_store:
                conv = conversation_store[call_sid]
                
                await save_call_log(
                    call_sid=call_sid,
                    company_id=conv.get("company_id"),
                    lead_id=conv.get("lead_id"),
                    to_phone=conv.get("to_phone"),
                    from_phone=conv.get("from_phone"),
                    call_type=conv.get("call_type"),
                    call_status=call_status
                )
                
                # Update metrics
                if call_status == "completed":
                    metrics["calls_completed"][conv.get("call_type", "unknown")] += 1
                elif call_status in ["failed", "busy", "no-answer"]:
                    metrics["calls_failed"][conv.get("call_type", "unknown")] += 1
            
            return {"ok": True}
            
        except Exception as e:
            logger.error(f"Call status callback error: {e}")
            return {"ok": False}

    @router.post("/recording_status")
    async def recording_status_callback(request: Request):
        """
        Twilio recording status callback
        
        Module 1 Requirement: Call recording
        """
        try:
            form_data = await request.form()
            call_sid = form_data.get("CallSid")
            recording_url = form_data.get("RecordingUrl")
            recording_status = form_data.get("RecordingStatus")
            
            logger.info(f"Recording status: {call_sid} -> {recording_status}")
            
            if recording_status == "completed" and recording_url:
                # Update database
                if call_sid in conversation_store:
                    conv = conversation_store[call_sid]
                    
                    await save_call_log(
                        call_sid=call_sid,
                        company_id=conv.get("company_id"),
                        lead_id=conv.get("lead_id"),
                        to_phone=conv.get("to_phone"),
                        from_phone=conv.get("from_phone"),
                        call_type=conv.get("call_type"),
                        call_status="completed",
                        recording_url=recording_url
                    )
            
            return {"ok": True}
            
        except Exception as e:
            logger.error(f"Recording callback error: {e}")
            return {"ok": False}

    @router.post("/dial_status")
    async def dial_status_callback(request: Request):
        """Handle Twilio Dial status (after transfer)"""
        try:
            form_data = await request.form()
            call_sid = form_data.get("CallSid")
            dial_status = form_data.get("DialCallStatus")
            
            logger.info(f"Dial status: {call_sid} -> {dial_status}")
            
            if dial_status == "completed":
                # Human answered
                logger.info(f"✅ Call transferred successfully: {call_sid}")
            elif dial_status in ["busy", "no-answer", "failed"]:
                # Human didn't answer - fallback to voicemail
                logger.warning(f"⚠️ Transfer failed ({dial_status}), sending to voicemail")
                
                # Send WhatsApp fallback
                if call_sid in conversation_store:
                    conv = conversation_store[call_sid]
                    await send_whatsapp_summary(
                        conv.get("to_phone"),
                        f"We tried to connect you with our team but couldn't reach them. We'll call you back within 30 minutes!",
                        metrics
                    )
            
            return {"ok": True}
            
        except Exception as e:
            logger.error(f"Dial status error: {e}")
            return {"ok": False}
    
    return router