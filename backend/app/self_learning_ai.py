"""
Self-Learning AI Engine
Learns from user behavior, trends, and system metrics to adapt and improve
"""

import hashlib
import json
import time
from typing import Dict, List, Optional
from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func

from .db import engine
from .models import (
    UserBehavior, LearningPattern, TrendingContent, User,
)
from .auth import get_current_user

router = APIRouter(prefix="/api/learning")


class SelfLearningAI:
    """Self-learning AI that adapts based on user behavior and trends."""

    PATTERN_TYPES = {
        "creator_preference": "What types of tools creators prefer",
        "content_type": "Most popular content types",
        "time_of_day": "When users are most active",
        "seasonal": "Seasonal content patterns",
    }

    def __init__(self):
        self.learning_enabled = True
        self.min_pattern_frequency = 5
        self.confidence_threshold = 0.6

    async def track_user_behavior(self, user_id: str, action_type: str, service_name: Optional[str] = None):
        """Track user action for learning."""
        with Session(engine) as session:
            existing = session.exec(
                select(UserBehavior).where(
                    (UserBehavior.user_id == user_id)
                    & (UserBehavior.action_type == action_type)
                    & (UserBehavior.service_name == service_name)
                )
            ).first()

            if existing:
                existing.frequency += 1
                existing.last_occurrence = time.time()
            else:
                behavior = UserBehavior(
                    id=hashlib.md5(
                        f"{user_id}{action_type}{service_name}{time.time()}".encode()
                    ).hexdigest(),
                    user_id=user_id,
                    action_type=action_type,
                    service_name=service_name,
                    frequency=1,
                    last_occurrence=time.time(),
                    timestamp=time.time(),
                )
                session.add(behavior)
            session.commit()

    async def detect_patterns(self):
        """Detect recurring patterns in user behavior."""
        with Session(engine) as session:
            behaviors = session.exec(
                select(UserBehavior).where(UserBehavior.frequency >= self.min_pattern_frequency)
            ).all()

            patterns_by_type = {}
            for behavior in behaviors:
                key = f"{behavior.action_type}:{behavior.service_name or 'all'}"
                if key not in patterns_by_type:
                    patterns_by_type[key] = {
                        "count": 0,
                        "total_frequency": 0,
                        "users": set(),
                        "action": behavior.action_type,
                        "service": behavior.service_name,
                    }
                patterns_by_type[key]["count"] += 1
                patterns_by_type[key]["total_frequency"] += behavior.frequency
                patterns_by_type[key]["users"].add(behavior.user_id)

            for pattern_key, pattern_data in patterns_by_type.items():
                max_users = session.exec(func.count(User.id)).first()
                applicable_ratio = len(pattern_data["users"]) / max(max_users or 1, 1)
                confidence = min(1.0, applicable_ratio * 0.8 + 0.2)

                if confidence >= self.confidence_threshold:
                    pattern_id = hashlib.md5(pattern_key.encode()).hexdigest()
                    existing = session.exec(
                        select(LearningPattern).where(LearningPattern.id == pattern_id)
                    ).first()
                    pattern_record = LearningPattern(
                        id=pattern_id,
                        pattern_type="creator_preference",
                        pattern_data=json.dumps({
                            "action": pattern_data["action"],
                            "service": pattern_data["service"],
                            "frequency": pattern_data["total_frequency"],
                            "applicable_users": len(pattern_data["users"]),
                        }),
                        confidence_score=confidence,
                        applicable_users=len(pattern_data["users"]),
                        last_updated=time.time(),
                        created_at=existing.created_at if existing else time.time(),
                    )
                    if existing:
                        session.merge(pattern_record)
                    else:
                        session.add(pattern_record)
            session.commit()

    async def generate_recommendations(self, user_id: str) -> List[Dict]:
        """Generate personalized recommendations based on learned patterns."""
        with Session(engine) as session:
            user_behaviors = session.exec(select(UserBehavior).where(UserBehavior.user_id == user_id)).all()
            if not user_behaviors:
                trends = session.exec(
                    select(TrendingContent).order_by(TrendingContent.trend_velocity.desc()).limit(5)
                ).all()
                return [{"type": "trending", "title": t.title, "category": t.category} for t in trends]

            user_actions = set(b.action_type for b in user_behaviors)
            similar_patterns = session.exec(
                select(LearningPattern).where(LearningPattern.confidence_score >= 0.7)
            ).all()

            recommendations = []
            for pattern in similar_patterns:
                try:
                    pattern_data = json.loads(pattern.pattern_data)
                    if pattern_data.get("action") not in user_actions:
                        recommendations.append({
                            "type": "suggested_action",
                            "action": pattern_data.get("action"),
                            "reason": f"Popular with {pattern.applicable_users} creators",
                            "confidence": pattern.confidence_score,
                        })
                except Exception:
                    continue

            trends = session.exec(
                select(TrendingContent).order_by(TrendingContent.trend_velocity.desc()).limit(3)
            ).all()
            for trend in trends:
                recommendations.append({
                    "type": "trending",
                    "title": trend.title,
                    "category": trend.category,
                    "velocity": trend.trend_velocity,
                })
            return recommendations[:10]

    async def get_learning_status(self) -> Dict:
        """Get current learning system status."""
        with Session(engine) as session:
            pattern_count = session.exec(func.count(LearningPattern.id)).first()
            behavior_count = session.exec(func.count(UserBehavior.id)).first()
            trend_count = session.exec(func.count(TrendingContent.id)).first()
            return {
                "enabled": self.learning_enabled,
                "patterns_learned": pattern_count or 0,
                "behaviors_tracked": behavior_count or 0,
                "trends_detected": trend_count or 0,
                "status": "active",
                "last_update": time.time(),
            }

    async def export_learned_insights(self) -> Dict:
        """Export all learned insights."""
        with Session(engine) as session:
            patterns = session.exec(select(LearningPattern)).all()
            trends = session.exec(select(TrendingContent)).all()
            behaviors = session.exec(select(UserBehavior)).all()
            return {
                "patterns": [
                    {
                        "type": p.pattern_type,
                        "confidence": p.confidence_score,
                        "applicable_users": p.applicable_users,
                        "data": json.loads(p.pattern_data),
                    }
                    for p in patterns
                ],
                "trends": [
                    {
                        "title": t.title,
                        "category": t.category,
                        "velocity": t.trend_velocity,
                        "mentions": t.mentions_count,
                    }
                    for t in trends
                ],
                "behaviors_tracked": len(behaviors),
                "export_time": time.time(),
            }


self_learning_ai = SelfLearningAI()


@router.get("/status")
async def get_learning_status(current_user=Depends(get_current_user)):
    """Return the current learning system status for the authenticated user."""
    return await self_learning_ai.get_learning_status()


@router.get("/recommendations")
async def get_recommendations(current_user=Depends(get_current_user)):
    """Return personalized recommendations based on learned behavior."""
    return await self_learning_ai.generate_recommendations(current_user["id"])


@router.get("/export")
async def export_insights(current_user=Depends(get_current_user)):
    """Export learned insights for review."""
    return await self_learning_ai.export_learned_insights()
