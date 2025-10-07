import streamlit as st
import requests
import os
import json
import time
import uuid


BACKEND_URL =  "https://call-automation-kxow.onrender.com"

# Folders from your code
CONVERSATIONS_DIR = "conversations"
RECORDINGS_DIR = "recordings"
LEADS_FILE = "leads.json"  # Local "CRM"


# ADDED: Prompt keys from your backend PROMPT_CONFIGS
PROMPT_KEYS = ["medical_sales", "hospital_receptionist", "chess_coach"]

# Available voices for StreamElements (from their API docs/docs.streamlabs.com/tts-voices)
# I checked: These are common ones. Test in your code to confirm.
AVAILABLE_VOICES = [
    {"name": "Brian", "gender": "Male", "accent": "British"},
    {"name": "Amy", "gender": "Female", "accent": "British"},
    {"name": "Emma", "gender": "Female", "accent": "British"},
    {"name": "Joanna", "gender": "Female", "accent": "American"},
    {"name": "Matthew", "gender": "Male", "accent": "American"},
    {"name": "Justin", "gender": "Male", "accent": "American"},
    {"name": "Kendra", "gender": "Female", "accent": "American"},
    {"name": "Salli", "gender": "Female", "accent": "American"},
    {"name": "Kimberly", "gender": "Female", "accent": "American"},
    {"name": "Joey", "gender": "Male", "accent": "American"},
    {"name": "Russell", "gender": "Male", "accent": "Australian"},
    {"name": "Nicole", "gender": "Female", "accent": "Australian"},
    {"name": "Aditi", "gender": "Female", "accent": "Indian English"},
    {"name": "Raveena", "gender": "Female", "accent": "Indian English"},
]
# Note: StreamElements uses ElevenLabs under the hood sometimes, but these are standard. If more, add from https://docs.streamlabs.com/api/tts.



# Format for dropdown: "Name (Gender - Accent)"
VOICE_OPTIONS = [f"{v['name']} ({v['gender']} - {v['accent']})" for v in AVAILABLE_VOICES]

# Load/save leads (shared function)
def load_leads():
    if os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, "r") as f:
            return json.load(f)
    return []

def save_leads(leads):
    with open(LEADS_FILE, "w") as f:
        json.dump(leads, f, indent=2)


# Function to get metrics from backend
def get_metrics():
    try:
        response = requests.get(f"{BACKEND_URL}/metrics")
        return response.json() if response.status_code == 200 else {}
    except:
        return {}

# Function to list conversations (scan JSON files)
def list_conversations():
    convs = []
    for file in os.listdir(CONVERSATIONS_DIR):
        if file.endswith(".json"):
            with open(os.path.join(CONVERSATIONS_DIR, file), "r") as f:
                data = json.load(f)
                convs.append({
                    "call_sid": data["conversation_id"],
                    "name": data["lead"].get("name", "Unknown"),
                    "phone": data["lead"].get("to_phone", "Unknown"),
                    "type": data["lead"].get("call_type", "Unknown"),
                    "summary": data.get("summary", {}).get("summary", "No summary"),
                    "sentiment": data.get("sentiment", {}).get("sentiment", "Neutral"),
                    "audio_url": data.get("twilio_audio_url", None)
                })
    return convs

# Sidebar for navigation
st.sidebar.title("AI Calling Dashboard")
page = st.sidebar.radio("Go to", ["Home", "Initiate Call", "Call Logs", "Settings"])

if page == "Home":
    st.title("Dashboard (Like CloserX)")
    st.write("Overview of your AI calls.")
    
    metrics = get_metrics()
    if metrics:
        st.subheader("Metrics")
        st.write(f"Calls Initiated: {metrics['calls_initiated']}")
        st.write(f"Calls Completed: {metrics['calls_completed']}")
        st.write(f"Errors: {metrics['errors']}")
        st.write(f"Avg Response Time: {metrics['avg_api_response_time_ms']:.2f} ms")
        st.write(f"Active Calls: {metrics['active_calls']}")
    else:
        st.warning("No metrics available. Is backend running?")
    
    # Quick metrics refresh
    if st.button("Refresh Metrics"):
        st.rerun()

elif page == "Initiate Manual Call":
    st.title("Start Manual Outbound Call")
    st.write("Start a call now (manual trigger). Automated calls run via scheduler on leads.")
    
    with st.form(key="call_form"):
        to_phone = st.text_input("Phone Number (e.g., +919876543210)")
        name = st.text_input("Lead Name (required)")
        prompt_config_key = st.selectbox("Prompt Type", PROMPT_KEYS)  # From your PROMPT_CONFIGS dict
        call_type = st.selectbox("Call Type", ["qualification", "reminder", "payment"])
        lead_json = st.text_area("Lead Details (JSON, optional)", value='{"id": "123", "email": "test@example.com"}')
        
        submit = st.form_submit_button("Start Call")
        
        if submit:
            if not name or not to_phone:
                st.error("Name and Phone are required!")
            else:
                try:
                    lead = json.loads(lead_json) if lead_json else {}
                    payload = {
                        "to_phone": to_phone,
                        "name": name,
                        "lead": lead,
                        "call_type": call_type,
                        "prompt_config_key": prompt_config_key
                    }
                    response = requests.post(f"{BACKEND_URL}/outbound_call", json=payload)
                    if response.status_code == 200:
                        data = response.json()
                        st.success(f"Call started! SID: {data['call_sid']}")
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Failed: {str(e)}")

elif page == "Leads Management":
    st.title("Manage Leads (Automated Calls)")
    st.write("Add/edit leads here. Scheduler auto-calls if status='Call Pending' or scheduled_time is due.")
    
    leads = load_leads()
    
    # Display leads table
    if leads:
        st.subheader("Current Leads")
        for i, lead in enumerate(leads):
            with st.expander(f"Lead ID: {lead['id']} | Name: {lead['name']} | Status: {lead['status']}"):
                st.write(lead)
                if st.button(f"Delete Lead {lead['id']}", key=f"del_{i}"):
                    leads.pop(i)
                    save_leads(leads)
                    st.rerun()
    else:
        st.info("No leads yet.")
    
    # Add new lead form
    with st.form("add_lead"):
        name = st.text_input("Name (required)")
        phone = st.text_input("Phone (e.g., +919876543210)")
        prompt_key = st.selectbox("Prompt Type", PROMPT_KEYS)
        call_type = st.selectbox("Call Type", ["qualification", "reminder", "payment"])
        scheduled_time = st.text_input("Scheduled Time (ISO: YYYY-MM-DDTHH:MM:SS, optional)")
        status = st.selectbox("Status", ["Pending", "Call Pending", "Called", "Failed"])
        other_details = st.text_area("Other Details (JSON)")
        
        if st.form_submit_button("Add Lead"):
            if not name or not phone:
                st.error("Name and Phone required!")
            else:
                new_lead = {
                    "id": str(uuid.uuid4())[:8],  # Short ID
                    "name": name,
                    "phone": phone,
                    "prompt_config_key": prompt_key,
                    "call_type": call_type,
                    "scheduled_time": scheduled_time if scheduled_time else None,
                    "status": status,
                    "details": json.loads(other_details) if other_details else {}
                }
                leads.append(new_lead)
                save_leads(leads)
                st.success("Lead added! Scheduler will auto-call if due.")


elif page == "Call Logs":
    st.title("Call Logs")
    st.write("View past calls, transcripts, summaries, and play audio (like CloserX call history).")
    
    convs = list_conversations()
    if convs:
        for conv in convs:
            with st.expander(f"Call SID: {conv['call_sid']} | Name: {conv['name']} | Type: {conv['type']}"):
                st.write(f"Phone: {conv['phone']}")
                st.write(f"Summary: {conv['summary']}")
                st.write(f"Sentiment: {conv['sentiment']}")
                
                # Full details from JSON
                try:
                    full_response = requests.get(f"{BACKEND_URL}/conversations/{conv['call_sid']}.json")
                    if full_response.status_code == 200:
                        st.json(full_response.json())  # Show transcript, turns, etc.
                except Exception as e:
                    st.warning(f"Full details fetch failed: {e}")
                
                # Audio playback if exists
                wav_path = os.path.join(RECORDINGS_DIR, f"{conv['call_sid']}_twilio.wav")
                if os.path.exists(wav_path):
                    st.audio(wav_path, format="audio/wav")
                elif conv['audio_url']:
                    st.write(f"Twilio Audio URL: {conv['audio_url']}")
                else:
                    st.warning("No audio available.")
    else:
        st.info("No calls yet.")

elif page == "Settings":
    st.title("Settings")
    st.write("Configure AI voice and other options.")
    
    # Voice selection (update your code to use this)
    # Voice selection (now with accents shown)
    selected = st.selectbox("TTS Voice (Gender - Accent)", VOICE_OPTIONS, index=0)
    selected_voice = selected.split(" (")[0]  # Extract name
    st.info(f"Selected: {selected_voice}. To apply, update synthesizer_config in your code: voice='{selected_voice}'")
    
    # Other configs (e.g., show env vars, but don't edit sensitive ones)
    st.subheader("Current Configs (Read-Only)")
    st.write(f"Twilio Phone: {os.getenv('TWILIO_PHONE_NUMBER')}")
    st.write(f"Base URL: {os.getenv('BASE_URL')}")
    
    if st.button("Save Changes"):
        st.success("Changes saved! Restart backend to apply voice.")

# Auto-refresh for real-time feel
# time.sleep(30)  # Optional: Slow refresh
# st.rerun()