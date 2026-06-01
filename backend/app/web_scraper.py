"""
Web Scraper Module
Ingests data from RSS feeds and web sources for self-learning
"""

import asyncio
import hashlib
import time
import json
from datetime import datetime
from typing import Optional
import feedparser
from sqlmodel import Session, select
from .db import engine
from .models import (
    LearningDataSource, TrendingContent, UserBehavior,
    FirewallThreat, FirewallLog
)


class WebScraper:
    """Scrapes RSS feeds and web content for learning"""
    
    DEFAULT_SOURCES = [
        {
            "url": "https://medium.com/feed/tag/creators",
            "category": "creator_tools",
            "type": "rss_feed"
        },
        {
            "url": "https://dev.to/api/articles?tag=ai",
            "category": "tech",
            "type": "api"
        },
        {
            "url": "https://news.ycombinator.com/rss",
            "category": "tech",
            "type": "rss_feed"
        },
        {
            "url": "https://www.producthunt.com/feed",
            "category": "trends",
            "type": "rss_feed"
        },
        {
            "url": "https://www.techcrunch.com/feed/",
            "category": "tech",
            "type": "rss_feed"
        },
    ]

    def __init__(self):
        self.session = None
        self.scraped_count = 0
        self.error_count = 0

    async def initialize_default_sources(self):
        """Initialize default RSS feed sources"""
        with Session(engine) as session:
            for source in self.DEFAULT_SOURCES:
                existing = session.exec(
                    select(LearningDataSource).where(
                        LearningDataSource.source_url == source["url"]
                    )
                ).first()
                
                if not existing:
                    new_source = LearningDataSource(
                        id=hashlib.md5(source["url"].encode()).hexdigest(),
                        source_type=source["type"],
                        source_url=source["url"],
                        category=source["category"],
                        enabled=True,
                        created_at=time.time()
                    )
                    session.add(new_source)
            session.commit()

    async def fetch_rss_feed(self, url: str) -> list:
        """Fetch and parse RSS feed"""
        try:
            # Use feedparser to get RSS data
            feed = feedparser.parse(url)
            entries = []
            
            for entry in feed.entries[:20]:  # Limit to 20 latest entries
                entries.append({
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "summary": entry.get("summary", "")[:500],  # Limit summary
                    "published": entry.get("published", ""),
                    "tags": [tag.get("term", "") for tag in entry.get("tags", [])]
                })
            
            return entries
        except Exception as e:
            self.error_count += 1
            self._log_firewall_error(
                f"RSS fetch error from {url}: {str(e)}",
                severity="low"
            )
            return []

    async def process_entries(self, entries: list, source_category: str):
        """Process scraped entries and extract trends"""
        with Session(engine) as session:
            for entry in entries:
                try:
                    # Create trending content record
                    title = entry.get("title", "")
                    summary = entry.get("summary", "")
                    
                    # Calculate relevance score based on content length and structure
                    relevance_score = min(1.0, len(summary) / 500)
                    
                    content_hash = hashlib.sha256(
                        f"{title}{source_category}".encode()
                    ).hexdigest()
                    
                    # Check if trend already exists
                    existing = session.exec(
                        select(TrendingContent).where(
                            TrendingContent.id == content_hash
                        )
                    ).first()
                    
                    if existing:
                        # Update trend metrics
                        existing.mentions_count += 1
                        existing.trend_velocity += 0.1
                        existing.last_updated = time.time()
                    else:
                        # Create new trend
                        new_trend = TrendingContent(
                            id=content_hash,
                            title=title,
                            category=source_category,
                            description=summary,
                            source_url=entry.get("link", ""),
                            relevance_score=relevance_score,
                            mentions_count=1,
                            trend_velocity=0.5,
                            last_updated=time.time(),
                            created_at=time.time()
                        )
                        session.add(new_trend)
                    
                    self.scraped_count += 1
                    
                except Exception as e:
                    self.error_count += 1
            
            session.commit()

    async def scrape_all_sources(self):
        """Scrape all enabled data sources"""
        with Session(engine) as session:
            sources = session.exec(
                select(LearningDataSource).where(
                    LearningDataSource.enabled == True
                )
            ).all()
            
            for source in sources:
                # Check if it's time to fetch (based on interval)
                if source.last_fetch:
                    elapsed = time.time() - source.last_fetch
                    if elapsed < source.fetch_interval_seconds:
                        continue
                
                entries = await self.fetch_rss_feed(source.source_url)
                await self.process_entries(entries, source.category)
                
                # Update last fetch time
                source.last_fetch = time.time()
                session.add(source)
            
            session.commit()

    def _log_firewall_error(self, message: str, severity: str = "low"):
        """Log scraper errors to firewall"""
        with Session(engine) as session:
            threat = FirewallThreat(
                id=hashlib.md5(
                    f"{message}{time.time()}".encode()
                ).hexdigest(),
                threat_type="learning_drift",
                severity=severity,
                description=message,
                detected_in="web_scrape",
                action_taken="logged",
                blocked=False,
                timestamp=time.time()
            )
            session.add(threat)
            session.commit()

    async def get_trending_topics(self, limit: int = 10) -> list:
        """Get top trending topics"""
        with Session(engine) as session:
            trends = session.exec(
                select(TrendingContent)
                .order_by(TrendingContent.trend_velocity.desc())
                .limit(limit)
            ).all()
            
            return [
                {
                    "title": t.title,
                    "category": t.category,
                    "trend_velocity": t.trend_velocity,
                    "mentions": t.mentions_count,
                    "relevance": t.relevance_score
                }
                for t in trends
            ]

    async def cleanup_old_trends(self, days: int = 30):
        """Remove trends older than specified days"""
        cutoff_time = time.time() - (days * 86400)
        with Session(engine) as session:
            session.query(TrendingContent).filter(
                TrendingContent.created_at < cutoff_time
            ).delete()
            session.commit()


# Singleton instance
web_scraper = WebScraper()
