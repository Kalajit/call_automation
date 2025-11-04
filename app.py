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
# if 'authenticated' not in st.session_state:
#     st.session_state.authenticated = False
# if 'company_id' not in st.session_state:
#     st.session_state.company_id = 1
# if 'user_role' not in st.session_state:
#     st.session_state.user_role = "admin"


# # ---------- API HELPERS (auto-add company_id) ----------
# def _url(endpoint: str) -> str:
#     return f"{API_BASE_URL}/{endpoint}"

# # API Helper Functions
# def api_get(endpoint):
#     try:
#         response = requests.get(f"{API_BASE_URL}/{endpoint}", timeout=10)
#         response.raise_for_status()
#         return response.json()
#     except Exception as e:
#         st.error(f"API Error: {str(e)}")
#         return None

# def api_post(endpoint, data):
#     try:
#         response = requests.post(f"{API_BASE_URL}/{endpoint}", json=data, timeout=10)
#         response.raise_for_status()
#         return response.json()
#     except Exception as e:
#         st.error(f"API Error: {str(e)}")
#         return None

# def python_api_post(endpoint, data):
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
#     if not stats:
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

# # Page 2: Companies Management
# def page_companies():
#     st.title("🏢 Companies Management")
    
#     tab1, tab2 = st.tabs(["View Companies", "Add New Company"])
    
#     with tab1:
#         companies = api_get("companies")
#         if companies and companies.get('data'):
#             df = pd.DataFrame(companies['data'])
#             st.dataframe(df, use_container_width=True)
#         else:
#             st.info("No companies found")
    
#     with tab2:
#         st.subheader("Create New Company")
        
#         with st.form("add_company"):
#             name = st.text_input("Company Name*")
#             phone = st.text_input("Phone Number*", placeholder="+919876543210")
            
#             if st.form_submit_button("Create Company"):
#                 if name and phone:
#                     result = api_post("companies", {"name": name, "phone_number": phone})
#                     if result and result.get('success'):
#                         st.success(f"✅ Company created! ID: {result.get('data', {}).get('id')}")
#                         st.rerun()
#                     else:
#                         st.error("Failed to create company")
#                 else:
#                     st.warning("Please fill all required fields")

# # Page 3: AI Agents
# def page_agents():
#     st.title("🤖 AI Agent Instances (CloserX Style)")
    
#     tab1, tab2, tab3 = st.tabs(["View Agents", "Create Agent", "Configure Agent"])
    
#     with tab1:
#         company_id = st.selectbox("Select Company", [1, 2, 3], key="agent_company_select")
#         agents = api_get(f"agent-instances/company/{company_id}")
        
#         if agents and agents.get('data'):
#             for agent in agents['data']:
#                 with st.expander(f"🤖 {agent['agent_name']} ({agent['agent_type']})"):
#                     col1, col2 = st.columns(2)
#                     with col1:
#                         st.write(f"**Phone:** {agent['phone_number']}")
#                         st.write(f"**Status:** {'🟢 Active' if agent['is_active'] else '🔴 Inactive'}")
#                     with col2:
#                         st.write(f"**Created:** {agent['created_at'][:10]}")
#                         st.write(f"**Voice:** {agent.get('default_voice', 'N/A')}")
                    
#                     if st.button(f"Edit {agent['agent_name']}", key=f"edit_{agent['id']}"):
#                         st.session_state.edit_agent_id = agent['id']
#                         st.rerun()
#         else:
#             st.info("No agents found for this company")
    
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
#         st.subheader("🚀 Initiate Outbound Call")
        
#         with st.form("make_call"):
#             col1, col2 = st.columns(2)
            
#             with col1:
#                 company_id = st.number_input("Company ID", min_value=1, value=1)
#                 lead_id = st.number_input("Lead ID", min_value=1, value=1)
#                 to_phone = st.text_input("Phone Number*", placeholder="+919876543210")
#                 name = st.text_input("Name", placeholder="Ajsal")
            
#             with col2:
#                 call_type = st.selectbox("Call Type", ["qualification", "reminder", "payment", "support"])
#                 prompt_key = st.selectbox("Prompt", ["chess_coach", "medical_sales", "hospital_receptionist"])
#                 agent_instance_id = st.number_input("Agent Instance ID (optional)", min_value=0, value=0)
            
#             if st.form_submit_button("📞 Make Call Now"):
#                 if to_phone:
#                     data = {
#                         "company_id": company_id,
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
#                         st.success(f"✅ Call initiated! SID: {result.get('call_sid')}")
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
                    
#                     # This would call n8n webhook
#                     st.info("Message queued for delivery via n8n workflow")
#                     st.json(data)
#                 else:
#                     st.warning("Phone number is required")
    
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









# app.py
import streamlit as st
import requests
import pandas as pd
import json
from datetime import datetime, timedelta
import plotly.express as px
import time
from typing import Optional, Dict, List

# ==================== CONFIGURATION ====================
API_BASE_URL = "http://localhost:3000/api"
PYTHON_API_URL = "http://localhost:8000/api"

st.set_page_config(
    page_title="4champz AI Sales CRM",
    page_icon="Robot",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    .main-header {font-size: 2.5rem; font-weight: bold; color: #667eea; margin-bottom: 1rem;}
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px; border-radius: 10px; color: white; margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .lead-card {
        border-left: 4px solid #667eea; padding: 12px; margin: 8px 0;
        background: white; border-radius: 5px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .agent-card {
        border: 2px solid #667eea; border-radius: 10px; padding: 15px; margin: 10px 0;
        background: #f8f9fa;
    }
    .status-badge {padding: 5px 10px; border-radius: 15px; font-size: 0.85rem; font-weight: bold;}
    .status-active {background: #d4edda; color: #155724;}
    .status-inactive {background: #f8d7da; color: #721c24;}
    .status-qualified {background: #cfe2ff; color: #084298;}
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; border: none; border-radius: 5px; padding: 0.5rem 1rem; font-weight: bold;
    }
    .stButton>button:hover {opacity: 0.9; transform: translateY(-2px); transition: 0.3s;}
    .success-box {background: #d4edda; border: 1px solid #c3e6cb; padding: 10px; border-radius: 5px; margin: 10px 0;}
    .warning-box {background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; border-radius: 5px; margin: 10px 0;}
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
for key in ['authenticated', 'company_id', 'company_name', 'user_role', 'page']:
    if key not in st.session_state:
        st.session_state[key] = None

# ==================== API HELPERS ====================
def api_get(endpoint: str, params: Dict = None) -> Optional[Dict]:
    try:
        url = f"{API_BASE_URL}/{endpoint}"
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

def api_post(endpoint: str, data: Dict) -> Optional[Dict]:
    try:
        response = requests.post(f"{API_BASE_URL}/{endpoint}", json=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

def api_patch(endpoint: str, data: Dict) -> Optional[Dict]:
    try:
        response = requests.patch(f"{API_BASE_URL}/{endpoint}", json=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

def python_api_post(endpoint: str, data: Dict) -> Optional[Dict]:
    try:
        response = requests.post(f"{PYTHON_API_URL}/{endpoint}", json=data, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Python API Error: {str(e)}")
        return None

# ==================== AUTH ====================
def render_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="main-header">4champz AI CRM</div>', unsafe_allow_html=True)
        st.markdown("### Login to Your Dashboard")
        with st.form("login_form"):
            company_id = st.number_input("Company ID", min_value=1, value=1)
            username = st.text_input("Username (demo: any)")
            password = st.text_input("Password (demo: any)", type="password")
            if st.form_submit_button("Login", use_container_width=True):
                company = api_get(f"companies/{company_id}")
                if company and company.get('success'):
                    st.session_state.update({
                        'authenticated': True,
                        'company_id': company_id,
                        'company_name': company['data']['name'],
                        'user_role': 'admin'
                    })
                    st.rerun()
                else:
                    st.error("Invalid Company ID")
        st.info("Demo: Use Company ID 1, 2, or 3")

# ==================== SIDEBAR ====================
def render_sidebar():
    with st.sidebar:
        st.markdown(f"### {st.session_state.company_name}")
        st.caption(f"ID: {st.session_state.company_id} | Role: {st.session_state.user_role}")
        st.divider()
        menu = {
            "Dashboard": "dashboard",
            "Companies": "companies",
            "AI Agents": "agents",
            "Calling": "calling",
            "WhatsApp": "whatsapp",
            "Leads": "leads",
            "Analytics": "analytics",
            "Notifications": "notifications",
            "Settings": "settings"
        }
        selected = st.radio("Navigation", list(menu.keys()), label_visibility="collapsed")
        st.session_state.page = menu[selected]
        st.divider()
        if st.button("Logout", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

# ==================== PAGES ====================

def page_dashboard():
    st.markdown('<div class="main-header">Dashboard Overview</div>', unsafe_allow_html=True)
    stats = api_get("stats/dashboard")
    if not stats or not stats.get('success'):
        st.warning("Unable to load data"); return
    data = stats['data']

    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        ("Total Leads", 'total_leads'), 
        ("Conversations", 'total_conversations'), 
        ("Pending Invoices", 'pending_invoices'), 
        ("Avg Interest", 'avg_interest_level')
    ]
    for col, (label, key) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            value = data.get(key, 0)
            if key == 'avg_interest_level':
                try:
                    value = f"{float(value):.1f}/10"
                except (ValueError, TypeError):
                    value = "N/A"
            st.metric(label, value)
            st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Leads by Status")
        if data.get('leads_by_status'):
            df = pd.DataFrame(data['leads_by_status'])
            fig = px.pie(df, names='lead_status', values='count', hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("Hot Leads Today")
        hot = api_get("hot-leads")
        if hot and hot.get('data'):
            for lead in hot['data'][:5]:
                st.markdown(f"""
                <div class="lead-card">
                    <b>{lead['name']}</b> • {lead['phone_number']}<br>
                    <small>Tone: {lead.get('tone_score','N/A')} | Intent: {lead.get('intent','N/A')}</small>
                </div>
                """, unsafe_allow_html=True)

    st.subheader("Recent Activity")
    tab1, tab2 = st.tabs(["Calls", "Messages"])
    with tab1:
        calls = api_get(f"call-logs?company_id={st.session_state.company_id}&limit=10")
        if calls and calls.get('data'):
            df = pd.DataFrame(calls['data'])
            df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
            st.dataframe(df[['to_phone', 'call_status', 'call_duration', 'created_at']], use_container_width=True)
    with tab2:
        msg = api_get("stats/messages")
        if msg and msg.get('data'):
            st.dataframe(pd.DataFrame(msg['data']), use_container_width=True)

def page_companies():
    st.markdown('<div class="main-header">Companies Management</div>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["View Companies", "Add New Company"])
    with tab1:
        companies = api_get("companies")
        if companies and companies.get('data'):
            df = pd.DataFrame(companies['data'])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No companies found")
    with tab2:
        with st.form("add_company"):
            name = st.text_input("Company Name*")
            phone = st.text_input("Phone Number*", placeholder="+919876543210")
            if st.form_submit_button("Create Company"):
                if name and phone:
                    result = api_post("companies", {"name": name, "phone_number": phone})
                    if result and result.get('success'):
                        st.success(f"Company created! ID: {result.get('data', {}).get('id')}")
                        st.rerun()
                    else:
                        st.error("Failed to create company")
                else:
                    st.warning("Please fill all required fields")

def page_agents():
    st.markdown('<div class="main-header">AI Agent Instances</div>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["My Agents", "Create New", "Apply Template"])
    with tab1:
        agents = api_get(f"agent-instances/company/{st.session_state.company_id}")
        if agents and agents.get('data'):
            for agent in agents['data']:
                with st.expander(f"{agent['agent_name']} ({agent['agent_type'].upper()})"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**Phone:** {agent.get('phone_number', 'N/A')}")
                        st.write(f"**WhatsApp:** {agent.get('whatsapp_number', 'N/A')}")
                    with col2:
                        status_class = "status-active" if agent['is_active'] else "status-inactive"
                        status_text = "Active" if agent['is_active'] else "Inactive"
                        st.markdown(f'<span class="status-badge {status_class}">{status_text}</span>', unsafe_allow_html=True)
                        st.write(f"**Voice:** {agent.get('custom_voice') or agent.get('default_voice', 'N/A')}")
                    with col3:
                        st.write(f"**Created:** {agent['created_at'][:10]}")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        new_status = not agent['is_active']
                        btn_text = "Deactivate" if agent['is_active'] else "Activate"
                        if st.button(btn_text, key=f"toggle_{agent['id']}"):
                            result = api_patch(f"agent-instances/{agent['id']}", {"is_active": new_status})
                            if result: st.success(f"Agent {btn_text}d!"); time.sleep(1); st.rerun()
                    with col_b:
                        if st.button("View Webhook", key=f"webhook_{agent['id']}"):
                            st.code(f"Webhook: {API_BASE_URL}/webhooks/whatsapp-universal")
        else:
            st.info("No agents found")
    with tab2:
        with st.form("create_agent"):
            agent_name = st.text_input("Agent Name*")
            agent_type = st.selectbox("Type*", ["voice", "whatsapp"])
            col1, col2 = st.columns(2)
            with col1:
                phone = st.text_input("Phone (Voice)", "")
            with col2:
                whatsapp = st.text_input("WhatsApp Number", "")
            prompt = st.text_area("Custom Prompt (Optional)", height=150)
            voice = st.selectbox("Voice", ["Raveena", "Aditi", "Brian", "Matthew"])
            if st.form_submit_button("Create Agent"):
                if not agent_name:
                    st.error("Name required")
                else:
                    data = {
                        "company_id": st.session_state.company_id,
                        "agent_name": agent_name,
                        "agent_type": agent_type,
                        "phone_number": phone or None,
                        "whatsapp_number": whatsapp or None,
                        "custom_prompt": prompt or None,
                        "custom_voice": voice
                    }
                    result = api_post("agent-instances", data)
                    if result and result.get('success'):
                        st.success(f"Agent created! ID: {result['data']['id']}")
                        time.sleep(2); st.rerun()
    with tab3:
        templates = api_get("extraction-templates")
        if templates and templates.get('data'):
            template_names = [t['template_name'] for t in templates['data']]
            selected = st.selectbox("Template", template_names)
            agent_id = st.number_input("Agent ID (optional)", 0)
            if st.button("Apply Template"):
                template_id = next(t['id'] for t in templates['data'] if t['template_name'] == selected)
                result = api_post(f"companies/{st.session_state.company_id}/apply-template", {
                    "template_id": template_id,
                    "agent_instance_id": agent_id if agent_id > 0 else None
                })
                if result and result.get('success'):
                    st.success(f"Template applied! {len(result['data'])} fields configured")

def page_calling():
    st.markdown('<div class="main-header">AI Calling System</div>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["Make Call", "Call Logs", "Schedule Call"])
    with tab1:
        with st.form("make_call"):
            col1, col2 = st.columns(2)
            with col1:
                lead_id = st.number_input("Lead ID", min_value=1)
                to_phone = st.text_input("Phone*", "")
                name = st.text_input("Name", "")
            with col2:
                call_type = st.selectbox("Type", ["qualification", "reminder", "payment"])
                agents = api_get(f"agent-instances/company/{st.session_state.company_id}?agent_type=voice")
                agent_id = None
                if agents and agents.get('data'):
                    opt = st.selectbox("Agent", ["Default"] + [f"{a['agent_name']}" for a in agents['data']])
                    if opt != "Default":
                        agent_id = next(a['id'] for a in agents['data'] if a['agent_name'] == opt)
            if st.form_submit_button("Call Now"):
                data = {"company_id": st.session_state.company_id, "lead_id": lead_id, "to_phone": to_phone, "name": name, "call_type": call_type}
                result = python_api_post(f"outbound-call-agent?agent_instance_id={agent_id}" if agent_id else "outbound-call", data)
                if result and result.get('success'):
                    st.success(f"Call SID: {result.get('call_sid')}")
    with tab2:
        calls = api_get(f"call-logs?company_id={st.session_state.company_id}&limit=50")
        if calls and calls.get('data'):
            for call in calls['data']:
                with st.expander(f"{call['to_phone']} - {call['call_status']}"):
                    st.write(f"**Duration:** {call.get('call_duration',0)}s")
                    if call.get('recording_url'):
                        st.markdown(f"[Recording]({call['recording_url']})")
                    if call.get('transcript'):
                        st.text_area("Transcript", call['transcript'], height=100, disabled=True, key=f"t_{call['id']}")
    with tab3:
        with st.form("schedule_call"):
            lead_id = st.number_input("Lead ID", 1)
            call_type = st.selectbox("Type", ["qualification", "reminder"])
            date = st.date_input("Date", datetime.now() + timedelta(days=1))
            time_ = st.time_input("Time", datetime.now().time())
            if st.form_submit_button("Schedule"):
                scheduled = datetime.combine(date, time_).isoformat()
                result = api_post("schedule-call", {
                    "company_id": st.session_state.company_id,
                    "lead_id": lead_id,
                    "call_type": call_type,
                    "scheduled_time": scheduled
                })
                if result and result.get('success'):
                    st.success("Call scheduled!")

def page_whatsapp():
    st.markdown('<div class="main-header">WhatsApp Management</div>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["Send", "Conversations", "Setup"])
    with tab1:
        agents = api_get(f"agent-instances/company/{st.session_state.company_id}?agent_type=whatsapp")
        if not agents or not agents.get('data'):
            st.warning("No WhatsApp agent"); return
        agent = st.selectbox("From", [f"{a['agent_name']}" for a in agents['data']])
        agent_id = next(a['id'] for a in agents['data'] if a['agent_name'] == agent)
        with st.form("send_wa"):
            to = st.text_input("To Phone*")
            msg = st.text_area("Message*")
            if st.form_submit_button("Send"):
                result = api_post("whatsapp/send", {"to": to, "message": msg, "agent_instance_id": agent_id})
                if result and result.get('success'):
                    st.success("Sent!")
    with tab2:
        phone = st.text_input("Search Phone")
        if phone:
            conv = api_get(f"conversations/{phone}")
            if conv and conv.get('data'):
                st.text_area("History", conv['data'].get('conversation_history', ''), height=300)
    with tab3:
        st.code(f"Webhook URL: https://n8n-render-host-n0ym.onrender.com/webhook-test/webhook/whatsapp-trigger")
        with st.form("wa_setup"):
            agent_id = st.number_input("Agent ID", 1)
            token = st.text_input("Access Token*", type="password")
            phone_id = st.text_input("Phone Number ID*")
            if st.form_submit_button("Save"):
                result = api_post(f"agent-instances/{agent_id}/whatsapp-credentials", {
                    "access_token": token, "phone_number_id": phone_id
                })
                if result and result.get('success'):
                    st.success("Saved!")
                    st.code(f"Verify Token: {result.get('verify_token')}")

def page_leads():
    st.markdown('<div class="main-header">Lead Management</div>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["View Leads", "Add Lead", "Bulk Import"])
    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            status = st.selectbox("Status", ["All", "new", "contacted", "qualified", "lost"])
        with col2:
            source = st.selectbox("Source", ["All", "whatsapp", "website", "google_ads", "meta_ads"])
        with col3:
            limit = st.number_input("Limit", 10, 500, 50)
        params = {"limit": limit}
        if status != "All": params["status"] = status
        leads = api_get("leads", params=params)
        if not leads or not leads.get('data'):
            st.info("No leads"); return
        for lead in leads['data']:
            with st.expander(f"{lead['name']} - {lead['phone_number']} ({lead['lead_status']})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Email:** {lead.get('email','N/A')}")
                    st.write(f"**Source:** {lead['lead_source']}")
                    st.write(f"**Interest:** {lead['interest_level']}/10")
                with col2:
                    st.write(f"**Chess Rating:** {lead.get('chess_rating','N/A')}")
                    st.write(f"**Location:** {lead.get('location','N/A')}")
                    st.write(f"**Last Contact:** {lead.get('last_contacted','Never')[:10]}")
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    if st.button("Call", key=f"call_{lead['id']}"):
                        st.session_state.call_lead = lead
                with col_b:
                    if st.button("WhatsApp", key=f"wa_{lead['id']}"):
                        st.session_state.wa_lead = lead
                with col_c:
                    if st.button("Edit", key=f"edit_{lead['id']}"):
                        with st.form(f"edit_{lead['id']}"):
                            new_status = st.selectbox("Status", ["new", "contacted", "qualified", "lost"], index=["new", "contacted", "qualified", "lost"].index(lead['lead_status']), key=f"status_{lead['id']}")
                            interest = st.slider("Interest", 1, 10, lead['interest_level'], key=f"int_{lead['id']}")
                            if st.form_submit_button("Update"):
                                api_patch(f"leads/{lead['id']}", {"lead_status": new_status, "interest_level": interest})
                                st.success("Updated"); st.rerun()
    with tab2:
        with st.form("add_lead"):
            col1, col2 = st.columns(2)
            with col1:
                phone = st.text_input("Phone Number*")
                name = st.text_input("Name")
                email = st.text_input("Email")
                source = st.selectbox("Source", ["whatsapp", "website", "google_ads", "meta_ads"])
            with col2:
                chess = st.number_input("Chess Rating", 0, 3000, 0)
                location = st.text_input("Location")
                interest = st.slider("Interest", 1, 10, 5)
            if st.form_submit_button("Add Lead"):
                if phone:
                    result = api_post("leads", {
                        "phone_number": phone, "name": name, "email": email, "lead_source": source,
                        "interest_level": interest, "chess_rating": chess if chess > 0 else None, "location": location
                    })
                    if result and result.get('success'):
                        st.success(f"Lead added! ID: {result['data']['id']}")
                        st.rerun()
    with tab3:
        uploaded = st.file_uploader("Upload CSV", type="csv")
        if uploaded:
            df = pd.read_csv(uploaded)
            st.dataframe(df.head())
            if st.button("Import All"):
                result = api_post("leads/bulk", {"leads": df.to_dict('records')})
                if result and result.get('success'):
                    st.success(f"Imported {result.get('imported')} leads!")

def page_analytics():
    st.markdown('<div class="main-header">Analytics</div>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["Call", "Lead", "Revenue"])
    with tab1:
        metrics = api_get("metrics/dashboard")
        if metrics and metrics.get('data'):
            data = metrics['data']
            col1, col2, col3 = st.columns(3)
            with col1: st.metric("Active Calls", data.get('active_calls',0))
            with col2: st.metric("Calls (24h)", sum(c.get('count',0) for c in data.get('calls_24h',[])))
            with col3: st.metric("Success Rate", f"{data.get('success_rate',0)}%")
    with tab2:
        stats = api_get("stats/leads")
        if stats and stats.get('data'):
            df = pd.DataFrame(stats['data'])
            fig = px.bar(df, x='lead_status', y='count', color='lead_status')
            st.plotly_chart(fig, use_container_width=True)
    with tab3:
        st.info("Revenue tracking coming soon...")

def page_notifications():
    st.markdown('<div class="main-header">Notifications</div>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Recent", "Alerts"])
    with tab1:
        notifs = api_get("system-notifications?limit=20")
        if notifs and notifs.get('data'):
            for n in notifs['data']:
                with st.expander(f"{n['title']} - {n['created_at'][:16]}"):
                    st.write(n['message'])
                    if not n.get('is_read') and st.button("Mark Read", key=f"read_{n['id']}"):
                        api_post(f"system-notifications/{n['id']}/read", {})
                        st.rerun()
    with tab2:
        alerts = api_get("alerts?limit=20")
        if alerts and alerts.get('data'):
            for a in alerts['data']:
                with st.expander(f"{a['title']} - {a['created_at'][:16]}"):
                    st.write(a['message'])

def page_settings():
    st.markdown('<div class="main-header">Settings</div>', unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(["Human Agents", "Custom Fields", "Integrations", "System"])
    with tab1:
        agents = api_get("human-agents")
        if agents and agents.get('data'):
            for a in agents['data']:
                with st.expander(f"{a['name']}"):
                    st.write(f"**Email:** {a['email']} | **Status:** {a['status']}")
                    new = st.selectbox("Status", ["available", "busy", "offline"], key=f"s_{a['id']}")
                    if st.button("Update", key=f"u_{a['id']}"):
                        api_patch(f"human-agents/{a['id']}/status", {"status": new})
                        st.success("Updated")
    with tab2:
        templates = api_get("extraction-templates")
        if templates and templates.get('data'):
            for t in templates['data']:
                with st.expander(f"{t['template_name']}"):
                    st.write(t['description'])
    with tab3:
        st.info("Twilio, WhatsApp, Stripe: Connected")
    with tab4:
        health = api_get("health")
        if health:
            st.json(health)

# ==================== MAIN ====================
def main():
    if not st.session_state.authenticated:
        render_login()
        return
    render_sidebar()
    page = st.session_state.get('page', 'dashboard')
    globals()[f"page_{page}"]()

if __name__ == "__main__":
    main()