"""
Deadline formatting utilities for consistent deadline display across the system.
"""

from datetime import datetime


def format_deadline_display(iso_deadline: str) -> str:
    """
    Convert ISO deadline string to human-readable format.
    
    Examples:
        - "2026-01-13T10:00:00" → "Tomorrow"
        - "2026-01-14T10:00:00" → "In 2 days"
        - Invalid input → "In 1 day"
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
        
        if days_diff <= 0:
            return "Today"
        elif days_diff == 1:
            return "Tomorrow"
        elif days_diff > 1:
            return f"In {days_diff} days"
        else:
            return "Overdue"
            
    except (ValueError, TypeError, AttributeError):
        # Safe fallback for any parsing errors
        return "In 1 day"


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
