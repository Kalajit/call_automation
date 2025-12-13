from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, Request
from datetime import datetime, timezone
from src.api.models import OutboundCallRequest, ScheduleCallRequest
from src.calling.outbound import make_outbound_call
from src.database.connection import get_db_pool
from src.utils.logging_config import get_logger
from src.utils.security import get_current_user, verify_company_access
from src.utils.rate_limiter import check_rate_limit

logger = get_logger(__name__)

router = APIRouter(prefix="/api", tags=["calls"])


def setup_calls_routes(conversation_store: dict, active_calls: dict, metrics: dict, call_semaphore):
    """Setup call routes with dependencies"""
    
    @router.post("/outbound-call")
    async def trigger_outbound_call(
        req: OutboundCallRequest,
        background_tasks: BackgroundTasks,
        request: Request,
        current_user: dict = Depends(get_current_user),
        _rate_limit: bool = Depends(check_rate_limit)
    ):
        """
        Trigger immediate outbound call
        
        Module 1 Requirement: Outbound calling API
        """
        try:

            # Verify user has access to this company
            verify_company_access(current_user, req.company_id)
            
            # Log authenticated request
            logger.info(
                f"Outbound call initiated by user {current_user['user_id']} "
                f"for company {req.company_id}, lead {req.lead_id}"
            )
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
                "message": "Call initiated",
                "authenticated_user": current_user["user_id"]
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Outbound call failed: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/outbound-call-agent")
    async def trigger_outbound_call_with_agent(
        req: OutboundCallRequest, 
        agent_instance_id: int,
        background_tasks: BackgroundTasks,
        request: Request,
        current_user: dict = Depends(get_current_user),
        _rate_limit: bool = Depends(check_rate_limit)
    ):
        """
        Trigger outbound call with specific agent instance
        
        NEW ENDPOINT for CloserX-like agent support
        """
        try:
            # Verify user has access to this company
            verify_company_access(current_user, req.company_id)
            
            # Log authenticated request
            logger.info(
                f"Outbound call with agent {agent_instance_id} initiated by user {current_user['user_id']} "
                f"for company {req.company_id}, lead {req.lead_id}"
            )

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
                "message": "Call initiated with agent instance",
                "authenticated_user": current_user["user_id"]
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Outbound call with agent failed: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/schedule-call")
    async def schedule_call(
        req: ScheduleCallRequest,
        current_user: dict = Depends(get_current_user)
    ):
        """
        Schedule a call for later execution
        
        Module 1 Requirement: Scheduled calling
        """
        try:
            # Verify user has access to this company
            verify_company_access(current_user, req.company_id)
            
            logger.info(
                f"Call scheduled by user {current_user['user_id']} "
                f"for company {req.company_id}, lead {req.lead_id}"
            )

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
                "message": "Call scheduled",
                "authenticated_user": current_user["user_id"]
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Schedule call failed: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/call-logs/{call_sid}")
    async def get_call_log(
        call_sid: str,
        current_user: dict = Depends(get_current_user)
    ):
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
                
                # Verify user has access to this call's company
                call_company_id = row["company_id"]
                verify_company_access(current_user, call_company_id)
                
                return dict(row)
                
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Get call log failed: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/call-logs/lead/{lead_id}")
    async def get_lead_call_logs(
        lead_id: int,
        limit: int = 50,
        current_user: dict = Depends(get_current_user)
    ):
        """
        Get all call logs for a lead
        
        Module 1 Requirement: Lead call history
        """
        try:
            db_pool = get_db_pool()
            async with db_pool.acquire() as conn:
                # First, verify the lead belongs to user's company
                lead_row = await conn.fetchrow(
                    "SELECT company_id FROM leads WHERE id = $1",
                    lead_id
                )
                
                if not lead_row:
                    raise HTTPException(status_code=404, detail="Lead not found")
                
                verify_company_access(current_user, lead_row["company_id"])
                
                # Fetch call logs
                rows = await conn.fetch("""
                    SELECT * FROM call_logs 
                    WHERE lead_id = $1 
                    ORDER BY created_at DESC 
                    LIMIT $2
                """, lead_id, limit)
                
                return [dict(row) for row in rows]
                
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Get lead calls failed: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/active-calls")
    async def get_active_calls(current_user: dict = Depends(get_current_user)):
        """Get list of currently active calls"""
        try:
            user_company_id = current_user.get("company_id")
            is_admin = current_user.get("role") == "admin"
            is_service = current_user.get("role") == "service"
            
            # Filter calls by company (unless admin/service)
            filtered_calls = []
            for call_sid, data in active_calls.items():
                call_company_id = data.get("company_id")
                
                # Show all calls to admin/service, or only company's calls to regular users
                if is_admin or is_service or call_company_id == user_company_id:
                    filtered_calls.append({
                        "call_sid": call_sid,
                        "to_phone": data.get("to_phone"),
                        "name": data.get("name"),
                        "call_type": data.get("call_type"),
                        "started_at": data.get("started_at"),
                        "company_id": call_company_id
                    })
            
            return {
                "count": len(filtered_calls),
                "calls": filtered_calls
            }
            
        except Exception as e:
            logger.error(f"Get active calls failed: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))
    
    return router