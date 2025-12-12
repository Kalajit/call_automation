from fastapi import APIRouter, HTTPException
from src.database.connection import get_db_pool
from src.utils.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api", tags=["admin"])


@router.post("/companies")
async def create_company(name: str, phone_number: str):
    """
    Create a new company (multi-tenant)
    
    Module 1 Requirement: Multi-tenant support
    """
    try:
        db_pool = get_db_pool()
        async with db_pool.acquire() as conn:
            company_id = await conn.fetchval("""
                INSERT INTO companies (name, phone_number)
                VALUES ($1, $2)
                RETURNING id
            """, name, phone_number)
            
            return {
                "success": True,
                "company_id": company_id
            }
            
    except Exception as e:
        logger.error(f"Create company failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agent-configs")
async def create_agent_config(
    company_id: int,
    prompt_key: str,
    prompt_preamble: str,
    initial_message: str,
    voice: str = "Brian",
    model_name: str = "llama-3.1-8b-instant"
):
    """
    Create/update agent configuration
    
    Module 1 Requirement: Customizable AI agents per company
    """
    try:
        db_pool = get_db_pool()
        async with db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO agent_configs 
                (company_id, prompt_key, prompt_preamble, initial_message, voice, model_name)
                VALUES ($1, $2, $3, $4, $5, $6)
                ON CONFLICT (company_id, prompt_key) DO UPDATE SET
                    prompt_preamble = EXCLUDED.prompt_preamble,
                    initial_message = EXCLUDED.initial_message,
                    voice = EXCLUDED.voice,
                    model_name = EXCLUDED.model_name,
                    updated_at = CURRENT_TIMESTAMP
            """, company_id, prompt_key, prompt_preamble, initial_message, voice, model_name)
            
            return {
                "success": True,
                "message": "Agent config saved"
            }
            
    except Exception as e:
        logger.error(f"Create agent config failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agent-configs/{company_id}")
async def get_agent_configs(company_id: int):
    """Get all agent configs for a company"""
    try:
        db_pool = get_db_pool()
        async with db_pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM agent_configs WHERE company_id = $1 AND is_active = TRUE",
                company_id
            )
            return [dict(row) for row in rows]
            
    except Exception as e:
        logger.error(f"Get agent configs failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))