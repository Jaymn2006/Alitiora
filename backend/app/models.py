"""SQLModel schema definitions for users, content, AI tasks, and platform intelligence models."""

from typing import Optional
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    email: str
    password_hash: str
    salt: str
    created_at: float


class SessionModel(SQLModel, table=True):
    token: str = Field(primary_key=True)
    user_id: str
    created_at: float
    expires_at: Optional[float] = None


class Project(SQLModel, table=True):
    id: str = Field(primary_key=True)
    owner_id: str
    title: str
    description: Optional[str] = None
    visibility: Optional[str] = "private"
    created_at: float


class Post(SQLModel, table=True):
    id: str = Field(primary_key=True)
    author_id: str
    content: str
    media_refs: Optional[str] = None
    likes_count: int = 0
    created_at: float


class Upload(SQLModel, table=True):
    id: str = Field(primary_key=True)
    owner_id: str
    filename: str
    path: str
    hash: str
    created_at: float


class AITask(SQLModel, table=True):
    id: str = Field(primary_key=True)
    owner_id: str
    input: str
    task_type: Optional[str] = None
    status: str = "pending"
    result_ref: Optional[str] = None
    result_text: Optional[str] = None
    created_at: float


class Message(SQLModel, table=True):
    id: str = Field(primary_key=True)
    from_id: str
    to_id: str
    body: str
    created_at: float


class IPRecord(SQLModel, table=True):
    id: str = Field(primary_key=True)
    owner_id: str
    content_hash: str
    timestamp: float
    proof_meta: Optional[str] = None


class Payment(SQLModel, table=True):
    id: str = Field(primary_key=True)
    user_id: str
    provider: Optional[str] = None
    amount: Optional[float] = 0.0
    currency: Optional[str] = "USD"
    status: Optional[str] = "pending"
    created_at: float


# ============================================================================
# SELF-LEARNING AI MODELS
# ============================================================================

class LearningDataSource(SQLModel, table=True):
    """Tracks RSS feeds and web data sources for self-learning"""
    id: str = Field(primary_key=True)
    source_type: str  # "rss_feed" | "website" | "api"
    source_url: str
    category: str  # "tech" | "creator_tools" | "trends" | "news"
    enabled: bool = True
    last_fetch: Optional[float] = None
    fetch_interval_seconds: int = 3600  # Default 1 hour
    created_at: float


class UserBehavior(SQLModel, table=True):
    """Tracks user interaction patterns for learning"""
    id: str = Field(primary_key=True)
    user_id: str
    action_type: str  # "ai_service_used" | "file_uploaded" | "message_sent" | "payment_made"
    service_name: Optional[str] = None
    frequency: int = 1  # How many times this pattern occurred
    last_occurrence: float
    timestamp: float


class TrendingContent(SQLModel, table=True):
    """Stores learned trending topics and content"""
    id: str = Field(primary_key=True)
    title: str
    category: str
    description: Optional[str] = None
    source_url: Optional[str] = None
    relevance_score: float = 0.5  # 0.0 to 1.0
    mentions_count: int = 1
    trend_velocity: float = 0.0  # How fast it's trending
    last_updated: float
    created_at: float


class LearningPattern(SQLModel, table=True):
    """Stores learned patterns about creators and content"""
    id: str = Field(primary_key=True)
    pattern_type: str  # "creator_preference" | "content_type" | "time_of_day" | "seasonal"
    pattern_data: str  # JSON: {"key": "value", ...}
    confidence_score: float = 0.0  # 0.0 to 1.0
    applicable_users: int = 0  # How many users this pattern applies to
    last_updated: float
    created_at: float


class LearningConfig(SQLModel, table=True):
    """Configuration for self-learning system"""
    id: str = Field(primary_key=True)
    config_key: str  # "learning_enabled" | "update_interval" | "data_retention_days"
    config_value: str
    description: Optional[str] = None
    updated_at: float


# ============================================================================
# FIREWALL AI MODELS
# ============================================================================

class SystemHealth(SQLModel, table=True):
    """Tracks system performance and health metrics"""
    id: str = Field(primary_key=True)
    cpu_usage: float = 0.0  # Percentage
    memory_usage: float = 0.0  # Percentage
    disk_usage: float = 0.0  # Percentage
    database_size_mb: float = 0.0
    api_response_time_ms: float = 0.0
    error_rate: float = 0.0  # Percentage
    active_users: int = 0
    health_status: str = "healthy"  # "healthy" | "warning" | "critical"
    timestamp: float


class FirewallThreat(SQLModel, table=True):
    """Logs detected security and system threats"""
    id: str = Field(primary_key=True)
    threat_type: str  # "malicious_content" | "privacy_violation" | "attack" | "learning_drift"
    severity: str  # "low" | "medium" | "high" | "critical"
    description: str
    detected_in: str  # "ai_input" | "user_data" | "web_scrape" | "system_metric"
    source_id: Optional[str] = None  # user_id | aiTask_id | etc
    action_taken: str  # What the firewall did to mitigate
    blocked: bool = False
    quarantined_data: Optional[str] = None
    timestamp: float


class FirewallLog(SQLModel, table=True):
    """Audit log for all firewall actions"""
    id: str = Field(primary_key=True)
    action: str  # "blocked" | "quarantined" | "warned" | "updated_rules" | "system_adjusted"
    details: str  # JSON: {"reason": "...", "severity": "..."}
    affected_component: str  # "learning_ai" | "user_input" | "system_performance"
    severity: str
    resolved: bool = False
    resolution_details: Optional[str] = None
    timestamp: float


class LearningDriftDetector(SQLModel, table=True):
    """Monitors for AI learning drift and degradation"""
    id: str = Field(primary_key=True)
    check_type: str  # "pattern_validity" | "data_quality" | "recommendation_accuracy"
    metric_name: str
    expected_range_min: float
    expected_range_max: float
    current_value: float
    drift_detected: bool = False
    severity: str = "low"  # "low" | "medium" | "high"
    recommended_action: Optional[str] = None
    timestamp: float
