from fastapi import APIRouter
from datetime import datetime, timezone
from src.database.connection import get_db_pool
from src.utils.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api", tags=["metrics"])


def setup_metrics_routes(active_calls: dict, metrics: dict):
    """Setup metrics routes with dependencies"""
    
    @router.get("/metrics")
    async def get_metrics():
        """
        Get system metrics
        
        Module 1 Requirement: Reporting & analytics
        """
        return {
            "calls_initiated": dict(metrics["calls_initiated"]),
            "calls_completed": dict(metrics["calls_completed"]),
            "calls_failed": dict(metrics["calls_failed"]),
            "sentiment_distribution": dict(metrics["sentiment_distribution"]),
            "routing_decisions": dict(metrics["routing_decisions"]),
            "errors": dict(metrics["errors"]),
            "avg_call_duration_seconds": round(metrics["avg_call_duration"], 2),
            "total_recordings": metrics["total_recordings"],
            "active_calls": len(active_calls),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    @router.get("/health")
    async def health_check():
        """Health check endpoint"""
        db_pool = get_db_pool()
        return {
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "active_calls": len(active_calls),
            "db_connected": db_pool is not None
        }
    
    return router