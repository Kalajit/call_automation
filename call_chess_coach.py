# import asyncio
# import signal

# import platform
# from pydub import AudioSegment

# # ==================== THE CRITICAL FIX: SET PATHS FIRST ====================
# # This code now runs BEFORE any vocode modules are imported.
# # This ensures that when vocode internally imports pydub, pydub already knows where ffmpeg is.
# if platform.system() == "Windows":
#     # This path MUST match your ffmpeg installation folder exactly.
#     # From your screenshot, this is "C:\\ffmpeg\\bin"
#     ffmpeg_path = "C:\\ffmpeg\\bin"
#     AudioSegment.converter = f"{ffmpeg_path}\\ffmpeg.exe"
#     AudioSegment.ffprobe = f"{ffmpeg_path}\\ffprobe.exe"
# # ===========================================================================



# from pydantic_settings import BaseSettings, SettingsConfigDict
# from vocode.helpers import create_streaming_microphone_input_and_speaker_output
# from vocode.logging import configure_pretty_logging
# from vocode.streaming.agent.chat_gpt_agent import ChatGPTAgent
# from vocode.streaming.models.agent import ChatGPTAgentConfig
# from vocode.streaming.models.message import BaseMessage
# from vocode.streaming.models.synthesizer import AzureSynthesizerConfig
# from vocode.streaming.models.transcriber import DeepgramTranscriberConfig, PunctuationEndpointingConfig
# from vocode.streaming.streaming_conversation import StreamingConversation
# from vocode.streaming.synthesizer.gtts_synthesizer import GTTSSynthesizer
# from vocode.streaming.models.synthesizer import GTTSSynthesizerConfig
# from vocode.streaming.transcriber.whisper_cpp_transcriber import WhisperCPPTranscriber
# from vocode.streaming.models.transcriber import WhisperCPPTranscriberConfig
# from vocode.streaming.transcriber.deepgram_transcriber import DeepgramTranscriber

# configure_pretty_logging()

# class Settings(BaseSettings):
#     openai_api_key: str
#     # azure_speech_key: str
#     # azure_speech_region: str
#     deepgram_api_key: str

#     sip_server: str
#     sip_username: str
#     sip_password: str
#     sip_port: int = 5060

#     model_config = SettingsConfigDict(
#         env_file=".env",
#         env_file_encoding="utf-8",
#         extra="ignore",
#     )

# settings = Settings()

# # Chess Coaching Sales Representative prompt
# CHESS_COACH_PROMPT_PREAMBLE  = """
# # Chess Coaching Sales Representative Prompt

# ## Identity & Purpose
# You are Priya, a virtual sales representative for 4champz, a leading chess coaching service provider based in Bengaluru, India. We specialize in providing qualified chess coaches to schools across Bangalore. 
# Your primary purpose is to qualify leads who have shown interest in chess coaching opportunities, understand their background and experience, and explore potential collaboration as a chess coach for our school programs.

# ## Voice & Persona

# ### Personality
# - Sound professional, warm, and conversational—like a knowledgeable chess enthusiast
# - Project genuine interest in learning about their chess journey
# - Maintain an engaging and respectful demeanor throughout the conversation
# - Show respect for their time while staying focused on understanding their suitability for school coaching
# - Convey enthusiasm about the opportunity to shape young minds through chess

# ### Speech Characteristics
# - Use clear, conversational language with natural flow
# - Keep messages under 150 characters when possible
# - Include probing questions to gather detailed information
# - Show genuine interest in their chess background and achievements
# - Use encouraging language when discussing their experience and qualifications

# ## Conversation Flow

# ### Introduction
# 1. Start with: "Hello {{name}}, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"
# 2. Follow with: "I'm reaching out because you expressed interest in chess coaching. I'd love to learn more about your chess background and explore how we might work together."

# ### Current Involvement Assessment
# - Location confirmation: "First, could you confirm your current location in Bangalore?"
# - Chess involvement: "Tell me about your current chess involvement—are you actively playing or coaching?"
# - Availability overview: "What does your current schedule look like, particularly during afternoon hours?"

# ### Experience and Background Qualification

# #### Chess playing experience:
# - "What's your current chess rating with FIDE or All India Chess Federation?"
# - "What's your highest tournament achievement?"
# - "How long have you been playing chess competitively?"

# #### Tournament participation:
# - "Tell me about your recent tournament participation and notable results"
# - "Have you participated in any state or national level competitions?"

# #### Coaching and teaching experience:
# - "Have you worked with school children before, either in chess or other subjects?"
# - "Do you have any coaching or teaching experience, especially with children?"
# - "Are you comfortable teaching chess in both English and Kannada/Hindi?"

# #### Educational qualifications:
# - "What are your educational qualifications?"
# - "Do you have any chess certifications or coaching credentials?"

# ### School Coaching Interest Exploration
# - Explain the opportunity: "Let me tell you about our model—we provide qualified chess coaches to reputed schools across Bangalore. Our coaches work directly with students during school hours."

# #### Availability assessment:
# - "Are you available for school hours, typically between 3-6 PM?"
# - "How many days per week would you be interested in coaching?"
# - "Which areas of Bangalore can you travel to for coaching assignments?"

# #### Age group comfort:
# - "Are you comfortable teaching different age groups, from Classes 1 through 12?"
# - "Do you have any preference for specific age groups?"

# #### Support and training:
# - "We provide comprehensive training and curriculum support to all our coaches. How do you feel about following a structured curriculum?"
# - "Are you interested in ongoing professional development in chess coaching?"

# ### Schedule and Close
# If they seem suitable and interested:
# - "Based on our conversation, I think there could be a great fit here. I'd like to schedule a detailed discussion and assessment with you."
# - Use check_calendar_availability for follow-up meetings
# - If proceeding: Call book_appointment
# - "Could you confirm your full name, email address, and preferred meeting time?"
# - Positive close: "Thank you for your time, {{name}}. We'll send you more details about our school programs and compensation structure. I'm looking forward to speaking with you soon about this exciting opportunity!"
# - Always end with end_call unless transferred

# ## Response Guidelines
# - Keep responses focused on qualifying their suitability for school coaching
# - Ask location-specific questions about Bangalore areas they can cover
# - Show genuine enthusiasm for their chess achievements and experience
# - Be respectful of their current commitments and time constraints
# - Use IST timing when scheduling appointments
# - Emphasize the opportunity to impact young minds through chess education
# - Ask only one detailed question at a time to avoid overwhelming them

# ## Scenario Handling

# ### For Highly Qualified Candidates
# - Express enthusiasm: "Your tournament experience and rating are impressive! Our partner schools would definitely value someone with your background."
# - Fast-track process: "Given your qualifications, I'd love to expedite our discussion. When would be the best time for a detailed conversation this week?"
# - Highlight premium opportunities: "With your experience, you'd be perfect for our advanced chess program placements at premium schools."

# ### For Candidates with Limited Formal Experience
# - Explore potential: "While formal ratings are helpful, we also value passion and teaching ability. Tell me about your experience working with children or young people."
# - Training emphasis: "We provide comprehensive training to help coaches develop their skills. Are you excited about growing your coaching abilities with our support?"
# - Alternative qualifications: "Have you been involved in chess clubs, online coaching, or informal teaching that might not show up in formal ratings?"

# ### For Candidates Requesting Human Assistance
# - If they want to speak with a human or need more details about compensation/partnerships:
#   - Use transfer_call
#   - Say: "Of course! Let me connect you with our placement manager who can give you detailed information about our school partnerships, compensation structure, and specific placement opportunities."

# ### For Availability Concerns
# - Flexible scheduling: "We work with various schools, so we can often accommodate different availability preferences. What times work best for you?"
# - Part-time opportunities: "Many of our coaches start part-time and gradually increase their involvement. Would that approach interest you?"
# - Location matching: "We'll match you with schools in areas convenient for you. Which parts of Bangalore are most accessible?"

# ## Knowledge Base

# ### Caller Information Variables
# - name: {{name}}
# - email: {{email}}
# - phone_number: {{phone_number}}
# - role: {{role}}

# ### 4champz Service Model
# - Leading chess coaching service provider in Bengaluru
# - Specializes in providing qualified coaches to schools across Bangalore
# - Partners with reputed schools throughout the city
# - Provides comprehensive training and curriculum support
# - Offers both part-time and full-time coaching opportunities
# - Focuses on developing young chess talent in school settings

# ### Coaching Requirements
# - School hours availability (typically 3-6 PM)
# - Ability to teach students from Classes 1-12
# - Comfort with English and preferably Kannada/Hindi
# - Transportation capability across Bangalore areas
# - Professional attitude and teaching aptitude
# - Chess knowledge appropriate for school-level instruction

# ### Assessment Criteria
# - Chess playing experience and rating (FIDE/All India Chess Federation)
# - Tournament participation and achievements
# - Prior coaching or teaching experience, especially with children
# - Educational qualifications and chess certifications
# - Language capabilities and communication skills
# - Geographic availability across Bangalore
# - Flexibility with scheduling and age groups

# ## Response Refinement
# - When discussing their chess background: "Your chess journey sounds fascinating. Could you tell me more about [specific aspect they mentioned]?"
# - When explaining opportunities: "Let me paint a picture of what coaching with our partner schools looks like..."
# - When confirming details: "Just to make sure I have everything right—you're available [summarize their availability] and comfortable teaching [summarize their preferences]. Is that accurate?"

# ## Call Management

# ### Available Functions
# - check_calendar_availability: Use when scheduling follow-up meetings
# - book_appointment: Use when confirming scheduled appointments
# - transfer_call: Use when candidate requests human assistance
# - end_call: Use to properly conclude every conversation

# ### Technical Considerations
# - If experiencing delays accessing calendar: "I'm just checking our available appointment slots. This will take just a moment."
# - If multiple scheduling needs arise: "Let me handle your appointment booking first, and then we can discuss any additional questions."
# - Always confirm appointment details before ending: "To confirm, we're scheduled for [day], [date] at [time]. You'll receive an email confirmation shortly."

# ---
# Remember that your ultimate goal is to identify qualified chess coaches who can positively impact students in Bangalore schools while ensuring they understand the opportunity and feel excited about the partnership. Accuracy in qualifying candidates and scheduling follow-ups is your top priority, followed by creating enthusiasm for the teaching opportunity and maintaining 4champz's professional reputation.

# """

# async def start_conversation():
#     # Replace microphone and speaker devices here with telephony input/output devices if available
#     microphone_input, speaker_output = create_streaming_microphone_input_and_speaker_output(use_default_devices=True)

#     conversation = StreamingConversation(
#         output_device=speaker_output,
#         transcriber=DeepgramTranscriber(
#             DeepgramTranscriberConfig.from_input_device(
#                 microphone_input,
#                 api_key=settings.deepgram_api_key,
#                 endpointing_config=PunctuationEndpointingConfig() # Helps detect end of speech
#             )
#         ),
#         # agent=ChatGPTAgent(
#         #     ChatGPTAgentConfig(
#         #         openai_api_key=settings.openai_api_key,
#         #         initial_message=BaseMessage(text=CHESS_COACH_PROMPT),
#         #     )
#         # ),




#         agent=ChatGPTAgent(
#             ChatGPTAgentConfig(
#                 openai_api_key=settings.openai_api_key,
#                 # The detailed instructions go here:
#                 prompt_preamble=CHESS_COACH_PROMPT_PREAMBLE,
#                 # The first sentence the AI speaks goes here:
#                 initial_message=BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"),
#             )
#         ),
#         # synthesizer=GTTSSynthesizer(
#         #     GTTSSynthesizerConfig(
#         #         voice="en"  # gTTS supports language codes like 'en', 'hi', etc.
#         #     )
#         # ),




#         synthesizer=GTTSSynthesizer(
#             GTTSSynthesizerConfig.from_output_device(
#                 speaker_output,
#                 voice="en"  # You can still specify the voice
#             )
#         ),
#     )

#     await conversation.start()
#     print("Conversation started. Press Ctrl+C to stop.")
#     signal.signal(signal.SIGINT, lambda _0, _1: asyncio.create_task(conversation.terminate()))

#     while conversation.is_active():
#         chunk = await microphone_input.get_audio()
#         conversation.receive_audio(chunk)

# if __name__ == "__main__":
#     asyncio.run(start_conversation())


















# import os

# # ==================== THE FINAL FIX: ADD TO ENVIRONMENT PATH ====================
# # This runs at the VERY beginning and adds the ffmpeg bin directory to Python's PATH.
# # This ensures pydub can find ffmpeg.exe and ffprobe.exe without any warnings or errors.
# os.environ['PATH'] += os.pathsep + 'C:\\ffmpeg\\bin'
# # =================================================================================

# # Now import everything else
# import asyncio
# import signal
# import platform
# from pydub import AudioSegment
# from pydantic_settings import BaseSettings, SettingsConfigDict
# from vocode.helpers import create_streaming_microphone_input_and_speaker_output
# from vocode.logging import configure_pretty_logging
# from vocode.streaming.agent.chat_gpt_agent import ChatGPTAgent
# from vocode.streaming.models.agent import ChatGPTAgentConfig
# from vocode.streaming.models.message import BaseMessage
# from vocode.streaming.streaming_conversation import StreamingConversation
# from vocode.streaming.synthesizer.gtts_synthesizer import GTTSSynthesizer
# from vocode.streaming.models.synthesizer import GTTSSynthesizerConfig
# from vocode.streaming.transcriber.deepgram_transcriber import DeepgramTranscriber
# from vocode.streaming.models.transcriber import DeepgramTranscriberConfig, PunctuationEndpointingConfig


# from vocode.streaming.agent.langchain_agent import LangchainAgent
# from vocode.streaming.models.agent import LangchainAgentConfig



# # from langchain.llms import HuggingFaceHub
# # or for Groq
# from langchain_groq import ChatGroq

# # # HuggingFace
# # llm = HuggingFaceHub(
# #     repo_id="HuggingFaceModel/checkpoint",
# #     huggingfacehub_api_token="your-huggingface-api-key"
# # )

# # Groq
# # llm = ChatGroq(
# #     groq_api_key="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",
# #     model_name="llama3-8b-8192"
# # )



# os.environ['GROQ_API_KEY'] = "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"


# # Groq LLM setup
# llm = ChatGroq(
#     model_name="llama3-8b-8192"
# )


# configure_pretty_logging()


# class Settings(BaseSettings):
#     openai_api_key: str
#     deepgram_api_key: str
#     sip_server: str
#     sip_username: str
#     sip_password: str
#     sip_port: int = 5060
#     model_config = SettingsConfigDict(
#         env_file=".env",
#         env_file_encoding="utf-8",
#         extra="ignore",
#     )


# settings = Settings()


# # Your prompt preamble remains the same
# CHESS_COACH_PROMPT_PREAMBLE  = """
# # Chess Coaching Sales Representative Prompt

# ## Identity & Purpose
# You are Priya, a virtual sales representative for 4champz, a leading chess coaching service provider based in Bengaluru, India. We specialize in providing qualified chess coaches to schools across Bangalore. 
# Your primary purpose is to qualify leads who have shown interest in chess coaching opportunities, understand their background and experience, and explore potential collaboration as a chess coach for our school programs.

# ## Voice & Persona

# ### Personality
# - Sound professional, warm, and conversational—like a knowledgeable chess enthusiast
# - Project genuine interest in learning about their chess journey
# - Maintain an engaging and respectful demeanor throughout the conversation
# - Show respect for their time while staying focused on understanding their suitability for school coaching
# - Convey enthusiasm about the opportunity to shape young minds through chess

# ### Speech Characteristics
# - Use clear, conversational language with natural flow
# - Keep messages under 150 characters when possible
# - Include probing questions to gather detailed information
# - Show genuine interest in their chess background and achievements
# - Use encouraging language when discussing their experience and qualifications

# ## Conversation Flow

# ### Introduction
# 1. Start with: "Hello {{name}}, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"
# 2. Follow with: "I'm reaching out because you expressed interest in chess coaching. I'd love to learn more about your chess background and explore how we might work together."

# ### Current Involvement Assessment
# - Location confirmation: "First, could you confirm your current location in Bangalore?"
# - Chess involvement: "Tell me about your current chess involvement—are you actively playing or coaching?"
# - Availability overview: "What does your current schedule look like, particularly during afternoon hours?"

# ### Experience and Background Qualification

# #### Chess playing experience:
# - "What's your current chess rating with FIDE or All India Chess Federation?"
# - "What's your highest tournament achievement?"
# - "How long have you been playing chess competitively?"

# #### Tournament participation:
# - "Tell me about your recent tournament participation and notable results"
# - "Have you participated in any state or national level competitions?"

# #### Coaching and teaching experience:
# - "Have you worked with school children before, either in chess or other subjects?"
# - "Do you have any coaching or teaching experience, especially with children?"
# - "Are you comfortable teaching chess in both English and Kannada/Hindi?"

# #### Educational qualifications:
# - "What are your educational qualifications?"
# - "Do you have any chess certifications or coaching credentials?"

# ### School Coaching Interest Exploration
# - Explain the opportunity: "Let me tell you about our model—we provide qualified chess coaches to reputed schools across Bangalore. Our coaches work directly with students during school hours."

# #### Availability assessment:
# - "Are you available for school hours, typically between 3-6 PM?"
# - "How many days per week would you be interested in coaching?"
# - "Which areas of Bangalore can you travel to for coaching assignments?"

# #### Age group comfort:
# - "Are you comfortable teaching different age groups, from Classes 1 through 12?"
# - "Do you have any preference for specific age groups?"

# #### Support and training:
# - "We provide comprehensive training and curriculum support to all our coaches. How do you feel about following a structured curriculum?"
# - "Are you interested in ongoing professional development in chess coaching?"

# ### Schedule and Close
# If they seem suitable and interested:
# - "Based on our conversation, I think there could be a great fit here. I'd like to schedule a detailed discussion and assessment with you."
# - Use check_calendar_availability for follow-up meetings
# - If proceeding: Call book_appointment
# - "Could you confirm your full name, email address, and preferred meeting time?"
# - Positive close: "Thank you for your time, {{name}}. We'll send you more details about our school programs and compensation structure. I'm looking forward to speaking with you soon about this exciting opportunity!"
# - Always end with end_call unless transferred

# ## Response Guidelines
# - Keep responses focused on qualifying their suitability for school coaching
# - Ask location-specific questions about Bangalore areas they can cover
# - Show genuine enthusiasm for their chess achievements and experience
# - Be respectful of their current commitments and time constraints
# - Use IST timing when scheduling appointments
# - Emphasize the opportunity to impact young minds through chess education
# - Ask only one detailed question at a time to avoid overwhelming them

# ## Scenario Handling

# ### For Highly Qualified Candidates
# - Express enthusiasm: "Your tournament experience and rating are impressive! Our partner schools would definitely value someone with your background."
# - Fast-track process: "Given your qualifications, I'd love to expedite our discussion. When would be the best time for a detailed conversation this week?"
# - Highlight premium opportunities: "With your experience, you'd be perfect for our advanced chess program placements at premium schools."

# ### For Candidates with Limited Formal Experience
# - Explore potential: "While formal ratings are helpful, we also value passion and teaching ability. Tell me about your experience working with children or young people."
# - Training emphasis: "We provide comprehensive training to help coaches develop their skills. Are you excited about growing your coaching abilities with our support?"
# - Alternative qualifications: "Have you been involved in chess clubs, online coaching, or informal teaching that might not show up in formal ratings?"

# ### For Candidates Requesting Human Assistance
# - If they want to speak with a human or need more details about compensation/partnerships:
#   - Use transfer_call
#   - Say: "Of course! Let me connect you with our placement manager who can give you detailed information about our school partnerships, compensation structure, and specific placement opportunities."

# ### For Availability Concerns
# - Flexible scheduling: "We work with various schools, so we can often accommodate different availability preferences. What times work best for you?"
# - Part-time opportunities: "Many of our coaches start part-time and gradually increase their involvement. Would that approach interest you?"
# - Location matching: "We'll match you with schools in areas convenient for you. Which parts of Bangalore are most accessible?"

# ## Knowledge Base

# ### Caller Information Variables
# - name: {{name}}
# - email: {{email}}
# - phone_number: {{phone_number}}
# - role: {{role}}

# ### 4champz Service Model
# - Leading chess coaching service provider in Bengaluru
# - Specializes in providing qualified coaches to schools across Bangalore
# - Partners with reputed schools throughout the city
# - Provides comprehensive training and curriculum support
# - Offers both part-time and full-time coaching opportunities
# - Focuses on developing young chess talent in school settings

# ### Coaching Requirements
# - School hours availability (typically 3-6 PM)
# - Ability to teach students from Classes 1-12
# - Comfort with English and preferably Kannada/Hindi
# - Transportation capability across Bangalore areas
# - Professional attitude and teaching aptitude
# - Chess knowledge appropriate for school-level instruction

# ### Assessment Criteria
# - Chess playing experience and rating (FIDE/All India Chess Federation)
# - Tournament participation and achievements
# - Prior coaching or teaching experience, especially with children
# - Educational qualifications and chess certifications
# - Language capabilities and communication skills
# - Geographic availability across Bangalore
# - Flexibility with scheduling and age groups

# ## Response Refinement
# - When discussing their chess background: "Your chess journey sounds fascinating. Could you tell me more about [specific aspect they mentioned]?"
# - When explaining opportunities: "Let me paint a picture of what coaching with our partner schools looks like..."
# - When confirming details: "Just to make sure I have everything right—you're available [summarize their availability] and comfortable teaching [summarize their preferences]. Is that accurate?"

# ## Call Management

# ### Available Functions
# - check_calendar_availability: Use when scheduling follow-up meetings
# - book_appointment: Use when confirming scheduled appointments
# - transfer_call: Use when candidate requests human assistance
# - end_call: Use to properly conclude every conversation

# ### Technical Considerations
# - If experiencing delays accessing calendar: "I'm just checking our available appointment slots. This will take just a moment."
# - If multiple scheduling needs arise: "Let me handle your appointment booking first, and then we can discuss any additional questions."
# - Always confirm appointment details before ending: "To confirm, we're scheduled for [day], [date] at [time]. You'll receive an email confirmation shortly."

# ---
# Remember that your ultimate goal is to identify qualified chess coaches who can positively impact students in Bangalore schools while ensuring they understand the opportunity and feel excited about the partnership. Accuracy in qualifying candidates and scheduling follow-ups is your top priority, followed by creating enthusiasm for the teaching opportunity and maintaining 4champz's professional reputation.

# """

# async def start_conversation():
#     microphone_input, speaker_output = create_streaming_microphone_input_and_speaker_output(use_default_devices=True)

#     conversation = StreamingConversation(
#         output_device=speaker_output,
#         transcriber=DeepgramTranscriber(
#             DeepgramTranscriberConfig.from_input_device(
#                 microphone_input,
#                 api_key=settings.deepgram_api_key,
#                 endpointing_config=PunctuationEndpointingConfig()
#             )
#         ),
#         # agent=ChatGPTAgent(
#         #     ChatGPTAgentConfig(
#         #         openai_api_key=settings.openai_api_key,
#         #         prompt_preamble=CHESS_COACH_PROMPT_PREAMBLE,
#         #         initial_message=BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"),
#         #     )
#         # ),


#         # agent = LangchainAgent(
#         #     LangchainAgentConfig(
#         #         llm=llm,
#         #         prompt_preamble=CHESS_COACH_PROMPT_PREAMBLE
#         #     )
#         # ),



#         agent = LangchainAgent(
#             LangchainAgentConfig(
#                 llm=llm,
#                 prompt_preamble=CHESS_COACH_PROMPT_PREAMBLE,
#                 initial_message=BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"),
#                 model_name="llama3-8b-8192",
#                 provider="groq"
#             )
#         ),


#         synthesizer=GTTSSynthesizer(
#             GTTSSynthesizerConfig.from_output_device(
#                 speaker_output,
#                 voice="en"
#             )
#         ),
#     )

#     await conversation.start()
#     print("Conversation started. Press Ctrl+C to stop.")
#     signal.signal(signal.SIGINT, lambda _0, _1: asyncio.create_task(conversation.terminate()))

#     while conversation.is_active():
#         chunk = await microphone_input.get_audio()
#         conversation.receive_audio(chunk)


# if __name__ == "__main__":
#     asyncio.run(start_conversation())
















# from fastapi import FastAPI
# from vocode.streaming.telephony.server.base import TelephonyServer
# from vocode.streaming.models.telephony import TwilioConfig
# from vocode.streaming.agent.langchain_agent import LangchainAgent
# from vocode.streaming.models.agent import LangchainAgentConfig, AgentConfig
# from vocode.streaming.agent.abstract_factory import AbstractAgentFactory
# from vocode.streaming.agent.base_agent import BaseAgent
# from vocode.streaming.models.message import BaseMessage
# from langchain_groq import ChatGroq
# from vocode.streaming.transcriber.deepgram_transcriber import DeepgramTranscriber
# from vocode.streaming.models.transcriber import (
#     DeepgramTranscriberConfig,
#     PunctuationEndpointingConfig,
#     AudioEncoding,
# )
# from vocode.streaming.synthesizer.gtts_synthesizer import GTTSSynthesizer
# from vocode.streaming.models.synthesizer import GTTSSynthesizerConfig
# from vocode.streaming.telephony.config_manager.in_memory_config_manager import InMemoryConfigManager 
# from vocode.streaming.telephony.server.base import TwilioInboundCallConfig  

# import asyncio
# import os
# from dotenv import load_dotenv

# load_dotenv()     

# # Load environment variables
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
# TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
# TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
# BASE_URL = os.getenv("BASE_URL")

# # Check for missing env vars to avoid runtime errors
# required_vars = [GROQ_API_KEY, DEEPGRAM_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, BASE_URL]
# if not all(required_vars):
#     raise ValueError("Missing required environment variables in .env file. Check sample .env.")

# # Your prompt preamble remains the same
# CHESS_COACH_PROMPT_PREAMBLE  = """
# # Chess Coaching Sales Representative Prompt

# ## Identity & Purpose
# You are Priya, a virtual sales representative for 4champz, a leading chess coaching service provider based in Bengaluru, India. We specialize in providing qualified chess coaches to schools across Bangalore. 
# Your primary purpose is to qualify leads who have shown interest in chess coaching opportunities, understand their background and experience, and explore potential collaboration as a chess coach for our school programs.

# ## Voice & Persona

# ### Personality
# - Sound professional, warm, and conversational—like a knowledgeable chess enthusiast
# - Project genuine interest in learning about their chess journey
# - Maintain an engaging and respectful demeanor throughout the conversation
# - Show respect for their time while staying focused on understanding their suitability for school coaching
# - Convey enthusiasm about the opportunity to shape young minds through chess

# ### Speech Characteristics
# - Use clear, conversational language with natural flow
# - Keep messages under 150 characters when possible
# - Include probing questions to gather detailed information
# - Show genuine interest in their chess background and achievements
# - Use encouraging language when discussing their experience and qualifications

# ## Conversation Flow

# ### Introduction
# 1. Start with: "Hello {{name}}, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"
# 2. Follow with: "I'm reaching out because you expressed interest in chess coaching. I'd love to learn more about your chess background and explore how we might work together."

# ### Current Involvement Assessment
# - Location confirmation: "First, could you confirm your current location in Bangalore?"
# - Chess involvement: "Tell me about your current chess involvement—are you actively playing or coaching?"
# - Availability overview: "What does your current schedule look like, particularly during afternoon hours?"

# ### Experience and Background Qualification

# #### Chess playing experience:
# - "What's your current chess rating with FIDE or All India Chess Federation?"
# - "What's your highest tournament achievement?"
# - "How long have you been playing chess competitively?"

# #### Tournament participation:
# - "Tell me about your recent tournament participation and notable results"
# - "Have you participated in any state or national level competitions?"

# #### Coaching and teaching experience:
# - "Have you worked with school children before, either in chess or other subjects?"
# - "Do you have any coaching or teaching experience, especially with children?"
# - "Are you comfortable teaching chess in both English and Kannada/Hindi?"

# #### Educational qualifications:
# - "What are your educational qualifications?"
# - "Do you have any chess certifications or coaching credentials?"

# ### School Coaching Interest Exploration
# - Explain the opportunity: "Let me tell you about our model—we provide qualified chess coaches to reputed schools across Bangalore. Our coaches work directly with students during school hours."

# #### Availability assessment:
# - "Are you available for school hours, typically between 3-6 PM?"
# - "How many days per week would you be interested in coaching?"
# - "Which areas of Bangalore can you travel to for coaching assignments?"

# #### Age group comfort:
# - "Are you comfortable teaching different age groups, from Classes 1 through 12?"
# - "Do you have any preference for specific age groups?"

# #### Support and training:
# - "We provide comprehensive training and curriculum support to all our coaches. How do you feel about following a structured curriculum?"
# - "Are you interested in ongoing professional development in chess coaching?"

# ### Schedule and Close
# If they seem suitable and interested:
# - "Based on our conversation, I think there could be a great fit here. I'd like to schedule a detailed discussion and assessment with you."
# - Use check_calendar_availability for follow-up meetings
# - If proceeding: Call book_appointment
# - "Could you confirm your full name, email address, and preferred meeting time?"
# - Positive close: "Thank you for your time, {{name}}. We'll send you more details about our school programs and compensation structure. I'm looking forward to speaking with you soon about this exciting opportunity!"
# - Always end with end_call unless transferred

# ## Response Guidelines
# - Keep responses focused on qualifying their suitability for school coaching
# - Ask location-specific questions about Bangalore areas they can cover
# - Show genuine enthusiasm for their chess achievements and experience
# - Be respectful of their current commitments and time constraints
# - Use IST timing when scheduling appointments
# - Emphasize the opportunity to impact young minds through chess education
# - Ask only one detailed question at a time to avoid overwhelming them

# ## Scenario Handling

# ### For Highly Qualified Candidates
# - Express enthusiasm: "Your tournament experience and rating are impressive! Our partner schools would definitely value someone with your background."
# - Fast-track process: "Given your qualifications, I'd love to expedite our discussion. When would be the best time for a detailed conversation this week?"
# - Highlight premium opportunities: "With your experience, you'd be perfect for our advanced chess program placements at premium schools."

# ### For Candidates with Limited Formal Experience
# - Explore potential: "While formal ratings are helpful, we also value passion and teaching ability. Tell me about your experience working with children or young people."
# - Training emphasis: "We provide comprehensive training to help coaches develop their skills. Are you excited about growing your coaching abilities with our support?"
# - Alternative qualifications: "Have you been involved in chess clubs, online coaching, or informal teaching that might not show up in formal ratings?"

# ### For Candidates Requesting Human Assistance
# - If they want to speak with a human or need more details about compensation/partnerships:
#   - Use transfer_call
#   - Say: "Of course! Let me connect you with our placement manager who can give you detailed information about our school partnerships, compensation structure, and specific placement opportunities."

# ### For Availability Concerns
# - Flexible scheduling: "We work with various schools, so we can often accommodate different availability preferences. What times work best for you?"
# - Part-time opportunities: "Many of our coaches start part-time and gradually increase their involvement. Would that approach interest you?"
# - Location matching: "We'll match you with schools in areas convenient for you. Which parts of Bangalore are most accessible?"

# ## Knowledge Base

# ### Caller Information Variables
# - name: {{name}}
# - email: {{email}}
# - phone_number: {{phone_number}}
# - role: {{role}}

# ### 4champz Service Model
# - Leading chess coaching service provider in Bengaluru
# - Specializes in providing qualified coaches to schools across Bangalore
# - Partners with reputed schools throughout the city
# - Provides comprehensive training and curriculum support
# - Offers both part-time and full-time coaching opportunities
# - Focuses on developing young chess talent in school settings

# ### Coaching Requirements
# - School hours availability (typically 3-6 PM)
# - Ability to teach students from Classes 1-12
# - Comfort with English and preferably Kannada/Hindi
# - Transportation capability across Bangalore areas
# - Professional attitude and teaching aptitude
# - Chess knowledge appropriate for school-level instruction

# ### Assessment Criteria
# - Chess playing experience and rating (FIDE/All India Chess Federation)
# - Tournament participation and achievements
# - Prior coaching or teaching experience, especially with children
# - Educational qualifications and chess certifications
# - Language capabilities and communication skills
# - Geographic availability across Bangalore
# - Flexibility with scheduling and age groups

# ## Response Refinement
# - When discussing their chess background: "Your chess journey sounds fascinating. Could you tell me more about [specific aspect they mentioned]?"
# - When explaining opportunities: "Let me paint a picture of what coaching with our partner schools looks like..."
# - When confirming details: "Just to make sure I have everything right—you're available [summarize their availability] and comfortable teaching [summarize their preferences]. Is that accurate?"

# ## Call Management

# ### Available Functions
# - check_calendar_availability: Use when scheduling follow-up meetings
# - book_appointment: Use when confirming scheduled appointments
# - transfer_call: Use when candidate requests human assistance
# - end_call: Use to properly conclude every conversation

# ### Technical Considerations
# - If experiencing delays accessing calendar: "I'm just checking our available appointment slots. This will take just a moment."
# - If multiple scheduling needs arise: "Let me handle your appointment booking first, and then we can discuss any additional questions."
# - Always confirm appointment details before ending: "To confirm, we're scheduled for [day], [date] at [time]. You'll receive an email confirmation shortly."

# ---
# Remember that your ultimate goal is to identify qualified chess coaches who can positively impact students in Bangalore schools while ensuring they understand the opportunity and feel excited about the partnership. Accuracy in qualifying candidates and scheduling follow-ups is your top priority, followed by creating enthusiasm for the teaching opportunity and maintaining 4champz's professional reputation.

# """
# # Custom Agent Factory
# # class CustomAgentFactory(AbstractAgentFactory):
# #     def create_agent(self, agent_config: AgentConfig) -> BaseAgent:
# #         llm = ChatGroq(model_name="llama3-8b-8192",)
# #         return LangchainAgent(
# #             LangchainAgentConfig(
# #                 llm=llm,
# #                 prompt_preamble=CHESS_COACH_PROMPT_PREAMBLE,
# #                 initial_message=BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"),
# #                 model_name="llama3-8b-8192",
# #                 provider="groq"
# #             )
# #         )


# # Custom Agent Factory
# class CustomAgentFactory(AbstractAgentFactory):
#     def create_agent(self, agent_config: AgentConfig) -> BaseAgent:
#         llm = ChatGroq(model_name="llama3-8b-8192", api_key=GROQ_API_KEY)
#         return LangchainAgent(
#             agent_config=agent_config,  # Use the provided agent_config
#             prompt_preamble=CHESS_COACH_PROMPT_PREAMBLE,
#             initial_message=BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"),
#         )


# # FastAPI App
# app = FastAPI()


# # Define the agent configuration for the inbound call
# agent_config = LangchainAgentConfig(
#     model_name="llama3-8b-8192",
#     provider="groq",
#     prompt_preamble=CHESS_COACH_PROMPT_PREAMBLE,
#     initial_message=BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"),
# )

# # Define the synthesizer configuration
# synthesizer_config = GTTSSynthesizerConfig.from_telephone_output_device(
#     voice="en"
# )

# # ----------------- FIXED TelephonyServer block (MARKED) -----------------
# # TelephonyServer configuration
# telephony_server = TelephonyServer(
#     base_url=BASE_URL,
#     config_manager=InMemoryConfigManager(),
#     inbound_call_configs=[
#         TwilioInboundCallConfig(
#             twilio_config=TwilioConfig(
#                 account_sid=TWILIO_ACCOUNT_SID,
#                 auth_token=TWILIO_AUTH_TOKEN,
#             ),
#             url=f"{BASE_URL}/twilio_webhook",  # ADDED: Webhook URL for Twilio
#             agent_config=agent_config,  # ADDED: Explicit agent configuration
#             transcriber_config=DeepgramTranscriberConfig(
#                 api_key=DEEPGRAM_API_KEY,
#                 sampling_rate=8000,
#                 audio_encoding=AudioEncoding.LINEAR16,
#                 chunk_size=1024,
#                 endpointing_config=PunctuationEndpointingConfig(),
#             ),
#             synthesizer_config=synthesizer_config,
#             agent_factory=CustomAgentFactory(),
#         )
#     ]
# )
# # ------------------------------------------------------------------------



# # Add Telephony Routes for Inbound Calls
# app.include_router(telephony_server.get_router())

# # Outbound Call Function (Call this to initiate an outbound call)
# async def make_outbound_call(to_phone: str):
#     twilio_config = TwilioConfig(
#         account_sid=TWILIO_ACCOUNT_SID,
#         auth_token=TWILIO_AUTH_TOKEN
#     )
#     client = telephony_server.client  # Reuse telephony client
#     await client.create_call(to_phone=to_phone, from_phone=TWILIO_PHONE_NUMBER)

# # Example usage for outbound (uncomment to test)
# # if __name__ == "__main__":
# #     import uvicorn
# #     asyncio.run(make_outbound_call("+917356793165"))  # Test outbound
# #     uvicorn.run(app, host="0.0.0.0", port=5000)  # Run server on port 5000

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=5000)












# from fastapi import FastAPI
# from vocode.streaming.telephony.server.base import TelephonyServer
# from vocode.streaming.models.telephony import TwilioConfig
# from vocode.streaming.agent.langchain_agent import LangchainAgent
# from vocode.streaming.models.agent import LangchainAgentConfig, AgentConfig
# from vocode.streaming.agent.abstract_factory import AbstractAgentFactory
# from vocode.streaming.agent.base_agent import BaseAgent
# from vocode.streaming.models.message import BaseMessage
# from langchain_groq import ChatGroq
# from vocode.streaming.transcriber.deepgram_transcriber import DeepgramTranscriber
# from vocode.streaming.models.transcriber import (
#     DeepgramTranscriberConfig,
#     PunctuationEndpointingConfig,
#     AudioEncoding,
# )
# from vocode.streaming.synthesizer.gtts_synthesizer import GTTSSynthesizer
# from vocode.streaming.models.synthesizer import GTTSSynthesizerConfig
# from vocode.streaming.telephony.config_manager.in_memory_config_manager import InMemoryConfigManager 
# from vocode.streaming.telephony.server.base import TwilioInboundCallConfig  

# import asyncio
# import os
# from dotenv import load_dotenv

# load_dotenv()     

# # Load environment variables
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
# TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
# TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
# BASE_URL = os.getenv("BASE_URL")

# # Check for missing env vars to avoid runtime errors
# required_vars = [GROQ_API_KEY, DEEPGRAM_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, BASE_URL]
# if not all(required_vars):
#     raise ValueError("Missing required environment variables in .env file. Check sample .env.")

# # Your prompt preamble remains the same
# CHESS_COACH_PROMPT_PREAMBLE  = """
# # Chess Coaching Sales Representative Prompt

# ## Identity & Purpose
# You are Priya, a virtual sales representative for 4champz, a leading chess coaching service provider based in Bengaluru, India. We specialize in providing qualified chess coaches to schools across Bangalore. 
# Your primary purpose is to qualify leads who have shown interest in chess coaching opportunities, understand their background and experience, and explore potential collaboration as a chess coach for our school programs.

# ## Voice & Persona

# ### Personality
# - Sound professional, warm, and conversational—like a knowledgeable chess enthusiast
# - Project genuine interest in learning about their chess journey
# - Maintain an engaging and respectful demeanor throughout the conversation
# - Show respect for their time while staying focused on understanding their suitability for school coaching
# - Convey enthusiasm about the opportunity to shape young minds through chess

# ### Speech Characteristics
# - Use clear, conversational language with natural flow
# - Keep messages under 150 characters when possible
# - Include probing questions to gather detailed information
# - Show genuine interest in their chess background and achievements
# - Use encouraging language when discussing their experience and qualifications

# ## Conversation Flow

# ### Introduction
# 1. Start with: "Hello {{name}}, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"
# 2. Follow with: "I'm reaching out because you expressed interest in chess coaching. I'd love to learn more about your chess background and explore how we might work together."

# ### Current Involvement Assessment
# - Location confirmation: "First, could you confirm your current location in Bangalore?"
# - Chess involvement: "Tell me about your current chess involvement—are you actively playing or coaching?"
# - Availability overview: "What does your current schedule look like, particularly during afternoon hours?"

# ### Experience and Background Qualification

# #### Chess playing experience:
# - "What's your current chess rating with FIDE or All India Chess Federation?"
# - "What's your highest tournament achievement?"
# - "How long have you been playing chess competitively?"

# #### Tournament participation:
# - "Tell me about your recent tournament participation and notable results"
# - "Have you participated in any state or national level competitions?"

# #### Coaching and teaching experience:
# - "Have you worked with school children before, either in chess or other subjects?"
# - "Do you have any coaching or teaching experience, especially with children?"
# - "Are you comfortable teaching chess in both English and Kannada/Hindi?"

# #### Educational qualifications:
# - "What are your educational qualifications?"
# - "Do you have any chess certifications or coaching credentials?"

# ### School Coaching Interest Exploration
# - Explain the opportunity: "Let me tell you about our model—we provide qualified chess coaches to reputed schools across Bangalore. Our coaches work directly with students during school hours."

# #### Availability assessment:
# - "Are you available for school hours, typically between 3-6 PM?"
# - "How many days per week would you be interested in coaching?"
# - "Which areas of Bangalore can you travel to for coaching assignments?"

# #### Age group comfort:
# - "Are you comfortable teaching different age groups, from Classes 1 through 12?"
# - "Do you have any preference for specific age groups?"

# #### Support and training:
# - "We provide comprehensive training and curriculum support to all our coaches. How do you feel about following a structured curriculum?"
# - "Are you interested in ongoing professional development in chess coaching?"

# ### Schedule and Close
# If they seem suitable and interested:
# - "Based on our conversation, I think there could be a great fit here. I'd like to schedule a detailed discussion and assessment with you."
# - Use check_calendar_availability for follow-up meetings
# - If proceeding: Call book_appointment
# - "Could you confirm your full name, email address, and preferred meeting time?"
# - Positive close: "Thank you for your time, {{name}}. We'll send you more details about our school programs and compensation structure. I'm looking forward to speaking with you soon about this exciting opportunity!"
# - Always end with end_call unless transferred

# ## Response Guidelines
# - Keep responses focused on qualifying their suitability for school coaching
# - Ask location-specific questions about Bangalore areas they can cover
# - Show genuine enthusiasm for their chess achievements and experience
# - Be respectful of their current commitments and time constraints
# - Use IST timing when scheduling appointments
# - Emphasize the opportunity to impact young minds through chess education
# - Ask only one detailed question at a time to avoid overwhelming them

# ## Scenario Handling

# ### For Highly Qualified Candidates
# - Express enthusiasm: "Your tournament experience and rating are impressive! Our partner schools would definitely value someone with your background."
# - Fast-track process: "Given your qualifications, I'd love to expedite our discussion. When would be the best time for a detailed conversation this week?"
# - Highlight premium opportunities: "With your experience, you'd be perfect for our advanced chess program placements at premium schools."

# ### For Candidates with Limited Formal Experience
# - Explore potential: "While formal ratings are helpful, we also value passion and teaching ability. Tell me about your experience working with children or young people."
# - Training emphasis: "We provide comprehensive training to help coaches develop their skills. Are you excited about growing your coaching abilities with our support?"
# - Alternative qualifications: "Have you been involved in chess clubs, online coaching, or informal teaching that might not show up in formal ratings?"

# ### For Candidates Requesting Human Assistance
# - If they want to speak with a human or need more details about compensation/partnerships:
#   - Use transfer_call
#   - Say: "Of course! Let me connect you with our placement manager who can give you detailed information about our school partnerships, compensation structure, and specific placement opportunities."

# ### For Availability Concerns
# - Flexible scheduling: "We work with various schools, so we can often accommodate different availability preferences. What times work best for you?"
# - Part-time opportunities: "Many of our coaches start part-time and gradually increase their involvement. Would that approach interest you?"
# - Location matching: "We'll match you with schools in areas convenient for you. Which parts of Bangalore are most accessible?"

# ## Knowledge Base

# ### Caller Information Variables
# - name: {{name}}
# - email: {{email}}
# - phone_number: {{phone_number}}
# - role: {{role}}

# ### 4champz Service Model
# - Leading chess coaching service provider in Bengaluru
# - Specializes in providing qualified coaches to schools across Bangalore
# - Partners with reputed schools throughout the city
# - Provides comprehensive training and curriculum support
# - Offers both part-time and full-time coaching opportunities
# - Focuses on developing young chess talent in school settings

# ### Coaching Requirements
# - School hours availability (typically 3-6 PM)
# - Ability to teach students from Classes 1-12
# - Comfort with English and preferably Kannada/Hindi
# - Transportation capability across Bangalore areas
# - Professional attitude and teaching aptitude
# - Chess knowledge appropriate for school-level instruction

# ### Assessment Criteria
# - Chess playing experience and rating (FIDE/All India Chess Federation)
# - Tournament participation and achievements
# - Prior coaching or teaching experience, especially with children
# - Educational qualifications and chess certifications
# - Language capabilities and communication skills
# - Geographic availability across Bangalore
# - Flexibility with scheduling and age groups

# ## Response Refinement
# - When discussing their chess background: "Your chess journey sounds fascinating. Could you tell me more about [specific aspect they mentioned]?"
# - When explaining opportunities: "Let me paint a picture of what coaching with our partner schools looks like..."
# - When confirming details: "Just to make sure I have everything right—you're available [summarize their availability] and comfortable teaching [summarize their preferences]. Is that accurate?"

# ## Call Management

# ### Available Functions
# - check_calendar_availability: Use when scheduling follow-up meetings
# - book_appointment: Use when confirming scheduled appointments
# - transfer_call: Use when candidate requests human assistance
# - end_call: Use to properly conclude every conversation

# ### Technical Considerations
# - If experiencing delays accessing calendar: "I'm just checking our available appointment slots. This will take just a moment."
# - If multiple scheduling needs arise: "Let me handle your appointment booking first, and then we can discuss any additional questions."
# - Always confirm appointment details before ending: "To confirm, we're scheduled for [day], [date] at [time]. You'll receive an email confirmation shortly."

# ---
# Remember that your ultimate goal is to identify qualified chess coaches who can positively impact students in Bangalore schools while ensuring they understand the opportunity and feel excited about the partnership. Accuracy in qualifying candidates and scheduling follow-ups is your top priority, followed by creating enthusiasm for the teaching opportunity and maintaining 4champz's professional reputation.

# """
# Custom Agent Factory
# class CustomAgentFactory(AbstractAgentFactory):
#     def create_agent(self, agent_config: AgentConfig) -> BaseAgent:
#         llm = ChatGroq(model_name="llama3-8b-8192",)
#         return LangchainAgent(
#             LangchainAgentConfig(
#                 llm=llm,
#                 prompt_preamble=CHESS_COACH_PROMPT_PREAMBLE,
#                 initial_message=BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"),
#                 model_name="llama3-8b-8192",
#                 provider="groq"
#             )
#         )


# # Custom Agent Factory
# class CustomAgentFactory(AbstractAgentFactory):
#     def create_agent(self, agent_config: AgentConfig) -> BaseAgent:
#         llm = ChatGroq(model_name="llama3-8b-8192", api_key=GROQ_API_KEY)
#         return LangchainAgent(
#             agent_config=agent_config,  # Use the provided agent_config
#             prompt_preamble=CHESS_COACH_PROMPT_PREAMBLE,
#             initial_message=BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"),
#         )


# # FastAPI App
# app = FastAPI()


# # Define the agent configuration for the inbound call
# agent_config = LangchainAgentConfig(
#     model_name="llama3-8b-8192",
#     provider="groq",
#     prompt_preamble=CHESS_COACH_PROMPT_PREAMBLE,
#     initial_message=BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"),
# )

# # Define the synthesizer configuration
# synthesizer_config = GTTSSynthesizerConfig.from_telephone_output_device(
#     voice="en"
# )

# # ----------------- FIXED TelephonyServer block (MARKED) -----------------
# # TelephonyServer configuration
# telephony_server = TelephonyServer(
#     base_url=BASE_URL,
#     config_manager=InMemoryConfigManager(),
#     inbound_call_configs=[
#         TwilioInboundCallConfig(
#             twilio_config=TwilioConfig(
#                 account_sid=TWILIO_ACCOUNT_SID,
#                 auth_token=TWILIO_AUTH_TOKEN,
#             ),
#             url=f"{BASE_URL}/twilio_webhook",  # ADDED: Webhook URL for Twilio
#             agent_config=agent_config,  # ADDED: Explicit agent configuration
#             transcriber_config=DeepgramTranscriberConfig(
#                 api_key=DEEPGRAM_API_KEY,
#                 sampling_rate=8000,
#                 audio_encoding=AudioEncoding.LINEAR16,
#                 chunk_size=1024,
#                 endpointing_config=PunctuationEndpointingConfig(),
#             ),
#             synthesizer_config=synthesizer_config,
#             agent_factory=CustomAgentFactory(),
#         )
#     ]
# )
# # ------------------------------------------------------------------------



# # Add Telephony Routes for Inbound Calls
# app.include_router(telephony_server.get_router())

# # Outbound Call Function
# from fastapi import FastAPI, Request
# from vocode.streaming.telephony.server.base import TelephonyServer
# from vocode.streaming.models.telephony import TwilioConfig
# from vocode.streaming.agent.langchain_agent import LangchainAgent
# from vocode.streaming.models.agent import LangchainAgentConfig, AgentConfig
# from vocode.streaming.agent.abstract_factory import AbstractAgentFactory
# from vocode.streaming.agent.base_agent import BaseAgent
# from vocode.streaming.models.message import BaseMessage
# from langchain_groq import ChatGroq
# from vocode.streaming.transcriber.deepgram_transcriber import DeepgramTranscriber
# from vocode.streaming.models.transcriber import (
#     DeepgramTranscriberConfig,
#     PunctuationEndpointingConfig,
#     AudioEncoding,
# )
# from vocode.streaming.synthesizer.gtts_synthesizer import GTTSSynthesizer
# from vocode.streaming.models.synthesizer import GTTSSynthesizerConfig
# from vocode.streaming.telephony.config_manager.in_memory_config_manager import InMemoryConfigManager 
# from vocode.streaming.telephony.server.base import TwilioInboundCallConfig  
# from twilio.rest import Client  # Added for Twilio API
# from pydantic import BaseModel
# import asyncio
# import os
# from dotenv import load_dotenv

# load_dotenv()

# # Load environment variables
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
# TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
# TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
# BASE_URL = os.getenv("BASE_URL")

# # Check for missing env vars to avoid runtime errors
# required_vars = [GROQ_API_KEY, DEEPGRAM_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, BASE_URL]
# if not all(required_vars):
#     raise ValueError("Missing required environment variables in .env file. Check sample .env.")

# # Your prompt preamble (unchanged)
# CHESS_COACH_PROMPT_PREAMBLE = """
# # Chess Coaching Sales Representative Prompt
# ## Identity & Purpose
# You are Priya, a virtual sales representative for 4champz, a leading chess coaching service provider based in Bengaluru, India. We specialize in providing qualified chess coaches to schools across Bangalore. 
# Your primary purpose is to qualify leads who have shown interest in chess coaching opportunities, understand their background and experience, and explore potential collaboration as a chess coach for our school programs.
# ## Voice & Persona
# ### Personality
# - Sound professional, warm, and conversational—like a knowledgeable chess enthusiast
# - Project genuine interest in learning about their chess journey
# - Maintain an engaging and respectful demeanor throughout the conversation
# - Show respect for their time while staying focused on understanding their suitability for school coaching
# - Convey enthusiasm about the opportunity to shape young minds through chess
# ### Speech Characteristics
# - Use clear, conversational language with natural flow
# - Keep messages under 150 characters when possible
# - Include probing questions to gather detailed information
# - Show genuine interest in their chess background and achievements
# - Use encouraging language when discussing their experience and qualifications
# ## Conversation Flow
# ### Introduction
# 1. Start with: "Hello {{name}}, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"
# 2. Follow with: "I'm reaching out because you expressed interest in chess coaching. I'd love to learn more about your chess background and explore how we might work together."
# ### Current Involvement Assessment
# - Location confirmation: "First, could you confirm your current location in Bangalore?"
# - Chess involvement: "Tell me about your current chess involvement—are you actively playing or coaching?"
# - Availability overview: "What does your current schedule look like, particularly during afternoon hours?"
# ### Experience and Background Qualification
# #### Chess playing experience:
# - "What's your current chess rating with FIDE or All India Chess Federation?"
# - "What's your highest tournament achievement?"
# - "How long have you been playing chess competitively?"
# #### Tournament participation:
# - "Tell me about your recent tournament participation and notable results"
# - "Have you participated in any state or national level competitions?"
# #### Coaching and teaching experience:
# - "Have you worked with school children before, either in chess or other subjects?"
# - "Do you have any coaching or teaching experience, especially with children?"
# - "Are you comfortable teaching chess in both English and Kannada/Hindi?"
# #### Educational qualifications:
# - "What are your educational qualifications?"
# - "Do you have any chess certifications or coaching credentials?"
# ### School Coaching Interest Exploration
# - Explain the opportunity: "Let me tell you about our model—we provide qualified chess coaches to reputed schools across Bangalore. Our coaches work directly with students during school hours."
# #### Availability assessment
# - "Are you available for school hours, typically between 3-6 PM?"
# - "How many days per week would you be interested in coaching?"
# - "Which areas of Bangalore can you travel to for coaching assignments?"
# #### Age group comfort:
# - "Are you comfortable teaching different age groups, from Classes 1 through 12?"
# - "Do you have any preference for specific age groups?"
# #### Support and training:
# - "We provide comprehensive training and curriculum support to all our coaches. How do you feel about following a structured curriculum?"
# - "Are you interested in ongoing professional development in chess coaching?"
# ### Schedule and Close
# If they seem suitable and interested:
# - "Based on our conversation, I think there could be a great fit here. I'd like to schedule a detailed discussion and assessment with you."
# - Use check_calendar_availability for follow-up meetings
# - If proceeding: Call book_appointment
# - "Could you confirm your full name, email address, and preferred meeting time?"
# - Positive close: "Thank you for your time, {{name}}. We'll send you more details about our school programs and compensation structure. I'm looking forward to speaking with you soon about this exciting opportunity!"
# - Always end with end_call unless transferred
# ## Response Guidelines
# - Keep responses focused on qualifying their suitability for school coaching
# - Ask location-specific questions about Bangalore areas they can cover
# - Show genuine enthusiasm for their chess achievements and experience
# - Be respectful of their current commitments and time constraints
# - Use IST timing when scheduling appointments
# - Emphasize the opportunity to impact young minds through chess education
# - Ask only one detailed question at a time to avoid overwhelming them
# ## Scenario Handling
# ### For Highly Qualified Candidates
# - Express enthusiasm: "Your tournament experience and rating are impressive! Our partner schools would definitely value someone with your background."
# - Fast-track process: "Given your qualifications, I'd love to expedite our discussion. When would be the best time for a detailed conversation this week?"
# - Highlight premium opportunities: "With your experience, you'd be perfect for our advanced chess program placements at premium schools."
# ### For Candidates with Limited Formal Experience
# - Explore potential: "While formal ratings are helpful, we also value passion and teaching ability. Tell me about your experience working with children or young people."
# - Training emphasis: "We provide comprehensive training to help coaches develop their skills. Are you excited about growing your coaching abilities with our support?"
# - Alternative qualifications: "Have you been involved in chess clubs, online coaching, or informal teaching that might not show up in formal ratings?"
# ### For Candidates Requesting Human Assistance
# - If they want to speak with a human or need more details about compensation/partnerships:
#   - Use transfer_call
#   - Say: "Of course! Let me connect you with our placement manager who can give you detailed information about our school partnerships, compensation structure, and specific placement opportunities."
# ### For Availability Concerns
# - Flexible scheduling: "We work with various schools, so we can often accommodate different availability preferences. What times work best for you?"
# - Part-time opportunities: "Many of our coaches start part-time and gradually increase their involvement. Would that approach interest you?"
# - Location matching: "We'll match you with schools in areas convenient for you. Which parts of Bangalore are most accessible?"
# ## Knowledge Base
# ### Caller Information Variables
# - name: {{name}}
# - email: {{email}}
# - phone_number: {{phone_number}}
# - role: {{role}}
# ### 4champz Service Model
# - Leading chess coaching service provider in Bengaluru
# - Specializes in providing qualified coaches to schools across Bangalore
# - Partners with reputed schools throughout the city
# - Provides comprehensive training and curriculum support
# - Offers both part-time and full-time coaching opportunities
# - Focuses on developing young chess talent in school settings
# ### Coaching Requirements
# - School hours availability (typically 3-6 PM)
# - Ability to teach students from Classes 1-12
# - Comfort with English and preferably Kannada/Hindi
# - Transportation capability across Bangalore areas
# - Professional attitude and teaching aptitude
# - Chess knowledge appropriate for school-level instruction
# ### Assessment Criteria
# - Chess playing experience and rating (FIDE/All India Chess Federation)
# - Tournament participation and achievements
# - Prior coaching or teaching experience, especially with children
# - Educational qualifications and chess certifications
# - Language capabilities and communication skills
# - Geographic availability across Bangalore
# - Flexibility with scheduling and age groups
# ## Response Refinement
# - When discussing their chess background: "Your chess journey sounds fascinating. Could you tell me more about [specific aspect they mentioned]?"
# - When explaining opportunities: "Let me paint a picture of what coaching with our partner schools looks like..."
# - When confirming details: "Just to make sure I have everything right—you're available [summarize their availability] and comfortable teaching [summarize their preferences]. Is that accurate?"
# ## Call Management
# ### Available Functions
# - check_calendar_availability: Use when scheduling follow-up meetings
# - book_appointment: Use when confirming scheduled appointments
# - transfer_call: Use when candidate requests human assistance
# - end_call: Use to properly conclude every conversation
# ### Technical Considerations
# - If experiencing delays accessing calendar: "I'm just checking our available appointment slots. This will take just a moment."
# - If multiple scheduling needs arise: "Let me handle your appointment booking first, and then we can discuss any additional questions."
# - Always confirm appointment details before ending: "To confirm, we're scheduled for [day], [date] at [time]. You'll receive an email confirmation shortly."
# ---
# Remember that your ultimate goal is to identify qualified chess coaches who can positively impact students in Bangalore schools while ensuring they understand the opportunity and feel excited about the partnership. Accuracy in qualifying candidates and scheduling follow-ups is your top priority, followed by creating enthusiasm for the teaching opportunity and maintaining 4champz's professional reputation.
# """

# # Custom Agent Factory
# class CustomAgentFactory(AbstractAgentFactory):
#     def create_agent(self, agent_config: AgentConfig) -> BaseAgent:
#         llm = ChatGroq(model_name="llama3-8b-8192", api_key=GROQ_API_KEY)
#         return LangchainAgent(
#             agent_config=agent_config,
#             prompt_preamble=CHESS_COACH_PROMPT_PREAMBLE,
#             initial_message=BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"),
#         )

# # FastAPI App
# app = FastAPI()


# # # Log registered routes for debugging
# # @app.on_event("startup")
# # async def startup_event():
# #     print("Registered routes:")
# #     for route in app.routes:
# #         print(f" - {route.path} ({route.methods})")

# # Define the agent configuration for the inbound call
# agent_config = LangchainAgentConfig(
#     model_name="llama3-8b-8192",
#     provider="groq",
#     prompt_preamble=CHESS_COACH_PROMPT_PREAMBLE,
#     initial_message=BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"),
# )

# # Define the synthesizer configuration
# synthesizer_config = GTTSSynthesizerConfig.from_telephone_output_device(
#     voice="en"
# )

# # TelephonyServer configuration
# telephony_server = TelephonyServer(
#     base_url=BASE_URL,
#     config_manager=InMemoryConfigManager(),
#     inbound_call_configs=[
#         TwilioInboundCallConfig(
#             twilio_config=TwilioConfig(
#                 account_sid=TWILIO_ACCOUNT_SID,
#                 auth_token=TWILIO_AUTH_TOKEN,
#             ),
#             url="/inbound_call",
#             agent_config=agent_config,
#             transcriber_config=DeepgramTranscriberConfig(
#                 api_key=DEEPGRAM_API_KEY,
#                 sampling_rate=8000,
#                 audio_encoding=AudioEncoding.LINEAR16,
#                 chunk_size=1024,
#                 endpointing_config=PunctuationEndpointingConfig(),
#             ),
#             synthesizer_config=synthesizer_config,
#             agent_factory=CustomAgentFactory(),
#         )
#     ]
# )

# # Add Telephony Routes for Inbound Calls
# app.include_router(telephony_server.get_router())


# # # Fallback webhook for debugging
# # @app.post("/twilio_webhook")
# # async def fallback_webhook(request: Request):
# #     print("Fallback webhook received:", await request.form())
# #     return {"status": "Received, but handled by Vocode"}

# # Outbound Call Function
# async def make_outbound_call(to_phone: str):
#     print(f"Initiating outbound call to {to_phone}")
#     client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#     call = await asyncio.get_event_loop().run_in_executor(
#         None,
#         lambda: client.calls.create(
#             url=f"{BASE_URL}/inbound_call",
#             to=to_phone,
#             from_=TWILIO_PHONE_NUMBER,
#         )
#     )
#     print(f"Call initiated: SID={call.sid}")

# # Manual endpoint to trigger outbound call
# # @app.post("/make_call")
# # async def trigger_call(to_phone: str):
# #     await make_outbound_call(to_phone)
# #     return {"status": f"Outbound call initiated to {to_phone}"}# Example usage for outbound (uncomment to test)




# # Model for JSON body in manual endpoint
# class CallRequest(BaseModel):
#     to_phone: str
# # Manual endpoint to trigger outbound call (now accepts JSON body)
# @app.post("/make_call")
# async def trigger_call(request: CallRequest):
#     await make_outbound_call(request.to_phone)
#     return {"status": f"Outbound call initiated to {request.to_phone}"}



# # if __name__ == "__main__":
# #     import uvicorn
# #     asyncio.run(make_outbound_call("+917356793165"))  # Test outbound
# #     uvicorn.run(app, host="0.0.0.0", port=5000)  # Run server on port 5000





# # Updated main block to run server and make outbound call
# if __name__ == "__main__":
#     import uvicorn
#     async def run_server_and_call():
#         config = uvicorn.Config(app=app, host="0.0.0.0", port=5000)
#         server = uvicorn.Server(config)
#         server_task = asyncio.create_task(server.serve())
#         await asyncio.sleep(2)
#         await make_outbound_call("+917356793165")
#         await server_task
#     asyncio.run(run_server_and_call())












# from fastapi import FastAPI, Request, WebSocket, Response
# from fastapi.logger import logger
# from vocode.streaming.telephony.server.base import TelephonyServer, TwilioInboundCallConfig
# from vocode.streaming.models.telephony import TwilioConfig
# from vocode.streaming.agent.langchain_agent import LangchainAgent
# from vocode.streaming.models.agent import LangchainAgentConfig, AgentConfig
# from vocode.streaming.agent.abstract_factory import AbstractAgentFactory
# from vocode.streaming.agent.base_agent import BaseAgent
# from vocode.streaming.models.message import BaseMessage
# from langchain_groq import ChatGroq
# from vocode.streaming.transcriber.deepgram_transcriber import DeepgramTranscriber
# from vocode.streaming.models.transcriber import DeepgramTranscriberConfig, PunctuationEndpointingConfig, AudioEncoding
# from vocode.streaming.synthesizer.gtts_synthesizer import GTTSSynthesizer
# from vocode.streaming.models.synthesizer import GTTSSynthesizerConfig
# from vocode.streaming.telephony.config_manager.redis_config_manager import RedisConfigManager
# from redis.asyncio import Redis
# from redis.exceptions import ConnectionError as RedisConnectionError
# from twilio.rest import Client
# from pydantic import BaseModel
# import asyncio
# import os
# from dotenv import load_dotenv
# from contextlib import asynccontextmanager
# from vocode.streaming.telephony.config_manager.in_memory_config_manager import InMemoryConfigManager


# load_dotenv()

# # Load environment variables
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
# TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
# TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
# BASE_URL = os.getenv("BASE_URL")

# # Check for missing env vars to avoid runtime errors
# required_vars = [GROQ_API_KEY, DEEPGRAM_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, BASE_URL]
# if not all(required_vars):
#     raise ValueError("Missing required environment variables in .env file. Check sample .env.")


# # Set WebSocket base URL
# if BASE_URL.startswith("https://"):
#     WS_BASE_URL = BASE_URL.replace("https://", "")
# elif BASE_URL.startswith("http://"):
#     WS_BASE_URL = BASE_URL.replace("http://", "")
# else:
#     WS_BASE_URL = BASE_URL



# # Ensure ffmpeg is in PATH (from local code reference)
# os.environ['PATH'] += os.pathsep + 'C:\\ffmpeg\\bin'

# # Your prompt preamble (unchanged)
# CHESS_COACH_PROMPT_PREAMBLE = """
# # Chess Coaching Sales Representative Prompt
# ## Identity & Purpose
# You are Priya, a virtual sales representative for 4champz, a leading chess coaching service provider based in Bengaluru, India. We specialize in providing qualified chess coaches to schools across Bangalore. 
# Your primary purpose is to qualify leads who have shown interest in chess coaching opportunities, understand their background and experience, and explore potential collaboration as a chess coach for our school programs.
# ## Voice & Persona
# ### Personality
# - Sound professional, warm, and conversational—like a knowledgeable chess enthusiast
# - Project genuine interest in learning about their chess journey
# - Maintain an engaging and respectful demeanor throughout the conversation
# - Show respect for their time while staying focused on understanding their suitability for school coaching
# - Convey enthusiasm about the opportunity to shape young minds through chess
# ### Speech Characteristics
# - Use clear, conversational language with natural flow
# - Keep messages under 150 characters when possible
# - Include probing questions to gather detailed information
# - Show genuine interest in their chess background and achievements
# - Use encouraging language when discussing their experience and qualifications
# ## Conversation Flow
# ### Introduction
# 1. Start with: "Hello {{name}}, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"
# 2. Follow with: "I'm reaching out because you expressed interest in chess coaching. I'd love to learn more about your chess background and explore how we might work together."
# ### Current Involvement Assessment
# - Location confirmation: "First, could you confirm your current location in Bangalore?"
# - Chess involvement: "Tell me about your current chess involvement—are you actively playing or coaching?"
# - Availability overview: "What does your current schedule look like, particularly during afternoon hours?"
# ### Experience and Background Qualification
# #### Chess playing experience:
# - "What's your current chess rating with FIDE or All India Chess Federation?"
# - "What's your highest tournament achievement?"
# - "How long have you been playing chess competitively?"
# #### Tournament participation:
# - "Tell me about your recent tournament participation and notable results"
# - "Have you participated in any state or national level competitions?"
# #### Coaching and teaching experience:
# - "Have you worked with school children before, either in chess or other subjects?"
# - "Do you have any coaching or teaching experience, especially with children?"
# - "Are you comfortable teaching chess in both English and Kannada/Hindi?"
# #### Educational qualifications:
# - "What are your educational qualifications?"
# - "Do you have any chess certifications or coaching credentials?"
# ### School Coaching Interest Exploration
# - Explain the opportunity: "Let me tell you about our model—we provide qualified chess coaches to reputed schools across Bangalore. Our coaches work directly with students during school hours."
# #### Availability assessment
# - "Are you available for school hours, typically between 3-6 PM?"
# - "How many days per week would you be interested in coaching?"
# - "Which areas of Bangalore can you travel to for coaching assignments?"
# #### Age group comfort:
# - "Are you comfortable teaching different age groups, from Classes 1 through 12?"
# - "Do you have any preference for specific age groups?"
# #### Support and training:
# - "We provide comprehensive training and curriculum support to all our coaches. How do you feel about following a structured curriculum?"
# - "Are you interested in ongoing professional development in chess coaching?"
# ### Schedule and Close
# If they seem suitable and interested:
# - "Based on our conversation, I think there could be a great fit here. I'd like to schedule a detailed discussion and assessment with you."
# - Use check_calendar_availability for follow-up meetings
# - If proceeding: Call book_appointment
# - "Could you confirm your full name, email address, and preferred meeting time?"
# - Positive close: "Thank you for your time, {{name}}. We'll send you more details about our school programs and compensation structure. I'm looking forward to speaking with you soon about this exciting opportunity!"
# - Always end with end_call unless transferred
# ## Response Guidelines
# - Keep responses focused on qualifying their suitability for school coaching
# - Ask location-specific questions about Bangalore areas they can cover
# - Show genuine enthusiasm for their chess achievements and experience
# - Be respectful of their current commitments and time constraints
# - Use IST timing when scheduling appointments
# - Emphasize the opportunity to impact young minds through chess education
# - Ask only one detailed question at a time to avoid overwhelming them
# ## Scenario Handling
# ### For Highly Qualified Candidates
# - Express enthusiasm: "Your tournament experience and rating are impressive! Our partner schools would definitely value someone with your background."
# - Fast-track process: "Given your qualifications, I'd love to expedite our discussion. When would be the best time for a detailed conversation this week?"
# - Highlight premium opportunities: "With your experience, you'd be perfect for our advanced chess program placements at premium schools."
# ### For Candidates with Limited Formal Experience
# - Explore potential: "While formal ratings are helpful, we also value passion and teaching ability. Tell me about your experience working with children or young people."
# - Training emphasis: "We provide comprehensive training to help coaches develop their skills. Are you excited about growing your coaching abilities with our support?"
# - Alternative qualifications: "Have you been involved in chess clubs, online coaching, or informal teaching that might not show up in formal ratings?"
# ### For Candidates Requesting Human Assistance
# - If they want to speak with a human or need more details about compensation/partnerships:
#   - Use transfer_call
#   - Say: "Of course! Let me connect you with our placement manager who can give you detailed information about our school partnerships, compensation structure, and specific placement opportunities."
# ### For Availability Concerns
# - Flexible scheduling: "We work with various schools, so we can often accommodate different availability preferences. What times work best for you?"
# - Part-time opportunities: "Many of our coaches start part-time and gradually increase their involvement. Would that approach interest you?"
# - Location matching: "We'll match you with schools in areas convenient for you. Which parts of Bangalore are most accessible?"
# ## Knowledge Base
# ### Caller Information Variables
# - name: {{name}}
# - email: {{email}}
# - phone_number: {{phone_number}}
# - role: {{role}}
# ### 4champz Service Model
# - Leading chess coaching service provider in Bengaluru
# - Specializes in providing qualified coaches to schools across Bangalore
# - Partners with reputed schools throughout the city
# - Provides comprehensive training and curriculum support
# - Offers both part-time and full-time coaching opportunities
# - Focuses on developing young chess talent in school settings
# ### Coaching Requirements
# - School hours availability (typically 3-6 PM)
# - Ability to teach students from Classes 1-12
# - Comfort with English and preferably Kannada/Hindi
# - Transportation capability across Bangalore areas
# - Professional attitude and teaching aptitude
# - Chess knowledge appropriate for school-level instruction
# ### Assessment Criteria
# - Chess playing experience and rating (FIDE/All India Chess Federation)
# - Tournament participation and achievements
# - Prior coaching or teaching experience, especially with children
# - Educational qualifications and chess certifications
# - Language capabilities and communication skills
# - Geographic availability across Bangalore
# - Flexibility with scheduling and age groups
# ## Response Refinement
# - When discussing their chess background: "Your chess journey sounds fascinating. Could you tell me more about [specific aspect they mentioned]?"
# - When explaining opportunities: "Let me paint a picture of what coaching with our partner schools looks like..."
# - When confirming details: "Just to make sure I have everything right—you're available [summarize their availability] and comfortable teaching [summarize their preferences]. Is that accurate?"
# ## Call Management
# ### Available Functions
# - check_calendar_availability: Use when scheduling follow-up meetings
# - book_appointment: Use when confirming scheduled appointments
# - transfer_call: Use when candidate requests human assistance
# - end_call: Use to properly conclude every conversation
# ### Technical Considerations
# - If experiencing delays accessing calendar: "I'm just checking our available appointment slots. This will take just a moment."
# - If multiple scheduling needs arise: "Let me handle your appointment booking first, and then we can discuss any additional questions."
# - Always confirm appointment details before ending: "To confirm, we're scheduled for [day], [date] at [time]. You'll receive an email confirmation shortly."
# ---
# Remember that your ultimate goal is to identify qualified chess coaches who can positively impact students in Bangalore schools while ensuring they understand the opportunity and feel excited about the partnership. Accuracy in qualifying candidates and scheduling follow-ups is your top priority, followed by creating enthusiasm for the teaching opportunity and maintaining 4champz's professional reputation.
# """

# # Custom Agent Factory
# class CustomAgentFactory(AbstractAgentFactory):
#     def create_agent(self, agent_config: AgentConfig) -> BaseAgent:
#         llm = ChatGroq(model_name="llama-3.3-70b-versatile", api_key=GROQ_API_KEY)
#         return LangchainAgent(
#             agent_config=agent_config,
#             prompt_preamble=CHESS_COACH_PROMPT_PREAMBLE,
#             initial_message=BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"),
#         )

# # FastAPI App
# app = FastAPI()


# # Lifespan handler
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     logger.info("Starting up FastAPI application")
#     logger.info("Registered routes:")
#     for route in app.routes:
#         methods = getattr(route, "methods", ["WebSocket"])
#         logger.info(f" - {route.path} ({methods})")
#     yield
#     logger.info("Shutting down FastAPI application")

# app.router.lifespan_context = lifespan


# # # Log registered routes for debugging
# # @app.on_event("startup")
# # async def startup_event():
# #     print("Registered routes:")
# #     for route in app.routes:
# #         print(f" - {route.path} ({route.methods})")

# # Define the agent configuration for the inbound call
# agent_config = LangchainAgentConfig(
#     model_name="llama-3.1-8b-instant",
#     provider="groq",
#     prompt_preamble=CHESS_COACH_PROMPT_PREAMBLE,
#     initial_message=BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"),
# )

# # Define the synthesizer configuration
# synthesizer_config = GTTSSynthesizerConfig.from_telephone_output_device(
#     voice="en"
# )


# # Define the transcriber configuration (aligned with local code for telephony)
# transcriber_config = DeepgramTranscriberConfig(
#     api_key=DEEPGRAM_API_KEY,
#     sampling_rate=8000,
#     audio_encoding=AudioEncoding.MULAW,
#     chunk_size=1024,
#     endpointing_config=PunctuationEndpointingConfig(),
# )


# # Custom Telephony Server
# class CustomTelephonyServer(TelephonyServer):
#     async def handle_inbound_call(self, request: Request):
#         form_data = await request.form()
#         logger.info(f"Inbound call received with form data: {form_data}")
#         try:
#             headers = dict(request.headers)
#             headers["ngrok-skip-browser-warning"] = "true"
#             request._headers = headers
#             correct_url = f'wss://{WS_BASE_URL}/connect_call'
#             logger.info(f"Generated WebSocket URL: {correct_url}")
#             # Explicit TwiML to handle trial account prompt
#             twiml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
# <Response>
#     <Gather action="{BASE_URL}/inbound_call" method="POST" numDigits="1" timeout="10">
#         <Say>Please press any key to continue.</Say>
#     </Gather>
#     <Connect><Stream url="{correct_url}" /></Connect>
# </Response>'''
#             logger.info(f"Returning TwiML response: {twiml_content}")
#             return Response(content=twiml_content, media_type="application/xml")
#         except Exception as e:
#             logger.error(f"/inbound_call error: {str(e)}")
#             twiml = f'''<?xml version="1.0" encoding="UTF-8"?>
# <Response>
#     <Say>Error initiating conversation. Please try again later.</Say>
#     <Hangup />
# </Response>'''
#             return Response(content=twiml, media_type="application/xml")

#     async def handle_websocket(self, websocket: WebSocket, call_id: str):
#         logger.info(f"WebSocket connection attempt for call_id: {call_id}, headers: {websocket.headers}")
#         try:
#             await websocket.accept()
#             logger.info(f"WebSocket accepted for call_id: {call_id}")
#             await super().handle_websocket(websocket, call_id)
#             logger.info(f"WebSocket handling completed for call_id: {call_id}")
#         except Exception as e:
#             logger.error(f"WebSocket error for call_id {call_id}: {str(e)}")
#             await websocket.close(code=1000, reason=f"Error: {str(e)}")



# # Telephony Server configuration
# telephony_server = CustomTelephonyServer(
#     base_url=BASE_URL,
#     config_manager=InMemoryConfigManager(),
#     inbound_call_configs=[
#         TwilioInboundCallConfig(
#             twilio_config=TwilioConfig(
#                 account_sid=TWILIO_ACCOUNT_SID,
#                 auth_token=TWILIO_AUTH_TOKEN,
#             ),
#             url="/inbound_call",
#             agent_config=agent_config,
#             transcriber_config=transcriber_config,
#             synthesizer_config=synthesizer_config,
#             agent_factory=CustomAgentFactory(),
#             websocket_url=f"wss://{WS_BASE_URL}/connect_call"
#         )
#     ]
# )





# # Add custom routes
# class CallRequest(BaseModel):
#     to_phone: str

# @app.post("/make_call")
# async def trigger_call(request: CallRequest):
#     try:
#         call_sid = await make_outbound_call(request.to_phone)
#         return {"status": f"Outbound call initiated to {request.to_phone}, SID={call_sid}"}
#     except Exception as e:
#         logger.error(f"Error initiating outbound call: {str(e)}")
#         return Response(
#             content=f"Error initiating call: {str(e)}",
#             status_code=500,
#             media_type="text/plain"
#         )

# @app.get("/make_call")
# async def make_call_get(request: Request):
#     logger.warning(f"Received GET request to /make_call: {await request.body()}")
#     return Response(
#         content="Method Not Allowed: Use POST with JSON payload {'to_phone': '<number>'}",
#         status_code=405,
#         media_type="text/plain"
#     )



# @app.get("/test_deepgram")
# async def test_deepgram():
#     try:
#         transcriber = DeepgramTranscriber(transcriber_config)
#         logger.info("Deepgram API test: Successfully initialized transcriber")
#         return {"status": "Deepgram API test successful"}
#     except Exception as e:
#         logger.error(f"Deepgram API test failed: {str(e)}")
#         return {"status": f"Deepgram API test failed: {str(e)}"}

# @app.get("/test_grok")
# async def test_grok():
#     try:
#         llm = ChatGroq(model_name="llama-3.1-8b-instant", api_key=GROQ_API_KEY)
#         response = llm.invoke("Test prompt")
#         logger.info(f"Grok API test: Successfully got response: {response}")
#         return {"status": "Grok API test successful"}
#     except Exception as e:
#         logger.error(f"Grok API test failed: {str(e)}")
#         return {"status": f"Grok API test failed: {str(e)}"}

# # Add telephony routes
# app.include_router(telephony_server.get_router())


# # # Fallback webhook for debugging
# # @app.post("/twilio_webhook")
# # async def fallback_webhook(request: Request):
# #     print("Fallback webhook received:", await request.form())
# #     return {"status": "Received, but handled by Vocode"}



# # Fallback inbound call endpoint
# # @app.post("/inbound_call")
# # async def fallback_inbound_call(request: Request):
# #     form_data = await request.form()
# #     logger.info(f"Fallback /inbound_call received: {form_data}")
# #     twiml = '''<?xml version="1.0" encoding="UTF-8"?>
# # <Response>
# #     <Say>Fallback: Vocode failed to handle the call. Please try again.</Say>
# #     <Hangup />
# # </Response>'''
# #     return Response(content=twiml, media_type="application/xml")

# # # Handle GET on /inbound_call
# # @app.get("/inbound_call")
# # async def inbound_call_get(request: Request):
# #     logger.warning(f"Received GET request to /inbound_call: {await request.body()}")
# #     return Response(
# #         content="Method Not Allowed: Use POST for inbound calls",
# #         status_code=405,
# #         media_type="text/plain"
# #     )





# #Outbound call function
# async def make_outbound_call(to_phone: str):
#     logger.info(f"Initiating outbound call to {to_phone}")
#     client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#     call = await asyncio.get_event_loop().run_in_executor(
#         None,
#         lambda: client.calls.create(
#             url=f"{BASE_URL}/inbound_call",
#             to=to_phone,
#             from_=TWILIO_PHONE_NUMBER,
#         )
#     )
#     logger.info(f"Call initiated: SID={call.sid}")



# # Status callback endpoint
# @app.post("/call_status")
# async def call_status(request: Request):
#     form_data = await request.form()
#     logger.info(f"Call status callback received: {form_data}")
#     return Response(status_code=204)

# # Main block
# if __name__ == "__main__":
#     import uvicorn
#     async def run_server_and_call():
#         config = uvicorn.Config(app=app, host="0.0.0.0", port=5000)
#         server = uvicorn.Server(config)
#         server_task = asyncio.create_task(server.serve())
#         await asyncio.sleep(2)
#         await make_outbound_call("+917356793165")
#         await server_task
#     asyncio.run(run_server_and_call())











# from fastapi import FastAPI, Request, WebSocket, Response
# from fastapi.logger import logger
# from vocode.streaming.telephony.server.base import TelephonyServer, TwilioInboundCallConfig
# from vocode.streaming.models.telephony import TwilioConfig
# from vocode.streaming.agent.base_agent import BaseAgent, RespondAgent
# from vocode.streaming.models.agent import AgentConfig
# from vocode.streaming.agent.abstract_factory import AbstractAgentFactory
# from vocode.streaming.models.message import BaseMessage
# from vocode.streaming.transcriber.deepgram_transcriber import DeepgramTranscriber
# from vocode.streaming.models.transcriber import DeepgramTranscriberConfig, PunctuationEndpointingConfig, AudioEncoding
# from vocode.streaming.synthesizer.gtts_synthesizer import GTTSSynthesizer, AzureSynthesizer
# from vocode.streaming.models.synthesizer import GTTSSynthesizerConfig, AzureSynthesizerConfig
# from vocode.streaming.telephony.config_manager.in_memory_config_manager import InMemoryConfigManager
# from vocode.streaming.synthesizer.abstract_factory import AbstractSynthesizerFactory
# from langchain_groq import ChatGroq
# from twilio.rest import Client
# import os
# from dotenv import load_dotenv
# import asyncio
# from typing import Optional, Tuple
# from contextlib import asynccontextmanager
# import uvicorn
# import logging
# import time

# load_dotenv()

# # Environment variables
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
# TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
# TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
# BASE_URL = os.getenv("BASE_URL")

# # Validate environment variables
# required_vars = [GROQ_API_KEY, DEEPGRAM_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, BASE_URL]
# if not all(required_vars):
#     raise ValueError("Missing required environment variables in .env file. Check sample .env.")

# # Set WebSocket base URL
# if BASE_URL.startswith("https://"):
#     WS_BASE_URL = BASE_URL.replace("https://", "")
# elif BASE_URL.startswith("http://"):
#     WS_BASE_URL = BASE_URL.replace("http://", "")
# else:
#     WS_BASE_URL = BASE_URL

# # Ensure ffmpeg is in PATH
# os.environ['PATH'] += os.pathsep + 'C:\\ffmpeg\\bin'

# # # Chess coach prompt
# # CHESS_COACH_PROMPT_PREAMBLE = """
# # # Chess Coaching Sales Representative Prompt
# # ## Identity & Purpose
# # You are Priya, a virtual sales representative for 4champz, a leading chess coaching service provider based in Bengaluru, India. We specialize in providing qualified chess coaches to schools across Bangalore. 
# # Your primary purpose is to qualify leads who have shown interest in chess coaching opportunities, understand their background and experience, and explore potential collaboration as a chess coach for our school programs.
# # ## Voice & Persona
# # ### Personality
# # - Sound professional, warm, and conversational—like a knowledgeable chess enthusiast
# # - Project genuine interest in learning about their chess journey
# # - Maintain an engaging and respectful demeanor throughout the conversation
# # - Show respect for their time while staying focused on understanding their suitability for school coaching
# # - Convey enthusiasm about the opportunity to shape young minds through chess
# # ### Speech Characteristics
# # - Use clear, conversational language with natural flow
# # - Keep messages under 150 characters when possible
# # - Include probing questions to gather detailed information
# # - Show genuine interest in their chess background and achievements
# # - Use encouraging language when discussing their experience and qualifications
# # ## Conversation Flow
# # ### Introduction
# # 1. Start with: "Hello {{name}}, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"
# # 2. Follow with: "I'm reaching out because you expressed interest in chess coaching. I'd love to learn more about your chess background and explore how we might work together."
# # ### Current Involvement Assessment
# # - Location confirmation: "First, could you confirm your current location in Bangalore?"
# # - Chess involvement: "Tell me about your current chess involvement—are you actively playing or coaching?"
# # - Availability overview: "What does your current schedule look like, particularly during afternoon hours?"
# # ### Experience and Background Qualification
# # #### Chess playing experience:
# # - "What's your current chess rating with FIDE or All India Chess Federation?"
# # - "What's your highest tournament achievement?"
# # - "How long have you been playing chess competitively?"
# # #### Tournament participation:
# # - "Tell me about your recent tournament participation and notable results"
# # - "Have you participated in any state or national level competitions?"
# # #### Coaching and teaching experience:
# # - "Have you worked with school children before, either in chess or other subjects?"
# # - "Do you have any coaching or teaching experience, especially with children?"
# # - "Are you comfortable teaching chess in both English and Kannada/Hindi?"
# # #### Educational qualifications:
# # - "What are your educational qualifications?"
# # - "Do you have any chess certifications or coaching credentials?"
# # ### School Coaching Interest Exploration
# # - Explain the opportunity: "Let me tell you about our model—we provide qualified chess coaches to reputed schools across Bangalore. Our coaches work directly with students during school hours."
# # #### Availability assessment
# # - "Are you available for school hours, typically between 3-6 PM?"
# # - "How many days per week would you be interested in coaching?"
# # - "Which areas of Bangalore can you travel to for coaching assignments?"
# # #### Age group comfort:
# # - "Are you comfortable teaching different age groups, from Classes 1 through 12?"
# # - "Do you have any preference for specific age groups?"
# # #### Support and training:
# # - "We provide comprehensive training and curriculum support to all our coaches. How do you feel about following a structured curriculum?"
# # - "Are you interested in ongoing professional development in chess coaching?"
# # ### Schedule and Close
# # If they seem suitable and interested:
# # - "Based on our conversation, I think there could be a great fit here. I'd like to schedule a detailed discussion and assessment with you."
# # - Use check_calendar_availability for follow-up meetings
# # - If proceeding: Call book_appointment
# # - "Could you confirm your full name, email address, and preferred meeting time?"
# # - Positive close: "Thank you for your time, {{name}}. We'll send you more details about our school programs and compensation structure. I'm looking forward to speaking with you soon about this exciting opportunity!"
# # - Always end with end_call unless transferred
# # ## Response Guidelines
# # - Keep responses focused on qualifying their suitability for school coaching
# # - Ask location-specific questions about Bangalore areas they can cover
# # - Show genuine enthusiasm for their chess achievements and experience
# # - Be respectful of their current commitments and time constraints
# # - Use IST timing when scheduling appointments
# # - Emphasize the opportunity to impact young minds through chess education
# # - Ask only one detailed question at a time to avoid overwhelming them
# # ## Scenario Handling
# # ### For Highly Qualified Candidates
# # - Express enthusiasm: "Your tournament experience and rating are impressive! Our partner schools would definitely value someone with your background."
# # - Fast-track process: "Given your qualifications, I'd love to expedite our discussion. When would be the best time for a detailed conversation this week?"
# # - Highlight premium opportunities: "With your experience, you'd be perfect for our advanced chess program placements at premium schools."
# # ### For Candidates with Limited Formal Experience
# # - Explore potential: "While formal ratings are helpful, we also value passion and teaching ability. Tell me about your experience working with children or young people."
# # - Training emphasis: "We provide comprehensive training to help coaches develop their skills. Are you excited about growing your coaching abilities with our support?"
# # - Alternative qualifications: "Have you been involved in chess clubs, online coaching, or informal teaching that might not show up in formal ratings?"
# # ### For Candidates Requesting Human Assistance
# # - If they want to speak with a human or need more details about compensation/partnerships:
# #   - Use transfer_call
# #   - Say: "Of course! Let me connect you with our placement manager who can give you detailed information about our school partnerships, compensation structure, and specific placement opportunities."
# # ### For Availability Concerns
# # - Flexible scheduling: "We work with various schools, so we can often accommodate different availability preferences. What times work best for you?"
# # - Part-time opportunities: "Many of our coaches start part-time and gradually increase their involvement. Would that approach interest you?"
# # - Location matching: "We'll match you with schools in areas convenient for you. Which parts of Bangalore are most accessible?"
# # ## Knowledge Base
# # ### Caller Information Variables
# # - name: {{name}}
# # - email: {{email}}
# # - phone_number: {{phone_number}}
# # - role: {{role}}
# # ### 4champz Service Model
# # - Leading chess coaching service provider in Bengaluru
# # - Specializes in providing qualified chess coaches to schools across Bangalore
# # - Partners with reputed schools throughout the city
# # - Provides comprehensive training and curriculum support
# # - Offers both part-time and full-time coaching opportunities
# # - Focuses on developing young chess talent in school settings
# # ### Coaching Requirements
# # - School hours availability (typically 3-6 PM)
# # - Ability to teach students from Classes 1-12
# # - Comfort with English and preferably Kannada/Hindi
# # - Transportation capability across Bangalore areas
# # - Professional attitude and teaching aptitude
# # - Chess knowledge appropriate for school-level instruction
# # ### Assessment Criteria
# # - Chess playing experience and rating (FIDE/All India Chess Federation)
# # - Tournament participation and achievements
# # - Prior coaching or teaching experience, especially with children
# # - Educational qualifications and chess certifications
# # - Language capabilities and communication skills
# # - Geographic availability across Bangalore
# # - Flexibility with scheduling and age groups
# # ## Response Refinement
# # - When discussing their chess background: "Your chess journey sounds fascinating. Could you tell more about [specific aspect they mentioned]?"
# # - When explaining opportunities: "Let me paint a picture of what coaching with our partner schools looks like..."
# # - When confirming details: "Just to make sure I have everything right—you're available [summarize their availability] and comfortable teaching [summarize their preferences]. Is that accurate?"
# # ## Call Management
# # ### Available Functions
# # - check_calendar_availability: Use when scheduling follow-up meetings
# # - book_appointment: Use when confirming scheduled appointments
# # - transfer_call: Use when candidate requests human assistance
# # - end_call: Use to properly conclude every conversation
# # ### Technical Considerations
# # - If experiencing delays accessing calendar: "I'm just checking our available appointment slots. This will take just a moment."
# # - If multiple scheduling needs arise: "Let me handle your appointment booking first, and then we can discuss any additional questions."
# # - Always confirm appointment details before ending: "To confirm, we're scheduled for [day], [date] at [time]. You'll receive an email confirmation shortly."
# # ---
# # Remember that your ultimate goal is to identify qualified chess coaches who can positively impact students in Bangalore schools while ensuring they understand the opportunity and feel excited about the partnership. Accuracy in qualifying candidates and scheduling follow-ups is your top priority, followed by creating enthusiasm for the teaching opportunity and maintaining 4champz's professional reputation.
# # """



# # Trimmed chess coach prompt for faster LLM processing
# CHESS_COACH_PROMPT_PREAMBLE = """
# You are Priya, a virtual sales representative for 4champz, a chess coaching service in Bengaluru, India. Your goal is to qualify leads for chess coaching roles in schools. Be professional, warm, and conversational. Start with: "Hello, this is Priya from 4champz. Do you have 5-10 minutes to discuss chess coaching opportunities with schools in Bangalore?" Ask about their chess experience, coaching background, and availability. Keep responses concise, under 150 characters when possible. End with scheduling a follow-up or ending the call.
# """


# # Agent configuration for SpellerAgent
# class SpellerAgentConfig(AgentConfig, type="agent_speller"):
#     initial_message: BaseMessage = BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?")
#     prompt_preamble: str = CHESS_COACH_PROMPT_PREAMBLE

# # Custom SpellerAgent with fallback prompt
# class SpellerAgent(RespondAgent[SpellerAgentConfig]):
#     def __init__(self, agent_config: SpellerAgentConfig):
#         super().__init__(agent_config=agent_config)
#         self.llm = ChatGroq(model_name="llama3-8b-8192", api_key=GROQ_API_KEY)
#         logger.info("Initialized SpellerAgent with Groq LLM (llama3-8b-8192)")
#         self.last_response_time = time.time()

#     async def respond(
#         self,
#         human_input: str,
#         conversation_id: str,
#         is_interrupt: bool = False,
#     ) -> Tuple[Optional[str], bool]:
#         try:
#             start_time = time.time()
#             if not human_input and (start_time - self.last_response_time > 5):
#                 logger.info("No reply detected for 5s, sending fallback prompt")
#                 self.last_response_time = start_time
#                 return "Are you still there? I'd love to hear about your chess experience.", False
#             logger.info(f"Processing human input: {human_input}")
#             prompt = f"{self.agent_config.prompt_preamble}\n\nHuman: {human_input}\nAssistant: "
#             response = await self.llm.ainvoke([{"role": "user", "content": prompt}])
#             logger.info(f"Agent response: {response.content}, took {time.time() - start_time:.2f}s")
#             self.last_response_time = start_time
#             return response.content, False
#         except Exception as e:
#             logger.error(f"Error generating response: {str(e)}")
#             return "Sorry, I encountered an error. Please try again.", False       


# # Custom Agent Factory
# class SpellerAgentFactory(AbstractAgentFactory):
#     def create_agent(self, agent_config: AgentConfig) -> BaseAgent:
#         logger.info(f"Creating agent with config type: {agent_config.type}")
#         if isinstance(agent_config, SpellerAgentConfig):
#             logger.info("Creating SpellerAgent")
#             return SpellerAgent(agent_config=agent_config)
#         logger.error(f"Invalid agent config type: {agent_config.type}")
#         raise Exception(f"Invalid agent config: {agent_config.type}")

    



# # # Custom Synthesizer Factory
# # class GTTSSynthesizerFactory(AbstractSynthesizerFactory):
# #     def create_synthesizer(self, synthesizer_config) -> GTTSSynthesizer:
# #         logger.info(f"Creating synthesizer with config: {synthesizer_config}")
# #         if isinstance(synthesizer_config, GTTSSynthesizerConfig):
# #             logger.info("Creating GTTSSynthesizer")
# #             start_time = time.time()
# #             synthesizer = GTTSSynthesizer(synthesizer_config)
# #             logger.info(f"GTTSSynthesizer created, took {time.time() - start_time:.2f}s")
# #             return synthesizer
# #         logger.error(f"Invalid synthesizer config type: {synthesizer_config}")
# #         raise Exception(f"Invalid synthesizer config: {synthesizer_config}")    



# # Custom Synthesizer Factory
# class CustomSynthesizerFactory(AbstractSynthesizerFactory):
#     def create_synthesizer(self, synthesizer_config):
#         logger.info(f"Creating synthesizer with config: {synthesizer_config}")
#         start_time = time.time()
#         if isinstance(synthesizer_config, AzureSynthesizerConfig) and AZURE_API_KEY:
#             logger.info("Creating AzureSynthesizer")
#             synthesizer = AzureSynthesizer(synthesizer_config)
#         elif isinstance(synthesizer_config, GTTSSynthesizerConfig):
#             logger.info("Creating GTTSSynthesizer")
#             synthesizer = GTTSSynthesizer(synthesizer_config)
#         else:
#             logger.error(f"Invalid synthesizer config type: {synthesizer_config}")
#             raise Exception(f"Invalid synthesizer config: {synthesizer_config}")
#         logger.info(f"Synthesizer created, took {time.time() - start_time:.2f}s")
#         return synthesizer




# # Custom DeepgramTranscriber with enhanced logging
# class CustomDeepgramTranscriber(DeepgramTranscriber):
#     async def process(self, audio_chunk: bytes):
#         start_time = time.time()
#         logger.info(f"Processing audio chunk of size {len(audio_chunk)} bytes")
#         try:
#             result = await super().process(audio_chunk)
#             logger.info(f"Transcription result: {result}, took {time.time() - start_time:.2f}s")
#             return result
#         except Exception as e:
#             logger.error(f"Error processing audio chunk: {str(e)}")
#             raise


# # FastAPI App
# app = FastAPI()

# # Lifespan handler
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     logger.info("Starting up FastAPI application")
#     logger.info("Registered routes:")
#     for route in app.routes:
#         methods = getattr(route, "methods", ["WebSocket"])
#         logger.info(f" - {route.path} ({methods})")
#     yield
#     logger.info("Shutting down FastAPI application")

# app.router.lifespan_context = lifespan

# # Synthesizer configuration (prefer Azure if available, else GTTSSynthesizer)
# if AZURE_API_KEY:
#     synthesizer_config = AzureSynthesizerConfig(
#         subscription_key=AZURE_API_KEY,
#         region=AZURE_REGION,
#         voice_name="en-US-JennyNeural",
#         sampling_rate=8000,
#         audio_encoding=AudioEncoding.MULAW
#     )
# else:
#     synthesizer_config = GTTSSynthesizerConfig(
#         sampling_rate=8000,
#         audio_encoding=AudioEncoding.MULAW,
#         voice="en"
#     )

# # Transcriber configuration
# transcriber_config = DeepgramTranscriberConfig(
#     api_key=DEEPGRAM_API_KEY,
#     sampling_rate=8000,
#     audio_encoding=AudioEncoding.MULAW,
#     chunk_size=1024,  # Increased for stability
#     endpointing_config=PunctuationEndpointingConfig(
#         min_utterance_length=1.0,  # Relaxed for short replies
#         time_to_cut_silence=0.5   # Relaxed to reduce silence detection delay
#     ),
# )

# # Custom Telephony Server with timeout handling
# class CustomTelephonyServer(TelephonyServer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         logger.info("Initialized CustomTelephonyServer with SpellerAgentFactory and CustomSynthesizerFactory")

#     async def handle_inbound_call(self, request: Request):
#         form_data = await request.form()
#         logger.info(f"Inbound call received with form data: {form_data}")
#         try:
#             headers = dict(request.headers)
#             headers["ngrok-skip-browser-warning"] = "true"
#             request._headers = headers
#             correct_url = f'wss://{WS_BASE_URL}/connect_call'
#             logger.info(f"Generated WebSocket URL: {correct_url}")
#             twiml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
# <Response>
#     <Connect><Stream url="{correct_url}" /></Connect>
# </Response>'''
#             logger.info(f"Returning TwiML response: {twiml_content}")
#             return Response(content=twiml_content, media_type="application/xml")
#         except Exception as e:
#             logger.error(f"/inbound_call error: {str(e)}")
#             twiml = f'''<?xml version="1.0" encoding="UTF-8"?>
# <Response>
#     <Say>Error initiating conversation. Please try again later.</Say>
#     <Hangup />
# </Response>'''
#             return Response(content=twiml, media_type="application/xml")

#     async def handle_websocket(self, websocket: WebSocket, call_id: str):
#         logger.info(f"WebSocket connection attempt for call_id: {call_id}, headers: {websocket.headers}")
#         try:
#             await websocket.accept()
#             logger.info(f"WebSocket accepted for call_id: {call_id}")
#             async with asyncio.timeout(30):  # Prevent hang-up with 30s timeout
#                 await super().handle_websocket(websocket, call_id)
#             logger.info(f"WebSocket handling completed for call_id: {call_id}")
#         except asyncio.TimeoutError:
#             logger.error(f"WebSocket timeout for call_id {call_id}")
#             await websocket.close(code=1000, reason="Conversation timeout")
#         except Exception as e:
#             logger.error(f"WebSocket error for call_id {call_id}: {str(e)}")
#             await websocket.close(code=1000, reason=f"Error: {str(e)}")


# # Fallback inbound call endpoint for testing
# @app.post("/inbound_call_fallback")
# async def inbound_call_fallback(request: Request):
#     form_data = await request.form()
#     logger.info(f"Fallback inbound call received with form data: {form_data}")
#     twiml = '''<?xml version="1.0" encoding="UTF-8"?>
# <Response>
#     <Say>Hello, this is a test. You should hear this message after answering.</Say>
#     <Hangup />
# </Response>'''
#     logger.info(f"Returning fallback TwiML response: {twiml}")
#     return Response(content=twiml, media_type="application/xml")

# # Telephony Server configuration
# telephony_server = CustomTelephonyServer(
#     base_url=BASE_URL,
#     config_manager=InMemoryConfigManager(),
#     inbound_call_configs=[
#         TwilioInboundCallConfig(
#             twilio_config=TwilioConfig(
#                 account_sid=TWILIO_ACCOUNT_SID,
#                 auth_token=TWILIO_AUTH_TOKEN,
#             ),
#             url="/inbound_call",
#             agent_config=SpellerAgentConfig(),
#             transcriber_config=transcriber_config,
#             synthesizer_config=synthesizer_config,
#             agent_factory=SpellerAgentFactory(),
#             synthesizer_factory=CustomSynthesizerFactory(),
#             transcriber_factory=lambda config: CustomDeepgramTranscriber(config),
#             websocket_url=f"wss://{WS_BASE_URL}/connect_call"
#         )
#     ],
#     agent_factory=SpellerAgentFactory(),
#     synthesizer_factory=CustomSynthesizerFactory()
# )

# # Add telephony routes
# app.include_router(telephony_server.get_router())

# # Status callback endpoint
# @app.post("/call_status")
# async def call_status(request: Request):
#     form_data = await request.form()
#     call_status = form_data.get("CallStatus")
#     logger.info(f"Call status callback received: {form_data}, CallStatus: {call_status}")
#     return Response(status_code=204)

# # # Outbound call function
# # async def make_outbound_call(to_phone: str):
# #     logger.info(f"Initiating outbound call to {to_phone}")
# #     client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
# #     try:
# #         twilio_base_url = f"https://{BASE_URL}" if not BASE_URL.startswith(("http://", "https://")) else BASE_URL
# #         call = await asyncio.get_event_loop().run_in_executor(
# #             None,
# #             lambda: client.calls.create(
# #                 url=f"{twilio_base_url}/inbound_call",
# #                 to=to_phone,
# #                 from_=TWILIO_PHONE_NUMBER,
# #                 status_callback=f"{twilio_base_url}/call_status",
# #                 status_callback_method="POST",
# #                 status_callback_event=["initiated", "ringing", "answered", "completed"]
# #             )
# #         )
# #         logger.info(f"Call initiated: SID={call.sid}")
# #         return call.sid
# #     except Exception as e:
# #         logger.error(f"Error initiating Twilio call: {str(e)}")
# #         raise

# if __name__ == "__main__":
#     logger.info("Starting Uvicorn server")
#     uvicorn.run(app, host="0.0.0.0", port=3000)









# import os
# from fastapi import FastAPI, Request, WebSocket, Response
# from fastapi.logger import logger 
# from vocode.streaming.telephony.server.base import TelephonyServer, TwilioInboundCallConfig
# from vocode.streaming.models.telephony import TwilioConfig
# from vocode.streaming.models.agent import LangchainAgentConfig
# from vocode.streaming.agent.langchain_agent import LangchainAgent
# from vocode.streaming.models.message import BaseMessage
# from vocode.streaming.transcriber.deepgram_transcriber import DeepgramTranscriber
# from vocode.streaming.models.transcriber import DeepgramTranscriberConfig, AudioEncoding, PunctuationEndpointingConfig
# from vocode.streaming.synthesizer.gtts_synthesizer import GTTSSynthesizer
# from vocode.streaming.models.synthesizer import GTTSSynthesizerConfig
# from vocode.streaming.telephony.config_manager.in_memory_config_manager import InMemoryConfigManager
# from vocode.streaming.synthesizer.abstract_factory import AbstractSynthesizerFactory
# from vocode.streaming.agent.abstract_factory import AbstractAgentFactory
# from vocode.streaming.telephony.conversation.twilio_phone_conversation import TwilioPhoneConversation
# from vocode.streaming.utils import create_conversation_id
# from vocode.streaming.synthesizer.abstract_factory import AbstractSynthesizerFactory
# from vocode.streaming.transcriber.abstract_factory import AbstractTranscriberFactory
# from langchain_groq import ChatGroq
# import asyncio
# from typing import Optional, Tuple
# from contextlib import asynccontextmanager
# import uvicorn
# import logging
# import time
# from dotenv import load_dotenv
# import base64
# import json
# import httpx
# from vocode.streaming.models.events import Event, EventType
# from vocode.streaming.models.transcript import TranscriptCompleteEvent
# from vocode.streaming.utils import events_manager

# # Configure logging
# logging.basicConfig(level=logging.DEBUG)

# # Ensure ffmpeg is in PATH
# os.environ['PATH'] += os.pathsep + 'C:\\ffmpeg\\bin'

# load_dotenv()

# # Environment variables
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
# TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
# TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
# BASE_URL = os.getenv("BASE_URL")

# # Validate environment variables
# required_vars = [GROQ_API_KEY, DEEPGRAM_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, BASE_URL]
# if not all(required_vars):
#     raise ValueError("Missing required environment variables in .env file. Check sample .env.")

# # Validate Ngrok URL
# if not BASE_URL.endswith(".ngrok-free.app") and not BASE_URL.endswith(".ngrok.io"):
#     logger.warning(f"BASE_URL ({BASE_URL}) does not appear to be a valid Ngrok URL. Ensure it matches the current Ngrok session and is updated in Twilio Console.")

# # Set WebSocket base URL
# if BASE_URL.startswith("https://"):
#     WS_BASE_URL = BASE_URL.replace("https://", "")
# elif BASE_URL.startswith("http://"):
#     WS_BASE_URL = BASE_URL.replace("http://", "")
# else:
#     WS_BASE_URL = BASE_URL

# # Chess coach prompt (unchanged from your code)
# CHESS_COACH_PROMPT_PREAMBLE = """
# # Chess Coaching Sales Representative Prompt

# ## Identity & Purpose
# You are Priya, a virtual sales representative for 4champz, a leading chess coaching service provider based in Bengaluru, India. We specialize in providing qualified chess coaches to schools across Bangalore. 
# Your primary purpose is to qualify leads who have shown interest in chess coaching opportunities, understand their background and experience, and explore potential collaboration as a chess coach for our school programs.

# ## Voice & Persona

# ### Personality
# - Sound professional, warm, and conversational—like a knowledgeable chess enthusiast
# - Project genuine interest in learning about their chess journey
# - Maintain an engaging and respectful demeanor throughout the conversation
# - Show respect for their time while staying focused on understanding their suitability for school coaching
# - Convey enthusiasm about the opportunity to shape young minds through chess

# ### Speech Characteristics
# - Use clear, conversational language with natural flow
# - Keep messages under 150 characters when possible
# - Include probing questions to gather detailed information
# - Show genuine interest in their chess background and achievements
# - Use encouraging language when discussing their experience and qualifications

# ## Conversation Flow

# ### Introduction
# 1. Start with: "Hello {{name}}, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"
# 2. Follow with: "I'm reaching out because you expressed interest in chess coaching. I'd love to learn more about your chess background and explore how we might work together."

# ### Current Involvement Assessment
# - Location confirmation: "First, could you confirm your current location in Bangalore?"
# - Chess involvement: "Tell me about your current chess involvement—are you actively playing or coaching?"
# - Availability overview: "What does your current schedule look like, particularly during afternoon hours?"

# ### Experience and Background Qualification

# #### Chess playing experience:
# - "What's your current chess rating with FIDE or All India Chess Federation?"
# - "What's your highest tournament achievement?"
# - "How long have you been playing chess competitively?"

# #### Tournament participation:
# - "Tell me about your recent tournament participation and notable results"
# - "Have you participated in any state or national level competitions?"

# #### Coaching and teaching experience:
# - "Have you worked with school children before, either in chess or other subjects?"
# - "Do you have any coaching or teaching experience, especially with children?"
# - "Are you comfortable teaching chess in both English and Kannada/Hindi?"

# #### Educational qualifications:
# - "What are your educational qualifications?"
# - "Do you have any chess certifications or coaching credentials?"

# ### School Coaching Interest Exploration
# - Explain the opportunity: "Let me tell you about our model—we provide qualified chess coaches to reputed schools across Bangalore. Our coaches work directly with students during school hours."

# #### Availability assessment:
# - "Are you available for school hours, typically between 3-6 PM?"
# - "How many days per week would you be interested in coaching?"
# - "Which areas of Bangalore can you travel to for coaching assignments?"

# #### Age group comfort:
# - "Are you comfortable teaching different age groups, from Classes 1 through 12?"
# - "Do you have any preference for specific age groups?"

# #### Support and training:
# - "We provide comprehensive training and curriculum support to all our coaches. How do you feel about following a structured curriculum?"
# - "Are you interested in ongoing professional development in chess coaching?"

# ### Schedule and Close
# If they seem suitable and interested:
# - "Based on our conversation, I think there could be a great fit here. I'd like to schedule a detailed discussion and assessment with you."
# - Use check_calendar_availability for follow-up meetings
# - If proceeding: Call book_appointment
# - "Could you confirm your full name, email address, and preferred meeting time?"
# - Positive close: "Thank you for your time, {{name}}. We'll send you more details about our school programs and compensation structure. I'm looking forward to speaking with you soon about this exciting opportunity!"
# - Always end with end_call unless transferred

# ## Response Guidelines
# - Keep responses focused on qualifying their suitability for school coaching
# - Ask location-specific questions about Bangalore areas they can cover
# - Show genuine enthusiasm for their chess achievements and experience
# - Be respectful of their current commitments and time constraints
# - Use IST timing when scheduling appointments
# - Emphasize the opportunity to impact young minds through chess education
# - Ask only one detailed question at a time to avoid overwhelming them

# ## Scenario Handling

# ### For Highly Qualified Candidates
# - Express enthusiasm: "Your tournament experience and rating are impressive! Our partner schools would definitely value someone with your background."
# - Fast-track process: "Given your qualifications, I'd love to expedite our discussion. When would be the best time for a detailed conversation this week?"
# - Highlight premium opportunities: "With your experience, you'd be perfect for our advanced chess program placements at premium schools."

# ### For Candidates with Limited Formal Experience
# - Explore potential: "While formal ratings are helpful, we also value passion and teaching ability. Tell me about your experience working with children or young people."
# - Training emphasis: "We provide comprehensive training to help coaches develop their skills. Are you excited about growing your coaching abilities with our support?"
# - Alternative qualifications: "Have you been involved in chess clubs, online coaching, or informal teaching that might not show up in formal ratings?"

# ### For Candidates Requesting Human Assistance
# - If they want to speak with a human or need more details about compensation/partnerships:
#   - Use transfer_call
#   - Say: "Of course! Let me connect you with our placement manager who can give you detailed information about our school partnerships, compensation structure, and specific placement opportunities."

# ### For Availability Concerns
# - Flexible scheduling: "We work with various schools, so we can often accommodate different availability preferences. What times work best for you?"
# - Part-time opportunities: "Many of our coaches start part-time and gradually increase their involvement. Would that approach interest you?"
# - Location matching: "We'll match you with schools in areas convenient for you. Which parts of Bangalore are most accessible?"

# ## Knowledge Base

# ### Caller Information Variables
# - name: {{name}}
# - email: {{email}}
# - phone_number: {{phone_number}}
# - role: {{role}}

# ### 4champz Service Model
# - Leading chess coaching service provider in Bengaluru
# - Specializes in providing qualified coaches to schools across Bangalore
# - Partners with reputed schools throughout the city
# - Provides comprehensive training and curriculum support
# - Offers both part-time and full-time coaching opportunities
# - Focuses on developing young chess talent in school settings

# ### Coaching Requirements
# - School hours availability (typically 3-6 PM)
# - Ability to teach students from Classes 1-12
# - Comfort with English and preferably Kannada/Hindi
# - Transportation capability across Bangalore areas
# - Professional attitude and teaching aptitude
# - Chess knowledge appropriate for school-level instruction

# ### Assessment Criteria
# - Chess playing experience and rating (FIDE/All India Chess Federation)
# - Tournament participation and achievements
# - Prior coaching or teaching experience, especially with children
# - Educational qualifications and chess certifications
# - Language capabilities and communication skills
# - Geographic availability across Bangalore
# - Flexibility with scheduling and age groups

# ## Response Refinement
# - When discussing their chess background: "Your chess journey sounds fascinating. Could you tell more about [specific aspect they mentioned]?"
# - When explaining opportunities: "Let me paint a picture of what coaching with our partner schools looks like..."
# - When confirming details: "Just to make sure I have everything right—you're available [summarize their availability] and comfortable teaching [summarize their preferences]. Is that accurate?"

# ## Call Management

# ### Available Functions
# - check_calendar_availability: Use when scheduling follow-up meetings
# - book_appointment: Use when confirming scheduled appointments
# - transfer_call: Use when candidate requests human assistance
# - end_call: Use to properly conclude every conversation

# ### Technical Considerations
# - If experiencing delays accessing calendar: "I'm just checking our available appointment slots. This will take just a moment."
# - If multiple scheduling needs arise: "Let me handle your appointment booking first, and then we can discuss any additional questions."
# - Always confirm appointment details before ending: "To confirm, we're scheduled for [day], [date] at [time]. You'll receive an email confirmation shortly."

# ---
# Remember that your ultimate goal is to identify qualified chess coaches who can positively impact students in Bangalore schools while ensuring they understand the opportunity and feel excited about the partnership. Accuracy in qualifying candidates and scheduling follow-ups is your top priority, followed by creating enthusiasm for the teaching opportunity and maintaining 4champz's professional reputation.
# """

# # Groq LLM setup
# llm = ChatGroq(model_name="llama3-8b-8192")

# # Events Manager for transcript logging
# class ChessEventsManager(events_manager.EventsManager):
#     def __init__(self):
#         super().__init__(subscriptions=[EventType.TRANSCRIPT_COMPLETE])

#     async def handle_event(self, event: Event):
#         if event.type == EventType.TRANSCRIPT_COMPLETE:
#             transcript_complete_event = typing.cast(TranscriptCompleteEvent, event)
#             logger.debug(f"Transcript for conversation {transcript_complete_event.conversation_id}: {transcript_complete_event.transcript.to_string()}")
#             # Optionally send to a webhook
#             webhook_url = os.getenv("TRANSCRIPT_CALLBACK_URL")
#             if webhook_url:
#                 data = {
#                     "conversation_id": transcript_complete_event.conversation_id,
#                     "user_id": 1,  # Demo user ID
#                     "transcript": transcript_complete_event.transcript.to_string()
#                 }
#                 async with httpx.AsyncClient() as client:
#                     response = await client.post(webhook_url, json=data)
#                     if response.status_code == 200:
#                         logger.info("Transcript sent successfully to webhook")
#                     else:
#                         logger.error(f"Failed to send transcript to webhook: {response.status_code}")

# # Config Manager
# config_manager = InMemoryConfigManager()

# # Agent configuration for LangchainAgent
# class CustomLangchainAgentConfig(LangchainAgentConfig, type="agent_langchain"):
#     initial_message: BaseMessage = BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?")
#     prompt_preamble: str = CHESS_COACH_PROMPT_PREAMBLE
#     model_name: str = "llama3-8b-8192"
#     api_key: str = GROQ_API_KEY
#     provider: str = "groq"

# # Custom Agent Factory
# class LangchainAgentFactory(AbstractAgentFactory):
#     def create_agent(self, agent_config):
#         logger.debug(f"Creating agent with config type: {agent_config.type}")
#         if isinstance(agent_config, LangchainAgentConfig):
#             logger.debug("Creating CustomLangchainAgent")
#             return CustomLangchainAgent(agent_config=agent_config)
#         logger.error(f"Invalid agent config type: {agent_config.type}")
#         raise Exception(f"Invalid agent config: {agent_config.type}")

# # Custom LangchainAgent with fallback prompt
# class CustomLangchainAgent(LangchainAgent):
#     def __init__(self, agent_config: LangchainAgentConfig):
#         super().__init__(agent_config=agent_config)
#         self.last_response_time = time.time()
#         logger.debug("Initialized CustomLangchainAgent with Groq LLM (llama3-8b-8192)")

#     async def respond(
#         self,
#         human_input: str,
#         conversation_id: str,
#         is_interrupt: bool = False,
#     ) -> Tuple[Optional[str], bool]:
#         try:
#             start_time = time.time()
#             if not human_input and (start_time - self.last_response_time > 5):
#                 logger.debug("No reply detected for 5s, sending fallback prompt")
#                 self.last_response_time = start_time
#                 return "Are you still there? I'd love to hear about your chess experience.", False
#             logger.debug(f"Processing human input: {human_input}")
#             response = await super().respond(human_input, conversation_id, is_interrupt)
#             logger.debug(f"Agent response: {response[0]}, took {time.time() - start_time:.2f}s")
#             self.last_response_time = start_time
#             return response
#         except Exception as e:
#             logger.error(f"Error generating response: {str(e)}")
#             return "Sorry, I encountered an error. Please try again.", False

# # Custom Synthesizer Factory
# class GTTSSynthesizerFactory(AbstractSynthesizerFactory):
#     def create_synthesizer(self, synthesizer_config):
#         logger.debug(f"Creating synthesizer with config: {synthesizer_config}")
#         start_time = time.time()
#         if isinstance(synthesizer_config, GTTSSynthesizerConfig):
#             logger.debug("Creating GTTSSynthesizer")
#             synthesizer = GTTSSynthesizer(synthesizer_config)
#             logger.debug(f"GTTSSynthesizer created, took {time.time() - start_time:.2f}s")
#             return synthesizer
#         logger.error(f"Invalid synthesizer config type: {synthesizer_config}")
#         raise Exception(f"Invalid synthesizer config: {synthesizer_config}")

# # Custom DeepgramTranscriber with enhanced logging and audio saving
# class CustomDeepgramTranscriber(DeepgramTranscriber):
#     async def process(self, audio_chunk: bytes):
#         start_time = time.time()
#         logger.debug(f"Processing audio chunk of size {len(audio_chunk)} bytes")
#         if not audio_chunk:
#             logger.warning("Received empty audio chunk")
#             return None
#         # Save audio chunk for debugging
#         try:
#             with open(f"audio_chunk_{int(start_time)}.raw", "ab") as f:
#                 f.write(audio_chunk)
#             logger.debug(f"Saved audio chunk to audio_chunk_{int(start_time)}.raw")
#         except Exception as e:
#             logger.error(f"Error saving audio chunk: {str(e)}")
#         try:
#             result = await super().process(audio_chunk)
#             logger.debug(f"Transcription result: {result}, took {time.time() - start_time:.2f}s")
#             return result
#         except Exception as e:
#             logger.error(f"Error processing audio chunk: {str(e)}")
#             raise

# # Custom Transcriber Factory
# class CustomTranscriberFactory(AbstractTranscriberFactory):
#     def create_transcriber(self, transcriber_config):
#         logger.debug(f"Creating transcriber with config: {transcriber_config}")
#         if isinstance(transcriber_config, DeepgramTranscriberConfig):
#             logger.debug("Creating CustomDeepgramTranscriber")
#             return CustomDeepgramTranscriber(transcriber_config)
#         logger.error(f"Invalid transcriber config type: {transcriber_config}")
#         raise Exception(f"Invalid transcriber config: {transcriber_config}")

# # FastAPI App
# app = FastAPI()

# # Lifespan handler
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     logger.debug("Starting up FastAPI application")
#     logger.debug("Registered routes:")
#     for route in app.routes:
#         methods = getattr(route, "methods", ["WebSocket"])
#         logger.debug(f" - {route.path} ({methods})")
#     yield
#     logger.debug("Shutting down FastAPI application")

# app.router.lifespan_context = lifespan

# # Synthesizer configuration (aligned with your code)
# synthesizer_config = GTTSSynthesizerConfig(
#     sampling_rate=8000,
#     audio_encoding=AudioEncoding.MULAW,
#     voice="en"
# )

# # Transcriber configuration (aligned with your code)
# transcriber_config = DeepgramTranscriberConfig(
#     api_key=DEEPGRAM_API_KEY,
#     sampling_rate=8000,
#     audio_encoding=AudioEncoding.MULAW,
#     chunk_size=1024,
#     endpointing_config=PunctuationEndpointingConfig()
# )

# # Twilio configuration
# twilio_config = TwilioConfig(
#     account_sid=TWILIO_ACCOUNT_SID,
#     auth_token=TWILIO_AUTH_TOKEN
# )

# # Agent configuration
# agent_config = CustomLangchainAgentConfig(
#     llm=llm,
#     provider="groq",
#     model_name="llama3-8b-8192",
#     api_key=GROQ_API_KEY,
#     initial_message=BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"),
#     prompt_preamble=CHESS_COACH_PROMPT_PREAMBLE
# )

# # Telephony Server configuration
# telephony_server = TelephonyServer(
#     base_url=BASE_URL,
#     config_manager=config_manager,
#     inbound_call_configs=[
#         TwilioInboundCallConfig(
#             url="/inbound_call",
#             twilio_config=twilio_config,
#             agent_config=agent_config,
#             synthesizer_config=synthesizer_config,
#             transcriber_config=transcriber_config,
#             agent_factory=LangchainAgentFactory(),
#             synthesizer_factory=GTTSSynthesizerFactory(),
#             transcriber_factory=CustomTranscriberFactory()
#         )
#     ],
#     events_manager=ChessEventsManager(),
#     # logger=logger
# )

# # Add telephony routes
# app.include_router(telephony_server.get_router())

# # Status callback endpoint
# @app.post("/call_status")
# async def call_status(request: Request):
#     form_data = await request.form()
#     call_status = form_data.get("CallStatus")
#     logger.debug(f"Call status callback received: {form_data}, CallStatus: {call_status}")
#     return Response(status_code=204)

# # Fallback inbound call endpoint for testing
# @app.post("/inbound_call_fallback")
# async def inbound_call_fallback(request: Request):
#     form_data = await request.form()
#     logger.debug(f"Fallback inbound call received with form data: {form_data}")
#     twiml = '''<?xml version="1.0" encoding="UTF-8"?>
# <Response>
#     <Say>Hello, this is a test. You should hear this message after answering.</Say>
#     <Hangup />
# </Response>'''
#     logger.debug(f"Returning fallback TwiML response: {twiml}")
#     return Response(content=twiml, media_type="application/xml")

# if __name__ == "__main__":
#     logger.debug("Starting Uvicorn server")
#     uvicorn.run(app, host="0.0.0.0", port=3000)










# import os
# import logging
# import asyncio
# import httpx
# import typing
# from typing import Optional, Tuple
# from fastapi import FastAPI, Request, Response
# from fastapi.logger import logger as fastapi_logger
# from contextlib import asynccontextmanager
# from dotenv import load_dotenv
# from twilio.rest import Client
# from vocode.streaming.telephony.server.base import TelephonyServer, TwilioInboundCallConfig
# from vocode.streaming.models.telephony import TwilioConfig
# from vocode.streaming.models.agent import LangchainAgentConfig, AgentConfig
# from vocode.streaming.agent.langchain_agent import LangchainAgent
# from vocode.streaming.models.message import BaseMessage
# from vocode.streaming.transcriber.deepgram_transcriber import DeepgramTranscriber
# from vocode.streaming.models.transcriber import DeepgramTranscriberConfig, AudioEncoding, PunctuationEndpointingConfig
# from vocode.streaming.synthesizer.stream_elements_synthesizer import StreamElementsSynthesizer
# from vocode.streaming.models.synthesizer import StreamElementsSynthesizerConfig, SynthesizerConfig
# from vocode.streaming.synthesizer.base_synthesizer import BaseSynthesizer
# from vocode.streaming.telephony.config_manager.in_memory_config_manager import InMemoryConfigManager
# from vocode.streaming.agent.base_agent import BaseAgent
# from vocode.streaming.models.events import Event, EventType
# from vocode.streaming.models.transcript import TranscriptCompleteEvent
# from vocode.streaming.utils import events_manager
# from langchain_groq import ChatGroq
# import time

# # Configure logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# fastapi_logger.setLevel(logging.DEBUG)

# # Ensure ffmpeg is in PATH
# os.environ['PATH'] += os.pathsep + 'C:\\ffmpeg\\bin'

# load_dotenv()

# # Environment variables
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
# TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
# TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
# BASE_URL = os.getenv("BASE_URL")

# # Validate environment variables
# required_vars = [GROQ_API_KEY, DEEPGRAM_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, BASE_URL]
# if not all(required_vars):
#     raise ValueError("Missing required environment variables in .env file. Required: GROQ_API_KEY, DEEPGRAM_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, BASE_URL")

# # Validate Ngrok URL
# if not BASE_URL.endswith((".ngrok-free.app", ".ngrok.io")):
#     logger.warning(f"BASE_URL ({BASE_URL}) does not appear to be a valid Ngrok URL. Ensure it matches the current Ngrok session and is updated in Twilio Console.")

# # Chess coach prompt (unchanged)
# CHESS_COACH_PROMPT_PREAMBLE = """
# # Chess Coaching Sales Representative Prompt

# ## Identity & Purpose
# You are Priya, a virtual sales representative for 4champz, a leading chess coaching service provider based in Bengaluru, India. We specialize in providing qualified chess coaches to schools across Bangalore. 
# Your primary purpose is to qualify leads who have shown interest in chess coaching opportunities, understand their background and experience, and explore potential collaboration as a chess coach for our school programs.

# ## Voice & Persona

# ### Personality
# - Sound professional, warm, and conversational—like a knowledgeable chess enthusiast
# - Project genuine interest in learning about their chess journey
# - Maintain an engaging and respectful demeanor throughout the conversation
# - Show respect for their time while staying focused on understanding their suitability for school coaching
# - Convey enthusiasm about the opportunity to shape young minds through chess

# ### Speech Characteristics
# - Use clear, conversational language with natural flow
# - Keep messages under 150 characters when possible
# - Include probing questions to gather detailed information
# - Show genuine interest in their chess background and achievements
# - Use encouraging language when discussing their experience and qualifications

# ## Conversation Flow

# ### Introduction
# 1. Start with: "Hello {{name}}, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"
# 2. Follow with: "I'm reaching out because you expressed interest in chess coaching. I'd love to learn more about your chess background and explore how we might work together."

# ### Current Involvement Assessment
# - Location confirmation: "First, could you confirm your current location in Bangalore?"
# - Chess involvement: "Tell me about your current chess involvement—are you actively playing or coaching?"
# - Availability overview: "What does your current schedule look like, particularly during afternoon hours?"

# ### Experience and Background Qualification

# #### Chess playing experience:
# - "What's your current chess rating with FIDE or All India Chess Federation?"
# - "What's your highest tournament achievement?"
# - "How long have you been playing chess competitively?"

# #### Tournament participation:
# - "Tell me about your recent tournament participation and notable results"
# - "Have you participated in any state or national level competitions?"

# #### Coaching and teaching experience:
# - "Have you worked with school children before, either in chess or other subjects?"
# - "Do you have any coaching or teaching experience, especially with children?"
# - "Are you comfortable teaching chess in both English and Kannada/Hindi?"

# #### Educational qualifications:
# - "What are your educational qualifications?"
# - "Do you have any chess certifications or coaching credentials?"

# ### School Coaching Interest Exploration
# - Explain the opportunity: "Let me tell you about our model—we provide qualified chess coaches to reputed schools across Bangalore. Our coaches work directly with students during school hours."

# #### Availability assessment:
# - "Are you available for school hours, typically between 3-6 PM?"
# - "How many days per week would you be interested in coaching?"
# - "Which areas of Bangalore can you travel to for coaching assignments?"

# #### Age group comfort:
# - "Are you comfortable teaching different age groups, from Classes 1 through 12?"
# - "Do you have any preference for specific age groups?"

# #### Support and training:
# - "We provide comprehensive training and curriculum support to all our coaches. How do you feel about following a structured curriculum?"
# - "Are you interested in ongoing professional development in chess coaching?"

# ### Schedule and Close
# If they seem suitable and interested:
# - "Based on our conversation, I think there could be a great fit here. I'd like to schedule a detailed discussion and assessment with you."
# - Use check_calendar_availability for follow-up meetings
# - If proceeding: Call book_appointment
# - "Could you confirm your full name, email address, and preferred meeting time?"
# - Positive close: "Thank you for your time, {{name}}. We'll send you more details about our school programs and compensation structure. I'm looking forward to speaking with you soon about this exciting opportunity!"
# - Always end with end_call unless transferred

# ## Response Guidelines
# - Keep responses focused on qualifying their suitability for school coaching
# - Ask location-specific questions about Bangalore areas they can cover
# - Show genuine enthusiasm for their chess achievements and experience
# - Be respectful of their current commitments and time constraints
# - Use IST timing when scheduling appointments
# - Emphasize the opportunity to impact young minds through chess education
# - Ask only one detailed question at a time to avoid overwhelming them

# ## Scenario Handling

# ### For Highly Qualified Candidates
# - Express enthusiasm: "Your tournament experience and rating are impressive! Our partner schools would definitely value someone with your background."
# - Fast-track process: "Given your qualifications, I'd love to expedite our discussion. When would be the best time for a detailed conversation this week?"
# - Highlight premium opportunities: "With your experience, you'd be perfect for our advanced chess program placements at premium schools."

# ### For Candidates with Limited Formal Experience
# - Explore potential: "While formal ratings are helpful, we also value passion and teaching ability. Tell me about your experience working with children or young people."
# - Training emphasis: "We provide comprehensive training to help coaches develop their skills. Are you excited about growing your coaching abilities with our support?"
# - Alternative qualifications: "Have you been involved in chess clubs, online coaching, or informal teaching that might not show up in formal ratings?"

# ### For Candidates Requesting Human Assistance
# - If they want to speak with a human or need more details about compensation/partnerships:
#   - Use transfer_call
#   - Say: "Of course! Let me connect you with our placement manager who can give you detailed information about our school partnerships, compensation structure, and specific placement opportunities."

# ### For Availability Concerns
# - Flexible scheduling: "We work with various schools, so we can often accommodate different availability preferences. What times work best for you?"
# - Part-time opportunities: "Many of our coaches start part-time and gradually increase their involvement. Would that approach interest you?"
# - Location matching: "We'll match you with schools in areas convenient for you. Which parts of Bangalore are most accessible?"

# ## Knowledge Base

# ### Caller Information Variables
# - name: {{name}}
# - email: {{email}}
# - phone_number: {{phone_number}}
# - role: {{role}}

# ### 4champz Service Model
# - Leading chess coaching service provider in Bengaluru
# - Specializes in providing qualified coaches to schools across Bangalore
# - Partners with reputed schools throughout the city
# - Provides comprehensive training and curriculum support
# - Offers both part-time and full-time coaching opportunities
# - Focuses on developing young chess talent in school settings

# ### Coaching Requirements
# - School hours availability (typically 3-6 PM)
# - Ability to teach students from Classes 1-12
# - Comfort with English and preferably Kannada/Hindi
# - Transportation capability across Bangalore areas
# - Professional attitude and teaching aptitude
# - Chess knowledge appropriate for school-level instruction

# ### Assessment Criteria
# - Chess playing experience and rating (FIDE/All India Chess Federation)
# - Tournament participation and achievements
# - Prior coaching or teaching experience, especially with children
# - Educational qualifications and chess certifications
# - Language capabilities and communication skills
# - Geographic availability across Bangalore
# - Flexibility with scheduling and age groups

# ## Response Refinement
# - When discussing their chess background: "Your chess journey sounds fascinating. Could you tell more about [specific aspect they mentioned]?"
# - When explaining opportunities: "Let me paint a picture of what coaching with our partner schools looks like..."
# - When confirming details: "Just to make sure I have everything right—you're available [summarize their availability] and comfortable teaching [summarize their preferences]. Is that accurate?"

# ## Call Management

# ### Available Functions
# - check_calendar_availability: Use when scheduling follow-up meetings
# - book_appointment: Use when confirming scheduled appointments
# - transfer_call: Use when candidate requests human assistance
# - end_call: Use to properly conclude every conversation

# ### Technical Considerations
# - If experiencing delays accessing calendar: "I'm just checking our available appointment slots. This will take just a moment."
# - If multiple scheduling needs arise: "Let me handle your appointment booking first, and then we can discuss any additional questions."
# - Always confirm appointment details before ending: "To confirm, we're scheduled for [day], [date] at [time]. You'll receive an email confirmation shortly."

# ---
# Remember that your ultimate goal is to identify qualified chess coaches who can positively impact students in Bangalore schools while ensuring they understand the opportunity and feel excited about the partnership. Accuracy in qualifying candidates and scheduling follow-ups is your top priority, followed by creating enthusiasm for the teaching opportunity and maintaining 4champz's professional reputation.
# """

# # Groq LLM setup
# llm = ChatGroq(model_name="llama3-8b-8192")

# # Config Manager
# config_manager = InMemoryConfigManager()

# # Events Manager for transcript logging
# class ChessEventsManager(events_manager.EventsManager):
#     def __init__(self):
#         super().__init__(subscriptions=[EventType.TRANSCRIPT_COMPLETE])

#     async def handle_event(self, event: Event):
#         if event.type == EventType.TRANSCRIPT_COMPLETE:
#             transcript_complete_event = typing.cast(TranscriptCompleteEvent, event)
#             logger.debug(f"Transcript for conversation {transcript_complete_event.conversation_id}: {transcript_complete_event.transcript.to_string()}")
#             webhook_url = os.getenv("TRANSCRIPT_CALLBACK_URL")
#             if webhook_url:
#                 data = {
#                     "conversation_id": transcript_complete_event.conversation_id,
#                     "user_id": 1,  # Demo user ID
#                     "transcript": transcript_complete_event.transcript.to_string()
#                 }
#                 async with httpx.AsyncClient() as client:
#                     response = await client.post(webhook_url, json=data)
#                     if response.status_code == 200:
#                         logger.info("Transcript sent successfully to webhook")
#                     else:
#                         logger.error(f"Failed to send transcript to webhook: {response.status_code}")

# # Custom Agent Config
# class CustomLangchainAgentConfig(LangchainAgentConfig, type="agent_langchain"):
#     initial_message: BaseMessage = BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?")
#     prompt_preamble: str = CHESS_COACH_PROMPT_PREAMBLE
#     model_name: str = "llama3-8b-8192"
#     api_key: str = GROQ_API_KEY
#     provider: str = "groq"

# # Custom Langchain Agent
# class CustomLangchainAgent(LangchainAgent):
#     def __init__(self, agent_config: CustomLangchainAgentConfig):
#         super().__init__(agent_config=agent_config)
#         self.last_response_time = time.time()
#         logger.debug("Initialized CustomLangchainAgent with Groq LLM (llama3-8b-8192)")

#     async def respond(
#         self,
#         human_input: str,
#         conversation_id: str,
#         is_interrupt: bool = False,
#     ) -> Tuple[Optional[str], bool]:
#         try:
#             start_time = time.time()
#             if not human_input and (start_time - self.last_response_time > 5):
#                 logger.debug("No reply detected for 5s, sending fallback prompt")
#                 self.last_response_time = start_time
#                 return "Are you still there? I'd love to hear about your chess experience.", False
#             logger.debug(f"Processing human input: {human_input}")
#             response = await super().respond(human_input, conversation_id, is_interrupt)
#             logger.debug(f"Agent response: {response[0]}, took {time.time() - start_time:.2f}s")
#             self.last_response_time = start_time
#             return response
#         except Exception as e:
#             logger.error(f"Error generating response: {str(e)}")
#             return "Sorry, I encountered an error. Please try again.", False

# # Custom Deepgram Transcriber
# class CustomDeepgramTranscriber(DeepgramTranscriber):
#     async def process(self, audio_chunk: bytes):
#         start_time = time.time()
#         logger.debug(f"Processing audio chunk of size {len(audio_chunk)} bytes")
#         if not audio_chunk:
#             logger.warning("Received empty audio chunk")
#             return None
#         try:
#             with open(f"audio_chunk_{int(start_time)}.raw", "ab") as f:
#                 f.write(audio_chunk)
#             logger.debug(f"Saved audio chunk to audio_chunk_{int(start_time)}.raw")
#         except Exception as e:
#             logger.error(f"Error saving audio chunk: {str(e)}")
#         try:
#             result = await super().process(audio_chunk)
#             logger.debug(f"Transcription result: {result}, took {time.time() - start_time:.2f}s")
#             return result
#         except Exception as e:
#             logger.error(f"Error processing audio chunk: {str(e)}")
#             raise

# # Custom Agent Factory
# class CustomAgentFactory:
#     def create_agent(self, agent_config: AgentConfig, logger: Optional[logging.Logger] = None) -> BaseAgent:
#         log = logger or globals().get('logger', logging.getLogger(__name__))
#         log.debug(f"Creating agent with config type: {agent_config.type}")
#         log.debug(f"Agent config details: {agent_config}")
#         if agent_config.type == "agent_langchain":
#             log.debug("Creating CustomLangchainAgent")
#             return CustomLangchainAgent(agent_config=typing.cast(CustomLangchainAgentConfig, agent_config))
#         log.error(f"Invalid agent config type: {agent_config.type}")
#         raise Exception(f"Invalid agent config: {agent_config.type}")

# # Custom Synthesizer Factory
# class CustomSynthesizerFactory:
#     def create_synthesizer(self, synthesizer_config: SynthesizerConfig) -> BaseSynthesizer:
#         logger.debug(f"Creating synthesizer with config: {synthesizer_config}")
#         if isinstance(synthesizer_config, StreamElementsSynthesizerConfig):
#             logger.debug("Creating StreamElementsSynthesizer")
#             return StreamElementsSynthesizer(synthesizer_config)
#         logger.error(f"Invalid synthesizer config type: {synthesizer_config.type}")
#         raise Exception(f"Invalid synthesizer config: {synthesizer_config.type}")

# # FastAPI App
# app = FastAPI()

# # Lifespan handler
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     logger.debug("Starting up FastAPI application")
#     logger.debug("Registered routes:")
#     for route in app.routes:
#         methods = getattr(route, "methods", ["WebSocket"])
#         logger.debug(f" - {route.path} ({methods})")
#     yield
#     logger.debug("Shutting down FastAPI application")

# app.router.lifespan_context = lifespan

# # Configurations
# twilio_config = TwilioConfig(
#     account_sid=TWILIO_ACCOUNT_SID,
#     auth_token=TWILIO_AUTH_TOKEN
# )

# # Use StreamElementsSynthesizerConfig without API key
# synthesizer_config = StreamElementsSynthesizerConfig.from_telephone_output_device(
#     voice="Brian"
# )

# transcriber_config = DeepgramTranscriberConfig(
#     api_key=DEEPGRAM_API_KEY,
#     sampling_rate=8000,
#     audio_encoding=AudioEncoding.MULAW,
#     chunk_size=1024,
#     endpointing_config=PunctuationEndpointingConfig()
# )

# agent_config = CustomLangchainAgentConfig(
#     llm=llm,
#     provider="groq",
#     model_name="llama3-8b-8192",
#     api_key=GROQ_API_KEY,
#     initial_message=BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"),
#     prompt_preamble=CHESS_COACH_PROMPT_PREAMBLE
# )

# # Telephony Server
# telephony_server = TelephonyServer(
#     base_url=BASE_URL,
#     config_manager=config_manager,
#     inbound_call_configs=[
#         TwilioInboundCallConfig(
#             url="/inbound_call",
#             twilio_config=twilio_config,
#             agent_config=agent_config,
#             synthesizer_config=synthesizer_config,
#             transcriber_config=transcriber_config,
#         )
#     ],
#     agent_factory=CustomAgentFactory(),
#     synthesizer_factory=CustomSynthesizerFactory(),
#     events_manager=ChessEventsManager(),
#     # logger=logger
# )

# # Add telephony routes
# app.include_router(telephony_server.get_router())

# # Status callback endpoint
# @app.post("/call_status")
# async def call_status(request: Request):
#     form_data = await request.form()
#     call_status = form_data.get("CallStatus")
#     logger.debug(f"Call status callback received: {form_data}, CallStatus: {call_status}")
#     return Response(status_code=204)

# # Fallback inbound call endpoint
# @app.post("/inbound_call_fallback")
# async def inbound_call_fallback(request: Request):
#     form_data = await request.form()
#     logger.debug(f"Fallback inbound call received with form data: {form_data}")
#     twiml = '''<?xml version="1.0" encoding="UTF-8"?>
# <Response>
#     <Say>Hello, this is a test. You should hear this message after answering.</Say>
#     <Hangup />
# </Response>'''
#     logger.debug(f"Returning fallback TwiML response: {twiml}")
#     return Response(content=twiml, media_type="application/xml")

# # Outbound call function
# async def make_outbound_call(to_phone: str):
#     logger.info(f"Initiating outbound call to {to_phone}")
#     client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#     try:
#         twilio_base_url = f"https://{BASE_URL}" if not BASE_URL.startswith(("http://", "https://")) else BASE_URL
#         call = await asyncio.get_event_loop().run_in_executor(
#             None,
#             lambda: client.calls.create(
#                 url=f"{twilio_base_url}/inbound_call",
#                 to=to_phone,
#                 from_=TWILIO_PHONE_NUMBER,
#                 status_callback=f"{twilio_base_url}/call_status",
#                 status_callback_method="POST",
#                 status_callback_event=["initiated", "ringing", "answered", "completed"]
#             )
#         )
#         logger.info(f"Call initiated: SID={call.sid}")
#         return call.sid
#     except Exception as e:
#         logger.error(f"Error initiating Twilio call: {str(e)}")
#         raise

# # Main entry point
# if __name__ == "__main__":
#     import uvicorn
#     logger.debug("Starting Uvicorn server")
#     asyncio.run(make_outbound_call("+917356793165"))
#     uvicorn.run(app, host="0.0.0.0", port=3000)












# import os
# import logging
# import asyncio
# import httpx
# import typing
# from typing import Optional, Tuple
# from fastapi import FastAPI, Request, Response
# from fastapi.logger import logger as fastapi_logger
# from contextlib import asynccontextmanager
# from dotenv import load_dotenv
# from twilio.rest import Client
# from vocode.streaming.telephony.server.base import TelephonyServer, TwilioInboundCallConfig
# from vocode.streaming.models.telephony import TwilioConfig
# from vocode.streaming.models.agent import LangchainAgentConfig, AgentConfig
# from vocode.streaming.agent.langchain_agent import LangchainAgent
# from vocode.streaming.models.message import BaseMessage
# from vocode.streaming.transcriber.deepgram_transcriber import DeepgramTranscriber
# from vocode.streaming.models.transcriber import DeepgramTranscriberConfig, AudioEncoding, PunctuationEndpointingConfig
# from vocode.streaming.synthesizer.stream_elements_synthesizer import StreamElementsSynthesizer
# from vocode.streaming.models.synthesizer import StreamElementsSynthesizerConfig, SynthesizerConfig
# from vocode.streaming.synthesizer.base_synthesizer import BaseSynthesizer
# from vocode.streaming.telephony.config_manager.in_memory_config_manager import InMemoryConfigManager
# from vocode.streaming.agent.base_agent import BaseAgent
# from vocode.streaming.models.events import Event, EventType
# from vocode.streaming.models.transcript import TranscriptCompleteEvent
# from vocode.streaming.utils import events_manager
# from langchain_groq import ChatGroq
# import time
# import threading
# import numpy as np




# # Configure logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# fastapi_logger.setLevel(logging.DEBUG)

# # Ensure ffmpeg is in PATH
# os.environ['PATH'] += os.pathsep + 'C:\\ffmpeg\\bin'

# load_dotenv()

# # Environment variables
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
# TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
# TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
# BASE_URL = os.getenv("BASE_URL")

# # Validate environment variables
# required_vars = [GROQ_API_KEY, DEEPGRAM_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, BASE_URL]
# if not all(required_vars):
#     raise ValueError("Missing required environment variables in .env file. Required: GROQ_API_KEY, DEEPGRAM_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, BASE_URL")

# # Validate Ngrok URL
# if not BASE_URL.endswith((".ngrok-free.app", ".ngrok.io")):
#     logger.warning(f"BASE_URL ({BASE_URL}) does not appear to be a valid Ngrok URL. Ensure it matches the current Ngrok session and is updated in Twilio Console.")

# # Chess coach prompt (unchanged)
# CHESS_COACH_PROMPT_PREAMBLE = """
# # Chess Coaching Sales Representative Prompt

# ## Identity & Purpose
# You are Priya, a virtual sales representative for 4champz, a leading chess coaching service provider based in Bengaluru, India. We specialize in providing qualified chess coaches to schools across Bangalore. 
# Your primary purpose is to qualify leads who have shown interest in chess coaching opportunities, understand their background and experience, and explore potential collaboration as a chess coach for our school programs.

# ## Voice & Persona

# ### Personality
# - Sound professional, warm, and conversational—like a knowledgeable chess enthusiast
# - Project genuine interest in learning about their chess journey
# - Maintain an engaging and respectful demeanor throughout the conversation
# - Show respect for their time while staying focused on understanding their suitability for school coaching
# - Convey enthusiasm about the opportunity to shape young minds through chess

# ### Speech Characteristics
# - Use clear, conversational language with natural flow
# - Keep messages under 150 characters when possible
# - Include probing questions to gather detailed information
# - Show genuine interest in their chess background and achievements
# - Use encouraging language when discussing their experience and qualifications

# ## Conversation Flow

# ### Introduction
# 1. Start with: "Hello {{name}}, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"
# 2. Follow with: "I'm reaching out because you expressed interest in chess coaching. I'd love to learn more about your chess background and explore how we might work together."

# ### Current Involvement Assessment
# - Location confirmation: "First, could you confirm your current location in Bangalore?"
# - Chess involvement: "Tell me about your current chess involvement—are you actively playing or coaching?"
# - Availability overview: "What does your current schedule look like, particularly during afternoon hours?"

# ### Experience and Background Qualification

# #### Chess playing experience:
# - "What's your current chess rating with FIDE or All India Chess Federation?"
# - "What's your highest tournament achievement?"
# - "How long have you been playing chess competitively?"

# #### Tournament participation:
# - "Tell me about your recent tournament participation and notable results"
# - "Have you participated in any state or national level competitions?"

# #### Coaching and teaching experience:
# - "Have you worked with school children before, either in chess or other subjects?"
# - "Do you have any coaching or teaching experience, especially with children?"
# - "Are you comfortable teaching chess in both English and Kannada/Hindi?"

# #### Educational qualifications:
# - "What are your educational qualifications?"
# - "Do you have any chess certifications or coaching credentials?"

# ### School Coaching Interest Exploration
# - Explain the opportunity: "Let me tell you about our model—we provide qualified chess coaches to reputed schools across Bangalore. Our coaches work directly with students during school hours."

# #### Availability assessment:
# - "Are you available for school hours, typically between 3-6 PM?"
# - "How many days per week would you be interested in coaching?"
# - "Which areas of Bangalore can you travel to for coaching assignments?"

# #### Age group comfort:
# - "Are you comfortable teaching different age groups, from Classes 1 through 12?"
# - "Do you have any preference for specific age groups?"

# #### Support and training:
# - "We provide comprehensive training and curriculum support to all our coaches. How do you feel about following a structured curriculum?"
# - "Are you interested in ongoing professional development in chess coaching?"

# ### Schedule and Close
# If they seem suitable and interested:
# - "Based on our conversation, I think there could be a great fit here. I'd like to schedule a detailed discussion and assessment with you."
# - Use check_calendar_availability for follow-up meetings
# - If proceeding: Call book_appointment
# - "Could you confirm your full name, email address, and preferred meeting time?"
# - Positive close: "Thank you for your time, {{name}}. We'll send you more details about our school programs and compensation structure. I'm looking forward to speaking with you soon about this exciting opportunity!"
# - Always end with end_call unless transferred

# ## Response Guidelines
# - Keep responses focused on qualifying their suitability for school coaching
# - Ask location-specific questions about Bangalore areas they can cover
# - Show genuine enthusiasm for their chess achievements and experience
# - Be respectful of their current commitments and time constraints
# - Use IST timing when scheduling appointments
# - Emphasize the opportunity to impact young minds through chess education
# - Ask only one detailed question at a time to avoid overwhelming them

# ## Scenario Handling

# ### For Highly Qualified Candidates
# - Express enthusiasm: "Your tournament experience and rating are impressive! Our partner schools would definitely value someone with your background."
# - Fast-track process: "Given your qualifications, I'd love to expedite our discussion. When would be the best time for a detailed conversation this week?"
# - Highlight premium opportunities: "With your experience, you'd be perfect for our advanced chess program placements at premium schools."

# ### For Candidates with Limited Formal Experience
# - Explore potential: "While formal ratings are helpful, we also value passion and teaching ability. Tell me about your experience working with children or young people."
# - Training emphasis: "We provide comprehensive training to help coaches develop their skills. Are you excited about growing your coaching abilities with our support?"
# - Alternative qualifications: "Have you been involved in chess clubs, online coaching, or informal teaching that might not show up in formal ratings?"

# ### For Candidates Requesting Human Assistance
# - If they want to speak with a human or need more details about compensation/partnerships:
#   - Use transfer_call
#   - Say: "Of course! Let me connect you with our placement manager who can give you detailed information about our school partnerships, compensation structure, and specific placement opportunities."

# ### For Availability Concerns
# - Flexible scheduling: "We work with various schools, so we can often accommodate different availability preferences. What times work best for you?"
# - Part-time opportunities: "Many of our coaches start part-time and gradually increase their involvement. Would that approach interest you?"
# - Location matching: "We'll match you with schools in areas convenient for you. Which parts of Bangalore are most accessible?"

# ## Knowledge Base

# ### Caller Information Variables
# - name: {{name}}
# - email: {{email}}
# - phone_number: {{phone_number}}
# - role: {{role}}

# ### 4champz Service Model
# - Leading chess coaching service provider in Bengaluru
# - Specializes in providing qualified coaches to schools across Bangalore
# - Partners with reputed schools throughout the city
# - Provides comprehensive training and curriculum support
# - Offers both part-time and full-time coaching opportunities
# - Focuses on developing young chess talent in school settings

# ### Coaching Requirements
# - School hours availability (typically 3-6 PM)
# - Ability to teach students from Classes 1-12
# - Comfort with English and preferably Kannada/Hindi
# - Transportation capability across Bangalore areas
# - Professional attitude and teaching aptitude
# - Chess knowledge appropriate for school-level instruction

# ### Assessment Criteria
# - Chess playing experience and rating (FIDE/All India Chess Federation)
# - Tournament participation and achievements
# - Prior coaching or teaching experience, especially with children
# - Educational qualifications and chess certifications
# - Language capabilities and communication skills
# - Geographic availability across Bangalore
# - Flexibility with scheduling and age groups

# ## Response Refinement
# - When discussing their chess background: "Your chess journey sounds fascinating. Could you tell more about [specific aspect they mentioned]?"
# - When explaining opportunities: "Let me paint a picture of what coaching with our partner schools looks like..."
# - When confirming details: "Just to make sure I have everything right—you're available [summarize their availability] and comfortable teaching [summarize their preferences]. Is that accurate?"

# ## Call Management

# ### Available Functions
# - check_calendar_availability: Use when scheduling follow-up meetings
# - book_appointment: Use when confirming scheduled appointments
# - transfer_call: Use when candidate requests human assistance
# - end_call: Use to properly conclude every conversation

# ### Technical Considerations
# - If experiencing delays accessing calendar: "I'm just checking our available appointment slots. This will take just a moment."
# - If multiple scheduling needs arise: "Let me handle your appointment booking first, and then we can discuss any additional questions."
# - Always confirm appointment details before ending: "To confirm, we're scheduled for [day], [date] at [time]. You'll receive an email confirmation shortly."

# ---
# Remember that your ultimate goal is to identify qualified chess coaches who can positively impact students in Bangalore schools while ensuring they understand the opportunity and feel excited about the partnership. Accuracy in qualifying candidates and scheduling follow-ups is your top priority, followed by creating enthusiasm for the teaching opportunity and maintaining 4champz's professional reputation.
# """


# # Groq LLM setup
# llm = ChatGroq(model_name="llama-3.1-8b-instant")

# # Config Manager
# config_manager = InMemoryConfigManager()

# # Events Manager for transcript logging
# class ChessEventsManager(events_manager.EventsManager):
#     def __init__(self):
#         super().__init__(subscriptions=[EventType.TRANSCRIPT_COMPLETE])

#     async def handle_event(self, event: Event):
#         if event.type == EventType.TRANSCRIPT_COMPLETE:
#             transcript_complete_event = typing.cast(TranscriptCompleteEvent, event)
#             logger.debug(f"Transcript for conversation {transcript_complete_event.conversation_id}: {transcript_complete_event.transcript.to_string()}")
#             webhook_url = os.getenv("TRANSCRIPT_CALLBACK_URL")
#             if webhook_url:
#                 data = {
#                     "conversation_id": transcript_complete_event.conversation_id,
#                     "user_id": 1,  # Demo user ID
#                     "transcript": transcript_complete_event.transcript.to_string()
#                 }
#                 async with httpx.AsyncClient() as client:
#                     response = await client.post(webhook_url, json=data)
#                     if response.status_code == 200:
#                         logger.info("Transcript sent successfully to webhook")
#                     else:
#                         logger.error(f"Failed to send transcript to webhook: {response.status_code}")

# # Custom Agent Config
# class CustomLangchainAgentConfig(LangchainAgentConfig, type="agent_langchain"):
#     initial_message: BaseMessage = BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?")
#     prompt_preamble: str = CHESS_COACH_PROMPT_PREAMBLE
#     model_name: str = "llama-3.1-8b-instant"
#     api_key: str = GROQ_API_KEY
#     provider: str = "groq"

# # Custom Langchain Agent
# class CustomLangchainAgent(LangchainAgent):
#     def __init__(self, agent_config: CustomLangchainAgentConfig):
#         super().__init__(agent_config=agent_config)
#         self.last_response_time = time.time()
#         self.conversation_state = "initial"
#         self.no_input_count = 0  # Updated: Track consecutive no-input events
#         logger.debug("Initialized CustomLangchainAgent with Groq LLM (llama-3.1-8b-instant)")

#     async def respond(
#         self,
#         human_input: str,
#         conversation_id: str,
#         is_interrupt: bool = False,
#     ) -> Tuple[Optional[str], bool]:
#         try:
#             start_time = time.time()
#             # Updated: Handle no-input scenarios with counter
#             if not human_input or human_input.strip().lower() in ("", "mhmm", "okay", "what", "yes", "no"):
#                 self.no_input_count += 1
#                 logger.debug(f"No meaningful input detected (count: {self.no_input_count}, input: '{human_input}'), sending fallback prompt")
#                 if self.no_input_count >= 3:  # Updated: End call after 3 failed attempts
#                     logger.info("No valid input after 3 attempts, ending call")
#                     return "It seems we’re having trouble connecting. I’ll follow up later. Thank you!", True
#                 self.last_response_time = start_time
#                 if self.conversation_state == "initial":
#                     return "I didn't catch that clearly. Could you confirm if you're available to discuss chess coaching opportunities?", False
#                 else:
#                     return "Sorry, I didn't understand. Could you tell me about your current chess involvement?", False

#             # Updated: Reset no-input count on valid input
#             self.no_input_count = 0
#             logger.debug(f"Processing human input: {human_input}")
#             # Advance conversation state
#             if self.conversation_state == "initial" and any(word in human_input.lower() for word in ["yes", "sure", "okay", "available"]):
#                 self.conversation_state = "background"
#                 response = "Great! I'm reaching out because you expressed interest in chess coaching. First, could you confirm your current location in Bangalore?"
#             else:
#                 response = await super().respond(human_input, conversation_id, is_interrupt)
#                 if response[0] and "location" in response[0].lower():
#                     self.conversation_state = "background"

#             logger.debug(f"Agent response: {response[0]}, took {time.time() - start_time:.2f}s")
#             self.last_response_time = start_time
#             return response
#         except Exception as e:
#             logger.error(f"Error generating response: {str(e)}")
#             return "Sorry, I encountered an error. Please try again.", False

# # Custom Deepgram Transcriber
# class CustomDeepgramTranscriber(DeepgramTranscriber):
#     async def process(self, audio_chunk: bytes):
#         start_time = time.time()
#         logger.debug(f"Processing audio chunk of size {len(audio_chunk)} bytes")
#         # Updated: Validate chunk size for 16000 Hz (320 bytes for 20ms)
#         if not audio_chunk or len(audio_chunk) < 320:
#             logger.warning(f"Received invalid audio chunk (size: {len(audio_chunk)}), sending silence packet")
#             silence_packet = b"\x00" * 320
#             try:
#                 await super().process(silence_packet)
#             except Exception as e:
#                 logger.error(f"Error sending silence packet: {str(e)}")
#             return None
#         # Updated: Lower energy threshold for silence detection
#         try:
#             audio_array = np.frombuffer(audio_chunk, dtype=np.int8)
#             energy = np.sum(audio_array.astype(np.float32) ** 2)
#             logger.debug(f"Audio chunk energy: {energy}")
#             if energy < 100:  # Updated: Reduced threshold to 100
#                 logger.warning("Low energy audio detected, sending silence packet")
#                 silence_packet = b"\x00" * 320
#                 await super().process(silence_packet)
#                 return None
#         except Exception as e:
#             logger.error(f"Error analyzing audio energy: {str(e)}")

#         try:
#             # Save audio chunk for debugging
#             if os.getenv("DEBUG_AUDIO", "false").lower() == "true":
#                 with open(f"audio_chunk_{int(start_time)}.raw", "ab") as f:
#                     f.write(audio_chunk)
#                 logger.debug(f"Saved audio chunk to audio_chunk_{int(start_time)}.raw")
#             result = await super().process(audio_chunk)
#             logger.debug(f"Transcription result: {result}, took {time.time() - start_time:.2f}s")
#             return result
#         except Exception as e:
#             logger.error(f"Error processing audio chunk: {str(e)}")
#             raise

#     async def keepalive(self):
#         while True:
#             await asyncio.sleep(1)  # Updated: Reduced to 1 second for more frequent keepalives
#             try:
#                 silence_packet = b"\x00" * 320
#                 await super().process(silence_packet)
#                 logger.debug("Sent keepalive silence packet to Deepgram")
#             except Exception as e:
#                 logger.error(f"Error sending keepalive packet: {str(e)}")
#                 break

# # Custom Agent Factory
# class CustomAgentFactory:
#     def create_agent(self, agent_config: AgentConfig, logger: Optional[logging.Logger] = None) -> BaseAgent:
#         log = logger or globals().get('logger', logging.getLogger(__name__))
#         log.debug(f"Creating agent with config type: {agent_config.type}")
#         log.debug(f"Agent config details: {agent_config}")
#         if agent_config.type == "agent_langchain":
#             log.debug("Creating CustomLangchainAgent")
#             return CustomLangchainAgent(agent_config=typing.cast(CustomLangchainAgentConfig, agent_config))
#         log.error(f"Invalid agent config type: {agent_config.type}")
#         raise Exception(f"Invalid agent config: {agent_config.type}")

# # Custom Synthesizer Factory
# class CustomSynthesizerFactory:
#     def create_synthesizer(self, synthesizer_config: SynthesizerConfig) -> BaseSynthesizer:
#         logger.debug(f"Creating synthesizer with config: {synthesizer_config}")
#         if isinstance(synthesizer_config, StreamElementsSynthesizerConfig):
#             logger.debug("Creating StreamElementsSynthesizer")
#             return StreamElementsSynthesizer(synthesizer_config)
#         logger.error(f"Invalid synthesizer config type: {synthesizer_config.type}")
#         raise Exception(f"Invalid synthesizer config: {synthesizer_config.type}")

# # FastAPI App
# app = FastAPI()

# # Lifespan handler
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     logger.debug("Starting up FastAPI application")
#     logger.debug("Registered routes:")
#     for route in app.routes:
#         methods = getattr(route, "methods", ["WebSocket"])
#         logger.debug(f" - {route.path} ({methods})")
#     yield
#     logger.debug("Shutting down FastAPI application")

# app.router.lifespan_context = lifespan

# # Configurations
# twilio_config = TwilioConfig(
#     account_sid=TWILIO_ACCOUNT_SID,
#     auth_token=TWILIO_AUTH_TOKEN
# )

# # Use StreamElementsSynthesizerConfig without API key
# synthesizer_config = StreamElementsSynthesizerConfig.from_telephone_output_device(
#     voice="Brian"
# )

# transcriber_config = DeepgramTranscriberConfig(
#     api_key=DEEPGRAM_API_KEY,
#     sampling_rate=16000,
#     audio_encoding=AudioEncoding.MULAW,
#     chunk_size=320,  # Updated: Adjusted to 320 bytes for 20ms at 16000 Hz
#     endpointing_config=PunctuationEndpointingConfig(),
#     model="nova-2",
#     language="en-IN"  # Updated: Added for Indian English
# )

# agent_config = CustomLangchainAgentConfig(
#     llm=llm,
#     provider="groq",
#     model_name="llama-3.1-8b-instant",
#     api_key=GROQ_API_KEY,
#     initial_message=BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"),
#     prompt_preamble=CHESS_COACH_PROMPT_PREAMBLE
# )

# # Telephony Server
# telephony_server = TelephonyServer(
#     base_url=BASE_URL,
#     config_manager=config_manager,
#     inbound_call_configs=[
#         TwilioInboundCallConfig(
#             url="/inbound_call",
#             twilio_config=twilio_config,
#             agent_config=agent_config,
#             synthesizer_config=synthesizer_config,
#             transcriber_config=transcriber_config,
#             twiml_fallback_response='''<?xml version="1.0" encoding="UTF-8"?>
# <Response>
#     <Say>I didn't hear a response. Are you still there? Please say something to continue.</Say>
#     <Pause length="5"/>
#     <Redirect method="POST">/inbound_call</Redirect>
# </Response>'''  # Updated: Added method="POST" for consistency
#         )
#     ],
#     agent_factory=CustomAgentFactory(),
#     synthesizer_factory=CustomSynthesizerFactory(),
#     events_manager=ChessEventsManager(),
#     # logger=logger
# )

# # Add telephony routes
# app.include_router(telephony_server.get_router())

# # Status callback endpoint
# @app.post("/call_status")
# async def call_status(request: Request):
#     form_data = await request.form()
#     call_status = form_data.get("CallStatus")
#     logger.debug(f"Call status callback received: {form_data}, CallStatus: {call_status}")
#     return Response(status_code=204)

# # Fallback inbound call endpoint
# @app.post("/inbound_call_fallback")
# async def inbound_call_fallback(request: Request):
#     form_data = await request.form()
#     logger.debug(f"Fallback inbound call received with form data: {form_data}")
#     twiml = '''<?xml version="1.0" encoding="UTF-8"?>
# <Response>
#     <Say>Hello, this is a test. You should hear this message after answering.</Say>
#     <Pause length="5"/>
#     <Redirect method="POST">/inbound_call</Redirect>
# </Response>'''  # Updated: Added method="POST" for consistency
#     logger.debug(f"Returning fallback TwiML response: {twiml}")
#     return Response(content=twiml, media_type="application/xml")

# # Outbound call function
# async def make_outbound_call(to_phone: str):
#     logger.info(f"Initiating outbound call to {to_phone}")
#     client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#     try:
#         twilio_base_url = f"https://{BASE_URL}" if not BASE_URL.startswith(("http://", "https://")) else BASE_URL
#         call = await asyncio.get_event_loop().run_in_executor(
#             None,
#             lambda: client.calls.create(
#                 url=f"{twilio_base_url}/inbound_call",
#                 to=to_phone,
#                 from_=TWILIO_PHONE_NUMBER,
#                 status_callback=f"{twilio_base_url}/call_status",
#                 status_callback_method="POST",
#                 status_callback_event=["initiated", "ringing", "answered", "completed"],
#                 timeout=60
#             )
#         )
#         logger.info(f"Call initiated: SID={call.sid}")
#         return call.sid
#     except Exception as e:
#         logger.error(f"Error initiating Twilio call: {str(e)}")
#         raise

# # Main entry point
# if __name__ == "__main__":
#     import uvicorn

#     def run_server():
#         """Run the Uvicorn server in a separate thread."""
#         logger.debug("Starting Uvicorn server")
#         uvicorn.run(app, host="0.0.0.0", port=3000)

#     async def start_server_and_call():
#         """Start the keepalive task and outbound call."""
#         transcriber = CustomDeepgramTranscriber(transcriber_config)
#         keepalive_task = asyncio.create_task(transcriber.keepalive())
#         try:
#             # Start Uvicorn server in a separate thread
#             server_thread = threading.Thread(target=run_server, daemon=True)
#             server_thread.start()
#             # Wait briefly to ensure server starts
#             await asyncio.sleep(2)
#             # Make outbound call
#             await make_outbound_call("+917356793165")
#             # Keep the event loop running to handle keepalive and other async tasks
#             await asyncio.Event().wait()
#         finally:
#             keepalive_task.cancel()
#             logger.debug("Cancelled keepalive task")

#     # Run the async tasks
#     asyncio.run(start_server_and_call())













# import os
# import logging
# import asyncio
# import httpx
# import typing
# import time
# from typing import Optional, Tuple
# from fastapi import FastAPI, Request, Response
# from fastapi.logger import logger as fastapi_logger
# from contextlib import asynccontextmanager
# from dotenv import load_dotenv
# from twilio.rest import Client
# from vocode.streaming.telephony.server.base import TelephonyServer, TwilioInboundCallConfig
# from vocode.streaming.models.telephony import TwilioConfig
# from vocode.streaming.models.agent import LangchainAgentConfig, AgentConfig
# from vocode.streaming.agent.langchain_agent import LangchainAgent
# from vocode.streaming.models.message import BaseMessage
# from vocode.streaming.transcriber.deepgram_transcriber import DeepgramTranscriber
# from vocode.streaming.models.transcriber import DeepgramTranscriberConfig, AudioEncoding, PunctuationEndpointingConfig
# from vocode.streaming.synthesizer.stream_elements_synthesizer import StreamElementsSynthesizer
# from vocode.streaming.models.synthesizer import StreamElementsSynthesizerConfig, SynthesizerConfig
# from vocode.streaming.synthesizer.base_synthesizer import BaseSynthesizer
# from vocode.streaming.telephony.config_manager.in_memory_config_manager import InMemoryConfigManager
# from vocode.streaming.agent.base_agent import BaseAgent
# from vocode.streaming.models.events import Event, EventType
# from vocode.streaming.models.transcript import TranscriptCompleteEvent
# from vocode.streaming.utils import events_manager
# from langchain_groq import ChatGroq
# import threading
# import numpy as np

# # Configure logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# fastapi_logger.setLevel(logging.DEBUG)

# # Ensure ffmpeg is in PATH
# os.environ['PATH'] += os.pathsep + 'C:\\ffmpeg\\bin'

# load_dotenv()

# # Environment variables
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
# TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
# TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
# BASE_URL = os.getenv("BASE_URL")
# DEBUG_AUDIO = os.getenv("DEBUG_AUDIO", "false").lower() == "true"

# # Validate environment variables
# required_vars = [GROQ_API_KEY, DEEPGRAM_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, BASE_URL]
# if not all(required_vars):
#     raise ValueError("Missing required environment variables in .env file. Required: GROQ_API_KEY, DEEPGRAM_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, BASE_URL")

# # Validate Ngrok URL
# if not BASE_URL.endswith((".ngrok-free.app", ".ngrok.io")):
#     logger.warning(f"BASE_URL ({BASE_URL}) does not appear to be a valid Ngrok URL. Ensure it matches the current Ngrok session and is updated in Twilio Console.")

# # Chess coach prompt
# CHESS_COACH_PROMPT_PREAMBLE = """
# # Chess Coaching Sales Representative Prompt

# ## Identity & Purpose
# You are Priya, a virtual sales representative for 4champz, a leading chess coaching service provider based in Bengaluru, India. We specialize in providing qualified chess coaches to schools across Bangalore. 
# Your primary purpose is to qualify leads who have shown interest in chess coaching opportunities, understand their background and experience, and explore potential collaboration as a chess coach for our school programs.

# ## Voice & Persona

# ### Personality
# - Sound professional, warm, and conversational—like a knowledgeable chess enthusiast
# - Project genuine interest in learning about their chess journey
# - Maintain an engaging and respectful demeanor throughout the conversation
# - Show respect for their time while staying focused on understanding their suitability for school coaching
# - Convey enthusiasm about the opportunity to shape young minds through chess

# ### Speech Characteristics
# - Use clear, conversational language with natural flow
# - Keep messages under 150 characters when possible
# - Include probing questions to gather detailed information
# - Show genuine interest in their chess background and achievements
# - Use encouraging language when discussing their experience and qualifications

# ## Conversation Flow

# ### Introduction
# 1. Start with: "Hello {{name}}, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"
# 2. Follow with: "I'm reaching out because you expressed interest in chess coaching. I'd love to learn more about your chess background and explore how we might work together."

# ### Current Involvement Assessment
# - Location confirmation: "First, could you confirm your current location in Bangalore?"
# - Chess involvement: "Tell me about your current chess involvement—are you actively playing or coaching?"
# - Availability overview: "What does your current schedule look like, particularly during afternoon hours?"

# ### Experience and Background Qualification

# #### Chess playing experience:
# - "What's your current chess rating with FIDE or All India Chess Federation?"
# - "What's your highest tournament achievement?"
# - "How long have you been playing chess competitively?"

# #### Tournament participation:
# - "Tell me about your recent tournament participation and notable results"
# - "Have you participated in any state or national level competitions?"

# #### Coaching and teaching experience:
# - "Have you worked with school children before, either in chess or other subjects?"
# - "Do you have any coaching or teaching experience, especially with children?"
# - "Are you comfortable teaching chess in both English and Kannada/Hindi?"

# #### Educational qualifications:
# - "What are your educational qualifications?"
# - "Do you have any chess certifications or coaching credentials?"

# ### School Coaching Interest Exploration
# - Explain the opportunity: "Let me tell you about our model—we provide qualified chess coaches to reputed schools across Bangalore. Our coaches work directly with students during school hours."

# #### Availability assessment:
# - "Are you available for school hours, typically between 3-6 PM?"
# - "How many days per week would you be interested in coaching?"
# - "Which areas of Bangalore can you travel to for coaching assignments?"

# #### Age group comfort:
# - "Are you comfortable teaching different age groups, from Classes 1 through 12?"
# - "Do you have any preference for specific age groups?"

# #### Support and training:
# - "We provide comprehensive training and curriculum support to all our coaches. How do you feel about following a structured curriculum?"
# - "Are you interested in ongoing professional development in chess coaching?"

# ### Schedule and Close
# If they seem suitable and interested:
# - "Based on our conversation, I think there could be a great fit here. I'd like to schedule a detailed discussion and assessment with you."
# - Use check_calendar_availability for follow-up meetings
# - If proceeding: Call book_appointment
# - "Could you confirm your full name, email address, and preferred meeting time?"
# - Positive close: "Thank you for your time, {{name}}. We'll send you more details about our school programs and compensation structure. I'm looking forward to speaking with you soon about this exciting opportunity!"
# - Always end with end_call unless transferred

# ## Response Guidelines
# - Keep responses focused on qualifying their suitability for school coaching
# - Ask location-specific questions about Bangalore areas they can cover
# - Show genuine enthusiasm for their chess achievements and experience
# - Be respectful of their current commitments and time constraints
# - Use IST timing when scheduling appointments
# - Emphasize the opportunity to impact young minds through chess education
# - Ask only one detailed question at a time to avoid overwhelming them

# ## Scenario Handling

# ### For Highly Qualified Candidates
# - Express enthusiasm: "Your tournament experience and rating are impressive! Our partner schools would definitely value someone with your background."
# - Fast-track process: "Given your qualifications, I'd love to expedite our discussion. When would be the best time for a detailed conversation this week?"
# - Highlight premium opportunities: "With your experience, you'd be perfect for our advanced chess program placements at premium schools."

# ### For Candidates with Limited Formal Experience
# - Explore potential: "While formal ratings are helpful, we also value passion and teaching ability. Tell me about your experience working with children or young people."
# - Training emphasis: "We provide comprehensive training to help coaches develop their skills. Are you excited about growing your coaching abilities with our support?"
# - Alternative qualifications: "Have you been involved in chess clubs, online coaching, or informal teaching that might not show up in formal ratings?"

# ### For Candidates Requesting Human Assistance
# - If they want to speak with a human or need more details about compensation/partnerships:
#   - Use transfer_call
#   - Say: "Of course! Let me connect you with our placement manager who can give you detailed information about our school partnerships, compensation structure, and specific placement opportunities."

# ### For Availability Concerns
# - Flexible scheduling: "We work with various schools, so we can often accommodate different availability preferences. What times work best for you?"
# - Part-time opportunities: "Many of our coaches start part-time and gradually increase their involvement. Would that approach interest you?"
# - Location matching: "We'll match you with schools in areas convenient for you. Which parts of Bangalore are most accessible?"

# ## Knowledge Base

# ### Caller Information Variables
# - name: {{name}}
# - email: {{email}}
# - phone_number: {{phone_number}}
# - role: {{role}}

# ### 4champz Service Model
# - Leading chess coaching service provider in Bengaluru
# - Specializes in providing qualified coaches to schools across Bangalore
# - Partners with reputed schools throughout the city
# - Provides comprehensive training and curriculum support
# - Offers both part-time and full-time coaching opportunities
# - Focuses on developing young chess talent in school settings

# ### Coaching Requirements
# - School hours availability (typically 3-6 PM)
# - Ability to teach students from Classes 1-12
# - Comfort with English and preferably Kannada/Hindi
# - Transportation capability across Bangalore areas
# - Professional attitude and teaching aptitude
# - Chess knowledge appropriate for school-level instruction

# ### Assessment Criteria
# - Chess playing experience and rating (FIDE/All India Chess Federation)
# - Tournament participation and achievements
# - Prior coaching or teaching experience, especially with children
# - Educational qualifications and chess certifications
# - Language capabilities and communication skills
# - Geographic availability across Bangalore
# - Flexibility with scheduling and age groups

# ## Response Refinement
# - When discussing their chess background: "Your chess journey sounds fascinating. Could you tell more about [specific aspect they mentioned]?"
# - When explaining opportunities: "Let me paint a picture of what coaching with our partner schools looks like..."
# - When confirming details: "Just to make sure I have everything right—you're available [summarize their availability] and comfortable teaching [summarize their preferences]. Is that accurate?"

# ## Call Management

# ### Available Functions
# - check_calendar_availability: Use when scheduling follow-up meetings
# - book_appointment: Use when confirming scheduled appointments
# - transfer_call: Use when candidate requests human assistance
# - end_call: Use to properly conclude every conversation

# ### Technical Considerations
# - If experiencing delays accessing calendar: "I'm just checking our available appointment slots. This will take just a moment."
# - If multiple scheduling needs arise: "Let me handle your appointment booking first, and then we can discuss any additional questions."
# - Always confirm appointment details before ending: "To confirm, we're scheduled for [day], [date] at [time]. You'll receive an email confirmation shortly."

# ---
# Remember that your ultimate goal is to identify qualified chess coaches who can positively impact students in Bangalore schools while ensuring they understand the opportunity and feel excited about the partnership. Accuracy in qualifying candidates and scheduling follow-ups is your top priority, followed by creating enthusiasm for the teaching opportunity and maintaining 4champz's professional reputation.
# """

# # Groq LLM setup
# llm = ChatGroq(model_name="llama-3.1-8b-instant")

# # Config Manager
# config_manager = InMemoryConfigManager()

# # Events Manager for transcript logging
# class ChessEventsManager(events_manager.EventsManager):
#     def __init__(self):
#         super().__init__(subscriptions=[EventType.TRANSCRIPT_COMPLETE])

#     async def handle_event(self, event: Event):
#         if event.type == EventType.TRANSCRIPT_COMPLETE:
#             transcript_complete_event = typing.cast(TranscriptCompleteEvent, event)
#             logger.debug(f"Transcript for conversation {transcript_complete_event.conversation_id}: {transcript_complete_event.transcript.to_string()}")
#             webhook_url = os.getenv("TRANSCRIPT_CALLBACK_URL")
#             if webhook_url:
#                 data = {
#                     "conversation_id": transcript_complete_event.conversation_id,
#                     "user_id": 1,
#                     "transcript": transcript_complete_event.transcript.to_string()
#                 }
#                 async with httpx.AsyncClient() as client:
#                     response = await client.post(webhook_url, json=data)
#                     if response.status_code == 200:
#                         logger.info("Transcript sent successfully to webhook")
#                     else:
#                         logger.error(f"Failed to send transcript to webhook: {response.status_code}")

# # Custom Agent Config
# class CustomLangchainAgentConfig(LangchainAgentConfig, type="agent_langchain"):
#     initial_message: BaseMessage = BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?")
#     prompt_preamble: str = CHESS_COACH_PROMPT_PREAMBLE
#     model_name: str = "llama-3.1-8b-instant"
#     api_key: str = GROQ_API_KEY
#     provider: str = "groq"

# # Custom Langchain Agent
# class CustomLangchainAgent(LangchainAgent):
#     def __init__(self, agent_config: CustomLangchainAgentConfig):
#         logger.debug(f"Initializing CustomLangchainAgent with config: {agent_config}")
#         super().__init__(agent_config=agent_config)
#         self.last_response_time = time.time()
#         self.conversation_state = "initial"
#         self.no_input_count = 0
#         logger.debug("Initialized CustomLangchainAgent with Groq LLM (llama-3.1-8b-instant)")

#     async def respond(
#         self,
#         human_input: str,
#         conversation_id: str,
#         is_interrupt: bool = False,
#     ) -> Tuple[Optional[str], bool]:
#         try:
#             start_time = time.time()
#             if time.time() - self.last_response_time > 15:  # 15-second timeout
#                 logger.warning("No transcription received for 15 seconds, sending fallback")
#                 self.no_input_count += 1
#                 if self.no_input_count >= 3:
#                     logger.info("No valid input after 3 attempts, ending call")
#                     return "It seems we’re having trouble connecting. I’ll follow up later. Thank you!", True
#                 return "I didn't catch that clearly. Could you confirm if you're available to discuss chess coaching opportunities?", False

#             if not human_input or human_input.strip().lower() in ("", "mhmm", "okay", "what", "yes", "no", "a-", "four"):
#                 self.no_input_count += 1
#                 logger.debug(f"No meaningful input detected (count: {self.no_input_count}, input: '{human_input}'), sending fallback prompt")
#                 if self.no_input_count >= 3:
#                     logger.info("No valid input after 3 attempts, ending call")
#                     return "It seems we’re having trouble connecting. I’ll follow up later. Thank you!", True
#                 self.last_response_time = start_time
#                 if self.conversation_state == "initial":
#                     return "I didn't catch that clearly. Could you confirm if you're available to discuss chess coaching opportunities?", False
#                 else:
#                     return "Sorry, I didn't understand. Could you tell me about your current chess involvement?", False

#             self.no_input_count = 0
#             logger.debug(f"Processing human input: {human_input}")
#             if self.conversation_state == "initial" and any(word in human_input.lower() for word in ["yes", "sure", "okay", "available", "hello"]):
#                 self.conversation_state = "background"
#                 response = "Great! I'm reaching out because you expressed interest in chess coaching. First, could you confirm your current location in Bangalore?"
#             else:
#                 # Avoid assuming incorrect input as a name
#                 if "name is" not in human_input.lower():
#                     response = "Sorry, I might have misheard you. Could you confirm if you're available to discuss chess coaching opportunities?"
#                 else:
#                     response = await super().respond(human_input, conversation_id, is_interrupt)
#                     if response[0] and "location" in response[0].lower():
#                         self.conversation_state = "background"

#             logger.debug(f"Agent response: {response}, took {time.time() - start_time:.2f}s")
#             self.last_response_time = start_time
#             return response, False
#         except Exception as e:
#             logger.error(f"Error generating response: {str(e)}")
#             return "Sorry, I encountered an error. Please try again.", False

# # Custom Deepgram Transcriber
# class CustomDeepgramTranscriber(DeepgramTranscriber):
#     async def process(self, audio_chunk: bytes):
#         start_time = time.time()
#         logger.debug(f"Processing audio chunk of size {len(audio_chunk)} bytes")
#         if not audio_chunk or len(audio_chunk) == 0:
#             logger.warning("Received empty audio chunk, skipping")
#             return None
#         # Save audio chunk for debugging
#         timestamp = int(time.time())
#         with open(f"audio_chunk_{timestamp}.raw", "wb") as f:
#             f.write(audio_chunk)
#         logger.debug(f"Saved audio chunk to audio_chunk_{timestamp}.raw")
#         audio_array = np.frombuffer(audio_chunk, dtype=np.int8)
#         if len(audio_array) > 0 and np.var(audio_array) == 0:
#             logger.warning(f"Audio chunk appears to be silent or invalid (variance=0), skipping")
#             return None
#         try:
#             result = await super().process(audio_chunk)
#             logger.debug(f"Transcription result: {result}, took {time.time() - start_time:.2f}s")
#             return result
#         except Exception as e:
#             logger.error(f"Error processing audio chunk: {str(e)}")
#             raise

#     async def keepalive(self):
#         while True:
#             await asyncio.sleep(10)
#             try:
#                 silence_packet = b"\x00" * 160
#                 await super().process(silence_packet)
#                 logger.debug("Sent keepalive silence packet to Deepgram")
#             except Exception as e:
#                 logger.error(f"Error sending keepalive packet: {str(e)}")
#                 break

# # Custom Agent Factory
# class CustomAgentFactory:
#     def create_agent(self, agent_config: AgentConfig, logger: Optional[logging.Logger] = None) -> BaseAgent:
#         log = logger or globals().get('logger', logging.getLogger(__name__))
#         log.debug(f"Creating agent with config type: {agent_config.type}")
#         if agent_config.type == "agent_langchain":
#             log.debug("Creating CustomLangchainAgent")
#             return CustomLangchainAgent(agent_config=typing.cast(CustomLangchainAgentConfig, agent_config))
#         log.error(f"Invalid agent config type: {agent_config.type}")
#         raise Exception(f"Invalid agent config: {agent_config.type}")

# # Custom Synthesizer Factory
# class CustomSynthesizerFactory:
#     def create_synthesizer(self, synthesizer_config: SynthesizerConfig) -> BaseSynthesizer:
#         logger.debug(f"Creating synthesizer with config: {synthesizer_config}")
#         if isinstance(synthesizer_config, StreamElementsSynthesizerConfig):
#             logger.debug("Creating StreamElementsSynthesizer")
#             return StreamElementsSynthesizer(synthesizer_config)
#         logger.error(f"Invalid synthesizer config type: {synthesizer_config.type}")
#         raise Exception(f"Invalid synthesizer config: {synthesizer_config.type}")

# # FastAPI App
# app = FastAPI()

# # Lifespan handler
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     logger.debug("Starting up FastAPI application")
#     logger.debug("Registered routes:")
#     for route in app.routes:
#         methods = getattr(route, "methods", ["WebSocket"])
#         logger.debug(f" - {route.path} ({methods})")
#     yield
#     logger.debug("Shutting down FastAPI application")

# app.router.lifespan_context = lifespan

# # Configurations
# twilio_config = TwilioConfig(
#     account_sid=TWILIO_ACCOUNT_SID,
#     auth_token=TWILIO_AUTH_TOKEN
# )

# synthesizer_config = StreamElementsSynthesizerConfig.from_telephone_output_device(
#     voice="Brian"
# )

# transcriber_config = DeepgramTranscriberConfig(
#     api_key=DEEPGRAM_API_KEY,
#     sampling_rate=16000,
#     audio_encoding=AudioEncoding.LINEAR16,
#     chunk_size=320,
#     endpointing_config=PunctuationEndpointingConfig(),
#     model="nova-2-phonecall",
#     language="en",
#     vad_turnoff=200,
#     interim_results=True,
#     smart_format=True
# )

# agent_config = CustomLangchainAgentConfig(
#     llm=llm,
#     provider="groq",
#     model_name="llama-3.1-8b-instant",
#     api_key=GROQ_API_KEY,
#     initial_message=BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"),
#     prompt_preamble=CHESS_COACH_PROMPT_PREAMBLE
# )

# # Telephony Server
# telephony_server = TelephonyServer(
#     base_url=BASE_URL,
#     config_manager=config_manager,
#     inbound_call_configs=[
#         TwilioInboundCallConfig(
#             url="/inbound_call",
#             twilio_config=twilio_config,
#             agent_config=agent_config,
#             synthesizer_config=synthesizer_config,
#             transcriber_config=transcriber_config,
#             twiml_fallback_response='''<?xml version="1.0" encoding="UTF-8"?>
# <Response>
#     <Say>I didn't hear a response. Are you still there? Please say something to continue.</Say>
#     <Pause length="15"/>
#     <Redirect method="POST">/inbound_call</Redirect>
# </Response>'''
#         )
#     ],
#     agent_factory=CustomAgentFactory(),
#     synthesizer_factory=CustomSynthesizerFactory(),
#     events_manager=ChessEventsManager(),
#     # logger=logger
# )

# # Add telephony routes
# app.include_router(telephony_server.get_router())

# # Status callback endpoint
# @app.post("/call_status")
# async def call_status(request: Request):
#     form_data = await request.form()
#     call_status = form_data.get("CallStatus")
#     logger.debug(f"Call status callback received: {form_data}, CallStatus: {call_status}")
#     return Response(status_code=204)

# # Fallback inbound call endpoint
# @app.post("/inbound_call_fallback")
# async def inbound_call_fallback(request: Request):
#     form_data = await request.form()
#     logger.debug(f"Fallback inbound call received with form data: {form_data}")
#     twiml = '''<?xml version="1.0" encoding="UTF-8"?>
# <Response>
#     <Say>Hello, this is a test. You should hear this message after answering.</Say>
#     <Pause length="15"/>
#     <Redirect method="POST">/inbound_call</Redirect>
# </Response>'''
#     logger.debug(f"Returning fallback TwiML response: {twiml}")
#     return Response(content=twiml, media_type="application/xml")

# # Outbound call function
# async def make_outbound_call(to_phone: str):
#     logger.info(f"Initiating outbound call to {to_phone}")
#     client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#     try:
#         twilio_base_url = f"https://{BASE_URL}" if not BASE_URL.startswith(("http://", "https://")) else BASE_URL
#         call = await asyncio.get_event_loop().run_in_executor(
#             None,
#             lambda: client.calls.create(
#                 url=f"{twilio_base_url}/inbound_call",
#                 to=to_phone,
#                 from_=TWILIO_PHONE_NUMBER,
#                 status_callback=f"{twilio_base_url}/call_status",
#                 status_callback_method="POST",
#                 status_callback_event=["initiated", "ringing", "answered", "completed"],
#                 timeout=180,
#                 record=True,
#                 recording_channels="dual",
#                 twiml='''<?xml version="1.0" encoding="UTF-8"?>
# <Response>
#     <Start>
#         <Stream url="wss://{BASE_URL}/connect_call" track="both" />
#     </Start>
#     <Say>Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?</Say>
#     <Pause length="10"/>
# </Response>'''.replace("{BASE_URL}", BASE_URL)
#             )
#         )
#         logger.info(f"Call initiated: SID={call.sid}")
#         return call.sid
#     except Exception as e:
#         logger.error(f"Error initiating Twilio call: {str(e)}")
#         raise

# # Main entry point
# if __name__ == "__main__":
#     import uvicorn

#     def run_server():
#         logger.debug("Starting Uvicorn server")
#         uvicorn.run(app, host="0.0.0.0", port=3000)

#     async def start_server_and_call():
#         try:
#             server_thread = threading.Thread(target=run_server, daemon=True)
#             server_thread.start()
#             await asyncio.sleep(2)
#             await make_outbound_call("+917356793165")
#             await asyncio.Event().wait()
#         except Exception as e:
#             logger.error(f"Error in start_server_and_call: {str(e)}")
#             raise

#     asyncio.run(start_server_and_call())



















# import os
# import logging
# import asyncio
# import httpx
# import typing
# import time
# from typing import Optional, Tuple
# from fastapi import FastAPI, Request, Response
# from fastapi.logger import logger as fastapi_logger
# from contextlib import asynccontextmanager
# from dotenv import load_dotenv
# from twilio.rest import Client
# from vocode.streaming.telephony.server.base import TelephonyServer, TwilioInboundCallConfig
# from vocode.streaming.models.telephony import TwilioConfig
# from vocode.streaming.models.agent import LangchainAgentConfig, AgentConfig
# from vocode.streaming.agent.langchain_agent import LangchainAgent
# from vocode.streaming.models.message import BaseMessage
# from vocode.streaming.transcriber.deepgram_transcriber import DeepgramTranscriber
# from vocode.streaming.models.transcriber import DeepgramTranscriberConfig, AudioEncoding, PunctuationEndpointingConfig
# from vocode.streaming.synthesizer.stream_elements_synthesizer import StreamElementsSynthesizer
# from vocode.streaming.models.synthesizer import StreamElementsSynthesizerConfig, SynthesizerConfig
# from vocode.streaming.synthesizer.base_synthesizer import BaseSynthesizer
# from vocode.streaming.telephony.config_manager.in_memory_config_manager import InMemoryConfigManager
# from vocode.streaming.agent.base_agent import BaseAgent
# from vocode.streaming.models.events import Event, EventType
# from vocode.streaming.models.transcript import TranscriptCompleteEvent
# from vocode.streaming.utils import events_manager
# from langchain_groq import ChatGroq
# import threading
# import numpy as np


# # Configure logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# fastapi_logger.setLevel(logging.DEBUG)


# # Ensure ffmpeg is in PATH
# os.environ['PATH'] += os.pathsep + 'C:\\ffmpeg\\bin'


# load_dotenv()


# # Environment variables
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
# TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
# TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
# BASE_URL = os.getenv("BASE_URL")
# DEBUG_AUDIO = os.getenv("DEBUG_AUDIO", "false").lower() == "true"


# # Validate environment variables
# required_vars = [GROQ_API_KEY, DEEPGRAM_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, BASE_URL]
# if not all(required_vars):
#     raise ValueError("Missing required environment variables in .env file. Required: GROQ_API_KEY, DEEPGRAM_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, BASE_URL")


# # Validate Ngrok URL
# if not BASE_URL.endswith((".ngrok-free.app", ".ngrok.io")):
#     logger.warning(f"BASE_URL ({BASE_URL}) does not appear to be a valid Ngrok URL. Ensure it matches the current Ngrok session and is updated in Twilio Console.")


# # Chess coach prompt
# CHESS_COACH_PROMPT_PREAMBLE = """
# # Chess Coaching Sales Representative Prompt

# ## Identity & Purpose
# You are Priya, a virtual sales representative for 4champz, a leading chess coaching service provider based in Bengaluru, India. We specialize in providing qualified chess coaches to schools across Bangalore. 
# Your primary purpose is to qualify leads who have shown interest in chess coaching opportunities, understand their background and experience, and explore potential collaboration as a chess coach for our school programs.

# ## Voice & Persona

# ### Personality
# - Sound professional, warm, and conversational—like a knowledgeable chess enthusiast
# - Project genuine interest in learning about their chess journey
# - Maintain an engaging and respectful demeanor throughout the conversation
# - Show respect for their time while staying focused on understanding their suitability for school coaching
# - Convey enthusiasm about the opportunity to shape young minds through chess

# ### Speech Characteristics
# - Use clear, conversational language with natural flow
# - Keep messages under 150 characters when possible
# - Include probing questions to gather detailed information
# - Show genuine interest in their chess background and achievements
# - Use encouraging language when discussing their experience and qualifications

# ## Conversation Flow

# ### Introduction
# 1. Start with: "Hello {{name}}, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"
# 2. Follow with: "I'm reaching out because you expressed interest in chess coaching. I'd love to learn more about your chess background and explore how we might work together."

# ### Current Involvement Assessment
# - Location confirmation: "First, could you confirm your current location in Bangalore?"
# - Chess involvement: "Tell me about your current chess involvement—are you actively playing or coaching?"
# - Availability overview: "What does your current schedule look like, particularly during afternoon hours?"

# ### Experience and Background Qualification

# #### Chess playing experience:
# - "What's your current chess rating with FIDE or All India Chess Federation?"
# - "What's your highest tournament achievement?"
# - "How long have you been playing chess competitively?"

# #### Tournament participation:
# - "Tell me about your recent tournament participation and notable results"
# - "Have you participated in any state or national level competitions?"

# #### Coaching and teaching experience:
# - "Have you worked with school children before, either in chess or other subjects?"
# - "Do you have any coaching or teaching experience, especially with children?"
# - "Are you comfortable teaching chess in both English and Kannada/Hindi?"

# #### Educational qualifications:
# - "What are your educational qualifications?"
# - "Do you have any chess certifications or coaching credentials?"

# ### School Coaching Interest Exploration
# - Explain the opportunity: "Let me tell you about our model—we provide qualified chess coaches to reputed schools across Bangalore. Our coaches work directly with students during school hours."

# #### Availability assessment:
# - "Are you available for school hours, typically between 3-6 PM?"
# - "How many days per week would you be interested in coaching?"
# - "Which areas of Bangalore can you travel to for coaching assignments?"

# #### Age group comfort:
# - "Are you comfortable teaching different age groups, from Classes 1 through 12?"
# - "Do you have any preference for specific age groups?"

# #### Support and training:
# - "We provide comprehensive training and curriculum support to all our coaches. How do you feel about following a structured curriculum?"
# - "Are you interested in ongoing professional development in chess coaching?"

# ### Schedule and Close
# If they seem suitable and interested:
# - "Based on our conversation, I think there could be a great fit here. I'd like to schedule a detailed discussion and assessment with you."
# - Use check_calendar_availability for follow-up meetings
# - If proceeding: Call book_appointment
# - "Could you confirm your full name, email address, and preferred meeting time?"
# - Positive close: "Thank you for your time, {{name}}. We'll send you more details about our school programs and compensation structure. I'm looking forward to speaking with you soon about this exciting opportunity!"
# - Always end with end_call unless transferred

# ## Response Guidelines
# - Keep responses focused on qualifying their suitability for school coaching
# - Ask location-specific questions about Bangalore areas they can cover
# - Show genuine enthusiasm for their chess achievements and experience
# - Be respectful of their current commitments and time constraints
# - Use IST timing when scheduling appointments
# - Emphasize the opportunity to impact young minds through chess education
# - Ask only one detailed question at a time to avoid overwhelming them

# ## Scenario Handling

# ### For Highly Qualified Candidates
# - Express enthusiasm: "Your tournament experience and rating are impressive! Our partner schools would definitely value someone with your background."
# - Fast-track process: "Given your qualifications, I'd love to expedite our discussion. When would be the best time for a detailed conversation this week?"
# - Highlight premium opportunities: "With your experience, you'd be perfect for our advanced chess program placements at premium schools."

# ### For Candidates with Limited Formal Experience
# - Explore potential: "While formal ratings are helpful, we also value passion and teaching ability. Tell me about your experience working with children or young people."
# - Training emphasis: "We provide comprehensive training to help coaches develop their skills. Are you excited about growing your coaching abilities with our support?"
# - Alternative qualifications: "Have you been involved in chess clubs, online coaching, or informal teaching that might not show up in formal ratings?"

# ### For Candidates Requesting Human Assistance
# - If they want to speak with a human or need more details about compensation/partnerships:
#   - Use transfer_call
#   - Say: "Of course! Let me connect you with our placement manager who can give you detailed information about our school partnerships, compensation structure, and specific placement opportunities."

# ### For Availability Concerns
# - Flexible scheduling: "We work with various schools, so we can often accommodate different availability preferences. What times work best for you?"
# - Part-time opportunities: "Many of our coaches start part-time and gradually increase their involvement. Would that approach interest you?"
# - Location matching: "We'll match you with schools in areas convenient for you. Which parts of Bangalore are most accessible?"

# ## Knowledge Base

# ### Caller Information Variables
# - name: {{name}}
# - email: {{email}}
# - phone_number: {{phone_number}}
# - role: {{role}}

# ### 4champz Service Model
# - Leading chess coaching service provider in Bengaluru
# - Specializes in providing qualified coaches to schools across Bangalore
# - Partners with reputed schools throughout the city
# - Provides comprehensive training and curriculum support
# - Offers both part-time and full-time coaching opportunities
# - Focuses on developing young chess talent in school settings

# ### Coaching Requirements
# - School hours availability (typically 3-6 PM)
# - Ability to teach students from Classes 1-12
# - Comfort with English and preferably Kannada/Hindi
# - Transportation capability across Bangalore areas
# - Professional attitude and teaching aptitude
# - Chess knowledge appropriate for school-level instruction

# ### Assessment Criteria
# - Chess playing experience and rating (FIDE/All India Chess Federation)
# - Tournament participation and achievements
# - Prior coaching or teaching experience, especially with children
# - Educational qualifications and chess certifications
# - Language capabilities and communication skills
# - Geographic availability across Bangalore
# - Flexibility with scheduling and age groups

# ## Response Refinement
# - When discussing their chess background: "Your chess journey sounds fascinating. Could you tell more about [specific aspect they mentioned]?"
# - When explaining opportunities: "Let me paint a picture of what coaching with our partner schools looks like..."
# - When confirming details: "Just to make sure I have everything right—you're available [summarize their availability] and comfortable teaching [summarize their preferences]. Is that accurate?"

# ## Call Management

# ### Available Functions
# - check_calendar_availability: Use when scheduling follow-up meetings
# - book_appointment: Use when confirming scheduled appointments
# - transfer_call: Use when candidate requests human assistance
# - end_call: Use to properly conclude every conversation

# ## Technical Considerations
# - If experiencing delays accessing calendar: "I'm just checking our available appointment slots. This will take just a moment."
# - If multiple scheduling needs arise: "Let me handle your appointment booking first, and then we can discuss any additional questions."
# - Always confirm appointment details before ending: "To confirm, we're scheduled for [day], [date] at [time]. You'll receive an email confirmation shortly."

# ---
# Remember that your ultimate goal is to identify qualified chess coaches who can positively impact students in Bangalore schools while ensuring they understand the opportunity and feel excited about the partnership. Accuracy in qualifying candidates and scheduling follow-ups is your top priority, followed by creating enthusiasm for the teaching opportunity and maintaining 4champz's professional reputation.
# """


# # Groq LLM setup
# llm = ChatGroq(model_name="llama-3.1-8b-instant")


# # Config Manager
# config_manager = InMemoryConfigManager()


# # Events Manager to log transcripts
# class ChessEventsManager(events_manager.EventsManager):
#     def __init__(self):
#         super().__init__(subscriptions=[EventType.TRANSCRIPT_COMPLETE])

#     async def handle_event(self, event: Event):
#         if event.type == EventType.TRANSCRIPT_COMPLETE:
#             transcript_complete_event = typing.cast(TranscriptCompleteEvent, event)
#             logger.debug(f"Transcript for conversation {transcript_complete_event.conversation_id}: {transcript_complete_event.transcript.to_string()}")
#             webhook_url = os.getenv("TRANSCRIPT_CALLBACK_URL")
#             if webhook_url:
#                 data = {"conversation_id": transcript_complete_event.conversation_id, "user_id": 1, "transcript": transcript_complete_event.transcript.to_string()}
#                 async with httpx.AsyncClient() as client:
#                     response = await client.post(webhook_url, json=data)
#                     if response.status_code == 200:
#                         logger.info("Transcript sent successfully to webhook")
#                     else:
#                         logger.error(f"Failed to send transcript to webhook: {response.status_code}")


# # Custom Agent Config
# class CustomLangchainAgentConfig(LangchainAgentConfig, type="agent_langchain"):
#     initial_message: BaseMessage = BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?")
#     prompt_preamble: str = CHESS_COACH_PROMPT_PREAMBLE
#     model_name: str = "llama-3.1-8b-instant"
#     api_key: str = GROQ_API_KEY
#     provider: str = "groq"


# # Custom Langchain Agent
# class CustomLangchainAgent(LangchainAgent):
#     def __init__(self, agent_config: CustomLangchainAgentConfig):
#         logger.debug(f"Initializing CustomLangchainAgent with config: {agent_config}")
#         super().__init__(agent_config=agent_config)
#         self.last_response_time = time.time()
#         self.conversation_state = "initial"
#         self.no_input_count = 0
#         self.user_name = None  # store extracted/confirmed name
#         logger.debug("Initialized CustomLangchainAgent with Groq LLM (llama-3.1-8b-instant)")

#     async def respond(self, human_input: str, conversation_id: str, is_interrupt: bool = False) -> Tuple[Optional[str], bool]:
#         try:
#             start_time = time.time()

#             # Helper function to sanitize / replace {name} placeholder in bot replies
#             def personalize_response(text: str) -> str:
#                 if self.user_name:
#                     return text.replace("{name}", self.user_name)
#                 else:
#                     # Remove or replace with generic fallback if no name known
#                     return text.replace("{name}", "there")

#             # Timeout: fallback if no transcription for 15s
#             if time.time() - self.last_response_time > 15:
#                 self.no_input_count += 1
#                 logger.warning(f"No transcription for 15 seconds (attempt {self.no_input_count}), sending fallback")
#                 if self.no_input_count >= 3:
#                     logger.info("No valid input after 3 fallback attempts, ending call")
#                     return personalize_response("It seems we’re having trouble connecting. I’ll follow up later. Thank you!"), True
#                 return personalize_response("I didn't catch that clearly. Could you confirm if you're available to discuss chess coaching opportunities?"), False

#             # Normalize input for checks
#             normalized = (human_input or "").strip().lower()

#             # Basic heuristic: ignore very short or common filler responses
#             filler_phrases = {"", "mhmm", "okay", "what", "yes", "no", "a-", "four", "hello", "hi"}
#             if normalized in filler_phrases:
#                 self.no_input_count += 1
#                 logger.debug(f"Detected filler/no meaningful input (count {self.no_input_count}): '{human_input}'")
#                 if self.no_input_count >= 3:
#                     logger.info("No valid input after 3 attempts, ending call")
#                     return personalize_response("It seems we’re having trouble connecting. I’ll follow up later. Thank you!"), True
#                 self.last_response_time = start_time
#                 # Different prompt depending on conversation state
#                 if self.conversation_state == "initial":
#                     return personalize_response("I didn't catch that clearly. Could you confirm if you're available to discuss chess coaching opportunities?"), False
#                 else:
#                     return personalize_response("Sorry, I didn't understand. Could you tell me about your current chess involvement?"), False

#             # If input looks like gibberish or incomplete question (simple heuristic)
#             gibberish_indicators = ["what is the first time", "first time", "please repeat", "say again"]
#             if any(phrase in normalized for phrase in gibberish_indicators):
#                 logger.debug(f"Input looks like unclear/gibberish: '{human_input}', prompting clarification")
#                 self.no_input_count += 1
#                 if self.no_input_count >= 3:
#                     logger.info("No valid input after 3 unclear attempts, ending call")
#                     return personalize_response("It seems we’re having trouble connecting. I’ll follow up later. Thank you!"), True
#                 self.last_response_time = start_time
#                 return personalize_response("Sorry, I didn't catch that. Could you please repeat or say yes/no if you're available?"), False

#             # Reset no input count on valid input
#             self.no_input_count = 0

#             # Try extract user name from input if mentioned (very basic detection)
#             # e.g. "My name is Priya"
#             if "name is" in normalized:
#                 try:
#                     # Extract after "name is"
#                     name_part = human_input.lower().split("name is", 1)[1].strip().split()[0]
#                     self.user_name = name_part.capitalize()
#                     logger.debug(f"Extracted user name: {self.user_name}")
#                 except Exception:
#                     # fallback to generic
#                     self.user_name = None

#             # Conversation state machine
#             if self.conversation_state == "initial":
#                 # Expect positive confirmation to move forward
#                 if any(word in normalized for word in ["yes", "sure", "okay", "available"]):
#                     self.conversation_state = "background"
#                     response = "Great! I'm reaching out because you expressed interest in chess coaching. First, could you confirm your current location in Bangalore?"
#                 else:
#                     response = personalize_response("Sorry, I might have misheard you. Could you confirm if you're available to discuss chess coaching opportunities?")
#                 self.last_response_time = start_time
#                 logger.debug(f"Agent response: {response}")
#                 return response, False

#             # After initial state, forward input to langchain super() for processing
#             else:
#                 response, should_end = await super().respond(human_input, conversation_id, is_interrupt)
#                 if response:
#                     response_text = response
#                     # Personalize {name} if present
#                     response_text = personalize_response(response_text)
#                     # If response asks location, confirm we moved to background state
#                     if "location" in response_text.lower():
#                         self.conversation_state = "background"
#                     self.last_response_time = start_time
#                     logger.debug(f"Agent super responded: {response_text}, should_end={should_end}")
#                     return response_text, should_end

#                 # Fallback generic message if super returns nothing
#                 fallback_msg = personalize_response("Sorry, I didn't quite get that. Could you please tell me more?")
#                 self.last_response_time = start_time
#                 return fallback_msg, False

#         except Exception as e:
#             logger.error(f"Error generating response: {str(e)}")
#             fallback_error_msg = personalize_response("Sorry, I encountered an error. Please try again.")
#             return fallback_error_msg, False


# # Custom Deepgram Transcriber with keepalive and chunk logging
# class CustomDeepgramTranscriber(DeepgramTranscriber):
#     def __init__(self, transcriber_config: DeepgramTranscriberConfig):
#         super().__init__(transcriber_config)
#     async def process(self, audio_chunk: bytes):
#         logger.debug(f"Processing audio chunk size: {len(audio_chunk)} bytes")  # Added
#         if not audio_chunk or len(audio_chunk) == 0:
#             logger.warning("Empty audio chunk - skipping")
#             return None
#         try:
#             return await super().process(audio_chunk)
#         except Exception as e:
#             logger.error(f"Deepgram process error: {e}")
#             raise
#     async def keepalive(self):
#         while True:
#             await asyncio.sleep(10)
#             try:
#                 await super().process(b"\x00" * 160)
#                 logger.debug("Deepgram keepalive sent")
#             except Exception as e:
#                 logger.error(f"Keepalive failed: {e}")
#                 break

# # Custom Agent Factory
# class CustomAgentFactory:
#     def create_agent(self, agent_config: AgentConfig, logger: Optional[logging.Logger] = None) -> BaseAgent:
#         log = logger or globals().get('logger', logging.getLogger(__name__))
#         log.debug(f"Creating agent with config type: {agent_config.type}")
#         if agent_config.type == "agent_langchain":
#             log.debug("Creating CustomLangchainAgent")
#             return CustomLangchainAgent(agent_config=typing.cast(CustomLangchainAgentConfig, agent_config))
#         log.error(f"Invalid agent config type: {agent_config.type}")
#         raise Exception(f"Invalid agent config: {agent_config.type}")


# # Custom Synthesizer Factory
# class CustomSynthesizerFactory:
#     def create_synthesizer(self, synthesizer_config: SynthesizerConfig) -> BaseSynthesizer:
#         logger.debug(f"Creating synthesizer with config: {synthesizer_config}")
#         if isinstance(synthesizer_config, StreamElementsSynthesizerConfig):
#             logger.debug("Creating StreamElementsSynthesizer")
#             return StreamElementsSynthesizer(synthesizer_config)
#         logger.error(f"Invalid synthesizer config type: {synthesizer_config.type}")
#         raise Exception(f"Invalid synthesizer config: {synthesizer_config.type}")


# # FastAPI App
# app = FastAPI()


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     logger.debug("Starting up FastAPI application")
#     logger.debug("Registered routes:")
#     for route in app.routes:
#         methods = getattr(route, "methods", ["WebSocket"])
#         logger.debug(f" - {route.path} ({methods})")
#     yield
#     logger.debug("Shutting down FastAPI application")


# app.router.lifespan_context = lifespan


# # Twilio config
# twilio_config = TwilioConfig(
#     account_sid=TWILIO_ACCOUNT_SID,
#     auth_token=TWILIO_AUTH_TOKEN
# )


# # Synthesizer config (telephone voice output)
# synthesizer_config = StreamElementsSynthesizerConfig.from_telephone_output_device(
#     voice="Brian"
# )


# transcriber_config = DeepgramTranscriberConfig(
#     api_key=DEEPGRAM_API_KEY,
#     model="nova-2-phonecall",
#     language="en",
#     sampling_rate=8000,  # int primitive, not enum
#     audio_encoding="mulaw",  # lowercase string, not enum
#     chunk_size=320,
#     endpointing_config=PunctuationEndpointingConfig(),
#     downsampling=1,
# )



# agent_config = LangchainAgentConfig(
#     initial_message=BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"),
#     prompt_preamble=CHESS_COACH_PROMPT_PREAMBLE,
#     model_name="llama-3.1-8b-instant",
#     api_key=GROQ_API_KEY,
#     provider="groq",
# )


# # Create CustomDeepgramTranscriber instance with config
# # custom_deepgram_transcriber = CustomDeepgramTranscriber(transcriber_config)


# # Telephony Server setup
# telephony_server = TelephonyServer(
#     base_url=BASE_URL,  # your ngrok url
#     config_manager=config_manager,
#     inbound_call_configs=[
#         TwilioInboundCallConfig(
#             url="/inbound_call",
#             twilio_config=twilio_config,
#             agent_config=agent_config,
#             synthesizer_config=synthesizer_config,
#             transcriber_config=transcriber_config,  # Use instance
#             twiml_fallback_response='''<?xml version="1.0" encoding="UTF-8"?>
# <Response>
#     <Say>I didn't hear a response. Are you still there? Please say something to continue.</Say>
#     <Pause length="15"/>
#     <Redirect method="POST">/inbound_call</Redirect>
# </Response>'''
#         )
#     ],
#     agent_factory=CustomAgentFactory(),
#     synthesizer_factory=CustomSynthesizerFactory(),
#     events_manager=ChessEventsManager(),
# )


# # Add routes to FastAPI app
# app.include_router(telephony_server.get_router())


# # Outbound call helper
# async def make_outbound_call(to_phone: str):
#     client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#     twilio_base_url = f"https://{BASE_URL}"
#     call = await asyncio.get_event_loop().run_in_executor(
#         None,
#         lambda: client.calls.create(
#             to=to_phone,
#             from_=TWILIO_PHONE_NUMBER,
#             url=f"{twilio_base_url}/inbound_call",
#             status_callback=f"{twilio_base_url}/call_status",
#             status_callback_method="POST",
#             status_callback_event=["initiated", "ringing", "answered", "completed"],
#             record=True,
#             recording_channels="dual",
#         )
#     )
#     logger.info(f"Call initiated: SID={call.sid}")
#     return call.sid


# # Main entrypoint
# if __name__ == "__main__":
#     import uvicorn

#     def run_server():
#         logger.debug("Starting Uvicorn server")
#         uvicorn.run(app, host="0.0.0.0", port=3000)

#     async def start_server_and_call():
#         try:
#             server_thread = threading.Thread(target=run_server, daemon=True)
#             server_thread.start()
#             await asyncio.sleep(2)
#             await make_outbound_call("+917356793165")  # your target phone number
#             await asyncio.Event().wait()
#         except Exception as e:
#             logger.error(f"Error in start_server_and_call: {str(e)}")
#             raise

#     asyncio.run(start_server_and_call())












# import os
# import logging
# import asyncio
# import httpx
# import typing
# import time
# from typing import Optional, Tuple
# from fastapi import FastAPI, Request, Response
# from fastapi.logger import logger as fastapi_logger
# from contextlib import asynccontextmanager
# from dotenv import load_dotenv
# from twilio.rest import Client
# from vocode.streaming.telephony.server.base import TelephonyServer, TwilioInboundCallConfig
# from vocode.streaming.models.telephony import TwilioConfig
# from vocode.streaming.models.agent import LangchainAgentConfig, AgentConfig
# from vocode.streaming.agent.langchain_agent import LangchainAgent
# from vocode.streaming.models.message import BaseMessage
# from vocode.streaming.transcriber.deepgram_transcriber import DeepgramTranscriber
# from vocode.streaming.models.transcriber import DeepgramTranscriberConfig, AudioEncoding, PunctuationEndpointingConfig
# from vocode.streaming.synthesizer.stream_elements_synthesizer import StreamElementsSynthesizer
# from vocode.streaming.models.synthesizer import StreamElementsSynthesizerConfig, SynthesizerConfig
# from vocode.streaming.synthesizer.base_synthesizer import BaseSynthesizer
# from vocode.streaming.telephony.config_manager.in_memory_config_manager import InMemoryConfigManager
# from vocode.streaming.agent.base_agent import BaseAgent
# from vocode.streaming.models.events import Event, EventType
# from vocode.streaming.models.transcript import TranscriptCompleteEvent
# from vocode.streaming.utils import events_manager
# from langchain_groq import ChatGroq
# import threading
# import numpy as np


# # Configure logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# fastapi_logger.setLevel(logging.DEBUG)


# # Ensure ffmpeg is in PATH
# os.environ['PATH'] += os.pathsep + 'C:\\ffmpeg\\bin'


# load_dotenv()


# # Environment variables
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
# TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
# TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
# BASE_URL = os.getenv("BASE_URL")
# DEBUG_AUDIO = os.getenv("DEBUG_AUDIO", "false").lower() == "true"


# # Validate environment variables
# required_vars = [GROQ_API_KEY, DEEPGRAM_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, BASE_URL]
# if not all(required_vars):
#     raise ValueError("Missing required environment variables in .env file. Required: GROQ_API_KEY, DEEPGRAM_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, BASE_URL")


# # Validate Ngrok URL
# if not BASE_URL.endswith((".ngrok-free.app", ".ngrok.io")):
#     logger.warning(f"BASE_URL ({BASE_URL}) does not appear to be a valid Ngrok URL. Ensure it matches the current Ngrok session and is updated in Twilio Console.")


# # Chess coach prompt
# CHESS_COACH_PROMPT_PREAMBLE = """
# # Chess Coaching Sales Representative Prompt

# ## Identity & Purpose
# You are Priya, a virtual sales representative for 4champz, a leading chess coaching service provider based in Bengaluru, India. We specialize in providing qualified chess coaches to schools across Bangalore. 
# Your primary purpose is to qualify leads who have shown interest in chess coaching opportunities, understand their background and experience, and explore potential collaboration as a chess coach for our school programs.

# ## Voice & Persona

# ### Personality
# - Sound professional, warm, and conversational—like a knowledgeable chess enthusiast
# - Project genuine interest in learning about their chess journey
# - Maintain an engaging and respectful demeanor throughout the conversation
# - Show respect for their time while staying focused on understanding their suitability for school coaching
# - Convey enthusiasm about the opportunity to shape young minds through chess

# ### Speech Characteristics
# - Use clear, conversational language with natural flow
# - Keep messages under 150 characters when possible
# - Include probing questions to gather detailed information
# - Show genuine interest in their chess background and achievements
# - Use encouraging language when discussing their experience and qualifications

# ## Conversation Flow

# ### Introduction
# 1. Start with: "Hello {{name}}, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"
# 2. Follow with: "I'm reaching out because you expressed interest in chess coaching. I'd love to learn more about your chess background and explore how we might work together."

# ### Current Involvement Assessment
# - Location confirmation: "First, could you confirm your current location in Bangalore?"
# - Chess involvement: "Tell me about your current chess involvement—are you actively playing or coaching?"
# - Availability overview: "What does your current schedule look like, particularly during afternoon hours?"

# ### Experience and Background Qualification

# #### Chess playing experience:
# - "What's your current chess rating with FIDE or All India Chess Federation?"
# - "What's your highest tournament achievement?"
# - "How long have you been playing chess competitively?"

# #### Tournament participation:
# - "Tell me about your recent tournament participation and notable results"
# - "Have you participated in any state or national level competitions?"

# #### Coaching and teaching experience:
# - "Have you worked with school children before, either in chess or other subjects?"
# - "Do you have any coaching or teaching experience, especially with children?"
# - "Are you comfortable teaching chess in both English and Kannada/Hindi?"

# #### Educational qualifications:
# - "What are your educational qualifications?"
# - "Do you have any chess certifications or coaching credentials?"

# ### School Coaching Interest Exploration
# - Explain the opportunity: "Let me tell you about our model—we provide qualified chess coaches to reputed schools across Bangalore. Our coaches work directly with students during school hours."

# #### Availability assessment:
# - "Are you available for school hours, typically between 3-6 PM?"
# - "How many days per week would you be interested in coaching?"
# - "Which areas of Bangalore can you travel to for coaching assignments?"

# #### Age group comfort:
# - "Are you comfortable teaching different age groups, from Classes 1 through 12?"
# - "Do you have any preference for specific age groups?"

# #### Support and training:
# - "We provide comprehensive training and curriculum support to all our coaches. How do you feel about following a structured curriculum?"
# - "Are you interested in ongoing professional development in chess coaching?"

# ### Schedule and Close
# If they seem suitable and interested:
# - "Based on our conversation, I think there could be a great fit here. I'd like to schedule a detailed discussion and assessment with you."
# - Use check_calendar_availability for follow-up meetings
# - If proceeding: Call book_appointment
# - "Could you confirm your full name, email address, and preferred meeting time?"
# - Positive close: "Thank you for your time, {{name}}. We'll send you more details about our school programs and compensation structure. I'm looking forward to speaking with you soon about this exciting opportunity!"
# - Always end with end_call unless transferred

# ## Response Guidelines
# - Keep responses focused on qualifying their suitability for school coaching
# - Ask location-specific questions about Bangalore areas they can cover
# - Show genuine enthusiasm for their chess achievements and experience
# - Be respectful of their current commitments and time constraints
# - Use IST timing when scheduling appointments
# - Emphasize the opportunity to impact young minds through chess education
# - Ask only one detailed question at a time to avoid overwhelming them

# ## Scenario Handling

# ### For Highly Qualified Candidates
# - Express enthusiasm: "Your tournament experience and rating are impressive! Our partner schools would definitely value someone with your background."
# - Fast-track process: "Given your qualifications, I'd love to expedite our discussion. When would be the best time for a detailed conversation this week?"
# - Highlight premium opportunities: "With your experience, you'd be perfect for our advanced chess program placements at premium schools."

# ### For Candidates with Limited Formal Experience
# - Explore potential: "While formal ratings are helpful, we also value passion and teaching ability. Tell me about your experience working with children or young people."
# - Training emphasis: "We provide comprehensive training to help coaches develop their skills. Are you excited about growing your coaching abilities with our support?"
# - Alternative qualifications: "Have you been involved in chess clubs, online coaching, or informal teaching that might not show up in formal ratings?"

# ### For Candidates Requesting Human Assistance
# - If they want to speak with a human or need more details about compensation/partnerships:
#   - Use transfer_call
#   - Say: "Of course! Let me connect you with our placement manager who can give you detailed information about our school partnerships, compensation structure, and specific placement opportunities."

# ### For Availability Concerns
# - Flexible scheduling: "We work with various schools, so we can often accommodate different availability preferences. What times work best for you?"
# - Part-time opportunities: "Many of our coaches start part-time and gradually increase their involvement. Would that approach interest you?"
# - Location matching: "We'll match you with schools in areas convenient for you. Which parts of Bangalore are most accessible?"

# ## Knowledge Base

# ### Caller Information Variables
# - name: {{name}}
# - email: {{email}}
# - phone_number: {{phone_number}}
# - role: {{role}}

# ### 4champz Service Model
# - Leading chess coaching service provider in Bengaluru
# - Specializes in providing qualified coaches to schools across Bangalore
# - Partners with reputed schools throughout the city
# - Provides comprehensive training and curriculum support
# - Offers both part-time and full-time coaching opportunities
# - Focuses on developing young chess talent in school settings

# ### Coaching Requirements
# - School hours availability (typically 3-6 PM)
# - Ability to teach students from Classes 1-12
# - Comfort with English and preferably Kannada/Hindi
# - Transportation capability across Bangalore areas
# - Professional attitude and teaching aptitude
# - Chess knowledge appropriate for school-level instruction

# ### Assessment Criteria
# - Chess playing experience and rating (FIDE/All India Chess Federation)
# - Tournament participation and achievements
# - Prior coaching or teaching experience, especially with children
# - Educational qualifications and chess certifications
# - Language capabilities and communication skills
# - Geographic availability across Bangalore
# - Flexibility with scheduling and age groups

# ## Response Refinement
# - When discussing their chess background: "Your chess journey sounds fascinating. Could you tell more about [specific aspect they mentioned]?"
# - When explaining opportunities: "Let me paint a picture of what coaching with our partner schools looks like..."
# - When confirming details: "Just to make sure I have everything right—you're available [summarize their availability] and comfortable teaching [summarize their preferences]. Is that accurate?"

# ## Call Management

# ### Available Functions
# - check_calendar_availability: Use when scheduling follow-up meetings
# - book_appointment: Use when confirming scheduled appointments
# - transfer_call: Use when candidate requests human assistance
# - end_call: Use to properly conclude every conversation

# ## Technical Considerations
# - If experiencing delays accessing calendar: "I'm just checking our available appointment slots. This will take just a moment."
# - If multiple scheduling needs arise: "Let me handle your appointment booking first, and then we can discuss any additional questions."
# - Always confirm appointment details before ending: "To confirm, we're scheduled for [day], [date] at [time]. You'll receive an email confirmation shortly."

# ---
# Remember that your ultimate goal is to identify qualified chess coaches who can positively impact students in Bangalore schools while ensuring they understand the opportunity and feel excited about the partnership. Accuracy in qualifying candidates and scheduling follow-ups is your top priority, followed by creating enthusiasm for the teaching opportunity and maintaining 4champz's professional reputation.
# """


# # Groq LLM setup
# llm = ChatGroq(model_name="llama-3.1-8b-instant")


# # Config Manager
# config_manager = InMemoryConfigManager()


# # Events Manager to log transcripts
# class ChessEventsManager(events_manager.EventsManager):
#     def __init__(self):
#         super().__init__(subscriptions=[EventType.TRANSCRIPT_COMPLETE])

#     async def handle_event(self, event: Event):
#         if event.type == EventType.TRANSCRIPT_COMPLETE:
#             transcript_complete_event = typing.cast(TranscriptCompleteEvent, event)
#             logger.debug(f"Transcript for conversation {transcript_complete_event.conversation_id}: {transcript_complete_event.transcript.to_string()}")
#             webhook_url = os.getenv("TRANSCRIPT_CALLBACK_URL")
#             if webhook_url:
#                 data = {"conversation_id": transcript_complete_event.conversation_id, "user_id": 1, "transcript": transcript_complete_event.transcript.to_string()}
#                 async with httpx.AsyncClient() as client:
#                     response = await client.post(webhook_url, json=data)
#                     if response.status_code == 200:
#                         logger.info("Transcript sent successfully to webhook")
#                     else:
#                         logger.error(f"Failed to send transcript to webhook: {response.status_code}")


# # Custom Agent Config
# class CustomLangchainAgentConfig(LangchainAgentConfig, type="agent_langchain"):
#     initial_message: BaseMessage = BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?")
#     prompt_preamble: str = CHESS_COACH_PROMPT_PREAMBLE
#     model_name: str = "llama-3.1-8b-instant"
#     api_key: str = GROQ_API_KEY
#     provider: str = "groq"


# # Custom Langchain Agent
# class CustomLangchainAgent(LangchainAgent):
#     def __init__(self, agent_config: CustomLangchainAgentConfig):
#         logger.debug(f"Initializing CustomLangchainAgent with config: {agent_config}")
#         super().__init__(agent_config=agent_config)
#         self.last_response_time = time.time()
#         self.conversation_state = "initial"
#         self.no_input_count = 0
#         self.user_name = None  # store extracted/confirmed name
#         self.asked_for_name = False  # track if name is requested
#         logger.debug("Initialized CustomLangchainAgent with Groq LLM (llama-3.1-8b-instant)")

#     async def respond(self, human_input: str, conversation_id: str, is_interrupt: bool = False) -> Tuple[Optional[str], bool]:
#         try:
#             start_time = time.time()

#             # Helper function to sanitize / replace {name} placeholder in bot replies
#             def personalize_response(text: str) -> str:
#                 if self.user_name:
#                     return text.replace("{name}", self.user_name)
#                 else:
#                     # Replace with external fetch if implemented
#                     external_name = "there"
#                     return text.replace("{name}", external_name)

#             # Timeout: fallback if no transcription for 15s
#             if time.time() - self.last_response_time > 15:
#                 self.no_input_count += 1
#                 logger.warning(f"No transcription for 15 seconds (attempt {self.no_input_count}), sending fallback")
#                 if self.no_input_count >= 3:
#                     logger.info("No valid input after 3 fallback attempts, ending call")
#                     return personalize_response("It seems we’re having trouble connecting. I’ll follow up later. Thank you!"), True
#                 return personalize_response("I didn't catch that clearly. Could you confirm if you're available to discuss chess coaching opportunities?"), False

#             # Normalize input for checks
#             normalized = (human_input or "").strip().lower()

#             # Basic heuristic: ignore very short or common filler responses
#             filler_phrases = {"", "mhmm", "okay", "what", "yes", "no", "a-", "four", "hello", "hi"}
#             if normalized in filler_phrases:
#                 self.no_input_count += 1
#                 logger.debug(f"Detected filler/no meaningful input (count {self.no_input_count}): '{human_input}'")
#                 if self.no_input_count >= 3:
#                     logger.info("No valid input after 3 attempts, ending call")
#                     return personalize_response("It seems we’re having trouble connecting. I’ll follow up later. Thank you!"), True
#                 self.last_response_time = start_time
#                 # Different prompt depending on conversation state
#                 if self.conversation_state == "initial":
#                     return personalize_response("I didn't catch that clearly. Could you confirm if you're available to discuss chess coaching opportunities?"), False
#                 else:
#                     return personalize_response("Sorry, I didn't understand. Could you tell me about your current chess involvement?"), False

#             # If input looks like gibberish or incomplete question (simple heuristic)
#             gibberish_indicators = ["what is the first time", "first time", "please repeat", "say again"]
#             if any(phrase in normalized for phrase in gibberish_indicators):
#                 logger.debug(f"Input looks like unclear/gibberish: '{human_input}', prompting clarification")
#                 self.no_input_count += 1
#                 if self.no_input_count >= 3:
#                     logger.info("No valid input after 3 unclear attempts, ending call")
#                     return personalize_response("It seems we’re having trouble connecting. I’ll follow up later. Thank you!"), True
#                 self.last_response_time = start_time
#                 return personalize_response("Sorry, I didn't catch that. Could you please repeat or say yes/no if you're available?"), False

#             # Reset no input count on valid input
#             self.no_input_count = 0

#             # Try extract user name from input if mentioned (very basic detection)
#             # e.g. "My name is Priya"
#             if self.asked_for_name and "name is" in normalized:
#                 try:
#                     name_part = human_input.lower().split("name is", 1)[1].strip().split()[0]
#                     self.user_name = name_part.capitalize()
#                     logger.debug(f"Extracted user name: {self.user_name}")
#                 except Exception:
#                     self.user_name = None

#             # Conversation state machine
#             if self.conversation_state == "initial":
#                 # Expect positive confirmation to move forward
#                 if any(word in normalized for word in ["yes", "sure", "okay", "available"]):
#                     self.conversation_state = "background"
#                     response = "Great! I'm reaching out because you expressed interest in chess coaching. First, could you confirm your current location in Bangalore?"
#                     self.last_response_time = start_time
#                     logger.debug(f"Agent response: {response}")
#                     return response, False
#                 else:
#                     response = personalize_response("Sorry, I might have misheard you. Could you confirm if you're available to discuss chess coaching opportunities?")
#                     self.last_response_time = start_time
#                     logger.debug(f"Agent response: {response}")
#                     return response, False

#             # After initial state, forward input to langchain super() for processing
#             else:
#                 # Forward input to langchain super with timeout to reduce delay
#                 try:
#                     response, should_end = await asyncio.wait_for(
#                         super().respond(human_input, conversation_id, is_interrupt), timeout=5.0
#                     )
#                 except asyncio.TimeoutError:
#                     logger.warning("LLM response timed out")
#                     fallback_msg = personalize_response("Sorry, I'm having trouble responding quickly. Let's try again shortly.")
#                     return fallback_msg, False

#                 if response:
#                     response_text = personalize_response(response)
#                     if "location" in response_text.lower():
#                         self.conversation_state = "background"
#                     # Detect if AI asks for name and set flag
#                     if any(phrase in response_text.lower() for phrase in ["confirm your full name", "may I have your name"]):
#                         self.asked_for_name = True
#                     self.last_response_time = start_time
#                     logger.debug(f"Agent super responded: {response_text}, should_end={should_end}")
#                     return response_text, should_end

#                 # Fallback generic message if super returns nothing
#                 fallback_msg = personalize_response("Sorry, I didn't quite get that. Could you please tell me more?")
#                 self.last_response_time = start_time
#                 return fallback_msg, False

#         except Exception as e:
#             logger.error(f"Error generating response: {str(e)}")
#             fallback_error_msg = personalize_response("Sorry, I encountered an error. Please try again.")
#             return fallback_error_msg, False


# # Custom Deepgram Transcriber with keepalive and chunk logging
# class CustomDeepgramTranscriber(DeepgramTranscriber):
#     def __init__(self, transcriber_config: DeepgramTranscriberConfig):
#         super().__init__(transcriber_config)
#     async def process(self, audio_chunk: bytes):
#         logger.debug(f"Processing audio chunk size: {len(audio_chunk)} bytes")  # Added
#         if not audio_chunk or len(audio_chunk) == 0:
#             logger.warning("Empty audio chunk - skipping")
#             return None
#         try:
#             return await super().process(audio_chunk)
#         except Exception as e:
#             logger.error(f"Deepgram process error: {e}")
#             raise
#     async def keepalive(self):
#         while True:
#             await asyncio.sleep(10)
#             try:
#                 await super().process(b"\x00" * 160)
#                 logger.debug("Deepgram keepalive sent")
#             except Exception as e:
#                 logger.error(f"Keepalive failed: {e}")
#                 break

# # Custom Agent Factory
# class CustomAgentFactory:
#     def create_agent(self, agent_config: AgentConfig, logger: Optional[logging.Logger] = None) -> BaseAgent:
#         log = logger or globals().get('logger', logging.getLogger(__name__))
#         log.debug(f"Creating agent with config type: {agent_config.type}")
#         if agent_config.type == "agent_langchain":
#             log.debug("Creating CustomLangchainAgent")
#             return CustomLangchainAgent(agent_config=typing.cast(CustomLangchainAgentConfig, agent_config))
#         log.error(f"Invalid agent config type: {agent_config.type}")
#         raise Exception(f"Invalid agent config: {agent_config.type}")


# # Custom Synthesizer Factory
# class CustomSynthesizerFactory:
#     def create_synthesizer(self, synthesizer_config: SynthesizerConfig) -> BaseSynthesizer:
#         logger.debug(f"Creating synthesizer with config: {synthesizer_config}")
#         if isinstance(synthesizer_config, StreamElementsSynthesizerConfig):
#             logger.debug("Creating StreamElementsSynthesizer")
#             return StreamElementsSynthesizer(synthesizer_config)
#         logger.error(f"Invalid synthesizer config type: {synthesizer_config.type}")
#         raise Exception(f"Invalid synthesizer config: {synthesizer_config.type}")


# # FastAPI App
# app = FastAPI()


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     logger.debug("Starting up FastAPI application")
#     logger.debug("Registered routes:")
#     for route in app.routes:
#         methods = getattr(route, "methods", ["WebSocket"])
#         logger.debug(f" - {route.path} ({methods})")
#     yield
#     logger.debug("Shutting down FastAPI application")


# app.router.lifespan_context = lifespan


# # Twilio config
# twilio_config = TwilioConfig(
#     account_sid=TWILIO_ACCOUNT_SID,
#     auth_token=TWILIO_AUTH_TOKEN
# )


# # Synthesizer config (telephone voice output)
# synthesizer_config = StreamElementsSynthesizerConfig.from_telephone_output_device(
#     voice="Brian"
# )


# transcriber_config = DeepgramTranscriberConfig(
#     api_key=DEEPGRAM_API_KEY,
#     model="nova-2-phonecall",
#     language="en",
#     sampling_rate=8000,  # int primitive, not enum
#     audio_encoding="mulaw",  # lowercase string, not enum
#     chunk_size=320,
#     endpointing_config=PunctuationEndpointingConfig(),
#     downsampling=1,
# )



# agent_config = LangchainAgentConfig(
#     initial_message=BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"),
#     prompt_preamble=CHESS_COACH_PROMPT_PREAMBLE,
#     model_name="llama-3.1-8b-instant",
#     api_key=GROQ_API_KEY,
#     provider="groq",
# )


# # Create CustomDeepgramTranscriber instance with config
# # custom_deepgram_transcriber = CustomDeepgramTranscriber(transcriber_config)


# # Telephony Server setup
# telephony_server = TelephonyServer(
#     base_url=BASE_URL,  # your ngrok url
#     config_manager=config_manager,
#     inbound_call_configs=[
#         TwilioInboundCallConfig(
#             url="/inbound_call",
#             twilio_config=twilio_config,
#             agent_config=agent_config,
#             synthesizer_config=synthesizer_config,
#             transcriber_config=transcriber_config,  # Use instance
#             twiml_fallback_response='''<?xml version="1.0" encoding="UTF-8"?>
# <Response>
#     <Say>I didn't hear a response. Are you still there? Please say something to continue.</Say>
#     <Pause length="15"/>
#     <Redirect method="POST">/inbound_call</Redirect>
# </Response>'''
#         )
#     ],
#     agent_factory=CustomAgentFactory(),
#     synthesizer_factory=CustomSynthesizerFactory(),
#     events_manager=ChessEventsManager(),
# )


# # Add routes to FastAPI app
# app.include_router(telephony_server.get_router())


# # Outbound call helper
# async def make_outbound_call(to_phone: str):
#     client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#     twilio_base_url = f"https://{BASE_URL}"
#     call = await asyncio.get_event_loop().run_in_executor(
#         None,
#         lambda: client.calls.create(
#             to=to_phone,
#             from_=TWILIO_PHONE_NUMBER,
#             url=f"{twilio_base_url}/inbound_call",
#             status_callback=f"{twilio_base_url}/call_status",
#             status_callback_method="POST",
#             status_callback_event=["initiated", "ringing", "answered", "completed"],
#             record=True,
#             recording_channels="dual",
#         )
#     )
#     logger.info(f"Call initiated: SID={call.sid}")
#     return call.sid


# # Main entrypoint
# if __name__ == "__main__":
#     import uvicorn

#     def run_server():
#         logger.debug("Starting Uvicorn server")
#         uvicorn.run(app, host="0.0.0.0", port=3000)

#     async def start_server_and_call():
#         try:
#             server_thread = threading.Thread(target=run_server, daemon=True)
#             server_thread.start()
#             await asyncio.sleep(2)
#             await make_outbound_call("+917356793165")  # your target phone number
#             await asyncio.Event().wait()
#         except Exception as e:
#             logger.error(f"Error in start_server_and_call: {str(e)}")
#             raise

#     asyncio.run(start_server_and_call())










# import os
# import logging
# import asyncio
# import httpx
# import typing
# import time
# from typing import Optional, Tuple
# from fastapi import FastAPI, Request, Response
# from fastapi.logger import logger as fastapi_logger
# from contextlib import asynccontextmanager
# from dotenv import load_dotenv
# from twilio.rest import Client
# from vocode.streaming.telephony.server.base import TelephonyServer, TwilioInboundCallConfig
# from vocode.streaming.models.telephony import TwilioConfig
# from vocode.streaming.models.agent import LangchainAgentConfig, AgentConfig
# from vocode.streaming.agent.langchain_agent import LangchainAgent
# from vocode.streaming.models.message import BaseMessage
# from vocode.streaming.transcriber.deepgram_transcriber import DeepgramTranscriber
# from vocode.streaming.models.transcriber import DeepgramTranscriberConfig, AudioEncoding, PunctuationEndpointingConfig
# from vocode.streaming.synthesizer.stream_elements_synthesizer import StreamElementsSynthesizer
# from vocode.streaming.models.synthesizer import StreamElementsSynthesizerConfig, SynthesizerConfig
# from vocode.streaming.synthesizer.base_synthesizer import BaseSynthesizer
# from vocode.streaming.telephony.config_manager.in_memory_config_manager import InMemoryConfigManager
# from vocode.streaming.agent.base_agent import BaseAgent
# from vocode.streaming.models.events import Event, EventType
# from vocode.streaming.models.transcript import TranscriptCompleteEvent
# from vocode.streaming.utils import events_manager
# from langchain_groq import ChatGroq
# import threading
# import numpy as np

# # ADDED for JSON capture with LLM extraction
# import json  # ADDED for JSON capture with LLM extraction
# import re    # ADDED: general regex utilities
# from pathlib import Path  # ADDED: filesystem-safe paths

# # Configure logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# fastapi_logger.setLevel(logging.DEBUG)

# # Ensure ffmpeg is in PATH
# os.environ['PATH'] += os.pathsep + 'C:\\ffmpeg\\bin'

# load_dotenv()

# # Environment variables
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
# TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
# TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
# BASE_URL = os.getenv("BASE_URL")
# DEBUG_AUDIO = os.getenv("DEBUG_AUDIO", "false").lower() == "true"

# # Validate environment variables
# required_vars = [GROQ_API_KEY, DEEPGRAM_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, BASE_URL]
# if not all(required_vars):
#     raise ValueError("Missing required environment variables in .env file. Required: GROQ_API_KEY, DEEPGRAM_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, BASE_URL")

# # Validate Ngrok URL
# if not BASE_URL.endswith((".ngrok-free.app", ".ngrok.io")):
#     logger.warning(f"BASE_URL ({BASE_URL}) does not appear to be a valid Ngrok URL. Ensure it matches the current Ngrok session and is updated in Twilio Console.")

# # Chess coach prompt
# CHESS_COACH_PROMPT_PREAMBLE = """
# # Chess Coaching Sales Representative Prompt
# ## Identity & Purpose
# You are Priya, a virtual sales representative for 4champz, a leading chess coaching service provider based in Bengaluru, India. We specialize in providing qualified chess coaches to schools across Bangalore. 
# Your primary purpose is to qualify leads who have shown interest in chess coaching opportunities, understand their background and experience, and explore potential collaboration as a chess coach for our school programs.
# ## Voice & Persona
# ### Personality
# - Sound professional, warm, and conversational—like a knowledgeable chess enthusiast
# - Project genuine interest in learning about their chess journey
# - Maintain an engaging and respectful demeanor throughout the conversation
# - Show respect for their time while staying focused on understanding their suitability for school coaching
# - Convey enthusiasm about the opportunity to shape young minds through chess
# ### Speech Characteristics
# - Use clear, conversational language with natural flow
# - Keep messages under 150 characters when possible
# - Include probing questions to gather detailed information
# - Show genuine interest in their chess background and achievements
# - Use encouraging language when discussing their experience and qualifications
# ## Conversation Flow
# ### Introduction
# 1. Start with: "Hello {{name}}, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"
# 2. Follow with: "I'm reaching out because you expressed interest in chess coaching. I'd love to learn more about your chess background and explore how we might work together."
# ### Current Involvement Assessment
# - Location confirmation: "First, could you confirm your current location in Bangalore?"
# - Chess involvement: "Tell me about your current chess involvement—are you actively playing or coaching?"
# - Availability overview: "What does your current schedule look like, particularly during afternoon hours?"
# ### Experience and Background Qualification
# #### Chess playing experience:
# - "What's your current chess rating with FIDE or All India Chess Federation?"
# - "What's your highest tournament achievement?"
# - "How long have you been playing chess competitively?"
# #### Tournament participation:
# - "Tell me about your recent tournament participation and notable results"
# - "Have you participated in any state or national level competitions?"
# #### Coaching and teaching experience:
# - "Have you worked with school children before, either in chess or other subjects?"
# - "Do you have any coaching or teaching experience, especially with children?"
# - "Are you comfortable teaching chess in both English and Kannada/Hindi?"
# #### Educational qualifications:
# - "What are your educational qualifications?"
# - "Do you have any chess certifications or coaching credentials?"
# ### School Coaching Interest Exploration
# - Explain the opportunity: "Let me tell you about our model—we provide qualified chess coaches to reputed schools across Bangalore. Our coaches work directly with students during school hours."
# #### Availability assessment:
# - "Are you available for school hours, typically between 3-6 PM?"
# - "How many days per week would you be interested in coaching?"
# - "Which areas of Bangalore can you travel to for coaching assignments?"
# #### Age group comfort:
# - "Are you comfortable teaching different age groups, from Classes 1 through 12?"
# - "Do you have any preference for specific age groups?"
# #### Support and training:
# - "We provide comprehensive training and curriculum support to all our coaches. How do you feel about following a structured curriculum?"
# - "Are you interested in ongoing professional development in chess coaching?"
# ### Schedule and Close
# If they seem suitable and interested:
# - "Based on our conversation, I think there could be a great fit here. I'd like to schedule a detailed discussion and assessment with you."
# - Use check_calendar_availability for follow-up meetings
# - If proceeding: Call book_appointment
# - "Could you confirm your full name, email address, and preferred meeting time?"
# - Positive close: "Thank you for your time, {{name}}. We'll send you more details about our school programs and compensation structure. I'm looking forward to speaking with you soon about this exciting opportunity!"
# - Always end with end_call unless transferred
# ## Response Guidelines
# - Keep responses focused on qualifying their suitability for school coaching
# - Ask location-specific questions about Bangalore areas they can cover
# - Show genuine enthusiasm for their chess achievements and experience
# - Be respectful of their current commitments and time constraints
# - Use IST timing when scheduling appointments
# - Emphasize the opportunity to impact young minds through chess education
# - Ask only one detailed question at a time to avoid overwhelming them
# ## Scenario Handling
# ### For Highly Qualified Candidates
# - Express enthusiasm: "Your tournament experience and rating are impressive! Our partner schools would definitely value someone with your background."
# - Fast-track process: "Given your qualifications, I'd love to expedite our discussion. When would be the best time for a detailed conversation this week?"
# - Highlight premium opportunities: "With your experience, you'd be perfect for our advanced chess program placements at premium schools."
# ### For Candidates with Limited Formal Experience
# - Explore potential: "While formal ratings are helpful, we also value passion and teaching ability. Tell me about your experience working with children or young people."
# - Training emphasis: "We provide comprehensive training to help coaches develop their skills. Are you excited about growing your coaching abilities with our support?"
# - Alternative qualifications: "Have you been involved in chess clubs, online coaching, or informal teaching that might not show up in formal ratings?"
# ### For Candidates Requesting Human Assistance
# - If they want to speak with a human or need more details about compensation/partnerships:
#   - Use transfer_call
#   - Say: "Of course! Let me connect you with our placement manager who can give you detailed information about our school partnerships, compensation structure, and specific placement opportunities."
# ### For Availability Concerns
# - Flexible scheduling: "We work with various schools, so we can often accommodate different availability preferences. What times work best for you?"
# - Part-time opportunities: "Many of our coaches start part-time and gradually increase their involvement. Would that approach interest you?"
# - Location matching: "We'll match you with schools in areas convenient for you. Which parts of Bangalore are most accessible?"
# ## Knowledge Base
# ### Caller Information Variables
# - name: {{name}}
# - email: {{email}}
# - phone_number: {{phone_number}}
# - role: {{role}}
# ### 4champz Service Model
# - Leading chess coaching service provider in Bengaluru
# - Specializes in providing qualified coaches to schools across Bangalore
# - Partners with reputed schools throughout the city
# - Provides comprehensive training and curriculum support
# - Offers both part-time and full-time coaching opportunities
# - Focuses on developing young chess talent in school settings
# ### Coaching Requirements
# - School hours availability (typically 3-6 PM)
# - Ability to teach students from Classes 1-12
# - Comfort with English and preferably Kannada/Hindi
# - Transportation capability across Bangalore areas
# - Professional attitude and teaching aptitude
# - Chess knowledge appropriate for school-level instruction
# ### Assessment Criteria
# - Chess playing experience and rating (FIDE/All India Chess Federation)
# - Tournament participation and achievements
# - Prior coaching or teaching experience, especially with children
# - Educational qualifications and chess certifications
# - Language capabilities and communication skills
# - Geographic availability across Bangalore
# - Flexibility with scheduling and age groups
# ## Response Refinement
# - When discussing their chess background: "Your chess journey sounds fascinating. Could you tell more about [specific aspect they mentioned]?"
# - When explaining opportunities: "Let me paint a picture of what coaching with our partner schools looks like..."
# - When confirming details: "Just to make sure I have everything right—you're available [summarize their availability] and comfortable teaching [summarize their preferences]. Is that accurate?"
# ## Call Management
# ### Available Functions
# - check_calendar_availability: Use when scheduling follow-up meetings
# - book_appointment: Use when confirming scheduled appointments
# - transfer_call: Use when candidate requests human assistance
# - end_call: Use to properly conclude every conversation
# ## Technical Considerations
# - If experiencing delays accessing calendar: "I'm just checking our available appointment slots. This will take just a moment."
# - If multiple scheduling needs arise: "Let me handle your appointment booking first, and then we can discuss any additional questions."
# - Always confirm appointment details before ending: "To confirm, we're scheduled for [day], [date] at [time]. You'll receive an email confirmation shortly."
# ---
# Remember that your ultimate goal is to identify qualified chess coaches who can positively impact students in Bangalore schools while ensuring they understand the opportunity and feel excited about the partnership. Accuracy in qualifying candidates and scheduling follow-ups is your top priority, followed by creating enthusiasm for the teaching opportunity and maintaining 4champz's professional reputation.
# """

# # Groq LLM setup
# llm = ChatGroq(model_name="llama-3.1-8b-instant")
# # llm = ChatGroq(model_name="groq/compound-mini")

# # Config Manager
# config_manager = InMemoryConfigManager()

# # ADDED for JSON capture with LLM extraction: global in-memory store
# CONVERSATION_STORE: dict = {}  # ADDED for JSON LLM extraction

# # ADDED for JSON capture with LLM extraction: directory for local persistence
# CONVERSATIONS_DIR = Path("conversations")  # ADDED
# CONVERSATIONS_DIR.mkdir(exist_ok=True, parents=True)  # ADDED

# # Events Manager to log transcripts
# class ChessEventsManager(events_manager.EventsManager):
#     def __init__(self):
#         super().__init__(subscriptions=[EventType.TRANSCRIPT_COMPLETE])

#     async def handle_event(self, event: Event):
#         if event.type == EventType.TRANSCRIPT_COMPLETE:
#             transcript_complete_event = typing.cast(TranscriptCompleteEvent, event)
#             logger.debug(f"Transcript for conversation {transcript_complete_event.conversation_id}: {transcript_complete_event.transcript.to_string()}")
#             webhook_url = os.getenv("TRANSCRIPT_CALLBACK_URL")
#             if webhook_url:
#                 data = {"conversation_id": transcript_complete_event.conversation_id, "user_id": 1, "transcript": transcript_complete_event.transcript.to_string()}
#                 async with httpx.AsyncClient() as client:
#                     response = await client.post(webhook_url, json=data)
#                     if response.status_code == 200:
#                         logger.info("Transcript sent successfully to webhook")
#                     else:
#                         logger.error(f"Failed to send transcript to webhook: {response.status_code}")
#             # ADDED for JSON capture with LLM extraction: write store JSON to disk
#             try:
#                 convo = CONVERSATION_STORE.get(transcript_complete_event.conversation_id)
#                 if convo:
#                     out_path = CONVERSATIONS_DIR / f"{transcript_complete_event.conversation_id}.json"
#                     with open(out_path, "w", encoding="utf-8") as f:
#                         json.dump(convo, f, ensure_ascii=False, indent=2)
#                     logger.info(f"Wrote JSON summary to {out_path}")
#             except Exception as e:
#                 logger.error(f"Failed to write JSON summary: {e}")

# # Custom Agent Config
# class CustomLangchainAgentConfig(LangchainAgentConfig, type="agent_langchain"):
#     initial_message: BaseMessage = BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?")
#     prompt_preamble: str = CHESS_COACH_PROMPT_PREAMBLE
#     model_name: str = "llama-3.1-8b-instant"
#     # model_name: str = "groq/compound-mini"
#     api_key: str = GROQ_API_KEY
#     provider: str = "groq"

# # Custom Langchain Agent
# class CustomLangchainAgent(LangchainAgent):
#     def __init__(self, agent_config: CustomLangchainAgentConfig):
#         logger.debug(f"Initializing CustomLangchainAgent with config: {agent_config}")
#         super().__init__(agent_config=agent_config)
#         self.last_response_time = time.time()
#         self.conversation_state = "initial"
#         self.no_input_count = 0
#         self.user_name = None  # store extracted/confirmed name
#         self.asked_for_name = False  # track if name is requested
#         logger.debug("Initialized CustomLangchainAgent with Groq LLM (llama-3.1-8b-instant)")
#         # ADDED for JSON capture with LLM extraction
#         self.turns = []  # [{"speaker":"user"/"bot","text":..., "ts": epoch_ms}]
#         self.conversation_id_cache = None  # to index the global store
#         self.extracted_slots = {}  # LLM-extracted structured data

#     # ADDED for JSON capture with LLM extraction
#     def _flush_to_disk(self, conversation_id: str):
#         """Write the current conversation JSON to disk immediately."""
#         try:
#             payload = CONVERSATION_STORE.get(conversation_id)
#             if not payload:
#                 return
#             out_path = CONVERSATIONS_DIR / f"{conversation_id}.json"
#             with open(out_path, "w", encoding="utf-8") as f:
#                 json.dump(payload, f, ensure_ascii=False, indent=2)
#             logger.debug(f"Flushed conversation {conversation_id} to {out_path}")
#         except Exception as e:
#             logger.error(f"Flush to disk failed for {conversation_id}: {e}")

#     # ADDED for JSON capture with LLM extraction
#     def _persist_state(self, conversation_id: str):
#         now_ms = int(time.time() * 1000)
#         payload = {
#             "conversation_id": conversation_id,
#             "updated_at": now_ms,
#             "slots": self.extracted_slots,  # slots are LLM-extracted
#             "turns": self.turns
#         }
#         CONVERSATION_STORE[conversation_id] = payload
#         self._flush_to_disk(conversation_id)  # ADDED: always flush on persist

#     # ADDED for JSON capture with LLM extraction
#     def _strip_code_fences(self, s: str) -> str:
#         t = (s or "").strip()
#         if t.startswith("```"):
#             end = t.rfind("```")
#             if end > 0:
#                 inner = t[3:end].strip()
#                 if inner.lower().startswith("json"):
#                     inner = inner[4:].strip()
#                 return inner
#         return t

#     # ADDED for JSON capture with LLM extraction
#     async def _extract_slots_with_llm(self, conversation_id: str):
#         """
#         Call Groq LLM to extract structured fields from the current turns.
#         This minimizes if/else and uses the prompt-defined fields.
#         """
#         try:
#             # Build a compact transcript string (keep it bounded)
#             convo_lines = []
#             for t in self.turns[-30:]:
#                 role = "User" if t["speaker"] == "user" else "Agent"
#                 text_line = re.sub(r'\s+', ' ', t['text']).strip()
#                 convo_lines.append(f"{role}: {text_line}")
#             convo_text = "\n".join(convo_lines)

#             # Instruction for JSON-only schema
#             schema_instruction = (
#                 "Return ONLY a JSON object with these keys:\n"
#                 "{\n"
#                 '  "location": string|null,\n'
#                 '  "involvement": "playing"|"coaching"|null,\n'
#                 '  "availability": string|null,\n'
#                 '  "age_range": string|null,\n'
#                 '  "languages": string[]|null,\n'
#                 '  "rating": string|null,\n'
#                 '  "tournaments": string|null,\n'
#                 '  "certifications": string|null,\n'
#                 '  "questions": string[]|null\n'
#                 "}\n"
#                 "Infer conservatively. Use null if not explicitly known. Do not add extra keys or text."
#             )

#             prompt = f"{schema_instruction}\n\nConversation:\n{convo_text}\n\nJSON:"

#             extractor = ChatGroq(model_name="llama-3.1-8b-instant")
#             resp = await extractor.ainvoke([
#                 {"role": "system", "content": "You extract structured information from conversations."},
#                 {"role": "user", "content": prompt}
#             ])

#             # Normalize content
#             content = None
#             if hasattr(resp, "content"):
#                 content = resp.content
#             elif hasattr(resp, "generations"):
#                 try:
#                     content = resp.generations.text
#                 except Exception:
#                     content = str(resp)
#             else:
#                 content = str(resp)

#             parsed = None
#             try:
#                 c = self._strip_code_fences(content)
#                 parsed = json.loads(c)
#             except Exception:
#                 logger.warning("Primary JSON parse failed; attempting to locate JSON object")
#                 first = content.find("{")
#                 last = content.rfind("}")
#                 if first != -1 and last != -1 and last > first:
#                     snippet = content[first:last+1]
#                     try:
#                         parsed = json.loads(snippet)
#                     except Exception:
#                         parsed = None

#             if isinstance(parsed, dict):
#                 # normalize keys
#                 for k in ["location","involvement","availability","age_range","languages","rating","tournaments","certifications","questions"]:
#                     if k not in parsed:
#                         parsed[k] = None
#                 # Ensure types
#                 if parsed.get("languages") is not None and not isinstance(parsed["languages"], list):
#                     parsed["languages"] = [str(parsed["languages"])]
#                 if parsed.get("questions") is not None and not isinstance(parsed["questions"], list):
#                     parsed["questions"] = [str(parsed["questions"])]

#                 self.extracted_slots = parsed
#                 self._persist_state(conversation_id)
#             else:
#                 logger.warning("LLM extraction did not return a dict; keeping previous slots.")

#         except Exception as e:
#             logger.error(f"Slot extraction failed: {e}")

#     async def respond(self, human_input: str, conversation_id: str, is_interrupt: bool = False) -> Tuple[Optional[str], bool]:
#         try:
#             start_time = time.time()

#             # ADDED for JSON capture with LLM extraction: track turns
#             if conversation_id and self.conversation_id_cache != conversation_id:
#                 self.conversation_id_cache = conversation_id
#             current_id = self.conversation_id_cache or conversation_id or "unknown"

#             if human_input:
#                 self.turns.append({"speaker": "user", "text": human_input, "ts": int(time.time()*1000)})
#                 # Trigger lightweight, infrequent LLM extraction to avoid latency every token
#                 if len(self.turns) % 2 == 0:  # every user-bot pair approx.
#                     asyncio.create_task(self._extract_slots_with_llm(current_id))
#                 self._persist_state(current_id)

#             # Helper function to sanitize / replace {name} placeholder in bot replies
#             def personalize_response(text: str) -> str:
#                 if self.user_name:
#                     return text.replace("{name}", self.user_name)
#                 else:
#                     # Replace with external fetch if implemented
#                     external_name = "there"
#                     return text.replace("{name}", external_name)

#             # Timeout: fallback if no transcription for 15s
#             if time.time() - self.last_response_time > 15:
#                 self.no_input_count += 1
#                 logger.warning(f"No transcription for 15 seconds (attempt {self.no_input_count}), sending fallback")
#                 if self.no_input_count >= 3:
#                     logger.info("No valid input after 3 fallback attempts, ending call")
#                     bot_text = personalize_response("It seems we’re having trouble connecting. I’ll follow up later. Thank you!")
#                     self.turns.append({"speaker":"bot","text":bot_text,"ts":int(time.time()*1000)})
#                     self._persist_state(current_id)
#                     return bot_text, True
#                 bot_text = personalize_response("I didn't catch that clearly. Could you confirm if you're available to discuss chess coaching opportunities?")
#                 self.turns.append({"speaker":"bot","text":bot_text,"ts":int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return bot_text, False

#             # Normalize input for checks
#             normalized = (human_input or "").strip().lower()

#             # Basic heuristic: ignore very short or common filler responses
#             filler_phrases = {"", "mhmm", "okay", "what", "yes", "no", "a-", "four", "hello", "hi"}
#             if normalized in filler_phrases:
#                 self.no_input_count += 1
#                 logger.debug(f"Detected filler/no meaningful input (count {self.no_input_count}): '{human_input}'")
#                 if self.no_input_count >= 3:
#                     logger.info("No valid input after 3 attempts, ending call")
#                     bot_text = personalize_response("It seems we’re having trouble connecting. I’ll follow up later. Thank you!")
#                     self.turns.append({"speaker":"bot","text":bot_text,"ts":int(time.time()*1000)})
#                     self._persist_state(current_id)
#                     return bot_text, True
#                 self.last_response_time = start_time
#                 if self.conversation_state == "initial":
#                     bot_text = personalize_response("I didn't catch that clearly. Could you confirm if you're available to discuss chess coaching opportunities?")
#                 else:
#                     bot_text = personalize_response("Sorry, I didn't understand. Could you tell me about your current chess involvement?")
#                 self.turns.append({"speaker":"bot","text":bot_text,"ts":int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return bot_text, False

#             # If input looks like gibberish or incomplete question (simple heuristic)
#             gibberish_indicators = ["what is the first time", "first time", "please repeat", "say again"]
#             if any(phrase in normalized for phrase in gibberish_indicators):
#                 logger.debug(f"Input looks like unclear/gibberish: '{human_input}', prompting clarification")
#                 self.no_input_count += 1
#                 if self.no_input_count >= 3:
#                     logger.info("No valid input after 3 unclear attempts, ending call")
#                     bot_text = personalize_response("It seems we’re having trouble connecting. I’ll follow up later. Thank you!")
#                     self.turns.append({"speaker":"bot","text":bot_text,"ts":int(time.time()*1000)})
#                     self._persist_state(current_id)
#                     return bot_text, True
#                 self.last_response_time = start_time
#                 bot_text = personalize_response("Sorry, I didn't catch that. Could you please repeat or say yes/no if you're available?")
#                 self.turns.append({"speaker":"bot","text":bot_text,"ts":int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return bot_text, False

#             # Reset no input count on valid input
#             self.no_input_count = 0

#             # Try extract user name from input if mentioned (very basic detection)
#             # e.g. "My name is Priya"
#             if self.asked_for_name and "name is" in normalized:
#                 try:
#                     name_part = human_input.lower().split("name is", 1)[21].strip().split()
#                     self.user_name = name_part.capitalize()
#                     logger.debug(f"Extracted user name: {self.user_name}")
#                 except Exception:
#                     self.user_name = None

#             # Conversation state machine
#             if self.conversation_state == "initial":
#                 # Expect positive confirmation to move forward
#                 if any(word in normalized for word in ["yes", "sure", "okay", "available"]):
#                     self.conversation_state = "background"
#                     response = "Great! I'm reaching out because you expressed interest in chess coaching. First, could you confirm your current location in Bangalore?"
#                 else:
#                     response = personalize_response("Sorry, I might have misheard you. Could you confirm if you're available to discuss chess coaching opportunities?")
#                 self.last_response_time = start_time
#                 self.turns.append({"speaker":"bot","text":response,"ts":int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return response, False

#             # After initial state, forward input to langchain super() for processing
#             else:
#                 # Forward input to langchain super with timeout to reduce delay
#                 try:
#                     response, should_end = await asyncio.wait_for(
#                         super().respond(human_input, conversation_id, is_interrupt), timeout=5.0
#                     )
#                 except asyncio.TimeoutError:
#                     logger.warning("LLM response timed out")
#                     fallback_msg = personalize_response("Sorry, I'm having trouble responding quickly. Let's try again shortly.")
#                     self.turns.append({"speaker":"bot","text":fallback_msg,"ts":int(time.time()*1000)})
#                     self._persist_state(current_id)
#                     return fallback_msg, False

#                 if response:
#                     response_text = personalize_response(response)
#                     if "location" in response_text.lower():
#                         self.conversation_state = "background"
#                     # Detect if AI asks for name and set flag
#                     if any(phrase in response_text.lower() for phrase in ["confirm your full name", "may i have your name"]):
#                         self.asked_for_name = True
#                     self.last_response_time = start_time
#                     self.turns.append({"speaker":"bot","text":response_text,"ts":int(time.time()*1000)})
#                     # Opportunistically refresh extraction after bot turn too
#                     if len(self.turns) % 4 == 0:
#                         asyncio.create_task(self._extract_slots_with_llm(current_id))
#                     self._persist_state(current_id)
#                     return response_text, should_end

#                 # Fallback generic message if super returns nothing
#                 fallback_msg = personalize_response("Sorry, I didn't quite get that. Could you please tell me more?")
#                 self.last_response_time = start_time
#                 self.turns.append({"speaker":"bot","text":fallback_msg,"ts":int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return fallback_msg, False

#         except Exception as e:
#             logger.error(f"Error generating response: {str(e)}")
#             fallback_error_msg = "Sorry, I encountered an error. Please try again."
#             self.turns.append({"speaker":"bot","text":fallback_error_msg,"ts":int(time.time()*1000)})
#             # Use cached id or fallback
#             current_id = self.conversation_id_cache or conversation_id or "unknown"
#             self._persist_state(current_id)
#             return fallback_error_msg, False

# # Custom Deepgram Transcriber with keepalive and chunk logging
# class CustomDeepgramTranscriber(DeepgramTranscriber):
#     def __init__(self, transcriber_config: DeepgramTranscriberConfig):
#         super().__init__(transcriber_config)
#     async def process(self, audio_chunk: bytes):
#         logger.debug(f"Processing audio chunk size: {len(audio_chunk)} bytes")  # Added
#         if not audio_chunk or len(audio_chunk) == 0:
#             logger.warning("Empty audio chunk - skipping")
#             return None
#         try:
#             return await super().process(audio_chunk)
#         except Exception as e:
#             logger.error(f"Deepgram process error: {e}")
#             raise
#     async def keepalive(self):
#         while True:
#             await asyncio.sleep(10)
#             try:
#                 await super().process(b"\x00" * 160)
#                 logger.debug("Deepgram keepalive sent")
#             except Exception as e:
#                 logger.error(f"Keepalive failed: {e}")
#                 break

# # Custom Agent Factory
# class CustomAgentFactory:
#     def create_agent(self, agent_config: AgentConfig, logger: Optional[logging.Logger] = None) -> BaseAgent:
#         log = logger or globals().get('logger', logging.getLogger(__name__))
#         log.debug(f"Creating agent with config type: {agent_config.type}")
#         if agent_config.type == "agent_langchain":
#             log.debug("Creating CustomLangchainAgent")
#             return CustomLangchainAgent(agent_config=typing.cast(CustomLangchainAgentConfig, agent_config))
#         log.error(f"Invalid agent config type: {agent_config.type}")
#         raise Exception(f"Invalid agent config: {agent_config.type}")

# # Custom Synthesizer Factory
# class CustomSynthesizerFactory:
#     def create_synthesizer(self, synthesizer_config: SynthesizerConfig) -> BaseSynthesizer:
#         logger.debug(f"Creating synthesizer with config: {synthesizer_config}")
#         if isinstance(synthesizer_config, StreamElementsSynthesizerConfig):
#             logger.debug("Creating StreamElementsSynthesizer")
#             return StreamElementsSynthesizer(synthesizer_config)
#         logger.error(f"Invalid synthesizer config type: {synthesizer_config.type}")
#         raise Exception(f"Invalid synthesizer config: {synthesizer_config.type}")

# # FastAPI App
# app = FastAPI()

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     logger.debug("Starting up FastAPI application")
#     logger.debug("Registered routes:")
#     for route in app.routes:
#         methods = getattr(route, "methods", ["WebSocket"])
#         logger.debug(f" - {route.path} ({methods})")
#     yield
#     # ADDED: final sweep to persist any in-memory conversations at shutdown
#     try:
#         for conv_id in list(CONVERSATION_STORE.keys()):
#             out_path = CONVERSATIONS_DIR / f"{conv_id}.json"
#             with open(out_path, "w", encoding="utf-8") as f:
#                 json.dump(CONVERSATION_STORE[conv_id], f, ensure_ascii=False, indent=2)
#         logger.debug("Shutdown flush completed for all conversations")
#     except Exception as e:
#         logger.error(f"Error during shutdown flush: {e}")
#     logger.debug("Shutting down FastAPI application")

# app.router.lifespan_context = lifespan

# # Twilio config
# twilio_config = TwilioConfig(
#     account_sid=TWILIO_ACCOUNT_SID,
#     auth_token=TWILIO_AUTH_TOKEN
# )

# # Synthesizer config (telephone voice output)
# synthesizer_config = StreamElementsSynthesizerConfig.from_telephone_output_device(
#     voice="Brian"
# )

# transcriber_config = DeepgramTranscriberConfig(
#     api_key=DEEPGRAM_API_KEY,
#     model="nova-2-phonecall",
#     language="en",
#     sampling_rate=8000,  # int primitive, not enum
#     audio_encoding="mulaw",  # lowercase string, not enum
#     chunk_size=320,
#     endpointing_config=PunctuationEndpointingConfig(),
#     downsampling=1,
# )

# agent_config = LangchainAgentConfig(
#     initial_message=BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"),
#     prompt_preamble=CHESS_COACH_PROMPT_PREAMBLE,
#     model_name="llama-3.1-8b-instant",
#     # model_name="groq/compound-mini",
#     api_key=GROQ_API_KEY,
#     provider="groq",
# )

# # Create CustomDeepgramTranscriber instance with config
# # custom_deepgram_transcriber = CustomDeepgramTranscriber(transcriber_config)

# # Telephony Server setup
# telephony_server = TelephonyServer(
#     base_url=BASE_URL,  # your ngrok url
#     config_manager=config_manager,
#     inbound_call_configs=[
#         TwilioInboundCallConfig(
#             url="/inbound_call",
#             twilio_config=twilio_config,
#             agent_config=agent_config,
#             synthesizer_config=synthesizer_config,
#             transcriber_config=transcriber_config,  # Use instance
#             twiml_fallback_response='''<?xml version="1.0" encoding="UTF-8"?>
# <Response>
#     <Say>I didn't hear a response. Are you still there? Please say something to continue.</Say>
#     <Pause length="15"/>
#     <Redirect method="POST">/inbound_call</Redirect>
# </Response>'''
#         )
#     ],
#     agent_factory=CustomAgentFactory(),
#     synthesizer_factory=CustomSynthesizerFactory(),
#     events_manager=ChessEventsManager(),
# )

# # Add routes to FastAPI app
# app.include_router(telephony_server.get_router())

# # Outbound call helper
# async def make_outbound_call(to_phone: str):
#     client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#     twilio_base_url = f"https://{BASE_URL}"
#     call = await asyncio.get_event_loop().run_in_executor(
#         None,
#         lambda: client.calls.create(
#             to=to_phone,
#             from_=TWILIO_PHONE_NUMBER,
#             url=f"{twilio_base_url}/inbound_call",
#             status_callback=f"{twilio_base_url}/call_status",
#             status_callback_method="POST",
#             status_callback_event=["initiated", "ringing", "answered", "completed"],
#             record=True,
#             recording_channels="dual",
#         )
#     )
#     logger.info(f"Call initiated: SID={call.sid}")
#     return call.sid

# # Main entrypoint
# if __name__ == "__main__":
#     import uvicorn

#     def run_server():
#         logger.debug("Starting Uvicorn server")
#         uvicorn.run(app, host="0.0.0.0", port=3000)

#     async def start_server_and_call():
#         try:
#             server_thread = threading.Thread(target=run_server, daemon=True)
#             server_thread.start()
#             await asyncio.sleep(2)
#             await make_outbound_call("+917356793165")  # your target phone number
#             await asyncio.Event().wait()
#         except Exception as e:
#             logger.error(f"Error in start_server_and_call: {str(e)}")
#             raise

#     asyncio.run(start_server_and_call())









# import os
# import logging
# import asyncio
# import httpx
# import typing
# import time
# from typing import Optional, Tuple
# from fastapi import FastAPI, Request, Response
# from fastapi.logger import logger as fastapi_logger
# from contextlib import asynccontextmanager
# from dotenv import load_dotenv
# from twilio.rest import Client
# from vocode.streaming.telephony.server.base import TelephonyServer, TwilioInboundCallConfig
# from vocode.streaming.models.telephony import TwilioConfig
# from vocode.streaming.models.agent import LangchainAgentConfig, AgentConfig
# from vocode.streaming.agent.langchain_agent import LangchainAgent
# from vocode.streaming.models.message import BaseMessage
# from vocode.streaming.transcriber.deepgram_transcriber import DeepgramTranscriber
# from vocode.streaming.models.transcriber import DeepgramTranscriberConfig, AudioEncoding, PunctuationEndpointingConfig
# from vocode.streaming.synthesizer.stream_elements_synthesizer import StreamElementsSynthesizer
# from vocode.streaming.models.synthesizer import StreamElementsSynthesizerConfig, SynthesizerConfig
# from vocode.streaming.synthesizer.base_synthesizer import BaseSynthesizer
# from vocode.streaming.telephony.config_manager.in_memory_config_manager import InMemoryConfigManager
# from vocode.streaming.agent.base_agent import BaseAgent
# from vocode.streaming.models.events import Event, EventType
# from vocode.streaming.models.transcript import TranscriptCompleteEvent
# from vocode.streaming.utils import events_manager
# from langchain_groq import ChatGroq
# import threading
# import numpy as np

# # ADDED for JSON capture with LLM extraction
# import json  # ADDED for JSON capture with LLM extraction
# import re    # ADDED: general regex utilities
# from pathlib import Path  # ADDED: filesystem-safe paths
# from fastapi import HTTPException  # ADDED n8n
# from pydantic import BaseModel  # ADDED n8n

# # Configure logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# fastapi_logger.setLevel(logging.DEBUG)

# # Ensure ffmpeg is in PATH
# os.environ['PATH'] += os.pathsep + 'C:\\ffmpeg\\bin'

# load_dotenv()

# # Environment variables
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
# TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
# TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
# BASE_URL = os.getenv("BASE_URL")
# DEBUG_AUDIO = os.getenv("DEBUG_AUDIO", "false").lower() == "true"

# # Validate environment variables
# required_vars = [GROQ_API_KEY, DEEPGRAM_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, BASE_URL]
# if not all(required_vars):
#     raise ValueError("Missing required environment variables in .env file. Required: GROQ_API_KEY, DEEPGRAM_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, BASE_URL")

# # Validate Ngrok URL
# if not BASE_URL.endswith((".ngrok-free.app", ".ngrok.io")):
#     logger.warning(f"BASE_URL ({BASE_URL}) does not appear to be a valid Ngrok URL. Ensure it matches the current Ngrok session and is updated in Twilio Console.")

# # Chess coach prompt
# CHESS_COACH_PROMPT_PREAMBLE = """
# # Chess Coaching Sales Representative Prompt
# ## Identity & Purpose
# You are Priya, a virtual sales representative for 4champz, a leading chess coaching service provider based in Bengaluru, India. We specialize in providing qualified chess coaches to schools across Bangalore. 
# Your primary purpose is to qualify leads who have shown interest in chess coaching opportunities, understand their background and experience, and explore potential collaboration as a chess coach for our school programs.
# ## Voice & Persona
# ### Personality
# - Sound professional, warm, and conversational—like a knowledgeable chess enthusiast
# - Project genuine interest in learning about their chess journey
# - Maintain an engaging and respectful demeanor throughout the conversation
# - Show respect for their time while staying focused on understanding their suitability for school coaching
# - Convey enthusiasm about the opportunity to shape young minds through chess
# ### Speech Characteristics
# - Use clear, conversational language with natural flow
# - Keep messages under 150 characters when possible
# - Include probing questions to gather detailed information
# - Show genuine interest in their chess background and achievements
# - Use encouraging language when discussing their experience and qualifications
# ## Conversation Flow
# ### Introduction
# 1. Start with: "Hello {{name}}, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"
# 2. Follow with: "I'm reaching out because you expressed interest in chess coaching. I'd love to learn more about your chess background and explore how we might work together."
# ### Current Involvement Assessment
# - Location confirmation: "First, could you confirm your current location in Bangalore?"
# - Chess involvement: "Tell me about your current chess involvement—are you actively playing or coaching?"
# - Availability overview: "What does your current schedule look like, particularly during afternoon hours?"
# ### Experience and Background Qualification
# #### Chess playing experience:
# - "What's your current chess rating with FIDE or All India Chess Federation?"
# - "What's your highest tournament achievement?"
# - "How long have you been playing chess competitively?"
# #### Tournament participation:
# - "Tell me about your recent tournament participation and notable results"
# - "Have you participated in any state or national level competitions?"
# #### Coaching and teaching experience:
# - "Have you worked with school children before, either in chess or other subjects?"
# - "Do you have any coaching or teaching experience, especially with children?"
# - "Are you comfortable teaching chess in both English and Kannada/Hindi?"
# #### Educational qualifications:
# - "What are your educational qualifications?"
# - "Do you have any chess certifications or coaching credentials?"
# ### School Coaching Interest Exploration
# - Explain the opportunity: "Let me tell you about our model—we provide qualified chess coaches to reputed schools across Bangalore. Our coaches work directly with students during school hours."
# #### Availability assessment:
# - "Are you available for school hours, typically between 3-6 PM?"
# - "How many days per week would you be interested in coaching?"
# - "Which areas of Bangalore can you travel to for coaching assignments?"
# #### Age group comfort:
# - "Are you comfortable teaching different age groups, from Classes 1 through 12?"
# - "Do you have any preference for specific age groups?"
# #### Support and training:
# - "We provide comprehensive training and curriculum support to all our coaches. How do you feel about following a structured curriculum?"
# - "Are you interested in ongoing professional development in chess coaching?"
# ### Schedule and Close
# If they seem suitable and interested:
# - "Based on our conversation, I think there could be a great fit here. I'd like to schedule a detailed discussion and assessment with you."
# - Use check_calendar_availability for follow-up meetings
# - If proceeding: Call book_appointment
# - "Could you confirm your full name, email address, and preferred meeting time?"
# - Positive close: "Thank you for your time, {{name}}. We'll send you more details about our school programs and compensation structure. I'm looking forward to speaking with you soon about this exciting opportunity!"
# - Always end with end_call unless transferred
# ## Response Guidelines
# - Keep responses focused on qualifying their suitability for school coaching
# - Ask location-specific questions about Bangalore areas they can cover
# - Show genuine enthusiasm for their chess achievements and experience
# - Be respectful of their current commitments and time constraints
# - Use IST timing when scheduling appointments
# - Emphasize the opportunity to impact young minds through chess education
# - Ask only one detailed question at a time to avoid overwhelming them
# ## Scenario Handling
# ### For Highly Qualified Candidates
# - Express enthusiasm: "Your tournament experience and rating are impressive! Our partner schools would definitely value someone with your background."
# - Fast-track process: "Given your qualifications, I'd love to expedite our discussion. When would be the best time for a detailed conversation this week?"
# - Highlight premium opportunities: "With your experience, you'd be perfect for our advanced chess program placements at premium schools."
# ### For Candidates with Limited Formal Experience
# - Explore potential: "While formal ratings are helpful, we also value passion and teaching ability. Tell me about your experience working with children or young people."
# - Training emphasis: "We provide comprehensive training to help coaches develop their skills. Are you excited about growing your coaching abilities with our support?"
# - Alternative qualifications: "Have you been involved in chess clubs, online coaching, or informal teaching that might not show up in formal ratings?"
# ### For Candidates Requesting Human Assistance
# - If they want to speak with a human or need more details about compensation/partnerships:
#   - Use transfer_call
#   - Say: "Of course! Let me connect you with our placement manager who can give you detailed information about our school partnerships, compensation structure, and specific placement opportunities."
# ### For Availability Concerns
# - Flexible scheduling: "We work with various schools, so we can often accommodate different availability preferences. What times work best for you?"
# - Part-time opportunities: "Many of our coaches start part-time and gradually increase their involvement. Would that approach interest you?"
# - Location matching: "We'll match you with schools in areas convenient for you. Which parts of Bangalore are most accessible?"
# ## Knowledge Base
# ### Caller Information Variables
# - name: {{name}}
# - email: {{email}}
# - phone_number: {{phone_number}}
# - role: {{role}}
# ### 4champz Service Model
# - Leading chess coaching service provider in Bengaluru
# - Specializes in providing qualified coaches to schools across Bangalore
# - Partners with reputed schools throughout the city
# - Provides comprehensive training and curriculum support
# - Offers both part-time and full-time coaching opportunities
# - Focuses on developing young chess talent in school settings
# ### Coaching Requirements
# - School hours availability (typically 3-6 PM)
# - Ability to teach students from Classes 1-12
# - Comfort with English and preferably Kannada/Hindi
# - Transportation capability across Bangalore areas
# - Professional attitude and teaching aptitude
# - Chess knowledge appropriate for school-level instruction
# ### Assessment Criteria
# - Chess playing experience and rating (FIDE/All India Chess Federation)
# - Tournament participation and achievements
# - Prior coaching or teaching experience, especially with children
# - Educational qualifications and chess certifications
# - Language capabilities and communication skills
# - Geographic availability across Bangalore
# - Flexibility with scheduling and age groups
# ## Response Refinement
# - When discussing their chess background: "Your chess journey sounds fascinating. Could you tell more about [specific aspect they mentioned]?"
# - When explaining opportunities: "Let me paint a picture of what coaching with our partner schools looks like..."
# - When confirming details: "Just to make sure I have everything right—you're available [summarize their availability] and comfortable teaching [summarize their preferences]. Is that accurate?"
# ## Call Management
# ### Available Functions
# - check_calendar_availability: Use when scheduling follow-up meetings
# - book_appointment: Use when confirming scheduled appointments
# - transfer_call: Use when candidate requests human assistance
# - end_call: Use to properly conclude every conversation
# ## Technical Considerations
# - If experiencing delays accessing calendar: "I'm just checking our available appointment slots. This will take just a moment."
# - If multiple scheduling needs arise: "Let me handle your appointment booking first, and then we can discuss any additional questions."
# - Always confirm appointment details before ending: "To confirm, we're scheduled for [day], [date] at [time]. You'll receive an email confirmation shortly."
# ---
# Remember that your ultimate goal is to identify qualified chess coaches who can positively impact students in Bangalore schools while ensuring they understand the opportunity and feel excited about the partnership. Accuracy in qualifying candidates and scheduling follow-ups is your top priority, followed by creating enthusiasm for the teaching opportunity and maintaining 4champz's professional reputation.
# """

# # Groq LLM setup
# llm = ChatGroq(model_name="llama-3.1-8b-instant")
# # llm = ChatGroq(model_name="groq/compound-mini")

# # Config Manager
# config_manager = InMemoryConfigManager()

# # ADDED for JSON capture with LLM extraction: global in-memory store
# CONVERSATION_STORE: dict = {}  # ADDED for JSON LLM extraction

# # ADDED for JSON capture with LLM extraction: directory for local persistence
# CONVERSATIONS_DIR = Path("conversations")  # ADDED
# CONVERSATIONS_DIR.mkdir(exist_ok=True, parents=True)  # ADDED

# # ADDED n8n: store lead context by call_sid/conversation_id
# LEAD_CONTEXT_STORE: dict = {}  # ADDED n8n

# # Events Manager to log transcripts
# class ChessEventsManager(events_manager.EventsManager):
#     def __init__(self):
#         super().__init__(subscriptions=[EventType.TRANSCRIPT_COMPLETE])

#     async def handle_event(self, event: Event):
#         if event.type == EventType.TRANSCRIPT_COMPLETE:
#             transcript_complete_event = typing.cast(TranscriptCompleteEvent, event)
#             logger.debug(f"Transcript for conversation {transcript_complete_event.conversation_id}: {transcript_complete_event.transcript.to_string()}")
#             webhook_url = os.getenv("TRANSCRIPT_CALLBACK_URL")
#             if webhook_url:
#                 data = {"conversation_id": transcript_complete_event.conversation_id, "user_id": 1, "transcript": transcript_complete_event.transcript.to_string()}
#                 async with httpx.AsyncClient() as client:
#                     response = await client.post(webhook_url, json=data)
#                     if response.status_code == 200:
#                         logger.info("Transcript sent successfully to webhook")
#                     else:
#                         logger.error(f"Failed to send transcript to webhook: {response.status_code}")
#             # ADDED for JSON capture with LLM extraction: write store JSON to disk
#             try:
#                 convo = CONVERSATION_STORE.get(transcript_complete_event.conversation_id)
#                 if convo:
#                     out_path = CONVERSATIONS_DIR / f"{transcript_complete_event.conversation_id}.json"
#                     with open(out_path, "w", encoding="utf-8") as f:
#                         json.dump(convo, f, ensure_ascii=False, indent=2)
#                     logger.info(f"Wrote JSON summary to {out_path}")
#             except Exception as e:
#                 logger.error(f"Failed to write JSON summary: {e}")

# # Custom Agent Config
# class CustomLangchainAgentConfig(LangchainAgentConfig, type="agent_langchain"):
#     initial_message: BaseMessage = BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?")
#     prompt_preamble: str = CHESS_COACH_PROMPT_PREAMBLE
#     model_name: str = "llama-3.1-8b-instant"
#     # model_name: str = "groq/compound-mini"
#     api_key: str = GROQ_API_KEY
#     provider: str = "groq"

# # Custom Langchain Agent
# class CustomLangchainAgent(LangchainAgent):
#     def __init__(self, agent_config: CustomLangchainAgentConfig):
#         logger.debug(f"Initializing CustomLangchainAgent with config: {agent_config}")
#         super().__init__(agent_config=agent_config)
#         self.last_response_time = time.time()
#         self.conversation_state = "initial"
#         self.no_input_count = 0
#         self.user_name = None  # store extracted/confirmed name
#         self.asked_for_name = False  # track if name is requested
#         logger.debug("Initialized CustomLangchainAgent with Groq LLM (llama-3.1-8b-instant)")
#         # ADDED for JSON capture with LLM extraction
#         self.turns = []  # [{"speaker":"user"/"bot","text":..., "ts": epoch_ms}]
#         self.conversation_id_cache = None  # to index the global store
#         self.extracted_slots = {}  # LLM-extracted structured data


#     # ADDED n8n: helper to ensure id
#     def _ensure_conv_id(self, conversation_id: Optional[str]) -> str:
#         if conversation_id and isinstance(conversation_id, str) and conversation_id.strip():
#             return conversation_id
#         return f"unknown_{int(time.time()*1000)}"

#     # ADDED for JSON capture with LLM extraction
#     def _flush_to_disk(self, conversation_id: str):
#         """Write the current conversation JSON to disk immediately."""
#         try:
#             payload = CONVERSATION_STORE.get(conversation_id)
#             if not payload:
#                 return
#             out_path = CONVERSATIONS_DIR / f"{conversation_id}.json"
#             with open(out_path, "w", encoding="utf-8") as f:
#                 json.dump(payload, f, ensure_ascii=False, indent=2)
#             logger.debug(f"Flushed conversation {conversation_id} to {out_path}")
#         except Exception as e:
#             logger.error(f"Flush to disk failed for {conversation_id}: {e}")

#     # ADDED for JSON capture with LLM extraction
#     def _persist_state(self, conversation_id: Optional[str]):
#         conv_id = self._ensure_conv_id(conversation_id)
#         now_ms = int(time.time() * 1000)
#         lead = LEAD_CONTEXT_STORE.get(conv_id, {})  # ADDED n8n
#         payload = {
#             "conversation_id": conv_id,
#             "updated_at": now_ms,
#             "lead": lead,  # ADDED n8n
#             "slots": self.extracted_slots,  # slots are LLM-extracted
#             "turns": self.turns
#         }
#         CONVERSATION_STORE[conv_id] = payload
#         self._flush_to_disk(conv_id)  # ADDED: always flush on persist

#     # ADDED for JSON capture with LLM extraction
#     def _strip_code_fences(self, s: str) -> str:
#         t = (s or "").strip()
#         if t.startswith("```"):
#             end = t.rfind("```")
#             if end > 0:
#                 inner = t[3:end].strip()
#                 if inner.lower().startswith("json"):
#                     inner = inner[4:].strip()
#                 return inner
#         return t

#     # ADDED for JSON capture with LLM extraction
#     async def _extract_slots_with_llm(self, conversation_id: str):
#         """
#         Call Groq LLM to extract structured fields from the current turns.
#         This minimizes if/else and uses the prompt-defined fields.
#         """
#         try:
#             # Build a compact transcript string (keep it bounded)
#             convo_lines = []
#             for t in self.turns[-30:]:
#                 role = "User" if t["speaker"] == "user" else "Agent"
#                 text_line = re.sub(r'\s+', ' ', t['text']).strip()
#                 convo_lines.append(f"{role}: {text_line}")
#             convo_text = "\n".join(convo_lines)

#             # Instruction for JSON-only schema
#             schema_instruction = (
#                 "Return ONLY a JSON object with these keys:\n"
#                 "{\n"
#                 '  "location": string|null,\n'
#                 '  "involvement": "playing"|"coaching"|null,\n'
#                 '  "availability": string|null,\n'
#                 '  "age_range": string|null,\n'
#                 '  "languages": string[]|null,\n'
#                 '  "rating": string|null,\n'
#                 '  "tournaments": string|null,\n'
#                 '  "certifications": string|null,\n'
#                 '  "questions": string[]|null\n'
#                 "}\n"
#                 "Infer conservatively. Use null if not explicitly known. Do not add extra keys or text."
#             )

#             prompt = f"{schema_instruction}\n\nConversation:\n{convo_text}\n\nJSON:"

#             extractor = ChatGroq(model_name="llama-3.1-8b-instant")
#             resp = await extractor.ainvoke([
#                 {"role": "system", "content": "You extract structured information from conversations."},
#                 {"role": "user", "content": prompt}
#             ])

#             # Normalize content
#             content = None
#             if hasattr(resp, "content"):
#                 content = resp.content
#             elif hasattr(resp, "generations"):
#                 try:
#                     content = resp.generations.text
#                 except Exception:
#                     content = str(resp)
#             else:
#                 content = str(resp)

#             parsed = None
#             try:
#                 c = self._strip_code_fences(content)
#                 parsed = json.loads(c)
#             except Exception:
#                 logger.warning("Primary JSON parse failed; attempting to locate JSON object")
#                 first = content.find("{")
#                 last = content.rfind("}")
#                 if first != -1 and last != -1 and last > first:
#                     snippet = content[first:last+1]
#                     try:
#                         parsed = json.loads(snippet)
#                     except Exception:
#                         parsed = None

#             if isinstance(parsed, dict):
#                 # normalize keys
#                 for k in ["location","involvement","availability","age_range","languages","rating","tournaments","certifications","questions"]:
#                     if k not in parsed:
#                         parsed[k] = None
#                 # Ensure types
#                 if parsed.get("languages") is not None and not isinstance(parsed["languages"], list):
#                     parsed["languages"] = [str(parsed["languages"])]
#                 if parsed.get("questions") is not None and not isinstance(parsed["questions"], list):
#                     parsed["questions"] = [str(parsed["questions"])]

#                 self.extracted_slots = parsed
#                 self._persist_state(conversation_id)
#             else:
#                 logger.warning("LLM extraction did not return a dict; keeping previous slots.")

#         except Exception as e:
#             logger.error(f"Slot extraction failed: {e}")

#     async def respond(self, human_input: str, conversation_id: str, is_interrupt: bool = False) -> Tuple[Optional[str], bool]:
#         try:
#             start_time = time.time()

#             # ADDED for JSON capture with LLM extraction: track turns
#             if conversation_id and self.conversation_id_cache != conversation_id:
#                 self.conversation_id_cache = conversation_id
#             current_id = self.conversation_id_cache or conversation_id or "unknown"

#             if human_input:
#                 self.turns.append({"speaker": "user", "text": human_input, "ts": int(time.time()*1000)})
#                 # Trigger lightweight, infrequent LLM extraction to avoid latency every token
#                 if len(self.turns) % 2 == 0:  # every user-bot pair approx.
#                     asyncio.create_task(self._extract_slots_with_llm(current_id))
#                 self._persist_state(current_id)

#             # Helper function to sanitize / replace {name} placeholder in bot replies
#             def personalize_response(text: str) -> str:
#                 if self.user_name:
#                     return text.replace("{name}", self.user_name)
#                 else:
#                     # Replace with external fetch if implemented
#                     external_name = "there"
#                     return text.replace("{name}", external_name)

#             # Timeout: fallback if no transcription for 15s
#             if time.time() - self.last_response_time > 15:
#                 self.no_input_count += 1
#                 logger.warning(f"No transcription for 15 seconds (attempt {self.no_input_count}), sending fallback")
#                 if self.no_input_count >= 3:
#                     logger.info("No valid input after 3 fallback attempts, ending call")
#                     bot_text = personalize_response("It seems we’re having trouble connecting. I’ll follow up later. Thank you!")
#                     self.turns.append({"speaker":"bot","text":bot_text,"ts":int(time.time()*1000)})
#                     self._persist_state(current_id)
#                     return bot_text, True
#                 bot_text = personalize_response("I didn't catch that clearly. Could you confirm if you're available to discuss chess coaching opportunities?")
#                 self.turns.append({"speaker":"bot","text":bot_text,"ts":int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return bot_text, False

#             # Normalize input for checks
#             normalized = (human_input or "").strip().lower()

#             # Basic heuristic: ignore very short or common filler responses
#             filler_phrases = {"", "mhmm", "okay", "what", "yes", "no", "a-", "four", "hello", "hi"}
#             if normalized in filler_phrases:
#                 self.no_input_count += 1
#                 logger.debug(f"Detected filler/no meaningful input (count {self.no_input_count}): '{human_input}'")
#                 if self.no_input_count >= 3:
#                     logger.info("No valid input after 3 attempts, ending call")
#                     bot_text = personalize_response("It seems we’re having trouble connecting. I’ll follow up later. Thank you!")
#                     self.turns.append({"speaker":"bot","text":bot_text,"ts":int(time.time()*1000)})
#                     self._persist_state(current_id)
#                     return bot_text, True
#                 self.last_response_time = start_time
#                 if self.conversation_state == "initial":
#                     bot_text = personalize_response("I didn't catch that clearly. Could you confirm if you're available to discuss chess coaching opportunities?")
#                 else:
#                     bot_text = personalize_response("Sorry, I didn't understand. Could you tell me about your current chess involvement?")
#                 self.turns.append({"speaker":"bot","text":bot_text,"ts":int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return bot_text, False

#             # If input looks like gibberish or incomplete question (simple heuristic)
#             gibberish_indicators = ["what is the first time", "first time", "please repeat", "say again"]
#             if any(phrase in normalized for phrase in gibberish_indicators):
#                 logger.debug(f"Input looks like unclear/gibberish: '{human_input}', prompting clarification")
#                 self.no_input_count += 1
#                 if self.no_input_count >= 3:
#                     logger.info("No valid input after 3 unclear attempts, ending call")
#                     bot_text = personalize_response("It seems we’re having trouble connecting. I’ll follow up later. Thank you!")
#                     self.turns.append({"speaker":"bot","text":bot_text,"ts":int(time.time()*1000)})
#                     self._persist_state(current_id)
#                     return bot_text, True
#                 self.last_response_time = start_time
#                 bot_text = personalize_response("Sorry, I didn't catch that. Could you please repeat or say yes/no if you're available?")
#                 self.turns.append({"speaker":"bot","text":bot_text,"ts":int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return bot_text, False

#             # Reset no input count on valid input
#             self.no_input_count = 0

#             # Try extract user name from input if mentioned (very basic detection)
#             # e.g. "My name is Priya"
#             if self.asked_for_name and "name is" in normalized:
#                 try:
#                     name_part = human_input.lower().split("name is", 1)[21].strip().split()
#                     self.user_name = name_part.capitalize()
#                     logger.debug(f"Extracted user name: {self.user_name}")
#                 except Exception:
#                     self.user_name = None

#             # Conversation state machine
#             if self.conversation_state == "initial":
#                 # Expect positive confirmation to move forward
#                 if any(word in normalized for word in ["yes", "sure", "okay", "available"]):
#                     self.conversation_state = "background"
#                     response = "Great! I'm reaching out because you expressed interest in chess coaching. First, could you confirm your current location in Bangalore?"
#                 else:
#                     response = personalize_response("Sorry, I might have misheard you. Could you confirm if you're available to discuss chess coaching opportunities?")
#                 self.last_response_time = start_time
#                 self.turns.append({"speaker":"bot","text":response,"ts":int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return response, False

#             # After initial state, forward input to langchain super() for processing
#             else:
#                 # Forward input to langchain super with timeout to reduce delay
#                 try:
#                     response, should_end = await asyncio.wait_for(
#                         super().respond(human_input, conversation_id, is_interrupt), timeout=5.0
#                     )
#                 except asyncio.TimeoutError:
#                     logger.warning("LLM response timed out")
#                     fallback_msg = personalize_response("Sorry, I'm having trouble responding quickly. Let's try again shortly.")
#                     self.turns.append({"speaker":"bot","text":fallback_msg,"ts":int(time.time()*1000)})
#                     self._persist_state(current_id)
#                     return fallback_msg, False

#                 if response:
#                     response_text = personalize_response(response)
#                     if "location" in response_text.lower():
#                         self.conversation_state = "background"
#                     # Detect if AI asks for name and set flag
#                     if any(phrase in response_text.lower() for phrase in ["confirm your full name", "may i have your name"]):
#                         self.asked_for_name = True
#                     self.last_response_time = start_time
#                     self.turns.append({"speaker":"bot","text":response_text,"ts":int(time.time()*1000)})
#                     # Opportunistically refresh extraction after bot turn too
#                     if len(self.turns) % 4 == 0:
#                         asyncio.create_task(self._extract_slots_with_llm(current_id))
#                     self._persist_state(current_id)
#                     return response_text, should_end

#                 # Fallback generic message if super returns nothing
#                 fallback_msg = personalize_response("Sorry, I didn't quite get that. Could you please tell me more?")
#                 self.last_response_time = start_time
#                 self.turns.append({"speaker":"bot","text":fallback_msg,"ts":int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return fallback_msg, False

#         except Exception as e:
#             logger.error(f"Error generating response: {str(e)}")
#             fallback_error_msg = "Sorry, I encountered an error. Please try again."
#             self.turns.append({"speaker":"bot","text":fallback_error_msg,"ts":int(time.time()*1000)})
#             # Use cached id or fallback
#             current_id = self.conversation_id_cache or conversation_id or "unknown"
#             self._persist_state(current_id)
#             return fallback_error_msg, False

# # Custom Deepgram Transcriber with keepalive and chunk logging
# class CustomDeepgramTranscriber(DeepgramTranscriber):
#     def __init__(self, transcriber_config: DeepgramTranscriberConfig):
#         super().__init__(transcriber_config)
#     async def process(self, audio_chunk: bytes):
#         logger.debug(f"Processing audio chunk size: {len(audio_chunk)} bytes")  # Added
#         if not audio_chunk or len(audio_chunk) == 0:
#             logger.warning("Empty audio chunk - skipping")
#             return None
#         try:
#             return await super().process(audio_chunk)
#         except Exception as e:
#             logger.error(f"Deepgram process error: {e}")
#             raise
#     async def keepalive(self):
#         while True:
#             await asyncio.sleep(10)
#             try:
#                 await super().process(b"\x00" * 160)
#                 logger.debug("Deepgram keepalive sent")
#             except Exception as e:
#                 logger.error(f"Keepalive failed: {e}")
#                 break

# # Custom Agent Factory
# class CustomAgentFactory:
#     def create_agent(self, agent_config: AgentConfig, logger: Optional[logging.Logger] = None) -> BaseAgent:
#         log = logger or globals().get('logger', logging.getLogger(__name__))
#         log.debug(f"Creating agent with config type: {agent_config.type}")
#         if agent_config.type == "agent_langchain":
#             log.debug("Creating CustomLangchainAgent")
#             return CustomLangchainAgent(agent_config=typing.cast(CustomLangchainAgentConfig, agent_config))
#         log.error(f"Invalid agent config type: {agent_config.type}")
#         raise Exception(f"Invalid agent config: {agent_config.type}")

# # Custom Synthesizer Factory
# class CustomSynthesizerFactory:
#     def create_synthesizer(self, synthesizer_config: SynthesizerConfig) -> BaseSynthesizer:
#         logger.debug(f"Creating synthesizer with config: {synthesizer_config}")
#         if isinstance(synthesizer_config, StreamElementsSynthesizerConfig):
#             logger.debug("Creating StreamElementsSynthesizer")
#             return StreamElementsSynthesizer(synthesizer_config)
#         logger.error(f"Invalid synthesizer config type: {synthesizer_config.type}")
#         raise Exception(f"Invalid synthesizer config: {synthesizer_config.type}")

# # FastAPI App
# app = FastAPI()

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     logger.debug("Starting up FastAPI application")
#     logger.debug("Registered routes:")
#     for route in app.routes:
#         methods = getattr(route, "methods", ["WebSocket"])
#         logger.debug(f" - {route.path} ({methods})")
#     yield
#     # ADDED: final sweep to persist any in-memory conversations at shutdown
#     try:
#         for conv_id in list(CONVERSATION_STORE.keys()):
#             out_path = CONVERSATIONS_DIR / f"{conv_id}.json"
#             with open(out_path, "w", encoding="utf-8") as f:
#                 json.dump(CONVERSATION_STORE[conv_id], f, ensure_ascii=False, indent=2)
#         logger.debug("Shutdown flush completed for all conversations")
#     except Exception as e:
#         logger.error(f"Error during shutdown flush: {e}")
#     logger.debug("Shutting down FastAPI application")

# app.router.lifespan_context = lifespan

# # Twilio config
# twilio_config = TwilioConfig(
#     account_sid=TWILIO_ACCOUNT_SID,
#     auth_token=TWILIO_AUTH_TOKEN
# )

# # Synthesizer config (telephone voice output)
# synthesizer_config = StreamElementsSynthesizerConfig.from_telephone_output_device(
#     voice="Brian"
# )

# transcriber_config = DeepgramTranscriberConfig(
#     api_key=DEEPGRAM_API_KEY,
#     model="nova-2-phonecall",
#     language="en",
#     sampling_rate=8000,  # int primitive, not enum
#     audio_encoding="mulaw",  # lowercase string, not enum
#     chunk_size=320,
#     endpointing_config=PunctuationEndpointingConfig(),
#     downsampling=1,
# )

# agent_config = LangchainAgentConfig(
#     initial_message=BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"),
#     prompt_preamble=CHESS_COACH_PROMPT_PREAMBLE,
#     model_name="llama-3.1-8b-instant",
#     # model_name="groq/compound-mini",
#     api_key=GROQ_API_KEY,
#     provider="groq",
# )



# # Telephony Server setup
# telephony_server = TelephonyServer(
#     base_url=BASE_URL,  # your ngrok url
#     config_manager=config_manager,
#     inbound_call_configs=[
#         TwilioInboundCallConfig(
#             url="/inbound_call",
#             twilio_config=twilio_config,
#             agent_config=agent_config,
#             synthesizer_config=synthesizer_config,
#             transcriber_config=transcriber_config,  # Use instance
#             twiml_fallback_response='''<?xml version="1.0" encoding="UTF-8"?>
# <Response>
#     <Say>I didn't hear a response. Are you still there? Please say something to continue.</Say>
#     <Pause length="15"/>
#     <Redirect method="POST">/inbound_call</Redirect>
# </Response>'''
#         )
#     ],
#     agent_factory=CustomAgentFactory(),
#     synthesizer_factory=CustomSynthesizerFactory(),
#     events_manager=ChessEventsManager(),
# )

# # Add routes to FastAPI app
# app.include_router(telephony_server.get_router())


# # ADDED n8n: request schema for outbound_call
# class OutboundCallRequest(BaseModel):
#     to_phone: str
#     lead: typing.Optional[typing.Dict[str, typing.Any]] = None
#     transcript_callback_url: typing.Optional[str] = None

# # ADDED n8n: normalize to E164 basic
# def normalize_e164(number: str) -> str:
#     n = re.sub(r'\D+', '', number or '')
#     if not n:
#         return number
#     if n.startswith('0'):
#         n = n.lstrip('0')
#     if not n.startswith('+'):
#         if len(n) == 10:
#             n = '+91' + n
#         else:
#             n = '+' + n
#     return n

# # ADDED n8n: HTTP endpoint to start outbound call from n8n
# @app.post("/outbound_call")
# async def outbound_call(req: OutboundCallRequest):
#     try:
#         to_phone = normalize_e164(req.to_phone)
#         if not to_phone or len(to_phone) < 10:
#             raise HTTPException(status_code=400, detail="Invalid phone")
#         sid = await make_outbound_call(to_phone)
#         lead = req.lead or {}
#         lead["to_phone"] = to_phone
#         LEAD_CONTEXT_STORE[sid] = lead
#         logger.info(f"Outbound call requested via n8n: SID={sid}, lead={lead}")
#         if req.transcript_callback_url:
#             os.environ["TRANSCRIPT_CALLBACK_URL"] = req.transcript_callback_url
#         return {"ok": True, "call_sid": sid}
#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"/outbound_call failed: {e}")
#         raise HTTPException(status_code=500, detail=str(e))


# # Outbound call helper
# async def make_outbound_call(to_phone: str):
#     client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#     twilio_base_url = f"https://{BASE_URL}"
#     call = await asyncio.get_event_loop().run_in_executor(
#         None,
#         lambda: client.calls.create(
#             to=to_phone,
#             from_=TWILIO_PHONE_NUMBER,
#             url=f"{twilio_base_url}/inbound_call",
#             status_callback=f"{twilio_base_url}/call_status",
#             status_callback_method="POST",
#             status_callback_event=["initiated", "ringing", "answered", "completed"],
#             record=True,
#             recording_channels="dual",
#         )
#     )
#     logger.info(f"Call initiated: SID={call.sid}")
#     if call.sid not in LEAD_CONTEXT_STORE:
#         LEAD_CONTEXT_STORE[call.sid] = {"to_phone": to_phone}
#     CONVERSATION_STORE.setdefault(call.sid, {
#         "conversation_id": call.sid,
#         "updated_at": int(time.time()*1000),
#         "lead": LEAD_CONTEXT_STORE.get(call.sid, {}),
#         "slots": {},
#         "turns": []
#     })
#     return call.sid


# # Main entrypoint
# if __name__ == "__main__":
#     import uvicorn

#     def run_server():
#         logger.debug("Starting Uvicorn server")
#         uvicorn.run(app, host="0.0.0.0", port=3000)

#     # async def start_server_and_call():
#     #     try:
#     #         server_thread = threading.Thread(target=run_server, daemon=True)
#     #         server_thread.start()
#     #         await asyncio.sleep(2)
#     #         await make_outbound_call("+917356793165")  # your target phone number
#     #         await asyncio.Event().wait()
#     #     except Exception as e:
#     #         logger.error(f"Error in start_server_and_call: {str(e)}")
#     #         raise

#     # asyncio.run(start_server_and_call())


#     run_server() 



















# import os
# import logging
# import asyncio
# import httpx
# import typing
# import time
# from typing import Optional, Tuple
# from fastapi import FastAPI, Request, Response
# from fastapi.logger import logger as fastapi_logger
# from contextlib import asynccontextmanager
# from dotenv import load_dotenv
# from twilio.rest import Client
# from vocode.streaming.telephony.server.base import TelephonyServer, TwilioInboundCallConfig
# from vocode.streaming.models.telephony import TwilioConfig
# from vocode.streaming.models.agent import LangchainAgentConfig, AgentConfig
# from vocode.streaming.agent.langchain_agent import LangchainAgent
# from vocode.streaming.models.message import BaseMessage
# from vocode.streaming.transcriber.deepgram_transcriber import DeepgramTranscriber
# from vocode.streaming.models.transcriber import DeepgramTranscriberConfig, AudioEncoding, PunctuationEndpointingConfig
# from vocode.streaming.synthesizer.stream_elements_synthesizer import StreamElementsSynthesizer
# from vocode.streaming.models.synthesizer import StreamElementsSynthesizerConfig, SynthesizerConfig
# from vocode.streaming.synthesizer.base_synthesizer import BaseSynthesizer
# from vocode.streaming.telephony.config_manager.in_memory_config_manager import InMemoryConfigManager
# from vocode.streaming.agent.base_agent import BaseAgent
# from vocode.streaming.models.events import Event, EventType
# from vocode.streaming.models.transcript import TranscriptCompleteEvent
# from vocode.streaming.utils import events_manager
# from langchain_groq import ChatGroq
# import threading
# import numpy as np

# # ADDED for JSON capture with LLM extraction
# import json  # ADDED for JSON capture with LLM extraction
# import re    # ADDED: general regex utilities
# from pathlib import Path  # ADDED: filesystem-safe paths
# from fastapi import HTTPException  # ADDED n8n
# from pydantic import BaseModel  # ADDED n8n

# # NEW: For sentiment analysis and summaries (using Groq LLM)
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain


# # NEW: For email summaries (simple SMTP)
# import smtplib
# from email.mime.text import MIMEText

# # NEW: For WhatsApp summaries (using Twilio)
# from twilio.rest import Client as TwilioClient

# # NEW: Placeholder CRM API (replace with your CRM, e.g., HubSpot API)
# import requests  # NEW: for CRM API calls


# from pydub import AudioSegment  # NEW: For audio conversion (MP3/WAV)
# import wave  # NEW: For WAV file handling
# import io

# # Configure logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# fastapi_logger.setLevel(logging.DEBUG)

# # Ensure ffmpeg is in PATH
# os.environ['PATH'] += os.pathsep + 'C:\\ffmpeg\\bin'

# load_dotenv()

# # Environment variables
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
# TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
# TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
# BASE_URL = os.getenv("BASE_URL")
# DEBUG_AUDIO = os.getenv("DEBUG_AUDIO", "false").lower() == "true"


# # NEW: Storage directory for recordings
# RECORDINGS_DIR = Path("recordings")
# RECORDINGS_DIR.mkdir(exist_ok=True, parents=True)

# # NEW: Cloud storage URL (e.g., AWS S3 placeholder)
# CLOUD_STORAGE_URL = os.getenv("CLOUD_STORAGE_URL", "https://your-s3-bucket.s3.amazonaws.com/")


# # NEW: CRM environment variables (replace with your CRM details)
# CRM_API_URL = os.getenv("CRM_API_URL", "https://your-crm-api.com/leads")
# CRM_API_KEY = os.getenv("CRM_API_KEY", "your_crm_api_key")
# EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER", "smtp.example.com")
# EMAIL_SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", 587))
# EMAIL_SENDER = os.getenv("EMAIL_SENDER", "priya@4champz.com")
# EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your_email_password")
# CALENDAR_API_URL = os.getenv("CALENDAR_API_URL", "https://your-calendar-api.com/availability")  # NEW: for scheduling

# # NEW: WhatsApp sender number (for summaries)
# WHATSAPP_SENDER = os.getenv("WHATSAPP_SENDER", TWILIO_PHONE_NUMBER)



# # Validate environment variables
# required_vars = [GROQ_API_KEY, DEEPGRAM_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, BASE_URL, CRM_API_URL, CRM_API_KEY, EMAIL_SMTP_SERVER, EMAIL_SENDER, EMAIL_PASSWORD, CALENDAR_API_URL]
# if not all(required_vars):
#     raise ValueError("Missing required environment variables in .env file. Required: GROQ_API_KEY, DEEPGRAM_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, BASE_URL")

# # Validate Ngrok URL
# if not BASE_URL.endswith((".ngrok-free.app", ".ngrok.io")):
#     logger.warning(f"BASE_URL ({BASE_URL}) does not appear to be a valid Ngrok URL. Ensure it matches the current Ngrok session and is updated in Twilio Console.")

# # Chess coach prompt
# # CHESS_COACH_PROMPT_PREAMBLE = """
# # # Chess Coaching Sales Representative Prompt
# # ## Identity & Purpose
# # You are Priya, a virtual sales representative for 4champz, a leading chess coaching service provider based in Bengaluru, India. We specialize in providing qualified chess coaches to schools across Bangalore. 
# # Your primary purpose is to qualify leads who have shown interest in chess coaching opportunities, understand their background and experience, and explore potential collaboration as a chess coach for our school programs.
# # ## Voice & Persona
# # ### Personality
# # - Sound professional, warm, and conversational—like a knowledgeable chess enthusiast
# # - Project genuine interest in learning about their chess journey
# # - Maintain an engaging and respectful demeanor throughout the conversation
# # - Show respect for their time while staying focused on understanding their suitability for school coaching
# # - Convey enthusiasm about the opportunity to shape young minds through chess
# # ### Speech Characteristics
# # - Use clear, conversational language with natural flow
# # - Keep messages under 150 characters when possible
# # - Include probing questions to gather detailed information
# # - Show genuine interest in their chess background and achievements
# # - Use encouraging language when discussing their experience and qualifications
# # ## Conversation Flow
# # ### Introduction
# # 1. Start with: "Hello {{name}}, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"
# # 2. Follow with: "I'm reaching out because you expressed interest in chess coaching. I'd love to learn more about your chess background and explore how we might work together."
# # ### Current Involvement Assessment
# # - Location confirmation: "First, could you confirm your current location in Bangalore?"
# # - Chess involvement: "Tell me about your current chess involvement—are you actively playing or coaching?"
# # - Availability overview: "What does your current schedule look like, particularly during afternoon hours?"
# # ### Experience and Background Qualification
# # #### Chess playing experience:
# # - "What's your current chess rating with FIDE or All India Chess Federation?"
# # - "What's your highest tournament achievement?"
# # - "How long have you been playing chess competitively?"
# # #### Tournament participation:
# # - "Tell me about your recent tournament participation and notable results"
# # - "Have you participated in any state or national level competitions?"
# # #### Coaching and teaching experience:
# # - "Have you worked with school children before, either in chess or other subjects?"
# # - "Do you have any coaching or teaching experience, especially with children?"
# # - "Are you comfortable teaching chess in both English and Kannada/Hindi?"
# # #### Educational qualifications:
# # - "What are your educational qualifications?"
# # - "Do you have any chess certifications or coaching credentials?"
# # ### School Coaching Interest Exploration
# # - Explain the opportunity: "Let me tell you about our model—we provide qualified chess coaches to reputed schools across Bangalore. Our coaches work directly with students during school hours."
# # #### Availability assessment:
# # - "Are you available for school hours, typically between 3-6 PM?"
# # - "How many days per week would you be interested in coaching?"
# # - "Which areas of Bangalore can you travel to for coaching assignments?"
# # #### Age group comfort:
# # - "Are you comfortable teaching different age groups, from Classes 1 through 12?"
# # - "Do you have any preference for specific age groups?"
# # #### Support and training:
# # - "We provide comprehensive training and curriculum support to all our coaches. How do you feel about following a structured curriculum?"
# # - "Are you interested in ongoing professional development in chess coaching?"
# # ### Schedule and Close
# # If they seem suitable and interested:
# # - "Based on our conversation, I think there could be a great fit here. I'd like to schedule a detailed discussion and assessment with you."
# # - Use check_calendar_availability for follow-up meetings
# # - If proceeding: Call book_appointment
# # - "Could you confirm your full name, email address, and preferred meeting time?"
# # - Positive close: "Thank you for your time, {{name}}. We'll send you more details about our school programs and compensation structure. I'm looking forward to speaking with you soon about this exciting opportunity!"
# # - Always end with end_call unless transferred
# # ## Response Guidelines
# # - Keep responses focused on qualifying their suitability for school coaching
# # - Ask location-specific questions about Bangalore areas they can cover
# # - Show genuine enthusiasm for their chess achievements and experience
# # - Be respectful of their current commitments and time constraints
# # - Use IST timing when scheduling appointments
# # - Emphasize the opportunity to impact young minds through chess education
# # - Ask only one detailed question at a time to avoid overwhelming them
# # ## Scenario Handling
# # ### For Highly Qualified Candidates
# # - Express enthusiasm: "Your tournament experience and rating are impressive! Our partner schools would definitely value someone with your background."
# # - Fast-track process: "Given your qualifications, I'd love to expedite our discussion. When would be the best time for a detailed conversation this week?"
# # - Highlight premium opportunities: "With your experience, you'd be perfect for our advanced chess program placements at premium schools."
# # ### For Candidates with Limited Formal Experience
# # - Explore potential: "While formal ratings are helpful, we also value passion and teaching ability. Tell me about your experience working with children or young people."
# # - Training emphasis: "We provide comprehensive training to help coaches develop their skills. Are you excited about growing your coaching abilities with our support?"
# # - Alternative qualifications: "Have you been involved in chess clubs, online coaching, or informal teaching that might not show up in formal ratings?"
# # ### For Candidates Requesting Human Assistance
# # - If they want to speak with a human or need more details about compensation/partnerships:
# #   - Use transfer_call
# #   - Say: "Of course! Let me connect you with our placement manager who can give you detailed information about our school partnerships, compensation structure, and specific placement opportunities."
# # ### For Availability Concerns
# # - Flexible scheduling: "We work with various schools, so we can often accommodate different availability preferences. What times work best for you?"
# # - Part-time opportunities: "Many of our coaches start part-time and gradually increase their involvement. Would that approach interest you?"
# # - Location matching: "We'll match you with schools in areas convenient for you. Which parts of Bangalore are most accessible?"
# # ## Knowledge Base
# # ### Caller Information Variables
# # - name: {{name}}
# # - email: {{email}}
# # - phone_number: {{phone_number}}
# # - role: {{role}}
# # ### 4champz Service Model
# # - Leading chess coaching service provider in Bengaluru
# # - Specializes in providing qualified coaches to schools across Bangalore
# # - Partners with reputed schools throughout the city
# # - Provides comprehensive training and curriculum support
# # - Offers both part-time and full-time coaching opportunities
# # - Focuses on developing young chess talent in school settings
# # ### Coaching Requirements
# # - School hours availability (typically 3-6 PM)
# # - Ability to teach students from Classes 1-12
# # - Comfort with English and preferably Kannada/Hindi
# # - Transportation capability across Bangalore areas
# # - Professional attitude and teaching aptitude
# # - Chess knowledge appropriate for school-level instruction
# # ### Assessment Criteria
# # - Chess playing experience and rating (FIDE/All India Chess Federation)
# # - Tournament participation and achievements
# # - Prior coaching or teaching experience, especially with children
# # - Educational qualifications and chess certifications
# # - Language capabilities and communication skills
# # - Geographic availability across Bangalore
# # - Flexibility with scheduling and age groups
# # ## Response Refinement
# # - When discussing their chess background: "Your chess journey sounds fascinating. Could you tell more about [specific aspect they mentioned]?"
# # - When explaining opportunities: "Let me paint a picture of what coaching with our partner schools looks like..."
# # - When confirming details: "Just to make sure I have everything right—you're available [summarize their availability] and comfortable teaching [summarize their preferences]. Is that accurate?"
# # ## Call Management
# # ### Available Functions
# # - check_calendar_availability: Use when scheduling follow-up meetings
# # - book_appointment: Use when confirming scheduled appointments
# # - transfer_call: Use when candidate requests human assistance
# # - end_call: Use to properly conclude every conversation
# # ## Technical Considerations
# # - If experiencing delays accessing calendar: "I'm just checking our available appointment slots. This will take just a moment."
# # - If multiple scheduling needs arise: "Let me handle your appointment booking first, and then we can discuss any additional questions."
# # - Always confirm appointment details before ending: "To confirm, we're scheduled for [day], [date] at [time]. You'll receive an email confirmation shortly."
# # ---
# # Remember that your ultimate goal is to identify qualified chess coaches who can positively impact students in Bangalore schools while ensuring they understand the opportunity and feel excited about the partnership. Accuracy in qualifying candidates and scheduling follow-ups is your top priority, followed by creating enthusiasm for the teaching opportunity and maintaining 4champz's professional reputation.
# # """



# CHESS_COACH_PROMPT_PREAMBLE = """
# # Chess Coaching Sales Representative Prompt
# ## Identity & Purpose
# You are Priya, a virtual sales representative for 4champz, a leading chess coaching service provider based in Bengaluru, India. We specialize in providing qualified chess coaches to schools across Bangalore. 
# Your primary purpose is to qualify leads who have shown interest in chess coaching opportunities, understand their background and experience, explore potential collaboration as a chess coach for our school programs, handle FAQs, and schedule meetings for both inbound and outbound calls.
# ## Voice & Persona
# ### Personality
# - Sound professional, warm, and conversational—like a knowledgeable chess enthusiast
# - Project genuine interest in learning about their chess journey
# - Maintain an engaging and respectful demeanor throughout the conversation
# - Show respect for their time while staying focused on understanding their suitability for school coaching
# - Convey enthusiasm about the opportunity to shape young minds through chess
# ### Speech Characteristics
# - Use clear, conversational language with natural flow
# - Keep messages under 150 characters when possible
# - Include probing questions to gather detailed information
# - Show genuine interest in their chess background and achievements
# - Use encouraging language when discussing their experience and qualifications
# ## Conversation Flow
# ### Introduction
# 1. For inbound: "Hello {{name}}, this is Priya from 4champz. Do you have 5-10 minutes to discuss chess coaching opportunities in Bangalore?"
# 2. For outbound: "Hello {{name}}, this is Priya from 4champz. I’m reaching out due to your interest. Available to discuss?"
# 3. Follow with: "I’d love to explore your background, answer FAQs like pricing or timings, or assist with reminders if applicable."
# ### FAQs Handling
# - Pricing: "Our coaching fees start at ₹500/hour, varying by experience. Interested in details?"
# - Timings: "Coaching is typically 3-6 PM school hours. Flexible options available—want to discuss?"
# - Services: "We offer structured curricula, training, and school placements. More questions?"
# ### Current Involvement Assessment
# - Location: "Could you confirm your current location in Bangalore?"
# - Involvement: "Are you actively playing or coaching chess?"
# - Availability: "What’s your schedule like, especially afternoons?"
# ### Experience and Background Qualification
# - Chess playing: "What’s your FIDE or All India Chess Federation rating?"
# - Tournaments: "Tell me about your recent tournament participation."
# - Coaching: "Have you coached children before, especially in chess?"
# - Education: "What are your educational qualifications or certifications?"
# ### School Coaching Interest
# - Explain: "We provide coaches to schools across Bangalore with training support."
# - Availability: "Are you free 3-6 PM? How many days weekly?"
# - Age groups: "Comfortable with Classes 1-12? Any preferences?"
# - Support: "We offer training. Interested in a structured curriculum?"
# ### Scheduling
# - If interested: "Let’s schedule a detailed discussion. When are you free this week?"
# - Use check_calendar_availability and book_appointment.
# - Confirm: "Please provide your full name, email, and preferred time."
# ### Close
# - Positive: "Thank you, {{name}}. We’ll send details and a confirmation. Looking forward to it!"
# - End with end_call unless transferred
# ## Response Guidelines
# - Handle FAQs before diving into qualification if asked
# - Use IST timing for scheduling (e.g., today is 03:14 PM IST, Friday, September 19, 2025)
# - Ask one question at a time to avoid overwhelming them
# - Keep responses focused on qualifying their suitability for school coaching
# - Ask location-specific questions about Bangalore areas they can cover
# - Show genuine enthusiasm for their chess achievements and experience
# - Be respectful of their current commitments and time constraints
# - Emphasize the opportunity to impact young minds through chess education
# ## Scenario Handling
# ### Interested Leads
# - Enthusiasm: "Your experience is impressive! Let’s connect you with a rep."
# - Route: Use transfer_call to sales rep.
# ### Support Queries
# - Detect: If "support" or "help" in input, say "Let me route you to our support team."
# - Route: Use transfer_call to support.
# ### Reminders
# - Meeting: "This is a reminder for your demo on [date/time]. Ready to proceed?" (e.g., use current date + 1 day if unspecified)
# - Payment: "This is a payment reminder for ₹500 due by [date]. Settled?" (e.g., use current date + 1 day if unspecified)
# ### For Highly Qualified Candidates
# - Express enthusiasm: "Your tournament experience and rating are impressive! Our partner schools would definitely value someone with your background."
# - Fast-track process: "Given your qualifications, I’d love to expedite our discussion. When would be the best time this week?"
# - Highlight premium opportunities: "With your experience, you’d be perfect for our advanced chess program placements at premium schools."
# ### For Candidates with Limited Formal Experience
# - Explore potential: "While formal ratings are helpful, we also value passion and teaching ability. Tell me about your experience with children or young people."
# - Training emphasis: "We provide comprehensive training to develop skills. Are you excited about growing with our support?"
# - Alternative qualifications: "Have you been involved in chess clubs, online coaching, or informal teaching?"
# ### For Availability Concerns
# - Flexible scheduling: "We can often accommodate different preferences. What times work best for you?"
# - Part-time opportunities: "Many coaches start part-time. Would that interest you?"
# - Location matching: "We’ll match you with convenient schools. Which Bangalore areas are accessible?"
# ### For Candidates Requesting Human Assistance
# - If they want human help or details on compensation/partnerships:
#   - Use transfer_call
#   - Say: "Of course! Let me connect you with our placement manager for details on partnerships and compensation."
# ## Knowledge Base
# ### Caller Info
# - name: {{name}}, email: {{email}}, phone_number: {{phone_number}}, role: {{role}}
# ### 4champz Model
# - Leading chess coaching in Bengaluru, school-focused, training provided
# - Partners with reputed schools, offers part-time/full-time opportunities
# - Focuses on developing young chess talent
# ### Requirements
# - 3-6 PM availability, English/Kannada/Hindi, Bangalore travel
# - Professional attitude, teaching aptitude, school-level chess knowledge
# ### Assessment Criteria
# - Chess playing experience and rating (FIDE/All India Chess Federation)
# - Tournament participation and achievements
# - Prior coaching/teaching experience, especially with children
# - Educational qualifications and chess certifications
# - Language capabilities and communication skills
# - Geographic availability across Bangalore
# - Flexibility with scheduling and age groups
# ## Response Refinement
# - When discussing chess background: "Your chess journey sounds fascinating. Could you tell more about [specific aspect]?"
# - When explaining opportunities: "Let me paint a picture of coaching with our partner schools..."
# - When confirming details: "To confirm—you’re available [availability] and comfortable with [preferences]. Is that accurate?"
# ## Call Management
# ### Available Functions
# - check_calendar_availability: Use for scheduling follow-up meetings
# - book_appointment: Use to confirm scheduled appointments
# - transfer_call: Use when candidate requests human assistance
# - end_call: Use to conclude every conversation
# ## Technical Considerations
# - If calendar delays occur: "I’m checking available slots. This will take a moment."
# - If multiple scheduling needs: "Let’s book your appointment first, then address other questions."
# - Always confirm appointment details before ending: "To confirm, we’re scheduled for [day], [date] at [time IST]. You’ll receive an email."
# ---
# Your goal is to qualify chess coaches for Bangalore schools, ensure they understand and are excited about the opportunity, and maintain 4champz’s professional reputation. Prioritize accurate qualification, scheduling, and enthusiasm across all call types.
# """

# # Groq LLM setup
# llm = ChatGroq(model_name="llama-3.1-8b-instant")
# # llm = ChatGroq(model_name="groq/compound-mini")

# # Config Manager
# config_manager = InMemoryConfigManager()

# # ADDED for JSON capture with LLM extraction: global in-memory store
# CONVERSATION_STORE: dict = {}  # ADDED for JSON LLM extraction

# # ADDED for JSON capture with LLM extraction: directory for local persistence
# CONVERSATIONS_DIR = Path("conversations")  # ADDED
# CONVERSATIONS_DIR.mkdir(exist_ok=True, parents=True)  # ADDED

# # ADDED n8n: store lead context by call_sid/conversation_id
# LEAD_CONTEXT_STORE: dict = {}  # ADDED n8n


# # Sentiment Analysis Chain (using Groq LLM)
# sentiment_prompt = PromptTemplate(
#     input_variables=["transcript"],
#     template="Analyze the sentiment of this transcript: {transcript}. Return a JSON with 'sentiment' (positive, neutral, negative, angry, confused) and 'tone_score' (1-10, 10 being most positive)."
# )
# sentiment_chain = LLMChain(llm=llm, prompt=sentiment_prompt)

# # Summary Generation Chain (using Groq LLM)
# summary_prompt = PromptTemplate(
#     input_variables=["transcript"],
#     template="Generate a summary of this transcript: {transcript}. Include key points, customer intent, and next actions. Return a JSON with 'summary', 'intent', 'next_actions' (array of strings)."
# )
# summary_chain = LLMChain(llm=llm, prompt=summary_prompt)



# # Send Email Function
# def send_email(to_email: str, subject: str, body: str):
#     msg = MIMEText(body)
#     msg['Subject'] = subject
#     msg['From'] = EMAIL_SENDER
#     msg['To'] = to_email
#     with smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT) as server:
#         server.starttls()  # Added TLS for security
#         server.login(EMAIL_SENDER, EMAIL_PASSWORD)
#         server.sendmail(EMAIL_SENDER, to_email, msg.as_string())
#     logger.info(f"Email sent to {to_email}")

# # Send WhatsApp Summary Function (using Twilio)
# def send_whatsapp(to_phone: str, body: str):
#     client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#     client.messages.create(
#         from_='whatsapp:' + WHATSAPP_SENDER,
#         body=body,
#         to='whatsapp:' + to_phone
#     )
#     logger.info(f"WhatsApp sent to {to_phone}")



# # NEW: Check Calendar Availability
# async def check_calendar_availability(preferred_time: str) -> dict:
#     headers = {"Authorization": f"Bearer {CRM_API_KEY}"}
#     params = {"time": preferred_time, "timezone": "Asia/Kolkata"}
#     async with httpx.AsyncClient() as client:
#         response = await client.get(CALENDAR_API_URL, headers=headers, params=params)
#         if response.status_code == 200:
#             return response.json()
#         logger.error(f"Calendar check failed: {response.text}")
#         return {"available": False, "slots": []}
    


# # NEW: Book Appointment
# async def book_appointment(lead_id: str, name: str, email: str, time: str):
#     payload = {
#         "lead_id": lead_id,
#         "name": name,
#         "email": email,
#         "time": time,
#         "status": "Scheduled"
#     }
#     headers = {"Authorization": f"Bearer {CRM_API_KEY}"}
#     async with httpx.AsyncClient() as client:
#         response = await client.post(f"{CRM_API_URL}/appointments", json=payload, headers=headers)
#         if response.status_code == 200:
#             logger.info(f"Appointment booked for lead {lead_id}")
#             return True
#         logger.error(f"Appointment booking failed: {response.text}")
#         return False


# # NEW: Update CRM Function (placeholder; replace with your CRM API)
# def update_crm(lead_id: str, transcript: str, sentiment: dict, summary: dict, audio_url: str, twilio_audio_url: Optional[str] = None, status: str = "Called", appointment: dict = None):
#     payload = {
#         "lead_id": lead_id,
#         "transcript": transcript,
#         "sentiment": sentiment,
#         "summary": summary,
#         "audio_url": audio_url,
#         "twilio_audio_url": twilio_audio_url,  # NEW: Twilio full call recording
#         "status": status,
#         "appointment": appointment
#     }
#     headers = {"Authorization": f"Bearer {CRM_API_KEY}"}
#     response = requests.post(CRM_API_URL, json=payload, headers=headers)
#     if response.status_code == 200:
#         logger.info(f"CRM updated for lead {lead_id}")
#     else:
#         logger.error(f"CRM update failed: {response.text}")



# # Events Manager to log transcripts
# class ChessEventsManager(events_manager.EventsManager):
#     def __init__(self):
#         super().__init__(subscriptions=[EventType.TRANSCRIPT_COMPLETE])

#     async def handle_event(self, event: Event):
#         if event.type == EventType.TRANSCRIPT_COMPLETE:
#             transcript_complete_event = typing.cast(TranscriptCompleteEvent, event)
#             transcript = transcript_complete_event.transcript.to_string()
#             logger.debug(f"Transcript for conversation {transcript_complete_event.conversation_id}: {transcript}")

#             # NEW: Sentiment analysis
#             sentiment = await sentiment_chain.ainvoke({"transcript": transcript})

#             # NEW: Summary generation
#             summary = await summary_chain.ainvoke({"transcript": transcript})

#             # NEW: Recording storage (using Deepgram audio chunks)
#             audio_path = await save_recording(transcript_complete_event.conversation_id)
#             audio_url = f"{CLOUD_STORAGE_URL}/{os.path.basename(audio_path)}" if CLOUD_STORAGE_URL else audio_path

#             # NEW: Fetch Twilio recording URL if available
#             client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#             recordings = await asyncio.get_event_loop().run_in_executor(
#                 None,
#                 lambda: client.recordings.list(call_sid=transcript_complete_event.conversation_id)
#             )
#             twilio_audio_url = recordings[0].uri if recordings else None  # NEW: Get Twilio recording URL

#             await asyncio.get_event_loop().run_in_executor(
#                 None, 
#                 lambda: update_crm(transcript_complete_event.conversation_id, transcript, sentiment, summary, audio_url, twilio_audio_url=twilio_audio_url)  # Fixed to use audio_url
#             )

#             # NEW: Send summary to customer/management
#             # Assume email and phone from lead context or CRM
#             short_summary = f"Call Summary: {summary['summary'][:100]}... Next steps: {', '.join(summary['next_actions'][:2])}"
#             lead = LEAD_CONTEXT_STORE.get(transcript_complete_event.conversation_id, {})
#             if "email" in lead:
#                 send_email(lead["email"], "Call Summary", short_summary)
#             if "to_phone" in lead:
#                 send_whatsapp(lead["to_phone"], short_summary)

#             webhook_url = os.getenv("TRANSCRIPT_CALLBACK_URL")
#             if webhook_url:
#                 data = {"conversation_id": transcript_complete_event.conversation_id, "user_id": 1, "transcript": transcript}
#                 async with httpx.AsyncClient() as client:
#                     response = await client.post(webhook_url, json=data)
#                     if response.status_code == 200:
#                         logger.info("Transcript sent successfully to webhook")
#                     else:
#                         logger.error(f"Failed to send transcript to webhook: {response.status_code}")
#             # ADDED for JSON capture with LLM extraction: write store JSON to disk
#             try:
#                 convo = CONVERSATION_STORE.get(transcript_complete_event.conversation_id)
#                 if convo:
#                     convo["sentiment"] = sentiment  # NEW
#                     convo["summary"] = summary  # NEW
#                     out_path = CONVERSATIONS_DIR / f"{transcript_complete_event.conversation_id}.json"
#                     with open(out_path, "w", encoding="utf-8") as f:
#                         json.dump(convo, f, ensure_ascii=False, indent=2)
#                     logger.info(f"Wrote JSON summary to {out_path}")
#             except Exception as e:
#                 logger.error(f"Failed to write JSON summary: {e}")


# async def save_recording(conversation_id: str) -> str:
#     # Assume transcriber instance is accessible via a global or passed reference
#     transcriber = None  # Placeholder; should be injected or managed by TelephonyServer
#     if transcriber and hasattr(transcriber, 'audio_buffer') and transcriber.conversation_id == conversation_id:
#         await transcriber._save_audio()
#         audio_path = RECORDINGS_DIR / f"{conversation_id}.wav"
#         return str(audio_path)
#     logger.error(f"No valid transcriber or buffer for conversation {conversation_id}")
#     return ""

# # Custom Agent Config
# class CustomLangchainAgentConfig(LangchainAgentConfig, type="agent_langchain"):
#     initial_message: BaseMessage = BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?")
#     prompt_preamble: str = CHESS_COACH_PROMPT_PREAMBLE
#     model_name: str = "llama-3.1-8b-instant"
#     # model_name: str = "groq/compound-mini"
#     api_key: str = GROQ_API_KEY
#     provider: str = "groq"

# # Custom Langchain Agent
# class CustomLangchainAgent(LangchainAgent):
#     def __init__(self, agent_config: CustomLangchainAgentConfig):
#         logger.debug(f"Initializing CustomLangchainAgent with config: {agent_config}")
#         super().__init__(agent_config=agent_config)
#         self.last_response_time = time.time()
#         self.conversation_state = "initial"
#         self.no_input_count = 0
#         self.user_name = None  # store extracted/confirmed name
#         self.asked_for_name = False  # track if name is requested
#         logger.debug("Initialized CustomLangchainAgent with Groq LLM (llama-3.1-8b-instant)")
#         # ADDED for JSON capture with LLM extraction
#         self.turns = []  # [{"speaker":"user"/"bot","text":..., "ts": epoch_ms}]
#         self.conversation_id_cache = None  # to index the global store
#         self.extracted_slots = {}  # LLM-extracted structured data


#     # ADDED n8n: helper to ensure id
#     def _ensure_conv_id(self, conversation_id: Optional[str]) -> str:
#         if conversation_id and isinstance(conversation_id, str) and conversation_id.strip():
#             return conversation_id
#         return f"unknown_{int(time.time()*1000)}"

#     # ADDED for JSON capture with LLM extraction
#     def _flush_to_disk(self, conversation_id: str):
#         """Write the current conversation JSON to disk immediately."""
#         try:
#             payload = CONVERSATION_STORE.get(conversation_id)
#             if not payload:
#                 return
#             out_path = CONVERSATIONS_DIR / f"{conversation_id}.json"
#             with open(out_path, "w", encoding="utf-8") as f:
#                 json.dump(payload, f, ensure_ascii=False, indent=2)
#             logger.debug(f"Flushed conversation {conversation_id} to {out_path}")
#         except Exception as e:
#             logger.error(f"Flush to disk failed for {conversation_id}: {e}")

#     # ADDED for JSON capture with LLM extraction
#     def _persist_state(self, conversation_id: Optional[str]):
#         conv_id = self._ensure_conv_id(conversation_id)
#         now_ms = int(time.time() * 1000)
#         lead = LEAD_CONTEXT_STORE.get(conv_id, {})  # ADDED n8n
#         payload = {
#             "conversation_id": conv_id,
#             "updated_at": now_ms,
#             "lead": lead,  # ADDED n8n
#             "slots": self.extracted_slots,  # slots are LLM-extracted
#             "turns": self.turns
#         }
#         CONVERSATION_STORE[conv_id] = payload
#         self._flush_to_disk(conv_id)  # ADDED: always flush on persist

#     # ADDED for JSON capture with LLM extraction
#     def _strip_code_fences(self, s: str) -> str:
#         t = (s or "").strip()
#         if t.startswith("```"):
#             end = t.rfind("```")
#             if end > 0:
#                 inner = t[3:end].strip()
#                 if inner.lower().startswith("json"):
#                     inner = inner[4:].strip()
#                 return inner
#         return t

#     # ADDED for JSON capture with LLM extraction
#     async def _extract_slots_with_llm(self, conversation_id: str):
#         """Extract slots with retry logic."""
#         max_retries = 3
#         retry_delay = 2  # seconds

#         for attempt in range(max_retries):
#             try:
#                 # Build a compact transcript string
#                 convo_lines = []
#                 for t in self.turns[-30:]:
#                     role = "User" if t["speaker"] == "user" else "Agent"
#                     text_line = re.sub(r'\s+', ' ', t['text']).strip()
#                     convo_lines.append(f"{role}: {text_line}")
#                 convo_text = "\n".join(convo_lines)

#                 # Instruction for JSON-only schema
#                 schema_instruction = (
#                     "Return ONLY a JSON object with these keys:\n"
#                     "{\n"
#                     '  "location": string|null,\n'
#                     '  "involvement": "playing"|"coaching"|null,\n'
#                     '  "availability": string|null,\n'
#                     '  "age_range": string|null,\n'
#                     '  "languages": string[]|null,\n'
#                     '  "rating": string|null,\n'
#                     '  "tournaments": string|null,\n'
#                     '  "certifications": string|null,\n'
#                     '  "questions": string[]|null,\n'
#                     '  "intent": "interested"|"support"|"reminder"|null\n'
#                     '}\n'
#                     "Infer conservatively. Use null if not explicitly known."
#                 )

#                 prompt = f"{schema_instruction}\n\nConversation:\n{convo_text}\n\nJSON:"

#                 extractor = ChatGroq(model_name="llama-3.1-8b-instant")
#                 resp = await extractor.ainvoke([
#                     {"role": "system", "content": "You extract structured information from conversations."},
#                     {"role": "user", "content": prompt}
#                 ])

#                 # Normalize content
#                 content = None
#                 if hasattr(resp, "content"):
#                     content = resp.content
#                 elif hasattr(resp, "generations"):
#                     try:
#                         content = resp.generations.text
#                     except Exception:
#                         content = str(resp)
#                 else:
#                     content = str(resp)

#                 parsed = None
#                 try:
#                     c = self._strip_code_fences(content)
#                     parsed = json.loads(c)
#                 except Exception:
#                     logger.warning("Primary JSON parse failed; attempting to locate JSON object")
#                     first = content.find("{")
#                     last = content.rfind("}")
#                     if first != -1 and last != -1 and last > first:
#                         snippet = content[first:last+1]
#                         try:
#                             parsed = json.loads(snippet)
#                         except Exception:
#                             parsed = None

#                 if isinstance(parsed, dict):
#                     # normalize keys
#                     for k in ["location","involvement","availability","age_range","languages","rating","tournaments","certifications","questions"]:
#                         if k not in parsed:
#                             parsed[k] = None
#                     # Ensure types
#                     if parsed.get("languages") is not None and not isinstance(parsed["languages"], list):
#                         parsed["languages"] = [str(parsed["languages"])]
#                     if parsed.get("questions") is not None and not isinstance(parsed["questions"], list):
#                         parsed["questions"] = [str(parsed["questions"])]

#                     self.extracted_slots = parsed
#                     self._persist_state(conversation_id)
#                 else:
#                     logger.warning("LLM extraction did not return a dict; keeping previous slots.")
#                     if attempt < max_retries - 1:
#                         await asyncio.sleep(retry_delay)
#                         continue
#                     raise ValueError("Failed to parse valid JSON after retries")

#             except Exception as e:
#                 logger.error(f"Slot extraction failed (attempt {attempt + 1}/{max_retries}): {e}")
#                 if attempt < max_retries - 1:
#                     await asyncio.sleep(retry_delay)
#                     continue
#                 raise  # Re-raise after final attempt

#     async def end_call(self, conversation_id: str):
#         """End the call by returning a TwiML Hangup response."""
#         twiml_response = '<?xml version="1.0" encoding="UTF-8"?><Response><Hangup/></Response>'
#         await self.send_message(BaseMessage(text=twiml_response), conversation_id)  # Use existing send_message to pass TwiML
#         logger.info(f"Call ended for conversation_id: {conversation_id}")

#     async def respond(self, human_input: str, conversation_id: str, is_interrupt: bool = False) -> Tuple[Optional[str], bool]:
#         try:
#             start_time = time.time()

#             if conversation_id and self.conversation_id_cache != conversation_id:
#                 self.conversation_id_cache = conversation_id
#             current_id = self.conversation_id_cache or conversation_id or "unknown"

#             if human_input:
#                 self.turns.append({"speaker": "user", "text": human_input, "ts": int(time.time()*1000)})
#                 if len(self.turns) % 2 == 0:
#                     asyncio.create_task(self._extract_slots_with_llm(current_id))
#                 self._persist_state(current_id)

#             def personalize_response(text: str) -> str:
#                 if self.user_name:
#                     return text.replace("{name}", self.user_name)
#                 external_name = "there"
#                 return text.replace("{name}", external_name)

#             if time.time() - self.last_response_time > 15:
#                 self.no_input_count += 1
#                 logger.warning(f"No transcription for 15s (attempt {self.no_input_count})")
#                 if self.no_input_count >= 3:
#                     bot_text = personalize_response("Trouble connecting. I’ll follow up later. Thank you!")
#                     self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                     self._persist_state(current_id)
#                     await self.end_call(conversation_id)  # New: End the call
#                     return bot_text, True
#                 bot_text = personalize_response("I didn’t catch that. Available to discuss chess coaching?")
#                 self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return bot_text, False

#             normalized = (human_input or "").strip().lower()
#             filler_phrases = {"", "mhmm", "okay", "what", "yes", "no", "a-", "four", "hello", "hi"}
#             if normalized in filler_phrases:
#                 self.no_input_count += 1
#                 logger.debug(f"Filler input (count {self.no_input_count}): '{human_input}'")
#                 if self.no_input_count >= 3:
#                     bot_text = personalize_response("No valid input. I’ll follow up later. Thank you!")
#                     self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                     self._persist_state(current_id)
#                     return bot_text, True
#                 self.last_response_time = start_time
#                 bot_text = personalize_response("Didn’t catch that. Confirm availability?")
#                 self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return bot_text, False

#             gibberish_indicators = ["what is the first time", "first time", "please repeat", "say again"]
#             if any(phrase in normalized for phrase in gibberish_indicators):
#                 self.no_input_count += 1
#                 logger.debug(f"Gibberish input (count {self.no_input_count}): '{human_input}'")
#                 if self.no_input_count >= 3:
#                     bot_text = personalize_response("Trouble connecting. I’ll follow up later. Thank you!")
#                     self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                     self._persist_state(current_id)
#                     return bot_text, True
#                 self.last_response_time = start_time
#                 bot_text = personalize_response("Sorry, repeat or say yes/no if available?")
#                 self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return bot_text, False

#             self.no_input_count = 0

#             if self.asked_for_name and "name is" in normalized:
#                 try:
#                     name_part = human_input.lower().split("name is", 1)[1].strip().split()
#                     self.user_name = name_part[0].capitalize()
#                     logger.debug(f"Extracted user name: {self.user_name}")
#                 except Exception:
#                     self.user_name = None

#             slots = self.extracted_slots
#             intent = slots.get("intent")

#             # FAQ handling
#             if any(q in normalized for q in ["price", "pricing", "cost", "timings", "time", "services"]):
#                 if "price" in normalized or "cost" in normalized:
#                     response = "Our fees start at ₹500/hour, varying by experience. Want more details?"
#                 elif "timings" in normalized or "time" in normalized:
#                     response = "Coaching is 3-6 PM school hours. Flexible options available—discuss?"
#                 elif "services" in normalized:
#                     response = "We offer curricula, training, and school placements. More questions?"
#                 self.last_response_time = start_time
#                 self.turns.append({"speaker": "bot", "text": response, "ts": int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return response, False

#             # NEW: Real-time sentiment-based routing
#             sentiment = await sentiment_chain.ainvoke({"transcript": "\n".join(t["text"] for t in self.turns)})
#             if sentiment["sentiment"] == "angry" or "upset" in normalized:
#                 logger.info("Detected angry tone, routing to calm rep")
#                 bot_text = "I’ll connect you with a calm rep to assist you."
#                 self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return bot_text, True

#             if self.conversation_state == "initial":
#                 if any(word in normalized for word in ["yes", "sure", "okay", "available"]):
#                     self.conversation_state = "background"
#                     response = "Great! Due to your interest, confirm your Bangalore location?"
#                 else:
#                     response = personalize_response("Sorry, misheard. Available to discuss coaching?")
#                 self.last_response_time = start_time
#                 self.turns.append({"speaker": "bot", "text": response, "ts": int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return response, False
#             else:
#                 try:
#                     response, should_end = await asyncio.wait_for(
#                         super().respond(human_input, conversation_id, is_interrupt), timeout=5.0
#                     )
#                 except asyncio.TimeoutError:
#                     fallback_msg = personalize_response("Response delayed. Try again shortly.")
#                     self.turns.append({"speaker": "bot", "text": fallback_msg, "ts": int(time.time()*1000)})
#                     self._persist_state(current_id)
#                     await self.end_call(conversation_id)  # New: End call on timeout
#                     return fallback_msg, True

#                 if response:
#                     response_text = personalize_response(response)
#                     if "location" in response_text.lower():
#                         self.conversation_state = "background"
#                     if any(phrase in response_text.lower() for phrase in ["confirm your full name", "may i have your name"]):
#                         self.asked_for_name = True

#                     if intent == "interested" and "schedule" in response_text.lower():
#                         available_slots = await check_calendar_availability(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
#                         if available_slots["available"]:
#                             bot_text = f"Great! Available slots: {', '.join(available_slots['slots'])}. Provide name, email, and preferred time?"
#                             self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                             self._persist_state(current_id)
#                             return bot_text, False
#                         else:
#                             bot_text = "No slots available now. I’ll follow up. Thank you!"
#                             self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                             self._persist_state(current_id)
#                             await self.end_call(conversation_id)  # New: End the call
#                             return bot_text, True

#                     if intent == "support":
#                         bot_text = "Let me route you to our support team."
#                         self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                         self._persist_state(current_id)
#                         return bot_text, True
#                     elif intent == "interested":
#                         bot_text = "Impressive! Connecting you to a sales rep."
#                         self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                         self._persist_state(current_id)
#                         await self.end_call(conversation_id)  # New: End call after routing
#                         return bot_text, True

#                     self.last_response_time = start_time
#                     self.turns.append({"speaker": "bot", "text": response_text, "ts": int(time.time()*1000)})
#                     if len(self.turns) % 4 == 0:
#                         asyncio.create_task(self._extract_slots_with_llm(current_id))
#                     self._persist_state(current_id)
#                     return response_text, should_end

#                 fallback_msg = personalize_response("Didn’t get that. Tell me more?")
#                 self.last_response_time = start_time
#                 self.turns.append({"speaker": "bot", "text": fallback_msg, "ts": int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return fallback_msg, False

#         except Exception as e:
#             logger.error(f"Error generating response: {str(e)}")
#             fallback_error_msg = "Error occurred. Try again."
#             self.turns.append({"speaker": "bot", "text": fallback_error_msg, "ts": int(time.time()*1000)})
#             current_id = self.conversation_id_cache or conversation_id or "unknown"
#             self._persist_state(current_id)
#             return fallback_error_msg, False
    








# # Custom Deepgram Transcriber with keepalive and chunk logging
# class CustomDeepgramTranscriber(DeepgramTranscriber):
#     def __init__(self, transcriber_config: DeepgramTranscriberConfig):
#         super().__init__(transcriber_config)
#         self.audio_buffer = io.BytesIO()
#         self.conversation_id = None

#     async def process(self, audio_chunk: bytes):
#         logger.debug(f"Processing audio chunk size: {len(audio_chunk)} bytes")
#         if not audio_chunk or len(audio_chunk) == 0:
#             logger.warning("Empty audio chunk - skipping")
#             return None
#         try:
#             async with self.buffer_lock:
#                 if self.conversation_id:
#                     total_size = self.audio_buffer.tell() + len(audio_chunk)
#                     if total_size > 10 * 1024 * 1024:  # 10MB limit
#                         await self._save_audio()
#                     self.audio_buffer.write(audio_chunk)
#             return await super().process(audio_chunk)
#         except Exception as e:
#             logger.error(f"Deepgram process error: {e}")
#             raise
    

#     async def keepalive(self):
#         while True:
#             await asyncio.sleep(10)
#             try:
#                 await super().process(b"\x00" * 160)
#                 logger.debug("Deepgram keepalive sent")
#             except Exception as e:
#                 logger.error(f"Keepalive failed: {e}")
#                 break


#     def set_conversation_id(self, conversation_id: str):
#         if self.conversation_id != conversation_id:
#             if self.audio_buffer.tell() > 0:
#                 asyncio.create_task(self._save_audio())
#             self.conversation_id = conversation_id
#             self.audio_buffer = io.BytesIO()

#     async def _save_audio(self):
#         if self.conversation_id and self.audio_buffer.tell() > 0:
#             self.audio_buffer.seek(0)
#             audio_path = RECORDINGS_DIR / f"{self.conversation_id}.wav"
#             with open(audio_path, 'wb') as f:
#                 f.write(self.audio_buffer.getbuffer())
#             logger.info(f"Saved audio to {audio_path}")
#             self.audio_buffer = io.BytesIO()

# # Custom Agent Factory
# class CustomAgentFactory:
#     def create_agent(self, agent_config: AgentConfig, logger: Optional[logging.Logger] = None) -> BaseAgent:
#         log = logger or globals().get('logger', logging.getLogger(__name__))
#         log.debug(f"Creating agent with config type: {agent_config.type}")
#         if agent_config.type == "agent_langchain":
#             log.debug("Creating CustomLangchainAgent")
#             return CustomLangchainAgent(agent_config=typing.cast(CustomLangchainAgentConfig, agent_config))
#         log.error(f"Invalid agent config type: {agent_config.type}")
#         raise Exception(f"Invalid agent config: {agent_config.type}")

# # Custom Synthesizer Factory
# class CustomSynthesizerFactory:
#     def create_synthesizer(self, synthesizer_config: SynthesizerConfig) -> BaseSynthesizer:
#         logger.debug(f"Creating synthesizer with config: {synthesizer_config}")
#         if isinstance(synthesizer_config, StreamElementsSynthesizerConfig):
#             logger.debug("Creating StreamElementsSynthesizer")
#             return StreamElementsSynthesizer(synthesizer_config)
#         logger.error(f"Invalid synthesizer config type: {synthesizer_config.type}")
#         raise Exception(f"Invalid synthesizer config: {synthesizer_config.type}")

# # FastAPI App
# app = FastAPI()

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     logger.debug("Starting up FastAPI application")
#     logger.debug("Registered routes:")
#     for route in app.routes:
#         methods = getattr(route, "methods", ["WebSocket"])
#         logger.debug(f" - {route.path} ({methods})")
#     yield
#     # ADDED: final sweep to persist any in-memory conversations at shutdown
#     try:
#         for conv_id in list(CONVERSATION_STORE.keys()):
#             out_path = CONVERSATIONS_DIR / f"{conv_id}.json"
#             with open(out_path, "w", encoding="utf-8") as f:
#                 json.dump(CONVERSATION_STORE[conv_id], f, ensure_ascii=False, indent=2)
#         logger.debug("Shutdown flush completed for all conversations")
#     except Exception as e:
#         logger.error(f"Error during shutdown flush: {e}")
#     logger.debug("Shutting down FastAPI application")

# app.router.lifespan_context = lifespan

# # Twilio config
# twilio_config = TwilioConfig(
#     account_sid=TWILIO_ACCOUNT_SID,
#     auth_token=TWILIO_AUTH_TOKEN
# )

# # Synthesizer config (telephone voice output)
# synthesizer_config = StreamElementsSynthesizerConfig.from_telephone_output_device(
#     voice="Brian"
# )

# transcriber_config = DeepgramTranscriberConfig(
#     api_key=DEEPGRAM_API_KEY,
#     model="nova-2-phonecall",
#     language="en",
#     sampling_rate=8000,  # int primitive, not enum
#     audio_encoding="mulaw",  # lowercase string, not enum
#     chunk_size=320,
#     endpointing_config=PunctuationEndpointingConfig(),
#     downsampling=1,
# )

# agent_config = LangchainAgentConfig(
#     initial_message=BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"),
#     prompt_preamble=CHESS_COACH_PROMPT_PREAMBLE,
#     model_name="llama-3.1-8b-instant",
#     # model_name="groq/compound-mini",
#     api_key=GROQ_API_KEY,
#     provider="groq",
# )



# # Telephony Server setup
# telephony_server = TelephonyServer(
#     base_url=BASE_URL,  # your ngrok url
#     config_manager=config_manager,
#     inbound_call_configs=[
#         TwilioInboundCallConfig(
#             url="/inbound_call",
#             twilio_config=twilio_config,
#             agent_config=agent_config,
#             synthesizer_config=synthesizer_config,
#             transcriber_config=transcriber_config,  # Use instance
#             twiml_fallback_response='''<?xml version="1.0" encoding="UTF-8"?>
# <Response>
#     <Say>I didn't hear a response. Are you still there? Please say something to continue.</Say>
#     <Pause length="15"/>
#     <Redirect method="POST">/inbound_call</Redirect>
# </Response>''',
#             record=True
#         )
#     ],
#     agent_factory=CustomAgentFactory(),
#     synthesizer_factory=CustomSynthesizerFactory(),
#     events_manager=ChessEventsManager(),
# )

# # Add routes to FastAPI app
# app.include_router(telephony_server.get_router())


# # ADDED n8n: request schema for outbound_call
# class OutboundCallRequest(BaseModel):
#     to_phone: str
#     lead: typing.Optional[typing.Dict[str, typing.Any]] = None
#     transcript_callback_url: typing.Optional[str] = None
#     call_type: str = "qualification"  # NEW: qualification, reminder, payment

# # ADDED n8n: normalize to E164 basic
# def normalize_e164(number: str) -> str:
#     n = re.sub(r'\D+', '', number or '')
#     if not n:
#         return number
#     if n.startswith('0'):
#         n = n.lstrip('0')
#     if not n.startswith('+'):
#         if len(n) == 10:
#             n = '+91' + n
#         else:
#             n = '+' + n
#     return n

# # ADDED n8n: HTTP endpoint to start outbound call from n8n
# @app.post("/outbound_call")
# async def outbound_call(req: OutboundCallRequest):
#     try:
#         to_phone = normalize_e164(req.to_phone)
#         if not to_phone or len(to_phone) < 10:
#             raise HTTPException(status_code=400, detail="Invalid phone")
#         sid = await make_outbound_call(to_phone, req.call_type, req.lead)
#         lead = req.lead or {}
#         lead["to_phone"] = to_phone
#         LEAD_CONTEXT_STORE[sid] = lead
#         logger.info(f"Outbound call requested via n8n: SID={sid}, lead={lead}")
#         if req.transcript_callback_url:
#             os.environ["TRANSCRIPT_CALLBACK_URL"] = req.transcript_callback_url
#         return {"ok": True, "call_sid": sid}
#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"/outbound_call failed: {e}")
#         raise HTTPException(status_code=500, detail=str(e))


# # Outbound call helper
# async def make_outbound_call(to_phone: str, call_type: str, lead: dict = None):
#     client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#     twilio_base_url = f"https://{BASE_URL}"
#     initial_message = {
#         "qualification": "Hello, this is Priya from 4champz. Available to discuss chess coaching?",
#         "reminder": f"This is a reminder for your demo on {lead.get('demo_date', time.strftime('%Y-%m-%d %H:%M IST', time.localtime(time.time() + 86400)))}. Ready?",
#         "payment": f"Payment reminder for ₹500 due by {lead.get('due_date', time.strftime('%Y-%m-%d', time.localtime(time.time() + 86400)))}. Settled?"
#     }.get(call_type, "Hello, this is Priya from 4champz. How can I assist?")
#     call = await asyncio.get_event_loop().run_in_executor(
#         None,
#         lambda: client.calls.create(
#             to=to_phone,
#             from_=TWILIO_PHONE_NUMBER,
#             url=f"{twilio_base_url}/inbound_call",
#             status_callback=f"{twilio_base_url}/call_status",
#             status_callback_method="POST",
#             status_callback_event=["initiated", "ringing", "answered", "completed"],
#             record=True,
#             recording_channels="dual",
            
#         )
#     )
#     logger.info(f"Call initiated: SID={call.sid}, type={call_type}")
#     if call.sid not in LEAD_CONTEXT_STORE:
#         LEAD_CONTEXT_STORE[call.sid] = {"to_phone": to_phone, "call_type": call_type, **(lead or {})}
#     CONVERSATION_STORE.setdefault(call.sid, {
#         "conversation_id": call.sid,
#         "updated_at": int(time.time()*1000),
#         "lead": LEAD_CONTEXT_STORE.get(call.sid, {}),
#         "slots": {},
#         "turns": [{"speaker": "bot", "text": initial_message, "ts": int(time.time()*1000)}]
#     })
#     return call.sid




# # NEW: Outbound Call Scheduler (for auto-dialing from CRM)
# def outbound_scheduler():
#     while True:
#         response = requests.get(CRM_API_URL, headers={"Authorization": f"Bearer {CRM_API_KEY}"})
#         if response.status_code == 200:
#             leads = response.json().get("leads", [])  # Adjusted to 'leads' for generality
#             for lead in leads:
#                 if lead.get("status") == "Call Pending":
#                     call_type = lead.get("call_type", "qualification")
#                     asyncio.run(make_outbound_call(lead["phone"], call_type, lead))
#                     update_crm(lead["id"], "", {}, {}, "", status="Calling")
#         time.sleep(300)  # Poll every 5 minutes


# # # Main entrypoint
# # if __name__ == "__main__":
# #     import uvicorn

# #     def run_server():
# #         logger.debug("Starting Uvicorn server")
# #         uvicorn.run(app, host="0.0.0.0", port=3000)

# #     # async def start_server_and_call():
# #     #     try:
# #     #         server_thread = threading.Thread(target=run_server, daemon=True)
# #     #         server_thread.start()
# #     #         await asyncio.sleep(2)
# #     #         await make_outbound_call("+917356793165")  # your target phone number
# #     #         await asyncio.Event().wait()
# #     #     except Exception as e:
# #     #         logger.error(f"Error in start_server_and_call: {str(e)}")
# #     #         raise

# #     # asyncio.run(start_server_and_call())


# #     run_server() 



# # Main entrypoint (updated to include scheduler)
# if __name__ == "__main__":
#     import uvicorn

#     def run_server():
#         logger.debug("Starting Uvicorn server")
#         uvicorn.run(app, host="0.0.0.0", port=3000)

#     # Start outbound scheduler in a thread
#     scheduler_thread = threading.Thread(target=outbound_scheduler, daemon=True)
#     scheduler_thread.start()

#     run_server()

# # # NEW: Update CRM function (placeholder)
# # def update_crm(lead_id: staryr, transcript: str, sentiment: dict, summary: dict, audio_url: str, status: str = "Called", appointment: dict = None):
# #     payload = {
# #         "lead_id": lead_id,
# #         "transcript": transcript,
# #         "sentiment": sentiment,
# #         "summary": summary,
# #         "audio_url": audio_url,
# #         "status": status,
# #         "appointment": appointment
# #     }
# #     headers = {"Authorization": f"Bearer {CRM_API_KEY}"}
# #     response = requests.post(CRM_API_URL, json=payload, headers=headers)
# #     if response.status_code == 200:
# #         logger.info(f"CRM updated for lead {lead_id}")
# #     else:
# #         logger.error(f"CRM update failed: {response.text}")



















# import os
# import logging
# import asyncio
# import httpx
# import typing
# import time
# from typing import Optional, Tuple
# from fastapi import FastAPI, Request, Response
# from fastapi.logger import logger as fastapi_logger
# from contextlib import asynccontextmanager
# from dotenv import load_dotenv
# from twilio.rest import Client
# from vocode.streaming.telephony.server.base import TelephonyServer, TwilioInboundCallConfig
# from vocode.streaming.models.telephony import TwilioConfig
# from vocode.streaming.models.agent import LangchainAgentConfig, AgentConfig
# from vocode.streaming.agent.langchain_agent import LangchainAgent
# from vocode.streaming.models.message import BaseMessage
# from vocode.streaming.transcriber.deepgram_transcriber import DeepgramTranscriber
# from vocode.streaming.models.transcriber import DeepgramTranscriberConfig, AudioEncoding, PunctuationEndpointingConfig
# from vocode.streaming.synthesizer.stream_elements_synthesizer import StreamElementsSynthesizer
# from vocode.streaming.models.synthesizer import StreamElementsSynthesizerConfig, SynthesizerConfig
# from vocode.streaming.synthesizer.base_synthesizer import BaseSynthesizer
# from vocode.streaming.telephony.config_manager.in_memory_config_manager import InMemoryConfigManager
# from vocode.streaming.agent.base_agent import BaseAgent
# from vocode.streaming.models.events import Event, EventType
# from vocode.streaming.models.transcript import TranscriptCompleteEvent
# from vocode.streaming.utils import events_manager
# from langchain_groq import ChatGroq
# import threading
# import numpy as np

# # ADDED for JSON capture with LLM extraction
# import json  # ADDED for JSON capture with LLM extraction
# import re    # ADDED: general regex utilities
# from pathlib import Path  # ADDED: filesystem-safe paths
# from fastapi import HTTPException  # ADDED n8n
# from pydantic import BaseModel  # ADDED n8n

# # NEW: For sentiment analysis and summaries (using Groq LLM)
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain


# # NEW: For email summaries (simple SMTP)
# import smtplib
# from email.mime.text import MIMEText

# # NEW: For WhatsApp summaries (using Twilio)
# from twilio.rest import Client as TwilioClient

# # NEW: Placeholder CRM API (replace with your CRM, e.g., HubSpot API)
# import requests  # NEW: for CRM API calls


# from pydub import AudioSegment  # NEW: For audio conversion (MP3/WAV)
# import wave  # NEW: For WAV file handling
# import io

# # Configure logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# fastapi_logger.setLevel(logging.DEBUG)

# # Ensure ffmpeg is in PATH
# os.environ['PATH'] += os.pathsep + 'C:\\ffmpeg\\bin'

# load_dotenv()

# # Environment variables
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
# TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
# TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
# BASE_URL = os.getenv("BASE_URL")
# DEBUG_AUDIO = os.getenv("DEBUG_AUDIO", "false").lower() == "true"


# # NEW: Storage directory for recordings
# RECORDINGS_DIR = Path("recordings")
# RECORDINGS_DIR.mkdir(exist_ok=True, parents=True)

# # NEW: Cloud storage URL (e.g., AWS S3 placeholder)
# CLOUD_STORAGE_URL = os.getenv("CLOUD_STORAGE_URL", "https://your-s3-bucket.s3.amazonaws.com/")


# # NEW: CRM environment variables (replace with your CRM details)
# CRM_API_URL = os.getenv("CRM_API_URL", "https://your-crm-api.com/leads")
# CRM_API_KEY = os.getenv("CRM_API_KEY", "your_crm_api_key")
# EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER", "smtp.example.com")
# EMAIL_SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", 587))
# EMAIL_SENDER = os.getenv("EMAIL_SENDER", "priya@4champz.com")
# EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your_email_password")
# CALENDAR_API_URL = os.getenv("CALENDAR_API_URL", "https://your-calendar-api.com/availability")  # NEW: for scheduling

# # NEW: WhatsApp sender number (for summaries)
# WHATSAPP_SENDER = os.getenv("WHATSAPP_SENDER", TWILIO_PHONE_NUMBER)



# # Validate environment variables
# required_vars = [GROQ_API_KEY, DEEPGRAM_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, BASE_URL, CRM_API_URL, CRM_API_KEY, EMAIL_SMTP_SERVER, EMAIL_SENDER, EMAIL_PASSWORD, CALENDAR_API_URL]
# if not all(required_vars):
#     raise ValueError("Missing required environment variables in .env file. Required: GROQ_API_KEY, DEEPGRAM_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, BASE_URL")

# # Validate Ngrok URL
# if not BASE_URL.endswith((".ngrok-free.app", ".ngrok.io")):
#     logger.warning(f"BASE_URL ({BASE_URL}) does not appear to be a valid Ngrok URL. Ensure it matches the current Ngrok session and is updated in Twilio Console.")

# CHESS_COACH_PROMPT_PREAMBLE = """
# # Chess Coaching Sales Representative Prompt
# ## Identity & Purpose
# You are Priya, a virtual sales representative for 4champz, a leading chess coaching service provider based in Bengaluru, India. We specialize in providing qualified chess coaches to schools across Bangalore. 
# Your primary purpose is to qualify leads who have shown interest in chess coaching opportunities, understand their background and experience, explore potential collaboration as a chess coach for our school programs, handle FAQs, and schedule meetings for both inbound and outbound calls.
# ## Voice & Persona
# ### Personality
# - Sound professional, warm, and conversational—like a knowledgeable chess enthusiast
# - Project genuine interest in learning about their chess journey
# - Maintain an engaging and respectful demeanor throughout the conversation
# - Show respect for their time while staying focused on understanding their suitability for school coaching
# - Convey enthusiasm about the opportunity to shape young minds through chess
# ### Speech Characteristics
# - Use clear, conversational language with natural flow
# - Keep messages under 150 characters when possible
# - Include probing questions to gather detailed information
# - Show genuine interest in their chess background and achievements
# - Use encouraging language when discussing their experience and qualifications
# ## Conversation Flow
# ### Introduction
# 1. For inbound: "Hello {{name}}, this is Priya from 4champz. Do you have 5-10 minutes to discuss chess coaching opportunities in Bangalore?"
# 2. For outbound: "Hello {{name}}, this is Priya from 4champz. I’m reaching out due to your interest. Available to discuss?"
# 3. Follow with: "I’d love to explore your background, answer FAQs like pricing or timings, or assist with reminders if applicable."
# ### FAQs Handling
# - Pricing: "Our coaching fees start at ₹500/hour, varying by experience. Interested in details?"
# - Timings: "Coaching is typically 3-6 PM school hours. Flexible options available—want to discuss?"
# - Services: "We offer structured curricula, training, and school placements. More questions?"
# ### Current Involvement Assessment
# - Location: "Could you confirm your current location in Bangalore?"
# - Involvement: "Are you actively playing or coaching chess?"
# - Availability: "What’s your schedule like, especially afternoons?"
# ### Experience and Background Qualification
# - Chess playing: "What’s your FIDE or All India Chess Federation rating?"
# - Tournaments: "Tell me about your recent tournament participation."
# - Coaching: "Have you coached children before, especially in chess?"
# - Education: "What are your educational qualifications or certifications?"
# ### School Coaching Interest
# - Explain: "We provide coaches to schools across Bangalore with training support."
# - Availability: "Are you free 3-6 PM? How many days weekly?"
# - Age groups: "Comfortable with Classes 1-12? Any preferences?"
# - Support: "We offer training. Interested in a structured curriculum?"
# ### Scheduling
# - If interested: "Let’s schedule a detailed discussion. When are you free this week?"
# - Use check_calendar_availability and book_appointment.
# - Confirm: "Please provide your full name, email, and preferred time."
# ### Close
# - Positive: "Thank you, {{name}}. We’ll send details and a confirmation. Looking forward to it!"
# - End with end_call unless transferred
# ## Response Guidelines
# - Handle FAQs before diving into qualification if asked
# - Use IST timing for scheduling (e.g., today is 03:14 PM IST, Friday, September 19, 2025)
# - Ask one question at a time to avoid overwhelming them
# - Keep responses focused on qualifying their suitability for school coaching
# - Ask location-specific questions about Bangalore areas they can cover
# - Show genuine enthusiasm for their chess achievements and experience
# - Be respectful of their current commitments and time constraints
# - Emphasize the opportunity to impact young minds through chess education
# ## Scenario Handling
# ### Interested Leads
# - Enthusiasm: "Your experience is impressive! Let’s connect you with a rep."
# - Route: Use transfer_call to sales rep.
# ### Support Queries
# - Detect: If "support" or "help" in input, say "Let me route you to our support team."
# - Route: Use transfer_call to support.
# ### Reminders
# - Meeting: "This is a reminder for your demo on [date/time]. Ready to proceed?" (e.g., use current date + 1 day if unspecified)
# - Payment: "This is a payment reminder for ₹500 due by [date]. Settled?" (e.g., use current date + 1 day if unspecified)
# ### For Highly Qualified Candidates
# - Express enthusiasm: "Your tournament experience and rating are impressive! Our partner schools would definitely value someone with your background."
# - Fast-track process: "Given your qualifications, I’d love to expedite our discussion. When would be the best time this week?"
# - Highlight premium opportunities: "With your experience, you’d be perfect for our advanced chess program placements at premium schools."
# ### For Candidates with Limited Formal Experience
# - Explore potential: "While formal ratings are helpful, we also value passion and teaching ability. Tell me about your experience with children or young people."
# - Training emphasis: "We provide comprehensive training to develop skills. Are you excited about growing with our support?"
# - Alternative qualifications: "Have you been involved in chess clubs, online coaching, or informal teaching?"
# ### For Availability Concerns
# - Flexible scheduling: "We can often accommodate different preferences. What times work best for you?"
# - Part-time opportunities: "Many coaches start part-time. Would that interest you?"
# - Location matching: "We’ll match you with convenient schools. Which Bangalore areas are accessible?"
# ### For Candidates Requesting Human Assistance
# - If they want human help or details on compensation/partnerships:
#   - Use transfer_call
#   - Say: "Of course! Let me connect you with our placement manager for details on partnerships and compensation."
# ## Knowledge Base
# ### Caller Info
# - name: {{name}}, email: {{email}}, phone_number: {{phone_number}}, role: {{role}}
# ### 4champz Model
# - Leading chess coaching in Bengaluru, school-focused, training provided
# - Partners with reputed schools, offers part-time/full-time opportunities
# - Focuses on developing young chess talent
# ### Requirements
# - 3-6 PM availability, English/Kannada/Hindi, Bangalore travel
# - Professional attitude, teaching aptitude, school-level chess knowledge
# ### Assessment Criteria
# - Chess playing experience and rating (FIDE/All India Chess Federation)
# - Tournament participation and achievements
# - Prior coaching/teaching experience, especially with children
# - Educational qualifications and chess certifications
# - Language capabilities and communication skills
# - Geographic availability across Bangalore
# - Flexibility with scheduling and age groups
# ## Response Refinement
# - When discussing chess background: "Your chess journey sounds fascinating. Could you tell more about [specific aspect]?"
# - When explaining opportunities: "Let me paint a picture of coaching with our partner schools..."
# - When confirming details: "To confirm—you’re available [availability] and comfortable with [preferences]. Is that accurate?"
# ## Call Management
# ### Available Functions
# - check_calendar_availability: Use for scheduling follow-up meetings
# - book_appointment: Use to confirm scheduled appointments
# - transfer_call: Use when candidate requests human assistance
# - end_call: Use to conclude every conversation
# ## Technical Considerations
# - If calendar delays occur: "I’m checking available slots. This will take a moment."
# - If multiple scheduling needs: "Let’s book your appointment first, then address other questions."
# - Always confirm appointment details before ending: "To confirm, we’re scheduled for [day], [date] at [time IST]. You’ll receive an email."
# ---
# Your goal is to qualify chess coaches for Bangalore schools, ensure they understand and are excited about the opportunity, and maintain 4champz’s professional reputation. Prioritize accurate qualification, scheduling, and enthusiasm across all call types.
# """

# # Groq LLM setup
# llm = ChatGroq(model_name="llama-3.1-8b-instant")
# # llm = ChatGroq(model_name="groq/compound-mini")

# # Config Manager
# config_manager = InMemoryConfigManager()

# # ADDED for JSON capture with LLM extraction: global in-memory store
# CONVERSATION_STORE: dict = {}  # ADDED for JSON LLM extraction

# # ADDED for JSON capture with LLM extraction: directory for local persistence
# CONVERSATIONS_DIR = Path("conversations")  # ADDED
# CONVERSATIONS_DIR.mkdir(exist_ok=True, parents=True)  # ADDED

# # ADDED n8n: store lead context by call_sid/conversation_id
# LEAD_CONTEXT_STORE: dict = {}  # ADDED n8n


# # Sentiment Analysis Chain (using Groq LLM)
# sentiment_prompt = PromptTemplate(
#     input_variables=["transcript"],
#     template="Analyze the sentiment of this transcript: {transcript}. Return a JSON with 'sentiment' (positive, neutral, negative, angry, confused) and 'tone_score' (1-10, 10 being most positive)."
# )
# sentiment_chain = LLMChain(llm=llm, prompt=sentiment_prompt)

# # Summary Generation Chain (using Groq LLM)
# summary_prompt = PromptTemplate(
#     input_variables=["transcript"],
#     template="Generate a summary of this transcript: {transcript}. Include key points, customer intent, and next actions. Return a JSON with 'summary', 'intent', 'next_actions' (array of strings)."
# )
# summary_chain = LLMChain(llm=llm, prompt=summary_prompt)



# # Send Email Function
# def send_email(to_email: str, subject: str, body: str):
#     msg = MIMEText(body)
#     msg['Subject'] = subject
#     msg['From'] = EMAIL_SENDER
#     msg['To'] = to_email
#     with smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT) as server:
#         server.starttls()  # Added TLS for security
#         server.login(EMAIL_SENDER, EMAIL_PASSWORD)
#         server.sendmail(EMAIL_SENDER, to_email, msg.as_string())
#     logger.info(f"Email sent to {to_email}")

# # Send WhatsApp Summary Function (using Twilio)
# def send_whatsapp(to_phone: str, body: str):
#     client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#     client.messages.create(
#         from_='whatsapp:' + WHATSAPP_SENDER,
#         body=body,
#         to='whatsapp:' + to_phone
#     )
#     logger.info(f"WhatsApp sent to {to_phone}")



# # NEW: Check Calendar Availability
# async def check_calendar_availability(preferred_time: str) -> dict:
#     headers = {"Authorization": f"Bearer {CRM_API_KEY}"}
#     params = {"time": preferred_time, "timezone": "Asia/Kolkata"}
#     async with httpx.AsyncClient() as client:
#         response = await client.get(CALENDAR_API_URL, headers=headers, params=params)
#         if response.status_code == 200:
#             return response.json()
#         logger.error(f"Calendar check failed: {response.text}")
#         return {"available": False, "slots": []}
    


# # NEW: Book Appointment
# async def book_appointment(lead_id: str, name: str, email: str, time: str):
#     payload = {
#         "lead_id": lead_id,
#         "name": name,
#         "email": email,
#         "time": time,
#         "status": "Scheduled"
#     }
#     headers = {"Authorization": f"Bearer {CRM_API_KEY}"}
#     async with httpx.AsyncClient() as client:
#         response = await client.post(f"{CRM_API_URL}/appointments", json=payload, headers=headers)
#         if response.status_code == 200:
#             logger.info(f"Appointment booked for lead {lead_id}")
#             return True
#         logger.error(f"Appointment booking failed: {response.text}")
#         return False


# # NEW: Update CRM Function (placeholder; replace with your CRM API)
# def update_crm(lead_id: str, transcript: str, sentiment: dict, summary: dict, audio_url: str, twilio_audio_url: Optional[str] = None, status: str = "Called", appointment: dict = None):
#     payload = {
#         "lead_id": lead_id,
#         "transcript": transcript,
#         "sentiment": sentiment,
#         "summary": summary,
#         "audio_url": audio_url,
#         "twilio_audio_url": twilio_audio_url,  # NEW: Twilio full call recording
#         "status": status,
#         "appointment": appointment
#     }
#     headers = {"Authorization": f"Bearer {CRM_API_KEY}"}
#     response = requests.post(CRM_API_URL, json=payload, headers=headers)
#     if response.status_code == 200:
#         logger.info(f"CRM updated for lead {lead_id}")
#     else:
#         logger.error(f"CRM update failed: {response.text}")



# # Events Manager to log transcripts
# class ChessEventsManager(events_manager.EventsManager):
#     def __init__(self):
#         super().__init__(subscriptions=[EventType.TRANSCRIPT_COMPLETE])

#     async def handle_event(self, event: Event):
#         if event.type == EventType.TRANSCRIPT_COMPLETE:
#             transcript_complete_event = typing.cast(TranscriptCompleteEvent, event)
#             transcript = transcript_complete_event.transcript.to_string()
#             logger.debug(f"Transcript for conversation {transcript_complete_event.conversation_id}: {transcript}")

#             # NEW: Sentiment analysis
#             sentiment = await sentiment_chain.ainvoke({"transcript": transcript})

#             # NEW: Summary generation
#             summary = await summary_chain.ainvoke({"transcript": transcript})

#             # NEW: Recording storage (using Deepgram audio chunks)
#             audio_path = await save_recording(transcript_complete_event.conversation_id)
#             audio_url = f"{CLOUD_STORAGE_URL}/{os.path.basename(audio_path)}" if CLOUD_STORAGE_URL else audio_path

#             # NEW: Fetch Twilio recording URL if available
#             client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#             recordings = await asyncio.get_event_loop().run_in_executor(
#                 None,
#                 lambda: client.recordings.list(call_sid=transcript_complete_event.conversation_id)
#             )
#             twilio_audio_url = recordings[0].uri if recordings else None  # NEW: Get Twilio recording URL

#             await asyncio.get_event_loop().run_in_executor(
#                 None, 
#                 lambda: update_crm(transcript_complete_event.conversation_id, transcript, sentiment, summary, audio_url, twilio_audio_url=twilio_audio_url)  # Fixed to use audio_url
#             )

#             # NEW: Send summary to customer/management
#             # Assume email and phone from lead context or CRM
#             short_summary = f"Call Summary: {summary['summary'][:100]}... Next steps: {', '.join(summary['next_actions'][:2])}"
#             lead = LEAD_CONTEXT_STORE.get(transcript_complete_event.conversation_id, {})
#             if "email" in lead:
#                 send_email(lead["email"], "Call Summary", short_summary)
#             if "to_phone" in lead:
#                 send_whatsapp(lead["to_phone"], short_summary)

#             webhook_url = os.getenv("TRANSCRIPT_CALLBACK_URL")
#             if webhook_url:
#                 data = {"conversation_id": transcript_complete_event.conversation_id, "user_id": 1, "transcript": transcript}
#                 async with httpx.AsyncClient() as client:
#                     response = await client.post(webhook_url, json=data)
#                     if response.status_code == 200:
#                         logger.info("Transcript sent successfully to webhook")
#                     else:
#                         logger.error(f"Failed to send transcript to webhook: {response.status_code}")
#             # ADDED for JSON capture with LLM extraction: write store JSON to disk
#             try:
#                 convo = CONVERSATION_STORE.get(transcript_complete_event.conversation_id)
#                 if convo:
#                     convo["sentiment"] = sentiment  # NEW
#                     convo["summary"] = summary  # NEW
#                     out_path = CONVERSATIONS_DIR / f"{transcript_complete_event.conversation_id}.json"
#                     with open(out_path, "w", encoding="utf-8") as f:
#                         json.dump(convo, f, ensure_ascii=False, indent=2)
#                     logger.info(f"Wrote JSON summary to {out_path}")
#             except Exception as e:
#                 logger.error(f"Failed to write JSON summary: {e}")


# async def save_recording(conversation_id: str) -> str:
#     # Assume transcriber instance is accessible via a global or passed reference
#     transcriber = None  # Placeholder; should be injected or managed by TelephonyServer
#     if transcriber and hasattr(transcriber, 'audio_buffer') and transcriber.conversation_id == conversation_id:
#         await transcriber._save_audio()
#         audio_path = RECORDINGS_DIR / f"{conversation_id}.wav"
#         return str(audio_path)
#     logger.error(f"No valid transcriber or buffer for conversation {conversation_id}")
#     return ""

# # Custom Agent Config
# class CustomLangchainAgentConfig(LangchainAgentConfig, type="agent_langchain"):
#     initial_message: BaseMessage = BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?")
#     prompt_preamble: str = CHESS_COACH_PROMPT_PREAMBLE
#     model_name: str = "llama-3.1-8b-instant"
#     # model_name: str = "groq/compound-mini"
#     api_key: str = GROQ_API_KEY
#     provider: str = "groq"

# # Custom Langchain Agent
# class CustomLangchainAgent(LangchainAgent):
#     def __init__(self, agent_config: CustomLangchainAgentConfig):
#         logger.debug(f"Initializing CustomLangchainAgent with config: {agent_config}")
#         super().__init__(agent_config=agent_config)
#         self.last_response_time = time.time()
#         self.conversation_state = "initial"
#         self.no_input_count = 0
#         self.user_name = None  # store extracted/confirmed name
#         self.asked_for_name = False  # track if name is requested
#         logger.debug("Initialized CustomLangchainAgent with Groq LLM (llama-3.1-8b-instant)")
#         # ADDED for JSON capture with LLM extraction
#         self.turns = []  # [{"speaker":"user"/"bot","text":..., "ts": epoch_ms}]
#         self.conversation_id_cache = None  # to index the global store
#         self.extracted_slots = {}  # LLM-extracted structured data


#     # ADDED n8n: helper to ensure id
#     def _ensure_conv_id(self, conversation_id: Optional[str]) -> str:
#         if conversation_id and isinstance(conversation_id, str) and conversation_id.strip():
#             return conversation_id
#         return f"unknown_{int(time.time()*1000)}"

#     # ADDED for JSON capture with LLM extraction
#     def _flush_to_disk(self, conversation_id: str):
#         """Write the current conversation JSON to disk immediately."""
#         try:
#             payload = CONVERSATION_STORE.get(conversation_id)
#             if not payload:
#                 return
#             out_path = CONVERSATIONS_DIR / f"{conversation_id}.json"
#             with open(out_path, "w", encoding="utf-8") as f:
#                 json.dump(payload, f, ensure_ascii=False, indent=2)
#             logger.debug(f"Flushed conversation {conversation_id} to {out_path}")
#         except Exception as e:
#             logger.error(f"Flush to disk failed for {conversation_id}: {e}")

#     # ADDED for JSON capture with LLM extraction
#     def _persist_state(self, conversation_id: Optional[str]):
#         conv_id = self._ensure_conv_id(conversation_id)
#         now_ms = int(time.time() * 1000)
#         lead = LEAD_CONTEXT_STORE.get(conv_id, {})  # ADDED n8n
#         payload = {
#             "conversation_id": conv_id,
#             "updated_at": now_ms,
#             "lead": lead,  # ADDED n8n
#             "slots": self.extracted_slots,  # slots are LLM-extracted
#             "turns": self.turns
#         }
#         CONVERSATION_STORE[conv_id] = payload
#         self._flush_to_disk(conv_id)  # ADDED: always flush on persist

#     # ADDED for JSON capture with LLM extraction
#     def _strip_code_fences(self, s: str) -> str:
#         t = (s or "").strip()
#         if t.startswith("```"):
#             end = t.rfind("```")
#             if end > 0:
#                 inner = t[3:end].strip()
#                 if inner.lower().startswith("json"):
#                     inner = inner[4:].strip()
#                 return inner
#         return t

#     # ADDED for JSON capture with LLM extraction
#     async def _extract_slots_with_llm(self, conversation_id: str):
#         """Extract slots with retry logic."""
#         max_retries = 3
#         retry_delay = 2  # seconds

#         for attempt in range(max_retries):
#             try:
#                 # Build a compact transcript string
#                 convo_lines = []
#                 for t in self.turns[-30:]:
#                     role = "User" if t["speaker"] == "user" else "Agent"
#                     text_line = re.sub(r'\s+', ' ', t['text']).strip()
#                     convo_lines.append(f"{role}: {text_line}")
#                 convo_text = "\n".join(convo_lines)

#                 # Instruction for JSON-only schema
#                 schema_instruction = (
#                     "Return ONLY a JSON object with these keys:\n"
#                     "{\n"
#                     '  "location": string|null,\n'
#                     '  "involvement": "playing"|"coaching"|null,\n'
#                     '  "availability": string|null,\n'
#                     '  "age_range": string|null,\n'
#                     '  "languages": string[]|null,\n'
#                     '  "rating": string|null,\n'
#                     '  "tournaments": string|null,\n'
#                     '  "certifications": string|null,\n'
#                     '  "questions": string[]|null,\n'
#                     '  "intent": "interested"|"support"|"reminder"|null\n'
#                     '}\n'
#                     "Infer conservatively. Use null if not explicitly known."
#                 )

#                 prompt = f"{schema_instruction}\n\nConversation:\n{convo_text}\n\nJSON:"

#                 extractor = ChatGroq(model_name="llama-3.1-8b-instant")
#                 resp = await extractor.ainvoke([
#                     {"role": "system", "content": "You extract structured information from conversations."},
#                     {"role": "user", "content": prompt}
#                 ])

#                 # Normalize content
#                 content = None
#                 if hasattr(resp, "content"):
#                     content = resp.content
#                 elif hasattr(resp, "generations"):
#                     try:
#                         content = resp.generations.text
#                     except Exception:
#                         content = str(resp)
#                 else:
#                     content = str(resp)

#                 parsed = None
#                 try:
#                     c = self._strip_code_fences(content)
#                     parsed = json.loads(c)
#                 except Exception:
#                     logger.warning("Primary JSON parse failed; attempting to locate JSON object")
#                     first = content.find("{")
#                     last = content.rfind("}")
#                     if first != -1 and last != -1 and last > first:
#                         snippet = content[first:last+1]
#                         try:
#                             parsed = json.loads(snippet)
#                         except Exception:
#                             parsed = None

#                 if isinstance(parsed, dict):
#                     # normalize keys
#                     for k in ["location","involvement","availability","age_range","languages","rating","tournaments","certifications","questions"]:
#                         if k not in parsed:
#                             parsed[k] = None
#                     # Ensure types
#                     if parsed.get("languages") is not None and not isinstance(parsed["languages"], list):
#                         parsed["languages"] = [str(parsed["languages"])]
#                     if parsed.get("questions") is not None and not isinstance(parsed["questions"], list):
#                         parsed["questions"] = [str(parsed["questions"])]

#                     self.extracted_slots = parsed
#                     self._persist_state(conversation_id)
#                 else:
#                     logger.warning("LLM extraction did not return a dict; keeping previous slots.")
#                     if attempt < max_retries - 1:
#                         await asyncio.sleep(retry_delay)
#                         continue
#                     raise ValueError("Failed to parse valid JSON after retries")

#             except Exception as e:
#                 logger.error(f"Slot extraction failed (attempt {attempt + 1}/{max_retries}): {e}")
#                 if attempt < max_retries - 1:
#                     await asyncio.sleep(retry_delay)
#                     continue
#                 raise  # Re-raise after final attempt

#     async def end_call(self, conversation_id: str):
#         """End the call by returning a TwiML Hangup response."""
#         twiml_response = '<?xml version="1.0" encoding="UTF-8"?><Response><Hangup/></Response>'
#         await self.send_message(BaseMessage(text=twiml_response), conversation_id)  # Use existing send_message to pass TwiML
#         logger.info(f"Call ended for conversation_id: {conversation_id}")

#     async def respond(self, human_input: str, conversation_id: str, is_interrupt: bool = False) -> Tuple[Optional[str], bool]:
#         try:
#             start_time = time.time()

#             if conversation_id and self.conversation_id_cache != conversation_id:
#                 self.conversation_id_cache = conversation_id
#             current_id = self.conversation_id_cache or conversation_id or "unknown"

#             if human_input:
#                 self.turns.append({"speaker": "user", "text": human_input, "ts": int(time.time()*1000)})
#                 if len(self.turns) % 2 == 0:
#                     asyncio.create_task(self._extract_slots_with_llm(current_id))
#                 self._persist_state(current_id)

#             def personalize_response(text: str) -> str:
#                 if self.user_name:
#                     return text.replace("{name}", self.user_name)
#                 external_name = "there"
#                 return text.replace("{name}", external_name)

#             if time.time() - self.last_response_time > 15:
#                 self.no_input_count += 1
#                 logger.warning(f"No transcription for 15s (attempt {self.no_input_count})")
#                 if self.no_input_count >= 3:
#                     bot_text = personalize_response("Trouble connecting. I’ll follow up later. Thank you!")
#                     self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                     self._persist_state(current_id)
#                     await self.end_call(conversation_id)  # New: End the call
#                     return bot_text, True
#                 bot_text = personalize_response("I didn’t catch that. Available to discuss chess coaching?")
#                 self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return bot_text, False

#             normalized = (human_input or "").strip().lower()
#             filler_phrases = {"", "mhmm", "okay", "what", "yes", "no", "a-", "four", "hello", "hi"}
#             if normalized in filler_phrases:
#                 self.no_input_count += 1
#                 logger.debug(f"Filler input (count {self.no_input_count}): '{human_input}'")
#                 if self.no_input_count >= 3:
#                     bot_text = personalize_response("No valid input. I’ll follow up later. Thank you!")
#                     self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                     self._persist_state(current_id)
#                     return bot_text, True
#                 self.last_response_time = start_time
#                 bot_text = personalize_response("Didn’t catch that. Confirm availability?")
#                 self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return bot_text, False

#             gibberish_indicators = ["what is the first time", "first time", "please repeat", "say again"]
#             if any(phrase in normalized for phrase in gibberish_indicators):
#                 self.no_input_count += 1
#                 logger.debug(f"Gibberish input (count {self.no_input_count}): '{human_input}'")
#                 if self.no_input_count >= 3:
#                     bot_text = personalize_response("Trouble connecting. I’ll follow up later. Thank you!")
#                     self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                     self._persist_state(current_id)
#                     return bot_text, True
#                 self.last_response_time = start_time
#                 bot_text = personalize_response("Sorry, repeat or say yes/no if available?")
#                 self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return bot_text, False

#             self.no_input_count = 0

#             if self.asked_for_name and "name is" in normalized:
#                 try:
#                     name_part = human_input.lower().split("name is", 1)[1].strip().split()
#                     self.user_name = name_part[0].capitalize()
#                     logger.debug(f"Extracted user name: {self.user_name}")
#                 except Exception:
#                     self.user_name = None

#             slots = self.extracted_slots
#             intent = slots.get("intent")

#             # FAQ handling
#             if any(q in normalized for q in ["price", "pricing", "cost", "timings", "time", "services"]):
#                 if "price" in normalized or "cost" in normalized:
#                     response = "Our fees start at ₹500/hour, varying by experience. Want more details?"
#                 elif "timings" in normalized or "time" in normalized:
#                     response = "Coaching is 3-6 PM school hours. Flexible options available—discuss?"
#                 elif "services" in normalized:
#                     response = "We offer curricula, training, and school placements. More questions?"
#                 self.last_response_time = start_time
#                 self.turns.append({"speaker": "bot", "text": response, "ts": int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return response, False

#             # NEW: Real-time sentiment-based routing
#             sentiment = await sentiment_chain.ainvoke({"transcript": "\n".join(t["text"] for t in self.turns)})
#             if sentiment["sentiment"] == "angry" or "upset" in normalized:
#                 logger.info("Detected angry tone, routing to calm rep")
#                 bot_text = "I’ll connect you with a calm rep to assist you."
#                 self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return bot_text, True

#             if self.conversation_state == "initial":
#                 if any(word in normalized for word in ["yes", "sure", "okay", "available"]):
#                     self.conversation_state = "background"
#                     response = "Great! Due to your interest, confirm your Bangalore location?"
#                 else:
#                     response = personalize_response("Sorry, misheard. Available to discuss coaching?")
#                 self.last_response_time = start_time
#                 self.turns.append({"speaker": "bot", "text": response, "ts": int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return response, False
#             else:
#                 try:
#                     response, should_end = await asyncio.wait_for(
#                         super().respond(human_input, conversation_id, is_interrupt), timeout=5.0
#                     )
#                 except asyncio.TimeoutError:
#                     fallback_msg = personalize_response("Response delayed. Try again shortly.")
#                     self.turns.append({"speaker": "bot", "text": fallback_msg, "ts": int(time.time()*1000)})
#                     self._persist_state(current_id)
#                     await self.end_call(conversation_id)  # New: End call on timeout
#                     return fallback_msg, True

#                 if response:
#                     response_text = personalize_response(response)
#                     if "location" in response_text.lower():
#                         self.conversation_state = "background"
#                     if any(phrase in response_text.lower() for phrase in ["confirm your full name", "may i have your name"]):
#                         self.asked_for_name = True

#                     if intent == "interested" and "schedule" in response_text.lower():
#                         available_slots = await check_calendar_availability(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
#                         if available_slots["available"]:
#                             bot_text = f"Great! Available slots: {', '.join(available_slots['slots'])}. Provide name, email, and preferred time?"
#                             self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                             self._persist_state(current_id)
#                             return bot_text, False
#                         else:
#                             bot_text = "No slots available now. I’ll follow up. Thank you!"
#                             self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                             self._persist_state(current_id)
#                             await self.end_call(conversation_id)  # New: End the call
#                             return bot_text, True

#                     if intent == "support":
#                         bot_text = "Let me route you to our support team."
#                         self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                         self._persist_state(current_id)
#                         return bot_text, True
#                     elif intent == "interested":
#                         bot_text = "Impressive! Connecting you to a sales rep."
#                         self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                         self._persist_state(current_id)
#                         await self.end_call(conversation_id)  # New: End call after routing
#                         return bot_text, True

#                     self.last_response_time = start_time
#                     self.turns.append({"speaker": "bot", "text": response_text, "ts": int(time.time()*1000)})
#                     if len(self.turns) % 4 == 0:
#                         asyncio.create_task(self._extract_slots_with_llm(current_id))
#                     self._persist_state(current_id)
#                     return response_text, should_end

#                 fallback_msg = personalize_response("Didn’t get that. Tell me more?")
#                 self.last_response_time = start_time
#                 self.turns.append({"speaker": "bot", "text": fallback_msg, "ts": int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return fallback_msg, False

#         except Exception as e:
#             logger.error(f"Error generating response: {str(e)}")
#             fallback_error_msg = "Error occurred. Try again."
#             self.turns.append({"speaker": "bot", "text": fallback_error_msg, "ts": int(time.time()*1000)})
#             current_id = self.conversation_id_cache or conversation_id or "unknown"
#             self._persist_state(current_id)
#             return fallback_error_msg, False
    








# # Custom Deepgram Transcriber with keepalive and chunk logging
# class CustomDeepgramTranscriber(DeepgramTranscriber):
#     def __init__(self, transcriber_config: DeepgramTranscriberConfig):
#         super().__init__(transcriber_config)
#         self.audio_buffer = io.BytesIO()
#         self.conversation_id = None

#     async def process(self, audio_chunk: bytes):
#         logger.debug(f"Processing audio chunk size: {len(audio_chunk)} bytes")
#         if not audio_chunk or len(audio_chunk) == 0:
#             logger.warning("Empty audio chunk - skipping")
#             return None
#         try:
#             async with self.buffer_lock:
#                 if self.conversation_id:
#                     total_size = self.audio_buffer.tell() + len(audio_chunk)
#                     if total_size > 10 * 1024 * 1024:  # 10MB limit
#                         await self._save_audio()
#                     self.audio_buffer.write(audio_chunk)
#             return await super().process(audio_chunk)
#         except Exception as e:
#             logger.error(f"Deepgram process error: {e}")
#             raise
    

#     async def keepalive(self):
#         while True:
#             await asyncio.sleep(10)
#             try:
#                 await super().process(b"\x00" * 160)
#                 logger.debug("Deepgram keepalive sent")
#             except Exception as e:
#                 logger.error(f"Keepalive failed: {e}")
#                 break


#     def set_conversation_id(self, conversation_id: str):
#         if self.conversation_id != conversation_id:
#             if self.audio_buffer.tell() > 0:
#                 asyncio.create_task(self._save_audio())
#             self.conversation_id = conversation_id
#             self.audio_buffer = io.BytesIO()

#     async def _save_audio(self):
#         if self.conversation_id and self.audio_buffer.tell() > 0:
#             self.audio_buffer.seek(0)
#             audio_path = RECORDINGS_DIR / f"{self.conversation_id}.wav"
#             with open(audio_path, 'wb') as f:
#                 f.write(self.audio_buffer.getbuffer())
#             logger.info(f"Saved audio to {audio_path}")
#             self.audio_buffer = io.BytesIO()

# # Custom Agent Factory
# class CustomAgentFactory:
#     def create_agent(self, agent_config: AgentConfig, logger: Optional[logging.Logger] = None) -> BaseAgent:
#         log = logger or globals().get('logger', logging.getLogger(__name__))
#         log.debug(f"Creating agent with config type: {agent_config.type}")
#         if agent_config.type == "agent_langchain":
#             log.debug("Creating CustomLangchainAgent")
#             return CustomLangchainAgent(agent_config=typing.cast(CustomLangchainAgentConfig, agent_config))
#         log.error(f"Invalid agent config type: {agent_config.type}")
#         raise Exception(f"Invalid agent config: {agent_config.type}")

# # Custom Synthesizer Factory
# class CustomSynthesizerFactory:
#     def create_synthesizer(self, synthesizer_config: SynthesizerConfig) -> BaseSynthesizer:
#         logger.debug(f"Creating synthesizer with config: {synthesizer_config}")
#         if isinstance(synthesizer_config, StreamElementsSynthesizerConfig):
#             logger.debug("Creating StreamElementsSynthesizer")
#             return StreamElementsSynthesizer(synthesizer_config)
#         logger.error(f"Invalid synthesizer config type: {synthesizer_config.type}")
#         raise Exception(f"Invalid synthesizer config: {synthesizer_config.type}")

# # FastAPI App
# app = FastAPI()

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     logger.debug("Starting up FastAPI application")
#     logger.debug("Registered routes:")
#     for route in app.routes:
#         methods = getattr(route, "methods", ["WebSocket"])
#         logger.debug(f" - {route.path} ({methods})")
#     yield
#     # ADDED: final sweep to persist any in-memory conversations at shutdown
#     try:
#         for conv_id in list(CONVERSATION_STORE.keys()):
#             out_path = CONVERSATIONS_DIR / f"{conv_id}.json"
#             with open(out_path, "w", encoding="utf-8") as f:
#                 json.dump(CONVERSATION_STORE[conv_id], f, ensure_ascii=False, indent=2)
#         logger.debug("Shutdown flush completed for all conversations")
#     except Exception as e:
#         logger.error(f"Error during shutdown flush: {e}")
#     logger.debug("Shutting down FastAPI application")

# app.router.lifespan_context = lifespan

# # Twilio config
# twilio_config = TwilioConfig(
#     account_sid=TWILIO_ACCOUNT_SID,
#     auth_token=TWILIO_AUTH_TOKEN
# )

# # Synthesizer config (telephone voice output)
# synthesizer_config = StreamElementsSynthesizerConfig.from_telephone_output_device(
#     voice="Brian"
# )

# transcriber_config = DeepgramTranscriberConfig(
#     api_key=DEEPGRAM_API_KEY,
#     model="nova-2-phonecall",
#     language="en",
#     sampling_rate=8000,  # int primitive, not enum
#     audio_encoding="mulaw",  # lowercase string, not enum
#     chunk_size=320,
#     endpointing_config=PunctuationEndpointingConfig(),
#     downsampling=1,
# )

# agent_config = LangchainAgentConfig(
#     initial_message=BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"),
#     prompt_preamble=CHESS_COACH_PROMPT_PREAMBLE,
#     model_name="llama-3.1-8b-instant",
#     # model_name="groq/compound-mini",
#     api_key=GROQ_API_KEY,
#     provider="groq",
# )



# # Telephony Server setup
# telephony_server = TelephonyServer(
#     base_url=BASE_URL,  # your ngrok url
#     config_manager=config_manager,
#     inbound_call_configs=[
#         TwilioInboundCallConfig(
#             url="/inbound_call",
#             twilio_config=twilio_config,
#             agent_config=agent_config,
#             synthesizer_config=synthesizer_config,
#             transcriber_config=transcriber_config,  # Use instance
#             twiml_fallback_response='''<?xml version="1.0" encoding="UTF-8"?>
# <Response>
#     <Say>I didn't hear a response. Are you still there? Please say something to continue.</Say>
#     <Pause length="15"/>
#     <Redirect method="POST">/inbound_call</Redirect>
# </Response>''',
#             record=True,
#             status_callback=f"https://{BASE_URL}/call_status",  # NEW: Added for inbound call status
#             status_callback_method="POST",
#             status_callback_event=["completed"]  # Trigger on call completion
#         )
#     ],
#     agent_factory=CustomAgentFactory(),
#     synthesizer_factory=CustomSynthesizerFactory(),
#     events_manager=ChessEventsManager(),
# )

# # Add routes to FastAPI app
# app.include_router(telephony_server.get_router())


# # NEW: Endpoint to handle Twilio call status callbacks for inbound calls
# @app.post("/call_status")
# async def call_status(request: Request):
#     data = await request.json()
#     call_sid = data.get("CallSid")
#     if data.get("CallStatus") == "completed":
#         logger.info(f"Inbound call {call_sid} completed")
#     return {"ok": True}


# # NEW: Endpoint to serve conversation JSON files
# @app.get("/conversations/{call_sid}.json")
# async def get_conversation(call_sid: str):
#     path = CONVERSATIONS_DIR / f"{call_sid}.json"
#     if path.exists():
#         with open(path, "r", encoding="utf-8") as f:
#             return json.load(f)
#     raise HTTPException(status_code=404, detail="Conversation not found")


# # ADDED n8n: request schema for outbound_call
# class OutboundCallRequest(BaseModel):
#     to_phone: str
#     lead: typing.Optional[typing.Dict[str, typing.Any]] = None
#     transcript_callback_url: typing.Optional[str] = None
#     call_type: str = "qualification"  # NEW: qualification, reminder, payment

# # ADDED n8n: normalize to E164 basic
# def normalize_e164(number: str) -> str:
#     n = re.sub(r'\D+', '', number or '')
#     if not n:
#         return number
#     if n.startswith('0'):
#         n = n.lstrip('0')
#     if not n.startswith('+'):
#         if len(n) == 10:
#             n = '+91' + n
#         else:
#             n = '+' + n
#     return n

# # ADDED n8n: HTTP endpoint to start outbound call from n8n
# @app.post("/outbound_call")
# async def outbound_call(req: OutboundCallRequest):
#     try:
#         to_phone = normalize_e164(req.to_phone)
#         if not to_phone or len(to_phone) < 10:
#             raise HTTPException(status_code=400, detail="Invalid phone")
#         sid = await make_outbound_call(to_phone, req.call_type, req.lead)
#         lead = req.lead or {}
#         lead["to_phone"] = to_phone
#         LEAD_CONTEXT_STORE[sid] = lead
#         logger.info(f"Outbound call requested via n8n: SID={sid}, lead={lead}")
#         if req.transcript_callback_url:
#             os.environ["TRANSCRIPT_CALLBACK_URL"] = req.transcript_callback_url
#         return {"ok": True, "call_sid": sid}
#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"/outbound_call failed: {e}")
#         raise HTTPException(status_code=500, detail=str(e))


# # Outbound call helper
# async def make_outbound_call(to_phone: str, call_type: str, lead: dict = None):
#     client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#     twilio_base_url = f"https://{BASE_URL}"
#     initial_message = {
#         "qualification": "Hello, this is Priya from 4champz. Available to discuss chess coaching?",
#         "reminder": f"This is a reminder for your demo on {lead.get('demo_date', time.strftime('%Y-%m-%d %H:%M IST', time.localtime(time.time() + 86400)))}. Ready?",
#         "payment": f"Payment reminder for ₹500 due by {lead.get('due_date', time.strftime('%Y-%m-%d', time.localtime(time.time() + 86400)))}. Settled?"
#     }.get(call_type, "Hello, this is Priya from 4champz. How can I assist?")
#     call = await asyncio.get_event_loop().run_in_executor(
#         None,
#         lambda: client.calls.create(
#             to=to_phone,
#             from_=TWILIO_PHONE_NUMBER,
#             url=f"{twilio_base_url}/inbound_call",
#             status_callback=f"{twilio_base_url}/call_status",
#             status_callback_method="POST",
#             status_callback_event=["initiated", "ringing", "answered", "completed"],
#             record=True,
#             recording_channels="dual",
            
#         )
#     )
#     logger.info(f"Call initiated: SID={call.sid}, type={call_type}")
#     if call.sid not in LEAD_CONTEXT_STORE:
#         LEAD_CONTEXT_STORE[call.sid] = {"to_phone": to_phone, "call_type": call_type, **(lead or {})}
#     CONVERSATION_STORE.setdefault(call.sid, {
#         "conversation_id": call.sid,
#         "updated_at": int(time.time()*1000),
#         "lead": LEAD_CONTEXT_STORE.get(call.sid, {}),
#         "slots": {},
#         "turns": [{"speaker": "bot", "text": initial_message, "ts": int(time.time()*1000)}]
#     })
#     return call.sid




# # NEW: Outbound Call Scheduler (for auto-dialing from CRM)
# def outbound_scheduler():
#     while True:
#         response = requests.get(CRM_API_URL, headers={"Authorization": f"Bearer {CRM_API_KEY}"})
#         if response.status_code == 200:
#             leads = response.json().get("leads", [])  # Adjusted to 'leads' for generality
#             for lead in leads:
#                 if lead.get("status") == "Call Pending":
#                     call_type = lead.get("call_type", "qualification")
#                     asyncio.run(make_outbound_call(lead["phone"], call_type, lead))
#                     update_crm(lead["id"], "", {}, {}, "", status="Calling")
#         time.sleep(300)  # Poll every 5 minutes
# # Main entrypoint (updated to include scheduler)
# if __name__ == "__main__":
#     import uvicorn

#     def run_server():
#         logger.debug("Starting Uvicorn server")
#         uvicorn.run(app, host="0.0.0.0", port=3000)

#     # Start outbound scheduler in a thread
#     scheduler_thread = threading.Thread(target=outbound_scheduler, daemon=True)
#     scheduler_thread.start()

#     run_server()


















# import os
# import logging
# import asyncio
# import httpx
# import typing
# import time
# from typing import Optional, Tuple
# from fastapi import FastAPI, Request, Response
# from fastapi.logger import logger as fastapi_logger
# from contextlib import asynccontextmanager
# from dotenv import load_dotenv
# from twilio.rest import Client
# from vocode.streaming.telephony.server.base import TelephonyServer, TwilioInboundCallConfig
# from vocode.streaming.models.telephony import TwilioConfig
# from vocode.streaming.models.agent import LangchainAgentConfig, AgentConfig
# from vocode.streaming.agent.langchain_agent import LangchainAgent
# from vocode.streaming.models.message import BaseMessage
# from vocode.streaming.transcriber.deepgram_transcriber import DeepgramTranscriber
# from vocode.streaming.models.transcriber import DeepgramTranscriberConfig, AudioEncoding, PunctuationEndpointingConfig
# from vocode.streaming.synthesizer.stream_elements_synthesizer import StreamElementsSynthesizer
# from vocode.streaming.models.synthesizer import StreamElementsSynthesizerConfig, SynthesizerConfig
# from vocode.streaming.synthesizer.base_synthesizer import BaseSynthesizer
# from vocode.streaming.telephony.config_manager.in_memory_config_manager import InMemoryConfigManager
# from vocode.streaming.agent.base_agent import BaseAgent
# from vocode.streaming.models.events import Event, EventType
# from vocode.streaming.models.transcript import TranscriptCompleteEvent
# from vocode.streaming.utils import events_manager
# from langchain_groq import ChatGroq
# import threading
# import numpy as np

# # ADDED for JSON capture with LLM extraction
# import json  # ADDED for JSON capture with LLM extraction
# import re    # ADDED: general regex utilities
# from pathlib import Path  # ADDED: filesystem-safe paths
# from fastapi import HTTPException  # ADDED n8n
# from pydantic import BaseModel  # ADDED n8n

# # NEW: For sentiment analysis and summaries (using Groq LLM)
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain


# # NEW: For email summaries (simple SMTP)
# import smtplib
# from email.mime.text import MIMEText

# # NEW: For WhatsApp summaries (using Twilio)
# from twilio.rest import Client as TwilioClient

# # NEW: Placeholder CRM API (replace with your CRM, e.g., HubSpot API)
# import requests  # NEW: for CRM API calls


# from pydub import AudioSegment  # NEW: For audio conversion (MP3/WAV)
# import wave  # NEW: For WAV file handling
# import io

# # Configure logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# fastapi_logger.setLevel(logging.DEBUG)

# # Ensure ffmpeg is in PATH
# os.environ['PATH'] += os.pathsep + 'C:\\ffmpeg\\bin'

# load_dotenv()

# # Environment variables
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
# TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
# TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
# BASE_URL = os.getenv("BASE_URL")
# DEBUG_AUDIO = os.getenv("DEBUG_AUDIO", "false").lower() == "true"


# # NEW: Storage directory for recordings
# RECORDINGS_DIR = Path("recordings")
# RECORDINGS_DIR.mkdir(exist_ok=True, parents=True)

# # NEW: Cloud storage URL (e.g., AWS S3 placeholder)
# CLOUD_STORAGE_URL = os.getenv("CLOUD_STORAGE_URL", "https://your-s3-bucket.s3.amazonaws.com/")


# # NEW: CRM environment variables (replace with your CRM details)
# CRM_API_URL = os.getenv("CRM_API_URL", "https://your-crm-api.com/leads")
# CRM_API_KEY = os.getenv("CRM_API_KEY", "your_crm_api_key")
# EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER", "smtp.example.com")
# EMAIL_SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", 587))
# EMAIL_SENDER = os.getenv("EMAIL_SENDER", "priya@4champz.com")
# EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your_email_password")
# CALENDAR_API_URL = os.getenv("CALENDAR_API_URL", "https://your-calendar-api.com/availability")  # NEW: for scheduling

# # NEW: WhatsApp sender number (for summaries)
# WHATSAPP_SENDER = os.getenv("WHATSAPP_SENDER", TWILIO_PHONE_NUMBER)



# # Validate environment variables
# required_vars = [GROQ_API_KEY, DEEPGRAM_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, BASE_URL, CRM_API_URL, CRM_API_KEY, EMAIL_SMTP_SERVER, EMAIL_SENDER, EMAIL_PASSWORD, CALENDAR_API_URL]
# if not all(required_vars):
#     raise ValueError("Missing required environment variables in .env file. Required: GROQ_API_KEY, DEEPGRAM_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, BASE_URL")

# # Validate Ngrok URL
# if not BASE_URL.endswith((".ngrok-free.app", ".ngrok.io", ".onrender.com")):
#     logger.warning(f"BASE_URL ({BASE_URL}) does not appear to be a valid URL. Ensure it matches the current session.")

# CHESS_COACH_PROMPT_PREAMBLE = """
# # Chess Coaching Sales Representative Prompt
# ## Identity & Purpose
# You are Priya, a virtual sales representative for 4champz, a leading chess coaching service provider based in Bengaluru, India. We specialize in providing qualified chess coaches to schools across Bangalore. 
# Your primary purpose is to qualify leads who have shown interest in chess coaching opportunities, understand their background and experience, explore potential collaboration as a chess coach for our school programs, handle FAQs, and schedule meetings for both inbound and outbound calls.
# ## Voice & Persona
# ### Personality
# - Sound professional, warm, and conversational—like a knowledgeable chess enthusiast
# - Project genuine interest in learning about their chess journey
# - Maintain an engaging and respectful demeanor throughout the conversation
# - Show respect for their time while staying focused on understanding their suitability for school coaching
# - Convey enthusiasm about the opportunity to shape young minds through chess
# ### Speech Characteristics
# - Use clear, conversational language with natural flow
# - Keep messages under 150 characters when possible
# - Include probing questions to gather detailed information
# - Show genuine interest in their chess background and achievements
# - Use encouraging language when discussing their experience and qualifications
# ## Conversation Flow
# ### Introduction
# 1. For inbound: "Hello {{name}}, this is Priya from 4champz. Do you have 5-10 minutes to discuss chess coaching opportunities in Bangalore?"
# 2. For outbound: "Hello {{name}}, this is Priya from 4champz. I’m reaching out due to your interest. Available to discuss?"
# 3. Follow with: "I’d love to explore your background, answer FAQs like pricing or timings, or assist with reminders if applicable."
# ### FAQs Handling
# - Pricing: "Our coaching fees start at ₹500/hour, varying by experience. Interested in details?"
# - Timings: "Coaching is typically 3-6 PM school hours. Flexible options available—want to discuss?"
# - Services: "We offer structured curricula, training, and school placements. More questions?"
# ### Current Involvement Assessment
# - Location: "Could you confirm your current location in Bangalore?"
# - Involvement: "Are you actively playing or coaching chess?"
# - Availability: "What’s your schedule like, especially afternoons?"
# ### Experience and Background Qualification
# - Chess playing: "What’s your FIDE or All India Chess Federation rating?"
# - Tournaments: "Tell me about your recent tournament participation."
# - Coaching: "Have you coached children before, especially in chess?"
# - Education: "What are your educational qualifications or certifications?"
# ### School Coaching Interest
# - Explain: "We provide coaches to schools across Bangalore with training support."
# - Availability: "Are you free 3-6 PM? How many days weekly?"
# - Age groups: "Comfortable with Classes 1-12? Any preferences?"
# - Support: "We offer training. Interested in a structured curriculum?"
# ### Scheduling
# - If interested: "Let’s schedule a detailed discussion. When are you free this week?"
# - Use check_calendar_availability and book_appointment.
# - Confirm: "Please provide your full name, email, and preferred time."
# ### Close
# - Positive: "Thank you, {{name}}. We’ll send details and a confirmation. Looking forward to it!"
# - End with end_call unless transferred
# ## Response Guidelines
# - Handle FAQs before diving into qualification if asked
# - Use IST timing for scheduling (e.g., today is 03:14 PM IST, Friday, September 19, 2025)
# - Ask one question at a time to avoid overwhelming them
# - Keep responses focused on qualifying their suitability for school coaching
# - Ask location-specific questions about Bangalore areas they can cover
# - Show genuine enthusiasm for their chess achievements and experience
# - Be respectful of their current commitments and time constraints
# - Emphasize the opportunity to impact young minds through chess education
# ## Scenario Handling
# ### Interested Leads
# - Enthusiasm: "Your experience is impressive! Let’s connect you with a rep."
# - Route: Use transfer_call to sales rep.
# ### Support Queries
# - Detect: If "support" or "help" in input, say "Let me route you to our support team."
# - Route: Use transfer_call to support.
# ### Reminders
# - Meeting: "This is a reminder for your demo on [date/time]. Ready to proceed?" (e.g., use current date + 1 day if unspecified)
# - Payment: "This is a payment reminder for ₹500 due by [date]. Settled?" (e.g., use current date + 1 day if unspecified)
# ### For Highly Qualified Candidates
# - Express enthusiasm: "Your tournament experience and rating are impressive! Our partner schools would definitely value someone with your background."
# - Fast-track process: "Given your qualifications, I’d love to expedite our discussion. When would be the best time this week?"
# - Highlight premium opportunities: "With your experience, you’d be perfect for our advanced chess program placements at premium schools."
# ### For Candidates with Limited Formal Experience
# - Explore potential: "While formal ratings are helpful, we also value passion and teaching ability. Tell me about your experience with children or young people."
# - Training emphasis: "We provide comprehensive training to develop skills. Are you excited about growing with our support?"
# - Alternative qualifications: "Have you been involved in chess clubs, online coaching, or informal teaching?"
# ### For Availability Concerns
# - Flexible scheduling: "We can often accommodate different preferences. What times work best for you?"
# - Part-time opportunities: "Many coaches start part-time. Would that interest you?"
# - Location matching: "We’ll match you with convenient schools. Which Bangalore areas are accessible?"
# ### For Candidates Requesting Human Assistance
# - If they want human help or details on compensation/partnerships:
#   - Use transfer_call
#   - Say: "Of course! Let me connect you with our placement manager for details on partnerships and compensation."
# ## Knowledge Base
# ### Caller Info
# - name: {{name}}, email: {{email}}, phone_number: {{phone_number}}, role: {{role}}
# ### 4champz Model
# - Leading chess coaching in Bengaluru, school-focused, training provided
# - Partners with reputed schools, offers part-time/full-time opportunities
# - Focuses on developing young chess talent
# ### Requirements
# - 3-6 PM availability, English/Kannada/Hindi, Bangalore travel
# - Professional attitude, teaching aptitude, school-level chess knowledge
# ### Assessment Criteria
# - Chess playing experience and rating (FIDE/All India Chess Federation)
# - Tournament participation and achievements
# - Prior coaching/teaching experience, especially with children
# - Educational qualifications and chess certifications
# - Language capabilities and communication skills
# - Geographic availability across Bangalore
# - Flexibility with scheduling and age groups
# ## Response Refinement
# - When discussing chess background: "Your chess journey sounds fascinating. Could you tell more about [specific aspect]?"
# - When explaining opportunities: "Let me paint a picture of coaching with our partner schools..."
# - When confirming details: "To confirm—you’re available [availability] and comfortable with [preferences]. Is that accurate?"
# ## Call Management
# ### Available Functions
# - check_calendar_availability: Use for scheduling follow-up meetings
# - book_appointment: Use to confirm scheduled appointments
# - transfer_call: Use when candidate requests human assistance
# - end_call: Use to conclude every conversation
# ## Technical Considerations
# - If calendar delays occur: "I’m checking available slots. This will take a moment."
# - If multiple scheduling needs: "Let’s book your appointment first, then address other questions."
# - Always confirm appointment details before ending: "To confirm, we’re scheduled for [day], [date] at [time IST]. You’ll receive an email."
# ---
# Your goal is to qualify chess coaches for Bangalore schools, ensure they understand and are excited about the opportunity, and maintain 4champz’s professional reputation. Prioritize accurate qualification, scheduling, and enthusiasm across all call types.
# """



# medical_sales_prompt="""
# # Medical Sales Representative Prompt
# ## Identity & Purpose
# You are Sarah, a virtual sales representative for MediShop, a leading medical supplies provider based in Bengaluru, India. We specialize in providing high-quality medical equipment, consumables, and services to clinics, hospitals, and individual practitioners across Bangalore.
# Your primary purpose is to qualify leads who have shown interest in medical supplies, understand their needs and current setup, explore potential partnerships or sales opportunities, handle FAQs, and schedule follow-up meetings for both inbound and outbound calls.

# ## Voice & Persona
# ### Personality
# - Sound professional, empathetic, and knowledgeable—like a trusted healthcare advisor
# - Project genuine interest in understanding their medical supply needs
# - Maintain a courteous and solution-oriented demeanor throughout the conversation
# - Show respect for their time while focusing on their requirements for medical equipment
# - Convey enthusiasm about helping healthcare providers improve patient care through quality supplies

# ### Speech Characteristics
# - Use clear, concise, and professional language with a supportive tone
# - Keep messages under 150 characters when possible
# - Include probing questions to gather detailed information about their needs
# - Show genuine interest in their current setup and challenges
# - Use encouraging language when discussing potential solutions or partnerships

# ## Conversation Flow
# ### Introduction
# 1. For inbound: "Hello {{name}}, this is Sarah from MediShop. Do you have 5-10 minutes to discuss medical supply solutions for your practice?"
# 2. For outbound: "Hello {{name}}, this is Sarah from MediShop. I’m reaching out due to your interest in medical supplies. Available to discuss?"
# 3. Follow with: "I’d love to understand your current needs, answer FAQs like pricing or delivery, or assist with reminders if applicable."

# ### FAQs Handling
# - Pricing: "Our medical supplies start at competitive rates, tailored to your needs. Interested in a detailed quote?"
# - Delivery: "We offer same-day delivery in Bangalore for urgent orders. Want to discuss timelines?"
# - Products: "We provide equipment, consumables, and maintenance services. Any specific needs?"

# ### Current Needs Assessment
# - Location: "Could you confirm your clinic or hospital’s location in Bangalore?"
# - Current Setup: "What medical supplies or equipment are you currently using?"
# - Needs: "Are you looking for specific equipment, like diagnostic tools or consumables?"

# ### Qualification Questions
# - Volume: "What’s your typical monthly usage of medical consumables?"
# - Budget: "Do you have a budget range for new equipment or supplies?"
# - Decision Maker: "Are you the primary decision-maker for purchasing supplies?"
# - Current Suppliers: "Who are your current suppliers, and any challenges with them?"

# ### Sales Opportunity Exploration
# - Explain: "We offer tailored solutions for clinics and hospitals, with training and support."
# - Customization: "Need specific equipment or bulk discounts? We can customize."
# - Support: "We provide maintenance and training. Interested in learning more?"
# - Partnerships: "Interested in a long-term partnership for consistent supply?"

# ### Scheduling
# - If interested: "Let’s schedule a detailed discussion or demo. When are you free this week?"
# - Use check_calendar_availability and book_appointment.
# - Confirm: "Please provide your full name, email, and preferred time."

# ### Close
# - Positive: "Thank you, {{name}}. We’ll send details and a confirmation. Excited to assist!"
# - End with end_call unless transferred

# ## Response Guidelines
# - Handle FAQs before diving into qualification if asked
# - Use IST timing for scheduling (e.g., today is 03:46 PM IST, Tuesday, September 23, 2025)
# - Ask one question at a time to avoid overwhelming them
# - Keep responses focused on qualifying their suitability for MediShop’s offerings
# - Ask location-specific questions about Bangalore areas for delivery logistics
# - Show enthusiasm for solving their supply chain challenges
# - Be respectful of their busy schedules and operational constraints
# - Emphasize the opportunity to enhance patient care with reliable supplies

# ## Scenario Handling
# ### Interested Leads
# - Enthusiasm: "Your needs align perfectly with our offerings! Let’s connect you with a sales rep."
# - Route: Use transfer_call to sales rep.

# ### Support Queries
# - Detect: If "support" or "help" in input, say "Let me route you to our support team."
# - Route: Use transfer_call to support.

# ### Reminders
# - Meeting: "This is a reminder for your demo on [date/time]. Ready to proceed?" (e.g., use current date + 1 day if unspecified)
# - Payment: "This is a payment reminder for your invoice due by [date]. Settled?" (e.g., use current date + 1 day if unspecified)

# ### For High-Volume Buyers
# - Express enthusiasm: "Your usage volume is impressive! We can offer tailored discounts."
# - Fast-track process: "Given your needs, let’s expedite a detailed quote. When’s best?"
# - Highlight premium offerings: "Our premium equipment and bulk deals could be ideal."

# ### For Small Clinics or New Buyers
# - Explore potential: "Even small setups benefit from our flexible plans. Tell me about your needs."
# - Support emphasis: "We provide training and support to ease transitions. Interested?"
# - Alternative solutions: "Interested in starter kits or trial orders?"

# ### For Delivery or Logistics Concerns
# - Flexible scheduling: "We can adjust delivery times to suit you. What works best?"
# - Local support: "We have local teams in Bangalore. Which areas are you in?"
# - Assurance: "Our logistics ensure timely delivery. Want to discuss specifics?"

# ### For Candidates Requesting Human Assistance
# - If they want human help or details on contracts/partnerships:
#   - Use transfer_call
#   - Say: "Of course! Let me connect you with our sales manager for detailed discussions."

# ## Knowledge Base
# ### Caller Info
# - name: {{name}}, email: {{email}}, phone_number: {{phone_number}}, role: {{role}}

# ### MediShop Model
# - Leading medical supplies provider in Bengaluru, serving clinics and hospitals
# - Offers equipment, consumables, maintenance, and training
# - Focuses on reliable, high-quality supplies to improve patient care

# ### Requirements
# - Clear understanding of current supply needs and budget
# - Located in Bangalore with ability to receive deliveries
# - Professional communication and decision-making authority

# ### Assessment Criteria
# - Monthly supply volume and budget
# - Current suppliers and satisfaction levels
# - Specific equipment or consumable needs
# - Decision-making role and authority
# - Language capabilities (English/Kannada/Hindi)
# - Delivery location and logistics preferences

# ## Response Refinement
# - When discussing needs: "Your setup sounds interesting. Could you share more about [specific need]?"
# - When explaining offerings: "Let me share how MediShop can streamline your supply chain..."
# - When confirming details: "To confirm—your needs are [needs] and delivery is to [location]. Correct?"

# ## Call Management
# ### Available Functions
# - check_calendar_availability: Use for scheduling follow-up meetings
# - book_appointment: Use to confirm scheduled appointments
# - transfer_call: Use when candidate requests human assistance
# - end_call: Use to conclude every conversation

# ## Technical Considerations
# - If calendar delays occur: "I’m checking available slots. This will take a moment."
# - If multiple scheduling needs: "Let’s book your appointment first, then address other questions."
# - Always confirm appointment details before ending: "To confirm, we’re scheduled for [day], [date] at [time IST]. You’ll receive an email."

# ---
# Your goal is to qualify leads for medical supply sales, ensure they understand MediShop’s value, and maintain a professional reputation. Prioritize accurate qualification, scheduling, and enthusiasm across all call types.

# """



# hospital_receptionist_prompt="""
# # Hospital Receptionist Prompt
# ## Identity & Purpose
# You are Emma, a virtual receptionist for City Hospital, a premier healthcare facility in Bengaluru, India. We provide comprehensive medical services, including consultations, diagnostics, and surgeries, to patients across Bangalore.
# Your primary purpose is to assist callers with scheduling appointments, answering general inquiries about hospital services, directing calls to appropriate departments, and handling FAQs for both inbound and outbound calls.

# ## Voice & Persona
# ### Personality
# - Sound calm, professional, and empathetic—like a caring healthcare professional
# - Project genuine interest in helping callers with their medical needs
# - Maintain a patient and reassuring demeanor throughout the conversation
# - Show respect for their urgency while addressing their inquiries efficiently
# - Convey confidence in City Hospital’s ability to provide excellent care

# ### Speech Characteristics
# - Use clear, soothing, and professional language with a supportive tone
# - Keep messages under 150 characters when possible
# - Include clarifying questions to understand their needs
# - Show empathy for their health concerns or questions
# - Use reassuring language when addressing inquiries or scheduling

# ## Conversation Flow
# ### Introduction
# 1. For inbound: "Hello {{name}}, this is Emma from City Hospital. How can I assist with your appointment or inquiry today?"
# 2. For outbound: "Hello {{name}}, this is Emma from City Hospital. I’m following up on your inquiry. Available to discuss?"
# 3. Follow with: "I can help schedule appointments, answer questions about services, or connect you to a department."

# ### FAQs Handling
# - Appointment Process: "Appointments can be booked online or by phone. Want to schedule one now?"
# - Services: "We offer consultations, diagnostics, and surgeries. Need details on a specific service?"
# - Visiting Hours: "Visiting hours are 10 AM–8 PM. Need directions or parking info?"

# ### Caller Needs Assessment
# - Location: "Could you confirm if you’re visiting our Bangalore branch?"
# - Purpose: "Are you scheduling an appointment, seeking information, or needing support?"
# - Urgency: "Is this an urgent medical need, or a routine visit?"

# ### Appointment Scheduling
# - Department: "Which department or doctor would you like to see?"
# - Availability: "When are you available for an appointment?"
# - Details: "Please provide your full name, contact details, and preferred time."

# ### Inquiry Handling
# - Explain: "City Hospital offers comprehensive care with top specialists."
# - Specifics: "Need info on specific treatments, like cardiology or orthopedics?"
# - Support: "I can connect you to our patient support team if needed."

# ### Scheduling
# - If scheduling: "Let’s book your appointment. When are you free this week?"
# - Use check_calendar_availability and book_appointment.
# - Confirm: "Please confirm your full name, email, and preferred time."

# ### Close
# - Positive: "Thank you, {{name}}. Your appointment is confirmed, and details will be sent. Wishing you well!"
# - End with end_call unless transferred

# ## Response Guidelines
# - Handle FAQs before diving into scheduling or inquiries if asked
# - Use IST timing for scheduling (e.g., today is 03:46 PM IST, Tuesday, September 23, 2025)
# - Ask one question at a time to avoid overwhelming callers
# - Keep responses focused on assisting with their immediate needs
# - Ask location-specific questions about Bangalore for in-person visits
# - Show empathy for health concerns and urgency
# - Be respectful of their time and potential stress
# - Emphasize City Hospital’s commitment to patient care

# ## Scenario Handling
# ### Urgent Medical Inquiries
# - Urgency: "For emergencies, please visit our ER or call our hotline. Need directions?"
# - Route: Use transfer_call to emergency department if urgent.

# ### Support Queries
# - Detect: If "support" or "complaint" in input, say "Let me connect you to our patient support team."
# - Route: Use transfer_call to support.

# ### Reminders
# - Appointment: "This is a reminder for your appointment on [date/time]. Confirm or reschedule?" (e.g., use current date + 1 day if unspecified)
# - Follow-up: "This is a follow-up for your recent inquiry. Ready to proceed?"

# ### For First-Time Patients
# - Reassurance: "First visits are seamless with our support. Tell me about your needs."
# - Guidance: "We’ll guide you through the process. Need help with registration?"
# - Options: "Interested in a consultation or diagnostic services?"

# ### For Returning Patients
# - History: "Welcome back! Have you visited us before for [specific service]?"
# - Fast-track: "Let’s quickly schedule your next appointment. When’s convenient?"
# - Loyalty: "As a returning patient, we prioritize your care. Any specific needs?"

# ### For Logistical Concerns
# - Flexible scheduling: "We can adjust appointment times. What works for you?"
# - Directions: "We’re located in Bangalore. Need directions to our facility?"
# - Transport: "Need help with parking or transport options?"

# ### For Callers Requesting Human Assistance
# - If they want human help or detailed medical advice:
#   - Use transfer_call
#   - Say: "Let me connect you with our patient coordinator for further assistance."

# ## Knowledge Base
# ### Caller Info
# - name: {{name}}, email: {{email}}, phone_number: {{phone_number}}, role: {{role}}

# ### City Hospital Model
# - Premier healthcare facility in Bengaluru, offering consultations, diagnostics, and surgeries
# - Partners with top specialists and provides patient support
# - Focuses on accessible, high-quality healthcare

# ### Requirements
# - Clear understanding of caller’s medical or appointment needs
# - Located in or able to visit Bangalore
# - Basic contact information for scheduling

# ### Assessment Criteria
# - Purpose of call (appointment, inquiry, support)
# - Preferred department or doctor
# - Urgency of medical needs
# - Contact details and availability
# - Language capabilities (English/Kannada/Hindi)
# - Accessibility to Bangalore facility

# ## Response Refinement
# - When discussing needs: "I understand your concern. Could you share more about [specific need]?"
# - When explaining services: "Let me explain how City Hospital can assist you..."
# - When confirming details: "To confirm—your appointment is for [service] at [time]. Correct?"

# ## Call Management
# ### Available Functions
# - check_calendar_availability: Use for scheduling appointments
# - book_appointment: Use to confirm scheduled appointments
# - transfer_call: Use when caller requests human assistance
# - end_call: Use to conclude every conversation

# ## Technical Considerations
# - If calendar delays occur: "I’m checking available slots. This will take a moment."
# - If multiple scheduling needs: "Let’s book your appointment first, then address other questions."
# - Always confirm appointment details before ending: "To confirm, we’re scheduled for [day], [date] at [time IST]. You’ll receive an email."

# ---
# Your goal is to assist callers efficiently, ensure they feel supported, and maintain City Hospital’s reputation for excellent patient care. Prioritize accurate scheduling, empathy, and clear communication across all call types.

# """



# # Groq LLM setup
# llm = ChatGroq(model_name="llama-3.1-8b-instant")
# # llm = ChatGroq(model_name="groq/compound-mini")

# # Config Manager
# config_manager = InMemoryConfigManager()

# # ADDED for JSON capture with LLM extraction: global in-memory store
# CONVERSATION_STORE: dict = {}  # ADDED for JSON LLM extraction

# # ADDED for JSON capture with LLM extraction: directory for local persistence
# CONVERSATIONS_DIR = Path("conversations")  # ADDED
# CONVERSATIONS_DIR.mkdir(exist_ok=True, parents=True)  # ADDED

# # ADDED n8n: store lead context by call_sid/conversation_id
# LEAD_CONTEXT_STORE: dict = {}  # ADDED n8n


# # Sentiment Analysis Chain (using Groq LLM)
# sentiment_prompt = PromptTemplate(
#     input_variables=["transcript"],
#     template="Analyze the sentiment of this transcript: {transcript}. Return a JSON with 'sentiment' (positive, neutral, negative, angry, confused) and 'tone_score' (1-10, 10 being most positive)."
# )
# sentiment_chain = LLMChain(llm=llm, prompt=sentiment_prompt)

# # Summary Generation Chain (using Groq LLM)
# summary_prompt = PromptTemplate(
#     input_variables=["transcript"],
#     template="Generate a summary of this transcript: {transcript}. Include key points, customer intent, and next actions. Return a JSON with 'summary', 'intent', 'next_actions' (array of strings)."
# )
# summary_chain = LLMChain(llm=llm, prompt=summary_prompt)



# # Send Email Function
# def send_email(to_email: str, subject: str, body: str):
#     msg = MIMEText(body)
#     msg['Subject'] = subject
#     msg['From'] = EMAIL_SENDER
#     msg['To'] = to_email
#     with smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT) as server:
#         server.starttls()  # Added TLS for security
#         server.login(EMAIL_SENDER, EMAIL_PASSWORD)
#         server.sendmail(EMAIL_SENDER, to_email, msg.as_string())
#     logger.info(f"Email sent to {to_email}")

# # Send WhatsApp Summary Function (using Twilio)
# def send_whatsapp(to_phone: str, body: str):
#     client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#     client.messages.create(
#         from_='whatsapp:' + WHATSAPP_SENDER,
#         body=body,
#         to='whatsapp:' + to_phone
#     )
#     logger.info(f"WhatsApp sent to {to_phone}")



# # NEW: Check Calendar Availability
# async def check_calendar_availability(preferred_time: str) -> dict:
#     headers = {"Authorization": f"Bearer {CRM_API_KEY}"}
#     params = {"time": preferred_time, "timezone": "Asia/Kolkata"}
#     async with httpx.AsyncClient() as client:
#         response = await client.get(CALENDAR_API_URL, headers=headers, params=params)
#         if response.status_code == 200:
#             return response.json()
#         logger.error(f"Calendar check failed: {response.text}")
#         return {"available": False, "slots": []}
    


# # NEW: Book Appointment
# async def book_appointment(lead_id: str, name: str, email: str, time: str):
#     payload = {
#         "lead_id": lead_id,
#         "name": name,
#         "email": email,
#         "time": time,
#         "status": "Scheduled"
#     }
#     headers = {"Authorization": f"Bearer {CRM_API_KEY}"}
#     async with httpx.AsyncClient() as client:
#         response = await client.post(f"{CRM_API_URL}/appointments", json=payload, headers=headers)
#         if response.status_code == 200:
#             logger.info(f"Appointment booked for lead {lead_id}")
#             return True
#         logger.error(f"Appointment booking failed: {response.text}")
#         return False


# # NEW: Update CRM Function (placeholder; replace with your CRM API)
# def update_crm(lead_id: str, transcript: str, sentiment: dict, summary: dict, audio_url: str, twilio_audio_url: Optional[str] = None, status: str = "Called", appointment: dict = None):
#     payload = {
#         "lead_id": lead_id,
#         "transcript": transcript,
#         "sentiment": sentiment,
#         "summary": summary,
#         "audio_url": audio_url,
#         "twilio_audio_url": twilio_audio_url,  # NEW: Twilio full call recording
#         "status": status,
#         "appointment": appointment
#     }
#     headers = {"Authorization": f"Bearer {CRM_API_KEY}"}
#     response = requests.post(CRM_API_URL, json=payload, headers=headers)
#     if response.status_code == 200:
#         logger.info(f"CRM updated for lead {lead_id}")
#     else:
#         logger.error(f"CRM update failed: {response.text}")



# # Events Manager to log transcripts
# class ChessEventsManager(events_manager.EventsManager):
#     def __init__(self):
#         super().__init__(subscriptions=[EventType.TRANSCRIPT_COMPLETE])

#     async def handle_event(self, event: Event):
#         if event.type == EventType.TRANSCRIPT_COMPLETE:
#             transcript_complete_event = typing.cast(TranscriptCompleteEvent, event)
#             transcript = transcript_complete_event.transcript.to_string()
#             logger.debug(f"Transcript for conversation {transcript_complete_event.conversation_id}: {transcript}")

#             # NEW: Sentiment analysis
#             sentiment = await sentiment_chain.ainvoke({"transcript": transcript})

#             # NEW: Summary generation
#             summary = await summary_chain.ainvoke({"transcript": transcript})

#             # NEW: Recording storage (using Deepgram audio chunks)
#             audio_path = await save_recording(transcript_complete_event.conversation_id)
#             audio_url = f"{CLOUD_STORAGE_URL}/{os.path.basename(audio_path)}" if CLOUD_STORAGE_URL else audio_path

#             # NEW: Fetch Twilio recording URL if available
#             client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#             recordings = await asyncio.get_event_loop().run_in_executor(
#                 None,
#                 lambda: client.recordings.list(call_sid=transcript_complete_event.conversation_id)
#             )
#             twilio_audio_url = recordings[0].uri if recordings else None  # NEW: Get Twilio recording URL

#             await asyncio.get_event_loop().run_in_executor(
#                 None, 
#                 lambda: update_crm(transcript_complete_event.conversation_id, transcript, sentiment, summary, audio_url, twilio_audio_url=twilio_audio_url)  # Fixed to use audio_url
#             )

#             # NEW: Send summary to customer/management
#             # Assume email and phone from lead context or CRM
#             short_summary = f"Call Summary: {summary['summary'][:100]}... Next steps: {', '.join(summary['next_actions'][:2])}"
#             lead = LEAD_CONTEXT_STORE.get(transcript_complete_event.conversation_id, {})
#             if "email" in lead:
#                 send_email(lead["email"], "Call Summary", short_summary)
#             if "to_phone" in lead:
#                 send_whatsapp(lead["to_phone"], short_summary)

#             webhook_url = os.getenv("TRANSCRIPT_CALLBACK_URL")
#             if webhook_url:
#                 data = {"conversation_id": transcript_complete_event.conversation_id, "user_id": 1, "transcript": transcript}
#                 async with httpx.AsyncClient() as client:
#                     response = await client.post(webhook_url, json=data)
#                     if response.status_code == 200:
#                         logger.info("Transcript sent successfully to webhook")
#                     else:
#                         logger.error(f"Failed to send transcript to webhook: {response.status_code}")
#             # ADDED for JSON capture with LLM extraction: write store JSON to disk
#             try:
#                 convo = CONVERSATION_STORE.get(transcript_complete_event.conversation_id)
#                 if convo:
#                     convo["sentiment"] = sentiment  # NEW
#                     convo["summary"] = summary  # NEW
#                     out_path = CONVERSATIONS_DIR / f"{transcript_complete_event.conversation_id}.json"
#                     with open(out_path, "w", encoding="utf-8") as f:
#                         json.dump(convo, f, ensure_ascii=False, indent=2)
#                     logger.info(f"Wrote JSON summary to {out_path}")
#             except Exception as e:
#                 logger.error(f"Failed to write JSON summary: {e}")


# async def save_recording(conversation_id: str) -> str:
#     # Assume transcriber instance is accessible via a global or passed reference
#     transcriber = None  # Placeholder; should be injected or managed by TelephonyServer
#     if transcriber and hasattr(transcriber, 'audio_buffer') and transcriber.conversation_id == conversation_id:
#         await transcriber._save_audio()
#         audio_path = RECORDINGS_DIR / f"{conversation_id}.wav"
#         return str(audio_path)
#     logger.error(f"No valid transcriber or buffer for conversation {conversation_id}")
#     return ""

# # Custom Agent Config
# class CustomLangchainAgentConfig(LangchainAgentConfig, type="agent_langchain"):
#     initial_message: BaseMessage = BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?")
#     prompt_preamble: str = CHESS_COACH_PROMPT_PREAMBLE
#     model_name: str = "llama-3.1-8b-instant"
#     # model_name: str = "groq/compound-mini"
#     api_key: str = GROQ_API_KEY
#     provider: str = "groq"

# # Custom Langchain Agent
# class CustomLangchainAgent(LangchainAgent):
#     def __init__(self, agent_config: CustomLangchainAgentConfig):
#         logger.debug(f"Initializing CustomLangchainAgent with config: {agent_config}")
#         super().__init__(agent_config=agent_config)
#         self.last_response_time = time.time()
#         self.conversation_state = "initial"
#         self.no_input_count = 0
#         self.user_name = None  # store extracted/confirmed name
#         self.asked_for_name = False  # track if name is requested
#         logger.debug("Initialized CustomLangchainAgent with Groq LLM (llama-3.1-8b-instant)")
#         # ADDED for JSON capture with LLM extraction
#         self.turns = []  # [{"speaker":"user"/"bot","text":..., "ts": epoch_ms}]
#         self.conversation_id_cache = None  # to index the global store
#         self.extracted_slots = {}  # LLM-extracted structured data


#     # ADDED n8n: helper to ensure id
#     def _ensure_conv_id(self, conversation_id: Optional[str]) -> str:
#         if conversation_id and isinstance(conversation_id, str) and conversation_id.strip():
#             return conversation_id
#         return f"unknown_{int(time.time()*1000)}"

#     # ADDED for JSON capture with LLM extraction
#     def _flush_to_disk(self, conversation_id: str):
#         """Write the current conversation JSON to disk immediately."""
#         try:
#             payload = CONVERSATION_STORE.get(conversation_id)
#             if not payload:
#                 return
#             out_path = CONVERSATIONS_DIR / f"{conversation_id}.json"
#             with open(out_path, "w", encoding="utf-8") as f:
#                 json.dump(payload, f, ensure_ascii=False, indent=2)
#             logger.debug(f"Flushed conversation {conversation_id} to {out_path}")
#         except Exception as e:
#             logger.error(f"Flush to disk failed for {conversation_id}: {e}")

#     # ADDED for JSON capture with LLM extraction
#     def _persist_state(self, conversation_id: Optional[str]):
#         conv_id = self._ensure_conv_id(conversation_id)
#         now_ms = int(time.time() * 1000)
#         lead = LEAD_CONTEXT_STORE.get(conv_id, {})  # ADDED n8n
#         payload = {
#             "conversation_id": conv_id,
#             "updated_at": now_ms,
#             "lead": lead,  # ADDED n8n
#             "slots": self.extracted_slots,  # slots are LLM-extracted
#             "turns": self.turns
#         }
#         CONVERSATION_STORE[conv_id] = payload
#         self._flush_to_disk(conv_id)  # ADDED: always flush on persist

#     # ADDED for JSON capture with LLM extraction
#     def _strip_code_fences(self, s: str) -> str:
#         t = (s or "").strip()
#         if t.startswith("```"):
#             end = t.rfind("```")
#             if end > 0:
#                 inner = t[3:end].strip()
#                 if inner.lower().startswith("json"):
#                     inner = inner[4:].strip()
#                 return inner
#         return t

#     # ADDED for JSON capture with LLM extraction
#     async def _extract_slots_with_llm(self, conversation_id: str):
#         """Extract slots with retry logic."""
#         max_retries = 3
#         retry_delay = 2  # seconds

#         for attempt in range(max_retries):
#             try:
#                 # Build a compact transcript string
#                 convo_lines = []
#                 for t in self.turns[-30:]:
#                     role = "User" if t["speaker"] == "user" else "Agent"
#                     text_line = re.sub(r'\s+', ' ', t['text']).strip()
#                     convo_lines.append(f"{role}: {text_line}")
#                 convo_text = "\n".join(convo_lines)

#                 # Instruction for JSON-only schema
#                 schema_instruction = (
#                     "Return ONLY a JSON object with these keys:\n"
#                     "{\n"
#                     '  "location": string|null,\n'
#                     '  "involvement": "playing"|"coaching"|null,\n'
#                     '  "availability": string|null,\n'
#                     '  "age_range": string|null,\n'
#                     '  "languages": string[]|null,\n'
#                     '  "rating": string|null,\n'
#                     '  "tournaments": string|null,\n'
#                     '  "certifications": string|null,\n'
#                     '  "questions": string[]|null,\n'
#                     '  "intent": "interested"|"support"|"reminder"|null\n'
#                     '}\n'
#                     "Infer conservatively. Use null if not explicitly known."
#                 )

#                 prompt = f"{schema_instruction}\n\nConversation:\n{convo_text}\n\nJSON:"

#                 extractor = ChatGroq(model_name="llama-3.1-8b-instant")
#                 resp = await extractor.ainvoke([
#                     {"role": "system", "content": "You extract structured information from conversations."},
#                     {"role": "user", "content": prompt}
#                 ])

#                 # Normalize content
#                 content = None
#                 if hasattr(resp, "content"):
#                     content = resp.content
#                 elif hasattr(resp, "generations"):
#                     try:
#                         content = resp.generations.text
#                     except Exception:
#                         content = str(resp)
#                 else:
#                     content = str(resp)

#                 parsed = None
#                 try:
#                     c = self._strip_code_fences(content)
#                     parsed = json.loads(c)
#                 except Exception:
#                     logger.warning("Primary JSON parse failed; attempting to locate JSON object")
#                     first = content.find("{")
#                     last = content.rfind("}")
#                     if first != -1 and last != -1 and last > first:
#                         snippet = content[first:last+1]
#                         try:
#                             parsed = json.loads(snippet)
#                         except Exception:
#                             parsed = None

#                 if isinstance(parsed, dict):
#                     # normalize keys
#                     for k in ["location","involvement","availability","age_range","languages","rating","tournaments","certifications","questions"]:
#                         if k not in parsed:
#                             parsed[k] = None
#                     # Ensure types
#                     if parsed.get("languages") is not None and not isinstance(parsed["languages"], list):
#                         parsed["languages"] = [str(parsed["languages"])]
#                     if parsed.get("questions") is not None and not isinstance(parsed["questions"], list):
#                         parsed["questions"] = [str(parsed["questions"])]

#                     self.extracted_slots = parsed
#                     self._persist_state(conversation_id)
#                 else:
#                     logger.warning("LLM extraction did not return a dict; keeping previous slots.")
#                     if attempt < max_retries - 1:
#                         await asyncio.sleep(retry_delay)
#                         continue
#                     raise ValueError("Failed to parse valid JSON after retries")

#             except Exception as e:
#                 logger.error(f"Slot extraction failed (attempt {attempt + 1}/{max_retries}): {e}")
#                 if attempt < max_retries - 1:
#                     await asyncio.sleep(retry_delay)
#                     continue
#                 raise  # Re-raise after final attempt

#     async def end_call(self, conversation_id: str):
#         """End the call by returning a TwiML Hangup response."""
#         twiml_response = '<?xml version="1.0" encoding="UTF-8"?><Response><Hangup/></Response>'
#         await self.send_message(BaseMessage(text=twiml_response), conversation_id)  # Use existing send_message to pass TwiML
#         logger.info(f"Call ended for conversation_id: {conversation_id}")

#     async def respond(self, human_input: str, conversation_id: str, is_interrupt: bool = False) -> Tuple[Optional[str], bool]:
#         try:
#             start_time = time.time()

#             if conversation_id and self.conversation_id_cache != conversation_id:
#                 self.conversation_id_cache = conversation_id
#             current_id = self.conversation_id_cache or conversation_id or "unknown"

#             if human_input:
#                 self.turns.append({"speaker": "user", "text": human_input, "ts": int(time.time()*1000)})
#                 if len(self.turns) % 2 == 0:
#                     asyncio.create_task(self._extract_slots_with_llm(current_id))
#                 self._persist_state(current_id)

#             def personalize_response(text: str) -> str:
#                 if self.user_name:
#                     return text.replace("{name}", self.user_name)
#                 external_name = "there"
#                 return text.replace("{name}", external_name)

#             if time.time() - self.last_response_time > 15:
#                 self.no_input_count += 1
#                 logger.warning(f"No transcription for 15s (attempt {self.no_input_count})")
#                 if self.no_input_count >= 3:
#                     bot_text = personalize_response("Trouble connecting. I’ll follow up later. Thank you!")
#                     self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                     self._persist_state(current_id)
#                     await self.end_call(conversation_id)  # New: End the call
#                     return bot_text, True
#                 bot_text = personalize_response("I didn’t catch that. Available to discuss chess coaching?")
#                 self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return bot_text, False

#             normalized = (human_input or "").strip().lower()
#             filler_phrases = {"", "mhmm", "okay", "what", "yes", "no", "a-", "four", "hello", "hi"}
#             if normalized in filler_phrases:
#                 self.no_input_count += 1
#                 logger.debug(f"Filler input (count {self.no_input_count}): '{human_input}'")
#                 if self.no_input_count >= 3:
#                     bot_text = personalize_response("No valid input. I’ll follow up later. Thank you!")
#                     self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                     self._persist_state(current_id)
#                     return bot_text, True
#                 self.last_response_time = start_time
#                 bot_text = personalize_response("Didn’t catch that. Confirm availability?")
#                 self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return bot_text, False

#             gibberish_indicators = ["what is the first time", "first time", "please repeat", "say again"]
#             if any(phrase in normalized for phrase in gibberish_indicators):
#                 self.no_input_count += 1
#                 logger.debug(f"Gibberish input (count {self.no_input_count}): '{human_input}'")
#                 if self.no_input_count >= 3:
#                     bot_text = personalize_response("Trouble connecting. I’ll follow up later. Thank you!")
#                     self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                     self._persist_state(current_id)
#                     return bot_text, True
#                 self.last_response_time = start_time
#                 bot_text = personalize_response("Sorry, repeat or say yes/no if available?")
#                 self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return bot_text, False

#             self.no_input_count = 0

#             if self.asked_for_name and "name is" in normalized:
#                 try:
#                     name_part = human_input.lower().split("name is", 1)[1].strip().split()
#                     self.user_name = name_part[0].capitalize()
#                     logger.debug(f"Extracted user name: {self.user_name}")
#                 except Exception:
#                     self.user_name = None

#             slots = self.extracted_slots
#             intent = slots.get("intent")

#             # FAQ handling
#             if any(q in normalized for q in ["price", "pricing", "cost", "timings", "time", "services"]):
#                 if "price" in normalized or "cost" in normalized:
#                     response = "Our fees start at ₹500/hour, varying by experience. Want more details?"
#                 elif "timings" in normalized or "time" in normalized:
#                     response = "Coaching is 3-6 PM school hours. Flexible options available—discuss?"
#                 elif "services" in normalized:
#                     response = "We offer curricula, training, and school placements. More questions?"
#                 self.last_response_time = start_time
#                 self.turns.append({"speaker": "bot", "text": response, "ts": int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return response, False

#             # NEW: Real-time sentiment-based routing
#             sentiment = await sentiment_chain.ainvoke({"transcript": "\n".join(t["text"] for t in self.turns)})
#             if sentiment["sentiment"] == "angry" or "upset" in normalized:
#                 logger.info("Detected angry tone, routing to calm rep")
#                 bot_text = "I’ll connect you with a calm rep to assist you."
#                 self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return bot_text, True

#             if self.conversation_state == "initial":
#                 if any(word in normalized for word in ["yes", "sure", "okay", "available"]):
#                     self.conversation_state = "background"
#                     response = "Great! Due to your interest, confirm your Bangalore location?"
#                 else:
#                     response = personalize_response("Sorry, misheard. Available to discuss coaching?")
#                 self.last_response_time = start_time
#                 self.turns.append({"speaker": "bot", "text": response, "ts": int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return response, False
#             else:
#                 try:
#                     response, should_end = await asyncio.wait_for(
#                         super().respond(human_input, conversation_id, is_interrupt), timeout=5.0
#                     )
#                 except asyncio.TimeoutError:
#                     fallback_msg = personalize_response("Response delayed. Try again shortly.")
#                     self.turns.append({"speaker": "bot", "text": fallback_msg, "ts": int(time.time()*1000)})
#                     self._persist_state(current_id)
#                     await self.end_call(conversation_id)  # New: End call on timeout
#                     return fallback_msg, True

#                 if response:
#                     response_text = personalize_response(response)
#                     if "location" in response_text.lower():
#                         self.conversation_state = "background"
#                     if any(phrase in response_text.lower() for phrase in ["confirm your full name", "may i have your name"]):
#                         self.asked_for_name = True

#                     if intent == "interested" and "schedule" in response_text.lower():
#                         available_slots = await check_calendar_availability(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
#                         if available_slots["available"]:
#                             bot_text = f"Great! Available slots: {', '.join(available_slots['slots'])}. Provide name, email, and preferred time?"
#                             self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                             self._persist_state(current_id)
#                             return bot_text, False
#                         else:
#                             bot_text = "No slots available now. I’ll follow up. Thank you!"
#                             self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                             self._persist_state(current_id)
#                             await self.end_call(conversation_id)  # New: End the call
#                             return bot_text, True

#                     if intent == "support":
#                         bot_text = "Let me route you to our support team."
#                         self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                         self._persist_state(current_id)
#                         return bot_text, True
#                     elif intent == "interested":
#                         bot_text = "Impressive! Connecting you to a sales rep."
#                         self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                         self._persist_state(current_id)
#                         await self.end_call(conversation_id)  # New: End call after routing
#                         return bot_text, True

#                     self.last_response_time = start_time
#                     self.turns.append({"speaker": "bot", "text": response_text, "ts": int(time.time()*1000)})
#                     if len(self.turns) % 4 == 0:
#                         asyncio.create_task(self._extract_slots_with_llm(current_id))
#                     self._persist_state(current_id)
#                     return response_text, should_end

#                 fallback_msg = personalize_response("Didn’t get that. Tell me more?")
#                 self.last_response_time = start_time
#                 self.turns.append({"speaker": "bot", "text": fallback_msg, "ts": int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return fallback_msg, False

#         except Exception as e:
#             logger.error(f"Error generating response: {str(e)}")
#             fallback_error_msg = "Error occurred. Try again."
#             self.turns.append({"speaker": "bot", "text": fallback_error_msg, "ts": int(time.time()*1000)})
#             current_id = self.conversation_id_cache or conversation_id or "unknown"
#             self._persist_state(current_id)
#             return fallback_error_msg, False
    








# # Custom Deepgram Transcriber with keepalive and chunk logging
# class CustomDeepgramTranscriber(DeepgramTranscriber):
#     def __init__(self, transcriber_config: DeepgramTranscriberConfig):
#         super().__init__(transcriber_config)
#         self.audio_buffer = io.BytesIO()
#         self.conversation_id = None

#     async def process(self, audio_chunk: bytes):
#         logger.debug(f"Processing audio chunk size: {len(audio_chunk)} bytes")
#         if not audio_chunk or len(audio_chunk) == 0:
#             logger.warning("Empty audio chunk - skipping")
#             return None
#         try:
#             async with self.buffer_lock:
#                 if self.conversation_id:
#                     total_size = self.audio_buffer.tell() + len(audio_chunk)
#                     if total_size > 10 * 1024 * 1024:  # 10MB limit
#                         await self._save_audio()
#                     self.audio_buffer.write(audio_chunk)
#             return await super().process(audio_chunk)
#         except Exception as e:
#             logger.error(f"Deepgram process error: {e}")
#             raise
    

#     async def keepalive(self):
#         while True:
#             await asyncio.sleep(10)
#             try:
#                 await super().process(b"\x00" * 160)
#                 logger.debug("Deepgram keepalive sent")
#             except Exception as e:
#                 logger.error(f"Keepalive failed: {e}")
#                 break


#     def set_conversation_id(self, conversation_id: str):
#         if self.conversation_id != conversation_id:
#             if self.audio_buffer.tell() > 0:
#                 asyncio.create_task(self._save_audio())
#             self.conversation_id = conversation_id
#             self.audio_buffer = io.BytesIO()

#     async def _save_audio(self):
#         if self.conversation_id and self.audio_buffer.tell() > 0:
#             self.audio_buffer.seek(0)
#             audio_path = RECORDINGS_DIR / f"{self.conversation_id}.wav"
#             with open(audio_path, 'wb') as f:
#                 f.write(self.audio_buffer.getbuffer())
#             logger.info(f"Saved audio to {audio_path}")
#             self.audio_buffer = io.BytesIO()

# # Custom Agent Factory
# class CustomAgentFactory:
#     def create_agent(self, agent_config: AgentConfig, logger: Optional[logging.Logger] = None) -> BaseAgent:
#         log = logger or globals().get('logger', logging.getLogger(__name__))
#         log.debug(f"Creating agent with config type: {agent_config.type}")
#         if agent_config.type == "agent_langchain":
#             log.debug("Creating CustomLangchainAgent")
#             return CustomLangchainAgent(agent_config=typing.cast(CustomLangchainAgentConfig, agent_config))
#         log.error(f"Invalid agent config type: {agent_config.type}")
#         raise Exception(f"Invalid agent config: {agent_config.type}")

# # Custom Synthesizer Factory
# class CustomSynthesizerFactory:
#     def create_synthesizer(self, synthesizer_config: SynthesizerConfig) -> BaseSynthesizer:
#         logger.debug(f"Creating synthesizer with config: {synthesizer_config}")
#         if isinstance(synthesizer_config, StreamElementsSynthesizerConfig):
#             logger.debug("Creating StreamElementsSynthesizer")
#             return StreamElementsSynthesizer(synthesizer_config)
#         logger.error(f"Invalid synthesizer config type: {synthesizer_config.type}")
#         raise Exception(f"Invalid synthesizer config: {synthesizer_config.type}")

# # FastAPI App
# app = FastAPI()

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     logger.debug("Starting up FastAPI application")
#     logger.debug("Registered routes:")
#     for route in app.routes:
#         methods = getattr(route, "methods", ["WebSocket"])
#         logger.debug(f" - {route.path} ({methods})")
#     yield
#     # ADDED: final sweep to persist any in-memory conversations at shutdown
#     try:
#         for conv_id in list(CONVERSATION_STORE.keys()):
#             out_path = CONVERSATIONS_DIR / f"{conv_id}.json"
#             with open(out_path, "w", encoding="utf-8") as f:
#                 json.dump(CONVERSATION_STORE[conv_id], f, ensure_ascii=False, indent=2)
#         logger.debug("Shutdown flush completed for all conversations")
#     except Exception as e:
#         logger.error(f"Error during shutdown flush: {e}")
#     logger.debug("Shutting down FastAPI application")

# app.router.lifespan_context = lifespan

# # Twilio config
# twilio_config = TwilioConfig(
#     account_sid=TWILIO_ACCOUNT_SID,
#     auth_token=TWILIO_AUTH_TOKEN
# )

# # Synthesizer config (telephone voice output)
# synthesizer_config = StreamElementsSynthesizerConfig.from_telephone_output_device(
#     voice="Brian"
# )

# transcriber_config = DeepgramTranscriberConfig(
#     api_key=DEEPGRAM_API_KEY,
#     model="nova-2-phonecall",
#     language="en",
#     sampling_rate=8000,  # int primitive, not enum
#     audio_encoding="mulaw",  # lowercase string, not enum
#     chunk_size=320,
#     endpointing_config=PunctuationEndpointingConfig(),
#     downsampling=1,
# )

# default_agent_config = LangchainAgentConfig(
#     initial_message=BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"),
#     prompt_preamble=CHESS_COACH_PROMPT_PREAMBLE,
#     model_name="llama-3.1-8b-instant",
#     api_key=GROQ_API_KEY,
#     provider="groq",
# )



# # Telephony Server setup
# telephony_server = TelephonyServer(
#     base_url=BASE_URL,  # your ngrok url
#     config_manager=config_manager,
#     inbound_call_configs=[
#         TwilioInboundCallConfig(
#             url="/inbound_call",
#             twilio_config=twilio_config,
#             agent_config=default_agent_config,  # NEW: Use default for inbound calls
#             synthesizer_config=synthesizer_config,
#             transcriber_config=transcriber_config,  # Use instance
#             twiml_fallback_response='''<?xml version="1.0" encoding="UTF-8"?>
# <Response>
#     <Say>I didn't hear a response. Are you still there? Please say something to continue.</Say>
#     <Pause length="15"/>
#     <Redirect method="POST">/inbound_call</Redirect>
# </Response>''',
#             record=True,
#             status_callback=f"https://{BASE_URL}/call_status",  # NEW: Added for inbound call status
#             status_callback_method="POST",
#             status_callback_event=["completed"]  # Trigger on call completion
#         )
#     ],
#     agent_factory=CustomAgentFactory(),
#     synthesizer_factory=CustomSynthesizerFactory(),
#     events_manager=ChessEventsManager(),
# )

# # Add routes to FastAPI app
# app.include_router(telephony_server.get_router())


# # NEW: Endpoint to handle Twilio call status callbacks for inbound calls
# @app.post("/call_status")
# async def call_status(request: Request):
#     data = await request.json()
#     call_sid = data.get("CallSid")
#     if data.get("CallStatus") == "completed":
#         logger.info(f"Inbound call {call_sid} completed")
#     return {"ok": True}


# # NEW: Endpoint to serve conversation JSON files
# @app.get("/conversations/{call_sid}.json")
# async def get_conversation(call_sid: str):
#     path = CONVERSATIONS_DIR / f"{call_sid}.json"
#     if path.exists():
#         with open(path, "r", encoding="utf-8") as f:
#             return json.load(f)
#     raise HTTPException(status_code=404, detail="Conversation not found")


# # ADDED n8n: request schema for outbound_call
# class OutboundCallRequest(BaseModel):
#     to_phone: str
#     lead: typing.Optional[typing.Dict[str, typing.Any]] = None
#     transcript_callback_url: typing.Optional[str] = None
#     call_type: str = "qualification"
#     agent_type: str = "chess_coach"  # NEW: Added for dynamic agent selection
#     initial_message: typing.Optional[str] = None  # NEW: Allow custom initial message
#     prompt_preamble: typing.Optional[str] = None  # NEW: Allow custom prompt preamble

# # ADDED n8n: normalize to E164 basic
# def normalize_e164(number: str) -> str:
#     n = re.sub(r'\D+', '', number or '')
#     if not n:
#         return number
#     if n.startswith('0'):
#         n = n.lstrip('0')
#     if not n.startswith('+'):
#         if len(n) == 10:
#             n = '+91' + n
#         else:
#             n = '+' + n
#     return n

# # ADDED n8n: HTTP endpoint to start outbound call from n8n
# @app.post("/outbound_call")
# async def outbound_call(req: OutboundCallRequest):
#     try:
#         to_phone = normalize_e164(req.to_phone)
#         if not to_phone or len(to_phone) < 10:
#             raise HTTPException(status_code=400, detail="Invalid phone")

#         # NEW: Create dynamic agent config for outbound call
#         agent_config = LangchainAgentConfig(
#             initial_message=BaseMessage(text=req.initial_message or default_agent_config.initial_message.text),
#             prompt_preamble=req.prompt_preamble or default_agent_config.prompt_preamble,
#             model_name="llama-3.1-8b-instant",
#             api_key=GROQ_API_KEY,
#             provider="groq",
#         )

#         # NEW: Update telephony server with dynamic agent config for this call
#         telephony_server.inbound_call_configs[0].agent_config = agent_config

#         sid = await make_outbound_call(to_phone, req.call_type, req.lead, req.agent_type)
#         lead = req.lead or {}
#         lead["to_phone"] = to_phone
#         lead["agent_type"] = req.agent_type
#         LEAD_CONTEXT_STORE[sid] = lead
#         logger.info(f"Outbound call requested via n8n: SID={sid}, lead={lead}")
#         if req.transcript_callback_url:
#             os.environ["TRANSCRIPT_CALLBACK_URL"] = req.transcript_callback_url
#         return {"ok": True, "call_sid": sid}
#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"/outbound_call failed: {e}")
#         raise HTTPException(status_code=500, detail=str(e))


# # Outbound call helper
# async def make_outbound_call(to_phone: str, call_type: str, lead: dict = None, agent_type: str = "chess_coach"):
#     client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#     twilio_base_url = f"https://{BASE_URL}"
#     initial_message = {
#         "qualification": telephony_server.inbound_call_configs[0].agent_config.initial_message.text,
#         "reminder": f"This is a reminder for your demo on {lead.get('demo_date', time.strftime('%Y-%m-%d %H:%M IST', time.localtime(time.time() + 86400)))}. Ready?",
#         "payment": f"Payment reminder for ₹500 due by {lead.get('due_date', time.strftime('%Y-%m-%d', time.localtime(time.time() + 86400)))}. Settled?"
#     }.get(call_type, telephony_server.inbound_call_configs[0].agent_config.initial_message.text)
#     call = await asyncio.get_event_loop().run_in_executor(
#         None,
#         lambda: client.calls.create(
#             to=to_phone,
#             from_=TWILIO_PHONE_NUMBER,
#             url=f"{twilio_base_url}/inbound_call",
#             status_callback=f"{twilio_base_url}/call_status",
#             status_callback_method="POST",
#             status_callback_event=["initiated", "ringing", "answered", "completed"],
#             record=True,
#             recording_channels="dual",
#         )
#     )
#     logger.info(f"Call initiated: SID={call.sid}, type={call_type}, agent_type={agent_type}")
#     if call.sid not in LEAD_CONTEXT_STORE:
#         LEAD_CONTEXT_STORE[call.sid] = {"to_phone": to_phone, "call_type": call_type, "agent_type": agent_type, **(lead or {})}
#     CONVERSATION_STORE.setdefault(call.sid, {
#         "conversation_id": call.sid,
#         "updated_at": int(time.time()*1000),
#         "lead": LEAD_CONTEXT_STORE.get(call.sid, {}),
#         "slots": {},
#         "turns": [{"speaker": "bot", "text": initial_message, "ts": int(time.time()*1000)}]
#     })
#     return call.sid




# def outbound_scheduler():
#     while True:
#         response = requests.get(CRM_API_URL, headers={"Authorization": f"Bearer {CRM_API_KEY}"})
#         if response.status_code == 200:
#             leads = response.json().get("leads", [])
#             for lead in leads:
#                 if lead.get("status") == "Call Pending":
#                     call_type = lead.get("call_type", "qualification")
#                     agent_type = lead.get("agent_type", "chess_coach")  # NEW: Support agent_type in scheduler
#                     asyncio.run(make_outbound_call(lead["phone"], call_type, lead, agent_type))
#                     update_crm(lead["id"], "", {}, {}, "", status="Calling")
#         time.sleep(300)



# # Main entrypoint (updated to include scheduler)
# if __name__ == "__main__":
#     import uvicorn

#     def run_server():
#         logger.debug("Starting Uvicorn server")
#         uvicorn.run(app, host="0.0.0.0", port=3000)

#     # Start outbound scheduler in a thread
#     scheduler_thread = threading.Thread(target=outbound_scheduler, daemon=True)
#     scheduler_thread.start()

#     run_server()
















# import os
# import logging
# import asyncio
# import httpx
# import typing
# import time
# from typing import Optional, Tuple, Dict, Any
# from fastapi import FastAPI, Request, Response
# from fastapi.logger import logger as fastapi_logger
# from contextlib import asynccontextmanager
# from dotenv import load_dotenv
# from twilio.rest import Client
# from vocode.streaming.telephony.server.base import TelephonyServer, TwilioInboundCallConfig
# from vocode.streaming.models.telephony import TwilioConfig
# from vocode.streaming.models.agent import LangchainAgentConfig, AgentConfig
# from vocode.streaming.agent.langchain_agent import LangchainAgent
# from vocode.streaming.models.message import BaseMessage
# from vocode.streaming.transcriber.deepgram_transcriber import DeepgramTranscriber
# from vocode.streaming.models.transcriber import DeepgramTranscriberConfig, AudioEncoding, PunctuationEndpointingConfig
# from vocode.streaming.synthesizer.stream_elements_synthesizer import StreamElementsSynthesizer
# from vocode.streaming.models.synthesizer import StreamElementsSynthesizerConfig, SynthesizerConfig
# from vocode.streaming.synthesizer.base_synthesizer import BaseSynthesizer
# from vocode.streaming.telephony.config_manager.in_memory_config_manager import InMemoryConfigManager
# from vocode.streaming.agent.base_agent import BaseAgent
# from vocode.streaming.models.events import Event, EventType
# from vocode.streaming.models.transcript import TranscriptCompleteEvent
# from vocode.streaming.utils import events_manager
# from langchain_groq import ChatGroq
# import threading
# import numpy as np

# # ADDED for JSON capture with LLM extraction
# import json  # ADDED for JSON capture with LLM extraction
# import re    # ADDED: general regex utilities
# from pathlib import Path  # ADDED: filesystem-safe paths
# from fastapi import HTTPException  # ADDED n8n
# from pydantic import BaseModel  # ADDED n8n

# # NEW: For sentiment analysis and summaries (using Groq LLM)
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain


# # NEW: For email summaries (simple SMTP)
# import smtplib
# from email.mime.text import MIMEText

# # NEW: For WhatsApp summaries (using Twilio)
# from twilio.rest import Client as TwilioClient

# # NEW: Placeholder CRM API (replace with your CRM, e.g., HubSpot API)
# import requests  # NEW: for CRM API calls


# from pydub import AudioSegment  # NEW: For audio conversion (MP3/WAV)
# import wave  # NEW: For WAV file handling
# import io

# # Configure logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# fastapi_logger.setLevel(logging.DEBUG)

# # Ensure ffmpeg is in PATH
# os.environ['PATH'] += os.pathsep + 'C:\\ffmpeg\\bin'

# load_dotenv()




# # Environment variables
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
# TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
# TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
# BASE_URL = os.getenv("BASE_URL")
# DEBUG_AUDIO = os.getenv("DEBUG_AUDIO", "false").lower() == "true"


# # NEW: Storage directory for recordings
# RECORDINGS_DIR = Path("recordings")
# RECORDINGS_DIR.mkdir(exist_ok=True, parents=True)

# # NEW: Cloud storage URL (e.g., AWS S3 placeholder)
# CLOUD_STORAGE_URL = os.getenv("CLOUD_STORAGE_URL", "https://your-s3-bucket.s3.amazonaws.com/")


# # NEW: CRM environment variables (replace with your CRM details)
# CRM_API_URL = os.getenv("CRM_API_URL", "https://your-crm-api.com/leads")
# CRM_API_KEY = os.getenv("CRM_API_KEY", "your_crm_api_key")
# EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER", "smtp.example.com")
# EMAIL_SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", 587))
# EMAIL_SENDER = os.getenv("EMAIL_SENDER", "priya@4champz.com")
# EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your_email_password")
# CALENDAR_API_URL = os.getenv("CALENDAR_API_URL", "https://your-calendar-api.com/availability")  # NEW: for scheduling

# # NEW: WhatsApp sender number (for summaries)
# WHATSAPP_SENDER = os.getenv("WHATSAPP_SENDER", TWILIO_PHONE_NUMBER)



# # Validate environment variables
# required_vars = [GROQ_API_KEY, DEEPGRAM_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, BASE_URL, CRM_API_URL, CRM_API_KEY, EMAIL_SMTP_SERVER, EMAIL_SENDER, EMAIL_PASSWORD, CALENDAR_API_URL]
# if not all(required_vars):
#     raise ValueError("Missing required environment variables in .env file. Required: GROQ_API_KEY, DEEPGRAM_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, BASE_URL")

# # Validate Ngrok URL
# if not BASE_URL.endswith((".ngrok-free.app", ".ngrok.io", ".onrender.com")):
#     logger.warning(f"BASE_URL ({BASE_URL}) does not appear to be a valid URL. Ensure it matches the current session.")

# CHESS_COACH_PROMPT_PREAMBLE = """
# # Chess Coaching Sales Representative Prompt
# ## Identity & Purpose
# You are Priya, a virtual sales representative for 4champz, a leading chess coaching service provider based in Bengaluru, India. We specialize in providing qualified chess coaches to schools across Bangalore. 
# Your primary purpose is to qualify leads who have shown interest in chess coaching opportunities, understand their background and experience, explore potential collaboration as a chess coach for our school programs, handle FAQs, and schedule meetings for both inbound and outbound calls.
# ## Voice & Persona
# ### Personality
# - Sound professional, warm, and conversational—like a knowledgeable chess enthusiast
# - Project genuine interest in learning about their chess journey
# - Maintain an engaging and respectful demeanor throughout the conversation
# - Show respect for their time while staying focused on understanding their suitability for school coaching
# - Convey enthusiasm about the opportunity to shape young minds through chess
# ### Speech Characteristics
# - Use clear, conversational language with natural flow
# - Keep messages under 150 characters when possible
# - Include probing questions to gather detailed information
# - Show genuine interest in their chess background and achievements
# - Use encouraging language when discussing their experience and qualifications
# ## Conversation Flow
# ### Introduction
# 1. For inbound: "Hello {{name}}, this is Priya from 4champz. Do you have 5-10 minutes to discuss chess coaching opportunities in Bangalore?"
# 2. For outbound: "Hello {{name}}, this is Priya from 4champz. I’m reaching out due to your interest. Available to discuss?"
# 3. Follow with: "I’d love to explore your background, answer FAQs like pricing or timings, or assist with reminders if applicable."
# ### FAQs Handling
# - Pricing: "Our coaching fees start at ₹500/hour, varying by experience. Interested in details?"
# - Timings: "Coaching is typically 3-6 PM school hours. Flexible options available—want to discuss?"
# - Services: "We offer structured curricula, training, and school placements. More questions?"
# ### Current Involvement Assessment
# - Location: "Could you confirm your current location in Bangalore?"
# - Involvement: "Are you actively playing or coaching chess?"
# - Availability: "What’s your schedule like, especially afternoons?"
# ### Experience and Background Qualification
# - Chess playing: "What’s your FIDE or All India Chess Federation rating?"
# - Tournaments: "Tell me about your recent tournament participation."
# - Coaching: "Have you coached children before, especially in chess?"
# - Education: "What are your educational qualifications or certifications?"
# ### School Coaching Interest
# - Explain: "We provide coaches to schools across Bangalore with training support."
# - Availability: "Are you free 3-6 PM? How many days weekly?"
# - Age groups: "Comfortable with Classes 1-12? Any preferences?"
# - Support: "We offer training. Interested in a structured curriculum?"
# ### Scheduling
# - If interested: "Let’s schedule a detailed discussion. When are you free this week?"
# - Use check_calendar_availability and book_appointment.
# - Confirm: "Please provide your full name, email, and preferred time."
# ### Close
# - Positive: "Thank you, {{name}}. We’ll send details and a confirmation. Looking forward to it!"
# - End with end_call unless transferred
# ## Response Guidelines
# - Handle FAQs before diving into qualification if asked
# - Use IST timing for scheduling (e.g., today is 03:14 PM IST, Friday, September 19, 2025)
# - Ask one question at a time to avoid overwhelming them
# - Keep responses focused on qualifying their suitability for school coaching
# - Ask location-specific questions about Bangalore areas they can cover
# - Show genuine enthusiasm for their chess achievements and experience
# - Be respectful of their current commitments and time constraints
# - Emphasize the opportunity to impact young minds through chess education
# ## Scenario Handling
# ### Interested Leads
# - Enthusiasm: "Your experience is impressive! Let’s connect you with a rep."
# - Route: Use transfer_call to sales rep.
# ### Support Queries
# - Detect: If "support" or "help" in input, say "Let me route you to our support team."
# - Route: Use transfer_call to support.
# ### Reminders
# - Meeting: "This is a reminder for your demo on [date/time]. Ready to proceed?" (e.g., use current date + 1 day if unspecified)
# - Payment: "This is a payment reminder for ₹500 due by [date]. Settled?" (e.g., use current date + 1 day if unspecified)
# ### For Highly Qualified Candidates
# - Express enthusiasm: "Your tournament experience and rating are impressive! Our partner schools would definitely value someone with your background."
# - Fast-track process: "Given your qualifications, I’d love to expedite our discussion. When would be the best time this week?"
# - Highlight premium opportunities: "With your experience, you’d be perfect for our advanced chess program placements at premium schools."
# ### For Candidates with Limited Formal Experience
# - Explore potential: "While formal ratings are helpful, we also value passion and teaching ability. Tell me about your experience with children or young people."
# - Training emphasis: "We provide comprehensive training to develop skills. Are you excited about growing with our support?"
# - Alternative qualifications: "Have you been involved in chess clubs, online coaching, or informal teaching?"
# ### For Availability Concerns
# - Flexible scheduling: "We can often accommodate different preferences. What times work best for you?"
# - Part-time opportunities: "Many coaches start part-time. Would that interest you?"
# - Location matching: "We’ll match you with convenient schools. Which Bangalore areas are accessible?"
# ### For Candidates Requesting Human Assistance
# - If they want human help or details on compensation/partnerships:
#   - Use transfer_call
#   - Say: "Of course! Let me connect you with our placement manager for details on partnerships and compensation."
# ## Knowledge Base
# ### Caller Info
# - name: {{name}}, email: {{email}}, phone_number: {{phone_number}}, role: {{role}}
# ### 4champz Model
# - Leading chess coaching in Bengaluru, school-focused, training provided
# - Partners with reputed schools, offers part-time/full-time opportunities
# - Focuses on developing young chess talent
# ### Requirements
# - 3-6 PM availability, English/Kannada/Hindi, Bangalore travel
# - Professional attitude, teaching aptitude, school-level chess knowledge
# ### Assessment Criteria
# - Chess playing experience and rating (FIDE/All India Chess Federation)
# - Tournament participation and achievements
# - Prior coaching/teaching experience, especially with children
# - Educational qualifications and chess certifications
# - Language capabilities and communication skills
# - Geographic availability across Bangalore
# - Flexibility with scheduling and age groups
# ## Response Refinement
# - When discussing chess background: "Your chess journey sounds fascinating. Could you tell more about [specific aspect]?"
# - When explaining opportunities: "Let me paint a picture of coaching with our partner schools..."
# - When confirming details: "To confirm—you’re available [availability] and comfortable with [preferences]. Is that accurate?"
# ## Call Management
# ### Available Functions
# - check_calendar_availability: Use for scheduling follow-up meetings
# - book_appointment: Use to confirm scheduled appointments
# - transfer_call: Use when candidate requests human assistance
# - end_call: Use to conclude every conversation
# ## Technical Considerations
# - If calendar delays occur: "I’m checking available slots. This will take a moment."
# - If multiple scheduling needs: "Let’s book your appointment first, then address other questions."
# - Always confirm appointment details before ending: "To confirm, we’re scheduled for [day], [date] at [time IST]. You’ll receive an email."
# ---
# Your goal is to qualify chess coaches for Bangalore schools, ensure they understand and are excited about the opportunity, and maintain 4champz’s professional reputation. Prioritize accurate qualification, scheduling, and enthusiasm across all call types.
# """



# medical_sales_prompt="""
# # Medical Sales Representative Prompt
# ## Identity & Purpose
# You are Sarah, a virtual sales representative for MediShop, a leading medical supplies provider based in Bengaluru, India. We specialize in providing high-quality medical equipment, consumables, and services to clinics, hospitals, and individual practitioners across Bangalore.
# Your primary purpose is to qualify leads who have shown interest in medical supplies, understand their needs and current setup, explore potential partnerships or sales opportunities, handle FAQs, and schedule follow-up meetings for both inbound and outbound calls.

# ## Voice & Persona
# ### Personality
# - Sound professional, empathetic, and knowledgeable—like a trusted healthcare advisor
# - Project genuine interest in understanding their medical supply needs
# - Maintain a courteous and solution-oriented demeanor throughout the conversation
# - Show respect for their time while focusing on their requirements for medical equipment
# - Convey enthusiasm about helping healthcare providers improve patient care through quality supplies

# ### Speech Characteristics
# - Use clear, concise, and professional language with a supportive tone
# - Keep messages under 150 characters when possible
# - Include probing questions to gather detailed information about their needs
# - Show genuine interest in their current setup and challenges
# - Use encouraging language when discussing potential solutions or partnerships

# ## Conversation Flow
# ### Introduction
# 1. For inbound: "Hello {{name}}, this is Sarah from MediShop. Do you have 5-10 minutes to discuss medical supply solutions for your practice?"
# 2. For outbound: "Hello {{name}}, this is Sarah from MediShop. I’m reaching out due to your interest in medical supplies. Available to discuss?"
# 3. Follow with: "I’d love to understand your current needs, answer FAQs like pricing or delivery, or assist with reminders if applicable."

# ### FAQs Handling
# - Pricing: "Our medical supplies start at competitive rates, tailored to your needs. Interested in a detailed quote?"
# - Delivery: "We offer same-day delivery in Bangalore for urgent orders. Want to discuss timelines?"
# - Products: "We provide equipment, consumables, and maintenance services. Any specific needs?"

# ### Current Needs Assessment
# - Location: "Could you confirm your clinic or hospital’s location in Bangalore?"
# - Current Setup: "What medical supplies or equipment are you currently using?"
# - Needs: "Are you looking for specific equipment, like diagnostic tools or consumables?"

# ### Qualification Questions
# - Volume: "What’s your typical monthly usage of medical consumables?"
# - Budget: "Do you have a budget range for new equipment or supplies?"
# - Decision Maker: "Are you the primary decision-maker for purchasing supplies?"
# - Current Suppliers: "Who are your current suppliers, and any challenges with them?"

# ### Sales Opportunity Exploration
# - Explain: "We offer tailored solutions for clinics and hospitals, with training and support."
# - Customization: "Need specific equipment or bulk discounts? We can customize."
# - Support: "We provide maintenance and training. Interested in learning more?"
# - Partnerships: "Interested in a long-term partnership for consistent supply?"

# ### Scheduling
# - If interested: "Let’s schedule a detailed discussion or demo. When are you free this week?"
# - Use check_calendar_availability and book_appointment.
# - Confirm: "Please provide your full name, email, and preferred time."

# ### Close
# - Positive: "Thank you, {{name}}. We’ll send details and a confirmation. Excited to assist!"
# - End with end_call unless transferred

# ## Response Guidelines
# - Handle FAQs before diving into qualification if asked
# - Use IST timing for scheduling (e.g., today is 03:46 PM IST, Tuesday, September 23, 2025)
# - Ask one question at a time to avoid overwhelming them
# - Keep responses focused on qualifying their suitability for MediShop’s offerings
# - Ask location-specific questions about Bangalore areas for delivery logistics
# - Show enthusiasm for solving their supply chain challenges
# - Be respectful of their busy schedules and operational constraints
# - Emphasize the opportunity to enhance patient care with reliable supplies

# ## Scenario Handling
# ### Interested Leads
# - Enthusiasm: "Your needs align perfectly with our offerings! Let’s connect you with a sales rep."
# - Route: Use transfer_call to sales rep.

# ### Support Queries
# - Detect: If "support" or "help" in input, say "Let me route you to our support team."
# - Route: Use transfer_call to support.

# ### Reminders
# - Meeting: "This is a reminder for your demo on [date/time]. Ready to proceed?" (e.g., use current date + 1 day if unspecified)
# - Payment: "This is a payment reminder for your invoice due by [date]. Settled?" (e.g., use current date + 1 day if unspecified)

# ### For High-Volume Buyers
# - Express enthusiasm: "Your usage volume is impressive! We can offer tailored discounts."
# - Fast-track process: "Given your needs, let’s expedite a detailed quote. When’s best?"
# - Highlight premium offerings: "Our premium equipment and bulk deals could be ideal."

# ### For Small Clinics or New Buyers
# - Explore potential: "Even small setups benefit from our flexible plans. Tell me about your needs."
# - Support emphasis: "We provide training and support to ease transitions. Interested?"
# - Alternative solutions: "Interested in starter kits or trial orders?"

# ### For Delivery or Logistics Concerns
# - Flexible scheduling: "We can adjust delivery times to suit you. What works best?"
# - Local support: "We have local teams in Bangalore. Which areas are you in?"
# - Assurance: "Our logistics ensure timely delivery. Want to discuss specifics?"

# ### For Candidates Requesting Human Assistance
# - If they want human help or details on contracts/partnerships:
#   - Use transfer_call
#   - Say: "Of course! Let me connect you with our sales manager for detailed discussions."

# ## Knowledge Base
# ### Caller Info
# - name: {{name}}, email: {{email}}, phone_number: {{phone_number}}, role: {{role}}

# ### MediShop Model
# - Leading medical supplies provider in Bengaluru, serving clinics and hospitals
# - Offers equipment, consumables, maintenance, and training
# - Focuses on reliable, high-quality supplies to improve patient care

# ### Requirements
# - Clear understanding of current supply needs and budget
# - Located in Bangalore with ability to receive deliveries
# - Professional communication and decision-making authority

# ### Assessment Criteria
# - Monthly supply volume and budget
# - Current suppliers and satisfaction levels
# - Specific equipment or consumable needs
# - Decision-making role and authority
# - Language capabilities (English/Kannada/Hindi)
# - Delivery location and logistics preferences

# ## Response Refinement
# - When discussing needs: "Your setup sounds interesting. Could you share more about [specific need]?"
# - When explaining offerings: "Let me share how MediShop can streamline your supply chain..."
# - When confirming details: "To confirm—your needs are [needs] and delivery is to [location]. Correct?"

# ## Call Management
# ### Available Functions
# - check_calendar_availability: Use for scheduling follow-up meetings
# - book_appointment: Use to confirm scheduled appointments
# - transfer_call: Use when candidate requests human assistance
# - end_call: Use to conclude every conversation

# ## Technical Considerations
# - If calendar delays occur: "I’m checking available slots. This will take a moment."
# - If multiple scheduling needs: "Let’s book your appointment first, then address other questions."
# - Always confirm appointment details before ending: "To confirm, we’re scheduled for [day], [date] at [time IST]. You’ll receive an email."

# ---
# Your goal is to qualify leads for medical supply sales, ensure they understand MediShop’s value, and maintain a professional reputation. Prioritize accurate qualification, scheduling, and enthusiasm across all call types.

# """



# hospital_receptionist_prompt="""
# # Hospital Receptionist Prompt
# ## Identity & Purpose
# You are Emma, a virtual receptionist for City Hospital, a premier healthcare facility in Bengaluru, India. We provide comprehensive medical services, including consultations, diagnostics, and surgeries, to patients across Bangalore.
# Your primary purpose is to assist callers with scheduling appointments, answering general inquiries about hospital services, directing calls to appropriate departments, and handling FAQs for both inbound and outbound calls.

# ## Voice & Persona
# ### Personality
# - Sound calm, professional, and empathetic—like a caring healthcare professional
# - Project genuine interest in helping callers with their medical needs
# - Maintain a patient and reassuring demeanor throughout the conversation
# - Show respect for their urgency while addressing their inquiries efficiently
# - Convey confidence in City Hospital’s ability to provide excellent care

# ### Speech Characteristics
# - Use clear, soothing, and professional language with a supportive tone
# - Keep messages under 150 characters when possible
# - Include clarifying questions to understand their needs
# - Show empathy for their health concerns or questions
# - Use reassuring language when addressing inquiries or scheduling

# ## Conversation Flow
# ### Introduction
# 1. For inbound: "Hello {{name}}, this is Emma from City Hospital. How can I assist with your appointment or inquiry today?"
# 2. For outbound: "Hello {{name}}, this is Emma from City Hospital. I’m following up on your inquiry. Available to discuss?"
# 3. Follow with: "I can help schedule appointments, answer questions about services, or connect you to a department."

# ### FAQs Handling
# - Appointment Process: "Appointments can be booked online or by phone. Want to schedule one now?"
# - Services: "We offer consultations, diagnostics, and surgeries. Need details on a specific service?"
# - Visiting Hours: "Visiting hours are 10 AM–8 PM. Need directions or parking info?"

# ### Caller Needs Assessment
# - Location: "Could you confirm if you’re visiting our Bangalore branch?"
# - Purpose: "Are you scheduling an appointment, seeking information, or needing support?"
# - Urgency: "Is this an urgent medical need, or a routine visit?"

# ### Appointment Scheduling
# - Department: "Which department or doctor would you like to see?"
# - Availability: "When are you available for an appointment?"
# - Details: "Please provide your full name, contact details, and preferred time."

# ### Inquiry Handling
# - Explain: "City Hospital offers comprehensive care with top specialists."
# - Specifics: "Need info on specific treatments, like cardiology or orthopedics?"
# - Support: "I can connect you to our patient support team if needed."

# ### Scheduling
# - If scheduling: "Let’s book your appointment. When are you free this week?"
# - Use check_calendar_availability and book_appointment.
# - Confirm: "Please confirm your full name, email, and preferred time."

# ### Close
# - Positive: "Thank you, {{name}}. Your appointment is confirmed, and details will be sent. Wishing you well!"
# - End with end_call unless transferred

# ## Response Guidelines
# - Handle FAQs before diving into scheduling or inquiries if asked
# - Use IST timing for scheduling (e.g., today is 03:46 PM IST, Tuesday, September 23, 2025)
# - Ask one question at a time to avoid overwhelming callers
# - Keep responses focused on assisting with their immediate needs
# - Ask location-specific questions about Bangalore for in-person visits
# - Show empathy for health concerns and urgency
# - Be respectful of their time and potential stress
# - Emphasize City Hospital’s commitment to patient care

# ## Scenario Handling
# ### Urgent Medical Inquiries
# - Urgency: "For emergencies, please visit our ER or call our hotline. Need directions?"
# - Route: Use transfer_call to emergency department if urgent.

# ### Support Queries
# - Detect: If "support" or "complaint" in input, say "Let me connect you to our patient support team."
# - Route: Use transfer_call to support.

# ### Reminders
# - Appointment: "This is a reminder for your appointment on [date/time]. Confirm or reschedule?" (e.g., use current date + 1 day if unspecified)
# - Follow-up: "This is a follow-up for your recent inquiry. Ready to proceed?"

# ### For First-Time Patients
# - Reassurance: "First visits are seamless with our support. Tell me about your needs."
# - Guidance: "We’ll guide you through the process. Need help with registration?"
# - Options: "Interested in a consultation or diagnostic services?"

# ### For Returning Patients
# - History: "Welcome back! Have you visited us before for [specific service]?"
# - Fast-track: "Let’s quickly schedule your next appointment. When’s convenient?"
# - Loyalty: "As a returning patient, we prioritize your care. Any specific needs?"

# ### For Logistical Concerns
# - Flexible scheduling: "We can adjust appointment times. What works for you?"
# - Directions: "We’re located in Bangalore. Need directions to our facility?"
# - Transport: "Need help with parking or transport options?"

# ### For Callers Requesting Human Assistance
# - If they want human help or detailed medical advice:
#   - Use transfer_call
#   - Say: "Let me connect you with our patient coordinator for further assistance."

# ## Knowledge Base
# ### Caller Info
# - name: {{name}}, email: {{email}}, phone_number: {{phone_number}}, role: {{role}}

# ### City Hospital Model
# - Premier healthcare facility in Bengaluru, offering consultations, diagnostics, and surgeries
# - Partners with top specialists and provides patient support
# - Focuses on accessible, high-quality healthcare

# ### Requirements
# - Clear understanding of caller’s medical or appointment needs
# - Located in or able to visit Bangalore
# - Basic contact information for scheduling

# ### Assessment Criteria
# - Purpose of call (appointment, inquiry, support)
# - Preferred department or doctor
# - Urgency of medical needs
# - Contact details and availability
# - Language capabilities (English/Kannada/Hindi)
# - Accessibility to Bangalore facility

# ## Response Refinement
# - When discussing needs: "I understand your concern. Could you share more about [specific need]?"
# - When explaining services: "Let me explain how City Hospital can assist you..."
# - When confirming details: "To confirm—your appointment is for [service] at [time]. Correct?"

# ## Call Management
# ### Available Functions
# - check_calendar_availability: Use for scheduling appointments
# - book_appointment: Use to confirm scheduled appointments
# - transfer_call: Use when caller requests human assistance
# - end_call: Use to conclude every conversation

# ## Technical Considerations
# - If calendar delays occur: "I’m checking available slots. This will take a moment."
# - If multiple scheduling needs: "Let’s book your appointment first, then address other questions."
# - Always confirm appointment details before ending: "To confirm, we’re scheduled for [day], [date] at [time IST]. You’ll receive an email."

# ---
# Your goal is to assist callers efficiently, ensure they feel supported, and maintain City Hospital’s reputation for excellent patient care. Prioritize accurate scheduling, empathy, and clear communication across all call types.

# """



# # Groq LLM setup
# llm = ChatGroq(model_name="llama-3.1-8b-instant")
# # llm = ChatGroq(model_name="groq/compound-mini")

# # Config Manager
# config_manager = InMemoryConfigManager()
# shared_config_manager = InMemoryConfigManager()  # CHANGED

# # ADDED for JSON capture with LLM extraction: global in-memory store
# CONVERSATION_STORE: dict = {}  # ADDED for JSON LLM extraction

# # ADDED for JSON capture with LLM extraction: directory for local persistence
# CONVERSATIONS_DIR = Path("conversations")  # ADDED
# CONVERSATIONS_DIR.mkdir(exist_ok=True, parents=True)  # ADDED

# # ADDED n8n: store lead context by call_sid/conversation_id
# LEAD_CONTEXT_STORE: dict = {}  # ADDED n8n


# # Sentiment Analysis Chain (using Groq LLM)
# sentiment_prompt = PromptTemplate(
#     input_variables=["transcript"],
#     template="Analyze the sentiment of this transcript: {transcript}. Return a JSON with 'sentiment' (positive, neutral, negative, angry, confused) and 'tone_score' (1-10, 10 being most positive)."
# )
# sentiment_chain = LLMChain(llm=llm, prompt=sentiment_prompt)

# # Summary Generation Chain (using Groq LLM)
# summary_prompt = PromptTemplate(
#     input_variables=["transcript"],
#     template="Generate a summary of this transcript: {transcript}. Include key points, customer intent, and next actions. Return a JSON with 'summary', 'intent', 'next_actions' (array of strings)."
# )
# summary_chain = LLMChain(llm=llm, prompt=summary_prompt)



# # Send Email Function
# def send_email(to_email: str, subject: str, body: str):
#     msg = MIMEText(body)
#     msg['Subject'] = subject
#     msg['From'] = EMAIL_SENDER
#     msg['To'] = to_email
#     with smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT) as server:
#         server.starttls()  # Added TLS for security
#         server.login(EMAIL_SENDER, EMAIL_PASSWORD)
#         server.sendmail(EMAIL_SENDER, to_email, msg.as_string())
#     logger.info(f"Email sent to {to_email}")

# # Send WhatsApp Summary Function (using Twilio)
# def send_whatsapp(to_phone: str, body: str):
#     client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#     client.messages.create(
#         from_='whatsapp:' + WHATSAPP_SENDER,
#         body=body,
#         to='whatsapp:' + to_phone
#     )
#     logger.info(f"WhatsApp sent to {to_phone}")



# # NEW: Check Calendar Availability
# async def check_calendar_availability(preferred_time: str) -> dict:
#     headers = {"Authorization": f"Bearer {CRM_API_KEY}"}
#     params = {"time": preferred_time, "timezone": "Asia/Kolkata"}
#     async with httpx.AsyncClient() as client:
#         response = await client.get(CALENDAR_API_URL, headers=headers, params=params)
#         if response.status_code == 200:
#             return response.json()
#         logger.error(f"Calendar check failed: {response.text}")
#         return {"available": False, "slots": []}
    


# # NEW: Book Appointment
# async def book_appointment(lead_id: str, name: str, email: str, time: str):
#     payload = {
#         "lead_id": lead_id,
#         "name": name,
#         "email": email,
#         "time": time,
#         "status": "Scheduled"
#     }
#     headers = {"Authorization": f"Bearer {CRM_API_KEY}"}
#     async with httpx.AsyncClient() as client:
#         response = await client.post(f"{CRM_API_URL}/appointments", json=payload, headers=headers)
#         if response.status_code == 200:
#             logger.info(f"Appointment booked for lead {lead_id}")
#             return True
#         logger.error(f"Appointment booking failed: {response.text}")
#         return False


# # NEW: Update CRM Function (placeholder; replace with your CRM API)
# def update_crm(lead_id: str, transcript: str, sentiment: dict, summary: dict, audio_url: str, twilio_audio_url: Optional[str] = None, status: str = "Called", appointment: dict = None):
#     payload = {
#         "lead_id": lead_id,
#         "transcript": transcript,
#         "sentiment": sentiment,
#         "summary": summary,
#         "audio_url": audio_url,
#         "twilio_audio_url": twilio_audio_url,  # NEW: Twilio full call recording
#         "status": status,
#         "appointment": appointment
#     }
#     headers = {"Authorization": f"Bearer {CRM_API_KEY}"}
#     response = requests.post(CRM_API_URL, json=payload, headers=headers)
#     if response.status_code == 200:
#         logger.info(f"CRM updated for lead {lead_id}")
#     else:
#         logger.error(f"CRM update failed: {response.text}")



# # Events Manager to log transcripts
# class ChessEventsManager(events_manager.EventsManager):
#     def __init__(self):
#         super().__init__(subscriptions=[EventType.TRANSCRIPT_COMPLETE])

#     async def handle_event(self, event: Event):
#         if event.type == EventType.TRANSCRIPT_COMPLETE:
#             transcript_complete_event = typing.cast(TranscriptCompleteEvent, event)
#             transcript = transcript_complete_event.transcript.to_string()
#             logger.debug(f"Transcript for conversation {transcript_complete_event.conversation_id}: {transcript}")

#             # NEW: Sentiment analysis
#             sentiment = await sentiment_chain.ainvoke({"transcript": transcript})

#             # NEW: Summary generation
#             summary = await summary_chain.ainvoke({"transcript": transcript})

#             # NEW: Recording storage (using Deepgram audio chunks)
#             audio_path = await save_recording(transcript_complete_event.conversation_id)
#             audio_url = f"{CLOUD_STORAGE_URL}/{os.path.basename(audio_path)}" if CLOUD_STORAGE_URL else audio_path

#             # NEW: Fetch Twilio recording URL if available
#             client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#             recordings = await asyncio.get_event_loop().run_in_executor(
#                 None,
#                 lambda: client.recordings.list(call_sid=transcript_complete_event.conversation_id)
#             )
#             twilio_audio_url = recordings[0].uri if recordings else None  # NEW: Get Twilio recording URL

#             await asyncio.get_event_loop().run_in_executor(
#                 None, 
#                 lambda: update_crm(transcript_complete_event.conversation_id, transcript, sentiment, summary, audio_url, twilio_audio_url=twilio_audio_url)  # Fixed to use audio_url
#             )

#             # NEW: Send summary to customer/management
#             # Assume email and phone from lead context or CRM
#             short_summary = f"Call Summary: {summary['summary'][:100]}... Next steps: {', '.join(summary['next_actions'][:2])}"
#             lead = LEAD_CONTEXT_STORE.get(transcript_complete_event.conversation_id, {})
#             if "email" in lead:
#                 send_email(lead["email"], "Call Summary", short_summary)
#             if "to_phone" in lead:
#                 send_whatsapp(lead["to_phone"], short_summary)

#             webhook_url = os.getenv("TRANSCRIPT_CALLBACK_URL")
#             if webhook_url:
#                 data = {"conversation_id": transcript_complete_event.conversation_id, "user_id": 1, "transcript": transcript}
#                 async with httpx.AsyncClient() as client:
#                     response = await client.post(webhook_url, json=data)
#                     if response.status_code == 200:
#                         logger.info("Transcript sent successfully to webhook")
#                     else:
#                         logger.error(f"Failed to send transcript to webhook: {response.status_code}")
#             # ADDED for JSON capture with LLM extraction: write store JSON to disk
#             try:
#                 convo = CONVERSATION_STORE.get(transcript_complete_event.conversation_id)
#                 if convo:
#                     convo["sentiment"] = sentiment  # NEW
#                     convo["summary"] = summary  # NEW
#                     out_path = CONVERSATIONS_DIR / f"{transcript_complete_event.conversation_id}.json"
#                     with open(out_path, "w", encoding="utf-8") as f:
#                         json.dump(convo, f, ensure_ascii=False, indent=2)
#                     logger.info(f"Wrote JSON summary to {out_path}")
#             except Exception as e:
#                 logger.error(f"Failed to write JSON summary: {e}")


# async def save_recording(conversation_id: str) -> str:
#     # Assume transcriber instance is accessible via a global or passed reference
#     transcriber = None  # Placeholder; should be injected or managed by TelephonyServer
#     if transcriber and hasattr(transcriber, 'audio_buffer') and transcriber.conversation_id == conversation_id:
#         await transcriber._save_audio()
#         audio_path = RECORDINGS_DIR / f"{conversation_id}.wav"
#         return str(audio_path)
#     logger.error(f"No valid transcriber or buffer for conversation {conversation_id}")
#     return ""

# # Custom Agent Config
# class CustomLangchainAgentConfig(LangchainAgentConfig, type="agent_langchain"):
#     initial_message: BaseMessage = BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?")
#     prompt_preamble: str = CHESS_COACH_PROMPT_PREAMBLE
#     model_name: str = "llama-3.1-8b-instant"
#     # model_name: str = "groq/compound-mini"
#     api_key: str = GROQ_API_KEY
#     provider: str = "groq"

# # Custom Langchain Agent
# class CustomLangchainAgent(LangchainAgent):
#     def __init__(self, agent_config: CustomLangchainAgentConfig):
#         logger.debug(f"Initializing CustomLangchainAgent with config: {agent_config}")
#         super().__init__(agent_config=agent_config)
#         self.last_response_time = time.time()
#         self.conversation_state = "initial"
#         self.no_input_count = 0
#         self.user_name = None  # store extracted/confirmed name
#         self.asked_for_name = False  # track if name is requested
#         logger.debug("Initialized CustomLangchainAgent with Groq LLM (llama-3.1-8b-instant)")
#         # ADDED for JSON capture with LLM extraction
#         self.turns = []  # [{"speaker":"user"/"bot","text":..., "ts": epoch_ms}]
#         self.conversation_id_cache = None  # to index the global store
#         self.extracted_slots = {}  # LLM-extracted structured data


#     # ADDED n8n: helper to ensure id
#     def _ensure_conv_id(self, conversation_id: Optional[str]) -> str:
#         if conversation_id and isinstance(conversation_id, str) and conversation_id.strip():
#             return conversation_id
#         return f"unknown_{int(time.time()*1000)}"

#     # ADDED for JSON capture with LLM extraction
#     def _flush_to_disk(self, conversation_id: str):
#         """Write the current conversation JSON to disk immediately."""
#         try:
#             payload = CONVERSATION_STORE.get(conversation_id)
#             if not payload:
#                 return
#             out_path = CONVERSATIONS_DIR / f"{conversation_id}.json"
#             with open(out_path, "w", encoding="utf-8") as f:
#                 json.dump(payload, f, ensure_ascii=False, indent=2)
#             logger.debug(f"Flushed conversation {conversation_id} to {out_path}")
#         except Exception as e:
#             logger.error(f"Flush to disk failed for {conversation_id}: {e}")

#     # ADDED for JSON capture with LLM extraction
#     def _persist_state(self, conversation_id: Optional[str]):
#         conv_id = self._ensure_conv_id(conversation_id)
#         now_ms = int(time.time() * 1000)
#         lead = LEAD_CONTEXT_STORE.get(conv_id, {})  # ADDED n8n
#         payload = {
#             "conversation_id": conv_id,
#             "updated_at": now_ms,
#             "lead": lead,  # ADDED n8n
#             "slots": self.extracted_slots,  # slots are LLM-extracted
#             "turns": self.turns
#         }
#         CONVERSATION_STORE[conv_id] = payload
#         self._flush_to_disk(conv_id)  # ADDED: always flush on persist

#     # ADDED for JSON capture with LLM extraction
#     def _strip_code_fences(self, s: str) -> str:
#         t = (s or "").strip()
#         if t.startswith("```"):
#             end = t.rfind("```")
#             if end > 0:
#                 inner = t[3:end].strip()
#                 if inner.lower().startswith("json"):
#                     inner = inner[4:].strip()
#                 return inner
#         return t

#     # ADDED for JSON capture with LLM extraction
#     async def _extract_slots_with_llm(self, conversation_id: str):
#         """Extract slots with retry logic."""
#         max_retries = 3
#         retry_delay = 2  # seconds

#         for attempt in range(max_retries):
#             try:
#                 # Build a compact transcript string
#                 convo_lines = []
#                 for t in self.turns[-30:]:
#                     role = "User" if t["speaker"] == "user" else "Agent"
#                     text_line = re.sub(r'\s+', ' ', t['text']).strip()
#                     convo_lines.append(f"{role}: {text_line}")
#                 convo_text = "\n".join(convo_lines)

#                 # Instruction for JSON-only schema
#                 schema_instruction = (
#                     "Return ONLY a JSON object with these keys:\n"
#                     "{\n"
#                     '  "location": string|null,\n'
#                     '  "involvement": "playing"|"coaching"|null,\n'
#                     '  "availability": string|null,\n'
#                     '  "age_range": string|null,\n'
#                     '  "languages": string[]|null,\n'
#                     '  "rating": string|null,\n'
#                     '  "tournaments": string|null,\n'
#                     '  "certifications": string|null,\n'
#                     '  "questions": string[]|null,\n'
#                     '  "intent": "interested"|"support"|"reminder"|null\n'
#                     '}\n'
#                     "Infer conservatively. Use null if not explicitly known."
#                 )

#                 prompt = f"{schema_instruction}\n\nConversation:\n{convo_text}\n\nJSON:"

#                 extractor = ChatGroq(model_name="llama-3.1-8b-instant")
#                 resp = await extractor.ainvoke([
#                     {"role": "system", "content": "You extract structured information from conversations."},
#                     {"role": "user", "content": prompt}
#                 ])

#                 # Normalize content
#                 content = None
#                 if hasattr(resp, "content"):
#                     content = resp.content
#                 elif hasattr(resp, "generations"):
#                     try:
#                         content = resp.generations.text
#                     except Exception:
#                         content = str(resp)
#                 else:
#                     content = str(resp)

#                 parsed = None
#                 try:
#                     c = self._strip_code_fences(content)
#                     parsed = json.loads(c)
#                 except Exception:
#                     logger.warning("Primary JSON parse failed; attempting to locate JSON object")
#                     first = content.find("{")
#                     last = content.rfind("}")
#                     if first != -1 and last != -1 and last > first:
#                         snippet = content[first:last+1]
#                         try:
#                             parsed = json.loads(snippet)
#                         except Exception:
#                             parsed = None

#                 if isinstance(parsed, dict):
#                     # normalize keys
#                     for k in ["location","involvement","availability","age_range","languages","rating","tournaments","certifications","questions"]:
#                         if k not in parsed:
#                             parsed[k] = None
#                     # Ensure types
#                     if parsed.get("languages") is not None and not isinstance(parsed["languages"], list):
#                         parsed["languages"] = [str(parsed["languages"])]
#                     if parsed.get("questions") is not None and not isinstance(parsed["questions"], list):
#                         parsed["questions"] = [str(parsed["questions"])]

#                     self.extracted_slots = parsed
#                     self._persist_state(conversation_id)
#                 else:
#                     logger.warning("LLM extraction did not return a dict; keeping previous slots.")
#                     if attempt < max_retries - 1:
#                         await asyncio.sleep(retry_delay)
#                         continue
#                     raise ValueError("Failed to parse valid JSON after retries")

#             except Exception as e:
#                 logger.error(f"Slot extraction failed (attempt {attempt + 1}/{max_retries}): {e}")
#                 if attempt < max_retries - 1:
#                     await asyncio.sleep(retry_delay)
#                     continue
#                 raise  # Re-raise after final attempt

#     async def end_call(self, conversation_id: str):
#         """End the call by returning a TwiML Hangup response."""
#         twiml_response = '<?xml version="1.0" encoding="UTF-8"?><Response><Hangup/></Response>'
#         await self.send_message(BaseMessage(text=twiml_response), conversation_id)  # Use existing send_message to pass TwiML
#         logger.info(f"Call ended for conversation_id: {conversation_id}")

#     async def respond(self, human_input: str, conversation_id: str, is_interrupt: bool = False) -> Tuple[Optional[str], bool]:
#         try:
#             start_time = time.time()

#             if conversation_id and self.conversation_id_cache != conversation_id:
#                 self.conversation_id_cache = conversation_id
#             current_id = self.conversation_id_cache or conversation_id or "unknown"

#             if human_input:
#                 self.turns.append({"speaker": "user", "text": human_input, "ts": int(time.time()*1000)})
#                 if len(self.turns) % 2 == 0:
#                     asyncio.create_task(self._extract_slots_with_llm(current_id))
#                 self._persist_state(current_id)

#             def personalize_response(text: str) -> str:
#                 if self.user_name:
#                     return text.replace("{name}", self.user_name)
#                 external_name = "there"
#                 return text.replace("{name}", external_name)

#             if time.time() - self.last_response_time > 15:
#                 self.no_input_count += 1
#                 logger.warning(f"No transcription for 15s (attempt {self.no_input_count})")
#                 if self.no_input_count >= 3:
#                     bot_text = personalize_response("Trouble connecting. I’ll follow up later. Thank you!")
#                     self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                     self._persist_state(current_id)
#                     await self.end_call(conversation_id)  # New: End the call
#                     return bot_text, True
#                 bot_text = personalize_response("I didn’t catch that. Available to discuss chess coaching?")
#                 self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return bot_text, False

#             normalized = (human_input or "").strip().lower()
#             filler_phrases = {"", "mhmm", "okay", "what", "yes", "no", "a-", "four", "hello", "hi"}
#             if normalized in filler_phrases:
#                 self.no_input_count += 1
#                 logger.debug(f"Filler input (count {self.no_input_count}): '{human_input}'")
#                 if self.no_input_count >= 3:
#                     bot_text = personalize_response("No valid input. I’ll follow up later. Thank you!")
#                     self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                     self._persist_state(current_id)
#                     return bot_text, True
#                 self.last_response_time = start_time
#                 bot_text = personalize_response("Didn’t catch that. Confirm availability?")
#                 self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return bot_text, False

#             gibberish_indicators = ["what is the first time", "first time", "please repeat", "say again"]
#             if any(phrase in normalized for phrase in gibberish_indicators):
#                 self.no_input_count += 1
#                 logger.debug(f"Gibberish input (count {self.no_input_count}): '{human_input}'")
#                 if self.no_input_count >= 3:
#                     bot_text = personalize_response("Trouble connecting. I’ll follow up later. Thank you!")
#                     self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                     self._persist_state(current_id)
#                     return bot_text, True
#                 self.last_response_time = start_time
#                 bot_text = personalize_response("Sorry, repeat or say yes/no if available?")
#                 self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return bot_text, False

#             self.no_input_count = 0

#             if self.asked_for_name and "name is" in normalized:
#                 try:
#                     name_part = human_input.lower().split("name is", 1)[1].strip().split()
#                     self.user_name = name_part[0].capitalize()
#                     logger.debug(f"Extracted user name: {self.user_name}")
#                 except Exception:
#                     self.user_name = None

#             slots = self.extracted_slots
#             intent = slots.get("intent")

#             # FAQ handling
#             if any(q in normalized for q in ["price", "pricing", "cost", "timings", "time", "services"]):
#                 if "price" in normalized or "cost" in normalized:
#                     response = "Our fees start at ₹500/hour, varying by experience. Want more details?"
#                 elif "timings" in normalized or "time" in normalized:
#                     response = "Coaching is 3-6 PM school hours. Flexible options available—discuss?"
#                 elif "services" in normalized:
#                     response = "We offer curricula, training, and school placements. More questions?"
#                 self.last_response_time = start_time
#                 self.turns.append({"speaker": "bot", "text": response, "ts": int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return response, False

#             # NEW: Real-time sentiment-based routing
#             sentiment = await sentiment_chain.ainvoke({"transcript": "\n".join(t["text"] for t in self.turns)})
#             if sentiment["sentiment"] == "angry" or "upset" in normalized:
#                 logger.info("Detected angry tone, routing to calm rep")
#                 bot_text = "I’ll connect you with a calm rep to assist you."
#                 self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return bot_text, True

#             if self.conversation_state == "initial":
#                 if any(word in normalized for word in ["yes", "sure", "okay", "available"]):
#                     self.conversation_state = "background"
#                     response = "Great! Due to your interest, confirm your Bangalore location?"
#                 else:
#                     response = personalize_response("Sorry, misheard. Available to discuss coaching?")
#                 self.last_response_time = start_time
#                 self.turns.append({"speaker": "bot", "text": response, "ts": int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return response, False
#             else:
#                 try:
#                     response, should_end = await asyncio.wait_for(
#                         super().respond(human_input, conversation_id, is_interrupt), timeout=5.0
#                     )
#                 except asyncio.TimeoutError:
#                     fallback_msg = personalize_response("Response delayed. Try again shortly.")
#                     self.turns.append({"speaker": "bot", "text": fallback_msg, "ts": int(time.time()*1000)})
#                     self._persist_state(current_id)
#                     await self.end_call(conversation_id)  # New: End call on timeout
#                     return fallback_msg, True

#                 if response:
#                     response_text = personalize_response(response)
#                     if "location" in response_text.lower():
#                         self.conversation_state = "background"
#                     if any(phrase in response_text.lower() for phrase in ["confirm your full name", "may i have your name"]):
#                         self.asked_for_name = True

#                     if intent == "interested" and "schedule" in response_text.lower():
#                         available_slots = await check_calendar_availability(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
#                         if available_slots["available"]:
#                             bot_text = f"Great! Available slots: {', '.join(available_slots['slots'])}. Provide name, email, and preferred time?"
#                             self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                             self._persist_state(current_id)
#                             return bot_text, False
#                         else:
#                             bot_text = "No slots available now. I’ll follow up. Thank you!"
#                             self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                             self._persist_state(current_id)
#                             await self.end_call(conversation_id)  # New: End the call
#                             return bot_text, True

#                     if intent == "support":
#                         bot_text = "Let me route you to our support team."
#                         self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                         self._persist_state(current_id)
#                         return bot_text, True
#                     elif intent == "interested":
#                         bot_text = "Impressive! Connecting you to a sales rep."
#                         self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
#                         self._persist_state(current_id)
#                         await self.end_call(conversation_id)  # New: End call after routing
#                         return bot_text, True

#                     self.last_response_time = start_time
#                     self.turns.append({"speaker": "bot", "text": response_text, "ts": int(time.time()*1000)})
#                     if len(self.turns) % 4 == 0:
#                         asyncio.create_task(self._extract_slots_with_llm(current_id))
#                     self._persist_state(current_id)
#                     return response_text, should_end

#                 fallback_msg = personalize_response("Didn’t get that. Tell me more?")
#                 self.last_response_time = start_time
#                 self.turns.append({"speaker": "bot", "text": fallback_msg, "ts": int(time.time()*1000)})
#                 self._persist_state(current_id)
#                 return fallback_msg, False

#         except Exception as e:
#             logger.error(f"Error generating response: {str(e)}")
#             fallback_error_msg = "Error occurred. Try again."
#             self.turns.append({"speaker": "bot", "text": fallback_error_msg, "ts": int(time.time()*1000)})
#             current_id = self.conversation_id_cache or conversation_id or "unknown"
#             self._persist_state(current_id)
#             return fallback_error_msg, False
    








# # Custom Deepgram Transcriber with keepalive and chunk logging
# class CustomDeepgramTranscriber(DeepgramTranscriber):
#     def __init__(self, transcriber_config: DeepgramTranscriberConfig):
#         super().__init__(transcriber_config)
#         self.audio_buffer = io.BytesIO()
#         self.conversation_id = None

#     async def process(self, audio_chunk: bytes):
#         logger.debug(f"Processing audio chunk size: {len(audio_chunk)} bytes")
#         if not audio_chunk or len(audio_chunk) == 0:
#             logger.warning("Empty audio chunk - skipping")
#             return None
#         try:
#             async with self.buffer_lock:
#                 if self.conversation_id:
#                     total_size = self.audio_buffer.tell() + len(audio_chunk)
#                     if total_size > 10 * 1024 * 1024:  # 10MB limit
#                         await self._save_audio()
#                     self.audio_buffer.write(audio_chunk)
#             return await super().process(audio_chunk)
#         except Exception as e:
#             logger.error(f"Deepgram process error: {e}")
#             raise
    

#     async def keepalive(self):
#         while True:
#             await asyncio.sleep(10)
#             try:
#                 await super().process(b"\x00" * 160)
#                 logger.debug("Deepgram keepalive sent")
#             except Exception as e:
#                 logger.error(f"Keepalive failed: {e}")
#                 break


#     def set_conversation_id(self, conversation_id: str):
#         if self.conversation_id != conversation_id:
#             if self.audio_buffer.tell() > 0:
#                 asyncio.create_task(self._save_audio())
#             self.conversation_id = conversation_id
#             self.audio_buffer = io.BytesIO()

#     async def _save_audio(self):
#         if self.conversation_id and self.audio_buffer.tell() > 0:
#             self.audio_buffer.seek(0)
#             audio_path = RECORDINGS_DIR / f"{self.conversation_id}.wav"
#             with open(audio_path, 'wb') as f:
#                 f.write(self.audio_buffer.getbuffer())
#             logger.info(f"Saved audio to {audio_path}")
#             self.audio_buffer = io.BytesIO()

# # Custom Agent Factory
# class CustomAgentFactory:
#     def create_agent(self, agent_config: AgentConfig, logger: Optional[logging.Logger] = None) -> BaseAgent:
#         log = logger or globals().get("logger", logging.getLogger(__name__))
#         log.debug("Creating agent with config type: %s", agent_config.type)
#         # CHANGED: print the resolved config that TelephonyServer is about to use
#         try:
#             init_head = getattr(getattr(agent_config, "initial_message", None), "text", "")
#             init_head = (init_head or "")[:120]
#             prompt = getattr(agent_config, "prompt_preamble", "") or ""
#             prompt_len = len(prompt)
#             prompt_head = prompt[:120]
#             log.info("Factory using -> init_head=%r | prompt_len=%d | prompt_head=%r", init_head, prompt_len, prompt_head)  # CHANGED
#         except Exception as e:
#             log.warning("Factory logging failed: %s", e)  # CHANGED

#         if agent_config.type == "agent_langchain":
#             log.debug("Creating CustomLangchainAgent")
#             return CustomLangchainAgent(agent_config=typing.cast(CustomLangchainAgentConfig, agent_config))
#         log.error("Invalid agent config type: %s", agent_config.type)
#         raise Exception(f"Invalid agent config: {agent_config.type}")



# # Custom Synthesizer Factory
# class CustomSynthesizerFactory:
#     def create_synthesizer(self, synthesizer_config: SynthesizerConfig) -> BaseSynthesizer:
#         logger.debug(f"Creating synthesizer with config: {synthesizer_config}")
#         if isinstance(synthesizer_config, StreamElementsSynthesizerConfig):
#             logger.debug("Creating StreamElementsSynthesizer")
#             return StreamElementsSynthesizer(synthesizer_config)
#         logger.error(f"Invalid synthesizer config type: {synthesizer_config.type}")
#         raise Exception(f"Invalid synthesizer config: {synthesizer_config.type}")

# # FastAPI App
# app = FastAPI()

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     logger.debug("Starting up FastAPI application")
#     logger.debug("Registered routes:")
#     for route in app.routes:
#         methods = getattr(route, "methods", ["WebSocket"])
#         logger.debug(f" - {route.path} ({methods})")
#     yield
#     # ADDED: final sweep to persist any in-memory conversations at shutdown
#     try:
#         for conv_id in list(CONVERSATION_STORE.keys()):
#             out_path = CONVERSATIONS_DIR / f"{conv_id}.json"
#             with open(out_path, "w", encoding="utf-8") as f:
#                 json.dump(CONVERSATION_STORE[conv_id], f, ensure_ascii=False, indent=2)
#         logger.debug("Shutdown flush completed for all conversations")
#     except Exception as e:
#         logger.error(f"Error during shutdown flush: {e}")
#     logger.debug("Shutting down FastAPI application")

# app.router.lifespan_context = lifespan

# # Twilio config
# twilio_config = TwilioConfig(
#     account_sid=TWILIO_ACCOUNT_SID,
#     auth_token=TWILIO_AUTH_TOKEN
# )

# # Synthesizer config (telephone voice output)
# synthesizer_config = StreamElementsSynthesizerConfig.from_telephone_output_device(
#     voice="Brian"
# )

# transcriber_config = DeepgramTranscriberConfig(
#     api_key=DEEPGRAM_API_KEY,
#     model="nova-2-phonecall",
#     language="en",
#     sampling_rate=8000,  # int primitive, not enum
#     audio_encoding="mulaw",  # lowercase string, not enum
#     chunk_size=320,
#     endpointing_config=PunctuationEndpointingConfig(),
#     downsampling=1,
# )

# # Default config as a fallback
# default_agent_config = LangchainAgentConfig(
#     initial_message=BaseMessage(text="Hello, this is a default message."),
#     prompt_preamble="",
#     model_name="llama-3.1-8b-instant",
#     api_key=GROQ_API_KEY,
#     provider="groq",
# )



# # Telephony Server setup
# telephony_server = TelephonyServer(
#     base_url=BASE_URL,  # your ngrok url
#     config_manager=config_manager,
#     inbound_call_configs=[
#         TwilioInboundCallConfig(
#             url="/inbound_call",
#             twilio_config=twilio_config,
#             config_manager=shared_config_manager, 
#             agent_config=default_agent_config,  # NEW: Use default for inbound calls
#             synthesizer_config=synthesizer_config,
#             transcriber_config=transcriber_config,  # Use instance
#             agent_factory=CustomAgentFactory(),
#             twiml_fallback_response='''<?xml version="1.0" encoding="UTF-8"?>
# <Response>
#     <Say>I didn't hear a response. Are you still there? Please say something to continue.</Say>
#     <Pause length="15"/>
#     <Redirect method="POST">/inbound_call</Redirect>
# </Response>''',
#             record=True,
#             status_callback=f"https://{BASE_URL}/call_status",  # NEW: Added for inbound call status
#             status_callback_method="POST",
#             status_callback_event=["completed"]  # Trigger on call completion
#         )
#     ],
#     agent_factory=CustomAgentFactory(),
#     synthesizer_factory=CustomSynthesizerFactory(),
#     events_manager=ChessEventsManager(),
# )

# # Add routes to FastAPI app
# app.include_router(telephony_server.get_router())


# # Fix call_status to handle empty JSON
# @app.post("/call_status")
# async def call_status(request: Request):
#     try:
#         # Twilio sends application/x-www-form-urlencoded by default
#         form = await request.form()
#         call_sid = form.get("CallSid")
#         status = form.get("CallStatus")
#         recording_sid = form.get("RecordingSid")
#         recording_url = form.get("RecordingUrl")
#         logger.info(f"Call status update: SID={call_sid}, Status={status}, RecSid={recording_sid}, RecUrl={recording_url}")

#         if call_sid and call_sid in CONVERSATION_STORE:
#             CONVERSATION_STORE[call_sid]["status"] = status
#             if status in ["completed", "failed", "no-answer", "busy"]:
#                 conversation = CONVERSATION_STORE.get(call_sid, {}).get("conversation")
#                 if conversation and hasattr(conversation, "terminate"):
#                     await conversation.terminate()
#                 else:
#                     logger.warning(f"No conversation or terminate method for SID={call_sid}")
#         return {"ok": True}
#     except Exception as e:
#         logger.error(f"/call_status failed: {e}")
#         raise HTTPException(status_code=500, detail=str(e))


# # NEW: Endpoint to serve conversation JSON files
# @app.get("/conversations/{call_sid}.json")
# async def get_conversation(call_sid: str):
#     path = CONVERSATIONS_DIR / f"{call_sid}.json"
#     if path.exists():
#         with open(path, "r", encoding="utf-8") as f:
#             return json.load(f)
#     raise HTTPException(status_code=404, detail="Conversation not found")


# # ADDED n8n: request schema for outbound_call
# class OutboundCallRequest(BaseModel):
#     to_phone: str
#     lead: Optional[Dict[str, Any]] = None
#     transcript_callback_url: Optional[str] = None
#     call_type: str = "qualification"
#     agent_type: str = "chess_coach"
#     initial_message: str = "Hello, this is a default message."
#     prompt_preamble: str = ""

# # ADDED n8n: normalize to E164 basic
# def normalize_e164(number: str) -> str:
#     n = re.sub(r'\D+', '', number or '')
#     if not n:
#         return number
#     if n.startswith('0'):
#         n = n.lstrip('0')
#     if not n.startswith('+'):
#         if len(n) == 10:
#             n = '+91' + n
#         else:
#             n = '+' + n
#     return n



# # ADDED n8n: HTTP endpoint to start outbound call from n8n
# @app.post("/outbound_call")
# async def outbound_call(req: OutboundCallRequest):
#     try:
#         # CHANGED: richer logging of what arrived from n8n/CSV (safe heads only)
#         logger.info(
#             "OUTBOUND payload -> agent_type=%s | init_len=%d | init_head=%r | prompt_len=%d | prompt_head=%r",
#             req.agent_type,
#             len((req.initial_message or "")),
#             (req.initial_message or "")[:120],
#             len((req.prompt_preamble or "")),
#             (req.prompt_preamble or "")[:120],
#         )  # CHANGED

#         to_phone = normalize_e164(req.to_phone)
#         if not to_phone or len(to_phone) < 10:
#             raise HTTPException(status_code=400, detail="Invalid phone")

#         # Resolve the prompt: prefer CSV input; otherwise fall back by agent_type
#         prompt_preamble = req.prompt_preamble or {
#             "chess_coach": CHESS_COACH_PROMPT_PREAMBLE,
#             "medical_sales": medical_sales_prompt,
#             "hospital_receptionist": hospital_receptionist_prompt,
#         }.get((req.agent_type or "").strip(), "")

#         # Use the received prompt_preamble and initial_message directly
#         agent_config = CustomLangchainAgentConfig(  # CHANGED: use custom config class
#             initial_message=BaseMessage(text=req.initial_message or "Hello, this is a default message."),  # CHANGED
#             prompt_preamble=prompt_preamble,  # CHANGED
#             model_name="llama-3.1-8b-instant",
#             api_key=GROQ_API_KEY,
#             provider="groq",
#         )

#         # CHANGED: save config in the SAME manager TelephonyServer reads
#         call_key = f"outbound_{int(time.time()*1000)}_{hash(to_phone)}"  # CHANGED
#         await telephony_server.config_manager.save_config(call_key, agent_config)  # CHANGED

#         logger.info(
#             "Saved agent under custom id: %s | agent_type=%s | init_head=%r | prompt_len=%d",
#             call_key,
#             req.agent_type,
#             agent_config.initial_message.text[:120] if agent_config.initial_message else "",
#             len(agent_config.prompt_preamble or ""),
#         )  # CHANGED

#         sid = await make_outbound_call(
#             to_phone,
#             req.call_type,
#             req.lead,
#             req.agent_type,
#             agent_config,
#             call_sid=call_key,
#         )

#         lead = req.lead or {}
#         lead["to_phone"] = to_phone
#         lead["agent_type"] = req.agent_type
#         LEAD_CONTEXT_STORE[sid] = lead
#         logger.info("Call SID=%s, agent_type=%s", sid, req.agent_type)
#         if req.transcript_callback_url:
#             os.environ["TRANSCRIPT_CALLBACK_URL"] = req.transcript_callback_url
#         return {"ok": True, "call_sid": sid}
#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error("Error: %s", e)
#         raise HTTPException(status_code=500, detail=str(e))




# # Outbound call helper
# async def make_outbound_call(
#     to_phone: str,
#     call_type: str,
#     lead: dict = None,
#     agent_type: str = "chess_coach",
#     agent_config: AgentConfig = None,
#     call_sid: str = None,
# ):
#     client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#     twilio_base_url = f"https://{BASE_URL}"

#     # Use agent_config.initial_message if available, fallback to a minimal default
#     initial_message = (
#         agent_config.initial_message.text
#         if agent_config and agent_config.initial_message
#         else f"Hello, this is a generic message for {call_type}."
#     )
#     call_sid = call_sid or f"outbound_{int(time.time()*1000)}_{hash(to_phone)}"

#     # CHANGED: make sure query has the correct key AND '=' sign; send both keys for compatibility
#     twiml_url = f"{twilio_base_url}/inbound_call?call_sid={call_sid}&callsid={call_sid}"  # CHANGED

#     call = await asyncio.get_event_loop().run_in_executor(
#         None,
#         lambda: client.calls.create(
#             to=to_phone,
#             from_=TWILIO_PHONE_NUMBER,
#             url=twiml_url,
#             status_callback=f"{twilio_base_url}/call_status",
#             status_callback_method="POST",
#             status_callback_event=["initiated", "ringing", "answered", "completed"],
#             record=True,
#             recording_channels="dual",
#         ),
#     )
#     logger.info("Call initiated: TwilioSID=%s | type=%s | agent_type=%s", call.sid, call_type, agent_type)

#     # CHANGED: mirror-save under Twilio’s real CallSid in the SAME manager
#     try:
#         if agent_config:
#             await telephony_server.config_manager.save_config(call.sid, agent_config)  # CHANGED
#         logger.info(
#             "Mirrored agent for live call: custom_id=%s -> TwilioSID=%s | init_head=%r | prompt_len=%d",
#             call_sid,
#             call.sid,
#             agent_config.initial_message.text[:120] if agent_config and agent_config.initial_message else "",
#             len(agent_config.prompt_preamble or "") if agent_config else 0,
#         )  # CHANGED
#     except Exception as e:
#         logger.warning("Failed to mirror agent under TwilioSID %s: %s", call.sid, e)  # CHANGED

#     # Seed local stores for your dashboards (unchanged structure)
#     if call_sid not in LEAD_CONTEXT_STORE:
#         LEAD_CONTEXT_STORE[call_sid] = {"to_phone": to_phone, "call_type": call_type, "agent_type": agent_type, **(lead or {})}
#     CONVERSATION_STORE.setdefault(
#         call_sid,
#         {
#             "conversation_id": call_sid,
#             "updated_at": int(time.time() * 1000),
#             "lead": LEAD_CONTEXT_STORE.get(call_sid, {}),
#             "slots": {},
#             "turns": [{"speaker": "bot", "text": initial_message, "ts": int(time.time() * 1000)}],
#             "agent_config": agent_config,
#         },
#     )
#     return call_sid





# # In your CustomAgentFactory (e.g., in telephony_server setup)
# def custom_agent_factory(conversation_id: str):
#     config = config_manager.get_config(conversation_id) or CONVERSATION_STORE.get(conversation_id, {}).get("agent_config", default_agent_config)
#     if not config.prompt_preamble:  # Fallback if no config
#         config.prompt_preamble = "Default prompt if none provided."
#     return CustomLangchainAgent(config)




# def outbound_scheduler():
#     while True:
#         response = requests.get(CRM_API_URL, headers={"Authorization": f"Bearer {CRM_API_KEY}"})
#         if response.status_code == 200:
#             leads = response.json().get("leads", [])
#             for lead in leads:
#                 if lead.get("status") == "Call Pending":
#                     call_type = lead.get("call_type", "qualification")
#                     agent_type = lead.get("agent_type", "chess_coach")  # NEW: Support agent_type in scheduler
#                     asyncio.run(make_outbound_call(lead["phone"], call_type, lead, agent_type))
#                     update_crm(lead["id"], "", {}, {}, "", status="Calling")
#         time.sleep(300)



# # Main entrypoint (updated to include scheduler)
# if __name__ == "__main__":
#     import uvicorn

#     def run_server():
#         logger.debug("Starting Uvicorn server")
#         uvicorn.run(app, host="0.0.0.0", port=3000)

#     # Start outbound scheduler in a thread
#     scheduler_thread = threading.Thread(target=outbound_scheduler, daemon=True)
#     scheduler_thread.start()

#     run_server()
























import os
import logging
import asyncio
import httpx
import typing
import time
from typing import Optional, Tuple, Any, Dict
from fastapi import FastAPI, Request, Response
from fastapi.logger import logger as fastapi_logger
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from twilio.rest import Client
from vocode.streaming.telephony.server.base import TelephonyServer, TwilioInboundCallConfig
from vocode.streaming.models.telephony import TwilioConfig
from vocode.streaming.models.agent import LangchainAgentConfig, AgentConfig
from vocode.streaming.agent.langchain_agent import LangchainAgent
from vocode.streaming.models.message import BaseMessage
from vocode.streaming.transcriber.deepgram_transcriber import DeepgramTranscriber
from vocode.streaming.models.transcriber import DeepgramTranscriberConfig, AudioEncoding, PunctuationEndpointingConfig
from vocode.streaming.synthesizer.stream_elements_synthesizer import StreamElementsSynthesizer
from vocode.streaming.models.synthesizer import StreamElementsSynthesizerConfig, SynthesizerConfig
from vocode.streaming.synthesizer.base_synthesizer import BaseSynthesizer
from vocode.streaming.telephony.config_manager.in_memory_config_manager import InMemoryConfigManager
from vocode.streaming.agent.base_agent import BaseAgent
from vocode.streaming.models.events import Event, EventType
from vocode.streaming.models.transcript import TranscriptCompleteEvent
from vocode.streaming.utils import events_manager
from langchain_groq import ChatGroq
import threading
import numpy as np

# ADDED for JSON capture with LLM extraction
import json  # ADDED for JSON capture with LLM extraction
import re    # ADDED: general regex utilities
from pathlib import Path  # ADDED: filesystem-safe paths
from fastapi import HTTPException  # ADDED n8n
from pydantic import BaseModel  # ADDED n8n

# NEW: For sentiment analysis and summaries (using Groq LLM)
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


# NEW: For email summaries (simple SMTP)
import smtplib
from email.mime.text import MIMEText

# NEW: For WhatsApp summaries (using Twilio)
from twilio.rest import Client as TwilioClient

# NEW: Placeholder CRM API (replace with your CRM, e.g., HubSpot API)
import requests  # NEW: for CRM API calls


from pydub import AudioSegment  # NEW: For audio conversion (MP3/WAV)
import wave  # NEW: For WAV file handling
import io

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fastapi_logger.setLevel(logging.DEBUG)

# Ensure ffmpeg is in PATH
os.environ['PATH'] += os.pathsep + 'C:\\ffmpeg\\bin'

load_dotenv()

# Environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
BASE_URL = os.getenv("BASE_URL")
DEBUG_AUDIO = os.getenv("DEBUG_AUDIO", "false").lower() == "true"


# NEW: Storage directory for recordings
RECORDINGS_DIR = Path("recordings")
RECORDINGS_DIR.mkdir(exist_ok=True, parents=True)

# NEW: Cloud storage URL (e.g., AWS S3 placeholder)
CLOUD_STORAGE_URL = os.getenv("CLOUD_STORAGE_URL", "https://your-s3-bucket.s3.amazonaws.com/")


# NEW: CRM environment variables (replace with your CRM details)
CRM_API_URL = os.getenv("CRM_API_URL", "https://your-crm-api.com/leads")
CRM_API_KEY = os.getenv("CRM_API_KEY", "your_crm_api_key")
EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER", "smtp.example.com")
EMAIL_SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", 587))
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "priya@4champz.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your_email_password")
CALENDAR_API_URL = os.getenv("CALENDAR_API_URL", "https://your-calendar-api.com/availability")  # NEW: for scheduling

# NEW: WhatsApp sender number (for summaries)
WHATSAPP_SENDER = os.getenv("WHATSAPP_SENDER", TWILIO_PHONE_NUMBER)



# Validate environment variables
required_vars = [GROQ_API_KEY, DEEPGRAM_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, BASE_URL, CRM_API_URL, CRM_API_KEY, EMAIL_SMTP_SERVER, EMAIL_SENDER, EMAIL_PASSWORD, CALENDAR_API_URL]
if not all(required_vars):
    raise ValueError("Missing required environment variables in .env file. Required: GROQ_API_KEY, DEEPGRAM_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, BASE_URL")

# Validate Ngrok URL
if not BASE_URL.endswith((".ngrok-free.app", ".ngrok.io")):
    logger.warning(f"BASE_URL ({BASE_URL}) does not appear to be a valid Ngrok URL. Ensure it matches the current Ngrok session and is updated in Twilio Console.")

CHESS_COACH_PROMPT_PREAMBLE = """
# Chess Coaching Sales Representative Prompt
## Identity & Purpose
You are Priya, a virtual sales representative for 4champz, a leading chess coaching service provider based in Bengaluru, India. We specialize in providing qualified chess coaches to schools across Bangalore. 
Your primary purpose is to qualify leads who have shown interest in chess coaching opportunities, understand their background and experience, explore potential collaboration as a chess coach for our school programs, handle FAQs, and schedule meetings for both inbound and outbound calls.
## Voice & Persona
### Personality
- Sound professional, warm, and conversational—like a knowledgeable chess enthusiast
- Project genuine interest in learning about their chess journey
- Maintain an engaging and respectful demeanor throughout the conversation
- Show respect for their time while staying focused on understanding their suitability for school coaching
- Convey enthusiasm about the opportunity to shape young minds through chess
### Speech Characteristics
- Use clear, conversational language with natural flow
- Keep messages under 150 characters when possible
- Include probing questions to gather detailed information
- Show genuine interest in their chess background and achievements
- Use encouraging language when discussing their experience and qualifications
## Conversation Flow
### Introduction
1. For inbound: "Hello {{name}}, this is Priya from 4champz. Do you have 5-10 minutes to discuss chess coaching opportunities in Bangalore?"
2. For outbound: "Hello {{name}}, this is Priya from 4champz. I’m reaching out due to your interest. Available to discuss?"
3. Follow with: "I’d love to explore your background, answer FAQs like pricing or timings, or assist with reminders if applicable."
### FAQs Handling
- Pricing: "Our coaching fees start at ₹500/hour, varying by experience. Interested in details?"
- Timings: "Coaching is typically 3-6 PM school hours. Flexible options available—want to discuss?"
- Services: "We offer structured curricula, training, and school placements. More questions?"
### Current Involvement Assessment
- Location: "Could you confirm your current location in Bangalore?"
- Involvement: "Are you actively playing or coaching chess?"
- Availability: "What’s your schedule like, especially afternoons?"
### Experience and Background Qualification
- Chess playing: "What’s your FIDE or All India Chess Federation rating?"
- Tournaments: "Tell me about your recent tournament participation."
- Coaching: "Have you coached children before, especially in chess?"
- Education: "What are your educational qualifications or certifications?"
### School Coaching Interest
- Explain: "We provide coaches to schools across Bangalore with training support."
- Availability: "Are you free 3-6 PM? How many days weekly?"
- Age groups: "Comfortable with Classes 1-12? Any preferences?"
- Support: "We offer training. Interested in a structured curriculum?"
### Scheduling
- If interested: "Let’s schedule a detailed discussion. When are you free this week?"
- Use check_calendar_availability and book_appointment.
- Confirm: "Please provide your full name, email, and preferred time."
### Close
- Positive: "Thank you, {{name}}. We’ll send details and a confirmation. Looking forward to it!"
- End with end_call unless transferred
## Response Guidelines
- Handle FAQs before diving into qualification if asked
- Use IST timing for scheduling (e.g., today is 03:14 PM IST, Friday, September 19, 2025)
- Ask one question at a time to avoid overwhelming them
- Keep responses focused on qualifying their suitability for school coaching
- Ask location-specific questions about Bangalore areas they can cover
- Show genuine enthusiasm for their chess achievements and experience
- Be respectful of their current commitments and time constraints
- Emphasize the opportunity to impact young minds through chess education
## Scenario Handling
### Interested Leads
- Enthusiasm: "Your experience is impressive! Let’s connect you with a rep."
- Route: Use transfer_call to sales rep.
### Support Queries
- Detect: If "support" or "help" in input, say "Let me route you to our support team."
- Route: Use transfer_call to support.
### Reminders
- Meeting: "This is a reminder for your demo on [date/time]. Ready to proceed?" (e.g., use current date + 1 day if unspecified)
- Payment: "This is a payment reminder for ₹500 due by [date]. Settled?" (e.g., use current date + 1 day if unspecified)
### For Highly Qualified Candidates
- Express enthusiasm: "Your tournament experience and rating are impressive! Our partner schools would definitely value someone with your background."
- Fast-track process: "Given your qualifications, I’d love to expedite our discussion. When would be the best time this week?"
- Highlight premium opportunities: "With your experience, you’d be perfect for our advanced chess program placements at premium schools."
### For Candidates with Limited Formal Experience
- Explore potential: "While formal ratings are helpful, we also value passion and teaching ability. Tell me about your experience with children or young people."
- Training emphasis: "We provide comprehensive training to develop skills. Are you excited about growing with our support?"
- Alternative qualifications: "Have you been involved in chess clubs, online coaching, or informal teaching?"
### For Availability Concerns
- Flexible scheduling: "We can often accommodate different preferences. What times work best for you?"
- Part-time opportunities: "Many coaches start part-time. Would that interest you?"
- Location matching: "We’ll match you with convenient schools. Which Bangalore areas are accessible?"
### For Candidates Requesting Human Assistance
- If they want human help or details on compensation/partnerships:
  - Use transfer_call
  - Say: "Of course! Let me connect you with our placement manager for details on partnerships and compensation."
## Knowledge Base
### Caller Info
- name: {{name}}, email: {{email}}, phone_number: {{phone_number}}, role: {{role}}
### 4champz Model
- Leading chess coaching in Bengaluru, school-focused, training provided
- Partners with reputed schools, offers part-time/full-time opportunities
- Focuses on developing young chess talent
### Requirements
- 3-6 PM availability, English/Kannada/Hindi, Bangalore travel
- Professional attitude, teaching aptitude, school-level chess knowledge
### Assessment Criteria
- Chess playing experience and rating (FIDE/All India Chess Federation)
- Tournament participation and achievements
- Prior coaching/teaching experience, especially with children
- Educational qualifications and chess certifications
- Language capabilities and communication skills
- Geographic availability across Bangalore
- Flexibility with scheduling and age groups
## Response Refinement
- When discussing chess background: "Your chess journey sounds fascinating. Could you tell more about [specific aspect]?"
- When explaining opportunities: "Let me paint a picture of coaching with our partner schools..."
- When confirming details: "To confirm—you’re available [availability] and comfortable with [preferences]. Is that accurate?"
## Call Management
### Available Functions
- check_calendar_availability: Use for scheduling follow-up meetings
- book_appointment: Use to confirm scheduled appointments
- transfer_call: Use when candidate requests human assistance
- end_call: Use to conclude every conversation
## Technical Considerations
- If calendar delays occur: "I’m checking available slots. This will take a moment."
- If multiple scheduling needs: "Let’s book your appointment first, then address other questions."
- Always confirm appointment details before ending: "To confirm, we’re scheduled for [day], [date] at [time IST]. You’ll receive an email."
---
Your goal is to qualify chess coaches for Bangalore schools, ensure they understand and are excited about the opportunity, and maintain 4champz’s professional reputation. Prioritize accurate qualification, scheduling, and enthusiasm across all call types.
"""

# Groq LLM setup
llm = ChatGroq(model_name="llama-3.1-8b-instant")
# llm = ChatGroq(model_name="groq/compound-mini")

# Config Manager
config_manager = InMemoryConfigManager()

# ADDED for JSON capture with LLM extraction: global in-memory store
CONVERSATION_STORE: dict = {}  # ADDED for JSON LLM extraction

# ADDED for JSON capture with LLM extraction: directory for local persistence
CONVERSATIONS_DIR = Path("conversations")  # ADDED
CONVERSATIONS_DIR.mkdir(exist_ok=True, parents=True)  # ADDED

# ADDED n8n: store lead context by call_sid/conversation_id
LEAD_CONTEXT_STORE: dict = {}  # ADDED n8n


# Sentiment Analysis Chain (using Groq LLM)
sentiment_prompt = PromptTemplate(
    input_variables=["transcript"],
    template="Analyze the sentiment of this transcript: {transcript}. Return a JSON with 'sentiment' (positive, neutral, negative, angry, confused) and 'tone_score' (1-10, 10 being most positive)."
)
sentiment_chain = LLMChain(llm=llm, prompt=sentiment_prompt)

# Summary Generation Chain (using Groq LLM)
summary_prompt = PromptTemplate(
    input_variables=["transcript"],
    template="Generate a summary of this transcript: {transcript}. Include key points, customer intent, and next actions. Return a JSON with 'summary', 'intent', 'next_actions' (array of strings)."
)
summary_chain = LLMChain(llm=llm, prompt=summary_prompt)



# Send Email Function
def send_email(to_email: str, subject: str, body: str):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = to_email
    with smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT) as server:
        server.starttls()  # Added TLS for security
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, to_email, msg.as_string())
    logger.info(f"Email sent to {to_email}")

# Send WhatsApp Summary Function (using Twilio)
def send_whatsapp(to_phone: str, body: str):
    client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        from_='whatsapp:' + WHATSAPP_SENDER,
        body=body,
        to='whatsapp:' + to_phone
    )
    logger.info(f"WhatsApp sent to {to_phone}")



# NEW: Check Calendar Availability
async def check_calendar_availability(preferred_time: str) -> dict:
    headers = {"Authorization": f"Bearer {CRM_API_KEY}"}
    params = {"time": preferred_time, "timezone": "Asia/Kolkata"}
    async with httpx.AsyncClient() as client:
        response = await client.get(CALENDAR_API_URL, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        logger.error(f"Calendar check failed: {response.text}")
        return {"available": False, "slots": []}
    


# NEW: Book Appointment
async def book_appointment(lead_id: str, name: str, email: str, time: str):
    payload = {
        "lead_id": lead_id,
        "name": name,
        "email": email,
        "time": time,
        "status": "Scheduled"
    }
    headers = {"Authorization": f"Bearer {CRM_API_KEY}"}
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{CRM_API_URL}/appointments", json=payload, headers=headers)
        if response.status_code == 200:
            logger.info(f"Appointment booked for lead {lead_id}")
            return True
        logger.error(f"Appointment booking failed: {response.text}")
        return False


# NEW: Update CRM Function (placeholder; replace with your CRM API)
def update_crm(lead_id: str, transcript: str, sentiment: dict, summary: dict, audio_url: str, twilio_audio_url: Optional[str] = None, status: str = "Called", appointment: dict = None):
    payload = {
        "lead_id": lead_id,
        "transcript": transcript,
        "sentiment": sentiment,
        "summary": summary,
        "audio_url": audio_url,
        "twilio_audio_url": twilio_audio_url,  # NEW: Twilio full call recording
        "status": status,
        "appointment": appointment
    }
    headers = {"Authorization": f"Bearer {CRM_API_KEY}"}
    response = requests.post(CRM_API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        logger.info(f"CRM updated for lead {lead_id}")
    else:
        logger.error(f"CRM update failed: {response.text}")



# Events Manager to log transcripts
class ChessEventsManager(events_manager.EventsManager):
    def __init__(self):
        super().__init__(subscriptions=[EventType.TRANSCRIPT_COMPLETE])

    async def handle_event(self, event: Event):
        if event.type == EventType.TRANSCRIPT_COMPLETE:
            transcript_complete_event = typing.cast(TranscriptCompleteEvent, event)
            transcript = transcript_complete_event.transcript.to_string()
            logger.debug(f"Transcript for conversation {transcript_complete_event.conversation_id}: {transcript}")

            # NEW: Sentiment analysis
            sentiment = await sentiment_chain.ainvoke({"transcript": transcript})

            # NEW: Summary generation
            summary = await summary_chain.ainvoke({"transcript": transcript})

            # NEW: Recording storage (using Deepgram audio chunks)
            audio_path = await save_recording(transcript_complete_event.conversation_id)
            audio_url = f"{CLOUD_STORAGE_URL}/{os.path.basename(audio_path)}" if CLOUD_STORAGE_URL else audio_path

            # NEW: Fetch Twilio recording URL if available
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            recordings = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: client.recordings.list(call_sid=transcript_complete_event.conversation_id)
            )
            twilio_audio_url = recordings[0].uri if recordings else None  # NEW: Get Twilio recording URL

            await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: update_crm(transcript_complete_event.conversation_id, transcript, sentiment, summary, audio_url, twilio_audio_url=twilio_audio_url)  # Fixed to use audio_url
            )

            # NEW: Send summary to customer/management
            # Assume email and phone from lead context or CRM
            short_summary = f"Call Summary: {summary['summary'][:100]}... Next steps: {', '.join(summary['next_actions'][:2])}"
            lead = LEAD_CONTEXT_STORE.get(transcript_complete_event.conversation_id, {})
            if "email" in lead:
                send_email(lead["email"], "Call Summary", short_summary)
            if "to_phone" in lead:
                send_whatsapp(lead["to_phone"], short_summary)

            webhook_url = os.getenv("TRANSCRIPT_CALLBACK_URL")
            if webhook_url:
                data = {"conversation_id": transcript_complete_event.conversation_id, "user_id": 1, "transcript": transcript}
                async with httpx.AsyncClient() as client:
                    response = await client.post(webhook_url, json=data)
                    if response.status_code == 200:
                        logger.info("Transcript sent successfully to webhook")
                    else:
                        logger.error(f"Failed to send transcript to webhook: {response.status_code}")
            # ADDED for JSON capture with LLM extraction: write store JSON to disk
            try:
                convo = CONVERSATION_STORE.get(transcript_complete_event.conversation_id)
                if convo:
                    convo["sentiment"] = sentiment  # NEW
                    convo["summary"] = summary  # NEW
                    out_path = CONVERSATIONS_DIR / f"{transcript_complete_event.conversation_id}.json"
                    with open(out_path, "w", encoding="utf-8") as f:
                        json.dump(convo, f, ensure_ascii=False, indent=2)
                    logger.info(f"Wrote JSON summary to {out_path}")
            except Exception as e:
                logger.error(f"Failed to write JSON summary: {e}")


async def save_recording(conversation_id: str) -> str:
    # Assume transcriber instance is accessible via a global or passed reference
    transcriber = None  # Placeholder; should be injected or managed by TelephonyServer
    if transcriber and hasattr(transcriber, 'audio_buffer') and transcriber.conversation_id == conversation_id:
        await transcriber._save_audio()
        audio_path = RECORDINGS_DIR / f"{conversation_id}.wav"
        return str(audio_path)
    logger.error(f"No valid transcriber or buffer for conversation {conversation_id}")
    return ""

# Custom Agent Config
class CustomLangchainAgentConfig(LangchainAgentConfig, type="agent_langchain"):
    initial_message: BaseMessage = BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?")
    prompt_preamble: str = CHESS_COACH_PROMPT_PREAMBLE
    model_name: str = "llama-3.1-8b-instant"
    # model_name: str = "groq/compound-mini"
    api_key: str = GROQ_API_KEY
    provider: str = "groq"

# Custom Langchain Agent
class CustomLangchainAgent(LangchainAgent):
    def __init__(self, agent_config: CustomLangchainAgentConfig):
        logger.debug(f"Initializing CustomLangchainAgent with config: {agent_config}")
        super().__init__(agent_config=agent_config)
        self.last_response_time = time.time()
        self.conversation_state = "initial"
        self.no_input_count = 0
        self.user_name = None  # store extracted/confirmed name
        self.asked_for_name = False  # track if name is requested
        logger.debug("Initialized CustomLangchainAgent with Groq LLM (llama-3.1-8b-instant)")
        # ADDED for JSON capture with LLM extraction
        self.turns = []  # [{"speaker":"user"/"bot","text":..., "ts": epoch_ms}]
        self.conversation_id_cache = None  # to index the global store
        self.extracted_slots = {}  # LLM-extracted structured data


    # ADDED n8n: helper to ensure id
    def _ensure_conv_id(self, conversation_id: Optional[str]) -> str:
        if conversation_id and isinstance(conversation_id, str) and conversation_id.strip():
            return conversation_id
        return f"unknown_{int(time.time()*1000)}"

    # ADDED for JSON capture with LLM extraction
    def _flush_to_disk(self, conversation_id: str):
        """Write the current conversation JSON to disk immediately."""
        try:
            payload = CONVERSATION_STORE.get(conversation_id)
            if not payload:
                return
            out_path = CONVERSATIONS_DIR / f"{conversation_id}.json"
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
            logger.debug(f"Flushed conversation {conversation_id} to {out_path}")
        except Exception as e:
            logger.error(f"Flush to disk failed for {conversation_id}: {e}")

    # ADDED for JSON capture with LLM extraction
    def _persist_state(self, conversation_id: Optional[str]):
        conv_id = self._ensure_conv_id(conversation_id)
        now_ms = int(time.time() * 1000)
        lead = LEAD_CONTEXT_STORE.get(conv_id, {})  # ADDED n8n
        payload = {
            "conversation_id": conv_id,
            "updated_at": now_ms,
            "lead": lead,  # ADDED n8n
            "slots": self.extracted_slots,  # slots are LLM-extracted
            "turns": self.turns
        }
        CONVERSATION_STORE[conv_id] = payload
        self._flush_to_disk(conv_id)  # ADDED: always flush on persist

    # ADDED for JSON capture with LLM extraction
    def _strip_code_fences(self, s: str) -> str:
        t = (s or "").strip()
        if t.startswith("```"):
            end = t.rfind("```")
            if end > 0:
                inner = t[3:end].strip()
                if inner.lower().startswith("json"):
                    inner = inner[4:].strip()
                return inner
        return t

    # ADDED for JSON capture with LLM extraction
    async def _extract_slots_with_llm(self, conversation_id: str):
        """Extract slots with retry logic."""
        max_retries = 3
        retry_delay = 2  # seconds

        for attempt in range(max_retries):
            try:
                # Build a compact transcript string
                convo_lines = []
                for t in self.turns[-30:]:
                    role = "User" if t["speaker"] == "user" else "Agent"
                    text_line = re.sub(r'\s+', ' ', t['text']).strip()
                    convo_lines.append(f"{role}: {text_line}")
                convo_text = "\n".join(convo_lines)

                # Instruction for JSON-only schema
                schema_instruction = (
                    "Return ONLY a JSON object with these keys:\n"
                    "{\n"
                    '  "location": string|null,\n'
                    '  "involvement": "playing"|"coaching"|null,\n'
                    '  "availability": string|null,\n'
                    '  "age_range": string|null,\n'
                    '  "languages": string[]|null,\n'
                    '  "rating": string|null,\n'
                    '  "tournaments": string|null,\n'
                    '  "certifications": string|null,\n'
                    '  "questions": string[]|null,\n'
                    '  "intent": "interested"|"support"|"reminder"|null\n'
                    '}\n'
                    "Infer conservatively. Use null if not explicitly known."
                )

                prompt = f"{schema_instruction}\n\nConversation:\n{convo_text}\n\nJSON:"

                extractor = ChatGroq(model_name="llama-3.1-8b-instant")
                resp = await extractor.ainvoke([
                    {"role": "system", "content": "You extract structured information from conversations."},
                    {"role": "user", "content": prompt}
                ])

                # Normalize content
                content = None
                if hasattr(resp, "content"):
                    content = resp.content
                elif hasattr(resp, "generations"):
                    try:
                        content = resp.generations.text
                    except Exception:
                        content = str(resp)
                else:
                    content = str(resp)

                parsed = None
                try:
                    c = self._strip_code_fences(content)
                    parsed = json.loads(c)
                except Exception:
                    logger.warning("Primary JSON parse failed; attempting to locate JSON object")
                    first = content.find("{")
                    last = content.rfind("}")
                    if first != -1 and last != -1 and last > first:
                        snippet = content[first:last+1]
                        try:
                            parsed = json.loads(snippet)
                        except Exception:
                            parsed = None

                if isinstance(parsed, dict):
                    # normalize keys
                    for k in ["location","involvement","availability","age_range","languages","rating","tournaments","certifications","questions"]:
                        if k not in parsed:
                            parsed[k] = None
                    # Ensure types
                    if parsed.get("languages") is not None and not isinstance(parsed["languages"], list):
                        parsed["languages"] = [str(parsed["languages"])]
                    if parsed.get("questions") is not None and not isinstance(parsed["questions"], list):
                        parsed["questions"] = [str(parsed["questions"])]

                    self.extracted_slots = parsed
                    self._persist_state(conversation_id)
                else:
                    logger.warning("LLM extraction did not return a dict; keeping previous slots.")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(retry_delay)
                        continue
                    raise ValueError("Failed to parse valid JSON after retries")

            except Exception as e:
                logger.error(f"Slot extraction failed (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay)
                    continue
                raise  # Re-raise after final attempt

    async def end_call(self, conversation_id: str):
        """End the call by returning a TwiML Hangup response."""
        twiml_response = '<?xml version="1.0" encoding="UTF-8"?><Response><Hangup/></Response>'
        await self.send_message(BaseMessage(text=twiml_response), conversation_id)  # Use existing send_message to pass TwiML
        logger.info(f"Call ended for conversation_id: {conversation_id}")

    async def respond(self, human_input: str, conversation_id: str, is_interrupt: bool = False) -> Tuple[Optional[str], bool]:
        try:
            start_time = time.time()

            if conversation_id and self.conversation_id_cache != conversation_id:
                self.conversation_id_cache = conversation_id
            current_id = self.conversation_id_cache or conversation_id or "unknown"

            if human_input:
                self.turns.append({"speaker": "user", "text": human_input, "ts": int(time.time()*1000)})
                if len(self.turns) % 2 == 0:
                    asyncio.create_task(self._extract_slots_with_llm(current_id))
                self._persist_state(current_id)

            def personalize_response(text: str) -> str:
                if self.user_name:
                    return text.replace("{name}", self.user_name)
                external_name = "there"
                return text.replace("{name}", external_name)

            if time.time() - self.last_response_time > 15:
                self.no_input_count += 1
                logger.warning(f"No transcription for 15s (attempt {self.no_input_count})")
                if self.no_input_count >= 3:
                    bot_text = personalize_response("Trouble connecting. I’ll follow up later. Thank you!")
                    self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
                    self._persist_state(current_id)
                    await self.end_call(conversation_id)  # New: End the call
                    return bot_text, True
                bot_text = personalize_response("I didn’t catch that. Available to discuss chess coaching?")
                self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
                self._persist_state(current_id)
                return bot_text, False

            normalized = (human_input or "").strip().lower()
            filler_phrases = {"", "mhmm", "okay", "what", "yes", "no", "a-", "four", "hello", "hi"}
            if normalized in filler_phrases:
                self.no_input_count += 1
                logger.debug(f"Filler input (count {self.no_input_count}): '{human_input}'")
                if self.no_input_count >= 3:
                    bot_text = personalize_response("No valid input. I’ll follow up later. Thank you!")
                    self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
                    self._persist_state(current_id)
                    return bot_text, True
                self.last_response_time = start_time
                bot_text = personalize_response("Didn’t catch that. Confirm availability?")
                self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
                self._persist_state(current_id)
                return bot_text, False

            gibberish_indicators = ["what is the first time", "first time", "please repeat", "say again"]
            if any(phrase in normalized for phrase in gibberish_indicators):
                self.no_input_count += 1
                logger.debug(f"Gibberish input (count {self.no_input_count}): '{human_input}'")
                if self.no_input_count >= 3:
                    bot_text = personalize_response("Trouble connecting. I’ll follow up later. Thank you!")
                    self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
                    self._persist_state(current_id)
                    return bot_text, True
                self.last_response_time = start_time
                bot_text = personalize_response("Sorry, repeat or say yes/no if available?")
                self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
                self._persist_state(current_id)
                return bot_text, False

            self.no_input_count = 0

            if self.asked_for_name and "name is" in normalized:
                try:
                    name_part = human_input.lower().split("name is", 1)[1].strip().split()
                    self.user_name = name_part[0].capitalize()
                    logger.debug(f"Extracted user name: {self.user_name}")
                except Exception:
                    self.user_name = None

            slots = self.extracted_slots
            intent = slots.get("intent")

            # FAQ handling
            if any(q in normalized for q in ["price", "pricing", "cost", "timings", "time", "services"]):
                if "price" in normalized or "cost" in normalized:
                    response = "Our fees start at ₹500/hour, varying by experience. Want more details?"
                elif "timings" in normalized or "time" in normalized:
                    response = "Coaching is 3-6 PM school hours. Flexible options available—discuss?"
                elif "services" in normalized:
                    response = "We offer curricula, training, and school placements. More questions?"
                self.last_response_time = start_time
                self.turns.append({"speaker": "bot", "text": response, "ts": int(time.time()*1000)})
                self._persist_state(current_id)
                return response, False

            # NEW: Real-time sentiment-based routing
            sentiment = await sentiment_chain.ainvoke({"transcript": "\n".join(t["text"] for t in self.turns)})
            if sentiment["sentiment"] == "angry" or "upset" in normalized:
                logger.info("Detected angry tone, routing to calm rep")
                bot_text = "I’ll connect you with a calm rep to assist you."
                self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
                self._persist_state(current_id)
                return bot_text, True

            if self.conversation_state == "initial":
                if any(word in normalized for word in ["yes", "sure", "okay", "available"]):
                    self.conversation_state = "background"
                    response = "Great! Due to your interest, confirm your Bangalore location?"
                else:
                    response = personalize_response("Sorry, misheard. Available to discuss coaching?")
                self.last_response_time = start_time
                self.turns.append({"speaker": "bot", "text": response, "ts": int(time.time()*1000)})
                self._persist_state(current_id)
                return response, False
            else:
                try:
                    response, should_end = await asyncio.wait_for(
                        super().respond(human_input, conversation_id, is_interrupt), timeout=5.0
                    )
                except asyncio.TimeoutError:
                    fallback_msg = personalize_response("Response delayed. Try again shortly.")
                    self.turns.append({"speaker": "bot", "text": fallback_msg, "ts": int(time.time()*1000)})
                    self._persist_state(current_id)
                    await self.end_call(conversation_id)  # New: End call on timeout
                    return fallback_msg, True

                if response:
                    response_text = personalize_response(response)
                    if "location" in response_text.lower():
                        self.conversation_state = "background"
                    if any(phrase in response_text.lower() for phrase in ["confirm your full name", "may i have your name"]):
                        self.asked_for_name = True

                    if intent == "interested" and "schedule" in response_text.lower():
                        available_slots = await check_calendar_availability(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                        if available_slots["available"]:
                            bot_text = f"Great! Available slots: {', '.join(available_slots['slots'])}. Provide name, email, and preferred time?"
                            self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
                            self._persist_state(current_id)
                            return bot_text, False
                        else:
                            bot_text = "No slots available now. I’ll follow up. Thank you!"
                            self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
                            self._persist_state(current_id)
                            await self.end_call(conversation_id)  # New: End the call
                            return bot_text, True

                    if intent == "support":
                        bot_text = "Let me route you to our support team."
                        self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
                        self._persist_state(current_id)
                        return bot_text, True
                    elif intent == "interested":
                        bot_text = "Impressive! Connecting you to a sales rep."
                        self.turns.append({"speaker": "bot", "text": bot_text, "ts": int(time.time()*1000)})
                        self._persist_state(current_id)
                        await self.end_call(conversation_id)  # New: End call after routing
                        return bot_text, True

                    self.last_response_time = start_time
                    self.turns.append({"speaker": "bot", "text": response_text, "ts": int(time.time()*1000)})
                    if len(self.turns) % 4 == 0:
                        asyncio.create_task(self._extract_slots_with_llm(current_id))
                    self._persist_state(current_id)
                    return response_text, should_end

                fallback_msg = personalize_response("Didn’t get that. Tell me more?")
                self.last_response_time = start_time
                self.turns.append({"speaker": "bot", "text": fallback_msg, "ts": int(time.time()*1000)})
                self._persist_state(current_id)
                return fallback_msg, False

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            fallback_error_msg = "Error occurred. Try again."
            self.turns.append({"speaker": "bot", "text": fallback_error_msg, "ts": int(time.time()*1000)})
            current_id = self.conversation_id_cache or conversation_id or "unknown"
            self._persist_state(current_id)
            return fallback_error_msg, False
    








# Custom Deepgram Transcriber with keepalive and chunk logging
class CustomDeepgramTranscriber(DeepgramTranscriber):
    def __init__(self, transcriber_config: DeepgramTranscriberConfig):
        super().__init__(transcriber_config)
        self.audio_buffer = io.BytesIO()
        self.conversation_id = None

    async def process(self, audio_chunk: bytes):
        logger.debug(f"Processing audio chunk size: {len(audio_chunk)} bytes")
        if not audio_chunk or len(audio_chunk) == 0:
            logger.warning("Empty audio chunk - skipping")
            return None
        try:
            async with self.buffer_lock:
                if self.conversation_id:
                    total_size = self.audio_buffer.tell() + len(audio_chunk)
                    if total_size > 10 * 1024 * 1024:  # 10MB limit
                        await self._save_audio()
                    self.audio_buffer.write(audio_chunk)
            return await super().process(audio_chunk)
        except Exception as e:
            logger.error(f"Deepgram process error: {e}")
            raise
    

    async def keepalive(self):
        while True:
            await asyncio.sleep(10)
            try:
                await super().process(b"\x00" * 160)
                logger.debug("Deepgram keepalive sent")
            except Exception as e:
                logger.error(f"Keepalive failed: {e}")
                break


    def set_conversation_id(self, conversation_id: str):
        if self.conversation_id != conversation_id:
            if self.audio_buffer.tell() > 0:
                asyncio.create_task(self._save_audio())
            self.conversation_id = conversation_id
            self.audio_buffer = io.BytesIO()

    async def _save_audio(self):
        if self.conversation_id and self.audio_buffer.tell() > 0:
            self.audio_buffer.seek(0)
            audio_path = RECORDINGS_DIR / f"{self.conversation_id}.wav"
            with open(audio_path, 'wb') as f:
                f.write(self.audio_buffer.getbuffer())
            logger.info(f"Saved audio to {audio_path}")
            self.audio_buffer = io.BytesIO()

# Custom Agent Factory
class CustomAgentFactory:
    def create_agent(self, agent_config: AgentConfig, logger: Optional[logging.Logger] = None) -> BaseAgent:
        log = logger or globals().get('logger', logging.getLogger(__name__))
        log.debug(f"Creating agent with config type: {agent_config.type}")
        if agent_config.type == "agent_langchain":
            log.debug("Creating CustomLangchainAgent")
            return CustomLangchainAgent(agent_config=typing.cast(CustomLangchainAgentConfig, agent_config))
        log.error(f"Invalid agent config type: {agent_config.type}")
        raise Exception(f"Invalid agent config: {agent_config.type}")

# Custom Synthesizer Factory
class CustomSynthesizerFactory:
    def create_synthesizer(self, synthesizer_config: SynthesizerConfig) -> BaseSynthesizer:
        logger.debug(f"Creating synthesizer with config: {synthesizer_config}")
        if isinstance(synthesizer_config, StreamElementsSynthesizerConfig):
            logger.debug("Creating StreamElementsSynthesizer")
            return StreamElementsSynthesizer(synthesizer_config)
        logger.error(f"Invalid synthesizer config type: {synthesizer_config.type}")
        raise Exception(f"Invalid synthesizer config: {synthesizer_config.type}")

# FastAPI App
app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.debug("Starting up FastAPI application")
    logger.debug("Registered routes:")
    for route in app.routes:
        methods = getattr(route, "methods", ["WebSocket"])
        logger.debug(f" - {route.path} ({methods})")
    yield
    # ADDED: final sweep to persist any in-memory conversations at shutdown
    try:
        for conv_id in list(CONVERSATION_STORE.keys()):
            out_path = CONVERSATIONS_DIR / f"{conv_id}.json"
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(CONVERSATION_STORE[conv_id], f, ensure_ascii=False, indent=2)
        logger.debug("Shutdown flush completed for all conversations")
    except Exception as e:
        logger.error(f"Error during shutdown flush: {e}")
    logger.debug("Shutting down FastAPI application")

app.router.lifespan_context = lifespan

# Twilio config
twilio_config = TwilioConfig(
    account_sid=TWILIO_ACCOUNT_SID,
    auth_token=TWILIO_AUTH_TOKEN,
    phone_number=TWILIO_PHONE_NUMBER
)

# Synthesizer config (telephone voice output)
synthesizer_config = StreamElementsSynthesizerConfig.from_telephone_output_device(
    voice="Brian"
)

transcriber_config = DeepgramTranscriberConfig(
    api_key=DEEPGRAM_API_KEY,
    model="nova-2-phonecall",
    language="en",
    sampling_rate=8000,  # int primitive, not enum
    audio_encoding="mulaw",  # lowercase string, not enum
    chunk_size=320,
    endpointing_config=PunctuationEndpointingConfig(),
    downsampling=1,
)

agent_config = LangchainAgentConfig(
    initial_message=BaseMessage(text="Hello, this is Priya from 4champz, a leading chess coaching service in Bengaluru. Do you have 5-10 minutes to discuss some exciting chess coaching opportunities with schools in Bangalore?"),
    prompt_preamble=CHESS_COACH_PROMPT_PREAMBLE,
    model_name="llama-3.1-8b-instant",
    # model_name="groq/compound-mini",
    api_key=GROQ_API_KEY,
    provider="groq",
)



# Telephony Server setup
telephony_server = TelephonyServer(
    base_url=BASE_URL,  # your ngrok url
    config_manager=config_manager,
    inbound_call_configs=[
        TwilioInboundCallConfig(
            url="/inbound_call",
            twilio_config=twilio_config,
            config_manager=config_manager,
            agent_config=agent_config,
            synthesizer_config=synthesizer_config,
            transcriber_config=transcriber_config,  # Use instance
            twiml_fallback_response='''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>I didn't hear a response. Are you still there? Please say something to continue.</Say>
    <Pause length="15"/>
    <Redirect method="POST">/inbound_call</Redirect>
</Response>''',
            record=True,
            status_callback=f"https://{BASE_URL}/call_status",  # NEW: Added for inbound call status
            status_callback_method="POST",
            status_callback_event=["completed"]  # Trigger on call completion
        )
    ],
    agent_factory=CustomAgentFactory(),
    synthesizer_factory=CustomSynthesizerFactory(),
    events_manager=ChessEventsManager(),
)

# Add routes to FastAPI app
app.include_router(telephony_server.get_router())


# NEW: Endpoint to handle Twilio call status callbacks for inbound calls
@app.post("/call_status")
async def call_status(request: Request):
    data = await request.json()
    call_sid = data.get("CallSid")
    if data.get("CallStatus") == "completed":
        logger.info(f"Inbound call {call_sid} completed")
    return {"ok": True}


# NEW: Endpoint to serve conversation JSON files
@app.get("/conversations/{call_sid}.json")
async def get_conversation(call_sid: str):
    path = CONVERSATIONS_DIR / f"{call_sid}.json"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    raise HTTPException(status_code=404, detail="Conversation not found")


# ADDED n8n: request schema for outbound_call
class OutboundCallRequest(BaseModel):
    to_phone: str
    lead: Optional[Dict[str, Any]] = None
    transcript_callback_url: Optional[str] = None
    call_type: str = "qualification"
    agent_type: str = "chess_coach"
    initial_message: str = "Hello, this is a default message."
    prompt_preamble: str = ""



# ADDED n8n: normalize to E164 basic
def normalize_e164(number: str) -> str:
    n = re.sub(r'\D+', '', number or '')
    if not n:
        return number
    if n.startswith('0'):
        n = n.lstrip('0')
    if not n.startswith('+'):
        if len(n) == 10:
            n = '+91' + n
        else:
            n = '+' + n
    return n

# ADDED n8n: HTTP endpoint to start outbound call from n8n
@app.post("/outbound_call")
async def outbound_call(req: OutboundCallRequest):
    try:
        logger.info(
            "OUTBOUND payload -> agent_type=%s | init_len=%d | init_head=%r | prompt_len=%d | prompt_head=%r",
            req.agent_type,
            len(req.initial_message or ""),
            (req.initial_message or "")[:120],
            len(req.prompt_preamble or ""),
            (req.prompt_preamble or "")[:120],
        )
        to_phone = normalize_e164(req.to_phone)
        if not to_phone or len(to_phone) < 10:
            raise HTTPException(status_code=400, detail="Invalid phone")
        
        agent_type = req.agent_type.strip()
        initial_message = req.initial_message.strip()
        prompt_preamble = req.prompt_preamble.strip()

        agent_config = LangchainAgentConfig(
            initial_message=BaseMessage(text=initial_message),
            prompt_preamble=prompt_preamble,
            model_name="llama-3.1-8b-instant",
            api_key=GROQ_API_KEY,
            provider="groq",
        )


        call_key = f"outbound_{int(time.time()*1000)}_{hash(to_phone)}"

        # CHANGED: await save to shared config_manager singleton for consistency
        res = config_manager.save_config(call_key, agent_config)
        if asyncio.iscoroutine(res):
            await res

        logger.info(f"Saved agent under call_key {call_key} with init_message head: {initial_message[:120]}")



        sid = await make_outbound_call(to_phone, req.call_type, req.lead, agent_type, agent_config, call_sid=call_key)

        lead = req.lead or {}
        lead["to_phone"] = to_phone
        LEAD_CONTEXT_STORE[sid] = lead
        logger.info(f"Outbound call requested via n8n: SID={sid}, lead={lead}")
        if req.transcript_callback_url:
            os.environ["TRANSCRIPT_CALLBACK_URL"] = req.transcript_callback_url
        return {"ok": True, "call_sid": sid}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"/outbound_call failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Outbound call helper
async def make_outbound_call(to_phone: str, call_type: str, lead: dict, agent_type: str, agent_config: AgentConfig, call_sid: str = None):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    twilio_base_url = f"https://{BASE_URL}"
    
    initial_message = agent_config.initial_message.text if agent_config.initial_message else f"Hello, this is a generic message for {call_type}."

    call_sid = call_sid or f"outbound_{int(time.time()*1000)}_{hash(to_phone)}"

    twiml_url = f"{twilio_base_url}/inbound_call?call_sid={call_sid}"


    call = await asyncio.get_event_loop().run_in_executor(
        None,
        lambda: client.calls.create(
            to=to_phone,
            from_=TWILIO_PHONE_NUMBER,
            url=twiml_url,
            status_callback=f"{twilio_base_url}/call_status",
            status_callback_method="POST",
            status_callback_event=["initiated", "ringing", "answered", "completed"],
            record=True,
            recording_channels="dual",
        )
    )
    logger.info(f"Call initiated: TwilioSID={call.sid} | type={call_type} | agent_type={agent_type}")

    res2 = config_manager.save_config(call.sid, agent_config)
    if asyncio.iscoroutine(res2):
        await res2

    logger.info(f"Mirrored agent save: custom_id={call_sid} -> TwilioSID={call.sid} with init_message head: {agent_config.initial_message.text[:120]}")


    if call.sid not in LEAD_CONTEXT_STORE:
        LEAD_CONTEXT_STORE[call.sid] = {"to_phone": to_phone, "call_type": call_type, **(lead or {})}
    CONVERSATION_STORE.setdefault(call.sid, {
        "conversation_id": call.sid,
        "updated_at": int(time.time()*1000),
        "lead": LEAD_CONTEXT_STORE.get(call.sid, {}),
        "slots": {},
        "turns": [{"speaker": "bot", "text": initial_message, "ts": int(time.time()*1000)}]
    })
    return call.sid




# NEW: Outbound Call Scheduler (for auto-dialing from CRM)
def outbound_scheduler():
    while True:
        response = requests.get(CRM_API_URL, headers={"Authorization": f"Bearer {CRM_API_KEY}"})
        if response.status_code == 200:
            leads = response.json().get("leads", [])  # Adjusted to 'leads' for generality
            for lead in leads:
                if lead.get("status") == "Call Pending":
                    call_type = lead.get("call_type", "qualification")
                    asyncio.run(make_outbound_call(lead["phone"], call_type, lead))
                    update_crm(lead["id"], "", {}, {}, "", status="Calling")
        time.sleep(300)  # Poll every 5 minutes
# Main entrypoint (updated to include scheduler)
if __name__ == "__main__":
    import uvicorn

    def run_server():
        logger.debug("Starting Uvicorn server")
        uvicorn.run(app, host="0.0.0.0", port=3000)

    # Start outbound scheduler in a thread
    scheduler_thread = threading.Thread(target=outbound_scheduler, daemon=True)
    scheduler_thread.start()

    run_server()