"""
Deadline formatting utilities for consistent deadline display across the system.
"""

from datetime import datetime
import calendar


def get_ordinal(n):
    """Get the ordinal suffix for a number (1st, 2nd, 3rd, etc.)."""
    if 11 <= n % 100 <= 13:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return suffix


def format_deadline_display(iso_deadline: str) -> str:
    """
    Convert ISO deadline string to human-readable format with full date and relative indicator.
    
    Examples:
        - "2026-01-21T10:00:00" → "Wednesday, 21st January 2026 (Tomorrow)"
        - "2026-01-20T10:00:00" → "Tuesday, 20th January 2026 (Today)"
        - Invalid input → "Invalid deadline"
    """
    try:
        # Parse ISO datetime string
        deadline_dt = datetime.fromisoformat(iso_deadline.replace('Z', '+00:00'))
        now = datetime.now()
        
        # Handle timezone-aware datetime
        if deadline_dt.tzinfo:
            now = now.replace(tzinfo=deadline_dt.tzinfo)
        
        # Calculate days difference (using date only, ignoring time)
        days_diff = (deadline_dt.date() - now.date()).days
        
        # Format the full date
        day_name = calendar.day_name[deadline_dt.weekday()]
        day = deadline_dt.day
        ordinal = get_ordinal(day)
        month_name = calendar.month_name[deadline_dt.month]
        year = deadline_dt.year
        date_str = f"{day_name}, {day}{ordinal} {month_name} {year}"
        
        # Determine relative indicator
        if days_diff < 0:
            relative = "Overdue"
        elif days_diff == 0:
            relative = "Today"
        elif days_diff == 1:
            relative = "Tomorrow"
        else:
            relative = f"In {days_diff} days"
        
        return f"{date_str} ({relative})"
            
    except (ValueError, TypeError, AttributeError):
        # Safe fallback for any parsing errors
        return "Invalid deadline"


def get_days_until_deadline(iso_deadline: str) -> int:
    """
    Get the number of days until deadline.
    Returns negative if deadline has passed.
    """
    try:
        deadline_dt = datetime.fromisoformat(iso_deadline.replace('Z', '+00:00'))
        now = datetime.now()
        
        if deadline_dt.tzinfo:
            now = now.replace(tzinfo=deadline_dt.tzinfo)
        
        return (deadline_dt.date() - now.date()).days
    except:
        return 1  # Safe fallback
