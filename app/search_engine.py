import os
import requests
from typing import Optional, List, Dict, Any
import json
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def serper_search_links(query: str, num_results: int = 5) -> List[Dict[str, Any]]:
    """
    Perform a Serper.dev search and return structured search results
    including title, url, and snippet.
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
        return []

    results = []

    for item in data.get("organic", []):
        link = item.get("link")
        title = item.get("title")
        snippet = item.get("snippet")

        if link:
            results.append({
                "type": "link",
                "title": title,
                "url": link,
                "description": snippet
            })

        if len(results) >= num_results:
            break

    return results[:num_results]