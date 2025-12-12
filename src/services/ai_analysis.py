import json
import asyncio
import httpx
from typing import Dict
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import LLMChain
from twilio.rest import Client
from src.config.settings import (
    GROQ_API_KEY, 
    TWILIO_ACCOUNT_SID, 
    TWILIO_AUTH_TOKEN,
    BASE_URL,
    CRM_API_URL,
    CRM_API_KEY
)
from src.utils.logging_config import get_logger

logger = get_logger(__name__)

# Initialize LLM
llm = ChatGroq(model_name="llama-3.1-8b-instant", api_key=GROQ_API_KEY)

# ============================================
# SENTIMENT ANALYSIS
# ============================================

sentiment_prompt = PromptTemplate(
    input_variables=["transcript"],
    template="""Analyze the sentiment of this call transcript and return ONLY a JSON object:
{
  "sentiment": "positive|neutral|negative|angry|confused",
  "tone_score": 1-10,
  "customer_emotion": "satisfied|frustrated|interested|uncertain",
  "urgency_level": "low|medium|high"
}

Transcript:
{transcript}

JSON:"""
)
sentiment_chain = LLMChain(llm=llm, prompt=sentiment_prompt)


async def analyze_sentiment(transcript: str, metrics: Dict) -> Dict:
    """Analyze call sentiment using LLM"""
    try:
        result = await sentiment_chain.ainvoke({"transcript": transcript})
        text = result.get('text', '{}')
        
        # Extract JSON from response
        start = text.find('{')
        end = text.rfind('}') + 1
        if start != -1 and end > start:
            text = text[start:end]
        
        sentiment = json.loads(text)
        
        # Update metrics
        metrics["sentiment_distribution"][sentiment.get("sentiment", "unknown")] += 1
        
        return sentiment
    except Exception as e:
        logger.error(f"Sentiment analysis failed: {e}")
        return {
            "sentiment": "neutral",
            "tone_score": 5,
            "customer_emotion": "unknown",
            "urgency_level": "medium"
        }


# ============================================
# SUMMARY GENERATION
# ============================================

summary_prompt = PromptTemplate(
    input_variables=["transcript"],
    template="""Generate a call summary and return ONLY a JSON object:
{
  "summary": "Brief 2-3 sentence summary",
  "intent": "interested|support|reminder|payment|information",
  "next_actions": ["action1", "action2"],
  "key_points": ["point1", "point2"],
  "customer_concerns": ["concern1"],
  "follow_up_required": true|false,
  "recommended_action": "specific action to take"
}

Transcript:
{transcript}

JSON:"""
)
summary_chain = LLMChain(llm=llm, prompt=summary_prompt)


async def generate_summary(transcript: str) -> Dict:
    """Generate call summary using LLM"""
    try:
        result = await summary_chain.ainvoke({"transcript": transcript})
        text = result.get('text', '{}')
        
        # Extract JSON
        start = text.find('{')
        end = text.rfind('}') + 1
        if start != -1 and end > start:
            text = text[start:end]
        
        summary = json.loads(text)
        return summary
    except Exception as e:
        logger.error(f"Summary generation failed: {e}")
        return {
            "summary": "Call completed",
            "intent": "unknown",
            "next_actions": [],
            "key_points": [],
            "customer_concerns": [],
            "follow_up_required": False,
            "recommended_action": "Review manually"
        }


# ============================================
# ROUTING LOGIC
# ============================================

async def route_based_on_sentiment(
    sentiment: Dict, 
    lead_id: int,
    metrics: Dict
) -> str:
    """Route call to appropriate team based on sentiment"""
    sentiment_type = sentiment.get("sentiment", "neutral")
    urgency = sentiment.get("urgency_level", "medium")
    tone_score = sentiment.get("tone_score", 5)
    
    # Routing logic
    if sentiment_type == "angry" or tone_score <= 3:
        team = "senior_support"
        metrics["routing_decisions"]["angry_escalation"] += 1
    elif sentiment_type == "confused" or urgency == "high":
        team = "specialist"
        metrics["routing_decisions"]["specialist_required"] += 1
    elif sentiment_type == "positive" and tone_score >= 8:
        team = "sales_closer"
        metrics["routing_decisions"]["hot_lead"] += 1
    else:
        team = "general_sales"
        metrics["routing_decisions"]["standard"] += 1
    
    # Log routing decision
    logger.info(f"Lead {lead_id} routed to {team} (sentiment={sentiment_type}, score={tone_score})")
    
    return team


# ============================================
# CALL TRANSFER LOGIC
# ============================================

async def check_call_transfer_criteria(
    sentiment: Dict, 
    summary: Dict, 
    lead_id: int, 
    call_sid: str,
    conversation_store: Dict,
    metrics: Dict
) -> bool:
    """
    Check if call should be transferred to human
    
    Criteria:
    - Angry customer (sentiment score < 3)
    - High value lead (intent = interested + tone_score >= 8)
    - Confused customer (asks for human 2+ times)
    - Customer explicitly requests human
    """
    should_transfer = False
    trigger_reason = None
    priority = 'medium'
    
    sentiment_type = sentiment.get('sentiment', 'neutral')
    tone_score = sentiment.get('tone_score', 5)
    intent = summary.get('intent', 'unknown')
    
    # 1. Angry customer
    if sentiment_type == 'angry' or tone_score <= 3:
        should_transfer = True
        trigger_reason = 'angry_customer'
        priority = 'urgent'
    
    # 2. High value lead
    elif intent == 'interested' and tone_score >= 8:
        should_transfer = True
        trigger_reason = 'high_value'
        priority = 'high'
    
    # 3. Confused customer (check conversation history)
    elif sentiment_type == 'confused':
        if call_sid in conversation_store:
            context = conversation_store[call_sid].get('conversation_context', '')
            if context.lower().count('human') >= 2 or context.lower().count('manager') >= 1:
                should_transfer = True
                trigger_reason = 'confused'
                priority = 'high'
    
    # 4. Explicit request for human
    if call_sid in conversation_store:
        context = conversation_store[call_sid].get('conversation_context', '')
        human_keywords = ['speak to human', 'talk to person', 'real person', 'manager', 'supervisor']
        if any(keyword in context.lower() for keyword in human_keywords):
            should_transfer = True
            trigger_reason = 'manual_request'
            priority = 'high'
    
    if should_transfer:
        logger.info(f"🚨 Call transfer criteria met: {trigger_reason} (priority: {priority})")
        
        # Create takeover request via API
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{CRM_API_URL}/takeover/request",
                    json={
                        "lead_id": lead_id,
                        "call_sid": call_sid,
                        "request_type": "call_transfer",
                        "trigger_reason": trigger_reason,
                        "ai_sentiment": sentiment,
                        "ai_summary": summary.get('summary'),
                        "conversation_context": conversation_store.get(call_sid, {}).get('conversation_context', ''),
                        "priority": priority
                    },
                    headers={"Authorization": f"Bearer {CRM_API_KEY}"}
                )
                response.raise_for_status()
                result = response.json()
                
                if result.get('success') and result.get('agent'):
                    agent = result['agent']
                    logger.info(f"✅ Call transfer request created, assigned to {agent['name']}")
                    
                    # Transfer call to agent's number
                    await transfer_call_to_human(call_sid, agent['phone'], agent['name'], metrics)
                    return True
                else:
                    logger.warning("⚠️ No agent available for call transfer")
                    return False
                
        except Exception as e:
            logger.error(f"Failed to create call transfer request: {e}")
            metrics["errors"]["call_transfer_failed"] += 1
            return False
    
    return False


async def transfer_call_to_human(
    call_sid: str, 
    agent_phone: str, 
    agent_name: str,
    metrics: Dict
):
    """Transfer Twilio call to human agent"""
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # Update call with <Dial>
        await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: client.calls(call_sid).update(
                twiml=f'''
                <Response>
                    <Say voice="Polly.Raveena">
                        Please hold while I connect you to {agent_name}.
                    </Say>
                    <Dial timeout="30" action="{BASE_URL}/dial_status">
                        <Number>{agent_phone}</Number>
                    </Dial>
                </Response>
                '''
            )
        )
        
        logger.info(f"📞 Call {call_sid} transferred to {agent_name} ({agent_phone})")
        metrics["routing_decisions"]["call_transferred"] += 1
        
    except Exception as e:
        logger.error(f"Call transfer failed: {e}")
        metrics["errors"]["call_transfer_execution"] += 1