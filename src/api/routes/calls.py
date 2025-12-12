from fastapi import APIRouter, HTTPException, BackgroundTasks
from datetime import datetime, timezone
from src.api.models import OutboundCallRequest, ScheduleCallRequest
from src.calling.outbound import make_outbound_call
from src.database.connection import get_db_pool
from src.utils.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api", tags=["calls"])


def setup_calls_routes(conversation_store: dict, active_calls: dict, metrics: dict, call_semaphore):
    """Setup call routes with dependencies"""
    
    @router.post("/outbound-call")
    async def trigger_outbound_call(req: OutboundCallRequest, background_tasks: BackgroundTasks):
        """
        Trigger immediate outbound call
        
        Module 1 Requirement: Outbound calling API
        """
        try:
            call_sid = await make_outbound_call(
                company_id=req.company_id,
                lead_id=req.lead_id,
                to_phone=req.to_phone,
                name=req.name,
                call_type=req.call_type,
                prompt_key=req.prompt_config_key,
                call_semaphore=call_semaphore,
                conversation_store=conversation_store,
                active_calls=active_calls,
                metrics=metrics
            )
            
            return {
                "success": True,
                "call_sid": call_sid,
                "message": "Call initiated"
            }
            
        except Exception as e:
            logger.error(f"Outbound call failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/outbound-call-agent")
    async def trigger_outbound_call_with_agent(
        req: OutboundCallRequest, 
        agent_instance_id: int, 
        background_tasks: BackgroundTasks
    ):
        """
        Trigger outbound call with specific agent instance
        
        NEW ENDPOINT for CloserX-like agent support
        """
        try:
            call_sid = await make_outbound_call(
                company_id=req.company_id,
                lead_id=req.lead_id,
                to_phone=req.to_phone,
                name=req.name,
                call_type=req.call_type,
                prompt_key=req.prompt_config_key,
                agent_instance_id=agent_instance_id,
                call_semaphore=call_semaphore,
                conversation_store=conversation_store,
                active_calls=active_calls,
                metrics=metrics
            )
            
            return {
                "success": True,
                "call_sid": call_sid,
                "agent_instance_id": agent_instance_id,
                "message": "Call initiated with agent instance"
            }
            
        except Exception as e:
            logger.error(f"Outbound call with agent failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/schedule-call")
    async def schedule_call(req: ScheduleCallRequest):
        """
        Schedule a call for later execution
        
        Module 1 Requirement: Scheduled calling
        """
        try:
            db_pool = get_db_pool()
            async with db_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO scheduled_calls 
                    (company_id, lead_id, call_type, scheduled_time)
                    VALUES ($1, $2, $3, $4)
                """, req.company_id, req.lead_id, req.call_type, 
                    datetime.fromisoformat(req.scheduled_time.replace('Z', '+00:00'))
                )
            
            return {
                "success": True,
                "message": "Call scheduled"
            }
            
        except Exception as e:
            logger.error(f"Schedule call failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/call-logs/{call_sid}")
    async def get_call_log(call_sid: str):
        """
        Get call log details
        
        Module 1 Requirement: Call history access
        """
        try:
            db_pool = get_db_pool()
            async with db_pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT * FROM call_logs WHERE call_sid = $1",
                    call_sid
                )
                
                if not row:
                    raise HTTPException(status_code=404, detail="Call not found")
                
                return dict(row)
                
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Get call log failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/call-logs/lead/{lead_id}")
    async def get_lead_call_logs(lead_id: int, limit: int = 50):
        """
        Get all call logs for a lead
        
        Module 1 Requirement: Lead call history
        """
        try:
            db_pool = get_db_pool()
            async with db_pool.acquire() as conn:
                rows = await conn.fetch("""
                    SELECT * FROM call_logs 
                    WHERE lead_id = $1 
                    ORDER BY created_at DESC 
                    LIMIT $2
                """, lead_id, limit)
                
                return [dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Get lead calls failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/active-calls")
    async def get_active_calls():
        """Get list of currently active calls"""
        return {
            "count": len(active_calls),
            "calls": [
                {
                    "call_sid": call_sid,
                    "to_phone": data.get("to_phone"),
                    "name": data.get("name"),
                    "call_type": data.get("call_type"),
                    "started_at": data.get("started_at")
                }
                for call_sid, data in active_calls.items()
            ]
        }
    
    return router