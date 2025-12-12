from collections import defaultdict
from typing import Dict

# ============================================
# LANGUAGE CONFIGURATION
# ============================================

# Language code mapping
LANGUAGE_MAP = {
    'en': 'English',
    'hi': 'Hindi',
    'kn': 'Kannada',
    'ml': 'Malayalam',
    'ta': 'Tamil',
    'te': 'Telugu'
}

# Language detection keywords
LANGUAGE_SWITCH_KEYWORDS = {
    'hi': ['hindi', 'hindi mein', 'हिंदी', 'hindi me bolo', 'speak hindi'],
    'kn': ['kannada', 'kannada mein', 'ಕನ್ನಡ', 'kannada nalli', 'speak kannada'],
    'ml': ['malayalam', 'malayalam il', 'മലയാളം', 'malayalam parayamo', 'speak malayalam'],
    'ta': ['tamil', 'tamil la', 'தமிழ்', 'tamil paesu', 'speak tamil'],
    'te': ['telugu', 'telugu lo', 'తెలుగు', 'telugu cheppu', 'speak telugu'],
    'en': ['english', 'english mein', 'speak english', 'english please']
}

# ============================================
# METRICS STRUCTURE
# ============================================

def get_fresh_metrics() -> Dict:
    """Returns a fresh metrics dictionary"""
    return {
        "calls_initiated": defaultdict(int),
        "calls_completed": defaultdict(int),
        "calls_failed": defaultdict(int),
        "sentiment_distribution": defaultdict(int),
        "routing_decisions": defaultdict(int),
        "errors": defaultdict(int),
        "avg_call_duration": 0,
        "total_recordings": 0
    }