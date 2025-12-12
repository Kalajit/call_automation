import httpx
from typing import Optional, Dict, List
from datetime import datetime, timedelta
from src.config.settings import CRM_API_URL, CRM_API_KEY
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


async def create_calendar_appointment(
    calendar_config_id: int,
    lead_id: int,
    title: str,
    start_time: datetime,
    duration_minutes: int = 60,
    attendee_email: str = None,
    description: str = None
) -> Optional[Dict]:
    """
    Create calendar appointment via CRM API
    """
    try:
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        attendees = [attendee_email] if attendee_email else []
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{CRM_API_URL}/calendar/create-event",
                json={
                    "calendar_config_id": calendar_config_id,
                    "lead_id": lead_id,
                    "title": title,
                    "description": description,
                    "start_time": start_time.isoformat(),
                    "end_time": end_time.isoformat(),
                    "attendees": attendees,
                    "send_confirmation": True  # Enable auto email
                },
                headers={"Authorization": f"Bearer {CRM_API_KEY}"}
            )
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"✅ Calendar event created: {result.get('data', {}).get('event_id')}")
            return result.get('data')
            
    except Exception as e:
        logger.error(f"Failed to create calendar event: {e}")
        return None


async def check_calendar_availability_for_call(
    calendar_config_id: int,
    proposed_time: datetime,
    duration_minutes: int = 60
) -> Dict:
    """
    Check if a time slot is available in the calendar
    Returns: {"available": bool, "busy_slots": [], "alternative_slots": []}
    """
    try:
        end_time = proposed_time + timedelta(minutes=duration_minutes)
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{CRM_API_URL}/calendar/check-availability",
                json={
                    "calendar_config_id": calendar_config_id,
                    "start_time": proposed_time.isoformat(),
                    "end_time": end_time.isoformat()
                },
                headers={"Authorization": f"Bearer {CRM_API_KEY}"}
            )
            response.raise_for_status()
            result = response.json()
            
            return result.get('data', {})
            
    except Exception as e:
        logger.error(f"Failed to check calendar availability: {e}")
        return {"available": False, "error": str(e)}


async def get_available_slots_for_call(
    calendar_config_id: int,
    start_date: datetime,
    days_ahead: int = 7,
    duration_minutes: int = 60
) -> List[Dict]:
    """
    Get available time slots for next N days
    """
    try:
        end_date = start_date + timedelta(days=days_ahead)
        
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                f"{CRM_API_URL}/calendar/available-slots",
                json={
                    "calendar_config_id": calendar_config_id,
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "duration_minutes": duration_minutes,
                    "buffer_minutes": 15
                },
                headers={"Authorization": f"Bearer {CRM_API_KEY}"}
            )
            response.raise_for_status()
            result = response.json()
            
            return result.get('data', {}).get('available_slots', [])
            
    except Exception as e:
        logger.error(f"Failed to get available slots: {e}")
        return []


async def get_active_calendar_config(company_id: int) -> Optional[Dict]:
    """
    Get active calendar configuration for a company
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{CRM_API_URL}/calendar/active/{company_id}",
                headers={"Authorization": f"Bearer {CRM_API_KEY}"}
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get('success'):
                return result.get('data')
            else:
                logger.warning(f"No active calendar for company {company_id}")
                return None
            
    except Exception as e:
        logger.error(f"Failed to get active calendar: {e}")
        return None