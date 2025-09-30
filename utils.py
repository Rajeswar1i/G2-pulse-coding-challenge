# utils.py
from datetime import datetime

def safe_text(element):
    """Safely extract text from a Selenium element or return empty string."""
    try:
        return element.text.strip()
    except Exception:
        return ""

def parse_date(date_str):
    """Parse a date string into a datetime object (adjust formats if needed)."""
    for fmt in ("%b %d, %Y", "%Y-%m-%d", "%d %b %Y"):
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except Exception:
            continue
    return None

def in_range(date_obj, start, end):
    """Check if date is within start and end range."""
    if not date_obj:
        return False
    return start <= date_obj <= end
