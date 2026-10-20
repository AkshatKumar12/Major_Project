import hashlib
from typing import Tuple, List

def get_content_hash(text: str) -> str:
    """Generates an MD5 hash of the text for exact-match deduplication."""
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def process_and_cluster(scraped_data: dict) -> Tuple[str, List[str]]:
    """
    Deduplicates scraped articles and combines them into a single context block 
    for the AI orchestrator. 
    """
    seen_hashes = set()
    unique_urls = []
    aggregated_text = []

    for article in scraped_data.get("articles", []):
        content = article["content"]
        url = article["url"]
        
        # Exact-match deduplication and length filter
        content_hash = get_content_hash(content)
        if content_hash not in seen_hashes and len(content) > 100: 
            seen_hashes.add(content_hash)
            unique_urls.append(url)
            aggregated_text.append(f"Source: {url}\nContent: {content}\n")
            
    # Join everything with clear separators for the LLM
    final_text = "\n---\n".join(aggregated_text)
    
    # Fallback if scraping yielded nothing
    if not final_text:
        final_text = "No substantial content could be scraped for this query."
        
    return final_text, unique_urls