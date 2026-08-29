"""
Scheduled scraper (owner: Rohit).

Runs twice daily via cron / scheduler. Broad harvest across configured
sources — not tied to any specific user query.

Output: list[Article] (see src/schemas/contracts.py) handed to
src/ingestion/dedup_cluster.py before hitting storage.
"""

from src.schemas.contracts import Article


SOURCES: list[str] = [
    # TODO: RSS feeds / news API endpoints
]


def run() -> list[Article]:
    """Entry point for the scheduled job."""
    articles: list[Article] = []
    for source in SOURCES:
        articles.extend(_scrape_source(source))
    return articles


def _scrape_source(source: str) -> list[Article]:
    # TODO: fetch + parse
    return []


if __name__ == "__main__":
    run()
