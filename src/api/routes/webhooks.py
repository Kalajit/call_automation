from fastapi import APIRouter, Request, Header, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from src.database.call_logs import save_call_log
from src.services.notifications import send_whatsapp_summary
from src.utils.security import verify_webhook_signature
from src.utils.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter(tags=["webhooks"])


def setup_webhook_routes(conversation_store: dict, metrics: dict):
    """Setup webhook routes with dependencies"""
    
    @router.post("/call_status")
    async def call_status_callback(
        request: Request,
        x_twilio_signature: Optional[str] = Header(None)
    ):
        """
        Twilio call status callback
        
        Module 1 Requirement: Call status tracking
        """
        try:
            # Verify Twilio signature for security
            form_data = await request.form()
            url = str(request.url)
            
            if x_twilio_signature:
                params = dict(form_data)
                # if not verify_twilio_signature(x_twilio_signature, url, params):
                if not verify_webhook_signature(x_twilio_signature, url, params):
                    logger.warning("⚠️ Invalid Twilio signature on call_status webhook")
                    return JSONResponse(
                        status_code=403,
                        content={"error": "Invalid signature"}
                    )
            else:
                logger.warning("⚠️ No Twilio signature provided on call_status webhook")
            
            call_sid = form_data.get("CallSid")
            call_status = form_data.get("CallStatus")
            
            logger.info(f"📞 Call status: {call_sid} -> {call_status}")
            
            # Update database
            if call_sid in conversation_store:
                conv = conversation_store[call_sid]
                
                try:
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
                        logger.info(f"✅ Call completed: {call_sid}")
                    elif call_status in ["failed", "busy", "no-answer"]:
                        metrics["calls_failed"][conv.get("call_type", "unknown")] += 1
                        logger.warning(f"❌ Call failed ({call_status}): {call_sid}")
                        
                except Exception as db_error:
                    logger.error(f"Failed to save call log: {db_error}", exc_info=True)
            else:
                logger.warning(f"Call {call_sid} not found in conversation store")
            
            return {"ok": True}
            
        except Exception as e:
            logger.error(f"Call status callback error: {e}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={"ok": False, "error": str(e)}
            )

    @router.post("/recording_status")
    async def recording_status_callback(
        request: Request,
        x_twilio_signature: Optional[str] = Header(None)
    ):

        """
        Twilio recording status callback
        
        Module 1 Requirement: Call recording
        """
        try:
            # Verify Twilio signature
            form_data = await request.form()
            url = str(request.url)
            
            if x_twilio_signature:
                params = dict(form_data)
                # if not verify_twilio_signature(x_twilio_signature, url, params):
                if not verify_webhook_signature(x_twilio_signature, url, params):
                    logger.warning("⚠️ Invalid Twilio signature on recording_status webhook")
                    return JSONResponse(
                        status_code=403,
                        content={"error": "Invalid signature"}
                    )
            
            call_sid = form_data.get("CallSid")
            recording_url = form_data.get("RecordingUrl")
            recording_status = form_data.get("RecordingStatus")
            recording_duration = form_data.get("RecordingDuration")
            
            logger.info(f"🎙️ Recording status: {call_sid} -> {recording_status}")
            
            if recording_status == "completed" and recording_url:
                # Update database with recording URL
                if call_sid in conversation_store:
                    conv = conversation_store[call_sid]
                    
                    try:
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
                        
                        logger.info(
                            f"✅ Recording saved: {call_sid} "
                            f"(duration: {recording_duration}s, url: {recording_url})"
                        )
                        
                    except Exception as db_error:
                        logger.error(f"Failed to save recording: {db_error}", exc_info=True)
                else:
                    logger.warning(f"Call {call_sid} not found in conversation store")
            
            return {"ok": True}
            
        except Exception as e:
            logger.error(f"Recording callback error: {e}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={"ok": False, "error": str(e)}
            )

    @router.post("/dial_status")
    async def dial_status_callback(
        request: Request,
        x_twilio_signature: Optional[str] = Header(None)
    ):
        """
        Handle Twilio Dial status (after transfer)
        **Now with Twilio signature verification**
        """
        try:
            # Verify Twilio signature
            form_data = await request.form()
            url = str(request.url)
            
            if x_twilio_signature:
                params = dict(form_data)
                # if not verify_twilio_signature(x_twilio_signature, url, params):
                if not verify_webhook_signature(x_twilio_signature, url, params):
                    logger.warning("⚠️ Invalid Twilio signature on dial_status webhook")
                    return JSONResponse(
                        status_code=403,
                        content={"error": "Invalid signature"}
                    )
            
            call_sid = form_data.get("CallSid")
            dial_status = form_data.get("DialCallStatus")
            
            logger.info(f"📲 Dial status: {call_sid} -> {dial_status}")
            
            if dial_status == "completed":
                # Human answered
                logger.info(f"✅ Call transferred successfully: {call_sid}")
                
            elif dial_status in ["busy", "no-answer", "failed"]:
                # Human didn't answer - fallback to voicemail
                logger.warning(f"⚠️ Transfer failed ({dial_status}), sending to voicemail")
                
                # Send WhatsApp fallback
                if call_sid in conversation_store:
                    conv = conversation_store[call_sid]
                    try:
                        await send_whatsapp_summary(
                            conv.get("to_phone"),
                            f"We tried to connect you with our team but couldn't reach them. "
                            f"We'll call you back within 30 minutes!",
                            metrics
                        )
                        logger.info(f"📨 WhatsApp fallback sent to {conv.get('to_phone')}")
                        
                    except Exception as wa_error:
                        logger.error(f"Failed to send WhatsApp fallback: {wa_error}", exc_info=True)
            
            return {"ok": True}
            
        except Exception as e:
            logger.error(f"Dial status error: {e}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={"ok": False, "error": str(e)}
            )
    
    return router