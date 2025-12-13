from typing import Dict
from collections import defaultdict
from datetime import datetime, timezone


class MetricsTracker:
    """
    Centralized metrics tracking
    """
    
    def __init__(self):
        self.metrics = {
            "calls_initiated": defaultdict(int),
            "calls_completed": defaultdict(int),
            "calls_failed": defaultdict(int),
            "sentiment_distribution": defaultdict(int),
            "routing_decisions": defaultdict(int),
            "errors": defaultdict(int),
            "avg_call_duration": 0,
            "total_recordings": 0,
            "total_calls": 0,
            "successful_transfers": 0,
            "failed_transfers": 0
        }
        self.call_durations = []
    
    def increment_calls_initiated(self, call_type: str):
        """Increment calls initiated counter"""
        self.metrics["calls_initiated"][call_type] += 1
        self.metrics["total_calls"] += 1
    
    def increment_calls_completed(self, call_type: str):
        """Increment calls completed counter"""
        self.metrics["calls_completed"][call_type] += 1
    
    def increment_calls_failed(self, call_type: str):
        """Increment calls failed counter"""
        self.metrics["calls_failed"][call_type] += 1
    
    def record_sentiment(self, sentiment: str):
        """Record sentiment distribution"""
        self.metrics["sentiment_distribution"][sentiment] += 1
    
    def record_routing_decision(self, decision: str):
        """Record routing decision"""
        self.metrics["routing_decisions"][decision] += 1
    
    def record_error(self, error_type: str):
        """Record error"""
        self.metrics["errors"][error_type] += 1
    
    def record_call_duration(self, duration: int):
        """Record call duration and update average"""
        if duration > 0:
            self.call_durations.append(duration)
            self.metrics["avg_call_duration"] = sum(self.call_durations) / len(self.call_durations)
    
    def increment_recordings(self):
        """Increment total recordings counter"""
        self.metrics["total_recordings"] += 1
    
    def increment_successful_transfer(self):
        """Increment successful transfer counter"""
        self.metrics["successful_transfers"] += 1
        self.metrics["routing_decisions"]["call_transferred"] += 1
    
    def increment_failed_transfer(self):
        """Increment failed transfer counter"""
        self.metrics["failed_transfers"] += 1
        self.metrics["errors"]["call_transfer_execution"] += 1
    
    def get_metrics_summary(self) -> Dict:
        """Get complete metrics summary"""
        return {
            "calls_initiated": dict(self.metrics["calls_initiated"]),
            "calls_completed": dict(self.metrics["calls_completed"]),
            "calls_failed": dict(self.metrics["calls_failed"]),
            "sentiment_distribution": dict(self.metrics["sentiment_distribution"]),
            "routing_decisions": dict(self.metrics["routing_decisions"]),
            "errors": dict(self.metrics["errors"]),
            "avg_call_duration_seconds": round(self.metrics["avg_call_duration"], 2),
            "total_recordings": self.metrics["total_recordings"],
            "total_calls": self.metrics["total_calls"],
            "successful_transfers": self.metrics["successful_transfers"],
            "failed_transfers": self.metrics["failed_transfers"],
            "success_rate": self._calculate_success_rate(),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    def _calculate_success_rate(self) -> float:
        """Calculate call success rate"""
        total_completed = sum(self.metrics["calls_completed"].values())
        total_initiated = sum(self.metrics["calls_initiated"].values())
        
        if total_initiated == 0:
            return 0.0
        
        return round((total_completed / total_initiated) * 100, 2)
    
    def reset_metrics(self):
        """Reset all metrics (for testing or periodic resets)"""
        self.__init__()