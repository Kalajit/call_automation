import asyncio
import os
from datetime import datetime, timezone
from twilio.rest import Client
from src.config.settings import (
    BASE_URL,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN
)
from src.database.companies import get_company_config
from src.database.call_logs import save_call_log, handle_call_failure
from src.utils.logging_config import get_logger

logger = get_logger(__name__)

# Available voice options
AVAILABLE_VOICES = ["Raveena", "Aditi", "Brian", "Matthew"]


async def make_outbound_call(
    company_id: int,
    lead_id: int,
    to_phone: str,
    name: str,
    call_type: str = "qualification",
    prompt_key: str = None,
    agent_instance_id: int = None,
    call_semaphore: asyncio.Semaphore = None,
    conversation_store: dict = None,
    active_calls: dict = None,
    metrics: dict = None
) -> str:
    """
    Make outbound call using agent-specific credentials (Twilio OAuth or SIP)
    """
    if call_semaphore:
        async with call_semaphore:
            return await _make_outbound_call_internal(
                company_id, lead_id, to_phone, name, call_type,
                prompt_key, agent_instance_id,
                conversation_store, active_calls, metrics
            )
    else:
        return await _make_outbound_call_internal(
            company_id, lead_id, to_phone, name, call_type,
            prompt_key, agent_instance_id,
            conversation_store, active_calls, metrics
        )


async def _make_outbound_call_internal(
    company_id: int,
    lead_id: int,
    to_phone: str,
    name: str,
    call_type: str,
    prompt_key: str,
    agent_instance_id: int,
    conversation_store: dict,
    active_calls: dict,
    metrics: dict
) -> str:
    """Internal implementation of outbound calling"""
    try:
        # Get agent config
        config = await get_company_config(company_id, prompt_key, agent_instance_id)
        if not config:
            raise ValueError(f"No config found for company {company_id}")
        
        company = config["company"]
        agent_cfg = config["agent"]
        agent_instance = config.get("agent_instance")
        
        if not agent_instance:
            raise ValueError(f"Agent instance {agent_instance_id} not found")
        
        # Prepare initial message
        initial_msg = agent_cfg["initial_message"].replace("{{name}}", name or "there")

        # Get voice from agent config
        agent_voice = agent_cfg.get("voice", "Brian")
        
        # Validate voice
        if agent_voice not in AVAILABLE_VOICES:
            logger.warning(f"Invalid voice '{agent_voice}', defaulting to Brian")
            agent_voice = "Brian"
        
        # Detect provider: Twilio OAuth or SIP
        sip_provider = agent_instance.get('sip_provider', 'twilio')
        
        if sip_provider == 'twilio' and agent_instance.get('twilio_credentials'):
            # TWILIO OAUTH
            twilio_creds = agent_instance['twilio_credentials']
            account_sid = twilio_creds.get('account_sid')
            auth_token = twilio_creds.get('auth_token')
            from_phone = agent_instance.get('phone_number') or twilio_creds.get('phone_number')
            
            if not account_sid or not auth_token or not from_phone:
                raise ValueError("Invalid Twilio credentials")
            
            client = Client(account_sid, auth_token)
            
            call = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: client.calls.create(
                    to=to_phone,
                    from_=from_phone,
                    url=f"https://{BASE_URL}/inbound_call",
                    status_callback=f"https://{BASE_URL}/call_status",
                    status_callback_method="POST",
                    status_callback_event=["initiated", "ringing", "answered", "completed"],
                    record=True,
                    recording_channels="dual",
                    recording_status_callback=f"https://{BASE_URL}/recording_status",
                    recording_status_callback_method="POST"
                )
            )
            
            call_sid = call.sid
            logger.info(f"📞 Twilio call initiated: {call_sid} via {from_phone}")
            
        elif sip_provider in ['airtel', 'custom'] and agent_instance.get('sip_credentials'):
            # AIRTEL/CUSTOM SIP
            sip_creds = agent_instance['sip_credentials']
            sip_domain = sip_creds.get('sip_domain')
            sip_username = sip_creds.get('sip_username')
            sip_password = sip_creds.get('sip_password')
            from_phone = sip_creds.get('did_number')
            
            if not all([sip_domain, sip_username, sip_password, from_phone]):
                raise ValueError("Invalid SIP credentials")
            
            # Use Twilio's SIP feature to route via Airtel
            fallback_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
            fallback_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
            
            if not fallback_account_sid or not fallback_auth_token:
                raise ValueError("System Twilio credentials not configured for SIP routing")
            
            client = Client(fallback_account_sid, fallback_auth_token)
            
            # Construct SIP URI
            sip_uri = f"sip:{to_phone}@{sip_domain};transport=udp"
            
            call = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: client.calls.create(
                    to=sip_uri,
                    from_=from_phone,
                    url=f"https://{BASE_URL}/inbound_call",
                    status_callback=f"https://{BASE_URL}/call_status",
                    status_callback_method="POST",
                    status_callback_event=["initiated", "ringing", "answered", "completed"],
                    record=True,
                    send_digits="wwww1234#"
                )
            )
            
            call_sid = call.sid
            logger.info(f"📞 SIP call initiated: {call_sid} via {sip_provider} ({from_phone})")
            
        else:
            raise ValueError(f"No valid credentials found for agent {agent_instance_id}. Please configure Twilio OAuth or SIP credentials.")
        
        # Store conversation context
        if conversation_store is not None:
            conversation_store[call_sid] = {
                "call_sid": call_sid,
                "company_id": company_id,
                "lead_id": lead_id,
                "to_phone": to_phone,
                "from_phone": from_phone,
                "name": name,
                "call_type": call_type,
                "prompt_key": prompt_key,
                "agent_instance_id": agent_instance_id,
                "agent_name": agent_instance['agent_name'],
                "sip_provider": sip_provider,
                "started_at": datetime.now(timezone.utc).isoformat(),
                "language": "en"
            }
        
        if active_calls is not None and conversation_store is not None:
            active_calls[call_sid] = conversation_store[call_sid]
        
        # Save call log
        await save_call_log(
            call_sid=call_sid,
            company_id=company_id,
            lead_id=lead_id,
            to_phone=to_phone,
            from_phone=from_phone,
            call_type=call_type,
            call_status="initiated"
        )
        
        if metrics:
            metrics["calls_initiated"][call_type] += 1
        
        return call_sid
        
    except Exception as e:
        logger.error(f"Failed to make call: {e}", exc_info=True)
        
        if metrics:
            metrics["errors"]["call_initiation"] += 1

        await handle_call_failure(
            company_id=company_id,
            lead_id=lead_id,
            to_phone=to_phone,
            from_phone=agent_instance.get('phone_number') if agent_instance else "unknown",
            call_type=call_type,
            error_message=str(e),
            metrics=metrics
        )
        
        raise