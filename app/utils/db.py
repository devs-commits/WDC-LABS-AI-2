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