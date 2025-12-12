from datetime import datetime
from typing import Optional
from src.database.connection import get_db_pool
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


async def update_lead_status(
    lead_id: int, 
    status: str, 
    last_contacted: datetime = None
):
    """Update lead status after call"""
    db_pool = get_db_pool()
    
    async with db_pool.acquire() as conn:
        await conn.execute("""
            UPDATE leads 
            SET lead_status = $1,
                last_contacted = COALESCE($2, CURRENT_TIMESTAMP),
                updated_at = CURRENT_TIMESTAMP
            WHERE id = $3
        """, status, last_contacted, lead_id)