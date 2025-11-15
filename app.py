# import streamlit as st
# import requests
# import pandas as pd
# import json
# from datetime import datetime, timedelta
# import plotly.express as px
# import plotly.graph_objects as go

# # Configuration
# API_BASE_URL = "http://localhost:3000/api"
# PYTHON_API_URL = "http://localhost:8000/api"
# WEBHOOK_URL = "https://yourdomain.com/api/webhooks/whatsapp"

# # Page config
# st.set_page_config(
#     page_title="4champz AI Sales CRM",
#     page_icon="📞",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS
# st.markdown("""
# <style>
#     .metric-card {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         padding: 20px;
#         border-radius: 10px;
#         color: white;
#         margin: 10px 0;
#     }
#     .stButton>button {
#         width: 100%;
#         background-color: #667eea;
#         color: white;
#         border-radius: 5px;
#     }
#     .success-box {
#         background-color: #d4edda;
#         border: 1px solid #c3e6cb;
#         padding: 10px;
#         border-radius: 5px;
#         margin: 10px 0;
#     }
#     .warning-box {
#         background-color: #fff3cd;
#         border: 1px solid #ffeaa7;
#         padding: 10px;
#         border-radius: 5px;
#         margin: 10px 0;
#     }
# </style>
# """, unsafe_allow_html=True)



# # Session state initialization
# DEFAULT_COMPANY_ID = 1                     # demo company
# if "authenticated" not in st.session_state:
#     st.session_state.authenticated = False
# if "company_id" not in st.session_state:
#     st.session_state.company_id = DEFAULT_COMPANY_ID
# if "user_role" not in st.session_state:
#     st.session_state.user_role = "admin"


# # ---------- API HELPERS (auto-add company_id) ----------
# def _url(endpoint: str) -> str:
#     return f"{API_BASE_URL}/{endpoint}"

# # API Helper Functions
# def api_get(endpoint):
#     try:
#         url = f"{API_BASE_URL}/{endpoint}"
#         params = {"company_id": st.session_state.company_id}
#         response = requests.get(url, params=params, timeout=10)
#         response.raise_for_status()
#         return response.json()
#     except Exception as e:
#         st.error(f"API Error: {str(e)}")
#         return None

# def api_post(endpoint, data):
#     if "company_id" not in data:
#         data["company_id"] = st.session_state.company_id
#     try:
#         response = requests.post(f"{API_BASE_URL}/{endpoint}", json=data, timeout=10)
#         response.raise_for_status()
#         return response.json()
#     except Exception as e:
#         st.error(f"API Error: {str(e)}")
#         return None

# def python_api_post(endpoint, data):
#     if "company_id" not in data:
#         data["company_id"] = st.session_state.company_id
#     try:
#         response = requests.post(f"{PYTHON_API_URL}/{endpoint}", json=data, timeout=30)
#         response.raise_for_status()
#         return response.json()
#     except Exception as e:
#         st.error(f"Python API Error: {str(e)}")
#         return None
    

# # Sidebar Navigation
# def render_sidebar():
#     with st.sidebar:
#         st.image("https://via.placeholder.com/150x50/667eea/ffffff?text=4champz+AI", width=150)
#         st.title("🎯 Navigation")
        
#         menu = {
#             "🏠 Dashboard": "dashboard",
#             "🏢 Companies": "companies",
#             "🤖 AI Agents": "agents",
#             "📞 Calling": "calling",
#             "💬 WhatsApp": "whatsapp",
#             "WhatsApp Connect": "whatsapp_connect",
#             "👥 Leads": "leads",
#             "📊 Analytics": "analytics",
#             "🔔 Notifications": "notifications",
#             "⚙️ Settings": "settings"
#         }
        
#         selected = st.radio("Menu", list(menu.keys()), label_visibility="collapsed")
#         st.session_state.page = menu[selected]
        
#         st.divider()
#         st.caption(f"Company ID: {st.session_state.company_id}")
#         st.caption(f"Role: {st.session_state.user_role}")
        
#         if st.button("🚪 Logout"):
#             st.session_state.authenticated = False
#             st.rerun()

# # Page 1: Dashboard
# def page_dashboard():
#     st.title("📊 Dashboard Overview")
    
#     # Fetch metrics
#     stats = api_get("stats/dashboard")
#     if not stats or not stats.get("data"):
#         st.warning("Unable to load dashboard data")
#         return
    
#     data = stats.get('data', {})
    
#     # Top metrics
#     col1, col2, col3, col4 = st.columns(4)
    
#     with col1:
#         st.markdown('<div class="metric-card">', unsafe_allow_html=True)
#         st.metric("Total Leads", data.get('total_leads', 0))
#         st.markdown('</div>', unsafe_allow_html=True)
    
#     with col2:
#         st.markdown('<div class="metric-card">', unsafe_allow_html=True)
#         st.metric("Conversations", data.get('total_conversations', 0))
#         st.markdown('</div>', unsafe_allow_html=True)
    
#     with col3:
#         st.markdown('<div class="metric-card">', unsafe_allow_html=True)
#         st.metric("Pending Invoices", data.get('pending_invoices', 0))
#         st.markdown('</div>', unsafe_allow_html=True)
    
#     with col4:
#         st.markdown('<div class="metric-card">', unsafe_allow_html=True)
#         st.metric("Avg Interest", f"{data.get('avg_interest_level', 0)}/10")
#         st.markdown('</div>', unsafe_allow_html=True)
    
#     # Charts
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.subheader("📈 Leads by Status")
#         status_data = data.get('leads_by_status', [])
#         if status_data:
#             df = pd.DataFrame(status_data)
#             fig = px.pie(df, names='lead_status', values='count', hole=0.4)
#             st.plotly_chart(fig, use_container_width=True)
    
#     with col2:
#         st.subheader("🔥 Hot Leads (Today)")
#         hot_leads = api_get("hot-leads")
#         if hot_leads and hot_leads.get('data'):
#             df = pd.DataFrame(hot_leads['data'][:5])
#             st.dataframe(df[['name', 'phone_number', 'tone_score', 'intent']], use_container_width=True)
#         else:
#             st.info("No hot leads today")
    
#     # Recent Activity
#     st.subheader("📋 Recent Activity")
    
#     tab1, tab2 = st.tabs(["Calls", "Messages"])
    
#     with tab1:
#         calls = api_get("call-logs?limit=10")
#         if calls and calls.get('data'):
#             df = pd.DataFrame(calls['data'])
#             df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
#             st.dataframe(df[['call_sid', 'to_phone', 'call_status', 'call_duration', 'created_at']], use_container_width=True)
    
#     with tab2:
#         messages = api_get("stats/messages")
#         if messages and messages.get('data'):
#             df = pd.DataFrame(messages['data'])
#             st.dataframe(df, use_container_width=True)

# # ---------- COMPANIES (read-only for demo) ----------
# def page_companies():
#     st.title("Companies Management")
    
#     companies = api_get("companies")
#     if companies and companies.get('data'):
#         df = pd.DataFrame(companies['data'])
#         st.dataframe(df, use_container_width=True)
#     else:
#         st.info("No companies found (demo mode – you can only see your own)")


# # Page 3: AI Agents
# def page_agents():
#     st.title("🤖 AI Agent Instances (CloserX Style)")
    
#     tab1, tab2, tab3 = st.tabs(["View Agents", "Create Agent", "Configure Agent"])
    
#     with tab1:
#         agents = api_get("agent-instances")
#         if agents and agents.get('data'):
#             for agent in agents['data']:
#                 with st.expander(f"{agent['agent_name']} ({agent['agent_type']})"):
#                     col1, col2 = st.columns(2)
#                     with col1:
#                         st.write(f"**Phone:** {agent['phone_number']}")
#                         st.write(f"**Status:** {'Active' if agent['is_active'] else 'Inactive'}")
#                     with col2:
#                         st.write(f"**Created:** {agent['created_at'][:10]}")
#                         st.write(f"**Voice:** {agent.get('default_voice', 'N/A')}")
#         else:
#             st.info("No agents found for your company")
    
#     with tab2:
#         st.subheader("Create New AI Agent")
        
#         with st.form("create_agent"):
#             company_id = st.selectbox("Company", [1, 2, 3], key="create_company")
#             agent_name = st.text_input("Agent Name*", placeholder="Chess Coach AI")
#             agent_type = st.selectbox("Agent Type*", ["voice", "whatsapp"])
#             phone_number = st.text_input("Phone Number", placeholder="+919876543210")
#             whatsapp_number = st.text_input("WhatsApp Number", placeholder="+919876543210")
            
#             custom_prompt = st.text_area("Custom Prompt (optional)", height=200, 
#                 placeholder="You are Priya from 4champz...")
            
#             voice = st.selectbox("Voice", ["Raveena", "Aditi", "Brian", "Matthew"])
            
#             if st.form_submit_button("Create Agent"):
#                 data = {
#                     "company_id": company_id,
#                     "agent_name": agent_name,
#                     "agent_type": agent_type,
#                     "phone_number": phone_number if phone_number else None,
#                     "whatsapp_number": whatsapp_number if whatsapp_number else None,
#                     "custom_prompt": custom_prompt if custom_prompt else None,
#                     "custom_voice": voice
#                 }
                
#                 result = api_post("agent-instances", data)
#                 if result and result.get('success'):
#                     st.success(f"✅ Agent created! ID: {result['data']['id']}")
#                     st.rerun()
#                 else:
#                     st.error("Failed to create agent")
    
#     with tab3:
#         st.subheader("Apply Template to Agent")
        
#         templates = api_get("extraction-templates")
#         if templates and templates.get('data'):
#             template_names = [t['template_name'] for t in templates['data']]
#             selected_template = st.selectbox("Select Template", template_names)
            
#             company_id = st.number_input("Company ID", min_value=1, value=1)
#             agent_id = st.number_input("Agent Instance ID (optional)", min_value=0, value=0)
            
#             if st.button("Apply Template"):
#                 template_id = next(t['id'] for t in templates['data'] if t['template_name'] == selected_template)
                
#                 result = api_post(f"companies/{company_id}/apply-template", {
#                     "template_id": template_id,
#                     "agent_instance_id": agent_id if agent_id > 0 else None
#                 })
                
#                 if result and result.get('success'):
#                     st.success(f"✅ Template applied! {len(result['data'])} fields configured")
#                 else:
#                     st.error("Failed to apply template")

# # Page 4: Calling
# def page_calling():
#     st.title("📞 AI Calling System")
    
#     tab1, tab2, tab3 = st.tabs(["Make Call", "Call Logs", "Scheduled Calls"])
    
#     with tab1:
#         with st.form("make_call"):
#             col1, col2 = st.columns(2)
#             with col1:
#                 lead_id = st.number_input("Lead ID", min_value=1, value=1)
#                 to_phone = st.text_input("Phone Number*", placeholder="+919876543210")
#                 name = st.text_input("Name", placeholder="Ajsal")
#             with col2:
#                 call_type = st.selectbox("Call Type", ["qualification", "reminder", "payment", "support"])
#                 prompt_key = st.selectbox("Prompt", ["chess_coach", "medical_sales", "hospital_receptionist"])
#                 agent_instance_id = st.number_input("Agent Instance ID (optional)", min_value=0, value=0)
            
#             if st.form_submit_button("Make Call Now"):
#                 if to_phone:
#                     data = {
#                         "lead_id": lead_id,
#                         "to_phone": to_phone,
#                         "name": name,
#                         "call_type": call_type,
#                         "prompt_config_key": prompt_key
#                     }
#                     if agent_instance_id > 0:
#                         result = python_api_post(f"outbound-call-agent?agent_instance_id={agent_instance_id}", data)
#                     else:
#                         result = python_api_post("outbound-call", data)
                    
#                     if result and result.get('success'):
#                         st.success(f"Call initiated! SID: {result.get('call_sid')}")
#                     else:
#                         st.error("Failed to initiate call")
#                 else:
#                     st.warning("Phone number is required")
    
#     with tab2:
#         st.subheader("📋 Recent Call Logs")
        
#         company_filter = st.selectbox("Filter by Company", ["All", "1", "2", "3"], key="call_company_filter")
        
#         endpoint = "call-logs"
#         if company_filter != "All":
#             endpoint += f"?company_id={company_filter}"
        
#         calls = api_get(endpoint)
        
#         if calls and calls.get('data'):
#             df = pd.DataFrame(calls['data'])
#             df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
            
#             # Add action buttons
#             for idx, row in df.iterrows():
#                 with st.expander(f"📞 {row['to_phone']} - {row['call_status']}"):
#                     col1, col2, col3 = st.columns(3)
#                     with col1:
#                         st.write(f"**Duration:** {row.get('call_duration', 0)}s")
#                         st.write(f"**Type:** {row.get('call_type', 'N/A')}")
#                     with col2:
#                         st.write(f"**Status:** {row['call_status']}")
#                         st.write(f"**Date:** {row['created_at']}")
#                     with col3:
#                         if row.get('recording_url'):
#                             st.markdown(f"[🎵 Recording]({row['recording_url']})")
                    
#                     if row.get('transcript'):
#                         st.text_area("Transcript", row['transcript'], height=100, key=f"transcript_{idx}")
#         else:
#             st.info("No call logs found")
    
#     with tab3:
#         st.subheader("🕐 Schedule Future Call")
        
#         with st.form("schedule_call"):
#             company_id = st.number_input("Company ID", min_value=1, value=1, key="sched_company")
#             lead_id = st.number_input("Lead ID", min_value=1, value=1, key="sched_lead")
#             call_type = st.selectbox("Call Type", ["qualification", "reminder", "payment"], key="sched_type")
            
#             schedule_date = st.date_input("Date", value=datetime.now() + timedelta(days=1))
#             schedule_time = st.time_input("Time", value=datetime.now().time())
            
#             if st.form_submit_button("Schedule Call"):
#                 scheduled_time = datetime.combine(schedule_date, schedule_time).isoformat()
                
#                 result = api_post("schedule-call", {
#                     "company_id": company_id,
#                     "lead_id": lead_id,
#                     "call_type": call_type,
#                     "scheduled_time": scheduled_time
#                 })
                
#                 if result and result.get('success'):
#                     st.success("✅ Call scheduled successfully!")
#                 else:
#                     st.error("Failed to schedule call")

# # Page 5: WhatsApp
# def page_whatsapp():
#     st.title("💬 WhatsApp Management")
    
#     tab1, tab2, tab3 = st.tabs(["Send Message", "Conversations", "Templates"])
    
#     with tab1:
#         st.subheader("📤 Send WhatsApp Message")
        
#         message_type = st.radio("Message Type", ["direct", "ai_generated"])
        
#         with st.form("send_whatsapp"):
#             phone_number = st.text_input("Phone Number*", placeholder="+919876543210")
            
#             if message_type == "direct":
#                 message = st.text_area("Message*", height=150)
#                 intent = None
#             else:
#                 intent = st.selectbox("Intent", [
#                     "follow_up_after_3_days",
#                     "payment_reminder_gentle",
#                     "payment_reminder_urgent",
#                     "booking_reminder",
#                     "booking_confirmation",
#                     "thank_you_after_session",
#                     "promotional_new_batch"
#                 ])
#                 message = None
                
#                 context = st.text_area("Context (JSON)", value='{"amount": 5000, "date": "tomorrow"}')
            
#             if st.form_submit_button("Send Message"):
#                 if phone_number:
#                     data = {
#                         "phone_number": phone_number,
#                         "message_type": message_type,
#                         "message": message,
#                         "intent": intent,
#                         "context": json.loads(context) if message_type == "ai_generated" else {}
#                     }
                    
#                     # Backend will forward to n8n with correct credentials
#                     result = api_post("whatsapp/send", data)
#                     if result and result.get("success"):
#                         st.success("Message queued")
#                     else:
#                         st.error("Failed")
#                 else:
#                     st.warning("Phone number required")
    
#     with tab2:
#         st.subheader("💬 Recent Conversations")
        
#         phone_search = st.text_input("Search by phone", placeholder="+919876543210")
        
#         if phone_search:
#             conv = api_get(f"conversations/{phone_search}")
#             if conv and conv.get('data'):
#                 st.write(f"**Name:** {conv['data'].get('name', 'N/A')}")
#                 st.write(f"**Status:** {conv['data'].get('lead_status', 'N/A')}")
#                 st.text_area("Conversation History", conv['data'].get('conversation_history', ''), height=300)
#             else:
#                 st.warning("No conversation found")
    
#     with tab3:
#         st.subheader("📝 Message Templates")
        
#         templates = api_get("whatsapp-templates")
#         if templates:
#             st.write("Templates coming soon...")
#         else:
#             st.info("No templates configured yet")



# # ---------- NEW: WHATSAPP CONNECT (OAuth + Credential Storage) ----------
# def page_whatsapp_connect():
#     st.title("Connect WhatsApp Business")
#     st.markdown("""
#     **One-time setup** – connects your WhatsApp number via Meta OAuth.  
#     After this, **all messages** go through **one webhook** and are routed by phone number.
#     """)
    
#     # Choose agent instance (or create new)
#     agents = api_get("agent-instances?agent_type=whatsapp")
#     options = {0: "Create new WhatsApp agent"}
#     if agents and agents.get("data"):
#         for a in agents["data"]:
#             options[a["id"]] = f"{a['agent_name']} – {a.get('whatsapp_number','—')}"
    
#     selected_id = st.selectbox("Select Agent Instance", list(options.values()))
#     agent_id = next((k for k, v in options.items() if v == selected_id), None)
    
#     if selected_id == "Create new WhatsApp agent":
#         with st.form("new_wa_agent"):
#             name = st.text_input("Agent Name*")
#             wa_num = st.text_input("WhatsApp Number*", placeholder="+919876543210")
#             if st.form_submit_button("Create Agent"):
#                 r = api_post("agent-instances", {
#                     "agent_name": name,
#                     "agent_type": "whatsapp",
#                     "whatsapp_number": wa_num
#                 })
#                 if r and r.get("success"):
#                     st.success("Agent created – refresh page")
#                     st.rerun()
    
#     if agent_id and agent_id != 0:
#         oauth_url = f"{API_BASE_URL}/whatsapp/oauth-start?agent_instance_id={agent_id}"
#         st.markdown(f'''
#         <a href="{oauth_url}" target="_blank">
#             <button style="background:#25D366;color:white;padding:12px 24px;border:none;border-radius:6px;font-size:16px;">
#                 Connect WhatsApp via Meta
#             </button>
#         </a>
#         ''', unsafe_allow_html=True)
        
#         st.info("""
#         **Flow:**  
#         1. Facebook login → pick Business number  
#         2. Callback saves encrypted `access_token`, `phone_number_id`  
#         3. Subscribes your **single webhook** for messages  
#         """)

# # Page 6: Leads
# def page_leads():
#     st.title("👥 Lead Management")
    
#     tab1, tab2, tab3 = st.tabs(["View Leads", "Add Lead", "Import Bulk"])
    
#     with tab1:
#         st.subheader("📋 Lead Database")
        
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             status_filter = st.selectbox("Filter by Status", ["All", "new", "contacted", "qualified", "lost"])
#         with col2:
#             source_filter = st.selectbox("Filter by Source", ["All", "whatsapp", "website", "google_ads", "meta_ads"])
#         with col3:
#             limit = st.number_input("Limit", min_value=10, max_value=500, value=50)
        
#         endpoint = f"leads?limit={limit}"
#         if status_filter != "All":
#             endpoint += f"&status={status_filter}"
        
#         leads = api_get(endpoint)
        
#         if leads and leads.get('data'):
#             df = pd.DataFrame(leads['data'])
            
#             # Display dataframe
#             st.dataframe(df[['id', 'name', 'phone_number', 'email', 'lead_status', 'interest_level', 'lead_source']], 
#                         use_container_width=True)
            
#             # Lead details expander
#             selected_lead_id = st.selectbox("View Details for Lead ID:", df['id'].tolist())
#             lead_details = next((l for l in leads['data'] if l['id'] == selected_lead_id), None)
            
#             if lead_details:
#                 with st.expander("📄 Full Lead Details", expanded=True):
#                     col1, col2 = st.columns(2)
#                     with col1:
#                         st.write(f"**Name:** {lead_details.get('name')}")
#                         st.write(f"**Phone:** {lead_details.get('phone_number')}")
#                         st.write(f"**Email:** {lead_details.get('email', 'N/A')}")
#                         st.write(f"**Status:** {lead_details.get('lead_status')}")
#                     with col2:
#                         st.write(f"**Interest:** {lead_details.get('interest_level')}/10")
#                         st.write(f"**Chess Rating:** {lead_details.get('chess_rating', 'N/A')}")
#                         st.write(f"**Location:** {lead_details.get('location', 'N/A')}")
#                         st.write(f"**Last Contact:** {lead_details.get('last_contacted', 'N/A')[:10]}")
                    
#                     st.text_area("Notes", lead_details.get('notes', ''), height=100)
#         else:
#             st.info("No leads found")
    
#     with tab2:
#         st.subheader("➕ Add New Lead")
        
#         with st.form("add_lead"):
#             col1, col2 = st.columns(2)
            
#             with col1:
#                 phone = st.text_input("Phone Number*", placeholder="+919876543210")
#                 name = st.text_input("Name", placeholder="John Doe")
#                 email = st.text_input("Email", placeholder="john@example.com")
#                 lead_source = st.selectbox("Source", ["whatsapp", "website", "google_ads", "meta_ads", "referral"])
            
#             with col2:
#                 chess_rating = st.number_input("Chess Rating", min_value=0, max_value=3000, value=0)
#                 location = st.text_input("Location", placeholder="Bangalore")
#                 interest_level = st.slider("Interest Level", 1, 10, 5)
            
#             if st.form_submit_button("Add Lead"):
#                 if phone:
#                     data = {
#                         "phone_number": phone,
#                         "name": name,
#                         "email": email,
#                         "lead_source": lead_source,
#                         "interest_level": interest_level,
#                         "chess_rating": chess_rating if chess_rating > 0 else None,
#                         "location": location if location else None
#                     }
                    
#                     result = api_post("leads", data)
#                     if result and result.get('success'):
#                         st.success(f"✅ Lead added! ID: {result['data']['id']}")
#                         st.rerun()
#                     else:
#                         st.error("Failed to add lead")
#                 else:
#                     st.warning("Phone number is required")
    
#     with tab3:
#         st.subheader("📥 Bulk Import Leads")
        
#         st.write("Upload a CSV file with columns: phone_number, name, email, lead_source, chess_rating, location")
        
#         uploaded_file = st.file_uploader("Choose CSV file", type=['csv'])
        
#         if uploaded_file:
#             df = pd.read_csv(uploaded_file)
#             st.dataframe(df.head())
            
#             if st.button("Import All Leads"):
#                 leads_data = df.to_dict('records')
#                 result = api_post("leads/bulk", {"leads": leads_data})
                
#                 if result and result.get('success'):
#                     st.success(f"✅ Imported {result.get('imported')} leads!")
#                     if result.get('errors'):
#                         st.warning(f"⚠️ {result.get('failed')} leads failed")
#                 else:
#                     st.error("Import failed")

# # Page 7: Analytics
# def page_analytics():
#     st.title("📊 Analytics & Reports")
    
#     tab1, tab2, tab3 = st.tabs(["Call Analytics", "Lead Analytics", "Revenue Analytics"])
    
#     with tab1:
#         st.subheader("📞 Call Performance")
        
#         metrics = api_get("metrics/dashboard")
#         if metrics and metrics.get('data'):
#             data = metrics['data']
            
#             col1, col2, col3 = st.columns(3)
#             with col1:
#                 st.metric("Active Calls", data.get('active_calls', 0))
#             with col2:
#                 total_calls = sum(data.get('calls_24h', [{}])[0].values()) if data.get('calls_24h') else 0
#                 st.metric("Calls (24h)", total_calls)
#             with col3:
#                 st.metric("Success Rate", f"{data.get('success_rate', 0)}%")
            
#             # Sentiment distribution
#             if data.get('sentiment_distribution'):
#                 st.subheader("😊 Sentiment Distribution")
#                 df = pd.DataFrame(data['sentiment_distribution'])
#                 fig = px.bar(df, x='sentiment_type', y='count', color='sentiment_type')
#                 st.plotly_chart(fig, use_container_width=True)
    
#     with tab2:
#         st.subheader("👥 Lead Analytics")
        
#         lead_stats = api_get("stats/leads")
#         if lead_stats and lead_stats.get('data'):
#             df = pd.DataFrame(lead_stats['data'])
            
#             fig = px.bar(df, x='lead_status', y='count', color='lead_status',
#                         title="Leads by Status")
#             st.plotly_chart(fig, use_container_width=True)
            
#             # Average interest by status
#             fig2 = px.scatter(df, x='lead_status', y='avg_interest', size='count',
#                              title="Average Interest Level by Status")
#             st.plotly_chart(fig2, use_container_width=True)
    
#     with tab3:
#         st.subheader("💰 Revenue Dashboard")
        
#         st.info("Revenue tracking coming soon...")
        
#         # Placeholder metrics
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             st.metric("Total Revenue", "₹0")
#         with col2:
#             st.metric("Pending Invoices", "0")
#         with col3:
#             st.metric("Collections", "0%")

# # Page 8: Notifications
# def page_notifications():
#     st.title("🔔 Notifications & Alerts")
    
#     tab1, tab2 = st.tabs(["Recent Notifications", "Alerts"])
    
#     with tab1:
#         notifications = api_get("system-notifications?limit=50")
        
#         if notifications and notifications.get('data'):
#             for notif in notifications['data']:
#                 priority_emoji = {
#                     'urgent': '🚨',
#                     'high': '⚠️',
#                     'normal': 'ℹ️',
#                     'low': '💡'
#                 }
                
#                 emoji = priority_emoji.get(notif.get('priority', 'normal'), 'ℹ️')
                
#                 with st.expander(f"{emoji} {notif['title']} - {notif['created_at'][:16]}"):
#                     st.write(notif['message'])
                    
#                     if not notif.get('is_read'):
#                         if st.button("Mark as Read", key=f"read_{notif['id']}"):
#                             result = api_post(f"system-notifications/{notif['id']}/read", {})
#                             if result:
#                                 st.success("Marked as read")
#                                 st.rerun()
#         else:
#             st.info("No notifications")
    
#     with tab2:
#         alerts = api_get("alerts?limit=20")
        
#         if alerts and alerts.get('data'):
#             for alert in alerts['data']:
#                 severity_color = {
#                     'critical': '🔴',
#                     'high': '🟠',
#                     'normal': '🟡',
#                     'low': '🟢'
#                 }
                
#                 icon = severity_color.get(alert.get('severity', 'normal'), '🟡')
                
#                 with st.expander(f"{icon} {alert['title']} - {alert['created_at'][:16]}"):
#                     st.write(alert['message'])
#                     st.caption(f"Severity: {alert.get('severity', 'normal')}")
                    
#                     if not alert.get('is_acknowledged'):
#                         if st.button("Acknowledge", key=f"ack_{alert['id']}"):
#                             st.success("Alert acknowledged")
#         else:
#             st.info("No alerts")

# # Page 9: Settings
# def page_settings():
#     st.title("⚙️ Settings & Configuration")
    
#     tab1, tab2, tab3, tab4 = st.tabs(["Human Agents", "Custom Fields", "Integration", "System"])
    
#     with tab1:
#         st.subheader("👨‍💼 Human Agents Management")
        
#         agents = api_get("human-agents")
#         if agents and agents.get('data'):
#             for agent in agents['data']:
#                 with st.expander(f"👤 {agent['name']} - {agent['role']}"):
#                     col1, col2 = st.columns(2)
#                     with col1:
#                         st.write(f"**Email:** {agent['email']}")
#                         st.write(f"**Phone:** {agent.get('phone', 'N/A')}")
#                         st.write(f"**Status:** {agent['status']}")
#                     with col2:
#                         st.write(f"**Assigned Leads:** {agent['assigned_leads']}")
#                         st.write(f"**Max Concurrent:** {agent['max_concurrent_leads']}")
                    
#                     new_status = st.selectbox(
#                         "Change Status",
#                         ["available", "busy", "offline"],
#                         key=f"status_{agent['id']}"
#                     )
                    
#                     if st.button("Update Status", key=f"update_{agent['id']}"):
#                         result = api_post(f"human-agents/{agent['id']}/status", {"status": new_status})
#                         if result:
#                             st.success("Status updated")
#                             st.rerun()
        
#         st.divider()
        
#         with st.form("add_agent"):
#             st.subheader("Add New Agent")
#             col1, col2 = st.columns(2)
#             with col1:
#                 name = st.text_input("Name*")
#                 email = st.text_input("Email*")
#                 phone = st.text_input("Phone")
#             with col2:
#                 role = st.selectbox("Role", ["sales_rep", "senior_rep", "specialist", "manager"])
#                 max_leads = st.number_input("Max Concurrent Leads", 1, 20, 5)
            
#             if st.form_submit_button("Add Agent"):
#                 st.info("Agent management API endpoint needed")
    
#     with tab2:
#         st.subheader("🔧 Custom Field Templates")
        
#         templates = api_get("extraction-templates")
        
#         if templates and templates.get('data'):
#             for template in templates['data']:
#                 with st.expander(f"📋 {template['template_name']} ({template['industry']})"):
#                     st.write(f"**Description:** {template['description']}")
                    
#                     fields = template['field_definitions'].get('fields', [])
#                     st.write(f"**Fields:** {len(fields)}")
                    
#                     if st.button(f"View Details", key=f"template_{template['id']}"):
#                         st.json(fields)
#         else:
#             st.info("No templates found")
        
#         st.divider()
        
#         st.subheader("Create Custom Field")
#         with st.form("custom_field"):
#             company_id = st.number_input("Company ID", 1, 100, 1)
#             field_key = st.text_input("Field Key", placeholder="chess_rating")
#             field_label = st.text_input("Field Label", placeholder="Chess Rating")
#             field_type = st.selectbox("Field Type", ["text", "number", "date", "email", "select"])
#             field_category = st.selectbox("Category", ["personal", "qualification", "preference"])
            
#             if st.form_submit_button("Create Field"):
#                 data = {
#                     "company_id": company_id,
#                     "field_key": field_key,
#                     "field_label": field_label,
#                     "field_type": field_type,
#                     "field_category": field_category
#                 }
#                 result = api_post("custom-fields", data)
#                 if result and result.get('success'):
#                     st.success("✅ Custom field created!")
#                 else:
#                     st.error("Failed to create field")
    
#     with tab3:
#         st.subheader("🔗 Integrations")
        
#         st.info("**Available Integrations:**")
        
#         integrations = {
#             "WhatsApp Business API": "✅ Connected",
#             "Twilio Voice": "✅ Connected",
#             "Google Calendar": "✅ Connected",
#             "Stripe Payments": "⚠️ Not Configured",
#             "Razorpay": "⚠️ Not Configured",
#             "SendGrid Email": "⚠️ Not Configured"
#         }
        
#         for name, status in integrations.items():
#             col1, col2 = st.columns([3, 1])
#             with col1:
#                 st.write(f"**{name}**")
#             with col2:
#                 st.write(status)
        
#         st.divider()
        
#         st.subheader("Configure WhatsApp Agent")
#         with st.form("whatsapp_config"):
#             agent_id = st.number_input("Agent Instance ID", 1)
#             access_token = st.text_input("Access Token", type="password")
#             phone_number_id = st.text_input("Phone Number ID")
#             business_account_id = st.text_input("Business Account ID")
            
#             if st.form_submit_button("Save Credentials"):
#                 data = {
#                     "access_token": access_token,
#                     "phone_number_id": phone_number_id,
#                     "business_account_id": business_account_id
#                 }
#                 result = api_post(f"agent-instances/{agent_id}/whatsapp-credentials", data)
#                 if result and result.get('success'):
#                     st.success(f"✅ Credentials saved!")
#                     st.code(f"Webhook URL: {result.get('webhook_url')}")
#                     st.code(f"Verify Token: {result.get('verify_token')}")
#                 else:
#                     st.error("Failed to save credentials")
    
#     with tab4:
#         st.subheader("🖥️ System Information")
        
#         health = api_get("health")
#         if health:
#             st.json(health)
        
#         st.divider()
        
#         col1, col2 = st.columns(2)
        
#         with col1:
#             st.subheader("Database Stats")
#             stats = api_get("stats/dashboard")
#             if stats:
#                 st.metric("Total Leads", stats.get('data', {}).get('total_leads', 0))
#                 st.metric("Total Conversations", stats.get('data', {}).get('total_conversations', 0))
#                 st.metric("Total Messages", stats.get('data', {}).get('total_messages', 0))
        
#         with col2:
#             st.subheader("Quick Actions")
            
#             if st.button("🔄 Refresh Cache"):
#                 st.success("Cache refreshed")
            
#             if st.button("📊 Generate Daily Report"):
#                 st.info("Report generation initiated")
            
#             if st.button("🧹 Cleanup Old Data"):
#                 st.warning("This will delete data older than 90 days")

# # Main App Logic
# def main():
#     # Simple auth (replace with real auth)
#     if not st.session_state.authenticated:
#         st.title("🔐 Login to 4champz AI CRM")
        
#         col1, col2, col3 = st.columns([1, 2, 1])
        
#         with col2:
#             with st.form("login"):
#                 username = st.text_input("Username")
#                 password = st.text_input("Password", type="password")
                
#                 if st.form_submit_button("Login"):
#                     # Simple demo login
#                     if username and password:
#                         st.session_state.authenticated = True
#                         st.session_state.username = username
#                         st.rerun()
#                     else:
#                         st.error("Invalid credentials")
            
#             st.info("Demo: Use any username/password to login")
        
#         return
    
#     # Render sidebar
#     render_sidebar()
    
#     # Route to pages
#     page = st.session_state.get('page', 'dashboard')
    
#     if page == 'dashboard':
#         page_dashboard()
#     elif page == 'companies':
#         page_companies()
#     elif page == 'agents':
#         page_agents()
#     elif page == 'calling':
#         page_calling()
#     elif page == 'whatsapp':
#         page_whatsapp()
#     elif page == 'whatsapp_connect':          # <-- NEW
#         page_whatsapp_connect()
#     elif page == 'leads':
#         page_leads()
#     elif page == 'analytics':
#         page_analytics()
#     elif page == 'notifications':
#         page_notifications()
#     elif page == 'settings':
#         page_settings()

# if __name__ == "__main__":
#     main()









# # app.py
# import streamlit as st
# import requests
# import pandas as pd
# import json
# from datetime import datetime, timedelta
# import plotly.express as px
# import time
# from typing import Optional, Dict, List

# # ==================== CONFIGURATION ====================
# API_BASE_URL = "http://localhost:3000/api"
# PYTHON_API_URL = "http://localhost:8000/api"

# st.set_page_config(
#     page_title="4champz AI Sales CRM",
#     page_icon="Robot",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ==================== CUSTOM CSS ====================
# st.markdown("""
# <style>
#     .main-header {font-size: 2.5rem; font-weight: bold; color: #667eea; margin-bottom: 1rem;}
#     .metric-card {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         padding: 20px; border-radius: 10px; color: white; margin: 10px 0;
#         box-shadow: 0 4px 6px rgba(0,0,0,0.1);
#     }
#     .lead-card {
#         border-left: 4px solid #667eea; padding: 12px; margin: 8px 0;
#         background: white; border-radius: 5px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);
#     }
#     .agent-card {
#         border: 2px solid #667eea; border-radius: 10px; padding: 15px; margin: 10px 0;
#         background: #f8f9fa;
#     }
#     .status-badge {padding: 5px 10px; border-radius: 15px; font-size: 0.85rem; font-weight: bold;}
#     .status-active {background: #d4edda; color: #155724;}
#     .status-inactive {background: #f8d7da; color: #721c24;}
#     .status-qualified {background: #cfe2ff; color: #084298;}
#     .stButton>button {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         color: white; border: none; border-radius: 5px; padding: 0.5rem 1rem; font-weight: bold;
#     }
#     .stButton>button:hover {opacity: 0.9; transform: translateY(-2px); transition: 0.3s;}
#     .success-box {background: #d4edda; border: 1px solid #c3e6cb; padding: 10px; border-radius: 5px; margin: 10px 0;}
#     .warning-box {background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; border-radius: 5px; margin: 10px 0;}
# </style>
# """, unsafe_allow_html=True)

# # ==================== SESSION STATE ====================
# for key in ['authenticated', 'company_id', 'company_name', 'user_role', 'page']:
#     if key not in st.session_state:
#         st.session_state[key] = None

# # ==================== API HELPERS ====================
# def api_get(endpoint: str, params: Dict = None) -> Optional[Dict]:
#     try:
#         url = f"{API_BASE_URL}/{endpoint}"
#         response = requests.get(url, params=params, timeout=10)
#         response.raise_for_status()
#         return response.json()
#     except Exception as e:
#         st.error(f"API Error: {str(e)}")
#         return None

# def api_post(endpoint: str, data: Dict) -> Optional[Dict]:
#     try:
#         response = requests.post(f"{API_BASE_URL}/{endpoint}", json=data, timeout=10)
#         response.raise_for_status()
#         return response.json()
#     except Exception as e:
#         st.error(f"API Error: {str(e)}")
#         return None

# def api_patch(endpoint: str, data: Dict) -> Optional[Dict]:
#     try:
#         response = requests.patch(f"{API_BASE_URL}/{endpoint}", json=data, timeout=10)
#         response.raise_for_status()
#         return response.json()
#     except Exception as e:
#         st.error(f"API Error: {str(e)}")
#         return None

# def python_api_post(endpoint: str, data: Dict) -> Optional[Dict]:
#     try:
#         response = requests.post(f"{PYTHON_API_URL}/{endpoint}", json=data, timeout=30)
#         response.raise_for_status()
#         return response.json()
#     except Exception as e:
#         st.error(f"Python API Error: {str(e)}")
#         return None

# # ==================== AUTH ====================
# def render_login():
#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         st.markdown('<div class="main-header">4champz AI CRM</div>', unsafe_allow_html=True)
#         st.markdown("### Login to Your Dashboard")
#         with st.form("login_form"):
#             company_id = st.number_input("Company ID", min_value=1, value=1)
#             username = st.text_input("Username (demo: any)")
#             password = st.text_input("Password (demo: any)", type="password")
#             if st.form_submit_button("Login", use_container_width=True):
#                 company = api_get(f"companies/{company_id}")
#                 if company and company.get('success'):
#                     st.session_state.update({
#                         'authenticated': True,
#                         'company_id': company_id,
#                         'company_name': company['data']['name'],
#                         'user_role': 'admin'
#                     })
#                     st.rerun()
#                 else:
#                     st.error("Invalid Company ID")
#         st.info("Demo: Use Company ID 1, 2, or 3")

# # ==================== SIDEBAR ====================
# def render_sidebar():
#     with st.sidebar:
#         st.markdown(f"### {st.session_state.company_name}")
#         st.caption(f"ID: {st.session_state.company_id} | Role: {st.session_state.user_role}")
#         st.divider()
#         menu = {
#             "Dashboard": "dashboard",
#             # "Companies": "companies",
#             "AI Agents": "agents",
#             "Calling": "calling",
#             "WhatsApp": "whatsapp",
#             "Leads": "leads",
#             "Analytics": "analytics",
#             "Notifications": "notifications",
#             "Settings": "settings"
#         }
#         selected = st.radio("Navigation", list(menu.keys()), label_visibility="collapsed")
#         st.session_state.page = menu[selected]
#         st.divider()
#         if st.button("Logout", use_container_width=True):
#             for k in list(st.session_state.keys()):
#                 del st.session_state[k]
#             st.rerun()

# # ==================== PAGES ====================

# def page_dashboard():
#     st.markdown('<div class="main-header">Dashboard Overview</div>', unsafe_allow_html=True)
#     stats = api_get("stats/dashboard")
#     if not stats or not stats.get('success'):
#         st.warning("Unable to load data"); return
#     data = stats['data']

#     col1, col2, col3, col4 = st.columns(4)
#     metrics = [
#         ("Total Leads", 'total_leads'), 
#         ("Conversations", 'total_conversations'), 
#         ("Pending Invoices", 'pending_invoices'), 
#         ("Avg Interest", 'avg_interest_level')
#     ]
#     for col, (label, key) in zip([col1, col2, col3, col4], metrics):
#         with col:
#             st.markdown('<div class="metric-card">', unsafe_allow_html=True)
#             value = data.get(key, 0)
#             if key == 'avg_interest_level':
#                 try:
#                     value = f"{float(value):.1f}/10"
#                 except (ValueError, TypeError):
#                     value = "N/A"
#             st.metric(label, value)
#             st.markdown('</div>', unsafe_allow_html=True)

#     col1, col2 = st.columns(2)
#     with col1:
#         st.subheader("Leads by Status")
#         if data.get('leads_by_status'):
#             df = pd.DataFrame(data['leads_by_status'])
#             fig = px.pie(df, names='lead_status', values='count', hole=0.4)
#             st.plotly_chart(fig, use_container_width=True)
#     with col2:
#         st.subheader("Hot Leads Today")
#         hot = api_get("hot-leads")
#         if hot and hot.get('data'):
#             for lead in hot['data'][:5]:
#                 st.markdown(f"""
#                 <div class="lead-card">
#                     <b>{lead['name']}</b> • {lead['phone_number']}<br>
#                     <small>Tone: {lead.get('tone_score','N/A')} | Intent: {lead.get('intent','N/A')}</small>
#                 </div>
#                 """, unsafe_allow_html=True)

#     st.subheader("Recent Activity")
#     tab1, tab2 = st.tabs(["Calls", "Messages"])
#     with tab1:
#         calls = api_get(f"call-logs?company_id={st.session_state.company_id}&limit=10")
#         if calls and calls.get('data'):
#             df = pd.DataFrame(calls['data'])
#             df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
#             st.dataframe(df[['to_phone', 'call_status', 'call_duration', 'created_at']], use_container_width=True)
#     with tab2:
#         msg = api_get("stats/messages")
#         if msg and msg.get('data'):
#             st.dataframe(pd.DataFrame(msg['data']), use_container_width=True)

# # def page_companies():
# #     st.markdown('<div class="main-header">Companies Management</div>', unsafe_allow_html=True)
# #     tab1, tab2 = st.tabs(["View Companies", "Add New Company"])
# #     with tab1:
# #         companies = api_get("companies")
# #         if companies and companies.get('data'):
# #             df = pd.DataFrame(companies['data'])
# #             st.dataframe(df, use_container_width=True)
# #         else:
# #             st.info("No companies found")
# #     with tab2:
# #         with st.form("add_company"):
# #             name = st.text_input("Company Name*")
# #             phone = st.text_input("Phone Number*", placeholder="+919876543210")
# #             if st.form_submit_button("Create Company"):
# #                 if name and phone:
# #                     result = api_post("companies", {"name": name, "phone_number": phone})
# #                     if result and result.get('success'):
# #                         st.success(f"Company created! ID: {result.get('data', {}).get('id')}")
# #                         st.rerun()
# #                     else:
# #                         st.error("Failed to create company")
# #                 else:
# #                     st.warning("Please fill all required fields")

# def page_agents():
#     st.markdown('<div class="main-header">AI Agent Instances</div>', unsafe_allow_html=True)
#     tab1, tab2, tab3 = st.tabs(["My Agents", "Create New", "Apply Template"])
#     with tab1:
#         agents = api_get(f"agent-instances/company/{st.session_state.company_id}")
#         if agents and agents.get('data'):
#             for agent in agents['data']:
#                 with st.expander(f"{agent['agent_name']} ({agent['agent_type'].upper()})"):
#                     col1, col2, col3 = st.columns(3)
#                     with col1:
#                         st.write(f"**Phone:** {agent.get('phone_number', 'N/A')}")
#                         st.write(f"**WhatsApp:** {agent.get('whatsapp_number', 'N/A')}")
#                     with col2:
#                         status_class = "status-active" if agent['is_active'] else "status-inactive"
#                         status_text = "Active" if agent['is_active'] else "Inactive"
#                         st.markdown(f'<span class="status-badge {status_class}">{status_text}</span>', unsafe_allow_html=True)
#                         st.write(f"**Voice:** {agent.get('custom_voice') or agent.get('default_voice', 'N/A')}")
#                     with col3:
#                         st.write(f"**Created:** {agent['created_at'][:10]}")
#                     col_a, col_b = st.columns(2)
#                     with col_a:
#                         new_status = not agent['is_active']
#                         btn_text = "Deactivate" if agent['is_active'] else "Activate"
#                         if st.button(btn_text, key=f"toggle_{agent['id']}"):
#                             result = api_patch(f"agent-instances/{agent['id']}", {"is_active": new_status})
#                             if result: st.success(f"Agent {btn_text}d!"); time.sleep(1); st.rerun()
#                     with col_b:
#                         if st.button("View Webhook", key=f"webhook_{agent['id']}"):
#                             st.code(f"Webhook: {API_BASE_URL}/webhooks/whatsapp-universal")
#         else:
#             st.info("No agents found")
#     with tab2:
#         with st.form("create_agent"):
#             agent_name = st.text_input("Agent Name*")
#             agent_type = st.selectbox("Type*", ["voice", "whatsapp"])
#             col1, col2 = st.columns(2)
#             with col1:
#                 phone = st.text_input("Phone (Voice)", "")
#             with col2:
#                 whatsapp = st.text_input("WhatsApp Number", "")
#             prompt = st.text_area("Custom Prompt (Optional)", height=150)
#             voice = st.selectbox("Voice", ["Raveena", "Aditi", "Brian", "Matthew"])
#             if st.form_submit_button("Create Agent"):
#                 if not agent_name:
#                     st.error("Name required")
#                 else:
#                     data = {
#                         "company_id": st.session_state.company_id,
#                         "agent_name": agent_name,
#                         "agent_type": agent_type,
#                         "phone_number": phone or None,
#                         "whatsapp_number": whatsapp or None,
#                         "custom_prompt": prompt or None,
#                         "custom_voice": voice
#                     }
#                     result = api_post("agent-instances", data)
#                     if result and result.get('success'):
#                         st.success(f"Agent created! ID: {result['data']['id']}")
#                         time.sleep(2); st.rerun()
#     with tab3:
#         templates = api_get("extraction-templates")
#         if templates and templates.get('data'):
#             template_names = [t['template_name'] for t in templates['data']]
#             selected = st.selectbox("Template", template_names)
#             agent_id = st.number_input("Agent ID (optional)", 0)
#             if st.button("Apply Template"):
#                 template_id = next(t['id'] for t in templates['data'] if t['template_name'] == selected)
#                 result = api_post(f"companies/{st.session_state.company_id}/apply-template", {
#                     "template_id": template_id,
#                     "agent_instance_id": agent_id if agent_id > 0 else None
#                 })
#                 if result and result.get('success'):
#                     st.success(f"Template applied! {len(result['data'])} fields configured")

# def page_calling():
#     st.markdown('<div class="main-header">AI Calling System</div>', unsafe_allow_html=True)
#     tab1, tab2, tab3 = st.tabs(["Make Call", "Call Logs", "Schedule Call"])
#     with tab1:
#         with st.form("make_call"):
#             col1, col2 = st.columns(2)
#             with col1:
#                 lead_id = st.number_input("Lead ID", min_value=1)
#                 to_phone = st.text_input("Phone*", "")
#                 name = st.text_input("Name", "")
#             with col2:
#                 call_type = st.selectbox("Type", ["qualification", "reminder", "payment"])
#                 agents = api_get(f"agent-instances/company/{st.session_state.company_id}?agent_type=voice")
#                 agent_id = None
#                 if agents and agents.get('data'):
#                     opt = st.selectbox("Agent", ["Default"] + [f"{a['agent_name']}" for a in agents['data']])
#                     if opt != "Default":
#                         agent_id = next(a['id'] for a in agents['data'] if a['agent_name'] == opt)
#             if st.form_submit_button("Call Now"):
#                 data = {"company_id": st.session_state.company_id, "lead_id": lead_id, "to_phone": to_phone, "name": name, "call_type": call_type}
#                 result = python_api_post(f"outbound-call-agent?agent_instance_id={agent_id}" if agent_id else "outbound-call", data)
#                 if result and result.get('success'):
#                     st.success(f"Call SID: {result.get('call_sid')}")
#     with tab2:
#         calls = api_get(f"call-logs?company_id={st.session_state.company_id}&limit=50")
#         if calls and calls.get('data'):
#             for call in calls['data']:
#                 with st.expander(f"{call['to_phone']} - {call['call_status']}"):
#                     st.write(f"**Duration:** {call.get('call_duration',0)}s")
#                     if call.get('recording_url'):
#                         st.markdown(f"[Recording]({call['recording_url']})")
#                     if call.get('transcript'):
#                         st.text_area("Transcript", call['transcript'], height=100, disabled=True, key=f"t_{call['id']}")
#     with tab3:
#         with st.form("schedule_call"):
#             lead_id = st.number_input("Lead ID", 1)
#             call_type = st.selectbox("Type", ["qualification", "reminder"])
#             date = st.date_input("Date", datetime.now() + timedelta(days=1))
#             time_ = st.time_input("Time", datetime.now().time())
#             if st.form_submit_button("Schedule"):
#                 scheduled = datetime.combine(date, time_).isoformat()
#                 result = api_post("schedule-call", {
#                     "company_id": st.session_state.company_id,
#                     "lead_id": lead_id,
#                     "call_type": call_type,
#                     "scheduled_time": scheduled
#                 })
#                 if result and result.get('success'):
#                     st.success("Call scheduled!")

# def page_whatsapp():
#     st.markdown('<div class="main-header">WhatsApp Management</div>', unsafe_allow_html=True)
#     tab1, tab2, tab3 = st.tabs(["Send", "Conversations", "Setup"])
#     with tab1:
#         agents = api_get(f"agent-instances/company/{st.session_state.company_id}?agent_type=whatsapp")
#         if not agents or not agents.get('data'):
#             st.warning("No WhatsApp agent"); return
#         agent = st.selectbox("From", [f"{a['agent_name']}" for a in agents['data']])
#         agent_id = next(a['id'] for a in agents['data'] if a['agent_name'] == agent)
#         with st.form("send_wa"):
#             to = st.text_input("To Phone*")
#             msg = st.text_area("Message*")
#             if st.form_submit_button("Send"):
#                 result = api_post("whatsapp/send", {"to": to, "message": msg, "agent_instance_id": agent_id})
#                 if result and result.get('success'):
#                     st.success("Sent!")
#     with tab2:
#         phone = st.text_input("Search Phone")
#         if phone:
#             conv = api_get(f"conversations/{phone}")
#             if conv and conv.get('data'):
#                 st.text_area("History", conv['data'].get('conversation_history', ''), height=300)
#     with tab3:
#         st.code(f"Webhook URL: https://n8n-render-host-n0ym.onrender.com/webhook-test/webhook/whatsapp-trigger")
#         with st.form("wa_setup"):
#             agent_id = st.number_input("Agent ID", 1)
#             token = st.text_input("Access Token*", type="password")
#             phone_id = st.text_input("Phone Number ID*")
#             if st.form_submit_button("Save"):
#                 result = api_post(f"agent-instances/{agent_id}/whatsapp-credentials", {
#                     "access_token": token, "phone_number_id": phone_id
#                 })
#                 if result and result.get('success'):
#                     st.success("Saved!")
#                     st.code(f"Verify Token: {result.get('verify_token')}")

# def page_leads():
#     st.markdown('<div class="main-header">Lead Management</div>', unsafe_allow_html=True)
#     tab1, tab2, tab3 = st.tabs(["View Leads", "Add Lead", "Bulk Import"])
#     with tab1:
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             status = st.selectbox("Status", ["All", "new", "contacted", "qualified", "lost"])
#         with col2:
#             source = st.selectbox("Source", ["All", "whatsapp", "website", "google_ads", "meta_ads"])
#         with col3:
#             limit = st.number_input("Limit", 10, 500, 50)
#         params = {"limit": limit}
#         if status != "All": params["status"] = status
#         leads = api_get("leads", params=params)
#         if not leads or not leads.get('data'):
#             st.info("No leads"); return
#         for lead in leads['data']:
#             with st.expander(f"{lead['name']} - {lead['phone_number']} ({lead['lead_status']})"):
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     st.write(f"**Email:** {lead.get('email','N/A')}")
#                     st.write(f"**Source:** {lead['lead_source']}")
#                     st.write(f"**Interest:** {lead['interest_level']}/10")
#                 with col2:
#                     st.write(f"**Chess Rating:** {lead.get('chess_rating','N/A')}")
#                     st.write(f"**Location:** {lead.get('location','N/A')}")
#                     st.write(f"**Last Contact:** {lead.get('last_contacted','Never')[:10]}")
#                 col_a, col_b, col_c = st.columns(3)
#                 with col_a:
#                     if st.button("Call", key=f"call_{lead['id']}"):
#                         st.session_state.call_lead = lead
#                 with col_b:
#                     if st.button("WhatsApp", key=f"wa_{lead['id']}"):
#                         st.session_state.wa_lead = lead
#                 with col_c:
#                     if st.button("Edit", key=f"edit_{lead['id']}"):
#                         with st.form(f"edit_{lead['id']}"):
#                             new_status = st.selectbox("Status", ["new", "contacted", "qualified", "lost"], index=["new", "contacted", "qualified", "lost"].index(lead['lead_status']), key=f"status_{lead['id']}")
#                             interest = st.slider("Interest", 1, 10, lead['interest_level'], key=f"int_{lead['id']}")
#                             if st.form_submit_button("Update"):
#                                 api_patch(f"leads/{lead['id']}", {"lead_status": new_status, "interest_level": interest})
#                                 st.success("Updated"); st.rerun()
#     with tab2:
#         with st.form("add_lead"):
#             col1, col2 = st.columns(2)
#             with col1:
#                 phone = st.text_input("Phone Number*")
#                 name = st.text_input("Name")
#                 email = st.text_input("Email")
#                 source = st.selectbox("Source", ["whatsapp", "website", "google_ads", "meta_ads"])
#             with col2:
#                 chess = st.number_input("Chess Rating", 0, 3000, 0)
#                 location = st.text_input("Location")
#                 interest = st.slider("Interest", 1, 10, 5)
#             if st.form_submit_button("Add Lead"):
#                 if phone:
#                     result = api_post("leads", {
#                         "phone_number": phone, "name": name, "email": email, "lead_source": source,
#                         "interest_level": interest, "chess_rating": chess if chess > 0 else None, "location": location
#                     })
#                     if result and result.get('success'):
#                         st.success(f"Lead added! ID: {result['data']['id']}")
#                         st.rerun()
#     with tab3:
#         uploaded = st.file_uploader("Upload CSV", type="csv")
#         if uploaded:
#             df = pd.read_csv(uploaded)
#             st.dataframe(df.head())
#             if st.button("Import All"):
#                 result = api_post("leads/bulk", {"leads": df.to_dict('records')})
#                 if result and result.get('success'):
#                     st.success(f"Imported {result.get('imported')} leads!")

# def page_analytics():
#     st.markdown('<div class="main-header">Analytics</div>', unsafe_allow_html=True)
#     tab1, tab2, tab3 = st.tabs(["Call", "Lead", "Revenue"])
#     with tab1:
#         metrics = api_get("metrics/dashboard")
#         if metrics and metrics.get('data'):
#             data = metrics['data']
#             col1, col2, col3 = st.columns(3)
#             with col1: st.metric("Active Calls", data.get('active_calls',0))
#             with col2: st.metric("Calls (24h)", sum(c.get('count',0) for c in data.get('calls_24h',[])))
#             with col3: st.metric("Success Rate", f"{data.get('success_rate',0)}%")
#     with tab2:
#         stats = api_get("stats/leads")
#         if stats and stats.get('data'):
#             df = pd.DataFrame(stats['data'])
#             fig = px.bar(df, x='lead_status', y='count', color='lead_status')
#             st.plotly_chart(fig, use_container_width=True)
#     with tab3:
#         st.info("Revenue tracking coming soon...")

# def page_notifications():
#     st.markdown('<div class="main-header">Notifications</div>', unsafe_allow_html=True)
#     tab1, tab2 = st.tabs(["Recent", "Alerts"])
#     with tab1:
#         notifs = api_get("system-notifications?limit=20")
#         if notifs and notifs.get('data'):
#             for n in notifs['data']:
#                 with st.expander(f"{n['title']} - {n['created_at'][:16]}"):
#                     st.write(n['message'])
#                     if not n.get('is_read') and st.button("Mark Read", key=f"read_{n['id']}"):
#                         api_post(f"system-notifications/{n['id']}/read", {})
#                         st.rerun()
#     with tab2:
#         alerts = api_get("alerts?limit=20")
#         if alerts and alerts.get('data'):
#             for a in alerts['data']:
#                 with st.expander(f"{a['title']} - {a['created_at'][:16]}"):
#                     st.write(a['message'])

# def page_settings():
#     st.markdown('<div class="main-header">Settings</div>', unsafe_allow_html=True)
#     tab1, tab2, tab3, tab4 = st.tabs(["Human Agents", "Custom Fields", "Integrations", "System"])
#     with tab1:
#         agents = api_get("human-agents")
#         if agents and agents.get('data'):
#             for a in agents['data']:
#                 with st.expander(f"{a['name']}"):
#                     st.write(f"**Email:** {a['email']} | **Status:** {a['status']}")
#                     new = st.selectbox("Status", ["available", "busy", "offline"], key=f"s_{a['id']}")
#                     if st.button("Update", key=f"u_{a['id']}"):
#                         api_patch(f"human-agents/{a['id']}/status", {"status": new})
#                         st.success("Updated")
#     with tab2:
#         templates = api_get("extraction-templates")
#         if templates and templates.get('data'):
#             for t in templates['data']:
#                 with st.expander(f"{t['template_name']}"):
#                     st.write(t['description'])
#     with tab3:
#         st.info("Twilio, WhatsApp, Stripe: Connected")
#     with tab4:
#         health = api_get("health")
#         if health:
#             st.json(health)

# # ==================== MAIN ====================
# def main():
#     if not st.session_state.authenticated:
#         render_login()
#         return
#     render_sidebar()
#     page = st.session_state.get('page', 'dashboard')
#     globals()[f"page_{page}"]()

# if __name__ == "__main__":
#     main()

































# import streamlit as st
# import requests
# import pandas as pd
# import json
# from datetime import datetime, timedelta
# import plotly.express as px
# import plotly.graph_objects as go
# from typing import Optional, Dict, List
# import time

# # ==================== CONFIGURATION ====================
# API_BASE_URL = "http://localhost:3000/api"        # Change if needed
# PYTHON_API_URL = "http://localhost:8000/api"      # Change if needed

# # Page config
# st.set_page_config(
#     page_title="AI Sales CRM",
#     page_icon="🤖",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS
# st.markdown("""
# <style>
#     .metric-card {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         padding: 20px;
#         border-radius: 10px;
#         color: white;
#         margin: 10px 0;
#     }
#     .stButton>button {
#         width: 100%;
#         background-color: #667eea;
#         color: white;
#         border-radius: 5px;
#         border: none;
#         padding: 10px;
#     }
#     .stButton>button:hover {
#         background-color: #5568d3;
#     }
#     .success-box {
#         background-color: #d4edda;
#         border: 1px solid #c3e6cb;
#         padding: 15px;
#         border-radius: 5px;
#         margin: 10px 0;
#     }
#     .warning-box {
#         background-color: #fff3cd;
#         border: 1px solid #ffeaa7;
#         padding: 15px;
#         border-radius: 5px;
#         margin: 10px 0;
#     }
#     .error-box {
#         background-color: #f8d7da;
#         border: 1px solid #f5c6cb;
#         padding: 15px;
#         border-radius: 5px;
#         margin: 10px 0;
#     }
#     .lead-card {
#         background: white;
#         border: 1px solid #e0e0e0;
#         border-radius: 8px;
#         padding: 15px;
#         margin: 10px 0;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#     }
# </style>
# """, unsafe_allow_html=True)

# # ==================== SESSION STATE ====================
# if 'authenticated' not in st.session_state:
#     st.session_state.authenticated = False
# if 'company_id' not in st.session_state:
#     st.session_state.company_id = None
# if 'company_name' not in st.session_state:
#     st.session_state.company_name = None
# if 'user_role' not in st.session_state:
#     st.session_state.user_role = "admin"

# # ==================== API HELPERS ====================
# def api_get(endpoint: str, timeout: int = 10) -> Optional[Dict]:
#     """GET request to API"""
#     try:
#         response = requests.get(f"{API_BASE_URL}/{endpoint}", timeout=timeout)
#         response.raise_for_status()
#         return response.json()
#     except Exception as e:
#         st.error(f"API Error: {str(e)}")
#         return None

# def api_post(endpoint: str, data: Dict, timeout: int = 10) -> Optional[Dict]:
#     """POST request to API"""
#     try:
#         response = requests.post(f"{API_BASE_URL}/{endpoint}", json=data, timeout=timeout)
#         response.raise_for_status()
#         return response.json()
#     except Exception as e:
#         st.error(f"API Error: {str(e)}")
#         return None

# def api_patch(endpoint: str, data: Dict, timeout: int = 10) -> Optional[Dict]:
#     """PATCH request to API"""
#     try:
#         response = requests.patch(f"{API_BASE_URL}/{endpoint}", json=data, timeout=timeout)
#         response.raise_for_status()
#         return response.json()
#     except Exception as e:
#         st.error(f"API Error: {str(e)}")
#         return None

# def python_api_post(endpoint: str, data: Dict, timeout: int = 30) -> Optional[Dict]:
#     """POST to Python AI API"""
#     try:
#         response = requests.post(f"{PYTHON_API_URL}/{endpoint}", json=data, timeout=timeout)
#         response.raise_for_status()
#         return response.json()
#     except Exception as e:
#         st.error(f"Python API Error: {str(e)}")
#         return None

# # ==================== SIDEBAR NAVIGATION ====================
# def render_sidebar():
#     with st.sidebar:
#         st.title("🤖 AI Sales CRM")
#         st.markdown(f"**Company:** {st.session_state.company_name}")
#         st.markdown(f"**Role:** {st.session_state.user_role}")
#         st.divider()
        
#         menu_options = {
#             "📊 Dashboard": "dashboard",
#             "👥 Leads": "leads",
#             "🤖 AI Agents": "agents",
#             "📞 Calling": "calling",
#             "💬 WhatsApp": "whatsapp",
#             "👨‍💼 Human Agents": "human_agents",
#             "📈 Analytics": "analytics",
#             "🔔 Notifications": "notifications",
#             "⚙️ Settings": "settings"
#         }
        
#         selected = st.radio("Navigation", list(menu_options.keys()), label_visibility="collapsed")
#         st.session_state.page = menu_options[selected]
        
#         st.divider()
        
#         if st.button("🚪 Logout"):
#             st.session_state.authenticated = False
#             st.session_state.company_id = None
#             st.session_state.company_name = None
#             st.rerun()

# # ==================== PAGE: DASHBOARD ====================
# def page_dashboard():
#     st.title("📊 Dashboard Overview")
    
#     stats = api_get("stats/dashboard")
#     if not stats or not stats.get('success'):
#         st.warning("Unable to load dashboard data")
#         return
    
#     data = stats.get('data', {})
    
#     # Top Metrics
#     col1, col2, col3, col4 = st.columns(4)
    
#     with col1:
#         st.markdown('<div class="metric-card">', unsafe_allow_html=True)
#         st.metric("Total Leads", data.get('total_leads', 0))
#         st.markdown('</div>', unsafe_allow_html=True)
    
#     with col2:
#         st.markdown('<div class="metric-card">', unsafe_allow_html=True)
#         st.metric("Conversations", data.get('total_conversations', 0))
#         st.markdown('</div>', unsafe_allow_html=True)
    
#     with col3:
#         st.markdown('<div class="metric-card">', unsafe_allow_html=True)
#         st.metric("Pending Invoices", data.get('pending_invoices', 0))
#         st.markdown('</div>', unsafe_allow_html=True)
    
#     with col4:
#         st.markdown('<div class="metric-card">', unsafe_allow_html=True)
#         st.metric("Avg Interest", f"{data.get('avg_interest_level', 0)}/10")
#         st.markdown('</div>', unsafe_allow_html=True)
    
#     # Charts
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.subheader("📈 Leads by Status")
#         status_data = data.get('leads_by_status', [])
#         if status_data:
#             df = pd.DataFrame(status_data)
#             fig = px.pie(df, names='lead_status', values='count', hole=0.4)
#             st.plotly_chart(fig, use_container_width=True)
    
#     with col2:
#         st.subheader("🔥 Hot Leads")
#         hot_leads_resp = api_get("hot-leads")
#         if hot_leads_resp and hot_leads_resp.get('success'):
#             df = pd.DataFrame(hot_leads_resp['data'][:5])
#             if not df.empty:
#                 st.dataframe(df[['name', 'phone_number', 'tone_score', 'intent']], use_container_width=True)
#             else:
#                 st.info("No hot leads today")
    
#     # Recent Activity
#     st.subheader("📋 Recent Activity")
    
#     tab1, tab2 = st.tabs(["Calls", "Messages"])
    
#     with tab1:
#         calls_resp = api_get(f"call-logs?company_id={st.session_state.company_id}&limit=10")
#         if calls_resp and calls_resp.get('success'):
#             df = pd.DataFrame(calls_resp['data'])
#             if not df.empty:
#                 df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
#                 st.dataframe(df[['call_sid', 'to_phone', 'call_status', 'call_duration', 'created_at']], 
#                            use_container_width=True)
    
#     with tab2:
#         messages_resp = api_get("stats/messages")
#         if messages_resp and messages_resp.get('success'):
#             df = pd.DataFrame(messages_resp['data'])
#             st.dataframe(df, use_container_width=True)

# # ==================== PAGE: LEADS ====================
# def page_leads():
#     st.title("👥 Lead Management")
    
#     # Filter options
#     col1, col2, col3, col4 = st.columns(4)
#     with col1:
#         status_filter = st.selectbox("Status", ["All", "new", "contacted", "qualified", "lost"])
#     with col2:
#         source_filter = st.selectbox("Source", ["All", "whatsapp", "website", "google_ads", "meta_ads"])
#     with col3:
#         limit = st.number_input("Limit", min_value=10, max_value=500, value=50)
#     with col4:
#         if st.button("🔍 Search"):
#             st.rerun()
    
#     # Build query
#     query_params = f"limit={limit}"
#     if status_filter != "All":
#         query_params += f"&status={status_filter}"
    
#     leads_resp = api_get(f"leads?{query_params}")
    
#     if not leads_resp or not leads_resp.get('success'):
#         st.warning("No leads found")
#         return
    
#     leads = leads_resp['data']
    
#     # Display leads as cards
#     for lead in leads:
#         with st.expander(f"📋 {lead.get('name', 'Unknown')} - {lead['phone_number']}"):
#             render_lead_detail(lead)

# def render_lead_detail(lead: Dict):
#     """Render detailed lead information"""
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.markdown("### Basic Info")
#         st.write(f"**ID:** {lead['id']}")
#         st.write(f"**Phone:** {lead['phone_number']}")
#         st.write(f"**Email:** {lead.get('email', 'N/A')}")
#         st.write(f"**Status:** {lead['lead_status']}")
#         st.write(f"**Interest:** {lead.get('interest_level', 0)}/10")
#         st.write(f"**Source:** {lead.get('lead_source', 'N/A')}")
    
#     with col2:
#         st.markdown("### Custom Fields")
#         st.write(f"**Chess Rating:** {lead.get('chess_rating', 'N/A')}")
#         st.write(f"**Location:** {lead.get('location', 'N/A')}")
#         st.write(f"**Availability:** {lead.get('availability', 'N/A')}")
#         st.write(f"**Last Contact:** {lead.get('last_contacted', 'N/A')[:10] if lead.get('last_contacted') else 'Never'}")
    
#     st.divider()
    
#     # Actions
#     st.markdown("### Quick Actions")
    
#     col1, col2, col3, col4 = st.columns(4)
    
#     with col1:
#         if st.button("📞 Make Call", key=f"call_{lead['id']}"):
#             st.session_state.selected_lead_for_call = lead
#             st.session_state.page = 'calling'
#             st.rerun()
    
#     with col2:
#         if st.button("💬 Send WhatsApp", key=f"whatsapp_{lead['id']}"):
#             st.session_state.selected_lead_for_whatsapp = lead
#             st.session_state.page = 'whatsapp'
#             st.rerun()
    
#     with col3:
#         if st.button("📅 Schedule Call", key=f"schedule_{lead['id']}"):
#             with st.form(f"schedule_form_{lead['id']}"):
#                 call_type = st.selectbox("Type", ["qualification", "reminder", "payment"])
#                 scheduled_date = st.date_input("Date", value=datetime.now() + timedelta(days=1))
#                 scheduled_time = st.time_input("Time")
                
#                 if st.form_submit_button("Schedule"):
#                     scheduled_datetime = datetime.combine(scheduled_date, scheduled_time).isoformat()
#                     result = api_post("schedule-call", {
#                         "company_id": st.session_state.company_id,
#                         "lead_id": lead['id'],
#                         "call_type": call_type,
#                         "scheduled_time": scheduled_datetime
#                     })
#                     if result and result.get('success'):
#                         st.success("Call scheduled!")
#                     else:
#                         st.error("Failed to schedule")
    
#     with col4:
#         if st.button("📝 Edit Lead", key=f"edit_{lead['id']}"):
#             with st.form(f"edit_form_{lead['id']}"):
#                 new_status = st.selectbox("Status", ["new", "contacted", "qualified", "lost"], 
#                                         index=["new", "contacted", "qualified", "lost"].index(lead['lead_status']))
#                 new_interest = st.slider("Interest Level", 1, 10, lead.get('interest_level', 5))
#                 notes = st.text_area("Notes", value=lead.get('notes', ''))
                
#                 if st.form_submit_button("Update"):
#                     result = api_patch(f"leads/{lead['id']}", {
#                         "lead_status": new_status,
#                         "interest_level": new_interest,
#                         "notes": notes
#                     })
#                     if result and result.get('success'):
#                         st.success("Lead updated!")
#                         st.rerun()
    
#     # Conversation History
#     st.divider()
#     st.markdown("### Conversation History")
    
#     conv_resp = api_get(f"conversations/{lead['phone_number']}")
#     if conv_resp and conv_resp.get('success') and conv_resp.get('data'):
#         conv_data = conv_resp['data']
#         st.text_area("Conversation", value=conv_data.get('conversation_history', ''), height=200, key=f"conv_{lead['id']}")
#     else:
#         st.info("No conversation history yet")
    
#     # Call Logs
#     st.divider()
#     st.markdown("### Call History")
    
#     calls_resp = api_get(f"call-logs/lead/{lead['id']}")
#     if calls_resp and calls_resp.get('success') and calls_resp.get('data'):
#         for call in calls_resp['data'][:3]:
#             st.write(f"**{call['call_type']}** - {call['call_status']} - {call['created_at'][:16]}")
#             if call.get('transcript'):
#                 with st.expander("View Transcript"):
#                     st.text(call['transcript'][:500])

# # ==================== PAGE: AI AGENTS ====================
# def page_agents():
#     st.title("🤖 AI Agent Management")
    
#     tab1, tab2 = st.tabs(["My Agents", "Create New Agent"])
    
#     with tab1:
#         agents_resp = api_get(f"agent-instances/company/{st.session_state.company_id}")
        
#         if not agents_resp or not agents_resp.get('success'):
#             st.info("No agents configured yet")
#             return
        
#         for agent in agents_resp['data']:
#             with st.expander(f"🤖 {agent['agent_name']} ({agent['agent_type']})"):
#                 col1, col2 = st.columns(2)
                
#                 with col1:
#                     st.write(f"**ID:** {agent['id']}")
#                     st.write(f"**Type:** {agent['agent_type']}")
#                     st.write(f"**Phone:** {agent.get('phone_number', 'N/A')}")
#                     st.write(f"**WhatsApp:** {agent.get('whatsapp_number', 'N/A')}")
#                     st.write(f"**Status:** {'🟢 Active' if agent['is_active'] else '🔴 Inactive'}")
                
#                 with col2:
#                     st.write(f"**Created:** {agent['created_at'][:10]}")
#                     st.write(f"**Voice:** {agent.get('custom_voice', agent.get('default_voice', 'N/A'))}")
#                     st.write(f"**Model:** {agent.get('model_name', 'N/A')}")
                
#                 if agent.get('custom_prompt'):
#                     with st.expander("View Custom Prompt"):
#                         st.text_area("Prompt", value=agent['custom_prompt'], height=200, key=f"prompt_{agent['id']}")
    
#     with tab2:
#         st.subheader("Create New AI Agent")
        
#         with st.form("create_agent"):
#             agent_name = st.text_input("Agent Name*", placeholder="Chess Coach AI")
#             agent_type = st.selectbox("Type*", ["voice", "whatsapp"])
            
#             if agent_type == "voice":
#                 phone_number = st.text_input("Phone Number", placeholder="+919876543210")
#             else:
#                 whatsapp_number = st.text_input("WhatsApp Number", placeholder="+919876543210")
            
#             custom_prompt = st.text_area("Custom Prompt (optional)", height=200, 
#                 placeholder="You are Priya from 4champz...")
            
#             voice = st.selectbox("Voice", ["Raveena", "Aditi", "Brian", "Matthew"])
            
#             if st.form_submit_button("Create Agent"):
#                 data = {
#                     "company_id": st.session_state.company_id,
#                     "agent_name": agent_name,
#                     "agent_type": agent_type,
#                     "phone_number": phone_number if agent_type == "voice" else None,
#                     "whatsapp_number": whatsapp_number if agent_type == "whatsapp" else None,
#                     "custom_prompt": custom_prompt if custom_prompt else None,
#                     "custom_voice": voice
#                 }
                
#                 result = api_post("agent-instances", data)
#                 if result and result.get('success'):
#                     st.success(f"✅ Agent created! ID: {result['data']['id']}")
#                     st.rerun()
#                 else:
#                     st.error("Failed to create agent")

# # ==================== PAGE: CALLING ====================
# def page_calling():
#     st.title("📞 AI Calling System")
    
#     tab1, tab2 = st.tabs(["Make Call", "Call Logs"])
    
#     with tab1:
#         st.subheader("🚀 Initiate Outbound Call")
        
#         with st.form("make_call"):
#             col1, col2 = st.columns(2)
            
#             with col1:
#                 lead_id = st.number_input("Lead ID*", min_value=1, value=1)
#                 to_phone = st.text_input("Phone Number*", placeholder="+919876543210")
#                 name = st.text_input("Name", placeholder="Ajsal")
            
#             with col2:
#                 call_type = st.selectbox("Call Type", ["qualification", "reminder", "payment", "support"])
                
#                 # Get agents for this company
#                 agents_resp = api_get(f"agent-instances/company/{st.session_state.company_id}?agent_type=voice")
#                 agent_options = {}
#                 if agents_resp and agents_resp.get('success'):
#                     agent_options = {f"{a['agent_name']} ({a['id']})": a['id'] for a in agents_resp['data']}
                
#                 if agent_options:
#                     agent_select = st.selectbox("Select Agent", ["Default"] + list(agent_options.keys()))
#                     agent_instance_id = agent_options.get(agent_select, None)
#                 else:
#                     st.warning("No voice agents configured")
#                     agent_instance_id = None
            
#             if st.form_submit_button("📞 Make Call Now"):
#                 if to_phone:
#                     data = {
#                         "company_id": st.session_state.company_id,
#                         "lead_id": lead_id,
#                         "to_phone": to_phone,
#                         "name": name,
#                         "call_type": call_type
#                     }
                    
#                     if agent_instance_id:
#                         result = python_api_post(f"outbound-call-agent?agent_instance_id={agent_instance_id}", data)
#                     else:
#                         result = python_api_post("outbound-call", data)
                    
#                     if result and result.get('success'):
#                         st.success(f"✅ Call initiated! SID: {result.get('call_sid')}")
#                     else:
#                         st.error("Failed to initiate call")
#                 else:
#                     st.warning("Phone number is required")
    
#     with tab2:
#         st.subheader("📋 Recent Call Logs")
        
#         calls_resp = api_get(f"call-logs?company_id={st.session_state.company_id}&limit=50")
        
#         if calls_resp and calls_resp.get('success'):
#             df = pd.DataFrame(calls_resp['data'])
#             if not df.empty:
#                 df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
                
#                 for idx, row in df.iterrows():
#                     with st.expander(f"📞 {row['to_phone']} - {row['call_status']} - {row['created_at']}"):
#                         col1, col2, col3 = st.columns(3)
#                         with col1:
#                             st.write(f"**Duration:** {row.get('call_duration', 0)}s")
#                             st.write(f"**Type:** {row.get('call_type', 'N/A')}")
#                         with col2:
#                             st.write(f"**Status:** {row['call_status']}")
#                             st.write(f"**Call SID:** {row['call_sid'][:20]}...")
#                         with col3:
#                             if row.get('recording_url'):
#                                 st.markdown(f"[🎵 Recording]({row['recording_url']})")
                        
#                         if row.get('transcript'):
#                             st.text_area("Transcript", row['transcript'], height=150, key=f"transcript_{idx}")

# # ==================== PAGE: WHATSAPP ====================
# def page_whatsapp():
#     st.title("💬 WhatsApp Management")
    
#     tab1, tab2, tab3 = st.tabs(["Send Message", "Conversations", "Setup"])
    
#     with tab1:
#         st.subheader("📤 Send WhatsApp Message")
        
#         # Get WhatsApp agents
#         agents_resp = api_get(f"agent-instances/company/{st.session_state.company_id}?agent_type=whatsapp")
        
#         if not agents_resp or not agents_resp.get('success') or not agents_resp['data']:
#             st.warning("⚠️ No WhatsApp agents configured. Please setup in 'Setup' tab.")
#             return
        
#         agent_options = {f"{a['agent_name']} ({a['whatsapp_number']})": a['id'] for a in agents_resp['data']}
        
#         with st.form("send_whatsapp"):
#             agent_select = st.selectbox("From Agent", list(agent_options.keys()))
#             agent_id = agent_options[agent_select]
            
#             to_phone = st.text_input("To Phone*", placeholder="+919876543210")
#             message = st.text_area("Message*", height=150)
            
#             if st.form_submit_button("Send Message"):
#                 if to_phone and message:
#                     result = api_post("whatsapp/send", {
#                         "to": to_phone,
#                         "message": message,
#                         "agent_instance_id": agent_id
#                     })
#                     if result and result.get('success'):
#                         st.success("✅ Message sent!")
#                     else:
#                         st.error("Failed to send message")
#                 else:
#                     st.warning("Phone and message are required")
    
#     with tab2:
#         st.subheader("💬 Recent Conversations")
        
#         phone_search = st.text_input("Search by phone", placeholder="+919876543210")
        
#         if phone_search:
#             conv_resp = api_get(f"conversations/{phone_search}")
#             if conv_resp and conv_resp.get('success') and conv_resp.get('data'):
#                 data = conv_resp['data']
#                 st.write(f"**Name:** {data.get('name', 'N/A')}")
#                 st.write(f"**Status:** {data.get('lead_status', 'N/A')}")
#                 st.text_area("Conversation History", data.get('conversation_history', ''), height=300)
#             else:
#                 st.warning("No conversation found")
    
#     with tab3:
#         st.subheader("⚙️ WhatsApp Setup")
        
#         st.markdown("""
#         ### Setup Instructions
        
#         1. **Create WhatsApp AI Agent** (if not already done)
#         2. **Get Meta WhatsApp Business API Credentials**
#         3. **Configure webhook in Meta**
        
#         #### Webhook URL
#         Copy this URL and paste in Meta Developer Console:
#         """)
        
#         webhook_url = f"{API_BASE_URL.replace('/api', '')}/api/webhooks/whatsapp-universal"
#         st.code(webhook_url)
        
#         st.markdown("#### Configure Credentials")
        
#         # Get existing agents
#         agents_resp = api_get(f"agent-instances/company/{st.session_state.company_id}?agent_type=whatsapp")
        
#         if agents_resp and agents_resp.get('success') and agents_resp['data']:
#             agent_options = {f"{a['agent_name']} (ID: {a['id']})": a['id'] for a in agents_resp['data']}
            
#             with st.form("whatsapp_credentials"):
#                 agent_select = st.selectbox("Select Agent", list(agent_options.keys()))
#                 agent_id = agent_options[agent_select]
                
#                 st.markdown("**Meta WhatsApp Business API Credentials:**")
#                 access_token = st.text_input("Access Token*", type="password")
#                 phone_number_id = st.text_input("Phone Number ID*")
#                 business_account_id = st.text_input("Business Account ID")
                
#                 if st.form_submit_button("Save Credentials"):
#                     result = api_post(f"agent-instances/{agent_id}/whatsapp-credentials", {
#                         "access_token": access_token,
#                         "phone_number_id": phone_number_id,
#                         "business_account_id": business_account_id
#                     })
#                     if result and result.get('success'):
#                         st.success("✅ Credentials saved!")
#                         st.info(f"**Webhook URL:** {result.get('webhook_url')}")
#                         st.info(f"**Verify Token:** {result.get('verify_token')}")
#                     else:
#                         st.error("Failed to save credentials")
#         else:
#             st.info("Create a WhatsApp agent first in 'AI Agents' page")

# # ==================== PAGE: HUMAN AGENTS ====================
# def page_human_agents():
#     st.title("👨‍💼 Human Sales Agents")
    
#     tab1, tab2 = st.tabs(["View Agents", "Takeover Requests"])
    
#     with tab1:
#         agents_resp = api_get("human-agents")
        
#         if agents_resp and agents_resp.get('success'):
#             for agent in agents_resp['data']:
#                 with st.expander(f"👤 {agent['name']} - {agent['role']}"):
#                     col1, col2 = st.columns(2)
                    
#                     with col1:
#                         st.write(f"**Email:** {agent['email']}")
#                         st.write(f"**Phone:** {agent.get('phone', 'N/A')}")
#                         st.write(f"**Status:** {agent['status']}")
                    
#                     with col2:
#                         st.write(f"**Assigned Leads:** {agent['assigned_leads']}")
#                         st.write(f"**Max Concurrent:** {agent['max_concurrent_leads']}")
                    
#                     new_status = st.selectbox(
#                         "Change Status",
#                         ["available", "busy", "offline"],
#                         key=f"status_{agent['id']}"
#                     )
                    
#                     if st.button("Update Status", key=f"update_{agent['id']}"):
#                         result = api_patch(f"human-agents/{agent['id']}/status", {"status": new_status})
#                         if result and result.get('success'):
#                             st.success("Status updated")
#                             st.rerun()
    
#     with tab2:
#         st.subheader("🔥 Pending Takeover Requests")
        
#         # This would show takeover requests for company's leads
#         st.info("Feature coming soon - view AI-to-human handoff requests")

# # ==================== PAGE: ANALYTICS ====================
# def page_analytics():
#     st.title("📈 Analytics & Reports")
    
#     tab1, tab2 = st.tabs(["Call Analytics", "Lead Analytics"])
    
#     with tab1:
#         st.subheader("📞 Call Performance")
        
#         metrics_resp = api_get("metrics/dashboard")
#         if metrics_resp and metrics_resp.get('success'):
#             data = metrics_resp['data']
            
#             col1, col2, col3 = st.columns(3)
#             with col1:
#                 st.metric("Active Calls", data.get('active_calls', 0))
#             with col2:
#                 calls_24h = data.get('calls_24h', [])
#                 total_calls = sum([c.get('count', 0) for c in calls_24h]) if calls_24h else 0
#                 st.metric("Calls (24h)", total_calls)
#             with col3:
#                 st.metric("Success Rate", f"{data.get('success_rate', 0)}%")
            
#             # Sentiment distribution
#             sentiment_data = data.get('sentiment_distribution', [])
#             if sentiment_data:
#                 st.subheader("😊 Sentiment Distribution")
#                 df = pd.DataFrame(sentiment_data)
#                 fig = px.bar(df, x='sentiment_type', y='count', color='sentiment_type')
#                 st.plotly_chart(fig, use_container_width=True)
    
#     with tab2:
#         st.subheader("👥 Lead Analytics")
        
#         lead_stats_resp = api_get("stats/leads")
#         if lead_stats_resp and lead_stats_resp.get('success'):
#             df = pd.DataFrame(lead_stats_resp['data'])
            
#             if not df.empty:
#                 fig = px.bar(df, x='lead_status', y='count', color='lead_status',
#                             title="Leads by Status")
#                 st.plotly_chart(fig, use_container_width=True)
                
#                 # Average interest by status
#                 fig2 = px.scatter(df, x='lead_status', y='avg_interest', size='count',
#                                  title="Average Interest Level by Status")
#                 st.plotly_chart(fig2, use_container_width=True)

# # ==================== PAGE: NOTIFICATIONS ====================
# def page_notifications():
#     st.title("🔔 Notifications & Alerts")
    
#     tab1, tab2 = st.tabs(["Recent Notifications", "Alerts"])
    
#     with tab1:
#         notif_resp = api_get("system-notifications?limit=50")
        
#         if notif_resp and notif_resp.get('success'):
#             for notif in notif_resp['data']:
#                 priority_emoji = {
#                     'urgent': '🚨',
#                     'high': '⚠️',
#                     'normal': 'ℹ️',
#                     'low': '💡'
#                 }
                
#                 emoji = priority_emoji.get(notif.get('priority', 'normal'), 'ℹ️')
                
#                 with st.expander(f"{emoji} {notif['title']} - {notif['created_at'][:16]}"):
#                     st.write(notif['message'])
                    
#                     if not notif.get('is_read'):
#                         if st.button("Mark as Read", key=f"read_{notif['id']}"):
#                             result = api_post(f"system-notifications/{notif['id']}/read", {})
#                             if result and result.get('success'):
#                                 st.success("Marked as read")
#                                 st.rerun()
#         else:
#             st.info("No notifications")
    
#     with tab2:
#         alerts_resp = api_get("alerts?limit=20")
        
#         if alerts_resp and alerts_resp.get('success'):
#             for alert in alerts_resp['data']:
#                 severity_color = {
#                     'critical': '🔴',
#                     'high': '🟠',
#                     'normal': '🟡',
#                     'low': '🟢'
#                 }
                
#                 icon = severity_color.get(alert.get('severity', 'normal'), '🟡')
                
#                 with st.expander(f"{icon} {alert['title']} - {alert['created_at'][:16]}"):
#                     st.write(alert['message'])
#                     st.caption(f"Severity: {alert.get('severity', 'normal')}")
#         else:
#             st.info("No alerts")

# # ==================== PAGE: SETTINGS ====================
# def page_settings():
#     st.title("⚙️ Settings & Configuration")
    
#     tab1, tab2, tab3 = st.tabs(["Company Info", "Custom Fields", "Integrations"])
    
#     with tab1:
#         st.subheader("🏢 Company Information")
        
#         company_resp = api_get(f"companies/{st.session_state.company_id}")
#         if company_resp and company_resp.get('success'):
#             company = company_resp['data']
            
#             with st.form("update_company"):
#                 name = st.text_input("Company Name", value=company.get('name', ''))
#                 phone = st.text_input("Phone Number", value=company.get('phone_number', ''))
                
#                 if st.form_submit_button("Update Company"):
#                     st.info("Company update feature coming soon")
        
#         st.divider()
        
#         st.subheader("🕐 Calling Hours Configuration")
        
#         with st.form("calling_hours"):
#             col1, col2 = st.columns(2)
#             with col1:
#                 start_hour = st.number_input("Start Hour (24h)", 0, 23, 9)
#             with col2:
#                 end_hour = st.number_input("End Hour (24h)", 0, 23, 18)
            
#             call_rate = st.number_input("Calls per Minute", 1, 10, 2)
#             max_concurrent = st.number_input("Max Concurrent Calls", 1, 20, 5)
            
#             if st.form_submit_button("Save Calling Hours"):
#                 result = api_patch(f"companies/{st.session_state.company_id}/calling-hours", {
#                     "start_hour": start_hour,
#                     "end_hour": end_hour,
#                     "call_rate_per_minute": call_rate,
#                     "max_concurrent_calls": max_concurrent
#                 })
#                 if result and result.get('success'):
#                     st.success("✅ Calling hours updated!")
    
#     with tab2:
#         st.subheader("🔧 Custom Field Templates")
        
#         templates_resp = api_get("extraction-templates")
        
#         if templates_resp and templates_resp.get('success'):
#             for template in templates_resp['data']:
#                 with st.expander(f"📋 {template['template_name']} ({template['industry']})"):
#                     st.write(f"**Description:** {template['description']}")
                    
#                     fields = template['field_definitions'].get('fields', [])
#                     st.write(f"**Fields:** {len(fields)}")
                    
#                     if st.button(f"Apply to Company", key=f"template_{template['id']}"):
#                         result = api_post(f"companies/{st.session_state.company_id}/apply-template", {
#                             "template_id": template['id']
#                         })
#                         if result and result.get('success'):
#                             st.success(f"✅ Applied {len(result['data'])} field definitions!")
#                             st.rerun()
        
#         st.divider()
        
#         st.subheader("Create Custom Field")
#         with st.form("custom_field"):
#             field_key = st.text_input("Field Key", placeholder="chess_rating")
#             field_label = st.text_input("Field Label", placeholder="Chess Rating")
#             field_type = st.selectbox("Field Type", ["text", "number", "date", "email", "select"])
#             field_category = st.selectbox("Category", ["personal", "qualification", "preference"])
            
#             if st.form_submit_button("Create Field"):
#                 result = api_post("custom-fields", {
#                     "company_id": st.session_state.company_id,
#                     "field_key": field_key,
#                     "field_label": field_label,
#                     "field_type": field_type,
#                     "field_category": field_category
#                 })
#                 if result and result.get('success'):
#                     st.success("✅ Custom field created!")
#                 else:
#                     st.error("Failed to create field")
    
#     with tab3:
#         st.subheader("🔗 Integration Status")
        
#         integrations = {
#             "WhatsApp Business API": "✅ Connected",
#             "Twilio Voice": "✅ Connected",
#             "Google Calendar": "✅ Connected",
#             "Stripe Payments": "⚠️ Not Configured",
#             "Razorpay": "⚠️ Not Configured",
#             "SendGrid Email": "⚠️ Not Configured"
#         }
        
#         for name, status in integrations.items():
#             col1, col2 = st.columns([3, 1])
#             with col1:
#                 st.write(f"**{name}**")
#             with col2:
#                 st.write(status)
        
#         st.divider()
        
#         st.subheader("📊 System Health")
#         health_resp = api_get("health")
#         if health_resp:
#             st.json(health_resp)

# # ==================== LOGIN PAGE ====================
# def page_login():
#     st.title("🔐 Login to AI Sales CRM")
    
#     col1, col2, col3 = st.columns([1, 2, 1])
    
#     with col2:
#         with st.form("login"):
#             st.markdown("### Sign In")
            
#             # For demo purposes, we'll use company selection
#             # In production, implement proper authentication
            
#             companies_resp = api_get("companies")
            
#             if companies_resp and companies_resp.get('success'):
#                 company_options = {f"{c['name']} (ID: {c['id']})": c for c in companies_resp['data']}
                
#                 if company_options:
#                     selected = st.selectbox("Select Company", list(company_options.keys()))
#                     selected_company = company_options[selected]
                    
#                     username = st.text_input("Username")
#                     password = st.text_input("Password", type="password")
                    
#                     if st.form_submit_button("Login"):
#                         # Simple demo login - in production use proper auth
#                         if username and password:
#                             st.session_state.authenticated = True
#                             st.session_state.company_id = selected_company['id']
#                             st.session_state.company_name = selected_company['name']
#                             st.session_state.username = username
#                             st.rerun()
#                         else:
#                             st.error("Please enter username and password")
#                 else:
#                     st.error("No companies found. Please create a company first.")
#             else:
#                 st.error("Unable to fetch companies. Please check API connection.")
        
#         st.info("**Demo Mode:** Use any username/password to login")
        
#         st.divider()
        
#         with st.expander("🆕 Create New Company"):
#             with st.form("create_company"):
#                 company_name = st.text_input("Company Name*")
#                 company_phone = st.text_input("Phone Number*", placeholder="+919876543210")
                
#                 if st.form_submit_button("Create Company"):
#                     if company_name and company_phone:
#                         result = api_post("companies", {
#                             "name": company_name,
#                             "phone_number": company_phone
#                         })
#                         if result and result.get('success'):
#                             st.success(f"✅ Company created! ID: {result['data']['id']}")
#                             time.sleep(1)
#                             st.rerun()
#                         else:
#                             st.error("Failed to create company")
#                     else:
#                         st.warning("Please fill all fields")

# # ==================== MAIN APP ====================
# def main():
#     # Check authentication
#     if not st.session_state.authenticated:
#         page_login()
#         return
    
#     # Render sidebar
#     render_sidebar()
    
#     # Route to pages
#     page = st.session_state.get('page', 'dashboard')
    
#     try:
#         if page == 'dashboard':
#             page_dashboard()
#         elif page == 'leads':
#             page_leads()
#         elif page == 'agents':
#             page_agents()
#         elif page == 'calling':
#             page_calling()
#         elif page == 'whatsapp':
#             page_whatsapp()
#         elif page == 'human_agents':
#             page_human_agents()
#         elif page == 'analytics':
#             page_analytics()
#         elif page == 'notifications':
#             page_notifications()
#         elif page == 'settings':
#             page_settings()
#         else:
#             st.error(f"Page '{page}' not found")
#     except Exception as e:
#         st.error(f"Error loading page: {str(e)}")
#         st.exception(e)

# if __name__ == "__main__":
#     main()





















# # streamlit three + streamlit two

# import streamlit as st
# import requests
# import pandas as pd
# import json
# from datetime import datetime, timedelta
# import plotly.express as px
# import plotly.graph_objects as go
# from typing import Optional, Dict, List
# import time
# # ==================== CONFIGURATION ====================
# API_BASE_URL = "http://localhost:3000/api"        # Change if needed
# PYTHON_API_URL = "http://localhost:8000/api"      # Change if needed
# # Page config
# st.set_page_config(
#     page_title="AI Sales CRM",
#     page_icon="🤖",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )
# # Custom CSS
# st.markdown("""
# <style>
#     .metric-card {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         padding: 20px;
#         border-radius: 10px;
#         color: white;
#         margin: 10px 0;
#     }
#     .stButton>button {
#         width: 100%;
#         background-color: #667eea;
#         color: white;
#         border-radius: 5px;
#         border: none;
#         padding: 10px;
#     }
#     .stButton>button:hover {
#         background-color: #5568d3;
#     }
#     .success-box {
#         background-color: #d4edda;
#         border: 1px solid #c3e6cb;
#         padding: 15px;
#         border-radius: 5px;
#         margin: 10px 0;
#     }
#     .warning-box {
#         background-color: #fff3cd;
#         border: 1px solid #ffeaa7;
#         padding: 15px;
#         border-radius: 5px;
#         margin: 10px 0;
#     }
#     .error-box {
#         background-color: #f8d7da;
#         border: 1px solid #f5c6cb;
#         padding: 15px;
#         border-radius: 5px;
#         margin: 10px 0;
#     }
#     .lead-card {
#         background: white;
#         border: 1px solid #e0e0e0;
#         border-radius: 8px;
#         padding: 15px;
#         margin: 10px 0;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#     }
# </style>
# """, unsafe_allow_html=True)
# # ==================== SESSION STATE ====================
# if 'authenticated' not in st.session_state:
#     st.session_state.authenticated = False
# if 'company_id' not in st.session_state:
#     st.session_state.company_id = None
# if 'company_name' not in st.session_state:
#     st.session_state.company_name = None
# if 'user_role' not in st.session_state:
#     st.session_state.user_role = "admin"
# # ==================== API HELPERS ====================
# def api_get(endpoint: str, timeout: int = 10) -> Optional[Dict]:
#     """GET request to API"""
#     try:
#         response = requests.get(f"{API_BASE_URL}/{endpoint}", timeout=timeout)
#         response.raise_for_status()
#         return response.json()
#     except Exception as e:
#         st.error(f"API Error: {str(e)}")
#         return None
# def api_post(endpoint: str, data: Dict, timeout: int = 10) -> Optional[Dict]:
#     """POST request to API"""
#     try:
#         response = requests.post(f"{API_BASE_URL}/{endpoint}", json=data, timeout=timeout)
#         response.raise_for_status()
#         return response.json()
#     except Exception as e:
#         st.error(f"API Error: {str(e)}")
#         return None
# def api_patch(endpoint: str, data: Dict, timeout: int = 10) -> Optional[Dict]:
#     """PATCH request to API"""
#     try:
#         response = requests.patch(f"{API_BASE_URL}/{endpoint}", json=data, timeout=timeout)
#         response.raise_for_status()
#         return response.json()
#     except Exception as e:
#         st.error(f"API Error: {str(e)}")
#         return None
# def python_api_post(endpoint: str, data: Dict, timeout: int = 30) -> Optional[Dict]:
#     """POST to Python AI API"""
#     try:
#         response = requests.post(f"{PYTHON_API_URL}/{endpoint}", json=data, timeout=timeout)
#         response.raise_for_status()
#         return response.json()
#     except Exception as e:
#         st.error(f"Python API Error: {str(e)}")
#         return None
# # ==================== SIDEBAR NAVIGATION ====================
# def render_sidebar():
#     with st.sidebar:
#         st.title("🤖 AI Sales CRM")
#         st.markdown(f"**Company:** {st.session_state.company_name}")
#         st.markdown(f"**Role:** {st.session_state.user_role}")
#         st.divider()
       
#         menu_options = {
#             "📊 Dashboard": "dashboard",
#             "👥 Leads": "leads",
#             "🤖 AI Agents": "agents",
#             "📞 Calling": "calling",
#             "💬 WhatsApp": "whatsapp",
#             "🎯 Campaigns": "campaigns",
#             "👨‍💼 Human Agents": "human_agents",
#             "📈 Analytics": "analytics",
#             "🔔 Notifications": "notifications",
#             "⚙️ Settings": "settings"
#         }
       
#         selected = st.radio("Navigation", list(menu_options.keys()), label_visibility="collapsed")
#         st.session_state.page = menu_options[selected]
       
#         st.divider()
       
#         if st.button("🚪 Logout"):
#             st.session_state.authenticated = False
#             st.session_state.company_id = None
#             st.session_state.company_name = None
#             st.rerun()
# # ==================== PAGE: DASHBOARD ====================
# def page_dashboard():
#     st.title("📊 Dashboard Overview")
   
#     stats = api_get("stats/dashboard")
#     if not stats or not stats.get('success'):
#         st.warning("Unable to load dashboard data")
#         return
   
#     data = stats.get('data', {})
   
#     # Top Metrics
#     col1, col2, col3, col4 = st.columns(4)
   
#     with col1:
#         st.markdown('<div class="metric-card">', unsafe_allow_html=True)
#         st.metric("Total Leads", data.get('total_leads', 0))
#         st.markdown('</div>', unsafe_allow_html=True)
   
#     with col2:
#         st.markdown('<div class="metric-card">', unsafe_allow_html=True)
#         st.metric("Conversations", data.get('total_conversations', 0))
#         st.markdown('</div>', unsafe_allow_html=True)
   
#     with col3:
#         st.markdown('<div class="metric-card">', unsafe_allow_html=True)
#         st.metric("Pending Invoices", data.get('pending_invoices', 0))
#         st.markdown('</div>', unsafe_allow_html=True)
   
#     with col4:
#         st.markdown('<div class="metric-card">', unsafe_allow_html=True)
#         st.metric("Avg Interest", f"{data.get('avg_interest_level', 0)}/10")
#         st.markdown('</div>', unsafe_allow_html=True)
   
#     # Charts
#     col1, col2 = st.columns(2)
   
#     with col1:
#         st.subheader("📈 Leads by Status")
#         status_data = data.get('leads_by_status', [])
#         if status_data:
#             df = pd.DataFrame(status_data)
#             fig = px.pie(df, names='lead_status', values='count', hole=0.4)
#             st.plotly_chart(fig, use_container_width=True)
   
#     with col2:
#         st.subheader("🔥 Hot Leads")
#         hot_leads_resp = api_get("hot-leads")
#         if hot_leads_resp and hot_leads_resp.get('success'):
#             df = pd.DataFrame(hot_leads_resp['data'][:5])
#             if not df.empty:
#                 st.dataframe(df[['name', 'phone_number', 'tone_score', 'intent']], use_container_width=True)
#             else:
#                 st.info("No hot leads today")
   
#     # Recent Activity
#     st.subheader("📋 Recent Activity")
   
#     tab1, tab2 = st.tabs(["Calls", "Messages"])
   
#     with tab1:
#         calls_resp = api_get(f"call-logs?company_id={st.session_state.company_id}&limit=10")
#         if calls_resp and calls_resp.get('success'):
#             df = pd.DataFrame(calls_resp['data'])
#             if not df.empty:
#                 df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
#                 st.dataframe(df[['call_sid', 'to_phone', 'call_status', 'call_duration', 'created_at']],
#                            use_container_width=True)
   
#     with tab2:
#         messages_resp = api_get("stats/messages")
#         if messages_resp and messages_resp.get('success'):
#             df = pd.DataFrame(messages_resp['data'])
#             st.dataframe(df, use_container_width=True)
# # ==================== PAGE: LEADS ====================
# def page_leads():
#     st.title("👥 Lead Management")
   
#     # Filter options
#     col1, col2, col3, col4 = st.columns(4)
#     with col1:
#         status_filter = st.selectbox("Status", ["All", "new", "contacted", "qualified", "lost"])
#     with col2:
#         source_filter = st.selectbox("Source", ["All", "whatsapp", "website", "google_ads", "meta_ads"])
#     with col3:
#         limit = st.number_input("Limit", min_value=10, max_value=500, value=50)
#     with col4:
#         search_term = st.text_input("Search", placeholder="Name or phone")
#         if st.button("🔍 Search"):
#             st.rerun()
   
#     # Build query
#     query_params = f"limit={limit}"
#     if status_filter != "All":
#         query_params += f"&status={status_filter}"
#     if source_filter != "All":
#         query_params += f"&source={source_filter}"
#     if search_term:
#         query_params += f"&search={search_term}"
   
#     leads_resp = api_get(f"leads?{query_params}")
   
#     if not leads_resp or not leads_resp.get('success'):
#         st.warning("No leads found")
#         return
   
#     leads = leads_resp['data']
   
#     # Export button
#     if st.button("📊 Export to CSV"):
#         csv_url = f"{API_BASE_URL}/leads/export/csv?company_id={st.session_state.company_id}"
#         st.download_button(
#             label="Download Leads CSV",
#             data=requests.get(csv_url).content,
#             file_name=f"leads_{st.session_state.company_name}_{datetime.now().strftime('%Y%m%d')}.csv",
#             mime="text/csv"
#         )
   
#     # Display leads as cards
#     for lead in leads:
#         with st.expander(f"📋 {lead.get('name', 'Unknown')} - {lead['phone_number']}"):
#             render_lead_detail(lead)

# def render_lead_detail(lead: Dict):
#     """Render detailed lead information"""
   
#     col1, col2 = st.columns(2)
   
#     with col1:
#         st.markdown("### Basic Info")
#         st.write(f"**ID:** {lead['id']}")
#         st.write(f"**Phone:** {lead['phone_number']}")
#         st.write(f"**Email:** {lead.get('email', 'N/A')}")
#         st.write(f"**Status:** {lead['lead_status']}")
#         st.write(f"**Interest:** {lead.get('interest_level', 0)}/10")
#         st.write(f"**Source:** {lead.get('lead_source', 'N/A')}")
   
#     with col2:
#         st.markdown("### Custom Fields")
#         st.write(f"**Chess Rating:** {lead.get('chess_rating', 'N/A')}")
#         st.write(f"**Location:** {lead.get('location', 'N/A')}")
#         st.write(f"**Availability:** {lead.get('availability', 'N/A')}")
#         st.write(f"**Last Contact:** {lead.get('last_contacted', 'N/A')[:10] if lead.get('last_contacted') else 'Never'}")
   
#     # Load custom fields
#     custom_fields_resp = api_get(f"leads/{lead['id']}/custom-fields")
#     if custom_fields_resp and custom_fields_resp.get('success'):
#         custom_fields = custom_fields_resp['data']
#         if custom_fields:
#             st.markdown("### Additional Custom Fields")
#             for key, field_data in custom_fields.items():
#                 st.write(f"**{field_data.get('label', key)}:** {field_data.get('value', 'N/A')}")
   
#     st.divider()
   
#     # Actions
#     st.markdown("### Quick Actions")
   
#     col1, col2, col3, col4 = st.columns(4)
   
#     with col1:
#         if st.button("📞 Make Call", key=f"call_{lead['id']}"):
#             st.session_state.selected_lead_for_call = lead
#             st.session_state.page = 'calling'
#             st.rerun()
   
#     with col2:
#         if st.button("💬 Send WhatsApp", key=f"whatsapp_{lead['id']}"):
#             st.session_state.selected_lead_for_whatsapp = lead
#             st.session_state.page = 'whatsapp'
#             st.rerun()
   
#     with col3:
#         if st.button("📅 Schedule Call", key=f"schedule_{lead['id']}"):
#             with st.form(f"schedule_form_{lead['id']}"):
#                 call_type = st.selectbox("Type", ["qualification", "reminder", "payment"])
#                 scheduled_date = st.date_input("Date", value=datetime.now() + timedelta(days=1))
#                 scheduled_time = st.time_input("Time")
               
#                 if st.form_submit_button("Schedule"):
#                     scheduled_datetime = datetime.combine(scheduled_date, scheduled_time).isoformat()
#                     result = api_post("schedule-call", {
#                         "company_id": st.session_state.company_id,
#                         "lead_id": lead['id'],
#                         "call_type": call_type,
#                         "scheduled_time": scheduled_datetime
#                     })
#                     if result and result.get('success'):
#                         st.success("Call scheduled!")
#                     else:
#                         st.error("Failed to schedule")
   
#     with col4:
#         if st.button("📝 Edit Lead", key=f"edit_{lead['id']}"):
#             with st.form(f"edit_form_{lead['id']}"):
#                 new_status = st.selectbox("Status", ["new", "contacted", "qualified", "lost"],
#                                         index=["new", "contacted", "qualified", "lost"].index(lead['lead_status']))
#                 new_interest = st.slider("Interest Level", 1, 10, lead.get('interest_level', 5))
#                 notes = st.text_area("Notes", value=lead.get('notes', ''))
               
#                 if st.form_submit_button("Update"):
#                     result = api_patch(f"leads/{lead['id']}/status", {
#                         "lead_status": new_status,
#                         "interest_level": new_interest,
#                         "notes": notes
#                     })
#                     if result and result.get('success'):
#                         st.success("Lead updated!")
#                         st.rerun()
   
#     # Conversation History
#     st.divider()
#     st.markdown("### Conversation History")
   
#     # Get detailed messages
#     messages_resp = api_get(f"conversations/{lead['phone_number']}/messages?limit=50")
#     if messages_resp and messages_resp.get('success') and messages_resp.get('data'):
#         conversation_text = ""
#         for msg in reversed(messages_resp['data']):  # Reverse to show oldest first
#             sender = "👤 You" if msg.get('is_from_user', False) else "🤖 AI"
#             timestamp = msg.get('timestamp', '')[:16] if msg.get('timestamp') else 'N/A'
#             conversation_text += f"[{timestamp}] {sender}: {msg.get('message_body', '')}\n\n"
        
#         st.text_area("Conversation", value=conversation_text, height=200, key=f"conv_{lead['id']}")
#     else:
#         conv_resp = api_get(f"conversations/{lead['phone_number']}")
#         if conv_resp and conv_resp.get('success') and conv_resp.get('data'):
#             conv_data = conv_resp['data']
#             st.text_area("Conversation", value=conv_data.get('conversation_history', ''), height=200, key=f"conv_{lead['id']}")
#         else:
#             st.info("No conversation history yet")
   
#     # Call Logs
#     st.divider()
#     st.markdown("### Call History")
   
#     calls_resp = api_get(f"call-logs/lead/{lead['id']}")
#     if calls_resp and calls_resp.get('success') and calls_resp.get('data'):
#         for call in calls_resp['data'][:3]:
#             st.write(f"**{call['call_type']}** - {call['call_status']} - {call['created_at'][:16]}")
#             if call.get('transcript'):
#                 with st.expander("View Transcript"):
#                     st.text(call['transcript'][:500])
# # ==================== PAGE: AI AGENTS ====================
# def page_agents():
#     st.title("🤖 AI Agent Management")
   
#     tab1, tab2 = st.tabs(["My Agents", "Create New Agent"])
   
#     with tab1:
#         agents_resp = api_get(f"agent-instances/company/{st.session_state.company_id}")
       
#         if not agents_resp or not agents_resp.get('success'):
#             st.info("No agents configured yet")
#             return
       
#         for agent in agents_resp['data']:
#             with st.expander(f"🤖 {agent['agent_name']} ({agent['agent_type']})"):
#                 col1, col2 = st.columns(2)
               
#                 with col1:
#                     st.write(f"**ID:** {agent['id']}")
#                     st.write(f"**Type:** {agent['agent_type']}")
#                     st.write(f"**Phone:** {agent.get('phone_number', 'N/A')}")
#                     st.write(f"**WhatsApp:** {agent.get('whatsapp_number', 'N/A')}")
#                     st.write(f"**Status:** {'🟢 Active' if agent['is_active'] else '🔴 Inactive'}")
               
#                 with col2:
#                     st.write(f"**Created:** {agent['created_at'][:10]}")
#                     st.write(f"**Voice:** {agent.get('custom_voice', agent.get('default_voice', 'N/A'))}")
#                     st.write(f"**Model:** {agent.get('model_name', 'N/A')}")
               
#                 # Agent performance stats
#                 stats_resp = api_get(f"agent-instances/{agent['id']}/stats")
#                 if stats_resp and stats_resp.get('success'):
#                     stats = stats_resp['data']
#                     st.markdown("### 📊 Performance (30 days)")
#                     col_s1, col_s2, col_s3 = st.columns(3)
#                     with col_s1:
#                         st.metric("Total Calls", stats.get('total_calls', 0))
#                     with col_s2:
#                         st.metric("Completed Calls", stats.get('completed_calls', 0))
#                     with col_s3:
#                         st.metric("Total Messages", stats.get('total_messages', 0))
               
#                 if agent.get('custom_prompt'):
#                     with st.expander("View Custom Prompt"):
#                         st.text_area("Prompt", value=agent['custom_prompt'], height=200, key=f"prompt_{agent['id']}")
   
#     with tab2:
#         st.subheader("Create New AI Agent")
       
#         with st.form("create_agent"):
#             agent_name = st.text_input("Agent Name*", placeholder="Chess Coach AI")
#             agent_type = st.selectbox("Type*", ["voice", "whatsapp"])
           
#             if agent_type == "voice":
#                 phone_number = st.text_input("Phone Number", placeholder="+919876543210")
#             else:
#                 whatsapp_number = st.text_input("WhatsApp Number", placeholder="+919876543210")
           
#             custom_prompt = st.text_area("Custom Prompt (optional)", height=200,
#                 placeholder="You are Priya from 4champz...")
           
#             voice = st.selectbox("Voice", ["Raveena", "Aditi", "Brian", "Matthew"])
           
#             if st.form_submit_button("Create Agent"):
#                 data = {
#                     "company_id": st.session_state.company_id,
#                     "agent_name": agent_name,
#                     "agent_type": agent_type,
#                     "phone_number": phone_number if agent_type == "voice" else None,
#                     "whatsapp_number": whatsapp_number if agent_type == "whatsapp" else None,
#                     "custom_prompt": custom_prompt if custom_prompt else None,
#                     "custom_voice": voice
#                 }
               
#                 result = api_post("agent-instances", data)
#                 if result and result.get('success'):
#                     st.success(f"✅ Agent created! ID: {result['data']['id']}")
#                     st.rerun()
#                 else:
#                     st.error("Failed to create agent")
# # ==================== PAGE: CALLING ====================
# def page_calling():
#     st.title("📞 AI Calling System")
   
#     tab1, tab2 = st.tabs(["Make Call", "Call Logs"])
   
#     with tab1:
#         st.subheader("🚀 Initiate Outbound Call")
       
#         with st.form("make_call"):
#             col1, col2 = st.columns(2)
           
#             with col1:
#                 lead_id = st.number_input("Lead ID*", min_value=1, value=1)
#                 to_phone = st.text_input("Phone Number*", placeholder="+919876543210")
#                 name = st.text_input("Name", placeholder="Ajsal")
           
#             with col2:
#                 call_type = st.selectbox("Call Type", ["qualification", "reminder", "payment", "support"])
               
#                 # Get agents for this company
#                 agents_resp = api_get(f"agent-instances/company/{st.session_state.company_id}?agent_type=voice")
#                 agent_options = {}
#                 if agents_resp and agents_resp.get('success'):
#                     agent_options = {f"{a['agent_name']} ({a['id']})": a['id'] for a in agents_resp['data']}
               
#                 if agent_options:
#                     agent_select = st.selectbox("Select Agent", ["Default"] + list(agent_options.keys()))
#                     agent_instance_id = agent_options.get(agent_select, None)
#                 else:
#                     st.warning("No voice agents configured")
#                     agent_instance_id = None
           
#             if st.form_submit_button("📞 Make Call Now"):
#                 if to_phone:
#                     data = {
#                         "company_id": st.session_state.company_id,
#                         "lead_id": lead_id,
#                         "to_phone": to_phone,
#                         "name": name,
#                         "call_type": call_type
#                     }
                   
#                     if agent_instance_id:
#                         result = python_api_post(f"outbound-call-agent?agent_instance_id={agent_instance_id}", data)
#                     else:
#                         result = python_api_post("outbound-call", data)
                   
#                     if result and result.get('success'):
#                         st.success(f"✅ Call initiated! SID: {result.get('call_sid')}")
#                     else:
#                         st.error("Failed to initiate call")
#                 else:
#                     st.warning("Phone number is required")
   
#     with tab2:
#         st.subheader("📋 Recent Call Logs")
       
#         calls_resp = api_get(f"call-logs?company_id={st.session_state.company_id}&limit=50")
       
#         if calls_resp and calls_resp.get('success'):
#             df = pd.DataFrame(calls_resp['data'])
#             if not df.empty:
#                 df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
               
#                 for idx, row in df.iterrows():
#                     with st.expander(f"📞 {row['to_phone']} - {row['call_status']} - {row['created_at']}"):
#                         col1, col2, col3 = st.columns(3)
#                         with col1:
#                             st.write(f"**Duration:** {row.get('call_duration', 0)}s")
#                             st.write(f"**Type:** {row.get('call_type', 'N/A')}")
#                         with col2:
#                             st.write(f"**Status:** {row['call_status']}")
#                             st.write(f"**Call SID:** {row['call_sid'][:20]}...")
#                         with col3:
#                             if row.get('recording_url'):
#                                 st.markdown(f"[🎵 Recording]({row['recording_url']})")
                       
#                         if row.get('transcript'):
#                             st.text_area("Transcript", row['transcript'], height=150, key=f"transcript_{idx}")
# # ==================== PAGE: WHATSAPP ====================
# def page_whatsapp():
#     st.title("💬 WhatsApp Management")
   
#     tab1, tab2, tab3 = st.tabs(["Send Message", "Conversations", "Setup"])
   
#     with tab1:
#         st.subheader("📤 Send WhatsApp Message")
       
#         # Get WhatsApp agents
#         agents_resp = api_get(f"agent-instances/company/{st.session_state.company_id}?agent_type=whatsapp")
       
#         if not agents_resp or not agents_resp.get('success') or not agents_resp['data']:
#             st.warning("⚠️ No WhatsApp agents configured. Please setup in 'Setup' tab.")
#             return
       
#         agent_options = {f"{a['agent_name']} ({a['whatsapp_number']})": a['id'] for a in agents_resp['data']}
       
#         # Single message
#         with st.form("send_whatsapp"):
#             agent_select = st.selectbox("From Agent", list(agent_options.keys()))
#             agent_id = agent_options[agent_select]
           
#             to_phone = st.text_input("To Phone*", placeholder="+919876543210")
#             message = st.text_area("Message*", height=150)
           
#             if st.form_submit_button("Send Single Message"):
#                 if to_phone and message:
#                     result = api_post("whatsapp/send-manual", {
#                         "to": to_phone,
#                         "message": message,
#                         "agent_instance_id": agent_id
#                     })
#                     if result and result.get('success'):
#                         st.success("✅ Message sent!")
#                     else:
#                         st.error("Failed to send message")
#                 else:
#                     st.warning("Phone and message are required")
       
#         # Bulk message
#         st.divider()
#         st.subheader("📤 Send Bulk Messages")
#         with st.form("send_bulk_whatsapp"):
#             agent_select_bulk = st.selectbox("From Agent (Bulk)", list(agent_options.keys()))
#             agent_id_bulk = agent_options[agent_select_bulk]
           
#             # Get leads for bulk selection
#             leads_resp = api_get(f"leads?company_id={st.session_state.company_id}&limit=100")
#             lead_options = {}
#             if leads_resp and leads_resp.get('success'):
#                 lead_options = {f"{l['name']} ({l['phone_number']})": l['phone_number'] for l in leads_resp['data']}
           
#             selected_leads = st.multiselect("Select Leads for Bulk Message", list(lead_options.keys()))
#             bulk_message = st.text_area("Bulk Message*", height=150)
           
#             if st.form_submit_button("Send Bulk Messages"):
#                 if selected_leads and bulk_message:
#                     messages = [{"to": lead_options[lead], "message": bulk_message} for lead in selected_leads]
#                     result = api_post("whatsapp/send-bulk", {
#                         "agent_instance_id": agent_id_bulk,
#                         "messages": messages
#                     })
#                     if result and result.get('success'):
#                         st.success(f"✅ Sent to {result.get('sent', 0)} leads!")
#                         if result.get('errors'):
#                             st.warning(f"Failed to send to {len(result['errors'])} leads")
#                     else:
#                         st.error("Failed to send bulk messages")
#                 else:
#                     st.warning("Please select leads and enter message")
   
#     with tab2:
#         st.subheader("💬 Recent Conversations")
       
#         phone_search = st.text_input("Search by phone", placeholder="+919876543210")
       
#         if phone_search:
#             # Get detailed messages
#             messages_resp = api_get(f"conversations/{phone_search}/messages?limit=100")
#             if messages_resp and messages_resp.get('success') and messages_resp.get('data'):
#                 data = messages_resp['data']
#                 # Get lead info
#                 lead_resp = api_get(f"leads?phone_number={phone_search}")
#                 lead_name = "Unknown"
#                 if lead_resp and lead_resp.get('success') and lead_resp.get('data'):
#                     lead_name = lead_resp['data'][0].get('name', 'Unknown') if lead_resp['data'] else "Unknown"
                
#                 st.write(f"**Name:** {lead_name}")
#                 st.write(f"**Status:** {lead_resp['data'][0].get('lead_status', 'N/A') if lead_resp and lead_resp.get('data') else 'N/A'}")
#                 st.write(f"**Total Messages:** {len(data)}")
               
#                 conversation_text = ""
#                 for msg in reversed(data):  # Show chronological order
#                     sender = "👤 You" if msg.get('is_from_user', False) else "🤖 AI"
#                     timestamp = msg.get('timestamp', '')[:16] if msg.get('timestamp') else 'N/A'
#                     conversation_text += f"[{timestamp}] {sender}: {msg.get('message_body', '')}\n\n"
                
#                 st.text_area("Conversation History", conversation_text, height=300)
#             else:
#                 st.warning("No conversation found")
   
#     with tab3:
#         st.subheader("⚙️ WhatsApp Setup")
       
#         st.markdown("""
#         ### Setup Instructions
       
#         1. **Create WhatsApp AI Agent** (if not already done)
#         2. **Get Meta WhatsApp Business API Credentials**
#         3. **Configure webhook in Meta**
       
#         #### Webhook URL
#         Copy this URL and paste in Meta Developer Console:
#         """)
       
#         webhook_url = f"{API_BASE_URL.replace('/api', '')}/api/webhooks/whatsapp-universal"
#         st.code(webhook_url)
       
#         st.markdown("#### Configure Credentials")
       
#         # Get existing agents
#         agents_resp = api_get(f"agent-instances/company/{st.session_state.company_id}?agent_type=whatsapp")
       
#         if agents_resp and agents_resp.get('success') and agents_resp['data']:
#             agent_options = {f"{a['agent_name']} (ID: {a['id']})": a['id'] for a in agents_resp['data']}
           
#             with st.form("whatsapp_credentials"):
#                 agent_select = st.selectbox("Select Agent", list(agent_options.keys()))
#                 agent_id = agent_options[agent_select]
               
#                 st.markdown("**Meta WhatsApp Business API Credentials:**")
#                 access_token = st.text_input("Access Token*", type="password")
#                 phone_number_id = st.text_input("Phone Number ID*")
#                 business_account_id = st.text_input("Business Account ID")
               
#                 if st.form_submit_button("Save Credentials"):
#                     result = api_post(f"agent-instances/{agent_id}/whatsapp-credentials", {
#                         "access_token": access_token,
#                         "phone_number_id": phone_number_id,
#                         "business_account_id": business_account_id
#                     })
#                     if result and result.get('success'):
#                         st.success("✅ Credentials saved!")
#                         st.info(f"**Webhook URL:** {result.get('webhook_url')}")
#                         st.info(f"**Verify Token:** {result.get('verify_token')}")
#                     else:
#                         st.error("Failed to save credentials")
#         else:
#             st.info("Create a WhatsApp agent first in 'AI Agents' page")
# # ==================== PAGE: CAMPAIGNS ====================
# def page_campaigns():
#     """Campaigns management page"""
#     st.title("🎯 Marketing Campaigns")
   
#     tab1, tab2 = st.tabs(["Active Campaigns", "Create Campaign"])
   
#     with tab1:
#         st.subheader("Campaign Performance")
       
#         # Fetch campaigns
#         campaigns_resp = api_get(f"campaigns?company_id={st.session_state.company_id}")
       
#         if campaigns_resp and campaigns_resp.get('success') and campaigns_resp.get('data'):
#             for campaign in campaigns_resp['data']:
#                 with st.expander(f"📢 {campaign['campaign_name']} - {campaign['status']}"):
#                     col1, col2, col3 = st.columns(3)
                   
#                     with col1:
#                         st.write(f"**Type:** {campaign['campaign_type']}")
#                         st.write(f"**Total Leads:** {campaign.get('total_leads', 0)}")
                   
#                     with col2:
#                         st.write(f"**Started:** {campaign.get('scheduled_start', 'N/A')[:10] if campaign.get('scheduled_start') else 'Not started'}")
#                         st.write(f"**Status:** {campaign['status']}")
                   
#                     with col3:
#                         st.write(f"**Call Rate:** {campaign.get('call_rate_per_minute', 1)}/min")
                   
#                     # Get campaign stats
#                     if st.button("View Stats", key=f"stats_{campaign['id']}"):
#                         stats_resp = api_get(f"campaigns/{campaign['id']}/stats")
#                         if stats_resp and stats_resp.get('success'):
#                             st.json(stats_resp['data'])
#                         else:
#                             st.info("Stats not available yet")
#         else:
#             st.info("No campaigns found. Create your first campaign!")
   
#     with tab2:
#         st.subheader("Create New Campaign")
       
#         with st.form("create_campaign_form"):
#             campaign_name = st.text_input("Campaign Name*", placeholder="Chess Coaching Outreach")
#             campaign_type = st.selectbox("Type", ["outbound", "follow_up", "renewal", "nurture"])
           
#             # Lead selection filters
#             st.markdown("**Target Leads**")
#             lead_source = st.multiselect("Lead Source",
#                 ["whatsapp", "website", "google_ads", "meta_ads", "referral"],
#                 default=["whatsapp", "website"])
#             lead_status = st.multiselect("Lead Status",
#                 ["new", "contacted", "qualified", "lost"],
#                 default=["new", "contacted"])
           
#             call_rate = st.slider("Calls per Minute", 1, 10, 2)
           
#             scheduled_start = st.date_input("Start Date",
#                 value=datetime.now() + timedelta(days=1))
#             start_time = st.time_input("Start Time", value=datetime.now().time())
           
#             message_template = st.text_area("WhatsApp Message Template (Optional)", 
#                 height=100, placeholder="Hi {{name}}, we're excited about your interest in chess coaching...")
           
#             if st.form_submit_button("Create Campaign", use_container_width=True):
#                 start_datetime = datetime.combine(scheduled_start, start_time).isoformat()
               
#                 # Build lead filter
#                 lead_filter = {
#                     "lead_sources": lead_source,
#                     "lead_statuses": lead_status
#                 }
               
#                 data = {
#                     "company_id": st.session_state.company_id,
#                     "campaign_name": campaign_name,
#                     "campaign_type": campaign_type,
#                     "lead_filter": lead_filter,
#                     "call_rate_per_minute": call_rate,
#                     "scheduled_start": start_datetime,
#                     "message_template": message_template if message_template else None
#                 }
               
#                 result = api_post("campaigns", data)
#                 if result and result.get('success'):
#                     st.success(f"✅ Campaign '{campaign_name}' created! ID: {result['data']['id']}")
#                     st.info("Campaign will start processing leads and scheduling calls")
#                     time.sleep(2)
#                     st.rerun()
#                 else:
#                     st.error("Failed to create campaign")
# # ==================== PAGE: HUMAN AGENTS ====================
# def page_human_agents():
#     st.title("👨‍💼 Human Sales Agents")
   
#     tab1, tab2 = st.tabs(["View Agents", "Takeover Requests"])
   
#     with tab1:
#         agents_resp = api_get("human-agents")
       
#         if agents_resp and agents_resp.get('success'):
#             for agent in agents_resp['data']:
#                 with st.expander(f"👤 {agent['name']} - {agent['role']}"):
#                     col1, col2 = st.columns(2)
                   
#                     with col1:
#                         st.write(f"**Email:** {agent['email']}")
#                         st.write(f"**Phone:** {agent.get('phone', 'N/A')}")
#                         st.write(f"**Status:** {agent['status']}")
                   
#                     with col2:
#                         st.write(f"**Assigned Leads:** {agent['assigned_leads']}")
#                         st.write(f"**Max Concurrent:** {agent['max_concurrent_leads']}")
                   
#                     new_status = st.selectbox(
#                         "Change Status",
#                         ["available", "busy", "offline"],
#                         key=f"status_{agent['id']}"
#                     )
                   
#                     if st.button("Update Status", key=f"update_{agent['id']}"):
#                         result = api_patch(f"human-agents/{agent['id']}/status", {"status": new_status})
#                         if result and result.get('success'):
#                             st.success("Status updated")
#                             st.rerun()
   
#     with tab2:
#         st.subheader("🔥 Pending Takeover Requests")
       
#         # This would show takeover requests for company's leads
#         st.info("Feature coming soon - view AI-to-human handoff requests")
# # ==================== PAGE: ANALYTICS ====================
# def page_analytics():
#     st.title("📈 Analytics & Reports")
   
#     tab1, tab2 = st.tabs(["Call Analytics", "Lead Analytics"])
   
#     with tab1:
#         st.subheader("📞 Call Performance")
       
#         metrics_resp = api_get("metrics/dashboard")
#         if metrics_resp and metrics_resp.get('success'):
#             data = metrics_resp['data']
           
#             col1, col2, col3 = st.columns(3)
#             with col1:
#                 st.metric("Active Calls", data.get('active_calls', 0))
#             with col2:
#                 calls_24h = data.get('calls_24h', [])
#                 total_calls = sum([c.get('count', 0) for c in calls_24h]) if calls_24h else 0
#                 st.metric("Calls (24h)", total_calls)
#             with col3:
#                 st.metric("Success Rate", f"{data.get('success_rate', 0)}%")
           
#             # Sentiment distribution
#             sentiment_data = data.get('sentiment_distribution', [])
#             if sentiment_data:
#                 st.subheader("😊 Sentiment Distribution")
#                 df = pd.DataFrame(sentiment_data)
#                 fig = px.bar(df, x='sentiment_type', y='count', color='sentiment_type')
#                 st.plotly_chart(fig, use_container_width=True)
   
#     with tab2:
#         st.subheader("👥 Lead Analytics")
       
#         lead_stats_resp = api_get("stats/leads")
#         if lead_stats_resp and lead_stats_resp.get('success'):
#             df = pd.DataFrame(lead_stats_resp['data'])
           
#             if not df.empty:
#                 fig = px.bar(df, x='lead_status', y='count', color='lead_status',
#                             title="Leads by Status")
#                 st.plotly_chart(fig, use_container_width=True)
               
#                 # Average interest by status
#                 fig2 = px.scatter(df, x='lead_status', y='avg_interest', size='count',
#                                  title="Average Interest Level by Status")
#                 st.plotly_chart(fig2, use_container_width=True)
# # ==================== PAGE: NOTIFICATIONS ====================
# def page_notifications():
#     st.title("🔔 Notifications & Alerts")
   
#     tab1, tab2 = st.tabs(["Recent Notifications", "Alerts"])
   
#     with tab1:
#         notif_resp = api_get("system-notifications?limit=50")
       
#         if notif_resp and notif_resp.get('success'):
#             for notif in notif_resp['data']:
#                 priority_emoji = {
#                     'urgent': '🚨',
#                     'high': '⚠️',
#                     'normal': 'ℹ️',
#                     'low': '💡'
#                 }
               
#                 emoji = priority_emoji.get(notif.get('priority', 'normal'), 'ℹ️')
               
#                 with st.expander(f"{emoji} {notif['title']} - {notif['created_at'][:16]}"):
#                     st.write(notif['message'])
                   
#                     if not notif.get('is_read'):
#                         if st.button("Mark as Read", key=f"read_{notif['id']}"):
#                             result = api_post(f"system-notifications/{notif['id']}/read", {})
#                             if result and result.get('success'):
#                                 st.success("Marked as read")
#                                 st.rerun()
#         else:
#             st.info("No notifications")
   
#     with tab2:
#         alerts_resp = api_get("alerts?limit=20")
       
#         if alerts_resp and alerts_resp.get('success'):
#             for alert in alerts_resp['data']:
#                 severity_color = {
#                     'critical': '🔴',
#                     'high': '🟠',
#                     'normal': '🟡',
#                     'low': '🟢'
#                 }
               
#                 icon = severity_color.get(alert.get('severity', 'normal'), '🟡')
               
#                 with st.expander(f"{icon} {alert['title']} - {alert['created_at'][:16]}"):
#                     st.write(alert['message'])
#                     st.caption(f"Severity: {alert.get('severity', 'normal')}")
#         else:
#             st.info("No alerts")
# # ==================== PAGE: SETTINGS ====================
# def page_settings():
#     st.title("⚙️ Settings & Configuration")
   
#     tab1, tab2, tab3 = st.tabs(["Company Info", "Custom Fields", "Integrations"])
   
#     with tab1:
#         st.subheader("🏢 Company Information")
       
#         company_resp = api_get(f"companies/{st.session_state.company_id}")
#         if company_resp and company_resp.get('success'):
#             company = company_resp['data']
           
#             with st.form("update_company"):
#                 name = st.text_input("Company Name", value=company.get('name', ''))
#                 phone = st.text_input("Phone Number", value=company.get('phone_number', ''))
               
#                 if st.form_submit_button("Update Company"):
#                     st.info("Company update feature coming soon")
       
#         st.divider()
       
#         st.subheader("🕐 Calling Hours Configuration")
       
#         with st.form("calling_hours"):
#             col1, col2 = st.columns(2)
#             with col1:
#                 start_hour = st.number_input("Start Hour (24h)", 0, 23, 9)
#             with col2:
#                 end_hour = st.number_input("End Hour (24h)", 0, 23, 18)
           
#             call_rate = st.number_input("Calls per Minute", 1, 10, 2)
#             max_concurrent = st.number_input("Max Concurrent Calls", 1, 20, 5)
           
#             if st.form_submit_button("Save Calling Hours"):
#                 result = api_patch(f"companies/{st.session_state.company_id}/calling-hours", {
#                     "start_hour": start_hour,
#                     "end_hour": end_hour,
#                     "call_rate_per_minute": call_rate,
#                     "max_concurrent_calls": max_concurrent
#                 })
#                 if result and result.get('success'):
#                     st.success("✅ Calling hours updated!")
   
#     with tab2:
#         st.subheader("🔧 Custom Field Templates")
       
#         templates_resp = api_get("extraction-templates")
       
#         if templates_resp and templates_resp.get('success'):
#             for template in templates_resp['data']:
#                 with st.expander(f"📋 {template['template_name']} ({template['industry']})"):
#                     st.write(f"**Description:** {template['description']}")
                   
#                     fields = template['field_definitions'].get('fields', [])
#                     st.write(f"**Fields:** {len(fields)}")
                   
#                     if st.button(f"Apply to Company", key=f"template_{template['id']}"):
#                         result = api_post(f"companies/{st.session_state.company_id}/apply-template", {
#                             "template_id": template['id']
#                         })
#                         if result and result.get('success'):
#                             st.success(f"✅ Applied {len(result['data'])} field definitions!")
#                             st.rerun()
       
#         st.divider()
       
#         st.subheader("Create Custom Field")
#         with st.form("custom_field"):
#             field_key = st.text_input("Field Key", placeholder="chess_rating")
#             field_label = st.text_input("Field Label", placeholder="Chess Rating")
#             field_type = st.selectbox("Field Type", ["text", "number", "date", "email", "select"])
#             field_category = st.selectbox("Category", ["personal", "qualification", "preference"])
           
#             if st.form_submit_button("Create Field"):
#                 result = api_post("custom-fields", {
#                     "company_id": st.session_state.company_id,
#                     "field_key": field_key,
#                     "field_label": field_label,
#                     "field_type": field_type,
#                     "field_category": field_category
#                 })
#                 if result and result.get('success'):
#                     st.success("✅ Custom field created!")
#                 else:
#                     st.error("Failed to create field")
   
#     with tab3:
#         st.subheader("🔗 Integration Status")
       
#         integrations = {
#             "WhatsApp Business API": "✅ Connected",
#             "Twilio Voice": "✅ Connected",
#             "Google Calendar": "✅ Connected",
#             "Stripe Payments": "⚠️ Not Configured",
#             "Razorpay": "⚠️ Not Configured",
#             "SendGrid Email": "⚠️ Not Configured"
#         }
       
#         for name, status in integrations.items():
#             col1, col2 = st.columns([3, 1])
#             with col1:
#                 st.write(f"**{name}**")
#             with col2:
#                 st.write(status)
       
#         st.divider()
       
#         st.subheader("📊 System Health")
#         health_resp = api_get("health")
#         if health_resp:
#             st.json(health_resp)
# # ==================== LOGIN PAGE ====================
# def page_login():
#     st.title("🔐 Login to AI Sales CRM")
   
#     col1, col2, col3 = st.columns([1, 2, 1])
   
#     with col2:
#         with st.form("login"):
#             st.markdown("### Sign In")
           
#             # For demo purposes, we'll use company selection
#             # In production, implement proper authentication
           
#             companies_resp = api_get("companies")
           
#             if companies_resp and companies_resp.get('success'):
#                 company_options = {f"{c['name']} (ID: {c['id']})": c for c in companies_resp['data']}
               
#                 if company_options:
#                     selected = st.selectbox("Select Company", list(company_options.keys()))
#                     selected_company = company_options[selected]
                   
#                     username = st.text_input("Username")
#                     password = st.text_input("Password", type="password")
                   
#                     if st.form_submit_button("Login"):
#                         # Simple demo login - in production use proper auth
#                         if username and password:
#                             st.session_state.authenticated = True
#                             st.session_state.company_id = selected_company['id']
#                             st.session_state.company_name = selected_company['name']
#                             st.session_state.username = username
#                             st.rerun()
#                         else:
#                             st.error("Please enter username and password")
#                 else:
#                     st.error("No companies found. Please create a company first.")
#             else:
#                 st.error("Unable to fetch companies. Please check API connection.")
       
#         st.info("**Demo Mode:** Use any username/password to login")
       
#         st.divider()
       
#         with st.expander("🆕 Create New Company"):
#             with st.form("create_company"):
#                 company_name = st.text_input("Company Name*")
#                 company_phone = st.text_input("Phone Number*", placeholder="+919876543210")
               
#                 if st.form_submit_button("Create Company"):
#                     if company_name and company_phone:
#                         result = api_post("companies", {
#                             "name": company_name,
#                             "phone_number": company_phone
#                         })
#                         if result and result.get('success'):
#                             st.success(f"✅ Company created! ID: {result['data']['id']}")
#                             time.sleep(1)
#                             st.rerun()
#                         else:
#                             st.error("Failed to create company")
#                     else:
#                         st.warning("Please fill all fields")
# # ==================== MAIN APP ====================
# def main():
#     # Check authentication
#     if not st.session_state.authenticated:
#         page_login()
#         return
   
#     # Render sidebar
#     render_sidebar()
   
#     # Route to pages
#     page = st.session_state.get('page', 'dashboard')
   
#     try:
#         if page == 'dashboard':
#             page_dashboard()
#         elif page == 'leads':
#             page_leads()
#         elif page == 'agents':
#             page_agents()
#         elif page == 'calling':
#             page_calling()
#         elif page == 'whatsapp':
#             page_whatsapp()
#         elif page == 'campaigns':
#             page_campaigns()
#         elif page == 'human_agents':
#             page_human_agents()
#         elif page == 'analytics':
#             page_analytics()
#         elif page == 'notifications':
#             page_notifications()
#         elif page == 'settings':
#             page_settings()
#         else:
#             st.error(f"Page '{page}' not found")
#     except Exception as e:
#         st.error(f"Error loading page: {str(e)}")
#         st.exception(e)
# if __name__ == "__main__":
#     main()



import streamlit as st
import requests
import pandas as pd
import json
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional, Dict, List
import time

# ==================== CONFIGURATION ====================
API_BASE_URL = "https://noily-deena-ancestrally.ngrok-free.dev/api"
PYTHON_API_URL = "https://call-automation-kxow.onrender.com"
N8N_WEBHOOK_URL = "https://n8n-render-host-n0ym.onrender.com/webhook-test/webhook/whatsapp-trigger"

# Page config
st.set_page_config(
    page_title="AI Sales CRM",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #667eea;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #5568d3;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .lead-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .conversation-user {
        background-color: #e3f2fd;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        text-align: right;
    }
    .conversation-bot {
        background-color: #f5f5f5;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        text-align: left;
    }
    .sentiment-positive {
        color: #4caf50;
        font-weight: bold;
    }
    .sentiment-negative {
        color: #f44336;
        font-weight: bold;
    }
    .sentiment-neutral {
        color: #ff9800;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'company_id' not in st.session_state:
    st.session_state.company_id = None
if 'company_name' not in st.session_state:
    st.session_state.company_name = None
if 'user_role' not in st.session_state:
    st.session_state.user_role = "admin"
if 'page' not in st.session_state:
    st.session_state.page = "dashboard"

# ==================== API HELPERS ====================
def api_get(endpoint: str, timeout: int = 10) -> Optional[Dict]:
    """GET request to API"""
    try:
        response = requests.get(f"{API_BASE_URL}/{endpoint}", timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

def api_post(endpoint: str, data: Dict, timeout: int = 10) -> Optional[Dict]:
    """POST request to API"""
    try:
        response = requests.post(f"{API_BASE_URL}/{endpoint}", json=data, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

def api_patch(endpoint: str, data: Dict, timeout: int = 10) -> Optional[Dict]:
    """PATCH request to API"""
    try:
        response = requests.patch(f"{API_BASE_URL}/{endpoint}", json=data, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

def api_delete(endpoint: str, timeout: int = 10) -> Optional[Dict]:
    """DELETE request to API"""
    try:
        response = requests.delete(f"{API_BASE_URL}/{endpoint}", timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

def python_api_post(endpoint: str, data: Dict, timeout: int = 30) -> Optional[Dict]:
    """POST to Python AI API"""
    try:
        response = requests.post(f"{PYTHON_API_URL}/{endpoint}", json=data, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Python API Error: {str(e)}")
        return None
    


def api_delete(endpoint: str, timeout: int = 10) -> Optional[Dict]:
    """DELETE request to API"""
    try:
        response = requests.delete(f"{API_BASE_URL}/{endpoint}", timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

# ==================== SIDEBAR NAVIGATION ====================
def render_sidebar():
    with st.sidebar:
        st.title("🤖 AI Sales CRM")
        st.markdown(f"**Company:** {st.session_state.company_name}")
        st.markdown(f"**Role:** {st.session_state.user_role}")
        st.divider()
        
        menu_options = {
            "📊 Dashboard": "dashboard",
            "👥 Leads": "leads",
            "➕ Add Lead": "add_lead",
            "🤖 AI Agents": "agents",
            "📞 Calling": "calling",
            "📅 Scheduled Calls": "scheduled_calls",
            "📅 Calendar": "calendar",
            "💬 WhatsApp": "whatsapp",
            "🎯 Campaigns": "campaigns",
            "👨‍💼 Human Agents": "human_agents",
            "📈 Analytics": "analytics",
            "🔔 Notifications": "notifications",
            "⚙️ Settings": "settings"
        }
        
        selected = st.radio("Navigation", list(menu_options.keys()), label_visibility="collapsed")
        st.session_state.page = menu_options[selected]
        
        st.divider()
        
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.company_id = None
            st.session_state.company_name = None
            st.rerun()

# ==================== PAGE: DASHBOARD ====================
def page_dashboard():
    st.title("📊 Dashboard Overview")
    
    stats = api_get("stats/dashboard")
    if not stats or not stats.get('success'):
        st.warning("Unable to load dashboard data")
        return
    
    data = stats.get('data', {})
    
    # Top Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Leads", data.get('total_leads', 0))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Conversations", data.get('total_conversations', 0))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Pending Invoices", data.get('pending_invoices', 0))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Avg Interest", f"{data.get('avg_interest_level', 0)}/10")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Leads by Status")
        status_data = data.get('leads_by_status', [])
        if status_data:
            df = pd.DataFrame(status_data)
            fig = px.pie(df, names='lead_status', values='count', hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🔥 Hot Leads")
        hot_leads_resp = api_get("hot-leads")
        if hot_leads_resp and hot_leads_resp.get('success'):
            df = pd.DataFrame(hot_leads_resp['data'][:5])
            if not df.empty:
                st.dataframe(df[['name', 'phone_number', 'tone_score', 'intent']], use_container_width=True)
            else:
                st.info("No hot leads today")
    
    # Recent Activity
    st.subheader("📋 Recent Activity")
    
    tab1, tab2 = st.tabs(["Calls", "Messages"])
    
    with tab1:
        calls_resp = api_get(f"call-logs?company_id={st.session_state.company_id}&limit=10")
        if calls_resp and calls_resp.get('success'):
            df = pd.DataFrame(calls_resp['data'])
            if not df.empty:
                df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
                st.dataframe(df[['call_sid', 'to_phone', 'call_status', 'call_duration', 'created_at']],
                           use_container_width=True)
    
    with tab2:
        messages_resp = api_get("stats/messages")
        if messages_resp and messages_resp.get('success'):
            df = pd.DataFrame(messages_resp['data'])
            st.dataframe(df, use_container_width=True)

# ==================== PAGE: ADD LEAD ====================
def page_add_lead():
    st.title("➕ Add New Lead")
    
    with st.form("add_lead_form"):
        st.subheader("Basic Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name*", placeholder="John Doe")
            phone_number = st.text_input("Phone Number*", placeholder="+919876543210")
            email = st.text_input("Email", placeholder="john@example.com")
            lead_source = st.selectbox("Lead Source", 
                ["whatsapp", "website", "google_ads", "meta_ads", "referral", "other"])
        
        with col2:
            interest_level = st.slider("Interest Level", 1, 10, 5)
            lead_status = st.selectbox("Lead Status", 
                ["new", "contacted", "qualified", "lost"])
            location = st.text_input("Location", placeholder="Bangalore, India")
        
        st.subheader("Additional Information")
        
        col3, col4 = st.columns(2)
        
        with col3:
            chess_rating = st.text_input("Chess Rating", placeholder="1500")
            availability = st.text_input("Availability", placeholder="Weekends")
        
        with col4:
            age_group_pref = st.text_input("Age Group Preference", placeholder="Kids 6-12")
        
        notes = st.text_area("Notes", placeholder="Any additional information...")
        tags = st.text_input("Tags (comma separated)", placeholder="vip, premium")
        
        submitted = st.form_submit_button("Add Lead", use_container_width=True)
        
        if submitted:
            if not phone_number:
                st.error("Phone number is required!")
                return
            
            # Prepare data
            lead_data = {
                "phone_number": phone_number,
                "name": name,
                "email": email if email else None,
                "lead_source": lead_source,
                "interest_level": interest_level,
                "lead_status": lead_status,
                "location": location if location else None,
                "chess_rating": chess_rating if chess_rating else None,
                "availability": availability if availability else None,
                "age_group_pref": age_group_pref if age_group_pref else None,
                "notes": notes if notes else None,
                "tags": tags.split(',') if tags else None,
                "company_id": st.session_state.company_id
            }
            
            result = api_post("leads", lead_data)
            
            if result and result.get('success'):
                st.success(f"✅ Lead added successfully! ID: {result['data']['id']}")
                time.sleep(1)
                st.session_state.page = 'leads'
                st.rerun()
            else:
                st.error("Failed to add lead. Please try again.")

# ==================== PAGE: LEADS ====================
def page_leads():
    st.title("👥 Lead Management")
    
    # Filter options
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        status_filter = st.selectbox("Status", ["All", "new", "contacted", "qualified", "lost"])
    with col2:
        source_filter = st.selectbox("Source", ["All", "whatsapp", "website", "google_ads", "meta_ads"])
    with col3:
        limit = st.number_input("Limit", min_value=10, max_value=500, value=50)
    with col4:
        search_term = st.text_input("Search", placeholder="Name or phone")
    
    # Build query
    query_params = f"company_id={st.session_state.company_id}&limit={limit}"
    if status_filter != "All":
        query_params += f"&status={status_filter}"
    if source_filter != "All":
        query_params += f"&source={source_filter}"
    if search_term:
        query_params += f"&search={search_term}"
    
    leads_resp = api_get(f"leads?{query_params}")
    
    if not leads_resp or not leads_resp.get('success'):
        st.warning("No leads found")
        return
    
    leads = leads_resp['data']
    
    # Export button
    if st.button("📊 Export to CSV"):
        csv_url = f"{API_BASE_URL}/leads/export/csv?company_id={st.session_state.company_id}"
        try:
            response = requests.get(csv_url)
            st.download_button(
                label="Download Leads CSV",
                data=response.content,
                file_name=f"leads_{st.session_state.company_name}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"Export failed: {str(e)}")
    
    st.divider()
    
    # Display leads as cards
    for lead in leads:
        with st.expander(f"📋 {lead.get('name', 'Unknown')} - {lead['phone_number']} - Status: {lead['lead_status']}"):
            if st.button("👁️ View Full Profile", key=f"view_{lead['id']}"):
                st.session_state.selected_lead_id = lead['id']
                st.session_state.page = 'lead_detail'
                st.rerun()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Phone:** {lead['phone_number']}")
                st.write(f"**Email:** {lead.get('email', 'N/A')}")
                st.write(f"**Status:** {lead['lead_status']}")
                st.write(f"**Interest:** {lead.get('interest_level', 0)}/10")
            
            with col2:
                st.write(f"**Source:** {lead.get('lead_source', 'N/A')}")
                st.write(f"**Location:** {lead.get('location', 'N/A')}")
                st.write(f"**Last Contact:** {lead.get('last_contacted', 'N/A')[:10] if lead.get('last_contacted') else 'Never'}")

# ==================== PAGE: LEAD DETAIL ====================
# def page_lead_detail():
#     if 'selected_lead_id' not in st.session_state:
#         st.warning("No lead selected")
#         if st.button("← Back to Leads"):
#             st.session_state.page = 'leads'
#             st.rerun()
#         return
    
#     lead_id = st.session_state.selected_lead_id
    
#     # Fetch lead details
#     lead_resp = api_get(f"leads/{lead_id}")
#     if not lead_resp or not lead_resp.get('success'):
#         st.error("Lead not found")
#         return
    
#     lead = lead_resp['data']
    
#     # Header
#     col1, col2 = st.columns([3, 1])
#     with col1:
#         st.title(f"👤 {lead.get('name', 'Unknown')}")
#     with col2:
#         if st.button("← Back to Leads"):
#             st.session_state.page = 'leads'
#             st.rerun()
    
#     # Tabs for different sections
#     tab1, tab2, tab3, tab4, tab5 = st.tabs([
#         "📋 Overview", 
#         "💬 WhatsApp Chat", 
#         "📞 Call History", 
#         "📊 Analytics",
#         "✏️ Edit"
#     ])
    
#     with tab1:
#         render_lead_overview(lead)
    
#     with tab2:
#         render_whatsapp_conversation(lead)
    
#     with tab3:
#         render_call_history(lead)
    
#     with tab4:
#         render_lead_analytics(lead)
    
#     with tab5:
#         render_lead_edit(lead)


def page_lead_detail():
    if 'selected_lead_id' not in st.session_state:
        st.warning("No lead selected")
        if st.button("← Back to Leads"):
            st.session_state.page = 'leads'
            st.rerun()
        return
    
    lead_id = st.session_state.selected_lead_id
    
    # ✅ UPDATED: Fetch lead details using new endpoint
    lead_resp = api_get(f"leads/id/{lead_id}")
    if not lead_resp or not lead_resp.get('success'):
        st.error("Lead not found")
        if st.button("← Back to Leads"):
            st.session_state.page = 'leads'
            st.rerun()
        return
    
    lead = lead_resp['data']
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title(f"👤 {lead.get('name', 'Unknown')}")
    with col2:
        if st.button("← Back to Leads"):
            st.session_state.page = 'leads'
            del st.session_state.selected_lead_id  # Clean up
            st.rerun()
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Overview", 
        "💬 WhatsApp Chat", 
        "📞 Call History", 
        "📊 Analytics",
        "✏️ Edit"
    ])
    
    with tab1:
        render_lead_overview(lead)
    
    with tab2:
        render_whatsapp_conversation(lead)
    
    with tab3:
        render_call_history(lead)
    
    with tab4:
        render_lead_analytics(lead)
    
    with tab5:
        render_lead_edit(lead)




def render_lead_overview(lead):
    """Render lead overview section with custom fields"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Basic Info")
        st.write(f"**ID:** {lead['id']}")
        st.write(f"**Phone:** {lead['phone_number']}")
        st.write(f"**Email:** {lead.get('email', 'N/A')}")
        st.write(f"**Status:** {lead['lead_status']}")
        st.write(f"**Interest:** {lead.get('interest_level', 0)}/10")
        st.write(f"**Source:** {lead.get('lead_source', 'N/A')}")
    
    with col2:
        st.markdown("### Standard Fields")
        st.write(f"**Chess Rating:** {lead.get('chess_rating', 'N/A')}")
        st.write(f"**Location:** {lead.get('location', 'N/A')}")
        st.write(f"**Availability:** {lead.get('availability', 'N/A')}")
        st.write(f"**Last Contact:** {lead.get('last_contacted', 'N/A')[:10] if lead.get('last_contacted') else 'Never'}")
    
    # ✅ NEW: Load custom field data
    st.divider()
    st.markdown("### 🎯 Custom Fields")
    
    custom_fields_resp = api_get(f"leads/{lead['id']}/custom-fields")
    
    if custom_fields_resp and custom_fields_resp.get('success'):
        custom_fields = custom_fields_resp['data']
        
        if custom_fields:
            # Display in a nice grid
            cols = st.columns(3)
            for idx, (field_key, field_data) in enumerate(custom_fields.items()):
                with cols[idx % 3]:
                    st.metric(
                        label=field_data.get('label', field_key),
                        value=field_data.get('value', 'N/A')
                    )
                    
                    # Show confidence if from AI extraction
                    if field_data.get('source') == 'ai_extraction':
                        confidence = field_data.get('confidence_score', 0) * 100
                        st.caption(f"🤖 AI Extracted ({confidence:.0f}% confidence)")
        else:
            st.info("No custom fields data yet")
    else:
        st.info("No custom fields configured for this lead")
    
    st.divider()
    
    # Quick Actions (rest remains the same)
    st.markdown("### Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📞 Make Call", use_container_width=True):
            st.session_state.selected_lead_for_call = lead
            st.session_state.page = 'calling'
            st.rerun()
    
    with col2:
        if st.button("💬 Send WhatsApp", use_container_width=True):
            st.session_state.selected_lead_for_whatsapp = lead
            st.session_state.page = 'whatsapp'
            st.rerun()
    
    with col3:
        if st.button("📅 Schedule Call", use_container_width=True):
            st.session_state.selected_lead_for_schedule = lead
            st.session_state.page = 'scheduled_calls'
            st.rerun()



def render_whatsapp_conversation(lead):
    """Render WhatsApp conversation history with sentiment"""
    st.markdown("### 💬 WhatsApp Conversation History")
    
    # Get conversation
    conv_resp = api_get(f"conversations/{lead['phone_number']}")
    messages_resp = api_get(f"conversations/{lead['phone_number']}/messages?limit=100")
    
    if messages_resp and messages_resp.get('success') and messages_resp.get('data'):
        messages = messages_resp['data']
        
        # Display conversation summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Messages", len(messages))
        with col2:
            user_msgs = len([m for m in messages if m.get('is_from_user')])
            st.metric("User Messages", user_msgs)
        with col3:
            bot_msgs = len(messages) - user_msgs
            st.metric("Bot Messages", bot_msgs)
        
        st.divider()
        
        # Display messages
        for msg in reversed(messages):
            timestamp = msg.get('timestamp', '')[:19] if msg.get('timestamp') else 'N/A'
            message_body = msg.get('message_body', '')
            is_from_user = msg.get('is_from_user', False)
            
            if is_from_user:
                st.markdown(f"""
                <div class="conversation-user">
                    <small>{timestamp}</small><br>
                    <strong>👤 User:</strong> {message_body}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="conversation-bot">
                    <small>{timestamp}</small><br>
                    <strong>🤖 AI:</strong> {message_body}
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No conversation history yet")
    
    # Show AI Summary if available
    if conv_resp and conv_resp.get('success') and conv_resp.get('data'):
        conv_data = conv_resp['data']
        if conv_data.get('ai_summary'):
            st.markdown("### 📝 AI Summary")
            st.info(conv_data['ai_summary'])

def render_call_history(lead):
    """Render call history with transcripts and sentiment"""
    st.markdown("### 📞 Call History")
    
    calls_resp = api_get(f"call-logs/lead/{lead['id']}")
    
    if not calls_resp or not calls_resp.get('success') or not calls_resp.get('data'):
        st.info("No call history yet")
        return
    
    calls = calls_resp['data']
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Calls", len(calls))
    with col2:
        completed = len([c for c in calls if c['call_status'] == 'completed'])
        st.metric("Completed", completed)
    with col3:
        failed = len([c for c in calls if c['call_status'] == 'failed'])
        st.metric("Failed", failed)
    with col4:
        avg_duration = sum([c.get('call_duration', 0) for c in calls]) / len(calls) if calls else 0
        st.metric("Avg Duration", f"{int(avg_duration)}s")
    
    st.divider()
    
    # Display each call
    for call in calls:
        with st.expander(f"📞 {call['call_type']} - {call['call_status']} - {call['created_at'][:19]}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Call SID:** {call['call_sid']}")
                st.write(f"**Type:** {call['call_type']}")
                st.write(f"**Status:** {call['call_status']}")
                st.write(f"**Duration:** {call.get('call_duration', 0)}s")
            
            with col2:
                # Sentiment Analysis
                if call.get('sentiment'):
                    sentiment_data = call['sentiment'] if isinstance(call['sentiment'], dict) else json.loads(call['sentiment'])
                    sentiment = sentiment_data.get('sentiment', 'neutral')
                    tone_score = sentiment_data.get('tone_score', 5)
                    
                    sentiment_class = f"sentiment-{sentiment}"
                    st.markdown(f"**Sentiment:** <span class='{sentiment_class}'>{sentiment.upper()}</span>", 
                              unsafe_allow_html=True)
                    st.write(f"**Tone Score:** {tone_score}/10")
            
            # Summary
            if call.get('summary'):
                summary_data = call['summary'] if isinstance(call['summary'], dict) else json.loads(call['summary'])
                st.markdown("**Summary:**")
                st.info(summary_data.get('summary', 'No summary available'))
                
                if summary_data.get('intent'):
                    st.write(f"**Intent:** {summary_data['intent']}")
            
            # Transcript
            if call.get('transcript'):
                st.markdown("**Transcript:**")
                st.text_area("", call['transcript'], height=200, key=f"transcript_{call['call_sid']}")
            
            # Recording
            if call.get('recording_url'):
                st.markdown(f"[🎵 Listen to Recording]({call['recording_url']})")

def render_lead_analytics(lead):
    """Render lead analytics and insights"""
    st.markdown("### 📊 Lead Analytics")
    
    # Sentiment trend over time
    calls_resp = api_get(f"call-logs/lead/{lead['id']}")
    
    if calls_resp and calls_resp.get('success') and calls_resp.get('data'):
        calls = calls_resp['data']
        
        # Extract sentiment scores
        sentiment_data = []
        for call in calls:
            if call.get('sentiment'):
                sent = call['sentiment'] if isinstance(call['sentiment'], dict) else json.loads(call['sentiment'])
                sentiment_data.append({
                    'date': call['created_at'][:10],
                    'tone_score': sent.get('tone_score', 5),
                    'sentiment': sent.get('sentiment', 'neutral')
                })
        
        if sentiment_data:
            df = pd.DataFrame(sentiment_data)
            
            # Sentiment Trend Chart
            st.subheader("Sentiment Trend Over Time")
            fig = px.line(df, x='date', y='tone_score', 
                         title='Tone Score Progression',
                         labels={'tone_score': 'Tone Score', 'date': 'Date'})
            st.plotly_chart(fig, use_container_width=True)
            
            # Sentiment Distribution
            st.subheader("Sentiment Distribution")
            sentiment_counts = df['sentiment'].value_counts()
            fig2 = px.pie(values=sentiment_counts.values, 
                         names=sentiment_counts.index,
                         title='Call Sentiment Breakdown')
            st.plotly_chart(fig2, use_container_width=True)
    
    # Engagement metrics
    st.subheader("Engagement Metrics")
    col1, col2, col3 = st.columns(3)
    
    # Get message count
    messages_resp = api_get(f"conversations/{lead['phone_number']}/messages?limit=1000")
    msg_count = len(messages_resp['data']) if messages_resp and messages_resp.get('success') else 0
    
    with col1:
        st.metric("WhatsApp Messages", msg_count)
    
    with col2:
        call_count = len(calls_resp['data']) if calls_resp and calls_resp.get('success') else 0
        st.metric("Total Calls", call_count)
    
    with col3:
        st.metric("Interest Level", f"{lead.get('interest_level', 0)}/10")

def render_lead_edit(lead):
    """Render lead edit form"""
    st.markdown("### ✏️ Edit Lead Information")
    
    with st.form("edit_lead_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_name = st.text_input("Name", value=lead.get('name', ''))
            new_email = st.text_input("Email", value=lead.get('email', ''))
            new_status = st.selectbox("Status", 
                ["new", "contacted", "qualified", "lost"],
                index=["new", "contacted", "qualified", "lost"].index(lead['lead_status']))
            new_interest = st.slider("Interest Level", 1, 10, lead.get('interest_level', 5))
        
        with col2:
            new_location = st.text_input("Location", value=lead.get('location', ''))
            new_chess_rating = st.text_input("Chess Rating", value=lead.get('chess_rating', ''))
            new_availability = st.text_input("Availability", value=lead.get('availability', ''))
        
        new_notes = st.text_area("Notes", value=lead.get('notes', ''), height=100)
        
        submitted = st.form_submit_button("Update Lead", use_container_width=True)
        
        if submitted:
            update_data = {
                "name": new_name,
                "email": new_email,
                "lead_status": new_status,
                "interest_level": new_interest,
                "location": new_location,
                "chess_rating": new_chess_rating,
                "availability": new_availability,
                "notes": new_notes
            }
            
            result = api_patch(f"leads/{lead['id']}", update_data)
            
            if result and result.get('success'):
                st.success("✅ Lead updated successfully!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Failed to update lead")




def render_lead_sources_settings():
    """
    Render Lead Sources OAuth connection management
    """
    st.subheader("📥 Lead Source Integrations")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <h3 style="margin: 0 0 10px 0;">🚀 Connect Your Lead Sources</h3>
        <p style="margin: 0; font-size: 14px;">
            Automatically import leads from Meta Ads, Google Ads, and LinkedIn Ads with OAuth
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get OAuth status
    oauth_status_resp = api_get(f"oauth/status/{st.session_state.company_id}")
    
    if oauth_status_resp and oauth_status_resp.get('success'):
        oauth_data = oauth_status_resp['data']
        
        # Create a dict for easy lookup
        oauth_dict = {item['platform']: item for item in oauth_data}
    else:
        oauth_dict = {}
    
    # ========================================
    # META ADS SECTION
    # ========================================
    st.markdown("---")
    st.markdown("### 📘 Meta Ads (Facebook)")
    
    meta_connected = 'meta' in oauth_dict and oauth_dict['meta'].get('is_active')
    
    if meta_connected:
        meta_info = oauth_dict['meta']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📱 Account", meta_info.get('account_name', 'Unknown'))
        with col2:
            days_left = meta_info.get('days_until_expiry')
            if days_left:
                if days_left < 7:
                    st.metric("⚠️ Token Expires", f"{days_left} days", delta_color="inverse")
                else:
                    st.metric("🔑 Token Valid", f"{days_left} days")
            else:
                st.metric("🔑 Status", "Active")
        with col3:
            st.success("✅ Connected")
        
        # Show lead forms
        with st.expander("📋 View Lead Forms"):
            forms_resp = api_get(f"lead-sources/meta/forms/{st.session_state.company_id}")
            if forms_resp and forms_resp.get('success'):
                forms = forms_resp['forms']
                if forms:
                    for form in forms:
                        st.write(f"**{form['name']}** (ID: {form['id']}) - Leads: {form.get('leads_count', 0)}")
                else:
                    st.info("No lead forms found")
        
        # Disconnect button
        if st.button("❌ Disconnect Meta", key="disconnect_meta"):
            result = api_delete(f"oauth/{st.session_state.company_id}/meta")
            if result and result.get('success'):
                st.success("Meta Ads disconnected!")
                time.sleep(1)
                st.rerun()
    else:
        st.warning("⚠️ Meta Ads not connected")
        
        if st.button("🔗 Connect Meta Ads", use_container_width=True, type="primary", key="connect_meta"):
            with st.spinner("Initializing Meta OAuth..."):
                oauth_resp = api_get(f"oauth/meta/start?company_id={st.session_state.company_id}")
                
                if oauth_resp and oauth_resp.get('success'):
                    # auth_url = oauth_resp['data']['auth_url']
                    auth_url = oauth_resp.get('data', {}).get('auth_url') or oauth_resp.get('auth_url')

                    
                    st.markdown(f"""
                    <div style="background: #e3f2fd; padding: 30px; border-radius: 15px; margin: 20px 0; text-align: center;">
                        <h3 style="color: #1976d2; margin-bottom: 20px;">🔐 Meta OAuth Ready</h3>
                        <p style="color: #424242; margin-bottom: 25px;">
                            Click below to authorize access to your Meta Ads account:
                        </p>
                        <a href="{auth_url}" target="_blank" style="
                            background: linear-gradient(135deg, #1877F2 0%, #0C63D4 100%);
                            color: white; 
                            padding: 18px 40px; 
                            border-radius: 10px; 
                            text-decoration: none; 
                            display: inline-block;
                            font-weight: bold;
                            font-size: 18px;
                            box-shadow: 0 4px 15px rgba(24, 119, 242, 0.4);
                        ">
                            🚀 Authorize Meta Ads
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("Failed to initialize Meta OAuth")
    
    # ========================================
    # GOOGLE ADS SECTION
    # ========================================
    st.markdown("---")
    st.markdown("### 🔴 Google Ads")
    
    google_connected = 'google_ads' in oauth_dict and oauth_dict['google_ads'].get('is_active')
    
    if google_connected:
        google_info = oauth_dict['google_ads']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📱 Customer ID", google_info.get('account_id', 'Unknown'))
        with col2:
            days_left = google_info.get('days_until_expiry')
            if days_left:
                if days_left < 7:
                    st.metric("⚠️ Token Expires", f"{days_left} days", delta_color="inverse")
                else:
                    st.metric("🔑 Token Valid", f"{days_left} days")
            else:
                st.metric("🔑 Status", "Active")
        with col3:
            st.success("✅ Connected")
        
        # Disconnect button
        if st.button("❌ Disconnect Google Ads", key="disconnect_google"):
            result = api_delete(f"oauth/{st.session_state.company_id}/google_ads")
            if result and result.get('success'):
                st.success("Google Ads disconnected!")
                time.sleep(1)
                st.rerun()
    else:
        st.warning("⚠️ Google Ads not connected")
        
        if st.button("🔗 Connect Google Ads", use_container_width=True, type="primary", key="connect_google"):
            with st.spinner("Initializing Google OAuth..."):
                oauth_resp = api_get(f"oauth/google-ads/start?company_id={st.session_state.company_id}")
                
                if oauth_resp and oauth_resp.get('success'):
                    # auth_url = oauth_resp['data']['auth_url']
                    auth_url = oauth_resp.get('data', {}).get('auth_url') or oauth_resp.get('auth_url')

                    
                    st.markdown(f"""
                    <div style="background: #e3f2fd; padding: 30px; border-radius: 15px; margin: 20px 0; text-align: center;">
                        <h3 style="color: #1976d2; margin-bottom: 20px;">🔐 Google OAuth Ready</h3>
                        <p style="color: #424242; margin-bottom: 25px;">
                            Click below to authorize access to your Google Ads account:
                        </p>
                        <a href="{auth_url}" target="_blank" style="
                            background: linear-gradient(135deg, #EA4335 0%, #FBBC04 100%);
                            color: white; 
                            padding: 18px 40px; 
                            border-radius: 10px; 
                            text-decoration: none; 
                            display: inline-block;
                            font-weight: bold;
                            font-size: 18px;
                            box-shadow: 0 4px 15px rgba(234, 67, 53, 0.4);
                        ">
                            🚀 Authorize Google Ads
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("Failed to initialize Google OAuth")
    
    # ========================================
    # LINKEDIN ADS SECTION
    # ========================================
    st.markdown("---")
    st.markdown("### 💼 LinkedIn Ads")
    
    linkedin_connected = 'linkedin' in oauth_dict and oauth_dict['linkedin'].get('is_active')
    
    if linkedin_connected:
        linkedin_info = oauth_dict['linkedin']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📱 Account", linkedin_info.get('account_name', 'Unknown'))
        with col2:
            days_left = linkedin_info.get('days_until_expiry')
            if days_left:
                if days_left < 7:
                    st.metric("⚠️ Token Expires", f"{days_left} days", delta_color="inverse")
                else:
                    st.metric("🔑 Token Valid", f"{days_left} days")
            else:
                st.metric("🔑 Status", "Active")
        with col3:
            st.success("✅ Connected")
        
        # Disconnect button
        if st.button("❌ Disconnect LinkedIn", key="disconnect_linkedin"):
            result = api_delete(f"oauth/{st.session_state.company_id}/linkedin")
            if result and result.get('success'):
                st.success("LinkedIn Ads disconnected!")
                time.sleep(1)
                st.rerun()
    else:
        st.warning("⚠️ LinkedIn Ads not connected")
        
        if st.button("🔗 Connect LinkedIn Ads", use_container_width=True, type="primary", key="connect_linkedin"):
            with st.spinner("Initializing LinkedIn OAuth..."):
                oauth_resp = api_get(f"oauth/linkedin/start?company_id={st.session_state.company_id}")
                
                if oauth_resp and oauth_resp.get('success'):
                    # auth_url = oauth_resp['data']['auth_url']
                    auth_url = oauth_resp.get('data', {}).get('auth_url') or oauth_resp.get('auth_url')

                    
                    st.markdown(f"""
                    <div style="background: #e3f2fd; padding: 30px; border-radius: 15px; margin: 20px 0; text-align: center;">
                        <h3 style="color: #1976d2; margin-bottom: 20px;">🔐 LinkedIn OAuth Ready</h3>
                        <p style="color: #424242; margin-bottom: 25px;">
                            Click below to authorize access to your LinkedIn Ads account:
                        </p>
                        <a href="{auth_url}" target="_blank" style="
                            background: linear-gradient(135deg, #0077B5 0%, #005885 100%);
                            color: white; 
                            padding: 18px 40px; 
                            border-radius: 10px; 
                            text-decoration: none; 
                            display: inline-block;
                            font-weight: bold;
                            font-size: 18px;
                            box-shadow: 0 4px 15px rgba(0, 119, 181, 0.4);
                        ">
                            🚀 Authorize LinkedIn Ads
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("Failed to initialize LinkedIn OAuth")
    
    # ========================================
    # LEAD SOURCE CONFIGURATIONS
    # ========================================
    st.markdown("---")
    st.markdown("### 🗺️ Lead Source Field Mappings")
    
    configs_resp = api_get(f"lead-sources/configs/{st.session_state.company_id}")
    
    if configs_resp and configs_resp.get('success') and configs_resp['data']:
        for config in configs_resp['data']:
            with st.expander(f"📋 {config['platform'].upper()} - {config['form_name']}"):
                st.write(f"**Form ID:** {config['form_id']}")
                st.write(f"**Status:** {'🟢 Active' if config['is_active'] else '🔴 Inactive'}")
                st.write(f"**Platform Connected:** {'✅ Yes' if config.get('platform_connected') else '❌ No'}")
                
                st.markdown("**Field Mappings:**")
                mappings = config['field_mappings']
                if mappings:
                    for platform_field, crm_field in mappings.items():
                        st.write(f"• `{platform_field}` → `{crm_field}`")
                else:
                    st.info("No field mappings configured")
                
                st.markdown(f"**Webhook URL:**")
                st.code(config['webhook_url'], language="text")
    else:
        st.info("No lead source configurations yet. Connect a platform above to get started!")
    
    # ========================================
    # IMPORT STATS
    # ========================================
    st.markdown("---")
    st.markdown("### 📊 Lead Import Statistics")
    
    stats_resp = api_get(f"lead-imports/stats/{st.session_state.company_id}")
    
    if stats_resp and stats_resp.get('success') and stats_resp['data']:
        df = pd.DataFrame(stats_resp['data'])
        
        # Group by platform and status
        summary = df.groupby(['platform', 'status'])['count'].sum().unstack(fill_value=0)
        
        st.dataframe(summary, use_container_width=True)
        
        # Visualization
        fig = px.bar(df, x='platform', y='count', color='status',
                    title='Lead Imports by Platform and Status',
                    barmode='group')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No import statistics available yet")



def render_whatsapp_oauth_setup(agent):
    """
    Render WhatsApp OAuth setup UI for an agent instance
    FIXED VERSION with proper error handling and status display
    """
    st.divider()
    st.markdown("### 🔧 WhatsApp Business Setup")
    
    # Check connection status with proper error handling
    try:
        status_resp = api_get(f"whatsapp/oauth/status/{agent['id']}")
        
        if not status_resp or not status_resp.get('success'):
            st.error("❌ Failed to check WhatsApp connection status")
            return
        
        status_data = status_resp.get('data', {})
        is_connected = status_data.get('is_connected', False)
        
        if is_connected:
            # ==================== CONNECTED STATE ====================
            st.success("✅ WhatsApp Business Connected!")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                phone = status_data.get('whatsapp_number', 'N/A')
                st.metric("📱 Phone Number", phone)
            
            with col2:
                days_left = status_data.get('days_until_expiry')
                if days_left is not None:
                    if days_left < 7:
                        st.metric("⚠️ Token Expires", f"{days_left} days", delta_color="inverse")
                    elif days_left < 30:
                        st.metric("🔑 Token Valid", f"{days_left} days")
                    else:
                        st.metric("🔑 Token Valid", f"{days_left} days", delta_color="normal")
                else:
                    st.metric("🔑 Token Status", "Unknown")
            
            with col3:
                needs_renewal = status_data.get('needs_renewal', False)
                if needs_renewal:
                    st.warning("⚠️ Renewal Needed")
                else:
                    st.success("✅ Healthy")
            
            # Webhook Configuration
            st.markdown("#### 🌐 Webhook Configuration")
            webhook_url = f"{API_BASE_URL.replace('/api', '')}/api/webhooks/whatsapp-universal"
            
            st.info("📌 **Webhook URL** (Use this in Meta Developer Console)")
            st.code(webhook_url, language="text")
            
            # Action buttons
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button("🔄 Reconnect WhatsApp", 
                           key=f"reconnect_{agent['id']}",
                           help="Refresh connection if token expired"):
                    with st.spinner("Initiating OAuth flow..."):
                        oauth_resp = api_get(
                            f"whatsapp/oauth/start?company_id={st.session_state.company_id}&agent_instance_id={agent['id']}"
                        )
                        
                        if oauth_resp and oauth_resp.get('success'):
                            auth_url = oauth_resp['data']['auth_url']
                            st.success("✅ OAuth flow ready!")
                            st.markdown(f"""
                            <div style="background: #d4edda; padding: 20px; border-radius: 10px; margin: 10px 0;">
                                <h4 style="color: #155724;">🔗 Click to Reconnect</h4>
                                <a href="{auth_url}" target="_blank" style="
                                    background: #28a745; 
                                    color: white; 
                                    padding: 12px 24px; 
                                    border-radius: 5px; 
                                    text-decoration: none; 
                                    display: inline-block;
                                    font-weight: bold;
                                ">
                                    Open Facebook Authorization
                                </a>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.error("❌ Failed to start OAuth flow")
            
            with col_btn2:
                if st.button("❌ Disconnect", 
                           key=f"disconnect_{agent['id']}",
                           help="Remove WhatsApp connection"):
                    st.warning("⚠️ This will disconnect your WhatsApp Business account")
                    
                    if st.checkbox(f"✓ I confirm disconnection", 
                                 key=f"confirm_disconnect_{agent['id']}"):
                        with st.spinner("Disconnecting..."):
                            disconnect_resp = api_delete(f"whatsapp/oauth/disconnect/{agent['id']}")
                            
                            if disconnect_resp and disconnect_resp.get('success'):
                                st.success("✅ WhatsApp disconnected successfully!")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("❌ Failed to disconnect")
        
        else:
            # ==================== NOT CONNECTED STATE ====================
            st.warning("⚠️ WhatsApp not connected")
            
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        color: white; padding: 30px; border-radius: 15px; margin: 20px 0;">
                <h3 style="margin: 0 0 15px 0;">🚀 Connect Your WhatsApp Business</h3>
                <p style="font-size: 16px; line-height: 1.6; margin: 0;">
                    <strong>Easy 3-Step Process:</strong><br>
                    1️⃣ Click "Connect WhatsApp" below<br>
                    2️⃣ Login with your Facebook account<br>
                    3️⃣ Approve the connection<br><br>
                    <strong>That's it!</strong> No technical knowledge required.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Main connect button
            if st.button("🔗 Connect WhatsApp Business", 
                        use_container_width=True, 
                        type="primary",
                        key=f"oauth_connect_{agent['id']}",
                        help="Start secure OAuth flow"):
                
                with st.spinner("🔄 Initializing secure connection..."):
                    oauth_resp = api_get(
                        f"whatsapp/oauth/start?company_id={st.session_state.company_id}&agent_instance_id={agent['id']}"
                    )
                    
                    if oauth_resp and oauth_resp.get('success'):
                        auth_url = oauth_resp['data']['auth_url']
                        
                        st.markdown(f"""
                        <div style="background: #e3f2fd; padding: 30px; border-radius: 15px; margin: 20px 0; text-align: center;">
                            <h3 style="color: #1976d2; margin-bottom: 20px;">🔐 Secure Connection Ready</h3>
                            <p style="color: #424242; margin-bottom: 25px; font-size: 16px;">
                                Click the button below to connect your WhatsApp Business account via Facebook OAuth:
                            </p>
                            <a href="{auth_url}" target="_blank" style="
                                background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
                                color: white; 
                                padding: 18px 40px; 
                                border-radius: 10px; 
                                text-decoration: none; 
                                display: inline-block;
                                font-weight: bold;
                                font-size: 18px;
                                box-shadow: 0 4px 15px rgba(37, 211, 102, 0.4);
                                transition: transform 0.2s;
                            "
                            onmouseover="this.style.transform='translateY(-2px)'" 
                            onmouseout="this.style.transform='translateY(0)'">
                                🚀 Open Facebook Authorization
                            </a>
                            <p style="color: #666; margin-top: 20px; font-size: 14px;">
                                You'll be redirected to Facebook for secure authentication.<br>
                                After approval, you'll receive setup instructions.
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Show expiry info
                        expires_in = oauth_resp['data'].get('expires_in', 3600)
                        st.info(f"⏱️ This authorization link expires in {expires_in // 60} minutes")
                        
                    else:
                        st.error("❌ Failed to initialize OAuth flow")
                        st.error("**Possible causes:**")
                        st.markdown("""
                        - META_APP_ID or META_APP_SECRET not configured in environment
                        - BASE_URL not set correctly
                        - Meta Developer App not created
                        """)
                        
                        # Show debug info
                        with st.expander("🔍 Debug Information"):
                            st.json({
                                "company_id": st.session_state.company_id,
                                "agent_instance_id": agent['id'],
                                "api_response": oauth_resp
                            })
            
            # Advanced manual setup (fallback)
            st.divider()
            with st.expander("🔧 Advanced: Manual Setup (Not Recommended)", expanded=False):
                st.warning("⚠️ **Warning:** Manual setup is complex and error-prone. OAuth method above is highly recommended.")
                
                st.markdown("""
                **Manual setup requires:**
                - Access to Meta Developer Console
                - Understanding of WhatsApp Business API
                - Manual token management
                
                **Use this only if OAuth fails.**
                """)
                
                with st.form(f"manual_whatsapp_{agent['id']}"):
                    st.markdown("**Meta WhatsApp Business API Credentials:**")
                    
                    col_m1, col_m2 = st.columns(2)
                    
                    with col_m1:
                        access_token = st.text_input(
                            "Access Token*", 
                            type="password",
                            help="From Meta Developer Console → WhatsApp → API Setup"
                        )
                        phone_number_id = st.text_input(
                            "Phone Number ID*",
                            help="Found in WhatsApp → Configuration"
                        )
                    
                    with col_m2:
                        business_account_id = st.text_input(
                            "Business Account ID",
                            help="Optional: Your WhatsApp Business Account ID"
                        )
                    
                    st.info("💡 **Tip:** Get these from Meta Developer Console → Your App → WhatsApp → API Setup")
                    
                    submitted = st.form_submit_button("💾 Save Manual Credentials", use_container_width=True)
                    
                    if submitted:
                        if not access_token or not phone_number_id:
                            st.error("❌ Access Token and Phone Number ID are required")
                        else:
                            with st.spinner("Saving credentials..."):
                                creds_data = {
                                    "access_token": access_token,
                                    "phone_number_id": phone_number_id,
                                    "business_account_id": business_account_id if business_account_id else None
                                }
                                
                                result = api_post(
                                    f"agent-instances/{agent['id']}/whatsapp-credentials", 
                                    creds_data
                                )
                                
                                if result and result.get('success'):
                                    st.success("✅ Manual credentials saved successfully!")
                                    
                                    st.markdown("### 📋 Next Steps:")
                                    st.info(f"**Webhook URL:** {result.get('webhook_url')}")
                                    st.code(result.get('webhook_url'), language="text")
                                    
                                    st.info(f"**Verify Token:** {result.get('verify_token')}")
                                    st.code(result.get('verify_token'), language="text")
                                    
                                    st.markdown("""
                                    **Register these in Meta Developer Console:**
                                    1. Go to your app → WhatsApp → Configuration
                                    2. Paste Webhook URL
                                    3. Paste Verify Token
                                    4. Click "Verify and Save"
                                    5. Subscribe to "messages" webhook field
                                    """)
                                    
                                    time.sleep(2)
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to save credentials")
                                    if result:
                                        st.error(f"Error: {result.get('error', 'Unknown error')}")
    
    except Exception as e:
        st.error(f"❌ Error loading WhatsApp setup: {str(e)}")
        st.exception(e)



def render_twilio_oauth_setup(agent):
    """
    Render Twilio OAuth setup UI for voice agent instances
    """
    st.divider()
    st.markdown("### 📞 Twilio Voice Setup")
    
    try:
        status_resp = api_get(f"twilio/oauth/status/{agent['id']}")
        
        if not status_resp or not status_resp.get('success'):
            st.error("❌ Failed to check Twilio connection status")
            return
        
        status_data = status_resp.get('data', {})
        is_connected = status_data.get('is_connected', False)
        
        if is_connected:
            # ==================== CONNECTED STATE ====================
            st.success("✅ Twilio Account Connected!")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                phone = status_data.get('phone_number', 'N/A')
                st.metric("📱 Phone Number", phone)
            
            with col2:
                days_left = status_data.get('days_until_expiry')
                if days_left is not None:
                    if days_left < 30:
                        st.metric("⚠️ Token Expires", f"{days_left} days", delta_color="inverse")
                    else:
                        st.metric("🔑 Token Valid", f"{days_left} days", delta_color="normal")
                else:
                    st.metric("🔑 Token Status", "Active")
            
            with col3:
                needs_renewal = status_data.get('needs_renewal', False)
                if needs_renewal:
                    st.warning("⚠️ Renewal Needed")
                else:
                    st.success("✅ Healthy")
            
            # Webhook Configuration
            st.markdown("#### 🌐 Webhook Configuration")
            webhook_url = f"{API_BASE_URL.replace('/api', '')}/twilio/voice-webhook"
            
            st.info("📌 **Voice Webhook URL** (Configure in Twilio Console)")
            st.code(webhook_url, language="text")
            
            st.markdown("""
            **Setup Instructions:**
            1. Go to [Twilio Console → Phone Numbers](https://console.twilio.com/us1/develop/phone-numbers/manage/incoming)
            2. Click on your phone number
            3. Under **Voice & Fax** → Set:
               - **A Call Comes In:** Webhook
               - **URL:** (paste above webhook URL)
               - **HTTP Method:** POST
            4. Click **Save**
            """)
            
            # Action buttons
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button("🔄 Reconnect Twilio", 
                           key=f"reconnect_twilio_{agent['id']}",
                           help="Refresh connection if expired"):
                    with st.spinner("Initiating OAuth flow..."):
                        oauth_resp = api_get(
                            f"twilio/oauth/start?company_id={st.session_state.company_id}&agent_instance_id={agent['id']}"
                        )
                        
                        if oauth_resp and oauth_resp.get('success'):
                            auth_url = oauth_resp['data']['auth_url']
                            st.success("✅ OAuth flow ready!")
                            st.markdown(f"""
                            <div style="background: #d4edda; padding: 20px; border-radius: 10px; margin: 10px 0;">
                                <h4 style="color: #155724;">🔗 Click to Reconnect</h4>
                                <a href="{auth_url}" target="_blank" style="
                                    background: #28a745; 
                                    color: white; 
                                    padding: 12px 24px; 
                                    border-radius: 5px; 
                                    text-decoration: none; 
                                    display: inline-block;
                                    font-weight: bold;
                                ">
                                    Open Twilio Authorization
                                </a>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.error("❌ Failed to start OAuth flow")
            
            with col_btn2:
                if st.button("❌ Disconnect", 
                           key=f"disconnect_twilio_{agent['id']}",
                           help="Remove Twilio connection"):
                    st.warning("⚠️ This will disconnect your Twilio account")
                    
                    if st.checkbox(f"✓ I confirm disconnection", 
                                 key=f"confirm_disconnect_twilio_{agent['id']}"):
                        with st.spinner("Disconnecting..."):
                            disconnect_resp = api_delete(f"twilio/oauth/disconnect/{agent['id']}")
                            
                            if disconnect_resp and disconnect_resp.get('success'):
                                st.success("✅ Twilio disconnected successfully!")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("❌ Failed to disconnect")
        
        else:
            # ==================== NOT CONNECTED STATE ====================
            st.warning("⚠️ Twilio not connected")
            
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        color: white; padding: 30px; border-radius: 15px; margin: 20px 0;">
                <h3 style="margin: 0 0 15px 0;">🚀 Connect Your Twilio Account</h3>
                <p style="font-size: 16px; line-height: 1.6; margin: 0;">
                    <strong>Easy 3-Step Process:</strong><br>
                    1️⃣ Click "Connect Twilio" below<br>
                    2️⃣ Login to your Twilio account<br>
                    3️⃣ Approve the connection<br><br>
                    <strong>That's it!</strong> Your phone numbers will be auto-configured.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Main connect button
            if st.button("🔗 Connect Twilio Account", 
                        use_container_width=True, 
                        type="primary",
                        key=f"oauth_connect_twilio_{agent['id']}",
                        help="Start secure OAuth flow"):
                
                with st.spinner("🔄 Initializing secure connection..."):
                    oauth_resp = api_get(
                        f"twilio/oauth/start?company_id={st.session_state.company_id}&agent_instance_id={agent['id']}"
                    )
                    
                    if oauth_resp and oauth_resp.get('success'):
                        auth_url = oauth_resp['data']['auth_url']
                        
                        st.markdown(f"""
                        <div style="background: #e3f2fd; padding: 30px; border-radius: 15px; margin: 20px 0; text-align: center;">
                            <h3 style="color: #1976d2; margin-bottom: 20px;">🔐 Secure Connection Ready</h3>
                            <p style="color: #424242; margin-bottom: 25px; font-size: 16px;">
                                Click the button below to connect your Twilio account via OAuth:
                            </p>
                            <a href="{auth_url}" target="_blank" style="
                                background: linear-gradient(135deg, #F22F46 0%, #E01B33 100%);
                                color: white; 
                                padding: 18px 40px; 
                                border-radius: 10px; 
                                text-decoration: none; 
                                display: inline-block;
                                font-weight: bold;
                                font-size: 18px;
                                box-shadow: 0 4px 15px rgba(242, 47, 70, 0.4);
                                transition: transform 0.2s;
                            "
                            onmouseover="this.style.transform='translateY(-2px)'" 
                            onmouseout="this.style.transform='translateY(0)'">
                                🚀 Open Twilio Authorization
                            </a>
                            <p style="color: #666; margin-top: 20px; font-size: 14px;">
                                You'll be redirected to Twilio for secure authentication.<br>
                                After approval, your phone numbers will be auto-configured.
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        expires_in = oauth_resp['data'].get('expires_in', 600)
                        st.info(f"⏱️ This authorization link expires in {expires_in // 60} minutes")
                        
                    else:
                        st.error("❌ Failed to initialize OAuth flow")
                        st.error("**Possible causes:**")
                        st.markdown("""
                        - TWILIO_APP_SID or TWILIO_APP_SECRET not configured in environment
                        - BASE_URL not set correctly
                        - Twilio OAuth app not created
                        """)
                        
                        with st.expander("🔍 Debug Information"):
                            st.json({
                                "company_id": st.session_state.company_id,
                                "agent_instance_id": agent['id'],
                                "api_response": oauth_resp
                            })
    
    except Exception as e:
        st.error(f"❌ Error loading Twilio setup: {str(e)}")
        st.exception(e)




def render_airtel_sip_setup(agent):
    """
    Render Airtel SIP configuration UI
    """
    st.divider()
    st.markdown("### 📡 Airtel SIP Configuration")
    
    try:
        status_resp = api_get(f"sip/status/{agent['id']}")
        
        if not status_resp or not status_resp.get('success'):
            st.error("❌ Failed to check SIP status")
            return
        
        status_data = status_resp.get('data', {})
        is_configured = status_data.get('is_configured', False)
        provider = status_data.get('provider', 'none')
        
        if is_configured and provider in ['airtel', 'custom']:
            # ==================== CONFIGURED STATE ====================
            st.success(f"✅ {provider.upper()} SIP Configured!")
            
            col1, col2 = st.columns(2)
            
            with col1:
                phone = status_data.get('phone_number', 'N/A')
                st.metric("📱 DID Number", phone)
            
            with col2:
                st.metric("🌐 Provider", provider.upper())
            
            st.info("💡 **Note:** SIP calls are routed through Twilio's SIP infrastructure")
            
            # Update credentials
            with st.expander("🔧 Update SIP Credentials"):
                with st.form(f"update_sip_{agent['id']}"):
                    st.markdown("**Update Airtel SIP Details:**")
                    
                    sip_domain = st.text_input("SIP Domain*", placeholder="sip.airtel.in")
                    sip_username = st.text_input("SIP Username*", placeholder="your_username")
                    sip_password = st.text_input("SIP Password*", type="password")
                    did_number = st.text_input("DID Number*", placeholder="+911234567890")
                    
                    if st.form_submit_button("Update SIP Credentials"):
                        if not all([sip_domain, sip_username, sip_password, did_number]):
                            st.error("All fields are required!")
                        else:
                            result = api_post("airtel-sip/configure", {
                                "agent_instance_id": agent['id'],
                                "sip_domain": sip_domain,
                                "sip_username": sip_username,
                                "sip_password": sip_password,
                                "did_number": did_number
                            })
                            
                            if result and result.get('success'):
                                st.success("✅ SIP credentials updated!")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("Failed to update credentials")
        
        else:
            # ==================== NOT CONFIGURED STATE ====================
            st.warning("⚠️ Airtel SIP not configured")
            
            st.markdown("""
            <div style="background: #fff3cd; padding: 20px; border-radius: 10px; margin: 10px 0;">
                <h4 style="color: #856404;">📋 Prerequisites:</h4>
                <ul style="color: #856404;">
                    <li>Active Airtel SIP trunk account</li>
                    <li>DID number assigned by Airtel</li>
                    <li>SIP credentials (domain, username, password)</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form(f"setup_sip_{agent['id']}"):
                st.markdown("**Enter Airtel SIP Credentials:**")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    sip_domain = st.text_input("SIP Domain*", placeholder="sip.airtel.in", help="Provided by Airtel")
                    sip_username = st.text_input("SIP Username*", placeholder="your_username")
                
                with col2:
                    sip_password = st.text_input("SIP Password*", type="password")
                    did_number = st.text_input("DID Number*", placeholder="+911234567890", help="Your Airtel DID number")
                
                st.info("💡 **Tip:** Get these credentials from your Airtel SIP account dashboard")
                
                submitted = st.form_submit_button("Configure Airtel SIP", use_container_width=True)
                
                if submitted:
                    if not all([sip_domain, sip_username, sip_password, did_number]):
                        st.error("All fields are required!")
                    else:
                        with st.spinner("Configuring SIP..."):
                            result = api_post("airtel-sip/configure", {
                                "agent_instance_id": agent['id'],
                                "sip_domain": sip_domain,
                                "sip_username": sip_username,
                                "sip_password": sip_password,
                                "did_number": did_number
                            })
                            
                            if result and result.get('success'):
                                st.success("✅ Airtel SIP configured successfully!")
                                st.info(f"**Your DID Number:** {result.get('phone_number')}")
                                time.sleep(2)
                                st.rerun()
                            else:
                                st.error("Failed to configure SIP")
                                if result:
                                    st.error(f"Error: {result.get('error')}")
    
    except Exception as e:
        st.error(f"❌ Error loading SIP setup: {str(e)}")
        st.exception(e)







def render_email_scanning_settings():
    """
    Render Email Scanning OAuth setup and management UI
    """
    st.subheader("📧 Email Inbox Scanning")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <h3 style="margin: 0 0 10px 0;">🚀 Auto-Extract Leads from Your Email Inbox</h3>
        <p style="margin: 0; font-size: 14px;">
            Connect your Gmail or Outlook account to automatically scan emails for lead information.
            Our AI extracts contact details and creates leads automatically!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get email scanning status
    status_resp = api_get(f"email/status/{st.session_state.company_id}")
    
    if status_resp and status_resp.get('success'):
        email_accounts = status_resp['data']
        
        if email_accounts:
            st.markdown("### 📬 Connected Email Accounts")
            
            for account in email_accounts:
                with st.expander(f"📧 {account['email_address']} ({account['provider'].upper()})"):
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        status_icon = "🟢" if account['is_active'] else "🔴"
                        st.metric("Status", f"{status_icon} {'Active' if account['is_active'] else 'Inactive'}")
                    
                    with col2:
                        st.metric("📨 Total Scanned", account.get('total_scanned', 0))
                    
                    with col3:
                        st.metric("👥 Leads Extracted", account.get('leads_extracted', 0))
                    
                    with col4:
                        days_left_raw = account.get('days_until_expiry')
                        token_expired = account.get('token_expired', False)
                        
                        if token_expired:
                            st.metric("Token Status", "⚠️ EXPIRED", delta_color="inverse")
                        elif days_left_raw is not None:
                            try:
                                days_left = int(float(days_left_raw))
                                if days_left == 0:
                                    st.metric("Token Status", "⚠️ EXPIRES TODAY", delta_color="inverse")
                                elif days_left < 7:
                                    st.metric("Token Expires", f"{days_left} days", delta_color="inverse")
                                else:
                                    st.metric("Token Valid", f"{days_left} days")
                            except (ValueError, TypeError):
                                st.metric("Token Status", "Unknown")
                        else:
                            st.metric("Status", "Active")
                    
                    # Last scan info
                    if account.get('last_scan_at'):
                        st.info(f"🕐 Last scanned: {account['last_scan_at'][:19]}")
                    else:
                        st.warning("⚠️ Never scanned yet")
                    
                    # Reauth warning
                    if account.get('needs_reauth'):
                        st.error("⚠️ **Token expired!** Please reconnect your account.")
                    
                    # Action buttons
                    st.divider()
                    col_btn1, col_btn2, col_btn3 = st.columns(3)
                    
                    # with col_btn1:
                    #     if st.button("🔄 Scan Now", key=f"scan_{account['id']}", 
                    #                help="Manually trigger email scan"):
                    #         with st.spinner("Scanning inbox..."):
                    #             scan_resp = api_post(f"email/scan/{st.session_state.company_id}", {})
                                
                    #             if scan_resp and scan_resp.get('success'):
                    #                 scanned = scan_resp.get('scanned', 0)
                    #                 st.success(f"✅ Scanned {scanned} emails!")
                                    
                    #                 if scan_resp.get('results'):
                    #                     new_leads = sum(1 for r in scan_resp['results'] if r.get('is_new'))
                    #                     st.info(f"📊 {new_leads} new leads created!")
                                    
                    #                 time.sleep(1)
                    #                 st.rerun()
                    #             else:
                    #                 st.error("❌ Scan failed. Check credentials.")



                    with col_btn1:
                        if st.button("🔄 Scan Now", key=f"scan_{account['id']}", 
                                help="Manually trigger email scan"):
                            with st.spinner("🔍 Scanning inbox with AI filter..."):
                                try:
                                    scan_resp = api_post(
                                        f"email/scan/{st.session_state.company_id}", 
                                        {},
                                        timeout=90  # Increased timeout for AI processing
                                    )
                                    
                                    if scan_resp and scan_resp.get('success'):
                                        scanned = scan_resp.get('scanned', 0)
                                        results = scan_resp.get('results', [])
                                        errors = scan_resp.get('errors', [])
                                        
                                        if scanned > 0:
                                            # Count lead types
                                            new_leads = sum(1 for r in results if r.get('is_new'))
                                            high_priority = sum(1 for r in results if r.get('extracted_data', {}).get('urgency') == 'high')
                                            
                                            st.success(f"✅ Successfully processed {scanned} lead emails!")
                                            
                                            col_s1, col_s2, col_s3 = st.columns(3)
                                            with col_s1:
                                                st.metric("📊 New Leads", new_leads)
                                            with col_s2:
                                                st.metric("🔄 Updated Leads", scanned - new_leads)
                                            with col_s3:
                                                if high_priority > 0:
                                                    st.metric("🔥 High Priority", high_priority, delta_color="inverse")
                                            
                                            # Show lead types breakdown
                                            lead_types = {}
                                            for r in results:
                                                lead_type = r.get('extracted_data', {}).get('lead_type', 'unknown')
                                                lead_types[lead_type] = lead_types.get(lead_type, 0) + 1
                                            
                                            if lead_types:
                                                st.info(f"📋 Lead Types: {', '.join([f'{k.title()}: {v}' for k, v in lead_types.items()])}")
                                        else:
                                            st.info("📭 No lead emails found. Newsletters and automated emails were filtered out.")
                                        
                                        if errors:
                                            with st.expander("⚠️ View Errors"):
                                                for err in errors:
                                                    st.warning(f"Error: {err.get('error', 'Unknown')}")
                                        
                                        time.sleep(1)
                                        st.rerun()
                                    else:
                                        st.error("❌ Scan failed. Please check logs.")
                                        
                                except requests.exceptions.Timeout:
                                    st.error("⏱️ Scan timed out. Large inbox may take longer. Check logs in a moment.")
                                except requests.exceptions.RequestException as e:
                                    st.error(f"❌ Connection error: {str(e)}")
                                except Exception as e:
                                    st.error(f"❌ Unexpected error: {str(e)}")
                    
                    with col_btn2:
                        if st.button("📋 View Logs", key=f"logs_{account['id']}", 
                                   help="View scan history"):
                            st.session_state[f'show_logs_{account["id"]}'] = True
                    
                    with col_btn3:
                        if st.button("❌ Disconnect", key=f"disconnect_{account['id']}", 
                                   help="Remove email connection"):
                            if st.checkbox(f"✓ Confirm disconnection", 
                                         key=f"confirm_disconnect_{account['id']}"):
                                with st.spinner("Disconnecting..."):
                                    disconnect_resp = api_delete(f"email/disconnect/{account['id']}")
                                    
                                    if disconnect_resp and disconnect_resp.get('success'):
                                        st.success("✅ Email account disconnected!")
                                        time.sleep(1)
                                        st.rerun()
                                    else:
                                        st.error("❌ Failed to disconnect")
                    
                    # Show scan logs if requested
                    if st.session_state.get(f'show_logs_{account["id"]}'):
                        st.divider()
                        st.markdown("#### 📊 Recent Scan Logs")
                        
                        logs_resp = api_get(f"email/scan-logs/{st.session_state.company_id}?limit=10")
                        
                        if logs_resp and logs_resp.get('success') and logs_resp.get('data'):
                            for log in logs_resp['data']:
                                status_emoji = {
                                    'success': '✅',
                                    'skipped': '⏭️',
                                    'failed': '❌',
                                    'pending': '⏳'
                                }.get(log.get('status', 'pending'), '❓')
                                
                                with st.expander(f"{status_emoji} {log.get('from_email', 'Unknown')} - {log.get('subject', 'No subject')[:50]}"):
                                    col_log1, col_log2 = st.columns(2)
                                    
                                    with col_log1:
                                        st.write(f"**From:** {log.get('from_email', 'N/A')}")
                                        st.write(f"**Subject:** {log.get('subject', 'N/A')}")
                                        st.write(f"**Status:** {log.get('status', 'N/A')}")
                                    
                                    with col_log2:
                                        st.write(f"**Lead ID:** {log.get('lead_id', 'N/A')}")
                                        st.write(f"**Lead Name:** {log.get('lead_name', 'N/A')}")
                                        st.write(f"**Scanned:** {log.get('created_at', 'N/A')[:19]}")
                                    
                                    if log.get('extracted_data'):
                                        st.json(log['extracted_data'])
                                    
                                    if log.get('error_message'):
                                        st.error(f"Error: {log['error_message']}")
                        else:
                            st.info("No scan logs yet")
                        
                        if st.button("Hide Logs", key=f"hide_logs_{account['id']}"):
                            st.session_state[f'show_logs_{account["id"]}'] = False
                            st.rerun()
        else:
            st.info("No email accounts connected yet")
    else:
        st.warning("Unable to fetch email scanning status")
    
    # Connect new email accounts
    st.markdown("---")
    st.markdown("### 🔗 Connect New Email Account")
    
    col_connect1, col_connect2 = st.columns(2)
    
    # Gmail Connection
    with col_connect1:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border: 2px solid #4285F4;">
            <h4 style="color: #4285F4; margin: 0 0 10px 0;">📧 Gmail</h4>
            <p style="font-size: 14px; color: #666; margin: 0;">
                Connect your Gmail account to scan emails for leads automatically.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("")
        
        if st.button("🔗 Connect Gmail", use_container_width=True, 
                   type="primary", key="connect_gmail"):
            with st.spinner("🔄 Initializing Gmail OAuth..."):
                oauth_resp = api_get(
                    f"email/oauth/gmail/start?company_id={st.session_state.company_id}"
                )
                
                # UPDATED: Now correctly reads auth_url from top level OR data
                if oauth_resp and oauth_resp.get('success'):
                    auth_url = (
                        oauth_resp.get('auth_url') or 
                        oauth_resp.get('data', {}).get('auth_url')
                    )
                    
                    if not auth_url:
                        st.error("auth_url missing in API response")
                        st.json(oauth_resp)
                    else:
                        st.markdown(f"""
                        <div style="background: #e3f2fd; padding: 30px; border-radius: 15px; margin: 20px 0; text-align: center;">
                            <h3 style="color: #1976d2; margin-bottom: 20px;">Gmail OAuth Ready</h3>
                            <p style="color: #424242; margin-bottom: 25px; font-size: 16px;">
                                Click the button below to authorize Gmail access:
                            </p>
                            <a href="{auth_url}" target="_blank" style="
                                background: linear-gradient(135deg, #4285F4 0%, #34A853 100%);
                                color: white; 
                                padding: 18px 40px; 
                                border-radius: 10px; 
                                text-decoration: none; 
                                display: inline-block;
                                font-weight: bold;
                                font-size: 18px;
                                box-shadow: 0 4px 15px rgba(66, 133, 244, 0.4);
                            ">
                                Authorize Gmail
                            </a>
                            <p style="color: #666; margin-top: 20px; font-size: 14px;">
                                You'll be redirected to Google for secure authentication.<br>
                                After approval, your inbox will be scanned every 15 minutes.
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.error("Failed to initialize Gmail OAuth")
                    st.markdown("### Debug Response:")
                    st.json(oauth_resp)
                    st.error("**Possible causes:**")
                    st.markdown("""
                    - GMAIL_CLIENT_ID or GMAIL_CLIENT_SECRET not configured
                    - BASE_URL not set correctly
                    - Gmail OAuth app not created in Google Cloud Console
                    """)

    
    # Outlook Connection
    with col_connect2:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border: 2px solid #0078D4;">
            <h4 style="color: #0078D4; margin: 0 0 10px 0;">Outlook</h4>
            <p style="font-size: 14px; color: #666; margin: 0;">
                Connect your Outlook/Microsoft 365 account to scan emails for leads.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("")
        
        if st.button("Connect Outlook", use_container_width=True, 
                   type="primary", key="connect_outlook"):
            with st.spinner("Initializing Outlook OAuth..."):
                oauth_resp = api_get(
                    f"email/oauth/outlook/start?company_id={st.session_state.company_id}"
                )
                
                # UPDATED: Unified auth_url extraction (same as Gmail)
                if oauth_resp and oauth_resp.get('success'):
                    auth_url = (
                        oauth_resp.get('auth_url') or 
                        oauth_resp.get('data', {}).get('auth_url')
                    )
                    
                    if not auth_url:
                        st.error("auth_url missing in API response")
                        st.json(oauth_resp)
                    else:
                        st.markdown(f"""
                        <div style="background: #e3f2fd; padding: 30px; border-radius: 15px; margin: 20px 0; text-align: center;">
                            <h3 style="color: #1976d2; margin-bottom: 20px;">Outlook OAuth Ready</h3>
                            <p style="color: #424242; margin-bottom: 25px; font-size: 16px;">
                                Click the button below to authorize Outlook access:
                            </p>
                            <a href="{auth_url}" target="_blank" style="
                                background: linear-gradient(135deg, #0078D4 0%, #106EBE 100%);
                                color: white; 
                                padding: 18px 40px; 
                                border-radius: 10px; 
                                text-decoration: none; 
                                display: inline-block;
                                font-weight: bold;
                                font-size: 18px;
                                box-shadow: 0 4px 15px rgba(0, 120, 212, 0.4);
                            ">
                                Authorize Outlook
                            </a>
                            <p style="color: #666; margin-top: 20px; font-size: 14px;">
                                You'll be redirected to Microsoft for secure authentication.<br>
                                After approval, your inbox will be scanned every 15 minutes.
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.error("Failed to initialize Outlook OAuth")
                    st.error("**Possible causes:**")
                    st.markdown("""
                    - OUTLOOK_CLIENT_ID or OUTLOOK_CLIENT_SECRET not configured
                    - BASE_URL not set correctly
                    - Outlook OAuth app not created in Azure Portal
                    """)
    
    # How it works section
    st.markdown("---")
    st.markdown("### ℹ️ How Email Scanning Works")
    
    with st.expander("📖 Click to learn more"):
        st.markdown("""
        #### 🔄 Automatic Process
        
        1. **OAuth Connection**: You securely connect your Gmail or Outlook account
        2. **Scheduled Scanning**: System scans your inbox every 15 minutes
        3. **AI Extraction**: Groq AI analyzes emails to extract:
           - Name
           - Phone number
           - Email address
           - Company name
           - Interest/intent
           - Urgency level
        4. **Lead Creation**: Valid leads are automatically created in your CRM
        5. **Auto-Follow-up**: Welcome messages sent via WhatsApp (if configured)
        
        #### 🔒 Security & Privacy
        
        - ✅ All OAuth tokens are **AES-256 encrypted** in database
        - ✅ We only read emails, never send or modify
        - ✅ You can disconnect anytime
        - ✅ Data is isolated per company (multi-tenant)
        
        #### 🎯 AI Rules Configuration
        
        By default, the AI looks for:
        - **Keywords**: "interested", "inquiry", "quote", "demo"
        - **Priority Keywords**: "urgent", "asap", "immediately"
        - **Exclude Keywords**: "unsubscribe", "newsletter", "spam"
        
        Contact support to customize these rules for your business!
        
        #### 📊 What Gets Scanned
        
        - **Gmail**: INBOX folder, unread emails
        - **Outlook**: Inbox folder, unread emails
        - **Frequency**: Every 15 minutes (configurable)
        - **Limits**: Last 10 unread emails per scan
        
        #### 🚀 Benefits
        
        - ⚡ **Never miss a lead** - Automatic 24/7 scanning
        - 🤖 **AI-powered extraction** - 95%+ accuracy
        - ⏱️ **Save time** - No manual data entry
        - 📈 **Faster response** - Instant lead creation
        - 🔗 **Multi-channel** - Email → CRM → WhatsApp → Calls
        """)
    
    # Statistics Section
    st.markdown("---")
    st.markdown("### 📊 Email Scanning Statistics")
    
    # Fetch overall stats
    logs_resp = api_get(f"email/scan-logs/{st.session_state.company_id}?limit=1000")
    
    if logs_resp and logs_resp.get('success') and logs_resp.get('data'):
        logs = logs_resp['data']
        
        total_scanned = len(logs)
        successful = sum(1 for log in logs if log.get('status') == 'success')
        skipped = sum(1 for log in logs if log.get('status') == 'skipped')
        failed = sum(1 for log in logs if log.get('status') == 'failed')
        
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        
        with col_stat1:
            st.metric("📨 Total Scanned", total_scanned)
        
        with col_stat2:
            st.metric("✅ Leads Created", successful)
        
        with col_stat3:
            st.metric("⏭️ Skipped", skipped)
        
        with col_stat4:
            st.metric("❌ Failed", failed)
        
        # Success rate
        if total_scanned > 0:
            success_rate = (successful / total_scanned) * 100
            st.progress(success_rate / 100)
            st.caption(f"Success Rate: {success_rate:.1f}%")
        
        # Show recent activity
        st.divider()
        st.markdown("#### 🕐 Recent Activity (Last 5)")
        
        recent_logs = logs[:5]
        for log in recent_logs:
            status_emoji = {
                'success': '✅',
                'skipped': '⏭️',
                'failed': '❌'
            }.get(log.get('status', 'pending'), '❓')
            
            col_r1, col_r2, col_r3 = st.columns([2, 3, 1])
            
            with col_r1:
                st.write(f"{status_emoji} **{log.get('status', 'N/A').upper()}**")
            
            with col_r2:
                st.write(f"{log.get('from_email', 'Unknown')}")
            
            with col_r3:
                st.caption(log.get('created_at', 'N/A')[:19])
    else:
        st.info("No scanning activity yet. Connect an email account to get started!")






# ==================== PAGE: AI AGENTS ====================
def page_agents():
    st.title("🤖 AI Agent Management")
    
    tab1, tab2 = st.tabs(["My Agents", "Create New Agent"])
    
    # with tab1:
    #     agents_resp = api_get(f"agent-instances/company/{st.session_state.company_id}")
        
    #     if not agents_resp or not agents_resp.get('success'):
    #         st.info("No agents configured yet")
    #     else:
    #         for agent in agents_resp['data']:
    #             with st.expander(f"🤖 {agent['agent_name']} ({agent['agent_type']})"):
    #                 col1, col2 = st.columns(2)
                    
    #                 with col1:
    #                     st.write(f"**ID:** {agent['id']}")
    #                     st.write(f"**Type:** {agent['agent_type']}")
    #                     st.write(f"**Phone:** {agent.get('phone_number', 'N/A')}")
    #                     st.write(f"**WhatsApp:** {agent.get('whatsapp_number', 'N/A')}")
    #                     st.write(f"**Status:** {'🟢 Active' if agent['is_active'] else '🔴 Inactive'}")
                    
    #                 with col2:
    #                     st.write(f"**Created:** {agent['created_at'][:10]}")
    #                     st.write(f"**Voice:** {agent.get('custom_voice', agent.get('default_voice', 'N/A'))}")
    #                     st.write(f"**Model:** {agent.get('model_name', 'N/A')}")
                    
    #                 # Agent performance stats
    #                 stats_resp = api_get(f"agent-instances/{agent['id']}/stats")
    #                 if stats_resp and stats_resp.get('success'):
    #                     stats = stats_resp['data']
    #                     st.markdown("### 📊 Performance (30 days)")
    #                     col_s1, col_s2, col_s3 = st.columns(3)
    #                     with col_s1:
    #                         st.metric("Total Calls", stats.get('total_calls', 0))
    #                     with col_s2:
    #                         st.metric("Completed Calls", stats.get('completed_calls', 0))
    #                     with col_s3:
    #                         st.metric("Total Messages", stats.get('total_messages', 0))
                    
    #                 if agent.get('custom_prompt'):
    #                     with st.expander("View Custom Prompt"):
    #                         st.text_area("Prompt", value=agent['custom_prompt'], height=200, key=f"prompt_{agent['id']}")
                    
    #                 # WhatsApp Credentials Setup
    #                 if agent['agent_type'] == 'whatsapp':
    #                     st.divider()
    #                     st.markdown("### 🔧 WhatsApp Setup")
                        
    #                     if agent.get('whatsapp_credentials'):
    #                         st.success("✅ WhatsApp credentials configured")
    #                         st.info(f"**Webhook URL:** {API_BASE_URL.replace('/api', '')}/api/webhooks/whatsapp-universal")
    #                         if agent.get('webhook_verify_token'):
    #                             st.info(f"**Verify Token:** {agent['webhook_verify_token']}")
    #                     else:
    #                         st.warning("⚠️ WhatsApp credentials not configured")
                            
    #                         with st.form(f"whatsapp_creds_{agent['id']}"):
    #                             st.markdown("**Meta WhatsApp Business API Credentials:**")
    #                             access_token = st.text_input("Access Token*", type="password")
    #                             phone_number_id = st.text_input("Phone Number ID*")
    #                             business_account_id = st.text_input("Business Account ID")
                                
    #                             if st.form_submit_button("Save Credentials"):
    #                                 creds_data = {
    #                                     "access_token": access_token,
    #                                     "phone_number_id": phone_number_id,
    #                                     "business_account_id": business_account_id
    #                                 }
                                    
    #                                 result = api_post(f"agent-instances/{agent['id']}/whatsapp-credentials", creds_data)
                                    
    #                                 if result and result.get('success'):
    #                                     st.success("✅ Credentials saved!")
    #                                     st.info(f"**Webhook URL:** {result.get('webhook_url')}")
    #                                     st.info(f"**Verify Token:** {result.get('verify_token')}")
    #                                     st.rerun()
    #                                 else:
    #                                     st.error("Failed to save credentials")
                    
    #                 # Delete agent
    #                 st.divider()
    #                 if st.button(f"🗑️ Delete Agent", key=f"delete_{agent['id']}"):
    #                     if st.checkbox(f"Confirm deletion of {agent['agent_name']}", key=f"confirm_{agent['id']}"):
    #                         result = api_delete(f"agent-instances/{agent['id']}")
    #                         if result and result.get('success'):
    #                             st.success("Agent deleted!")
    #                             st.rerun()



    with tab1:
        agents_resp = api_get(f"agent-instances/company/{st.session_state.company_id}")
        
        if not agents_resp or not agents_resp.get('success'):
            st.info("No agents configured yet")
        else:
            for agent in agents_resp['data']:
                with st.expander(f"🤖 {agent['agent_name']} ({agent['agent_type']})"):
                    # Basic Info
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**ID:** {agent['id']}")
                        st.write(f"**Type:** {agent['agent_type']}")
                        st.write(f"**Phone:** {agent.get('phone_number', 'N/A')}")
                        st.write(f"**WhatsApp:** {agent.get('whatsapp_number', 'N/A')}")
                        st.write(f"**Status:** {'🟢 Active' if agent['is_active'] else '🔴 Inactive'}")
                    
                    with col2:
                        st.write(f"**Created:** {agent['created_at'][:10]}")
                        st.write(f"**Voice:** {agent.get('custom_voice', agent.get('default_voice', 'N/A'))}")
                        st.write(f"**Model:** {agent.get('model_name', 'N/A')}")
                    
                    # ✅ FIXED: WhatsApp Setup with proper OAuth
                    if agent['agent_type'] == 'whatsapp':
                        render_whatsapp_oauth_setup(agent)

                    if agent['agent_type'] == 'voice':
                        # Provider selection
                        col_provider1, col_provider2 = st.columns(2)
                        
                        with col_provider1:
                            provider_choice = st.radio(
                                "Select Provider",
                                ["Twilio OAuth", "Airtel SIP"],
                                key=f"provider_{agent['id']}"
                            )
                        
                        if provider_choice == "Twilio OAuth":
                            render_twilio_oauth_setup(agent)
                        else:
                            render_airtel_sip_setup(agent)
                    
                    # Agent Performance Stats
                    stats_resp = api_get(f"agent-instances/{agent['id']}/stats")
                    if stats_resp and stats_resp.get('success'):
                        stats = stats_resp['data']
                        st.markdown("### 📊 Performance (30 days)")
                        col_s1, col_s2, col_s3 = st.columns(3)
                        with col_s1:
                            st.metric("Total Calls", stats.get('total_calls', 0))
                        with col_s2:
                            st.metric("Completed Calls", stats.get('completed_calls', 0))
                        with col_s3:
                            st.metric("Total Messages", stats.get('total_messages', 0))
                    
                    # Custom Prompt
                    if agent.get('custom_prompt'):
                        with st.expander("View Custom Prompt"):
                            st.text_area("Prompt", value=agent['custom_prompt'], 
                                       height=200, key=f"prompt_{agent['id']}", disabled=True)
                    
                    # Delete Agent
                    st.divider()
                    if st.button(f"🗑️ Delete Agent", key=f"delete_{agent['id']}", type="secondary"):
                        if st.checkbox(f"Confirm deletion of {agent['agent_name']}", 
                                     key=f"confirm_{agent['id']}"):
                            with st.spinner("Deleting..."):
                                result = api_delete(f"agent-instances/{agent['id']}")
                                if result and result.get('success'):
                                    st.success("Agent deleted!")
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.error("Failed to delete agent")
    
    with tab2:
        st.subheader("Create New AI Agent")
        
        with st.form("create_agent"):
            agent_name = st.text_input("Agent Name*", placeholder="Chess Coach AI")
            agent_type = st.selectbox("Type*", ["voice", "whatsapp"])
            
            col1, col2 = st.columns(2)
            
            with col1:
                if agent_type == "voice":
                    phone_number = st.text_input("Phone Number", placeholder="+919876543210")
                else:
                    phone_number = None
            
            with col2:
                if agent_type == "whatsapp":
                    whatsapp_number = st.text_input("WhatsApp Number", placeholder="+919876543210")
                else:
                    whatsapp_number = None
            
            custom_prompt = st.text_area("Custom Prompt (optional)", height=200,
                placeholder="You are Priya from 4champz...")
            
            voice = st.selectbox("Voice", ["Raveena", "Aditi", "Brian", "Matthew"])
            
            submitted = st.form_submit_button("Create Agent")
            
            if submitted:
                if not agent_name:
                    st.error("Agent name is required!")
                    return
                
                data = {
                    "company_id": st.session_state.company_id,
                    "agent_name": agent_name,
                    "agent_type": agent_type,
                    "phone_number": phone_number if agent_type == "voice" else None,
                    "whatsapp_number": whatsapp_number if agent_type == "whatsapp" else None,
                    "custom_prompt": custom_prompt if custom_prompt else None,
                    "custom_voice": voice
                }
                
                result = api_post("agent-instances", data)
                if result and result.get('success'):
                    st.success(f"✅ Agent created! ID: {result['data']['id']}")
                    if agent_type == "whatsapp":
                        st.info("⚠️ Don't forget to configure WhatsApp credentials in the agent settings!")
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("Failed to create agent")

# ==================== PAGE: CALLING ====================
def page_calling():
    st.title("📞 AI Calling System")
    
    tab1, tab2 = st.tabs(["Make Call", "Call Logs"])
    
    with tab1:
        st.subheader("🚀 Initiate Outbound Call")
        
        # Check if coming from lead detail
        if 'selected_lead_for_call' in st.session_state:
            lead = st.session_state.selected_lead_for_call
            st.info(f"Calling: {lead.get('name', 'Unknown')} ({lead['phone_number']})")
            default_lead_id = lead['id']
            default_phone = lead['phone_number']
            default_name = lead.get('name', '')
        else:
            default_lead_id = 1
            default_phone = ""
            default_name = ""
        
        with st.form("make_call"):
            col1, col2 = st.columns(2)
            
            with col1:
                lead_id = st.number_input("Lead ID*", min_value=1, value=default_lead_id)
                to_phone = st.text_input("Phone Number*", value=default_phone, placeholder="+919876543210")
                name = st.text_input("Name", value=default_name, placeholder="Ajsal")
            
            with col2:
                call_type = st.selectbox("Call Type", ["qualification", "reminder", "payment", "support"])
                
                # Get agents for this company
                agents_resp = api_get(f"agent-instances/company/{st.session_state.company_id}?agent_type=voice")
                agent_options = {}
                if agents_resp and agents_resp.get('success'):
                    agent_options = {f"{a['agent_name']} ({a['id']})": a['id'] for a in agents_resp['data']}
                
                if agent_options:
                    agent_select = st.selectbox("Select Agent", ["Default"] + list(agent_options.keys()))
                    agent_instance_id = agent_options.get(agent_select, None)
                else:
                    st.warning("No voice agents configured")
                    agent_instance_id = None
            
            submitted = st.form_submit_button("📞 Make Call Now")
            
            if submitted:
                if not to_phone:
                    st.error("Phone number is required!")
                    return
                
                data = {
                    "company_id": st.session_state.company_id,
                    "lead_id": lead_id,
                    "to_phone": to_phone,
                    "name": name,
                    "call_type": call_type
                }
                
                if agent_instance_id:
                    result = python_api_post(f"outbound-call-agent?agent_instance_id={agent_instance_id}", data)
                else:
                    result = python_api_post("outbound-call", data)
                
                if result and result.get('success'):
                    st.success(f"✅ Call initiated! SID: {result.get('call_sid')}")
                    # Clear selected lead
                    if 'selected_lead_for_call' in st.session_state:
                        del st.session_state.selected_lead_for_call
                else:
                    st.error("Failed to initiate call")
    
    with tab2:
        st.subheader("📋 Recent Call Logs")
        
        calls_resp = api_get(f"call-logs?company_id={st.session_state.company_id}&limit=50")
        
        if calls_resp and calls_resp.get('success'):
            df = pd.DataFrame(calls_resp['data'])
            if not df.empty:
                df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
                
                for idx, row in df.iterrows():
                    with st.expander(f"📞 {row['to_phone']} - {row['call_status']} - {row['created_at']}"):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.write(f"**Duration:** {row.get('call_duration', 0)}s")
                            st.write(f"**Type:** {row.get('call_type', 'N/A')}")
                        with col2:
                            st.write(f"**Status:** {row['call_status']}")
                            st.write(f"**Call SID:** {row['call_sid'][:20]}...")
                        with col3:
                            if row.get('recording_url'):
                                st.markdown(f"[🎵 Recording]({row['recording_url']})")
                        
                        if row.get('transcript'):
                            st.text_area("Transcript", row['transcript'], height=150, key=f"transcript_{idx}")





def page_calendar():
    """
    Calendar Integration Management Page
    """
    st.title("📅 Calendar Integration")
    
    tab1, tab2, tab3 = st.tabs(["Calendar Status", "Create Event", "Upcoming Events"])
    
    # Tab 1: Calendar Status & OAuth Setup
    with tab1:
        st.subheader("📊 Connected Calendars")
        
        status_resp = api_get(f"calendar/status/{st.session_state.company_id}")
        
        if status_resp and status_resp.get('success'):
            calendars = status_resp['data']
            
            if calendars:
                for cal in calendars:
                    with st.expander(f"📧 {cal['user_email']} ({cal['provider'].upper()})"):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            status_icon = "🟢" if cal['is_active'] else "🔴"
                            st.metric("Status", f"{status_icon} {'Active' if cal['is_active'] else 'Inactive'}")
                        
                        with col2:
                            st.metric("📅 Calendar ID", cal.get('calendar_id', 'primary'))
                        
                        with col3:
                            days_left = cal.get('days_until_expiry')
                            if days_left is not None:
                                # FIX: Convert to float
                                try:
                                    days_left = float(days_left)
                                except (ValueError, TypeError):
                                    days_left = None

                                if days_left < 7:
                                    st.metric("Token Expires", f"{days_left:.1f} days", delta_color="inverse")
                                else:
                                    st.metric("Token Valid", f"{days_left:.1f} days")
                            else:
                                st.metric("Status", "Active")
                        
                        st.info(f"🌐 **Timezone:** {cal.get('calendar_timezone', 'Asia/Kolkata')}")
                        
                        # Reconnect/Disconnect buttons
                        col_btn1, col_btn2 = st.columns(2)
                        
                        with col_btn1:
                            needs_reauth = cal.get('needs_reauth', False) or (days_left is not None and days_left < 7)
                            
                            if needs_reauth:
                                st.warning("⚠️ **Re-authentication Required**")
                            
                            if st.button("🔄 Reconnect Calendar", key=f"reconnect_{cal['id']}"):
                                with st.spinner("Initializing OAuth..."):
                                    oauth_resp = api_get(
                                        f"calendar/oauth/google/start?"
                                        f"company_id={st.session_state.company_id}&"
                                        f"user_email={cal['user_email']}"
                                    )
                                    
                                    if oauth_resp and oauth_resp.get('success'):
                                        auth_url = oauth_resp.get('auth_url')
                                        
                                        st.markdown(f"""
                                        <div style="background: #e3f2fd; padding: 30px; border-radius: 15px; margin: 20px 0; text-align: center;">
                                            <h3 style="color: #1976d2; margin-bottom: 20px;">🔐 Google Calendar OAuth Ready</h3>
                                            <p style="color: #424242; margin-bottom: 25px; font-size: 16px;">
                                                Click the button below to reconnect your calendar:
                                            </p>
                                            <a href="{auth_url}" target="_blank" style="
                                                background: linear-gradient(135deg, #4285F4 0%, #34A853 100%);
                                                color: white; 
                                                padding: 18px 40px; 
                                                border-radius: 10px; 
                                                text-decoration: none; 
                                                display: inline-block;
                                                font-weight: bold;
                                                font-size: 18px;
                                                box-shadow: 0 4px 15px rgba(66, 133, 244, 0.4);
                                            ">
                                                🚀 Authorize Google Calendar
                                            </a>
                                        </div>
                                        """, unsafe_allow_html=True)
                                    else:
                                        st.error("❌ Failed to initialize OAuth")
                        
                        with col_btn2:
                            if st.button("❌ Disconnect", key=f"disconnect_{cal['id']}"):
                                if st.checkbox(f"✓ Confirm disconnection", key=f"confirm_disconnect_{cal['id']}"):
                                    disconnect_resp = api_delete(f"calendar/disconnect/{cal['id']}")
                                    
                                    if disconnect_resp and disconnect_resp.get('success'):
                                        st.success("✅ Calendar disconnected!")
                                        time.sleep(1)
                                        st.rerun()
                                    else:
                                        st.error("❌ Failed to disconnect")
            else:
                st.info("No calendars connected yet")
        else:
            st.warning("Unable to fetch calendar status")
        
        st.markdown("---")
        st.markdown("### 🔗 Connect New Calendar")
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 20px; border-radius: 10px; margin: 20px 0;">
            <h3 style="margin: 0 0 10px 0;">🚀 Sync Your Google Calendar</h3>
            <p style="margin: 0; font-size: 14px;">
                Automatically create calendar events for bookings and meetings.<br>
                ✅ Google Meet links auto-generated<br>
                ✅ Automatic reminders<br>
                ✅ Prevent double-bookings
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("connect_calendar"):
            user_email = st.text_input(
                "Your Email*",
                placeholder="user@example.com",
                help="The Google account email to connect"
            )
            
            submitted = st.form_submit_button("🔗 Connect Google Calendar", use_container_width=True, type="primary")
            
            if submitted:
                if not user_email:
                    st.error("Email is required!")
                else:
                    with st.spinner("🔄 Initializing Google OAuth..."):
                        oauth_resp = api_get(
                            f"calendar/oauth/google/start?"
                            f"company_id={st.session_state.company_id}&"
                            f"user_email={user_email}"
                        )
                        
                        if oauth_resp and oauth_resp.get('success'):
                            auth_url = oauth_resp.get('auth_url')
                            
                            st.markdown(f"""
                            <div style="background: #e3f2fd; padding: 30px; border-radius: 15px; margin: 20px 0; text-align: center;">
                                <h3 style="color: #1976d2; margin-bottom: 20px;">🔐 Google Calendar OAuth Ready</h3>
                                <p style="color: #424242; margin-bottom: 25px; font-size: 16px;">
                                    Click the button below to authorize Google Calendar access:
                                </p>
                                <a href="{auth_url}" target="_blank" style="
                                    background: linear-gradient(135deg, #4285F4 0%, #34A853 100%);
                                    color: white; 
                                    padding: 18px 40px; 
                                    border-radius: 10px; 
                                    text-decoration: none; 
                                    display: inline-block;
                                    font-weight: bold;
                                    font-size: 18px;
                                    box-shadow: 0 4px 15px rgba(66, 133, 244, 0.4);
                                ">
                                    🚀 Authorize Google Calendar
                                </a>
                                <p style="color: #666; margin-top: 20px; font-size: 14px;">
                                    You'll be redirected to Google for secure authentication.<br>
                                    After approval, your calendar will be ready to use!
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.error("❌ Failed to initialize OAuth")
                            st.error("**Possible causes:**")
                            st.markdown("""
                            - GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET not configured
                            - BASE_URL not set correctly
                            - Google OAuth app not created in Google Cloud Console
                            """)
    
    # Tab 2: Create Calendar Event
    with tab2:
        st.subheader("➕ Create Calendar Event")
        
        # Get connected calendars
        status_resp = api_get(f"calendar/status/{st.session_state.company_id}")
        
        if not status_resp or not status_resp.get('success') or not status_resp['data']:
            st.warning("⚠️ No calendars connected. Please connect a calendar in the 'Calendar Status' tab first.")
            return
        
        calendars = status_resp['data']
        active_calendars = [c for c in calendars if c['is_active']]
        
        if not active_calendars:
            st.warning("⚠️ No active calendars found. Please reconnect your calendar.")
            return
        
        # Calendar selection
        cal_options = {f"{c['user_email']} ({c['provider']})": c['id'] for c in active_calendars}
        
        with st.form("create_calendar_event"):
            selected_cal = st.selectbox("Select Calendar", list(cal_options.keys()))
            calendar_config_id = cal_options[selected_cal]
            
            st.markdown("### 📋 Event Details")
            
            col1, col2 = st.columns(2)
            
            with col1:
                title = st.text_input("Event Title*", placeholder="Demo Session - Chess Coaching")
                
                # Lead selection (optional)
                leads_resp = api_get(f"leads?company_id={st.session_state.company_id}&limit=100")
                lead_options = {"None": None}
                if leads_resp and leads_resp.get('success'):
                    lead_options.update({
                        f"{l['name']} ({l['phone_number']})": l['id'] 
                        for l in leads_resp['data']
                    })
                
                selected_lead = st.selectbox("Link to Lead (Optional)", list(lead_options.keys()))
                lead_id = lead_options[selected_lead]
            
            with col2:
                duration = st.number_input("Duration (minutes)", min_value=15, max_value=480, value=60, step=15)
                
                attendee_emails = st.text_area(
                    "Attendee Emails (one per line)",
                    placeholder="attendee1@example.com\nattendee2@example.com",
                    height=100
                )
            
            description = st.text_area(
                "Description",
                placeholder="Meeting agenda, notes, etc.",
                height=100
            )
            
            st.markdown("### 🕐 Schedule")
            
            col3, col4 = st.columns(2)
            
            with col3:
                event_date = st.date_input("Date", value=datetime.now() + timedelta(days=1))
            
            with col4:
                event_time = st.time_input("Time", value=datetime.now().replace(hour=10, minute=0).time())
            
            submitted = st.form_submit_button("📅 Create Event", use_container_width=True, type="primary")
            
            if submitted:
                if not title:
                    st.error("Event title is required!")
                    return
                
                # Calculate start and end times
                start_datetime = datetime.combine(event_date, event_time)
                end_datetime = start_datetime + timedelta(minutes=duration)
                
                # Parse attendees
                attendees = []
                if attendee_emails:
                    attendees = [email.strip() for email in attendee_emails.split('\n') if email.strip()]
                
                # Create event
                event_data = {
                    "calendar_config_id": calendar_config_id,
                    "lead_id": lead_id,
                    "title": title,
                    "description": description,
                    "start_time": start_datetime.isoformat(),
                    "end_time": end_datetime.isoformat(),
                    "attendees": attendees
                }
                
                with st.spinner("Creating calendar event..."):
                    result = api_post("calendar/create-event", event_data)
                    
                    if result and result.get('success'):
                        event_info = result['data']
                        
                        st.success("✅ Calendar event created successfully!")
                        
                        col_success1, col_success2 = st.columns(2)
                        
                        with col_success1:
                            st.info(f"**Event ID:** {event_info.get('event_id')}")
                        
                        with col_success2:
                            if event_info.get('meeting_link'):
                                st.markdown(f"**📹 [Join Google Meet]({event_info['meeting_link']})**")
                        
                        if event_info.get('calendar_link'):
                            st.markdown(f"[📅 View in Google Calendar]({event_info['calendar_link']})")
                        
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error("❌ Failed to create calendar event")
                        if result:
                            st.error(f"Error: {result.get('error', 'Unknown error')}")
    
    # Tab 3: Upcoming Events
    with tab3:
        st.subheader("📆 Upcoming Events")
        
        # This would require a new API endpoint to fetch calendar events
        # For now, show placeholder
        st.info("📌 **Feature:** View and manage upcoming calendar events")
        st.markdown("""
        **Coming Soon:**
        - View all scheduled events
        - Edit/cancel events
        - Send reminders
        - Sync status updates
        """)
        
        # Placeholder for future implementation
        with st.expander("📋 Sample Event"):
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Title:** Demo Session")
                st.write("**Lead:** John Doe")
                st.write("**Date:** 2025-11-16 10:00 AM")
            with col2:
                st.write("**Duration:** 60 mins")
                st.write("**Attendees:** 2")
                st.markdown("[📹 Join Meet](#)")




def check_calendar_availability(calendar_config_id: int, start_time: str, end_time: str) -> Optional[Dict]:
    """
    Check if a time slot is available in the calendar
    
    Args:
        calendar_config_id: Calendar configuration ID
        start_time: ISO format datetime string
        end_time: ISO format datetime string
    
    Returns:
        Dict with availability status or None if error
    """
    try:
        data = {
            "calendar_config_id": calendar_config_id,
            "start_time": start_time,
            "end_time": end_time
        }
        
        response = api_post("calendar/check-availability", data)
        
        if response and response.get('success'):
            return response['data']
        else:
            st.error("Failed to check availability")
            return None
    except Exception as e:
        st.error(f"Error checking availability: {str(e)}")
        return None




# ==================== PAGE: SCHEDULED CALLS ====================
def page_scheduled_calls():
    st.title("📅 Scheduled Calls Management")
    
    tab1, tab2 = st.tabs(["View Scheduled", "Schedule New Call"])
    
    with tab1:
        st.subheader("Upcoming Scheduled Calls")
        
        # Get scheduled calls
        scheduled_resp = api_get(f"scheduled-calls/pending")
        
        if not scheduled_resp or not scheduled_resp.get('success'):
            st.info("No scheduled calls found")
        else:
            calls = scheduled_resp['data']
            
            if not calls:
                st.info("No pending scheduled calls")
            else:
                for call in calls:
                    with st.expander(f"📞 {call.get('name', 'Unknown')} - {call['scheduled_time'][:19]}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Lead ID:** {call['lead_id']}")
                            st.write(f"**Phone:** {call['phone_number']}")
                            st.write(f"**Type:** {call['call_type']}")
                            st.write(f"**Status:** {call['status']}")
                        
                        with col2:
                            st.write(f"**Scheduled:** {call['scheduled_time'][:19]}")
                            st.write(f"**Created:** {call.get('created_at', 'N/A')[:19]}")
                            st.write(f"**Retry Count:** {call.get('retry_count', 0)}")
                        
                        # Edit options
                        st.divider()
                        col_edit1, col_edit2, col_edit3 = st.columns(3)
                        
                        with col_edit1:
                            # Reschedule
                            with st.form(f"reschedule_{call['id']}"):
                                new_time = st.datetime_input("New Time", value=datetime.now() + timedelta(hours=1))
                                
                                if st.form_submit_button("Reschedule"):
                                    update_data = {
                                        "scheduled_time": new_time.isoformat(),
                                        "status": "pending"
                                    }
                                    result = api_patch(f"scheduled-calls/{call['id']}", update_data)
                                    if result and result.get('success'):
                                        st.success("Call rescheduled!")
                                        st.rerun()
                        
                        with col_edit2:
                            # Cancel
                            if st.button(f"❌ Cancel", key=f"cancel_{call['id']}"):
                                result = api_patch(f"scheduled-calls/{call['id']}", {"status": "cancelled"})
                                if result and result.get('success'):
                                    st.success("Call cancelled!")
                                    st.rerun()
                        
                        with col_edit3:
                            # Call Now
                            if st.button(f"📞 Call Now", key=f"now_{call['id']}"):
                                data = {
                                    "company_id": st.session_state.company_id,
                                    "lead_id": call['lead_id'],
                                    "to_phone": call['phone_number'],
                                    "name": call.get('name', ''),
                                    "call_type": call['call_type']
                                }
                                
                                result = python_api_post("outbound-call", data)
                                if result and result.get('success'):
                                    # Update scheduled call status
                                    api_patch(f"scheduled-calls/{call['id']}", {
                                        "status": "called",
                                        "call_sid": result.get('call_sid')
                                    })
                                    st.success("Call initiated!")
                                    st.rerun()
    
    with tab2:
        st.subheader("Schedule a New Call")
        
        # Check if coming from lead detail
        if 'selected_lead_for_schedule' in st.session_state:
            lead = st.session_state.selected_lead_for_schedule
            st.info(f"Scheduling for: {lead.get('name', 'Unknown')} ({lead['phone_number']})")
            default_lead_id = lead['id']
        else:
            default_lead_id = 1
        
        with st.form("schedule_call_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                lead_id = st.number_input("Lead ID*", min_value=1, value=default_lead_id)
                call_type = st.selectbox("Call Type", ["qualification", "reminder", "payment", "follow_up"])
            
            with col2:
                scheduled_date = st.date_input("Date", value=datetime.now() + timedelta(days=1))
                scheduled_time = st.time_input("Time", value=datetime.now().time())
            
            notes = st.text_area("Notes (optional)", placeholder="Any specific instructions...")
            
            submitted = st.form_submit_button("📅 Schedule Call")
            
            if submitted:
                scheduled_datetime = datetime.combine(scheduled_date, scheduled_time).isoformat()
                
                data = {
                    "company_id": st.session_state.company_id,
                    "lead_id": lead_id,
                    "call_type": call_type,
                    "scheduled_time": scheduled_datetime
                }
                
                result = api_post("schedule-call", data)
                
                if result and result.get('success'):
                    st.success(f"✅ Call scheduled for {scheduled_datetime}")
                    if 'selected_lead_for_schedule' in st.session_state:
                        del st.session_state.selected_lead_for_schedule
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Failed to schedule call")

# ==================== PAGE: WHATSAPP ====================
def page_whatsapp():
    st.title("💬 WhatsApp Management")
    
    tab1, tab2, tab3 = st.tabs(["Send Message", "Conversations", "Setup"])
    
    with tab1:
        st.subheader("📤 Send WhatsApp Message")
        
        # Get WhatsApp agents
        agents_resp = api_get(f"agent-instances/company/{st.session_state.company_id}?agent_type=whatsapp")
        
        if not agents_resp or not agents_resp.get('success') or not agents_resp['data']:
            st.warning("⚠️ No WhatsApp agents configured. Please setup in 'AI Agents' page.")
            return
        
        agent_options = {f"{a['agent_name']} ({a['whatsapp_number']})": a['id'] for a in agents_resp['data']}
        
        # Check if coming from lead detail
        if 'selected_lead_for_whatsapp' in st.session_state:
            lead = st.session_state.selected_lead_for_whatsapp
            st.info(f"Sending to: {lead.get('name', 'Unknown')} ({lead['phone_number']})")
            default_phone = lead['phone_number']
            default_lead_id = lead['id']
        else:
            default_phone = ""
            default_lead_id = None
        
        # Single message
        with st.form("send_whatsapp"):
            agent_select = st.selectbox("From Agent", list(agent_options.keys()))
            agent_id = agent_options[agent_select]
            
            to_phone = st.text_input("To Phone*", value=default_phone, placeholder="+919876543210")
            message = st.text_area("Message*", height=150)
            
            submitted = st.form_submit_button("Send Single Message")
            
            if submitted:
                if not to_phone or not message:
                    st.error("Phone and message are required!")
                    return
                
                result = api_post("whatsapp/send-manual", {
                    "to": to_phone,
                    "message": message,
                    "agent_instance_id": agent_id,
                    "lead_id": default_lead_id
                })
                
                if result and result.get('success'):
                    st.success("✅ Message sent!")
                    if 'selected_lead_for_whatsapp' in st.session_state:
                        del st.session_state.selected_lead_for_whatsapp
                else:
                    st.error("Failed to send message")
        
        # Bulk message
        st.divider()
        st.subheader("📤 Send Bulk Messages")
        
        with st.form("send_bulk_whatsapp"):
            agent_select_bulk = st.selectbox("From Agent (Bulk)", list(agent_options.keys()), key="bulk_agent")
            agent_id_bulk = agent_options[agent_select_bulk]
            
            # Get leads for bulk selection
            leads_resp = api_get(f"leads?company_id={st.session_state.company_id}&limit=100")
            lead_options = {}
            if leads_resp and leads_resp.get('success'):
                lead_options = {f"{l['name']} ({l['phone_number']})": l['phone_number'] for l in leads_resp['data']}
            
            selected_leads = st.multiselect("Select Leads for Bulk Message", list(lead_options.keys()))
            bulk_message = st.text_area("Bulk Message*", height=150, key="bulk_msg")
            
            submitted_bulk = st.form_submit_button("Send Bulk Messages")
            
            if submitted_bulk:
                if not selected_leads or not bulk_message:
                    st.error("Please select leads and enter message!")
                    return
                
                messages = [{"to": lead_options[lead], "message": bulk_message} for lead in selected_leads]
                
                result = api_post("whatsapp/send-bulk", {
                    "agent_instance_id": agent_id_bulk,
                    "messages": messages
                })
                
                if result and result.get('success'):
                    st.success(f"✅ Sent to {result.get('sent', 0)} leads!")
                    if result.get('errors'):
                        st.warning(f"Failed to send to {len(result['errors'])} leads")
                else:
                    st.error("Failed to send bulk messages")
    
    with tab2:
        st.subheader("💬 Recent Conversations")
        
        phone_search = st.text_input("Search by phone", placeholder="+919876543210")
        
        if phone_search:
            # Get detailed messages
            messages_resp = api_get(f"conversations/{phone_search}/messages?limit=100")
            
            if messages_resp and messages_resp.get('success') and messages_resp.get('data'):
                data = messages_resp['data']
                
                # Get lead info
                lead_resp = api_get(f"leads?phone_number={phone_search}")
                lead_name = "Unknown"
                lead_status = "N/A"
                
                if lead_resp and lead_resp.get('success') and lead_resp.get('data'):
                    lead_data = lead_resp['data'][0] if lead_resp['data'] else None
                    if lead_data:
                        lead_name = lead_data.get('name', 'Unknown')
                        lead_status = lead_data.get('lead_status', 'N/A')
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Name", lead_name)
                with col2:
                    st.metric("Status", lead_status)
                with col3:
                    st.metric("Total Messages", len(data))
                
                st.divider()
                
                # Display conversation
                for msg in reversed(data):
                    is_from_user = msg.get('is_from_user', False)
                    timestamp = msg.get('timestamp', '')[:19] if msg.get('timestamp') else 'N/A'
                    message_body = msg.get('message_body', '')
                    
                    if is_from_user:
                        st.markdown(f"""
                        <div class="conversation-user" style="color: black;">
                            <small>{timestamp}</small><br>
                            <strong>👤 User:</strong> {message_body}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="conversation-bot" style="color: black;">
                            <small>{timestamp}</small><br>
                            <strong>🤖 AI:</strong> {message_body}
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("No conversation found")
    
    with tab3:
        st.subheader("⚙️ WhatsApp Setup Instructions")
        
        st.markdown("""
        ### 📋 Setup Steps
        
        1. **Create WhatsApp AI Agent** in the 'AI Agents' page
        2. **Get Meta WhatsApp Business API Credentials** from Meta Business Manager
        3. **Configure credentials** in the agent settings (shown above in AI Agents page)
        4. **Register webhook** in Meta Developer Console
        
        #### 🔗 Webhook URL
        Copy this URL and paste in Meta Developer Console:
        """)
        
        webhook_url = f"{API_BASE_URL.replace('/api', '')}/api/webhooks/whatsapp-universal"
        st.code(webhook_url)
        
        st.markdown("""
        #### ℹ️ How to Get Credentials
        
        1. Go to [Meta Business Manager](https://business.facebook.com/)
        2. Navigate to **WhatsApp** > **API Setup**
        3. Get your:
           - **Access Token** (Permanent token recommended)
           - **Phone Number ID** (from your WhatsApp Business Account)
           - **Business Account ID**
        4. Save these credentials in your agent's WhatsApp setup section
        5. Register the webhook URL above in Meta's webhook configuration
        6. Use the **Verify Token** shown after saving credentials
        
        #### 🔒 Security Note
        Your credentials are encrypted and stored securely in the database.
        """)

# ==================== PAGE: CAMPAIGNS ====================
def page_campaigns():
    """Campaigns management page"""
    st.title("🎯 Marketing Campaigns")
    
    tab1, tab2 = st.tabs(["Active Campaigns", "Create Campaign"])
    
    with tab1:
        st.subheader("Campaign Performance")
        
        # Fetch campaigns
        campaigns_resp = api_get(f"campaigns?company_id={st.session_state.company_id}")
        
        if campaigns_resp and campaigns_resp.get('success') and campaigns_resp.get('data'):
            for campaign in campaigns_resp['data']:
                with st.expander(f"📢 {campaign['campaign_name']} - {campaign['status']}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**Type:** {campaign['campaign_type']}")
                        st.write(f"**Total Leads:** {campaign.get('total_leads', 0)}")
                    
                    with col2:
                        st.write(f"**Started:** {campaign.get('scheduled_start', 'N/A')[:10] if campaign.get('scheduled_start') else 'Not started'}")
                        st.write(f"**Status:** {campaign['status']}")
                    
                    with col3:
                        st.write(f"**Call Rate:** {campaign.get('call_rate_per_minute', 1)}/min")
                    
                    # Get campaign stats
                    if st.button("View Stats", key=f"stats_{campaign['id']}"):
                        stats_resp = api_get(f"campaigns/{campaign['id']}/stats")
                        if stats_resp and stats_resp.get('success'):
                            stats_data = stats_resp['data']
                            
                            col_s1, col_s2, col_s3, col_s4 = st.columns(4)
                            with col_s1:
                                st.metric("Pending", stats_data.get('pending', 0))
                            with col_s2:
                                st.metric("Called", stats_data.get('called', 0))
                            with col_s3:
                                st.metric("Completed", stats_data.get('completed', 0))
                            with col_s4:
                                st.metric("Failed", stats_data.get('failed', 0))
                        else:
                            st.info("Stats not available yet")
        else:
            st.info("No campaigns found. Create your first campaign!")
    
    with tab2:
        st.subheader("Create New Campaign")
        
        with st.form("create_campaign_form"):
            campaign_name = st.text_input("Campaign Name*", placeholder="Chess Coaching Outreach")
            campaign_type = st.selectbox("Type", ["outbound", "follow_up", "renewal", "nurture"])
            
            # Lead selection filters
            st.markdown("**Target Leads**")
            col1, col2 = st.columns(2)
            
            with col1:
                lead_source = st.multiselect("Lead Source",
                    ["whatsapp", "website", "google_ads", "meta_ads", "referral"],
                    default=["whatsapp", "website"])
            
            with col2:
                lead_status = st.multiselect("Lead Status",
                    ["new", "contacted", "qualified", "lost"],
                    default=["new", "contacted"])
            
            call_rate = st.slider("Calls per Minute", 1, 10, 2)
            
            col3, col4 = st.columns(2)
            with col3:
                scheduled_start = st.date_input("Start Date",
                    value=datetime.now() + timedelta(days=1))
            with col4:
                start_time = st.time_input("Start Time", value=datetime.now().time())
            
            message_template = st.text_area("WhatsApp Message Template (Optional)", 
                height=100, placeholder="Hi {{name}}, we're excited about your interest in chess coaching...")
            
            submitted = st.form_submit_button("Create Campaign", use_container_width=True)
            
            if submitted:
                if not campaign_name:
                    st.error("Campaign name is required!")
                    return
                
                start_datetime = datetime.combine(scheduled_start, start_time).isoformat()
                
                # Build lead filter
                lead_filter = {
                    "lead_sources": lead_source,
                    "lead_statuses": lead_status
                }
                
                data = {
                    "company_id": st.session_state.company_id,
                    "campaign_name": campaign_name,
                    "campaign_type": campaign_type,
                    "lead_filter": lead_filter,
                    "call_rate_per_minute": call_rate,
                    "scheduled_start": start_datetime,
                    "message_template": message_template if message_template else None
                }
                
                result = api_post("campaigns", data)
                if result and result.get('success'):
                    st.success(f"✅ Campaign '{campaign_name}' created! ID: {result['data']['id']}")
                    st.info("Campaign will start processing leads and scheduling calls")
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("Failed to create campaign")

# ==================== PAGE: HUMAN AGENTS ====================
def page_human_agents():
    st.title("👨‍💼 Human Sales Agents")
    
    tab1, tab2, tab3 = st.tabs(["View Agents", "Add Agent", "Takeover Requests"])
    
    with tab1:
        st.subheader("Sales Team")
        
        agents_resp = api_get("human-agents")
        
        if agents_resp and agents_resp.get('success'):
            for agent in agents_resp['data']:
                with st.expander(f"👤 {agent['name']} - {agent['role']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Email:** {agent['email']}")
                        st.write(f"**Phone:** {agent.get('phone', 'N/A')}")
                        st.write(f"**Status:** {agent['status']}")
                    
                    with col2:
                        st.write(f"**Assigned Leads:** {agent['assigned_leads']}")
                        st.write(f"**Max Concurrent:** {agent['max_concurrent_leads']}")
                        st.write(f"**Role:** {agent['role']}")
                    
                    # Update status
                    new_status = st.selectbox(
                        "Change Status",
                        ["available", "busy", "offline"],
                        key=f"status_{agent['id']}"
                    )
                    
                    if st.button("Update Status", key=f"update_{agent['id']}"):
                        result = api_patch(f"human-agents/{agent['id']}/status", {"status": new_status})
                        if result and result.get('success'):
                            st.success("Status updated")
                            st.rerun()
        else:
            st.info("No human agents found. Add your first agent!")
    
    with tab2:
        st.subheader("Add New Sales Agent")
        
        with st.form("add_agent_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Name*", placeholder="John Doe")
                email = st.text_input("Email*", placeholder="john@company.com")
                phone = st.text_input("Phone*", placeholder="+919876543210")
            
            with col2:
                role = st.selectbox("Role", ["sales_rep", "senior_rep", "manager"])
                max_concurrent = st.number_input("Max Concurrent Leads", min_value=1, max_value=50, value=5)
                expertise = st.multiselect("Expertise", 
                    ["chess_coaching", "payment_issues", "technical_support", "general_sales"],
                    default=["general_sales"])
            
            submitted = st.form_submit_button("Add Agent", use_container_width=True)
            
            if submitted:
                if not name or not email or not phone:
                    st.error("Name, email and phone are required!")
                    return
                
                data = {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "role": role,
                    "max_concurrent_leads": max_concurrent,
                    "expertise": expertise,
                    "status": "available",
                    "assigned_leads": 0
                }
                
                result = api_post("human-agents", data)
                
                if result and result.get('success'):
                    st.success(f"✅ Agent {name} added successfully!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Failed to add agent")
    
    with tab3:
        st.subheader("🔥 Pending Takeover Requests")
        
        takeover_resp = api_get("takeover/pending")
        
        if takeover_resp and takeover_resp.get('success') and takeover_resp.get('data'):
            requests = takeover_resp['data']
            
            for req in requests:
                with st.expander(f"🚨 {req['trigger_reason']} - Lead ID: {req['lead_id']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Priority:** {req['priority']}")
                        st.write(f"**Type:** {req['request_type']}")
                        st.write(f"**Status:** {req['status']}")
                    
                    with col2:
                        st.write(f"**Created:** {req['created_at'][:19]}")
                        if req.get('assigned_agent_id'):
                            st.write(f"**Assigned To:** Agent {req['assigned_agent_id']}")
                    
                    if req.get('ai_summary'):
                        st.info(f"**AI Summary:** {req['ai_summary']}")
                    
                    if req.get('conversation_context'):
                        with st.expander("View Context"):
                            st.text(req['conversation_context'])
                    
                    # Actions
                    col_a1, col_a2 = st.columns(2)
                    
                    with col_a1:
                        if st.button("Accept Takeover", key=f"accept_{req['id']}"):
                            # You would need to implement agent selection
                            result = api_patch(f"takeover/{req['id']}/accept", {"agent_id": 1})
                            if result and result.get('success'):
                                st.success("Takeover accepted!")
                                st.rerun()
                    
                    with col_a2:
                        if st.button("Dismiss", key=f"dismiss_{req['id']}"):
                            result = api_patch(f"takeover/{req['id']}/complete", {
                                "outcome": "dismissed",
                                "notes": "Dismissed by admin"
                            })
                            if result and result.get('success'):
                                st.success("Request dismissed")
                                st.rerun()
        else:
            st.info("No pending takeover requests")

# ==================== PAGE: ANALYTICS ====================
def page_analytics():
    st.title("📈 Analytics & Reports")
    
    tab1, tab2, tab3 = st.tabs(["Call Analytics", "Lead Analytics", "Revenue Analytics"])
    
    with tab1:
        st.subheader("📞 Call Performance")
        
        metrics_resp = api_get("metrics/dashboard")
        if metrics_resp and metrics_resp.get('success'):
            data = metrics_resp['data']
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Active Calls", data.get('active_calls', 0))
            with col2:
                calls_24h = data.get('calls_24h', [])
                total_calls = sum([c.get('count', 0) for c in calls_24h]) if calls_24h else 0
                st.metric("Calls (24h)", total_calls)
            with col3:
                st.metric("Success Rate", f"{data.get('success_rate', 0)}%")
            with col4:
                # Calculate avg duration
                avg_dur = 0
                for c in calls_24h:
                    if c.get('avg_duration'):
                        avg_dur += c['avg_duration']
                avg_dur = avg_dur / len(calls_24h) if calls_24h else 0
                st.metric("Avg Duration", f"{int(avg_dur)}s")
            
            st.divider()
            
            # Sentiment distribution
            sentiment_data = data.get('sentiment_distribution', [])
            if sentiment_data:
                st.subheader("😊 Sentiment Distribution")
                df = pd.DataFrame(sentiment_data)
                fig = px.bar(df, x='sentiment_type', y='count', color='sentiment_type',
                           title='Call Sentiment Breakdown')
                st.plotly_chart(fig, use_container_width=True)
            
            # Calls by type
            if calls_24h:
                st.subheader("Call Types (24h)")
                df_calls = pd.DataFrame(calls_24h)
                fig2 = px.pie(df_calls, names='call_type', values='count',
                            title='Call Distribution by Type')
                st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        st.subheader("👥 Lead Analytics")
        
        lead_stats_resp = api_get("stats/leads")
        if lead_stats_resp and lead_stats_resp.get('success'):
            df = pd.DataFrame(lead_stats_resp['data'])
            
            if not df.empty:
                df['count'] = pd.to_numeric(df['count'], errors='coerce')
                df['avg_interest'] = pd.to_numeric(df['avg_interest'], errors='coerce')

                # Leads by status
                st.subheader("Leads by Status")
                fig = px.bar(df, x='lead_status', y='count', color='lead_status',
                           title="Lead Distribution")
                st.plotly_chart(fig, use_container_width=True)
                
                # Average interest by status
                st.subheader("Interest Level by Status")
                fig2 = px.scatter(
                    df, x='lead_status', y='avg_interest', size='count',
                    title="Average Interest Level by Status"
                )

                st.plotly_chart(fig2, use_container_width=True)
                
                # Lead table
                st.subheader("Lead Status Summary")
                st.dataframe(df, use_container_width=True)
        else:
            st.info("No lead analytics available yet")
    
    with tab3:
        st.subheader("💰 Revenue Analytics")
        
        # Get invoice stats
        invoice_stats = api_get(f"invoices/stats?company_id={st.session_state.company_id}")
        
        if invoice_stats and invoice_stats.get('success'):
            data = invoice_stats['data']
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Revenue", f"₹{data.get('total_revenue', 0):,.2f}")
            with col2:
                st.metric("Pending Amount", f"₹{data.get('pending_amount', 0):,.2f}")
            with col3:
                st.metric("Paid Invoices", data.get('paid_count', 0))
            with col4:
                st.metric("Pending Invoices", data.get('pending_count', 0))
        else:
            st.info("No revenue data available yet")
            
            # Show placeholder metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Revenue", "₹0.00")
            with col2:
                st.metric("Pending Amount", "₹0.00")
            with col3:
                st.metric("Paid Invoices", 0)
            with col4:
                st.metric("Pending Invoices", 0)

# ==================== PAGE: NOTIFICATIONS ====================
def page_notifications():
    st.title("🔔 Notifications & Alerts")
    
    tab1, tab2 = st.tabs(["Recent Notifications", "Alerts"])
    
    with tab1:
        notif_resp = api_get("system-notifications?limit=50")
        
        if notif_resp and notif_resp.get('success'):
            for notif in notif_resp['data']:
                priority_emoji = {
                    'urgent': '🚨',
                    'high': '⚠️',
                    'normal': 'ℹ️',
                    'low': '💡'
                }
                
                emoji = priority_emoji.get(notif.get('priority', 'normal'), 'ℹ️')
                
                with st.expander(f"{emoji} {notif['title']} - {notif['created_at'][:16]}"):
                    st.write(notif['message'])
                    
                    if not notif.get('is_read'):
                        if st.button("Mark as Read", key=f"read_{notif['id']}"):
                            result = api_post(f"system-notifications/{notif['id']}/read", {})
                            if result and result.get('success'):
                                st.success("Marked as read")
                                st.rerun()
        else:
            st.info("No notifications")
    
    with tab2:
        alerts_resp = api_get("alerts?limit=20")
        
        if alerts_resp and alerts_resp.get('success'):
            for alert in alerts_resp['data']:
                severity_color = {
                    'critical': '🔴',
                    'high': '🟠',
                    'normal': '🟡',
                    'low': '🟢'
                }
                
                icon = severity_color.get(alert.get('severity', 'normal'), '🟡')
                
                with st.expander(f"{icon} {alert['title']} - {alert['created_at'][:16]}"):
                    st.write(alert['message'])
                    st.caption(f"Severity: {alert.get('severity', 'normal')}")
        else:
            st.info("No alerts")


def page_settings():
    st.title("⚙️ Settings & Configuration")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Company Info", "Lead Sources", "Email Scanning", "Integrations", "API Keys"])
    
    with tab1:
        st.subheader("🏢 Company Information")
        
        company_resp = api_get(f"companies/{st.session_state.company_id}")
        if company_resp and company_resp.get('success'):
            company = company_resp['data']
            
            with st.form("update_company"):
                name = st.text_input("Company Name", value=company.get('name', ''))
                phone = st.text_input("Phone Number", value=company.get('phone_number', ''))
                
                if st.form_submit_button("Update Company"):
                    result = api_patch(f"companies/{st.session_state.company_id}", {
                        "name": name,
                        "phone_number": phone
                    })
                    if result and result.get('success'):
                        st.success("Company updated!")
                        st.rerun()
        
        st.divider()
        
        st.subheader("🕐 Calling Hours Configuration")
        
        with st.form("calling_hours"):
            col1, col2 = st.columns(2)
            with col1:
                start_hour = st.number_input("Start Hour (24h)", 0, 23, 9)
            with col2:
                end_hour = st.number_input("End Hour (24h)", 0, 23, 18)
            
            call_rate = st.number_input("Calls per Minute", 1, 10, 2)
            max_concurrent = st.number_input("Max Concurrent Calls", 1, 20, 5)
            
            if st.form_submit_button("Save Calling Hours"):
                result = api_patch(f"companies/{st.session_state.company_id}/calling-hours", {
                    "start_hour": start_hour,
                    "end_hour": end_hour,
                    "call_rate_per_minute": call_rate,
                    "max_concurrent_calls": max_concurrent
                })
                if result and result.get('success'):
                    st.success("✅ Calling hours updated!")
    
    with tab2:
        render_lead_sources_settings()
    
    with tab3:
        render_email_scanning_settings()

    with tab4:
        st.subheader("🔗 Integration Status")
        
        integrations = {
            "WhatsApp Business API": "✅ Connected",
            "Twilio Voice": "✅ Connected",
            "Google Calendar": "✅ Connected",
            "Stripe Payments": "⚠️ Not Configured",
            "Razorpay": "⚠️ Not Configured",
            "SendGrid Email": "⚠️ Not Configured"
        }
        
        for name, status in integrations.items():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{name}**")
            with col2:
                st.write(status)
        
        st.divider()
        
        st.subheader("📊 System Health")
        health_resp = api_get("health")
        if health_resp:
            st.json(health_resp)
    
    with tab5:
        st.subheader("🔑 API Keys & Webhooks")
        
        st.markdown("### Webhook URLs")
        
        st.markdown("**WhatsApp Webhook:**")
        st.code(f"{API_BASE_URL.replace('/api', '')}/api/webhooks/whatsapp-universal")
        
        st.markdown("**n8n Webhook:**")
        st.code(f"{API_BASE_URL.replace('/api', '')}/api/webhooks/whatsapp-universal")
        
        st.divider()
        
        st.markdown("### API Configuration")
        st.info("API keys are configured in environment variables. Contact your system administrator to update them.")



# ==================== PAGE: LOGIN ====================
def page_login():
    st.title("🔐 Login to AI Sales CRM")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login"):
            st.markdown("### Sign In")
            
            companies_resp = api_get("companies")
            
            if companies_resp and companies_resp.get('success'):
                company_options = {f"{c['name']} (ID: {c['id']})": c for c in companies_resp['data']}
                
                if company_options:
                    selected = st.selectbox("Select Company", list(company_options.keys()))
                    selected_company = company_options[selected]
                    
                    username = st.text_input("Username")
                    password = st.text_input("Password", type="password")
                    
                    if st.form_submit_button("Login"):
                        if username and password:
                            st.session_state.authenticated = True
                            st.session_state.company_id = selected_company['id']
                            st.session_state.company_name = selected_company['name']
                            st.session_state.username = username
                            st.rerun()
                        else:
                            st.error("Please enter username and password")
                else:
                    st.error("No companies found. Please create a company first.")
            else:
                st.error("Unable to fetch companies. Please check API connection.")
        
        st.info("**Demo Mode:** Use any username/password to login")
        
        st.divider()
        
        with st.expander("🆕 Create New Company"):
            with st.form("create_company"):
                company_name = st.text_input("Company Name*")
                company_phone = st.text_input("Phone Number*", placeholder="+919876543210")
                
                if st.form_submit_button("Create Company"):
                    if company_name and company_phone:
                        result = api_post("companies", {
                            "name": company_name,
                            "phone_number": company_phone
                        })
                        if result and result.get('success'):
                            st.success(f"✅ Company created! ID: {result['data']['id']}")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Failed to create company")
                    else:
                        st.warning("Please fill all fields")

# ==================== MAIN APP ====================
def main():
    # Check authentication
    if not st.session_state.authenticated:
        page_login()
        return
    
    # Render sidebar
    render_sidebar()
    
    # Route to pages
    page = st.session_state.get('page', 'dashboard')
    
    try:
        if page == 'dashboard':
            page_dashboard()
        elif page == 'leads':
            page_leads()
        elif page == 'add_lead':
            page_add_lead()
        elif page == 'lead_detail':
            page_lead_detail()
        elif page == 'agents':
            page_agents()
        elif page == 'calling':
            page_calling()
        elif page == 'calendar':  # ← ADD THIS
            page_calendar()
        elif page == 'scheduled_calls':
            page_scheduled_calls()
        elif page == 'whatsapp':
            page_whatsapp()
        elif page == 'campaigns':
            page_campaigns()
        elif page == 'human_agents':
            page_human_agents()
        elif page == 'analytics':
            page_analytics()
        elif page == 'notifications':
            page_notifications()
        elif page == 'settings':
            page_settings()
        else:
            st.error(f"Page '{page}' not found")
    except Exception as e:
        st.error(f"Error loading page: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    main()