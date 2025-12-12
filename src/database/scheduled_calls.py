from typing import List, Dict, Optional
from src.database.connection import get_db_pool
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


async def get_pending_scheduled_calls() -> List[Dict]:
    """Fetch pending scheduled calls"""
    db_pool = get_db_pool()
    
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT sc.*, l.phone_number, l.name, l.email, l.company_id,
                   ac.prompt_key, ac.voice, ac.initial_message
            FROM scheduled_calls sc
            JOIN leads l ON sc.lead_id = l.id
            JOIN agent_configs ac ON sc.company_id = ac.company_id
            WHERE sc.status = 'pending' 
            AND sc.scheduled_time <= CURRENT_TIMESTAMP
            AND sc.retry_count < 3
            ORDER BY sc.scheduled_time ASC
            LIMIT 50
        """)
        return [dict(row) for row in rows]


async def update_scheduled_call(
    scheduled_id: int, 
    status: str, 
    call_sid: str = None
):
    """Update scheduled call status"""
    db_pool = get_db_pool()
    
    async with db_pool.acquire() as conn:
        if status == "called":
            await conn.execute("""
                UPDATE scheduled_calls 
                SET status = $1, call_sid = $2, updated_at = CURRENT_TIMESTAMP
                WHERE id = $3
            """, status, call_sid, scheduled_id)
        elif status == "failed":
            await conn.execute("""
                UPDATE scheduled_calls 
                SET status = $1, retry_count = retry_count + 1, 
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = $2
            """, status, scheduled_id)
        else:
            await conn.execute("""
                UPDATE scheduled_calls 
                SET status = $1, updated_at = CURRENT_TIMESTAMP
                WHERE id = $2
            """, status, scheduled_id)