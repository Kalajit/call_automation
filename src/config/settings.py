import os
from pathlib import Path
from dotenv import load_dotenv
from google.cloud import translate_v3 as translate

load_dotenv()

# ============================================
# TWILIO CONFIGURATION
# ============================================
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
BASE_URL = os.getenv("BASE_URL")

# ============================================
# AI CONFIGURATION
# ============================================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

# ============================================
# DATABASE CONFIGURATION
# ============================================
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "whatsapp_crm")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# ============================================
# CRM CONFIGURATION
# ============================================
CRM_API_URL = os.getenv("CRM_API_URL", "http://localhost:3000/api")
CRM_API_KEY = os.getenv("CRM_API_KEY")

# ============================================
# NOTIFICATION CONFIGURATION
# ============================================
EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER")
EMAIL_SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", 587))
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# ============================================
# STORAGE CONFIGURATION
# ============================================
RECORDINGS_DIR = Path("recordings")
RECORDINGS_DIR.mkdir(exist_ok=True, parents=True)

# ============================================
# GOOGLE CLOUD TRANSLATION CONFIGURATION
# ============================================
GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
GOOGLE_TRANSLATE_LOCATION = os.getenv("GOOGLE_TRANSLATE_LOCATION", "global")

if not GOOGLE_PROJECT_ID:
    raise ValueError("GOOGLE_PROJECT_ID is required for Google Translation")

# Sync client; will be called via run_in_executor
translation_client = translate.TranslationServiceClient()
TRANSLATE_PARENT = f"projects/{GOOGLE_PROJECT_ID}/locations/{GOOGLE_TRANSLATE_LOCATION}"

# ============================================
# ADDITIONAL CONFIGURATION
# ============================================
INDICTRANS_URL = os.getenv("INDICTRANS_URL", "http://indictrans:5000")
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY", None)

# ============================================
# RATE LIMITING
# ============================================
MAX_CONCURRENT_CALLS = int(os.getenv("MAX_CONCURRENT_CALLS", 10))

# ============================================
# VALIDATION
# ============================================
required_vars = [
    TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, BASE_URL,
    GROQ_API_KEY, DEEPGRAM_API_KEY,
    DB_USER, DB_PASSWORD
]

if not all(required_vars):
    raise ValueError("Missing required environment variables")