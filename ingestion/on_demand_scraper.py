import httpx
from bs4 import BeautifulSoup
import feedparser
import urllib.parse
from typing import List, Dict

async def fetch_news_data(query: str) -> List[Dict[str, str]]:
    """Fetches live news URLs and snippets using Google News RSS."""
    # Encode the query for a URL (e.g., "chip shortage" -> "chip%20shortage")
    encoded_query = urllib.parse.quote(query)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
    
    parsed_feed = feedparser.parse(rss_url)
    
    article_data = []
    # Grab the top 5 most relevant articles
    for entry in parsed_feed.entries[:5]: 
        article_data.append({
            "url": entry.link,
            "title": entry.title,
            "snippet": getattr(entry, "summary", "") # Fallback text
        })
        
    return article_data

async def scrape_article(url: str, fallback_snippet: str) -> str:
    """Scrapes the main text, falling back to the RSS snippet if blocked."""
    try:
        # follow_redirects=True is crucial for Google News links
        async with httpx.AsyncClient(follow_redirects=True) as client:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            response = await client.get(url, headers=headers, timeout=15.0)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            text = " ".join([p.get_text(strip=True) for p in paragraphs])
            
            # If we got blocked or the page has no paragraphs, use the fallback
            return text if len(text) > 200 else fallback_snippet
    except Exception as e:
        print(f"Failed to scrape full text for {url}: {e}")
        return fallback_snippet # Never return empty if we have a snippet

async def run_on_demand_scrape(query: str) -> Dict[str, any]:
    """Orchestrates the URL discovery and scraping for a user query."""
    news_items = await fetch_news_data(query)
    articles_content = []
    
    for item in news_items:
        content = await scrape_article(item["url"], item["snippet"])
        if content:
            articles_content.append({"url": item["url"], "content": content})
            
    return {"query": query, "articles": articles_content}