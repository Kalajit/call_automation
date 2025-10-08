# import streamlit as st
# import requests
# import json
# import time
# from datetime import datetime
# import os
# import re
# from typing import Optional

# BACKEND_URL = "https://call-automation-kxow.onrender.com"

# # Available prompt keys for call types
# PROMPT_KEYS = ["medical_sales", "hospital_receptionist", "chess_coach"]

# # Available voices for the synthesizer
# AVAILABLE_VOICES = [
#     {"name": "Brian", "gender": "Male", "accent": "British"},
#     {"name": "Amy", "gender": "Female", "accent": "British"},
#     {"name": "Emma", "gender": "Female", "accent": "British"},
#     {"name": "Joanna", "gender": "Female", "accent": "American"},
#     {"name": "Matthew", "gender": "Male", "accent": "American"},
#     {"name": "Justin", "gender": "Male", "accent": "American"},
#     {"name": "Kendra", "gender": "Female", "accent": "American"},
#     {"name": "Salli", "gender": "Female", "accent": "American"},
#     {"name": "Kimberly", "gender": "Female", "accent": "American"},
#     {"name": "Joey", "gender": "Male", "accent": "American"},
#     {"name": "Russell", "gender": "Male", "accent": "Australian"},
#     {"name": "Nicole", "gender": "Female", "accent": "Australian"},
#     {"name": "Aditi", "gender": "Female", "accent": "Indian English"},
#     {"name": "Raveena", "gender": "Female", "accent": "Indian English"},
# ]

# VOICE_OPTIONS = [f"{v['name']} ({v['gender']} - {v['accent']})" for v in AVAILABLE_VOICES]

# def get_leads() -> list:
#     """Fetch leads from the backend."""
#     try:
#         response = requests.get(f"{BACKEND_URL}/leads", timeout=10)
#         if response.status_code == 200:
#             return response.json().get("leads", [])
#         else:
#             st.error(f"Failed to fetch leads: {response.text}")
#             return []
#     except Exception as e:
#         st.error(f"Failed to fetch leads: {str(e)}")
#         return []

# def add_lead_to_backend(
#     name: str,
#     phone: str,
#     prompt_key: str,
#     call_type: str,
#     scheduled_time: Optional[str],
#     status: str,
#     details: dict
# ) -> Optional[str]:
#     """Add a lead to the backend with validation."""
#     payload = {
#         "name": name.strip(),
#         "phone": phone.strip(),
#         "prompt_config_key": prompt_key,
#         "call_type": call_type,
#         "scheduled_time": scheduled_time,
#         "status": status,
#         "details": details
#     }
#     try:
#         response = requests.post(f"{BACKEND_URL}/add_lead", json=payload, timeout=10)
#         if response.status_code == 200:
#             return response.json().get("lead_id")
#         else:
#             st.error(f"Backend error: {response.text}")
#             return None
#     except Exception as e:
#         st.error(f"Failed to add lead: {str(e)}")
#         return None

# def update_voice_in_backend(voice: str) -> bool:
#     """Update the synthesizer voice in the backend."""
#     payload = {"voice": voice}
#     try:
#         response = requests.post(f"{BACKEND_URL}/update_voice", json=payload, timeout=10)
#         if response.status_code == 200:
#             return True
#         else:
#             st.error(f"Failed to update voice: {response.text}")
#             return False
#     except Exception as e:
#         st.error(f"Failed to update voice: {str(e)}")
#         return False

# def delete_lead_from_backend(lead_id: str) -> bool:
#     """Delete a lead from the backend."""
#     payload = {"lead_id": lead_id}
#     try:
#         response = requests.post(f"{BACKEND_URL}/delete_lead", json=payload, timeout=10)
#         if response.status_code == 200:
#             return True
#         else:
#             st.error(f"Failed to delete lead: {response.text}")
#             return False
#     except Exception as e:
#         st.error(f"Failed to delete lead: {str(e)}")
#         return False

# def check_pending_leads(leads: list) -> tuple[list, list]:
#     """Check for pending and due leads based on scheduled time."""
#     now = datetime.now()
#     pending = []
#     due = []
#     for lead in leads:
#         if lead.get("status") == "Call Pending":
#             pending.append(lead)
#         elif lead.get("scheduled_time") and lead.get("status") == "Pending":
#             try:
#                 # Normalize to IST: strip any timezone and append +05:30
#                 sched_time_str = re.sub(r'(Z|[+-]\d{2}:\d{2})$', '', lead["scheduled_time"])
#                 sched_time_str += '+05:30'
#                 sched_time = datetime.fromisoformat(sched_time_str)
#                 if sched_time <= now:
#                     due.append(lead)
#             except ValueError as e:
#                 st.warning(f"Invalid time format for {lead['name']}: {lead['scheduled_time']} ({str(e)})")
#     return pending, due

# def get_metrics() -> dict:
#     """Fetch metrics from the backend."""
#     try:
#         response = requests.get(f"{BACKEND_URL}/metrics", timeout=10)
#         return response.json() if response.status_code == 200 else {}
#     except Exception as e:
#         st.error(f"Failed to fetch metrics: {str(e)}")
#         return {}

# def list_conversations() -> list:
#     """Fetch conversation summaries from the backend."""
#     try:
#         response = requests.get(f"{BACKEND_URL}/conversations", timeout=10)
#         return response.json().get("conversations", []) if response.status_code == 200 else []
#     except Exception as e:
#         st.error(f"Failed to fetch conversations: {str(e)}")
#         return []

# def auto_trigger_pending(leads: list):
#     """Auto-trigger calls for pending or due leads."""
#     if "last_triggered" in st.session_state and time.time() - st.session_state.last_triggered < 60:
#         st.info("Waiting 60s before next auto-trigger.")
#         return
#     st.session_state.last_triggered = time.time()
#     pending, due = check_pending_leads(leads)
#     all_ready = pending + due
#     if not all_ready:
#         return
#     first_lead = all_ready[0]
#     name = first_lead.get("name", "Unknown")
#     phone = first_lead.get("phone", "")
#     prompt_key = first_lead.get("prompt_config_key", "chess_coach")
#     call_type = first_lead.get("call_type", "qualification")
#     lead_data = first_lead.copy()
#     payload = {
#         "to_phone": phone,
#         "name": name,
#         "lead": lead_data,
#         "call_type": call_type,
#         "prompt_config_key": prompt_key
#     }
#     try:
#         response = requests.post(f"{BACKEND_URL}/outbound_call", json=payload, timeout=10)
#         if response.status_code == 200:
#             data = response.json()
#             st.success(f"🚀 Auto-started call for {name}! SID: {data.get('call_sid', 'Unknown')}")
#             st.info(f"Details: {call_type} via {prompt_key}")
#         else:
#             st.error(f"Auto-trigger failed for {name}: {response.text}")
#     except Exception as e:
#         st.error(f"Auto-trigger failed for {name}: {str(e)}")

# def validate_phone(phone: str) -> bool:
#     """Validate phone number format."""
#     pattern = r'^\+?\d{10,15}$'
#     return bool(re.match(pattern, phone.replace(" ", "")))

# def validate_scheduled_time(scheduled_time: str) -> bool:
#     """Validate scheduled time format (YYYY-MM-DDTHH:MM:SS)."""
#     if not scheduled_time:
#         return True
#     # Strictly validate YYYY-MM-DDTHH:MM:SS
#     pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
#     if not re.match(pattern, scheduled_time):
#         return False
#     try:
#         # Test parsing with IST timezone
#         datetime.fromisoformat(scheduled_time + '+05:30')
#         return True
#     except ValueError:
#         return False

# # Initialize session state
# if "last_triggered" not in st.session_state:
#     st.session_state.last_triggered = 0
# if "selected_voice" not in st.session_state:
#     st.session_state.selected_voice = VOICE_OPTIONS[0]  # Default to Brian
# if "leads_updated" not in st.session_state:
#     st.session_state.leads_updated = 0

# # Main app
# st.set_page_config(page_title="AI Calling Dashboard", layout="wide")
# st.title("AI Calling Dashboard")

# # Sidebar for navigation
# page = st.sidebar.selectbox("Navigate", ["Dashboard", "Leads Management", "Conversations", "Settings"])

# if page == "Dashboard":
#     st.header("Dashboard")
#     metrics = get_metrics()
#     if metrics:
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             st.metric("Calls Initiated", metrics.get("calls_initiated", {}).get("qualification", 0))
#         with col2:
#             st.metric("Calls Completed", metrics.get("calls_completed", {}).get("audio_saved", 0))
#         with col3:
#             st.metric("Active Calls", metrics.get("active_calls", 0))
#         st.subheader("Error Metrics")
#         for error_type, count in metrics.get("errors", {}).items():
#             st.write(f"{error_type.replace('_', ' ').title()}: {count}")
#     else:
#         st.warning("No metrics available.")

#     st.subheader("Pending Calls")
#     leads = get_leads()
#     pending, due = check_pending_leads(leads)
#     if pending or due:
#         st.write(f"Pending: {len(pending)}, Due: {len(due)}")
#         auto_trigger_pending(leads)
#     else:
#         st.info("No pending or due calls.")

# elif page == "Leads Management":
#     st.header("Leads Management")
    
#     # Add Lead Form
#     st.subheader("Add New Lead")
#     with st.form("add_lead_form"):
#         name = st.text_input("Name", placeholder="Enter lead name")
#         phone = st.text_input("Phone", placeholder="+919876543210")
#         prompt_key = st.selectbox("Prompt Type", PROMPT_KEYS)
#         call_type = st.selectbox("Call Type", ["qualification", "reminder", "payment"])
#         # Single text input for date and time without timezone
#         scheduled_time = st.text_input("Scheduled Time (YYYY-MM-DDTHH:MM:SS)", placeholder="2025-10-08T13:32:00")
#         details_input = st.text_area("Additional Details", "")  # Plain text
#         submit_button = st.form_submit_button("Add Lead")
        
#         if submit_button:
#             with st.spinner("Adding lead..."):
#                 # Validate inputs
#                 if not name.strip():
#                     st.error("Name cannot be empty.")
#                 elif not validate_phone(phone):
#                     st.error("Invalid phone number. Use format: +919876543210")
#                 elif scheduled_time and not validate_scheduled_time(scheduled_time):
#                     st.error("Invalid scheduled time. Use format: YYYY-MM-DDTHH:MM:SS (e.g., 2025-10-08T13:32:00)")
#                 else:
#                     # Send scheduled_time as is (no timezone); backend will handle IST
#                     final_scheduled_time = re.sub(r'(Z|[+-]\d{2}:\d{2})$', '', scheduled_time) if scheduled_time else None
#                     # Wrap plain text details in a dictionary
#                     details = {"text": details_input.strip()} if details_input.strip() else {}
#                     status = "Pending" if scheduled_time else "Call Pending"
#                     lead_id = add_lead_to_backend(name, phone, prompt_key, call_type, final_scheduled_time, status, details)
#                     if lead_id:
#                         st.success(f"Lead added successfully! ID: {lead_id}")
#                         st.session_state.leads_updated = time.time()  # Trigger lead refresh
#                     else:
#                         st.error("Failed to add lead. Check backend logs.")

#     # Display Leads
#     st.subheader("Existing Leads")
#     leads = get_leads()
#     if leads:
#         for lead in leads:
#             with st.expander(f"{lead['name']} ({lead['phone']}) - {lead['status']}"):
#                 st.write(f"ID: {lead['id']}")
#                 st.write(f"Prompt: {lead['prompt_config_key']}")
#                 st.write(f"Call Type: {lead['call_type']}")
#                 st.write(f"Scheduled Time: {lead.get('scheduled_time', 'N/A')}")
#                 st.write(f"Details: {json.dumps(lead.get('details', {}), indent=2)}")
#                 if st.button("Delete", key=f"delete_{lead['id']}"):
#                     with st.spinner("Deleting lead..."):
#                         if delete_lead_from_backend(lead['id']):
#                             st.success(f"Lead {lead['name']} deleted successfully!")
#                             st.session_state.leads_updated = time.time()
#                         else:
#                             st.error(f"Failed to delete lead {lead['name']}.")
#     else:
#         st.info("No leads found.")

# elif page == "Conversations":
#     st.header("Conversations")
#     conversations = list_conversations()
#     if conversations:
#         for conv in conversations:
#             with st.expander(f"{conv['name']} ({conv['phone']}) - {conv['type']}"):
#                 st.write(f"Call SID: {conv['call_sid']}")
#                 st.write(f"Summary: {conv['summary']}")
#                 st.write(f"Sentiment: {conv['sentiment']}")
#                 if conv['audio_url']:
#                     st.audio(conv['audio_url'])
#                 else:
#                     st.write("No audio available.")
#     else:
#         st.info("No conversations found.")

# elif page == "Settings":
#     st.header("Settings")
#     st.subheader("Voice Configuration")
#     selected_voice_option = st.selectbox(
#         "Select Voice",
#         VOICE_OPTIONS,
#         index=VOICE_OPTIONS.index(st.session_state.selected_voice)
#     )
#     if selected_voice_option != st.session_state.selected_voice:
#         voice_name = selected_voice_option.split(" (")[0]
#         with st.spinner("Updating voice..."):
#             if update_voice_in_backend(voice_name):
#                 st.session_state.selected_voice = selected_voice_option
#                 st.success(f"Voice updated to {voice_name}!")
#             else:
#                 st.error("Failed to update voice.")

# # Auto-refresh leads every 30 seconds
# if "last_lead_refresh" not in st.session_state:
#     st.session_state.last_lead_refresh = 0
# if time.time() - st.session_state.last_lead_refresh > 30 or st.session_state.leads_updated > st.session_state.last_lead_refresh:
#     st.session_state.last_lead_refresh = time.time()
#     st.rerun()

# if __name__ == "__main__":
#     st.write("Running AI Calling Dashboard...")







import streamlit as st
import requests
import json
import time
from datetime import datetime, timezone, timedelta
import os
import re
from typing import Optional

BACKEND_URL = "https://call-automation-kxow.onrender.com"

# Available prompt keys for call types
PROMPT_KEYS = ["medical_sales", "hospital_receptionist", "chess_coach"]

# Available voices for the synthesizer
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

def get_leads() -> list:
    """Fetch leads from the backend."""
    try:
        response = requests.get(f"{BACKEND_URL}/leads", timeout=10)
        if response.status_code == 200:
            return response.json().get("leads", [])
        else:
            st.error(f"Failed to fetch leads: {response.text}")
            return []
    except Exception as e:
        st.error(f"Failed to fetch leads: {str(e)}")
        return []

def add_lead_to_backend(
    name: str,
    phone: str,
    prompt_key: str,
    call_type: str,
    scheduled_time: Optional[str],
    status: str,
    details: dict
) -> Optional[str]:
    """Add a lead to the backend with validation."""
    payload = {
        "name": name.strip(),
        "phone": phone.strip(),
        "prompt_config_key": prompt_key,
        "call_type": call_type,
        "scheduled_time": scheduled_time,
        "status": status,
        "details": details
    }
    try:
        response = requests.post(f"{BACKEND_URL}/add_lead", json=payload, timeout=10)
        if response.status_code == 200:
            return response.json().get("lead_id")
        else:
            st.error(f"Backend error: {response.text}")
            return None
    except Exception as e:
        st.error(f"Failed to add lead: {str(e)}")
        return None

def update_lead_status(lead_id: str, status: str) -> bool:
    """Update the status of a lead in the backend."""
    payload = {"lead_id": lead_id, "status": status}
    try:
        response = requests.post(f"{BACKEND_URL}/update_lead_status", json=payload, timeout=10)
        if response.status_code == 200:
            return True
        else:
            st.error(f"Failed to update lead status: {response.text}")
            return False
    except Exception as e:
        st.error(f"Failed to update lead status: {str(e)}")
        return False

def update_voice_in_backend(voice: str) -> bool:
    """Update the synthesizer voice in the backend."""
    payload = {"voice": voice}
    try:
        response = requests.post(f"{BACKEND_URL}/update_voice", json=payload, timeout=10)
        if response.status_code == 200:
            return True
        else:
            st.error(f"Failed to update voice: {response.text}")
            return False
    except Exception as e:
        st.error(f"Failed to update voice: {str(e)}")
        return False

def delete_lead_from_backend(lead_id: str) -> bool:
    """Delete a lead from the backend."""
    payload = {"lead_id": lead_id}
    try:
        response = requests.post(f"{BACKEND_URL}/delete_lead", json=payload, timeout=10)
        if response.status_code == 200:
            return True
        else:
            st.error(f"Failed to delete lead: {response.text}")
            return False
    except Exception as e:
        st.error(f"Failed to delete lead: {str(e)}")
        return False

def check_pending_leads(leads: list) -> tuple[list, list]:
    """Check for pending and due leads based on scheduled time."""
    now = datetime.now(timezone(timedelta(hours=5, minutes=30)))  # IST timezone
    pending = []
    due = []
    for lead in leads:
        if lead.get("status") == "Call Pending":
            pending.append(lead)
        elif lead.get("scheduled_time") and lead.get("status") == "Pending":
            try:
                # Normalize to IST: strip any timezone and append +05:30
                sched_time_str = re.sub(r'(Z|[+-]\d{2}:\d{2})$', '', lead["scheduled_time"])
                sched_time_str += '+05:30'
                sched_time = datetime.fromisoformat(sched_time_str)
                if sched_time <= now:
                    due.append(lead)
            except ValueError as e:
                st.warning(f"Invalid time format for {lead['name']}: {lead['scheduled_time']} ({str(e)})")
    return pending, due

def get_metrics() -> dict:
    """Fetch metrics from the backend."""
    try:
        response = requests.get(f"{BACKEND_URL}/metrics", timeout=10)
        return response.json() if response.status_code == 200 else {}
    except Exception as e:
        st.error(f"Failed to fetch metrics: {str(e)}")
        return {}

def list_conversations() -> list:
    """Fetch conversation summaries from the backend."""
    try:
        response = requests.get(f"{BACKEND_URL}/conversations", timeout=10)
        return response.json().get("conversations", []) if response.status_code == 200 else []
    except Exception as e:
        st.error(f"Failed to fetch conversations: {str(e)}")
        return []

def auto_trigger_pending(leads: list):
    """Auto-trigger calls for pending or due leads."""
    if "last_triggered" in st.session_state and time.time() - st.session_state.last_triggered < 60:
        st.info("Waiting 60s before next auto-trigger.")
        return
    st.session_state.last_triggered = time.time()
    pending, due = check_pending_leads(leads)
    all_ready = pending + due
    if not all_ready:
        return
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
        response = requests.post(f"{BACKEND_URL}/outbound_call", json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            st.success(f"🚀 Auto-started call for {name}! SID: {data.get('call_sid', 'Unknown')}")
            st.info(f"Details: {call_type} via {prompt_key}")
        else:
            st.error(f"Auto-trigger failed for {name}: {response.text}")
    except Exception as e:
        st.error(f"Auto-trigger failed for {name}: {str(e)}")

def validate_phone(phone: str) -> bool:
    """Validate phone number format."""
    pattern = r'^\+?\d{10,15}$'
    return bool(re.match(pattern, phone.replace(" ", "")))

def validate_scheduled_time(scheduled_time: str) -> bool:
    """Validate scheduled time format (YYYY-MM-DDTHH:MM:SS)."""
    if not scheduled_time:
        return True
    # Strictly validate YYYY-MM-DDTHH:MM:SS
    pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
    if not re.match(pattern, scheduled_time):
        return False
    try:
        # Test parsing with IST timezone
        datetime.fromisoformat(scheduled_time + '+05:30')
        return True
    except ValueError:
        return False

# Initialize session state
if "last_triggered" not in st.session_state:
    st.session_state.last_triggered = 0
if "selected_voice" not in st.session_state:
    st.session_state.selected_voice = VOICE_OPTIONS[0]  # Default to Brian
if "leads_updated" not in st.session_state:
    st.session_state.leads_updated = 0

# Main app
st.set_page_config(page_title="AI Calling Dashboard", layout="wide")
st.title("AI Calling Dashboard")

# Sidebar for navigation
page = st.sidebar.selectbox("Navigate", ["Dashboard", "Leads Management", "Conversations", "Settings"])

if page == "Dashboard":
    st.header("Dashboard")
    metrics = get_metrics()
    if metrics:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Calls Initiated", metrics.get("calls_initiated", {}).get("qualification", 0))
        with col2:
            st.metric("Calls Completed", metrics.get("calls_completed", {}).get("audio_saved", 0))
        with col3:
            st.metric("Active Calls", metrics.get("active_calls", 0))
        st.subheader("Error Metrics")
        for error_type, count in metrics.get("errors", {}).items():
            st.write(f"{error_type.replace('_', ' ').title()}: {count}")
    else:
        st.warning("No metrics available.")

    st.subheader("Pending Calls")
    leads = get_leads()
    pending, due = check_pending_leads(leads)
    if pending or due:
        st.write(f"Pending: {len(pending)}, Due: {len(due)}")
        auto_trigger_pending(leads)
    else:
        st.info("No pending or due calls.")

elif page == "Leads Management":
    st.header("Leads Management")
    
    # Add Lead Form
    st.subheader("Add New Lead")
    with st.form("add_lead_form"):
        name = st.text_input("Name", placeholder="Enter lead name")
        phone = st.text_input("Phone", placeholder="+919876543210")
        prompt_key = st.selectbox("Prompt Type", PROMPT_KEYS)
        call_type = st.selectbox("Call Type", ["qualification", "reminder", "payment"])
        # Single text input for date and time without timezone
        scheduled_time = st.text_input("Scheduled Time (YYYY-MM-DDTHH:MM:SS)", placeholder="2025-10-08T13:32:00")
        details_input = st.text_area("Additional Details", "")  # Plain text
        submit_button = st.form_submit_button("Add Lead")
        
        if submit_button:
            with st.spinner("Adding lead..."):
                # Validate inputs
                if not name.strip():
                    st.error("Name cannot be empty.")
                elif not validate_phone(phone):
                    st.error("Invalid phone number. Use format: +919876543210")
                elif scheduled_time and not validate_scheduled_time(scheduled_time):
                    st.error("Invalid scheduled time. Use format: YYYY-MM-DDTHH:MM:SS (e.g., 2025-10-08T13:32:00)")
                else:
                    # Send scheduled_time as is (no timezone); backend will handle IST
                    final_scheduled_time = re.sub(r'(Z|[+-]\d{2}:\d{2})$', '', scheduled_time) if scheduled_time else None
                    # Wrap plain text details in a dictionary
                    details = {"text": details_input.strip()} if details_input.strip() else {}
                    status = "Pending" if scheduled_time else "Call Pending"
                    lead_id = add_lead_to_backend(name, phone, prompt_key, call_type, final_scheduled_time, status, details)
                    if lead_id:
                        st.success(f"Lead added successfully! ID: {lead_id}")
                        st.session_state.leads_updated = time.time()  # Trigger lead refresh
                    else:
                        st.error("Failed to add lead. Check backend logs.")

    # Display Leads in Table
    st.subheader("Existing Leads")
    leads = get_leads()
    if leads:
        # Prepare data for table
        table_data = []
        for lead in leads:
            table_data.append({
                "ID": lead["id"],
                "Name": lead["name"],
                "Phone": lead["phone"],
                "Prompt": lead["prompt_config_key"],
                "Call Type": lead["call_type"],
                "Scheduled Time": lead.get("scheduled_time", "N/A"),
                "Status": lead["status"],
                "Details": json.dumps(lead.get("details", {}), indent=2),
                "Delete": ""  # Placeholder for delete button
            })
        
        # Define column configuration for st.data_editor
        column_config = {
            "ID": st.column_config.TextColumn("ID", disabled=True),
            "Name": st.column_config.TextColumn("Name", disabled=True),
            "Phone": st.column_config.TextColumn("Phone", disabled=True),
            "Prompt": st.column_config.TextColumn("Prompt", disabled=True),
            "Call Type": st.column_config.TextColumn("Call Type", disabled=True),
            "Scheduled Time": st.column_config.TextColumn("Scheduled Time", disabled=True),
            "Status": st.column_config.SelectboxColumn(
                "Status",
                options=["Pending", "Call Pending", "Called", "Completed", "Failed"],
                default="Pending"
            ),
            "Details": st.column_config.TextColumn("Details", disabled=True),
            "Delete": st.column_config.TextColumn("Delete", disabled=True)
        }
        
        # Display editable table
        edited_data = st.data_editor(
            table_data,
            column_config=column_config,
            hide_index=True,
            key="leads_table",
            use_container_width=True
        )
        
        # Handle status updates
        for edited_row in edited_data:
            lead_id = edited_row["ID"]
            original_lead = next((lead for lead in leads if lead["id"] == lead_id), None)
            if original_lead and edited_row["Status"] != original_lead["status"]:
                with st.spinner(f"Updating status for {edited_row['Name']}..."):
                    if update_lead_status(lead_id, edited_row["Status"]):
                        st.success(f"Updated status for {edited_row['Name']} to {edited_row['Status']}")
                        st.session_state.leads_updated = time.time()
                    else:
                        st.error(f"Failed to update status for {edited_row['Name']}.")
        
        # Handle delete actions
        for row in edited_data:
            lead_id = row["ID"]
            if st.button("Delete", key=f"delete_{lead_id}"):
                with st.spinner(f"Deleting lead {row['Name']}..."):
                    if delete_lead_from_backend(lead_id):
                        st.success(f"Lead {row['Name']} deleted successfully!")
                        st.session_state.leads_updated = time.time()
                    else:
                        st.error(f"Failed to delete lead {row['Name']}.")
    else:
        st.info("No leads found.")

elif page == "Conversations":
    st.header("Conversations")
    conversations = list_conversations()
    if conversations:
        for conv in conversations:
            with st.expander(f"{conv['name']} ({conv['phone']}) - {conv['type']}"):
                st.write(f"Call SID: {conv['call_sid']}")
                st.write(f"Summary: {conv['summary']}")
                st.write(f"Sentiment: {conv['sentiment']}")
                if conv['audio_url']:
                    st.audio(conv['audio_url'])
                else:
                    st.write("No audio available.")
    else:
        st.info("No conversations found.")

elif page == "Settings":
    st.header("Settings")
    st.subheader("Voice Configuration")
    selected_voice_option = st.selectbox(
        "Select Voice",
        VOICE_OPTIONS,
        index=VOICE_OPTIONS.index(st.session_state.selected_voice)
    )
    if selected_voice_option != st.session_state.selected_voice:
        voice_name = selected_voice_option.split(" (")[0]
        with st.spinner("Updating voice..."):
            if update_voice_in_backend(voice_name):
                st.session_state.selected_voice = selected_voice_option
                st.success(f"Voice updated to {voice_name}!")
            else:
                st.error("Failed to update voice.")

# Auto-refresh leads every 30 seconds
if "last_lead_refresh" not in st.session_state:
    st.session_state.last_lead_refresh = 0
if time.time() - st.session_state.last_lead_refresh > 30 or st.session_state.leads_updated > st.session_state.last_lead_refresh:
    st.session_state.last_lead_refresh = time.time()
    st.rerun()

if __name__ == "__main__":
    st.write("Running AI Calling Dashboard...")