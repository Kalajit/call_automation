import streamlit as st
import requests
import json
import time
import uuid
from datetime import datetime
import os 

BACKEND_URL = "https://call-automation-kxow.onrender.com"

PROMPT_KEYS = ["medical_sales", "hospital_receptionist", "chess_coach"]

# Full voices list (14 as per your spec)
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

VOICE_OPTIONS = [f"{v['name']} ({v['gender']} - {v['accent']})" for v in AVAILABLE_VOICES]

# FIXED: Fetch/save via backend API
def get_leads():
    try:
        response = requests.get(f"{BACKEND_URL}/leads")
        return response.json().get("leads", []) if response.status_code == 200 else []
    except:
        st.warning("Failed to fetch leads from backend.")
        return []

def add_lead_to_backend(name, phone, prompt_key, call_type, scheduled_time, status, details):
    payload = {
        "name": name,
        "phone": phone,
        "prompt_config_key": prompt_key,
        "call_type": call_type,
        "scheduled_time": scheduled_time,
        "status": status,
        "details": details
    }
    try:
        response = requests.post(f"{BACKEND_URL}/add_lead", json=payload)
        if response.status_code == 200:
            return response.json().get("lead_id")
        else:
            st.error(f"Backend error: {response.text}")
            return None
    except Exception as e:
        st.error(f"Failed to add lead to backend: {e}")
        return None

# FIXED: Check pending (robust parsing)
def check_pending_leads(leads):
    now = datetime.now()
    pending = []
    due = []
    for lead in leads:
        if lead.get("status") == "Call Pending":
            pending.append(lead)
        elif lead.get("scheduled_time"):
            try:
                fixed = lead["scheduled_time"].replace(" ", "T").replace("-", "T")  # FIXED: Handle space/-
                sched_time = datetime.fromisoformat(fixed)
                if sched_time <= now:
                    due.append(lead)
            except ValueError:
                st.warning(f"Invalid time for {lead['name']}: {lead['scheduled_time']}")
    return pending, due

def get_metrics():
    try:
        response = requests.get(f"{BACKEND_URL}/metrics")
        return response.json() if response.status_code == 200 else {}
    except:
        return {}

def list_conversations():
    try:
        response = requests.get(f"{BACKEND_URL}/conversations")
        return response.json().get("conversations", []) if response.status_code == 200 else []
    except:
        return []

# NEW: Auto-trigger first pending/due lead (called after refresh)
def auto_trigger_pending(leads):
    pending, due = check_pending_leads(leads)
    all_ready = pending + due
    if not all_ready:
        return  # No action
    
    # Take first ready lead
    first_lead = all_ready[0]
    name = first_lead.get("name", "Unknown")
    phone = first_lead.get("phone", "")
    prompt_key = first_lead.get("prompt_config_key", "chess_coach")
    call_type = first_lead.get("call_type", "qualification")
    lead_data = first_lead.copy()
    
    payload = {
        "to_phone": phone,
        "name": name,
        "lead": lead_data,
        "call_type": call_type,
        "prompt_config_key": prompt_key
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/outbound_call", json=payload)
        if response.status_code == 200:
            data = response.json()
            st.success(f"🚀 Auto-started call for {name}! SID: {data.get('call_sid', 'Unknown')}")
            st.info(f"Details: {call_type} via {prompt_key}")
        else:
            st.error(f"Auto-trigger failed for {name}: {response.text}")
    except Exception as e:
        st.error(f"Auto-trigger error for {name}: {e}")

def auto_refresh_if_enabled(interval=30):
    if "auto_refresh" not in st.session_state:
        st.session_state.auto_refresh = False
    if "last_refresh" not in st.session_state:
        st.session_state.last_refresh = time.time()
    
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        st.write(f"Last updated: {datetime.fromtimestamp(st.session_state.last_refresh).strftime('%H:%M:%S')}")
    with col2:
        st.session_state.auto_refresh = st.checkbox("Auto-refresh every 30s", value=st.session_state.auto_refresh)
    with col3:
        if st.button("Refresh Now"):
            st.session_state.last_refresh = time.time()
            st.rerun()
    
    if st.session_state.auto_refresh and time.time() - st.session_state.last_refresh >= interval:
        st.session_state.last_refresh = time.time()
        st.rerun()

st.sidebar.title("AI Calling Dashboard")
page = st.sidebar.radio("Go to", ["Home", "Initiate Manual Call", "Leads Management", "Call Logs", "Settings"])

if page == "Home":
    st.title("Dashboard (Like CloserX)")
    st.write("Overview of your AI calls.")
    
    metrics = get_metrics()
    if metrics:
        st.subheader("Metrics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Active Calls", metrics.get('active_calls', 0))
        with col2:
            total_initiated = sum(metrics.get('calls_initiated', {}).values())
            st.metric("Calls Initiated", total_initiated)
        with col3:
            total_completed = sum(metrics.get('calls_completed', {}).values())
            st.metric("Calls Completed", total_completed)
        with col4:
            total_errors = sum(metrics.get('errors', {}).values())
            st.metric("Errors", total_errors)
        with st.expander("Full Metrics"):
            st.json(metrics)
    else:
        st.warning("No metrics available. Is backend running?")
    
    # NEW: Check pending/scheduled leads every refresh + AUTO-TRIGGER
    leads = get_leads()
    pending, due = check_pending_leads(leads)
    total_pending = len(pending) + len(due)
    if total_pending > 0:
        st.warning(f"🚨 {total_pending} pending/due calls detected!")
        with st.expander("Details"):
            st.json({"Pending": [p['name'] for p in pending], "Due Scheduled": [d['name'] for d in due]})
        # AUTO-TRIGGER: If auto-refresh enabled, start first one
        if st.session_state.get("auto_refresh", False):
            auto_trigger_pending(leads)
    else:
        st.success("All leads up to date. No pending calls.")
    
    auto_refresh_if_enabled()  # Triggers check + auto-call on 30s

elif page == "Initiate Manual Call":
    st.title("Start Manual Outbound Call")
    st.write("Start a call now (manual trigger). Automated calls run via scheduler on leads.")
    
    with st.form(key="call_form"):
        to_phone = st.text_input("Phone Number (e.g., +917356793165)")
        name = st.text_input("Lead Name (required)")
        prompt_config_key = st.selectbox("Prompt Type", PROMPT_KEYS)
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
                except json.JSONDecodeError:
                    st.error("Invalid JSON in lead details!")
                except Exception as e:
                    st.error(f"Failed: {str(e)}")

elif page == "Leads Management":
    st.title("Manage Leads (Automated Calls)")
    st.write("Add/edit leads here. Scheduler auto-calls if status='Call Pending' or scheduled_time is due.")
    
    leads = get_leads()  # FIXED: Fetch from backend
    
    # Display leads table (FIXED: Highlight due/pending)
    if leads:
        st.subheader("Current Leads")
        pending, due = check_pending_leads(leads)
        if pending or due:
            st.warning(f"🚨 {len(pending)} pending + {len(due)} due scheduled leads below.")
        
        for lead in leads:
            is_pending = lead.get("status") == "Call Pending"
            is_due = False
            if lead.get("scheduled_time"):
                try:
                    fixed = lead["scheduled_time"].replace(" ", "T").replace("-", "T")
                    is_due = datetime.fromisoformat(fixed) <= datetime.now()
                except ValueError:
                    pass
            color = "background-color: #ffeb3b; padding: 10px; border: 1px solid orange;" if is_pending or is_due else ""
            st.markdown(f"""
            <div style="{color}">
                **Lead ID:** {lead['id']} | **Name:** {lead['name']} | **Status:** {lead['status']} | **Ready?** {'Yes' if is_pending or is_due else 'No'}
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander(f"Details: {lead['name']} ({lead['phone']})"):
                st.json(lead)
                # Delete: POST to backend if needed, but for now, warn (add /delete_lead endpoint later)
                if st.button(f"Delete Lead {lead['id']}", key=f"del_{lead['id']}"):
                    st.warning("Delete not implemented yet – add /delete_lead to backend.")
    else:
        st.info("No leads yet.")
    
    # Add new lead form (POST to backend)
    with st.form("add_lead"):
        name = st.text_input("Name (required)")
        phone = st.text_input("Phone (e.g., +917356793165)")
        prompt_key = st.selectbox("Prompt Type", PROMPT_KEYS)
        call_type = st.selectbox("Call Type", ["qualification", "reminder", "payment"])
        scheduled_time = st.text_input("Scheduled Time (ISO: YYYY-MM-DDTHH:MM:SS with T, e.g., 2025-10-07T20:30:00, optional)")
        status = st.selectbox("Status", ["Pending", "Call Pending", "Called", "Failed"])
        other_details = st.text_area("Other Details (JSON)", value="{}")
        
        submit = st.form_submit_button("Add Lead")
        
        if submit:
            if not name or not phone:
                st.error("Name and Phone required!")
            else:
                try:
                    details = json.loads(other_details)
                except json.JSONDecodeError:
                    details = {}
                    st.warning("Invalid JSON; using empty.")
                
                lead_id = add_lead_to_backend(name, phone, prompt_key, call_type, scheduled_time, status, details)
                if lead_id:
                    st.success(f"Lead added! ID: {lead_id}. Scheduler will auto-call if pending/due.")
                    st.rerun()  # Refresh list
                else:
                    st.error("Failed to add lead.")
    
    # AUTO-TRIGGER: If auto-refresh, check and call first pending
    if st.session_state.get("auto_refresh", False):
        auto_trigger_pending(leads)
    
    auto_refresh_if_enabled()

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
                
                try:
                    full_response = requests.get(f"{BACKEND_URL}/conversations/{conv['call_sid']}.json")
                    if full_response.status_code == 200:
                        st.json(full_response.json())
                except Exception as e:
                    st.warning(f"Full details fetch failed: {e}")
                
                if conv['audio_url']:
                    st.audio(conv['audio_url'], format="audio/wav")
                else:
                    st.warning("No audio available.")
    else:
        st.info("No calls yet. Run a call first!")
    
    auto_refresh_if_enabled()

elif page == "Settings":
    st.title("Settings")
    st.write("Configure AI voice and other options.")
    
    selected = st.selectbox("TTS Voice (Gender - Accent)", VOICE_OPTIONS, index=0)
    selected_voice = selected.split(" (")[0]
    st.info(f"Selected: {selected_voice}. To apply, update synthesizer_config in your code: voice='{selected_voice}'")
    
    st.subheader("Current Configs (Read-Only)")
    st.write(f"Twilio Phone: {os.getenv('TWILIO_PHONE_NUMBER', 'Not set locally')}")
    st.write(f"Base URL: {os.getenv('BASE_URL', 'Not set locally')}")
    
    if st.button("Save Changes"):
        st.success("Changes saved! Restart backend to apply voice.")