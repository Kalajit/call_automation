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
API_BASE_URL = "http://localhost:3000/api"        # Change if needed
PYTHON_API_URL = "http://localhost:8000/api"      # Change if needed
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
if 'selected_lead_id' not in st.session_state:
    st.session_state.selected_lead_id = None

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
   
    stats = api_get(f"stats/dashboard?company_id={st.session_state.company_id}")
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
        st.metric("Hot Leads", data.get('hot_leads_count', 0))
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
        else:
            st.info("No status data")
   
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
        if calls_resp and calls_resp.get('success') and calls_resp.get('data'):
            df = pd.DataFrame(calls_resp['data'])
            df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
            st.dataframe(df[['call_sid', 'to_phone', 'call_status', 'call_duration', 'created_at']], use_container_width=True)
        else:
            st.info("No calls yet")
   
    with tab2:
        messages_resp = api_get(f"stats/messages?company_id={st.session_state.company_id}")
        if messages_resp and messages_resp.get('success') and messages_resp.get('data'):
            df = pd.DataFrame(messages_resp['data'])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No messages yet")

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
        # tags = st.text_input("Tags (comma separated)", placeholder="vip, premium")
        
        submitted = st.form_submit_button("Add Lead", use_container_width=True)
        
        if submitted:
            if not phone_number:
                st.error("Phone number is required!")
                return

            # # Convert tags → Postgres array literal
            # tags_array = None
            # if tags:
            #     tag_list = [t.strip() for t in tags.split(",") if t.strip()]
            #     tags_array = "{" + ",".join(tag_list) + "}"  # Postgres array literal format
            
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
                # "tags": tags_array,
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
#         tag_filter = st.text_input("Filter by Tag", placeholder="vip")
    
#     # Build query
#     query_params = f"company_id={st.session_state.company_id}&limit={limit}"
#     if status_filter != "All":
#         query_params += f"&status={status_filter}"
#     if source_filter != "All":
#         query_params += f"&source={source_filter}"
#     if search_term:
#         query_params += f"&search={search_term}"
#     if tag_filter:
#         query_params += f"&tag={tag_filter}"
    
#     leads_resp = api_get(f"leads?{query_params}")
    
#     if not leads_resp or not leads_resp.get('success'):
#         st.warning("No leads found")
#         return
    
#     leads = leads_resp['data']
    
#     # Export button
#     if st.button("📊 Export to CSV"):
#         csv_url = f"{API_BASE_URL}/leads/export/csv?company_id={st.session_state.company_id}"
#         try:
#             response = requests.get(csv_url)
#             st.download_button(
#                 label="Download Leads CSV",
#                 data=response.content,
#                 file_name=f"leads_{st.session_state.company_name}_{datetime.now().strftime('%Y%m%d')}.csv",
#                 mime="text/csv"
#             )
#         except Exception as e:
#             st.error(f"Export failed: {str(e)}")
    
#     st.divider()
    
#     # Display leads as cards
#     for lead in leads:
#         with st.container():
#             col1, col2 = st.columns([4, 1])
#             with col1:
#                 st.markdown(f"**{lead.get('name', 'Unknown')}** - {lead['phone_number']}")
#                 st.caption(f"Status: {lead['lead_status']} | Source: {lead.get('lead_source', 'N/A')} | Interest: {lead.get('interest_level', 0)}/10")
#             with col2:
#                 if st.button("View Profile", key=f"view_{lead['id']}"):
#                     st.session_state.selected_lead_id = lead['id']  # UPDATED: Properly set ID
#                     st.session_state.page = 'lead_detail'
#                     st.rerun()




def page_leads():
    st.title("Lead Management")

    # === FILTERS ===
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        status_filter = st.selectbox("Status", ["All", "new", "contacted", "qualified", "lost"], key="lead_status_filter")
    with col2:
        source_filter = st.selectbox("Source", ["All", "whatsapp", "website", "google_ads", "meta_ads"], key="lead_source_filter")
    with col3:
        limit = st.number_input("Limit", min_value=10, max_value=500, value=50, key="lead_limit")
    with col4:
        search_term = st.text_input("Search", placeholder="Name or phone", key="lead_search")

    # === BUILD QUERY ===
    query_params = f"company_id={st.session_state.company_id}&limit={limit}"
    if status_filter != "All":
        query_params += f"&status={status_filter}"
    if source_filter != "All":
        query_params += f"&source={source_filter}"
    if search_term:
        query_params += f"&search={search_term}"

    # === FETCH LEADS ===
    leads_resp = api_get(f"leads?{query_params}")
    if not leads_resp or not leads_resp.get('success') or not leads_resp.get('data'):
        st.warning("No leads found")
        return
    leads = leads_resp['data']

    # === EXPORT BUTTON ===
    if st.button("Export to CSV", key="export_csv_main"):
        try:
            response = requests.get(f"{API_BASE_URL}/leads/export/csv?company_id={st.session_state.company_id}")
            response.raise_for_status()
            st.download_button(
                label="Download CSV",
                data=response.content,
                file_name=f"leads_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"Export failed: {e}")

    st.divider()

    # === DISPLAY LEADS AS CARDS (FIXED BUTTON) ===
    for lead in leads:
        lead_id = lead['id']
        btn_key = f"view_profile_btn_{lead_id}"  # Unique key

        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"**{lead.get('name', 'Unknown')}** - {lead['phone_number']}")
            st.caption(f"Status: **{lead['lead_status']}** | Source: {lead.get('lead_source', 'N/A')} | Interest: {lead.get('interest_level', 0)}/10")
        with col2:
            # CRITICAL: Use `st.session_state` + immediate `st.rerun()`
            if st.button("View Profile", key=btn_key):
                st.session_state.selected_lead_id = lead_id
                st.session_state.page = 'lead_detail'
                st.rerun()  # This MUST be here

        st.divider()






# ==================== PAGE: LEAD DETAIL ====================
def page_lead_detail():
    # ---- 1. Safety check -------------------------------------------------
    if 'selected_lead_id' not in st.session_state or not st.session_state.selected_lead_id:
        st.warning("No lead selected")
        if st.button("Back to Leads"):
            st.session_state.page = 'leads'
            st.rerun()
        return

    lead_id = st.session_state.selected_lead_id

    # ---- 2. Fetch lead ---------------------------------------------------
    lead_resp = api_get(f"leads/{lead_id}")
    if not lead_resp or not lead_resp.get('success'):
        st.error("Lead not found or API error")
        st.session_state.selected_lead_id = None
        return

    lead = lead_resp['data']

    # ---- 3. Header -------------------------------------------------------
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.title(f"Lead: {lead.get('name', 'Unknown')}")
    with col_h2:
        if st.button("Back to Leads"):
            st.session_state.selected_lead_id = None
            st.session_state.page = 'leads'
            st.rerun()

    # ---- 4. Tabs ---------------------------------------------------------
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Overview",
        "WhatsApp Chat",
        "Call History",
        "Analytics",
        "Edit"
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

def render_lead_overview(lead: dict):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Basic Info")
        st.write(f"**ID:** {lead.get('id')}")
        st.write(f"**Phone:** {lead.get('phone_number')}")
        st.write(f"**Email:** {lead.get('email', '—')}")
        st.write(f"**Status:** {lead.get('lead_status', '—')}")
        st.write(f"**Interest:** {lead.get('interest_level', 0)} / 10")
        st.write(f"**Source:** {lead.get('lead_source', '—')}")
        tags = lead.get('tags') or []
        st.write(f"**Tags:** {', '.join(tags) if tags else '—'}")

    with col2:
        st.markdown("### Custom Fields")
        st.write(f"**Chess Rating:** {lead.get('chess_rating', '—')}")
        st.write(f"**Location:** {lead.get('location', '—')}")
        st.write(f"**Availability:** {lead.get('availability', '—')}")
        last = lead.get('last_contacted', '')
        st.write(f"**Last Contact:** {last[:10] if last else 'Never'}")

    # ---- Custom fields from separate endpoint ---------------------------
    cf_resp = api_get(f"leads/{lead['id']}/custom-fields")
    if cf_resp and cf_resp.get('success') and cf_resp.get('data'):
        st.markdown("### Additional Custom Fields")
        for key, val in cf_resp['data'].items():
            label = val.get('label', key)
            value = val.get('value', '—')
            st.write(f"**{label}:** {value}")

    st.divider()
    st.markdown("### Quick Actions")
    qa1, qa2, qa3 = st.columns(3)
    with qa1:
        if st.button("Make Call", use_container_width=True):
            st.session_state.selected_lead_for_call = lead
            st.session_state.page = 'calling'
            st.rerun()
    with qa2:
        if st.button("Send WhatsApp", use_container_width=True):
            st.session_state.selected_lead_for_whatsapp = lead
            st.session_state.page = 'whatsapp'
            st.rerun()
    with qa3:
        if st.button("Schedule Call", use_container_width=True):
            st.session_state.selected_lead_for_schedule = lead
            st.session_state.page = 'scheduled_calls'
            st.rerun()

def render_whatsapp_conversation(lead: dict):
    phone = lead['phone_number']
    st.markdown("### WhatsApp Conversation")

    # ---- Summary & Sentiment -------------------------------------------
    conv_resp = api_get(f"conversations/{phone}")
    if conv_resp and conv_resp.get('success'):
        conv = conv_resp['data']
        summary = conv.get('ai_summary')
        sentiment = conv.get('sentiment') or {}

        c1, c2 = st.columns(2)
        with c1:
            if summary:
                st.info(summary)
            else:
                if st.button("Generate AI Summary"):
                    with st.spinner("Summarising…"):
                        r = api_post(f"conversations/{phone}/summarize", {})
                        if r and r.get('success'):
                            st.success("Summary generated")
                            st.rerun()
        with c2:
            s = sentiment.get('sentiment', 'neutral') if isinstance(sentiment, dict) else 'neutral'
            tone = sentiment.get('tone_score', 5) if isinstance(sentiment, dict) else 5
            st.markdown(f"**Sentiment:** <span class='sentiment-{s}'>{s.upper()}</span>", unsafe_allow_html=True)
            st.progress(tone / 10)
            st.caption(f"Tone Score: {tone}/10")

    # ---- Messages -------------------------------------------------------
    msg_resp = api_get(f"conversations/{phone}/messages?limit=200")
    if msg_resp and msg_resp.get('success') and msg_resp.get('data'):
        for msg in reversed(msg_resp['data']):
            ts = msg.get('timestamp', '')[:19] if msg.get('timestamp') else ''
            body = msg.get('message_body', '')
            user = msg.get('is_from_user', False)

            if user:
                st.markdown(
                    f"<div class='conversation-user'><small>{ts}</small><br><strong>User:</strong> {body}</div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"<div class='conversation-bot'><small>{ts}</small><br><strong>AI:</strong> {body}</div>",
                    unsafe_allow_html=True,
                )
    else:
        st.info("No messages yet")

def render_call_history(lead: dict):
    st.markdown("### Call History")
    calls_resp = api_get(f"call-logs/lead/{lead['id']}")
    if not calls_resp or not calls_resp.get('success') or not calls_resp.get('data'):
        st.info("No calls yet")
        return

    calls = calls_resp['data']

    # ---- Summary metrics ------------------------------------------------
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Total Calls", len(calls))
    with c2: st.metric("Completed", len([c for c in calls if c['call_status'] == 'completed']))
    with c3: st.metric("Failed", len([c for c in calls if c['call_status'] == 'failed']))
    with c4:
        avg = sum(c.get('call_duration', 0) for c in calls) / len(calls) if calls else 0
        st.metric("Avg Duration", f"{int(avg)} s")

    st.divider()

    # ---- Individual call cards -----------------------------------------
    for call in calls:
        sid = call['call_sid']
        with st.expander(f"{call['call_type'].title()} – {call['call_status']} – {call['created_at'][:19]}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**SID:** {sid[:20]}…")
                st.write(f"**Type:** {call['call_type']}")
                st.write(f"**Status:** {call['call_status']}")
                st.write(f"**Duration:** {call.get('call_duration', 0)} s")
            with col2:
                # Sentiment
                sent = call.get('sentiment')
                if sent:
                    if isinstance(sent, str):
                        sent = json.loads(sent)
                    s = sent.get('sentiment', 'neutral')
                    tone = sent.get('tone_score', 5)
                    st.markdown(f"**Sentiment:** <span class='sentiment-{s}'>{s.upper()}</span>", unsafe_allow_html=True)
                    st.write(f"**Tone:** {tone}/10")

            # Summary
            summary = call.get('summary')
            if summary:
                if isinstance(summary, str):
                    summary = json.loads(summary)
                st.markdown("**AI Summary**")
                st.info(summary.get('summary', '—'))
                if summary.get('intent'):
                    st.write(f"**Intent:** {summary['intent']}")

            # Transcript
            if call.get('transcript'):
                st.text_area("Transcript", call['transcript'], height=150, key=f"tr_{sid}")

            # Recording
            if call.get('recording_url'):
                st.markdown(f"[Listen to recording]({call['recording_url']})")

def render_lead_analytics(lead: dict):
    st.markdown("### Lead Analytics")

    # ---- Sentiment trend ------------------------------------------------
    calls_resp = api_get(f"call-logs/lead/{lead['id']}")
    if calls_resp and calls_resp.get('success') and calls_resp.get('data'):
        rows = []
        for c in calls_resp['data']:
            sent = c.get('sentiment')
            if sent:
                if isinstance(sent, str):
                    sent = json.loads(sent)
                rows.append({
                    "date": c['created_at'][:10],
                    "tone": sent.get('tone_score', 5),
                    "sentiment": sent.get('sentiment', 'neutral')
                })
        if rows:
            df = pd.DataFrame(rows)
            st.subheader("Tone Trend")
            fig = px.line(df, x='date', y='tone', markers=True, title="Tone Score Over Time")
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Sentiment Distribution")
            cnt = df['sentiment'].value_counts().reset_index()
            cnt.columns = ['sentiment', 'count']
            fig2 = px.pie(cnt, names='sentiment', values='count')
            st.plotly_chart(fig2, use_container_width=True)

    # ---- Engagement metrics --------------------------------------------
    st.subheader("Engagement")
    msg_resp = api_get(f"conversations/{lead['phone_number']}/messages?limit=1000")
    msgs = len(msg_resp['data']) if msg_resp and msg_resp.get('success') else 0
    calls = len(calls_resp['data']) if calls_resp and calls_resp.get('success') else 0
    col_e1, col_e2, col_e3 = st.columns(3)
    with col_e1: st.metric("WhatsApp Messages", msgs)
    with col_e2: st.metric("Calls", calls)
    with col_e3: st.metric("Interest Level", f"{lead.get('interest_level', 0)} / 10")


def render_lead_edit(lead: dict):
    st.markdown("### Edit Lead")
    with st.form("edit_lead_form"):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Name", value=lead.get('name', ''))
            email = st.text_input("Email", value=lead.get('email', ''))
            status = st.selectbox(
                "Status",
                ["new", "contacted", "qualified", "lost"],
                index=["new", "contacted", "qualified", "lost"].index(lead.get('lead_status', 'new'))
            )
            interest = st.slider("Interest Level", 1, 10, lead.get('interest_level', 5))
        with c2:
            location = st.text_input("Location", value=lead.get('location', ''))
            rating = st.text_input("Chess Rating", value=lead.get('chess_rating', ''))
            avail = st.text_input("Availability", value=lead.get('availability', ''))

        notes = st.text_area("Notes", value=lead.get('notes', ''), height=100)
        tags = st.text_input(
            "Tags (comma separated)",
            value=', '.join(lead.get('tags', [])) if lead.get('tags') else ''
        )

        if st.form_submit_button("Update Lead", use_container_width=True):
            payload = {
                "name": name,
                "email": email or None,
                "lead_status": status,
                "interest_level": interest,
                "location": location or None,
                "chess_rating": rating or None,
                "availability": avail or None,
                "notes": notes or None,
                "tags": [t.strip() for t in tags.split(',') if t.strip()] or None
            }
            r = api_patch(f"leads/{lead['id']}", payload)
            if r and r.get('success'):
                st.success("Lead updated")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Update failed")

# ==================== PAGE: AI AGENTS ====================
def page_agents():
    st.title("🤖 AI Agent Management")
    
    tab1, tab2 = st.tabs(["My Agents", "Create New Agent"])
    
    with tab1:
        agents_resp = api_get(f"agent-instances/company/{st.session_state.company_id}")
        
        if not agents_resp or not agents_resp.get('success'):
            st.info("No agents configured yet")
        else:
            for agent in agents_resp['data']:
                with st.expander(f"🤖 {agent['agent_name']} ({agent['agent_type']})"):
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
                    
                    # Agent performance stats
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
                    
                    if agent.get('custom_prompt'):
                        with st.expander("View Custom Prompt"):
                            st.text_area("Prompt", value=agent['custom_prompt'], height=200, key=f"prompt_{agent['id']}")
                    
                    # WhatsApp Credentials Setup
                    if agent['agent_type'] == 'whatsapp':
                        st.divider()
                        st.markdown("### 🔧 WhatsApp Setup")
                        
                        if agent.get('whatsapp_credentials'):
                            st.success("✅ WhatsApp credentials configured")
                            st.info(f"**Webhook URL:** {API_BASE_URL.replace('/api', '')}/api/webhooks/whatsapp-universal")
                            if agent.get('webhook_verify_token'):
                                st.info(f"**Verify Token:** {agent['webhook_verify_token']}")
                        else:
                            st.warning("⚠️ WhatsApp credentials not configured")
                            
                            with st.form(f"whatsapp_creds_{agent['id']}"):
                                st.markdown("**Meta WhatsApp Business API Credentials:**")
                                access_token = st.text_input("Access Token*", type="password")
                                phone_number_id = st.text_input("Phone Number ID*")
                                business_account_id = st.text_input("Business Account ID")
                                
                                if st.form_submit_button("Save Credentials"):
                                    creds_data = {
                                        "access_token": access_token,
                                        "phone_number_id": phone_number_id,
                                        "business_account_id": business_account_id
                                    }
                                    
                                    result = api_post(f"agent-instances/{agent['id']}/whatsapp-credentials", creds_data)
                                    
                                    if result and result.get('success'):
                                        st.success("✅ Credentials saved!")
                                        st.info(f"**Webhook URL:** {result.get('webhook_url')}")
                                        st.info(f"**Verify Token:** {result.get('verify_token')}")
                                        st.rerun()
                                    else:
                                        st.error("Failed to save credentials")
                    
                    # Delete agent
                    st.divider()
                    if st.button(f"🗑️ Delete Agent", key=f"delete_{agent['id']}"):
                        if st.checkbox(f"Confirm deletion of {agent['agent_name']}", key=f"confirm_{agent['id']}"):
                            result = api_delete(f"agent-instances/{agent['id']}")
                            if result and result.get('success'):
                                st.success("Agent deleted!")
                                st.rerun()
    
    with tab2:
        st.subheader("Create New AI Agent")
        
        with st.form("create_agent"):
            agent_name = st.text_input("Agent Name*", placeholder="Chess Coach AI")
            agent_type = st.selectbox("Type*", ["voice", "whatsapp"])
            
            col1, col2 = st.columns(2)
            
            with col1:
                phone_number = st.text_input("Phone Number", placeholder="+919876543210")
            
            with col2:
                whatsapp_number = st.text_input("WhatsApp Number", placeholder="+919876543210")
            
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
                    "phone_number": phone_number if phone_number else None,
                    "whatsapp_number": whatsapp_number if whatsapp_number else None,
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
            
            # Schedule option
            schedule_call = st.checkbox("Schedule this call instead of calling now")
            
            if schedule_call:
                scheduled_date = st.date_input("Schedule Date", value=datetime.now() + timedelta(days=1))
                scheduled_time = st.time_input("Schedule Time")
            
            submitted = st.form_submit_button("📞 Make Call Now" if not schedule_call else "📅 Schedule Call")
            
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
                
                if schedule_call:
                    scheduled_datetime = datetime.combine(scheduled_date, scheduled_time).isoformat()
                    schedule_data = {
                        "company_id": st.session_state.company_id,
                        "lead_id": lead_id,
                        "call_type": call_type,
                        "scheduled_time": scheduled_datetime,
                        "to_phone": to_phone,
                        "name": name
                    }
                    result = api_post("schedule-call", schedule_data)
                    if result and result.get('success'):
                        st.success(f"✅ Call scheduled for {scheduled_datetime}!")
                        if 'selected_lead_for_call' in st.session_state:
                            del st.session_state.selected_lead_for_call
                    else:
                        st.error("Failed to schedule call")
                else:
                    if agent_instance_id:
                        result = python_api_post(f"outbound-call-agent?agent_instance_id={agent_instance_id}", data)
                    else:
                        result = python_api_post("outbound-call", data)
                    
                    if result and result.get('success'):
                        st.success(f"✅ Call initiated! SID: {result.get('call_sid')}")
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

# ==================== PAGE: SCHEDULED CALLS ====================
def page_scheduled_calls():
    st.title("📅 Scheduled Calls Management")
    
    tab1, tab2, tab3 = st.tabs(["View Scheduled", "Schedule New Call", "Bulk Schedule"])
    
    with tab1:
        st.subheader("Upcoming Scheduled Calls")
        
        # Get scheduled calls
        scheduled_resp = api_get(f"scheduled-calls/pending?company_id={st.session_state.company_id}")
        
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
                        col_edit1, col_edit2, col_edit3, col_edit4 = st.columns(4)
                        
                        with col_edit1:
                            # Reschedule
                            with st.form(f"reschedule_{call['id']}"):
                                new_time = st.datetime_input("New Time", value=datetime.fromisoformat(call['scheduled_time']))
                                
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
                            # Change Lead
                            with st.form(f"change_lead_{call['id']}"):
                                new_lead_id = st.number_input("New Lead ID", min_value=1, value=call['lead_id'])
                                
                                if st.form_submit_button("Change Lead"):
                                    result = api_patch(f"scheduled-calls/{call['id']}", {"lead_id": new_lead_id})
                                    if result and result.get('success'):
                                        st.success("Lead changed!")
                                        st.rerun()
                        
                        with col_edit3:
                            # Cancel
                            if st.button(f"❌ Cancel", key=f"cancel_{call['id']}"):
                                result = api_patch(f"scheduled-calls/{call['id']}", {"status": "cancelled"})
                                if result and result.get('success'):
                                    st.success("Call cancelled!")
                                    st.rerun()
                        
                        with col_edit4:
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
                    "scheduled_time": scheduled_datetime,
                    "notes": notes
                }
                
                result = api_post("schedule-call", data)
                
                if result and result.get('success'):
                    st.success(f"✅ Call scheduled for {scheduled_datetime}!")
                    if 'selected_lead_for_schedule' in st.session_state:
                        del st.session_state.selected_lead_for_schedule
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Failed to schedule call")
    
    with tab3:
        st.subheader("Bulk Schedule Calls")
        
        with st.form("bulk_schedule_form"):
            call_type = st.selectbox("Call Type", ["qualification", "reminder", "payment"], key="bulk_call_type")
            
            # Lead selection
            leads_resp = api_get(f"leads?company_id={st.session_state.company_id}&limit=200")
            lead_options = {}
            if leads_resp and leads_resp.get('success'):
                lead_options = {f"{l['name']} ({l['phone_number']})": l['id'] for l in leads_resp['data']}
            
            selected_leads = st.multiselect("Select Leads", list(lead_options.keys()))
            
            # Schedule options
            schedule_date = st.date_input("Schedule Date", value=datetime.now() + timedelta(days=1))
            start_time = st.time_input("Start Time")
            end_time = st.time_input("End Time")
            interval_minutes = st.number_input("Interval (minutes)", min_value=5, value=15)
            
            if st.form_submit_button("Schedule Bulk Calls"):
                if not selected_leads:
                    st.error("Please select at least one lead")
                    return
                
                start_dt = datetime.combine(schedule_date, start_time)
                end_dt = datetime.combine(schedule_date, end_time)
                current_time = start_dt
                
                success_count = 0
                for lead_name in selected_leads:
                    if current_time > end_dt:
                        break
                        
                    lead_id = lead_options[lead_name]
                    lead = next((l for l in leads_resp['data'] if l['id'] == lead_id), None)
                    
                    data = {
                        "company_id": st.session_state.company_id,
                        "lead_id": lead_id,
                        "call_type": call_type,
                        "scheduled_time": current_time.isoformat(),
                        "to_phone": lead['phone_number'],
                        "name": lead['name']
                    }
                    
                    result = api_post("schedule-call", data)
                    if result and result.get('success'):
                        success_count += 1
                    
                    current_time += timedelta(minutes=interval_minutes)
                
                st.success(f"✅ Scheduled {success_count} calls!")
                st.info(f"Calls scheduled from {start_dt.strftime('%H:%M')} to {current_time.strftime('%H:%M')}")
                time.sleep(2)
                st.rerun()

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
            
            # Resend failed option
            resend_failed = st.checkbox("Resend to failed numbers only")
            
            submitted_bulk = st.form_submit_button("Send Bulk Messages")
            
            if submitted_bulk:
                if not selected_leads or not bulk_message:
                    st.error("Please select leads and enter message!")
                    return
                
                messages = []
                for lead_name in selected_leads:
                    phone = lead_options[lead_name]
                    if resend_failed:
                        # Check if last message failed
                        msg_resp = api_get(f"whatsapp/messages/last?phone={phone}")
                        if msg_resp and msg_resp.get('success') and msg_resp.get('data'):
                            last_msg = msg_resp['data']
                            if last_msg.get('status') == 'failed':
                                messages.append({"to": phone, "message": bulk_message})
                    else:
                        messages.append({"to": phone, "message": bulk_message})
                
                if not messages:
                    st.info("No failed messages to resend")
                    return
                
                result = api_post("whatsapp/send-bulk", {
                    "agent_instance_id": agent_id_bulk,
                    "messages": messages
                })
                
                if result and result.get('success'):
                    st.success(f"✅ Sent to {result.get('sent', 0)} leads!")
                    if result.get('errors'):
                        st.warning(f"Failed to send to {len(result['errors'])} leads")
                        if st.button("View Failed Numbers"):
                            st.json(result['errors'])
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
            
            scheduled_start = st.date_input("Start Date",
                value=datetime.now() + timedelta(days=1))
            start_time = st.time_input("Start Time", value=datetime.now().time())
            
            message_template = st.text_area("WhatsApp Message Template (Optional)", 
                height=100, placeholder="Hi {{name}}, we're excited about your interest in chess coaching...")
            
            if st.form_submit_button("Create Campaign", use_container_width=True):
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
    
    with tab2:
        st.subheader("Add New Human Agent")
        
        with st.form("add_human_agent"):
            name = st.text_input("Name*", placeholder="Sarah Johnson")
            email = st.text_input("Email*", placeholder="sarah@company.com")
            phone = st.text_input("Phone", placeholder="+919876543210")
            role = st.selectbox("Role", ["sales", "support", "manager"])
            expertise = st.multiselect("Expertise", 
                ["chess_coaching", "premium_packages", "kids_program", "adult_training"])
            max_concurrent = st.number_input("Max Concurrent Leads", min_value=1, max_value=50, value=10)
            
            if st.form_submit_button("Add Agent"):
                if not name or not email:
                    st.error("Name and email are required!")
                    return
                
                data = {
                    "company_id": st.session_state.company_id,
                    "name": name,
                    "email": email,
                    "phone": phone if phone else None,
                    "role": role,
                    "expertise": expertise,
                    "max_concurrent_leads": max_concurrent,
                    "status": "available"
                }
                
                result = api_post("human-agents", data)
                if result and result.get('success'):
                    st.success(f"✅ Human agent {name} added!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Failed to add agent")
    
    with tab3:
        st.subheader("🔥 Takeover Requests")
        
        takeover_resp = api_get(f"takeover-requests?company_id={st.session_state.company_id}&status=pending")
        
        if takeover_resp and takeover_resp.get('success') and takeover_resp.get('data'):
            for request in takeover_resp['data']:
                with st.expander(f"🔥 {request.get('lead_name', 'Unknown')} - {request['trigger_reason']}"):
                    st.write(f"**Lead ID:** {request['lead_id']}")
                    st.write(f"**Phone:** {request['phone_number']}")
                    st.write(f"**Reason:** {request['trigger_reason']}")
                    st.write(f"**Requested:** {request['created_at'][:16]}")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("Assign to Me", key=f"assign_{request['id']}"):
                            # Assign to current user
                            result = api_patch(f"takeover-requests/{request['id']}", {
                                "status": "assigned",
                                "assigned_agent_id": st.session_state.user_role  # In real app, use user ID
                            })
                            if result and result.get('success'):
                                st.success("Lead assigned to you!")
                                st.rerun()
                    
                    with col2:
                        if st.button("Dismiss", key=f"dismiss_{request['id']}"):
                            result = api_patch(f"takeover-requests/{request['id']}", {"status": "dismissed"})
                            if result and result.get('success'):
                                st.success("Request dismissed")
                                st.rerun()
        else:
            st.info("No pending takeover requests")

# ==================== PAGE: ANALYTICS ====================
def page_analytics():
    st.title("📈 Analytics & Reports")
    
    tab1, tab2 = st.tabs(["Call Analytics", "Lead Analytics"])
    
    with tab1:
        st.subheader("📞 Call Performance")
        
        metrics_resp = api_get("metrics/dashboard")
        if metrics_resp and metrics_resp.get('success'):
            data = metrics_resp['data']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Active Calls", data.get('active_calls', 0))
            with col2:
                calls_24h = data.get('calls_24h', [])
                total_calls = sum([c.get('count', 0) for c in calls_24h]) if calls_24h else 0
                st.metric("Calls (24h)", total_calls)
            with col3:
                st.metric("Success Rate", f"{data.get('success_rate', 0)}%")
            
            # Sentiment distribution
            sentiment_data = data.get('sentiment_distribution', [])
            if sentiment_data:
                st.subheader("😊 Sentiment Distribution")
                df = pd.DataFrame(sentiment_data)
                fig = px.bar(df, x='sentiment_type', y='count', color='sentiment_type')
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("👥 Lead Analytics")
        
        lead_stats_resp = api_get("stats/leads")
        if lead_stats_resp and lead_stats_resp.get('success'):
            df = pd.DataFrame(lead_stats_resp['data'])
            
            if not df.empty:

                df['count'] = pd.to_numeric(df['count'], errors='coerce')
                df['avg_interest'] = pd.to_numeric(df['avg_interest'], errors='coerce')


                fig = px.bar(df, x='lead_status', y='count', color='lead_status',
                            title="Leads by Status")
                st.plotly_chart(fig, use_container_width=True)
                
                # Average interest by status
                fig2 = px.scatter(
                    df, x='lead_status', y='avg_interest', size='count',
                    title="Average Interest Level by Status"
                )
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("No lead data available yet")
        else:
            st.info("Unable to load lead analytics")

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

# ==================== PAGE: SETTINGS ====================
def page_settings():
    st.title("⚙️ Settings & Configuration")
    
    tab1, tab2, tab3 = st.tabs(["Company Info", "Custom Fields", "Integrations"])
    
    with tab1:
        st.subheader("🏢 Company Information")
        
        company_resp = api_get(f"companies/{st.session_state.company_id}")
        if company_resp and company_resp.get('success'):
            company = company_resp['data']
            
            with st.form("update_company"):
                name = st.text_input("Company Name", value=company.get('name', ''))
                phone = st.text_input("Phone Number", value=company.get('phone_number', ''))
                
                if st.form_submit_button("Update Company"):
                    st.info("Company update feature coming soon")
        
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
        st.subheader("🔧 Custom Field Templates")
        
        templates_resp = api_get("extraction-templates")
        
        if templates_resp and templates_resp.get('success'):
            for template in templates_resp['data']:
                with st.expander(f"📋 {template['template_name']} ({template['industry']})"):
                    st.write(f"**Description:** {template['description']}")
                    
                    fields = template['field_definitions'].get('fields', [])
                    st.write(f"**Fields:** {len(fields)}")
                    
                    if st.button(f"Apply to Company", key=f"template_{template['id']}"):
                        result = api_post(f"companies/{st.session_state.company_id}/apply-template", {
                            "template_id": template['id']
                        })
                        if result and result.get('success'):
                            st.success(f"✅ Applied {len(result['data'])} field definitions!")
                            st.rerun()
        
        st.divider()
        
        st.subheader("Create Custom Field")
        with st.form("custom_field"):
            field_key = st.text_input("Field Key", placeholder="chess_rating")
            field_label = st.text_input("Field Label", placeholder="Chess Rating")
            field_type = st.selectbox("Field Type", ["text", "number", "date", "email", "select"])
            field_category = st.selectbox("Category", ["personal", "qualification", "preference"])
            
            if st.form_submit_button("Create Field"):
                result = api_post("custom-fields", {
                    "company_id": st.session_state.company_id,
                    "field_key": field_key,
                    "field_label": field_label,
                    "field_type": field_type,
                    "field_category": field_category
                })
                if result and result.get('success'):
                    st.success("✅ Custom field created!")
                else:
                    st.error("Failed to create field")
    
    with tab3:
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

# ==================== LOGIN PAGE ====================
def page_login():
    st.title("🔐 Login to AI Sales CRM")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login"):
            st.markdown("### Sign In")
            
            # For demo purposes, we'll use company selection
            # In production, implement proper authentication
            
            companies_resp = api_get("companies")
            
            if companies_resp and companies_resp.get('success'):
                company_options = {f"{c['name']} (ID: {c['id']})": c for c in companies_resp['data']}
                
                if company_options:
                    selected = st.selectbox("Select Company", list(company_options.keys()))
                    selected_company = company_options[selected]
                    
                    username = st.text_input("Username")
                    password = st.text_input("Password", type="password")
                    
                    if st.form_submit_button("Login"):
                        # Simple demo login - in production use proper auth
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

    # CRITICAL: Reset selected_lead_id when going back to leads
    if st.session_state.page == 'leads':
        st.session_state.selected_lead_id = None
    
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