"""
On-demand scraper (owner: Rohit).

Triggered synchronously when a user submits an article/URL, so the
analysis reflects the current version of that story even if the
scheduled scraper hasn't picked it up yet.
"""

from src.schemas.contracts import Article


def scrape_url(url: str) -> Article:
    """Fetch a single article the user submitted directly."""
    # TODO: fetch + parse single URL
    raise NotImplementedError
