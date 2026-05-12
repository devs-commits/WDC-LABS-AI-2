import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize the Supabase client
if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    supabase = None
    print("Warning: SUPABASE_URL or SUPABASE_KEY missing from environment variables.")

async def get_learning_asset(topic_tag: str) -> dict:
    """
    Fetch a learning asset by its topic tag from the Supabase learning_assets table.
    """
    if not supabase:
        print("[DB] Supabase client not initialized.")
        return None
    
    try:
        # Query the learning_assets table where topic_tag matches Sola's output
        response = supabase.table("learning_assets").select("*").eq("topic_tag", topic_tag).limit(1).execute()
        
        # If we found a match, return the first row
        if response.data and len(response.data) > 0:
            return response.data[0]
        
        return None
    except Exception as e:
        print(f"[DB] Error fetching learning asset for {topic_tag}: {e}")
        return None

# --- NEW CACHING FUNCTIONS FOR SERPER ---

async def get_cached_search(query: str) -> list:
    """
    Checks if we have already performed this Google Search to save API costs.
    """
    if not supabase:
        return None
    try:
        response = supabase.table("search_cache").select("results").eq("query", query).limit(1).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]["results"]
        return None
    except Exception as e:
        print(f"[DB] Error reading cache for query '{query}': {e}")
        return None

async def save_cached_search(query: str, results: list):
    """
    Saves a fresh Google Search to the database so future interns get it for free.
    """
    if not supabase:
        return
    try:
        # Upsert ensures if the query already exists, it just updates the results
        supabase.table("search_cache").upsert({
            "query": query, 
            "results": results
        }).execute()
    except Exception as e:
        print(f"[DB] Error saving cache for query '{query}': {e}")