import asyncio
from src.database.scheduled_calls import get_pending_scheduled_calls, update_scheduled_call
from src.calling.outbound import make_outbound_call
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


async def outbound_call_scheduler(
    conversation_store: dict,
    active_calls: dict,
    metrics: dict,
    call_semaphore: asyncio.Semaphore
):
    """Poll database for scheduled calls and execute them"""
    logger.info("🚀 Starting outbound call scheduler")
    
    while True:
        try:
            # Fetch pending calls
            pending_calls = await get_pending_scheduled_calls()
            
            logger.debug(f"Scheduler: {len(pending_calls)} pending calls")
            
            for call_data in pending_calls:
                try:
                    #Make Call
                    call_sid= await make_outbound_call(
                        company_id=call_data["company_id"],
                        lead_id=call_data["lead_id"],
                        to_phone=call_data["phone_number"],
                        name=call_data["name"],
                        call_type=call_data["call_type"],
                        prompt_key=call_data["prompt_key"],
                        call_semaphore=call_semaphore,
                        conversation_store=conversation_store,
                        active_calls=active_calls,
                        metrics=metrics
                    )

                    # Update scheduled call status
                    await update_scheduled_call(call_data["id"], "called", call_sid)
                    
                    logger.info(f"✅ Scheduled call executed: {call_sid}")


                except Exception as e:
                    logger.error(f"Failed to execute scheduled call {call_data['id']}: {e}")   

                    await update_scheduled_call(call_data["id"], "failed")
                    if metrics:
                        metrics["calls_failed"][call_data["call_type"]] += 1
                
                # Rate limiting between calls
                await asyncio.sleep(2)

            # Poll every 30 seconds
            await asyncio.sleep(30)


        except Exception as e:
            logger.error(f"Scheduler error: {e}", exc_info=True)
            await asyncio.sleep(30)