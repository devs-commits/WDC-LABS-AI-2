import os
import requests
from typing import Optional
import json
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def serper_search_links(query: str, num_results: int = 5) -> Optional[str]:
    """
    Perform a Serper.dev search and return comma-separated URLs from organic results
    and People Also Ask.
    """
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {"q": query}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"Error during Serper search request: {e}")
        return ""

    links = []

    # Organic search results
    for item in data.get("organic", []):
        link = item.get("link")
        if link:
            links.append(link)

        # Also include sitelinks if they exist
        for sitelink in item.get("sitelinks", []):
            sl = sitelink.get("link")
            if sl:
                links.append(sl)

    # People Also Ask
    for item in data.get("peopleAlsoAsk", []):
        link = item.get("link")
        if link:
            links.append(link)

    # Deduplicate and limit number of results
    unique_links = list(dict.fromkeys(links))  # preserves order
    return ", ".join(unique_links[:num_results])
