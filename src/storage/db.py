"""
Time-indexed data store access layer (owner: Anmol).

Three logical tables (see src/schemas/contracts.py for shapes):
  - articles        : deduped raw records, keyed by content_hash
  - story_clusters   : one row per real-world event
  - story_articles    : join table, article -> story ordered by published_at

Swap in the real DB client here (Postgres/pgvector, Mongo, etc.)
Agents and ingestion code should only ever import from this module,
never touch a DB client directly, so the storage backend can change
without breaking anyone else's code.
"""

from src.schemas.contracts import Article, StoryCluster


def save_article(article: Article) -> None:
    raise NotImplementedError


def get_recent_clusters(hours: int = 48) -> list[StoryCluster]:
    raise NotImplementedError


def get_articles_for_story(story_id: str) -> list[Article]:
    """Ordered by published_at — this is what the Timeline agent queries."""
    raise NotImplementedError


def search_similar(query_embedding: list[float], top_k: int = 20) -> list[Article]:
    raise NotImplementedError
