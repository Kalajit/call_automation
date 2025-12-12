import asyncio
import time
import re
import json
import httpx
from typing import Optional, Tuple, Dict
from datetime import datetime, timezone, timedelta
from collections import defaultdict
import dateparser
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import LLMChain
from vocode.streaming.agent.langchain_agent import LangchainAgent
from vocode.streaming.models.agent import LangchainAgentConfig
from vocode.streaming.models.message import BaseMessage
from src.config.settings import GROQ_API_KEY, CRM_API_URL, CRM_API_KEY
from src.config.constants import LANGUAGE_MAP
from src.database.connection import get_db_pool
from src.services.calendar_service import create_calendar_appointment
from src.utils.logging_config import get_logger
from multilingual_service import (
    get_multilingual_service,
    SUPPORTED_LANGUAGES
)

logger = get_logger(__name__)


class CustomLangchainAgentConfig(LangchainAgentConfig, type="agent_langchain"):
    """Custom agent configuration"""
    initial_message: BaseMessage
    prompt_preamble: str
    model_name: str = "llama-3.1-8b-instant"
    api_key: str = GROQ_API_KEY
    provider: str = "groq"


class ProductionLangchainAgent(LangchainAgent):
    """Production agent with multilingual support"""
    
    def __init__(self, agent_config: CustomLangchainAgentConfig, conversation_id: str = None):
        super().__init__(agent_config=agent_config)
        self.conversation_id_cache = conversation_id
        self.no_input_count = 0
        self.last_response_time = time.time()
        self.current_language = 'en'  
        self.lead_id = None
        self.language_detection_threshold = 2  
        self.detected_language_count = defaultdict(int)

        # Initialize multilingual service
        self.ml_service = get_multilingual_service()
        logger.info(f"✅ Agent initialized with multilingual support")

    async def detect_language_switch(self, user_input: str) -> Optional[str]:
        """
        Detect if user wants to switch language
        Uses Google Cloud Translation API for accurate detection
        """
        # Use the multilingual service for detection
        detected = self.ml_service.detect_language(user_input)
        
        if detected != self.current_language and detected in SUPPORTED_LANGUAGES:
            self.detected_language_count[detected] += 1
            
            if self.detected_language_count[detected] >= self.language_detection_threshold:
                logger.info(f"🔄 Auto-detected language switch: {self.current_language} → {detected}")
                self.detected_language_count.clear()
                await self.save_language_to_db(detected)
                return detected
            else:
                logger.debug(f"🔍 Detected {detected} ({self.detected_language_count[detected]}/{self.language_detection_threshold})")
        else:
            if detected == self.current_language:
                self.detected_language_count.clear()
        
        return None

    async def translate_text(self, text: str, target_lang: str) -> str:
        """Translate text to target language"""
        if target_lang == 'en' or not text:
            return text
        
        return self.ml_service.translate_text(text, target_lang, 'en')

    async def translate_to_english(self, text: str, source_lang: str) -> str:
        """Translate text to English for AI processing"""
        if source_lang == 'en' or not text:
            return text
        
        translated = self.ml_service.translate_text(text, 'en', source_lang)
        
        # Quality check
        if len(translated.strip()) < len(text.strip()) * 0.3:
            logger.warning(f"⚠️ Translation quality check failed, using original text")
            return text
        
        return translated

    async def update_lead_language_preference(self, lang_code: str):
        """Update lead's language preference in database"""
        if not self.lead_id:
            logger.debug("No lead_id available, skipping language preference update")
            return
        
        db_pool = get_db_pool()
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                async with db_pool.acquire() as conn:
                    await conn.execute(
                        """UPDATE leads 
                        SET preferred_language = $1, updated_at = CURRENT_TIMESTAMP 
                        WHERE id = $2""",
                        lang_code, self.lead_id
                    )
                    logger.info(f"✅ Updated lead {self.lead_id} language preference to {lang_code}")
                    return
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"⚠️ Failed to update language preference (attempt {attempt + 1}/{max_retries}): {e}")
                    await asyncio.sleep(1 * (attempt + 1))
                else:
                    logger.error(f"❌ Failed to update language preference after {max_retries} attempts: {e}")

    async def save_language_to_db(self, lang_code: str, conversation_store: Dict):
        """Save detected language to conversation store"""
        if not self.conversation_id_cache:
            logger.debug("No conversation_id available, skipping language save")
            return
        
        try:
            if self.conversation_id_cache in conversation_store:
                conversation_store[self.conversation_id_cache]['language'] = lang_code
                logger.info(f"💾 Saved language '{lang_code}' to conversation {self.conversation_id_cache}")
            else:
                logger.warning(f"⚠️ Conversation {self.conversation_id_cache} not found in store")
        except Exception as e:
            logger.error(f"❌ Failed to save language: {e}")

    async def respond(
        self, 
        human_input: str, 
        conversation_id: str, 
        is_interrupt: bool = False,
        conversation_store: Dict = None
    ) -> Tuple[Optional[str], bool]:
        """Main response handler with multilingual and booking support"""
        try:
            # Reset no-input counter on valid input
            if human_input and len(human_input.strip()) > 2:
                self.no_input_count = 0
                self.last_response_time = time.time()
            else:
                self.no_input_count += 1
            
            # Handle timeout
            if self.no_input_count >= 3:
                goodbye = "I haven't heard from you. I'll follow up later. Thank you!"
                if self.current_language != 'en':
                    goodbye = await self.translate_text(goodbye, self.current_language)
                return goodbye, True
            
            # Check for language switch request
            new_language = await self.detect_language_switch(human_input)
            if new_language and new_language != self.current_language:
                self.current_language = new_language
                await self.update_lead_language_preference(new_language)
                
                # Acknowledge language switch
                switch_msg = f"Sure, I'll continue in {LANGUAGE_MAP[new_language]}."
                switch_msg_translated = await self.translate_text(switch_msg, new_language)
                logger.info(f"Language switched to {new_language} for conversation {conversation_id}")
                
                # Store language in conversation data
                if conversation_store and conversation_id in conversation_store:
                    conversation_store[conversation_id]['language'] = new_language
                
                return switch_msg_translated, False
            
            # Booking Intent Detection
            booking_intent = await self.handle_booking_intent(human_input, conversation_id)
            
            if booking_intent and conversation_store and conversation_id in conversation_store:
                conv = conversation_store[conversation_id]
                lead_id = conv.get('lead_id')
                company_id = conv.get('company_id')
                
                if lead_id and company_id:
                    try:
                        booking_result = await self.create_booking_for_lead(
                            company_id=company_id,
                            lead_id=lead_id,
                            booking_data=booking_intent,
                            conversation_id=conversation_id
                        )
                        
                        if booking_result and booking_result.get('success'):
                            success_msg = f"Great! I've scheduled your {booking_intent.get('purpose', 'appointment')} for {booking_result.get('date_str', 'soon')}. You'll receive a confirmation email shortly."
                            
                            if self.current_language != 'en':
                                success_msg = await self.translate_text(success_msg, self.current_language)
                            
                            return success_msg, False
                        else:
                            fallback_msg = "I'd love to schedule that for you. Let me connect you with our team to find the best time."
                            if self.current_language != 'en':
                                fallback_msg = await self.translate_text(fallback_msg, self.current_language)
                            return fallback_msg, False
                            
                    except Exception as booking_error:
                        logger.error(f"Booking creation failed: {booking_error}")
                        fallback_msg = "I'm having trouble accessing the calendar. Let me connect you with our team."
                        if self.current_language != 'en':
                            fallback_msg = await self.translate_text(fallback_msg, self.current_language)
                        return fallback_msg, False

            # Translate user input to English if needed
            english_input = human_input
            if self.current_language != 'en':
                english_input = await self.translate_to_english(human_input, self.current_language)
                logger.debug(f"Translated input: {human_input[:50]}... → {english_input[:50]}...")
            
            try:
                response, should_end = await super().respond(english_input, conversation_id, is_interrupt)
            except Exception as llm_error:
                logger.error(f"❌ LLM generation error: {llm_error}")
                response = "I'm having trouble processing that. Could you rephrase?"
                should_end = False
                
            # Translate response to user's language if needed
            if self.current_language != 'en' and response:
                translated_response = await self.translate_text(response, self.current_language)
                logger.debug(f"Translated response: {response[:50]}... → {translated_response[:50]}...")
                return translated_response, should_end
            
            return response, should_end
            
        except Exception as e:
            logger.error(f"Agent response error: {e}")
            error_msg = "I'm having trouble processing that. Could you repeat?"
            if self.current_language != 'en':
                error_msg = await self.translate_text(error_msg, self.current_language)
            return error_msg, False

    async def _extract_datetime_from_text(self, text: str) -> Optional[datetime]:
        """Extract date and time from natural language text"""
        try:
            # Use dateparser to extract datetime
            parsed = dateparser.parse(
                text,
                settings={
                    'TIMEZONE': 'Asia/Kolkata',
                    'RETURN_AS_TIMEZONE_AWARE': True,
                    'PREFER_DATES_FROM': 'future'
                }
            )
            
            if parsed:
                # Convert to UTC
                utc_time = parsed.astimezone(timezone.utc)
                logger.info(f"Extracted datetime: {utc_time.isoformat()} from '{text}'")
                return utc_time
            
        except Exception as e:
            logger.debug(f"Could not extract datetime from '{text}': {e}")
        
        # Pattern: "tomorrow at 3pm", "monday at 10am"
        patterns = [
            r'(?:tomorrow|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\s+at\s+(\d{1,2})\s*(?:am|pm)?',
            r'(\d{1,2})\s*(?:am|pm)\s+(?:tomorrow|today)',
            r'(?:at\s+)?(\d{1,2}):?(\d{2})?\s*(am|pm)?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                # Simple fallback: tomorrow at extracted hour
                now = datetime.now(timezone.utc)
                tomorrow = now + timedelta(days=1)
                
                hour = int(match.group(1))
                if 'pm' in text.lower() and hour < 12:
                    hour += 12
                
                proposed = tomorrow.replace(hour=hour, minute=0, second=0, microsecond=0)
                logger.info(f"Basic extraction: {proposed.isoformat()} from '{text}'")
                return proposed
        
        return None

    async def _get_lead_email(self, lead_id: int) -> Optional[str]:
        """Get lead email from database"""
        if not lead_id:
            return None
        
        db_pool = get_db_pool()
        
        try:
            async with db_pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT email FROM leads WHERE id = $1",
                    lead_id
                )
                return row['email'] if row else None
        except Exception as e:
            logger.error(f"Failed to get lead email: {e}")
            return None

    async def handle_booking_intent(self, user_input: str, conversation_id: str) -> Optional[Dict]:
        """Detect if user wants to book an appointment and extract details"""
        booking_keywords = [
            'book', 'schedule', 'appointment', 'meeting', 'demo', 'call back',
            'book करना', 'मिलना', 'समय', 'appointment', 'ಸಭೆ', 'മീറ്റിംഗ്'
        ]
        
        if not any(keyword in user_input.lower() for keyword in booking_keywords):
            return None
        
        try:
            booking_prompt = PromptTemplate(
                input_variables=["user_input"],
                template="""Extract booking details from this text. Return ONLY valid JSON with no extra text:
{{
"wants_booking": true,
"preferred_date": "YYYY-MM-DD or null",
"preferred_time": "HH:MM or null",
"duration_minutes": 30,
"purpose": "demo"
}}

User said: "{user_input}"

JSON:"""
            )
            llm = ChatGroq(model_name="llama-3.1-8b-instant", api_key=GROQ_API_KEY)
            booking_chain = LLMChain(llm=llm, prompt=booking_prompt)
            
            result = await booking_chain.ainvoke({"user_input": user_input})
            result_text = result.get('text') if result else '{}'
            
            if not result_text:
                logger.warning("Empty result from booking chain")
                return None
            
            # Extract JSON safely
            start = result_text.find('{')
            end = result_text.rfind('}') + 1
            
            if start == -1 or end <= start:
                logger.warning(f"No JSON found in booking detection response")
                return None
            
            try:
                booking_data = json.loads(result_text[start:end])
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON from LLM: {e}")
                return None
            
            if booking_data.get('wants_booking'):
                return booking_data
            
            return None
            
        except Exception as e:
            logger.error(f"Booking intent detection failed: {e}", exc_info=True)
            return None

    async def create_booking_for_lead(
        self,
        company_id: int,
        lead_id: int,
        booking_data: Dict,
        conversation_id: str
    ) -> Optional[Dict]:
        """Create calendar booking and send confirmation email"""
        try:
            db_pool = get_db_pool()
            
            # Get active calendar config
            async with httpx.AsyncClient(timeout=10.0) as client:
                calendar_response = await client.get(
                    f"{CRM_API_URL}/calendar/active/{company_id}",
                    headers={"Authorization": f"Bearer {CRM_API_KEY}"}
                )
                
                if calendar_response.status_code != 200:
                    logger.warning(f"No active calendar for company {company_id}")
                    return None
                
                calendar_config = calendar_response.json()['data']
                calendar_config_id = calendar_config['calendar_config_id']
            
            # Get lead details
            async with db_pool.acquire() as conn:
                lead = await conn.fetchrow(
                    "SELECT name, email, phone_number FROM leads WHERE id = $1",
                    lead_id
                )
            
            if not lead:
                return None
            
            # Parse booking time
            preferred_date = booking_data.get('preferred_date')
            preferred_time = booking_data.get('preferred_time')
            
            # Default to next business day at 10 AM if not specified
            if not preferred_date:
                start_time = datetime.now(timezone.utc) + timedelta(days=1)
                start_time = start_time.replace(hour=10, minute=0, second=0, microsecond=0)
            else:
                start_time = datetime.fromisoformat(preferred_date)
                if preferred_time:
                    hour, minute = map(int, preferred_time.split(':'))
                    start_time = start_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
                else:
                    start_time = start_time.replace(hour=10, minute=0, second=0, microsecond=0)
            
            duration = booking_data.get('duration_minutes', 60)
            purpose = booking_data.get('purpose', 'consultation')
            
            # Create calendar event
            event_result = await create_calendar_appointment(
                calendar_config_id=calendar_config_id,
                lead_id=lead_id,
                title=f"{purpose.title()} with {lead['name'] or 'Customer'}",
                start_time=start_time,
                duration_minutes=duration,
                attendee_email=lead['email'],
                description=f"Booked via AI call. Conversation ID: {conversation_id}"
            )
            
            if event_result:
                logger.info(f"✅ Booking created for lead {lead_id}: {event_result['event_id']}")
                
                date_str = start_time.strftime("%B %d, %Y at %I:%M %p")
                
                return {
                    'success': True,
                    'event_id': event_result['event_id'],
                    'meeting_link': event_result.get('meeting_link'),
                    'date_str': date_str
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to create booking: {e}")
            return None