"""
Cleaner (owner: Rohit).

Runs monthly. Compresses story clusters whose last_updated_date is
older than the cutoff into a single summary document, to keep storage
bounded while preserving long-term retention.
"""

from datetime import datetime, timedelta
from src.schemas.contracts import StoryCluster
from src.storage import db

COMPRESSION_CUTOFF_DAYS = 30


def run() -> None:
    cutoff = datetime.utcnow() - timedelta(days=COMPRESSION_CUTOFF_DAYS)
    stale_clusters = _get_stale_clusters(cutoff)
    for cluster in stale_clusters:
        _compress(cluster)


def _get_stale_clusters(cutoff: datetime) -> list[StoryCluster]:
    # TODO: query story_clusters where last_updated_date < cutoff and not is_compressed
    raise NotImplementedError


def _compress(cluster: StoryCluster) -> None:
    # TODO: summarize all articles in cluster.article_ids into one document,
    # store as cluster.compressed_summary, mark is_compressed=True,
    # archive/drop raw article bodies per retention policy.
    raise NotImplementedError


if __name__ == "__main__":
    run()
