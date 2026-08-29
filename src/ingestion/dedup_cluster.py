"""
Dedup & clustering (owner: Akshat).

1. Dedup exact/near-identical articles by content hash / canonical URL.
2. For anything new, compare its embedding against recent story
   clusters (last 24-48h window) and either attach it to an existing
   StoryCluster or spawn a new one.
"""

from src.schemas.contracts import Article, StoryCluster

SIMILARITY_THRESHOLD = 0.92  # tune empirically


def dedup(article: Article, existing_hashes: set[str]) -> bool:
    """Return True if this article is an exact duplicate we've already stored."""
    return article.content_hash in existing_hashes


def cluster(article: Article, recent_clusters: list[StoryCluster]) -> StoryCluster:
    """Attach article to an existing cluster (by embedding similarity) or create a new one."""
    # TODO: cosine similarity against recent_clusters' representative embeddings
    raise NotImplementedError
