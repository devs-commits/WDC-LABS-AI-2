import os
import httpx
from fastapi import APIRouter, Header, HTTPException, Request
from supabase import create_client, Client
from app.curriculum import get_curriculum_step # Adjust this import if your curriculum file is elsewhere

# Initialize Supabase strictly for the Cron Job (Using Service Role is best for backend automation)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") # Or SUPABASE_KEY depending on your env setup
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

NEXT_JS_URL = os.getenv("NEXT_JS_URL", "https://labs.wdc.ng")
CRON_SECRET = os.getenv("CRON_SECRET", "wdc_labs_cron_secure_884729xYz")

# Use APIRouter instead of app
router = APIRouter()

@router.post("/run-monday-task-release")
async def run_monday_task_release(request: Request, authorization: str = Header(None)):
    # 1. Verify the Cron Secret
    if authorization != CRON_SECRET:
        print("🚨 WDC Labs: Unauthorized Cron Request blocked.")
        raise HTTPException(status_code=401, detail="Unauthorized Cron Request")

    try:
        # 2. Fetch everyone who has passed their current week and is waiting
        response = supabase.table('user_progression') \
            .select("id, current_week, week_status, track, users(email, full_name)") \
            .eq('week_status', 'passed_waiting') \
            .execute()
            
        eligible_users = response.data
        processed_count = 0

        # We use an async client to efficiently fire off requests to Next.js
        async with httpx.AsyncClient() as client:
            for record in eligible_users:
                progression_id = record['id']
                next_week = record['current_week'] + 1
                track = record.get('track', 'general')
                
                # Safely extract user info
                user_info = record.get('users', {})
                user_email = user_info.get('email')
                user_name = user_info.get('full_name', 'Intern')

                # 3. Advance the progression week in the DB
                supabase.table('user_progression').update({
                    "current_week": next_week,
                    "week_status": "in_progress"
                }).eq("id", progression_id).execute()

                # 4. Fetch the Curriculum Topic/Objective for the email
                try:
                    step_info = get_curriculum_step(track, next_week)
                    next_week_topic = step_info.get("topic", f"Week {next_week} Masterclass")
                    next_week_outcome = step_info.get("objective", "Check your desk for the latest brief.")
                except Exception as e:
                    print(f"Failed to fetch curriculum info: {e}")
                    next_week_topic = f"Week {next_week} Objectives"
                    next_week_outcome = "Check your desk for the latest brief."

                # 5. Ping Next.js to send the ZeptoMail email!
                if user_email:
                    payload = {
                        "secret": CRON_SECRET,
                        "email": user_email,
                        "name": user_name,
                        "nextWeek": next_week,
                        "trackName": track.replace('_', ' ').replace('-', ' ').title(),
                        "nextWeekTopic": next_week_topic,
                        "nextWeekOutcome": next_week_outcome
                    }
                    try:
                        await client.post(f"{NEXT_JS_URL}/api/emails/monday-alert", json=payload)
                    except Exception as email_err:
                        print(f"Failed to trigger Next.js email route for {user_email}: {email_err}")
                        
                processed_count += 1

        print(f"✅ WDC Labs Cron: Successfully unlocked tasks and emailed {processed_count} interns.")
        return {
            "success": True, 
            "message": "Monday Task Release Complete",
            "users_updated": processed_count
        }

    except Exception as e:
        print(f"🔥 WDC Labs Cron Error: {str(e)}")
        return {"success": False, "error": str(e)}