import re
import httpx
import requests
from typing import List, Tuple
from urllib.parse import urlparse

async def extract_urls(text: str) -> List[str]:
    """Extract all URLs from text using regex."""
    url_pattern = re.compile(r'https?://[^\s<>"{}|\\^`[\]]+')
    return url_pattern.findall(text)

async def verify_url(url: str, timeout: int = 10) -> bool:
    """Check if a URL is accessible (returns 200)."""
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.head(url, follow_redirects=True)
            return response.status_code == 200
    except Exception:
        return False

async def filter_valid_urls(urls: List[str]) -> List[str]:
    """Return only valid URLs from the list."""
    valid_urls = []
    for url in urls:
        if await verify_url(url):
            valid_urls.append(url)
    return valid_urls

async def clean_broken_links(text: str) -> str:
    """
    Remove broken links from text.
    If a link is broken, remove the entire link markdown or just the URL.
    """
    urls = await extract_urls(text)
    broken_urls = []
    
    for url in urls:
        if not await verify_url(url):
            broken_urls.append(url)
    
    # Remove broken URLs
    for broken_url in broken_urls:
        # Remove markdown links [text](broken_url)
        text = re.sub(r'\[([^\]]+)\]\(' + re.escape(broken_url) + r'\)', r'\1', text)
        # Remove plain URLs
        text = text.replace(broken_url, '')
    
    # Clean up extra whitespace
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()

def verify_url_sync(url: str, timeout: int = 10) -> bool:
    """Sync version of verify_url using requests."""
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        return response.status_code == 200
    except Exception:
        return False

def clean_broken_links_sync(text: str) -> str:
    """
    Sync version of clean_broken_links.
    """
    # Better regex for URLs: stops at whitespace or certain punctuation
    url_pattern = re.compile(r'https?://[^\s<>"{}|\\^`[\]]+')
    urls = url_pattern.findall(text)
    broken_urls = []
    
    for url in urls:
        if not verify_url_sync(url):
            broken_urls.append(url)
    
    # Remove broken URLs
    for broken_url in broken_urls:
        # Remove markdown links [text](broken_url)
        text = re.sub(r'\[([^\]]+)\]\(' + re.escape(broken_url) + r'\)', r'\1', text)
        # Remove plain URLs
        text = text.replace(broken_url, '')
    
    # Clean up extra whitespace
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()