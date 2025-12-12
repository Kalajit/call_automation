import httpx
from typing import Dict
from src.config.settings import CRM_API_URL, CRM_API_KEY
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


async def update_crm(lead_id: int, call_data: Dict, metrics: Dict):
    """Update external CRM via API"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{CRM_API_URL}/webhook/call-completed",
                json=call_data,
                headers={"Authorization": f"Bearer {CRM_API_KEY}"}
            )
            response.raise_for_status()
            logger.info(f"CRM updated for lead {lead_id}")
    except Exception as e:
        logger.error(f"CRM update failed: {e}")
        metrics["errors"]["crm_update_failed"] += 1