"""
Shared data contracts for the news analysis pipeline.

Everyone builds against these, not against each other's live code.
If you need to change a shape here, flag it to the team first —
this file is the single source of truth for agent I/O.
"""

from datetime import datetime
from typing import Literal, TypedDict
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Storage layer (owner: Anmol)
# ---------------------------------------------------------------------------

class Article(BaseModel):
    article_id: str
    content_hash: str
    url: str
    source: str
    title: str
    body: str
    published_at: datetime | None = None
    scraped_at: datetime
    embedding: list[float] | None = None


class StoryCluster(BaseModel):
    story_id: str
    topic: str
    first_seen_date: datetime
    last_updated_date: datetime
    article_ids: list[str]
    is_compressed: bool = False           # true once the Cleaner has run on it
    compressed_summary: str | None = None


# ---------------------------------------------------------------------------
# Agent I/O (owner: Akshat)
# Each agent takes the shared AgentState and returns its own slice of it.
# This is the LangGraph state shape — see src/agents/orchestrator.py
# ---------------------------------------------------------------------------

class ClaimVerificationResult(BaseModel):
    claim: str
    verdict: Literal["supported", "disputed", "unverified"]
    evidence_article_ids: list[str]
    confidence: float = Field(ge=0, le=1)


class PerspectiveResult(BaseModel):
    source: str
    stance_summary: str
    article_id: str


class TimelineEvent(BaseModel):
    date: datetime
    headline: str
    article_id: str
    development: str  # what changed vs the previous event


class ImpactResult(BaseModel):
    stakeholder: str
    impact_summary: str
    severity: Literal["low", "medium", "high"]


class Report(BaseModel):
    story_id: str
    summary: str
    claims: list[ClaimVerificationResult]
    perspectives: list[PerspectiveResult]
    timeline: list[TimelineEvent]
    impacts: list[ImpactResult]
    generated_at: datetime


class AgentState(TypedDict, total=False):
    """The state object threaded through the LangGraph graph."""
    query: str
    story_id: str
    retrieved_articles: list[Article]
    claims: list[ClaimVerificationResult]
    perspectives: list[PerspectiveResult]
    timeline: list[TimelineEvent]
    impacts: list[ImpactResult]
    report: Report
