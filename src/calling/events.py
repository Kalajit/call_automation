import asyncio
import time
import httpx
from typing import List, Dict
from datetime import datetime, timezone
from twilio.rest import Client
from vocode.streaming.utils import events_manager
from vocode.streaming.models.events import Event, EventType
from vocode.streaming.models.transcript import TranscriptCompleteEvent
from src.config.settings import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    CRM_API_URL,
    CRM_API_KEY
)
from src.database.call_logs import save_call_log
from src.database.leads import update_lead_status
from src.services.ai_analysis import (
    analyze_sentiment,
    generate_summary,
    route_based_on_sentiment,
    check_call_transfer_criteria
)
from src.services.notifications import send_email_summary, send_whatsapp_summary
from src.services.crm_integration import update_crm
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


class ProductionEventsManager(events_manager.EventsManager):
    """Enhanced events manager with full Module 1 features"""
    
    def __init__(self, conversation_store: Dict, active_calls: Dict, metrics: Dict):
        super().__init__(subscriptions=[EventType.TRANSCRIPT, EventType.TRANSCRIPT_COMPLETE])
        self.conversation_store = conversation_store
        self.active_calls = active_calls
        self.metrics = metrics
    
    async def handle_event(self, event: Event):
        if event.type == EventType.TRANSCRIPT:
            await self._handle_transcript_update(event)  # Live updates
        elif event.type == EventType.TRANSCRIPT_COMPLETE:
            await self._handle_transcript_complete(event)  # Final updates
    
    # ============================================
    # LIVE PER-TURN HANDLER
    # ============================================
    async def _handle_transcript_update(self, event):
        """Process each conversational turn for LIVE updates"""
        call_sid = event.conversation_id
        
        try:
            if call_sid not in self.conversation_store:
                logger.warning(f"No conversation data for {call_sid}")
                return
            
            conv_data = self.conversation_store[call_sid]
            
            # Check if this is a TranscriptEvent (has transcript attribute)
            if not hasattr(event, 'transcript'):
                logger.debug(f"Event has no transcript attribute, skipping")
                return
            
            # Get all turns from the transcript
            turns_so_far = []
            for turn in event.transcript.turns:
                turns_so_far.append({
                    "speaker": "human" if turn.speaker == "human" else "bot",
                    "text": turn.text,
                    "timestamp": turn.timestamp or int(time.time() * 1000)
                })
            
            # Store in conversation data
            conv_data['turns'] = turns_so_far
            
            # Only analyze if there are human turns
            human_turns = [t for t in turns_so_far if t['speaker'] == 'human']
            if len(human_turns) == 0:
                return
            
            # Build transcript text
            transcript_text = self._build_transcript(turns_so_far)
            
            # Run LIVE sentiment + summary analysis
            sentiment = await analyze_sentiment(transcript_text, self.metrics)
            summary = await generate_summary(transcript_text)
            
            logger.info(f"🔴 LIVE Update: {call_sid} | Sentiment: {sentiment['sentiment']} | Intent: {summary['intent']}")
            
            # Save lightweight DB update with in-progress status
            await save_call_log(
                call_sid=call_sid,
                company_id=conv_data.get("company_id"),
                lead_id=conv_data.get("lead_id"),
                to_phone=conv_data.get("to_phone"),
                from_phone=conv_data.get("from_phone"),
                call_type=conv_data.get("call_type", "qualification"),
                call_status="in-progress",  # KEY: Mark as in-progress
                transcript=transcript_text,
                sentiment=sentiment,
                summary=summary,
                conversation_history=turns_so_far
            )
            
            # Broadcast LIVE update to WebSocket clients
            await self._broadcast_live_update(
                call_sid=call_sid,
                lead_id=conv_data.get("lead_id"),
                sentiment=sentiment,
                summary=summary,
                transcript=transcript_text,
                turn_count=len(turns_so_far)
            )
            
            # Check if human takeover needed (based on live sentiment)
            if conv_data.get("lead_id"):
                await check_call_transfer_criteria(
                    sentiment, summary, conv_data["lead_id"], call_sid,
                    self.conversation_store, self.metrics
                )
            
        except Exception as e:
            logger.error(f"❌ Error in live turn handler for {call_sid}: {e}", exc_info=True)

    # ============================================
    # TRANSCRIPT COMPLETE HANDLER
    # ============================================
    async def _handle_transcript_complete(self, event: TranscriptCompleteEvent):
        """Process completed call transcript with ALL features"""
        call_sid = event.conversation_id
        
        try:
            # Get conversation data
            if call_sid not in self.conversation_store:
                logger.warning(f"No conversation data for {call_sid}")
                return
            
            conv_data = self.conversation_store[call_sid]

            # Use accumulated turns or rebuild from event
            turns = conv_data.get('turns', [])
            if not turns:
                turns = [
                    {
                        "speaker": turn.speaker,
                        "text": turn.text,
                        "timestamp": turn.timestamp or int(time.time() * 1000)
                    }
                    for turn in event.transcript.turns
                ]
            
            transcript_text = self._build_transcript(turns)
            
            logger.info(f"📝 Processing transcript for {call_sid}")
            
            # 1. Analyze Sentiment (Module 1 Req)
            sentiment = await analyze_sentiment(transcript_text, self.metrics)
            logger.info(f"😊 Sentiment: {sentiment['sentiment']} (score: {sentiment.get('tone_score')})")
            
            # 2. Generate Summary (Module 1 Req)
            summary = await generate_summary(transcript_text)
            logger.info(f"📋 Intent: {summary['intent']}, Follow-up: {summary.get('follow_up_required')}")
            
            # 3. Route Based on Sentiment (Module 1 Req)
            lead_id = conv_data.get("lead_id")
            if lead_id:
                routing_team = await route_based_on_sentiment(sentiment, lead_id, self.metrics)
                summary["routed_to"] = routing_team
            
            # 4. Fetch Twilio Recording URL (Module 1 Req)
            recording_url = None
            try:
                client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                recordings = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: client.recordings.list(call_sid=call_sid, limit=1)
                )
                if recordings:
                    recording_url = f"https://api.twilio.com{recordings[0].uri.replace('.json', '.mp3')}"
                    self.metrics["total_recordings"] += 1
            except Exception as e:
                logger.error(f"Failed to fetch recording: {e}")
            
            # 5. Get Call Duration
            call_duration = 0
            try:
                client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                call = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: client.calls(call_sid).fetch()
                )
                call_duration = int(call.duration) if call.duration else 0
                
                # Update avg duration metric
                if call_duration > 0:
                    current_avg = self.metrics["avg_call_duration"]
                    total_completed = sum(self.metrics["calls_completed"].values())
                    self.metrics["avg_call_duration"] = (
                        (current_avg * (total_completed - 1) + call_duration) / total_completed
                        if total_completed > 0 else call_duration
                    )
            except Exception as e:
                logger.debug(f"Could not fetch call duration: {e}")

            # 6. Check if call should be transferred to human (BEFORE DB SAVE)
            transfer_initiated = False
            if lead_id:
                try:
                    transfer_initiated = await check_call_transfer_criteria(
                        sentiment, summary, lead_id, call_sid,
                        self.conversation_store, self.metrics
                    )
                    if transfer_initiated:
                        summary["transferred_to_human"] = True
                        summary["routed_to"] = "human_agent"
                        logger.info(f"Call {call_sid} flagged for transfer to human agent")
                except Exception as e:
                    logger.error(f"Error checking transfer criteria: {e}")
            
            # 7. Save to Database (Module 1 Req)
            await save_call_log(
                call_sid=call_sid,
                company_id=conv_data.get("company_id"),
                lead_id=lead_id,
                to_phone=conv_data.get("to_phone"),
                from_phone=conv_data.get("from_phone"),
                call_type=conv_data.get("call_type", "qualification"),
                call_status="completed",
                call_duration=call_duration,
                transcript=transcript_text,
                sentiment=sentiment,
                summary=summary,
                conversation_history=turns,
                recording_url=recording_url
            )
            
            # 8. Update Lead Status (Module 1 Req)
            if lead_id:
                new_status = "qualified" if summary.get("intent") == "interested" else "contacted"
                await update_lead_status(lead_id, new_status)
            
            # 9. Send Notifications (Module 1 Req - Email & WhatsApp)
            if conv_data.get("email"):
                email_body = f"""Call Summary
Duration: {call_duration}s
Sentiment: {sentiment['sentiment']} ({sentiment.get('tone_score')}/10)

Summary:
{summary['summary']}

Next Actions:
{chr(10).join(f'- {action}' for action in summary.get('next_actions', []))}

Recording: {recording_url or 'Processing...'}
"""
                await send_email_summary(
                    conv_data["email"],
                    "Call Summary - 4champz",
                    email_body,
                    self.metrics
                )
            
            if conv_data.get("to_phone"):
                whatsapp_body = f"📞 Call Summary: {summary['summary'][:100]}... Next: {', '.join(summary.get('next_actions', [])[:2])}"
                await send_whatsapp_summary(conv_data["to_phone"], whatsapp_body, self.metrics)
            
            # 10. Calculate duration if Twilio didn't provide it
            if call_duration == 0:
                call_duration = await self._calculate_call_duration(call_sid)
                logger.info(f"📊 Calculated call duration: {call_duration}s")

            # 11. Update External CRM (Module 1 Req)
            if lead_id:
                await update_crm(lead_id, {
                    "lead_id": lead_id,
                    "call_sid": call_sid,
                    "transcript": transcript_text,
                    "sentiment": sentiment,
                    "summary": summary,
                    "recording_url": recording_url,
                    "duration": call_duration
                }, self.metrics)

            # 12. Broadcast FINAL update to WebSocket
            await self._broadcast_live_update(
                call_sid=call_sid,
                lead_id=conv_data.get("lead_id"),
                sentiment=sentiment,
                summary=summary,
                transcript=transcript_text,
                turn_count=len(turns),
                call_status="completed",
                call_duration=call_duration,
                recording_url=recording_url
            )
            
            # 13. Update Metrics
            call_type = conv_data.get("call_type", "unknown")
            self.metrics["calls_completed"][call_type] += 1
            
            logger.info(f"✅ Call {call_sid} processed successfully")
            
            # 14. Cleanup after delay
            asyncio.create_task(self._cleanup_conversation(call_sid))
            
        except Exception as e:
            logger.error(f"❌ Error processing transcript for {call_sid}: {e}", exc_info=True)
            self.metrics["errors"]["transcript_processing"] += 1

    # ============================================
    # HELPER METHODS
    # ============================================
    
    async def _calculate_call_duration(self, call_sid: str) -> int:
        """Calculate accurate call duration"""
        try:
            if call_sid not in self.conversation_store:
                return 0
            
            conv_data = self.conversation_store[call_sid]
            started_at = conv_data.get('started_at')
            
            if not started_at:
                return 0
            
            start_time = datetime.fromisoformat(started_at)
            duration = (datetime.now(timezone.utc) - start_time).total_seconds()
            
            return int(duration)
            
        except Exception as e:
            logger.error(f"Failed to calculate duration: {e}")
            return 0
    
    def _build_transcript(self, turns: List[Dict]) -> str:
        """Build readable transcript from turns"""
        lines = []
        for turn in turns:
            speaker = turn['speaker'].upper()
            text = turn['text']
            lines.append(f"{speaker}: {text}")
        return "\n".join(lines)
    
    async def _broadcast_live_update(
        self, 
        call_sid: str, 
        lead_id: int,
        sentiment: Dict,
        summary: Dict,
        transcript: str,
        turn_count: int,
        call_status: str = "in-progress",
        call_duration: int = None,
        recording_url: str = None
    ):
        """Broadcast live update to Node.js WebSocket server"""
        try:
            payload = {
                "call_sid": call_sid,
                "lead_id": lead_id,
                "sentiment": sentiment,
                "summary": summary,
                "transcript": transcript,
                "turn_count": turn_count,
                "call_status": call_status,
                "call_duration": call_duration,
                "recording_url": recording_url,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.post(
                    f"{CRM_API_URL}/live-update",
                    json=payload,
                    headers={"Authorization": f"Bearer {CRM_API_KEY}"}
                )
                response.raise_for_status()
                logger.debug(f"✅ Live update broadcast for {call_sid}")
                
        except Exception as e:
            logger.warning(f"Failed to broadcast live update: {e}")
            # Don't fail the call if broadcast fails
    
    async def _cleanup_conversation(self, call_sid: str):
        """Clean up conversation data after 5 minutes"""
        await asyncio.sleep(300)
        self.conversation_store.pop(call_sid, None)
        self.active_calls.pop(call_sid, None)
        logger.debug(f"🧹 Cleaned up conversation {call_sid}")