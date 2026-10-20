import asyncio
import feedparser
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from typing import List, Dict
from src.storage.db import save_articles

from src.ingestion.dedup_cluster import process_and_cluster
# from src.storage.db import save_articles # We will connect this next

# Sample broad harvest sources
RSS_FEEDS = [
    "http://rss.cnn.com/rss/cnn_topstories.rss",
    "http://feeds.bbci.co.uk/news/world/rss.xml"
]

def fetch_rss_feeds() -> Dict[str, any]:
    """Fetches and parses broad news from predefined RSS feeds."""
    articles = []
    for feed_url in RSS_FEEDS:
        parsed_feed = feedparser.parse(feed_url)
        for entry in parsed_feed.entries[:10]:  # Limit to top 10 per feed for now
            articles.append({
                "url": entry.link,
                "content": entry.get("summary", entry.get("title", ""))
            })
            
    return {"query": "Scheduled Broad Harvest", "articles": articles}

async def run_scheduled_harvest():
    """Executes the broad harvest, deduplicates, and stores the results."""
    print(f"[{datetime.now()}] Starting scheduled broad harvest...")
    
    raw_data = fetch_rss_feeds()
    aggregated_content, source_urls = process_and_cluster(raw_data)
    
    # 3. Store in Database
    print(f"Harvested {len(source_urls)} unique articles.")
    await save_articles(aggregated_content, source_urls, source_type="rss_broad_harvest")
    
    print(f"[{datetime.now()}] Scheduled harvest complete.")

def start_scheduler():
    """Initializes and starts the twice-daily scheduler."""
    scheduler = AsyncIOScheduler()
    
    # Schedule to run at 8:00 AM and 8:00 PM every day
    scheduler.add_job(run_scheduled_harvest, 'cron', hour='8,20')
    scheduler.start()
    print("Scheduled scraper started. Running twice daily at 08:00 and 20:00.")