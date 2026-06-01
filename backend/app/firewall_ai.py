"""
Firewall AI Service
Background monitoring and protection system
Detects threats, maintains system health, and prevents learning drift
"""

import hashlib
import json
import os
import time
from typing import Dict, Optional, List
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from .db import engine
from .models import (
    SystemHealth, FirewallThreat, FirewallLog, LearningDriftDetector,
    LearningPattern, AITask, User,
)
from .auth import get_current_user

router = APIRouter(prefix="/api/firewall")


class FirewallAI:
    """Background security and health monitoring."""

    THREAT_RULES = [
        {
            "name": "malicious_keywords",
            "keywords": ["sql injection", "xss", "csrf", "exploit", "hack"],
            "type": "malicious_content",
        },
        {
            "name": "privacy_violations",
            "keywords": ["credit card", "ssn", "password", "private key", "api key"],
            "type": "privacy_violation",
        },
        {
            "name": "abuse_patterns",
            "keywords": ["spam", "phishing", "scam", "fraud"],
            "type": "attack",
        },
    ]

    def __init__(self):
        self.threat_severity_scores = {
            "low": 1,
            "medium": 5,
            "high": 10,
            "critical": 20,
        }
        self.total_threat_score = 0

    async def monitor_system_health(self) -> SystemHealth:
        """Monitor and record system health metrics."""
        try:
            cpu_usage = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")
            db_path = os.path.join(os.path.dirname(__file__), "..", "alitiora.db")
            db_size_mb = os.path.getsize(db_path) / (1024 * 1024) if os.path.exists(db_path) else 0.0

            if cpu_usage > 80 or memory.percent > 85 or disk.percent > 90:
                health_status = "critical"
            elif cpu_usage > 60 or memory.percent > 70 or disk.percent > 75:
                health_status = "warning"
            else:
                health_status = "healthy"

            with Session(engine) as session:
                active_users = session.exec(select(User)).all()
                health = SystemHealth(
                    id=hashlib.md5(str(time.time()).encode()).hexdigest(),
                    cpu_usage=cpu_usage,
                    memory_usage=memory.percent,
                    disk_usage=disk.percent,
                    database_size_mb=db_size_mb,
                    api_response_time_ms=10.0,
                    error_rate=0.0,
                    active_users=len(active_users),
                    health_status=health_status,
                    timestamp=time.time(),
                )
                session.add(health)
                if health_status == "critical":
                    self._create_firewall_log(
                        action="warning",
                        details=json.dumps({"cpu": cpu_usage, "memory": memory.percent, "disk": disk.percent}),
                        affected_component="system_performance",
                        severity="high",
                    )
                session.commit()
                return health
        except Exception as e:
            self._create_firewall_log(
                action="error",
                details=str(e),
                affected_component="system_monitoring",
                severity="low",
            )
            return None

    def scan_for_threats(self, content: str, source_type: str = "user_input", source_id: Optional[str] = None) -> Optional[FirewallThreat]:
        """Scan content for security threats."""
        content_lower = content.lower()
        for rule in self.THREAT_RULES:
            for keyword in rule["keywords"]:
                if keyword in content_lower:
                    severity = "medium" if len(keyword) < 10 else "high"
                    threat = FirewallThreat(
                        id=hashlib.md5(f"{source_id}{content}{time.time()}".encode()).hexdigest(),
                        threat_type=rule["type"],
                        severity=severity,
                        description=f"Detected: {rule['name']} (keyword: {keyword})",
                        detected_in=source_type,
                        source_id=source_id,
                        action_taken="blocked",
                        blocked=True,
                        quarantined_data=content[:100],
                        timestamp=time.time(),
                    )
                    with Session(engine) as session:
                        session.add(threat)
                        session.commit()
                    self.total_threat_score += self.threat_severity_scores.get(severity, 1)
                    return threat
        return None

    def validate_learning_pattern(self, pattern: LearningPattern) -> Dict:
        """Validate that learned patterns are healthy and not drifting."""
        try:
            pattern_data = json.loads(pattern.pattern_data)
            validation_result = {
                "pattern_id": pattern.id,
                "is_valid": True,
                "issues": [],
                "confidence_score": pattern.confidence_score,
            }
            if pattern.confidence_score < 0.3:
                validation_result["issues"].append("Low confidence score")
                validation_result["is_valid"] = False
            age_seconds = time.time() - pattern.last_updated
            if age_seconds < 60 and pattern.confidence_score < 0.5:
                validation_result["issues"].append("Too recent with low confidence")
                validation_result["is_valid"] = False
            if not isinstance(pattern_data, dict):
                validation_result["issues"].append("Invalid pattern data structure")
                validation_result["is_valid"] = False
            if not validation_result["is_valid"]:
                self._create_drift_detector(pattern=pattern, issues=validation_result["issues"])
            return validation_result
        except Exception as e:
            return {"pattern_id": pattern.id, "is_valid": False, "issues": [f"Validation error: {str(e)}"]}

    def _create_drift_detector(self, pattern: LearningPattern, issues: List[str]):
        """Create drift detection record."""
        with Session(engine) as session:
            drift_detector = LearningDriftDetector(
                id=hashlib.md5(f"{pattern.id}{time.time()}".encode()).hexdigest(),
                check_type="pattern_validity",
                metric_name=pattern.pattern_type,
                expected_range_min=0.6,
                expected_range_max=1.0,
                current_value=pattern.confidence_score,
                drift_detected=True,
                severity="high" if pattern.confidence_score < 0.3 else "medium",
                recommended_action="Review and possibly retrain pattern",
                timestamp=time.time(),
            )
            session.add(drift_detector)
            session.commit()

    def check_data_privacy_compliance(self, data: Dict) -> bool:
        """Ensure data privacy compliance."""
        sensitive_fields = ["email", "password", "credit_card", "ssn", "phone"]
        for field in sensitive_fields:
            if field in str(data).lower():
                self._create_firewall_log(
                    action="privacy_warning",
                    details=f"Sensitive field detected: {field}",
                    affected_component="data_privacy",
                    severity="high",
                )
                return False
        return True

    async def scan_ai_tasks(self):
        """Periodically scan AI tasks for threats."""
        with Session(engine) as session:
            recent_tasks = session.exec(
                select(AITask).where(AITask.created_at > time.time() - 3600)
            ).all()
            threats_found = 0
            for task in recent_tasks:
                if task.input:
                    threat = self.scan_for_threats(task.input, source_type="ai_input", source_id=task.id)
                    if threat:
                        threats_found += 1
            if threats_found > 0:
                self._create_firewall_log(
                    action="threat_detected",
                    details=f"Found {threats_found} threats in AI tasks",
                    affected_component="learning_ai",
                    severity="medium",
                )

    def _create_firewall_log(self, action: str, details: str, affected_component: str, severity: str = "low", resolved: bool = False):
        """Create firewall audit log entry."""
        with Session(engine) as session:
            log = FirewallLog(
                id=hashlib.md5(f"{action}{details}{time.time()}".encode()).hexdigest(),
                action=action,
                details=details,
                affected_component=affected_component,
                severity=severity,
                resolved=resolved,
                timestamp=time.time(),
            )
            session.add(log)
            session.commit()

    async def get_security_status(self) -> Dict:
        """Get overall security status."""
        with Session(engine) as session:
            threats = session.exec(select(FirewallThreat)).all()
            threats_by_severity = {"critical": 0, "high": 0, "medium": 0, "low": 0}
            for threat in threats:
                threats_by_severity[threat.severity] += 1
            total_score = (
                threats_by_severity["critical"] * 20
                + threats_by_severity["high"] * 10
                + threats_by_severity["medium"] * 5
                + threats_by_severity["low"] * 1
            )
            security_status = "secure"
            if total_score > 100:
                security_status = "critical"
            elif total_score > 50:
                security_status = "at_risk"
            return {
                "status": security_status,
                "total_threat_score": total_score,
                "threats": threats_by_severity,
                "last_check": time.time(),
            }

    async def get_firewall_logs(self, limit: int = 50) -> List[Dict]:
        """Get recent firewall logs."""
        with Session(engine) as session:
            logs = session.exec(select(FirewallLog).order_by(FirewallLog.timestamp.desc()).limit(limit)).all()
            return [
                {
                    "action": log.action,
                    "severity": log.severity,
                    "component": log.affected_component,
                    "timestamp": log.timestamp,
                    "resolved": log.resolved,
                }
                for log in logs
            ]


firewall_ai = FirewallAI()


@router.get("/status")
async def get_security_status(current_user=Depends(get_current_user)):
    """Return the current firewall security status."""
    return await firewall_ai.get_security_status()


@router.get("/logs")
async def get_firewall_logs(current_user=Depends(get_current_user)):
    """Return recent firewall logs for the authenticated user."""
    return await firewall_ai.get_firewall_logs()


@router.get("/health")
async def monitor_health(current_user=Depends(get_current_user)):
    """Return current system health metrics."""
    return await firewall_ai.monitor_system_health()

    def _create_firewall_log(self, action: str, details: str, 
                            affected_component: str, severity: str = "low",
                            resolved: bool = False):
        """Create firewall audit log entry"""
        with Session(engine) as session:
            log = FirewallLog(
                id=hashlib.md5(
                    f"{action}{details}{time.time()}".encode()
                ).hexdigest(),
                action=action,
                details=details,
                affected_component=affected_component,
                severity=severity,
                resolved=resolved,
                timestamp=time.time()
            )
            session.add(log)
            session.commit()

    async def get_security_status(self) -> Dict:
        """Get overall security status"""
        with Session(engine) as session:
            threat_count = session.exec(
                select(FirewallThreat)
            ).all()
            
            threats_by_severity = {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0
            }
            
            for threat in threat_count:
                threats_by_severity[threat.severity] += 1
            
            # Calculate threat score
            total_score = (
                threats_by_severity["critical"] * 20 +
                threats_by_severity["high"] * 10 +
                threats_by_severity["medium"] * 5 +
                threats_by_severity["low"] * 1
            )
            
            security_status = "secure"
            if total_score > 50:
                security_status = "at_risk"
            if total_score > 100:
                security_status = "critical"
            
            return {
                "status": security_status,
                "total_threat_score": total_score,
                "threats": threats_by_severity,
                "last_check": time.time()
            }

    async def get_firewall_logs(self, limit: int = 50) -> List[Dict]:
        """Get recent firewall logs"""
        with Session(engine) as session:
            logs = session.exec(
                select(FirewallLog)
                .order_by(FirewallLog.timestamp.desc())
                .limit(limit)
            ).all()
            
            return [
                {
                    "action": log.action,
                    "severity": log.severity,
                    "component": log.affected_component,
                    "timestamp": log.timestamp,
                    "resolved": log.resolved
                }
                for log in logs
            ]


# Singleton instance
firewall_ai = FirewallAI()
