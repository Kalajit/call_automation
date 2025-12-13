"""
AI Calling System - Main Application
Multi-tenant voice AI system with multilingual support
"""

import asyncio
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from vocode.streaming.telephony.server.base import TelephonyServer, TwilioInboundCallConfig
from vocode.streaming.models.telephony import TwilioConfig
from vocode.streaming.models.message import BaseMessage
from vocode.streaming.models.transcriber import DeepgramTranscriberConfig, PunctuationEndpointingConfig
from vocode.streaming.models.synthesizer import StreamElementsSynthesizerConfig
from vocode.streaming.telephony.config_manager.in_memory_config_manager import InMemoryConfigManager

# Configuration
from src.config.settings import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    BASE_URL,
    DEEPGRAM_API_KEY,
    GROQ_API_KEY,
    ALLOWED_ORIGINS,
    REQUIRE_HTTPS
)
from src.config.constants import get_fresh_metrics

# Database
from src.database import init_db, close_db

# Services
from src.services.multilingual_service import get_multilingual_service

# Calling
from src.calling.agent import CustomLangchainAgentConfig
from src.calling.factories import CustomAgentFactory, CustomSynthesizerFactory
from src.calling.events import ProductionEventsManager

# Scheduler
from src.scheduler import outbound_call_scheduler

# API Routes
from src.api.routes.calls import setup_calls_routes
from src.api.routes.webhooks import setup_webhook_routes
from src.api.routes.admin import router as admin_router
from src.api.routes.metrics import setup_metrics_routes

# Utilities
from src.utils.logging_config import setup_logging, get_logger

# Setup logging
setup_logging()
logger = get_logger(__name__)

# ============================================
# GLOBAL STATE
# ============================================

# In-memory stores (for active calls only)
ACTIVE_CALLS = {}  # call_sid -> call_data
CONVERSATION_STORE = {}  # call_sid -> conversation

# Rate limiting
CALL_SEMAPHORE = asyncio.Semaphore(10)

# Metrics
METRICS = get_fresh_metrics()

# ============================================
# APPLICATION LIFECYCLE
# ============================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """App lifecycle manager"""
    # Startup
    logger.info("🚀 Starting AI Calling System...")
    
    # Initialize multilingual service
    try:
        multilingual_service = get_multilingual_service('./google-credentials.json')
        logger.info("✅ Multilingual service initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize multilingual service: {e}")
        raise
    
    # Initialize database
    try:
        await init_db()
        logger.info("✅ Database initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {e}")
        raise
    
    # Start scheduler
    try:
        scheduler_task = asyncio.create_task(
            outbound_call_scheduler(
                CONVERSATION_STORE,
                ACTIVE_CALLS,
                METRICS,
                CALL_SEMAPHORE
            )
        )
        logger.info("✅ Scheduler started")
    except Exception as e:
        logger.error(f"❌ Failed to start scheduler: {e}")
        raise
    logger.info("✅ Scheduler started")
    
    logger.info("✅ App started successfully")
    
    yield
    
    # Shutdown
    logger.info("🔴 Shutting down...")
    try:
        scheduler_task.cancel()
        await close_db()
        logger.info("🔴 App shutdown complete")
    except Exception as e:
        logger.error(f"❌ Shutdown error: {e}")
    await close_db()
    logger.info("🔴 App shutdown complete")


# ============================================
# FASTAPI APPLICATION
# ============================================

app = FastAPI(
    title="AI Calling System",
    description="Multi-tenant voice AI system with multilingual support",
    version="1.0.0",
    lifespan=lifespan
)

# ============================================
# SECURITY MIDDLEWARE
# ============================================

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
    expose_headers=["X-RateLimit-Remaining", "X-RateLimit-Reset"]
)

# HTTPS Enforcement (production only)
if REQUIRE_HTTPS:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*.yourdomain.com", "localhost"]
    )
    logger.info("✅ HTTPS enforcement enabled")

# Request/Response Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests with timing and response status"""
    start_time = time.time()
    
    # Log incoming request
    logger.info(
        f"→ {request.method} {request.url.path} "
        f"from {request.client.host if request.client else 'unknown'}"
    )
    
    try:
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers if available
        if hasattr(request.state, "rate_limit_remaining"):
            response.headers["X-RateLimit-Remaining"] = str(request.state.rate_limit_remaining)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log response
        logger.info(
            f"← {request.method} {request.url.path} "
            f"completed in {process_time:.3f}s - Status: {response.status_code}"
        )
        
        return response
        
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(
            f"← {request.method} {request.url.path} "
            f"failed in {process_time:.3f}s - Error: {str(e)}",
            exc_info=True
        )
        raise

# Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add security headers to all responses"""
    response = await call_next(request)
    
    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    if REQUIRE_HTTPS:
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    return response

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle uncaught exceptions"""
    logger.error(
        f"Unhandled exception on {request.method} {request.url.path}: {str(exc)}",
        exc_info=True
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred. Please try again later.",
            "path": str(request.url.path)
        }
    )

# ============================================
# SETUP ROUTES WITH DEPENDENCIES
# ============================================

# Setup call routes

calls_router = setup_calls_routes(CONVERSATION_STORE, ACTIVE_CALLS, METRICS, CALL_SEMAPHORE)
app.include_router(calls_router)

# Setup webhook routes
webhooks_router = setup_webhook_routes(CONVERSATION_STORE, METRICS)
app.include_router(webhooks_router)

# Setup admin routes
app.include_router(admin_router)

# Setup metrics routes
metrics_router = setup_metrics_routes(ACTIVE_CALLS, METRICS)
app.include_router(metrics_router)

# ============================================
# VOCODE INTEGRATION
# ============================================
config_manager = InMemoryConfigManager() 

# Default agent config
default_agent_config = CustomLangchainAgentConfig(
    initial_message=BaseMessage(text="Hello, this is AI calling system."),
    prompt_preamble="You are a helpful assistant.",
    model_name="llama-3.1-8b-instant",
    api_key=GROQ_API_KEY,
    provider="groq"
)

# Default synthesizer config
default_synthesizer_config = StreamElementsSynthesizerConfig.from_telephone_output_device(
    voice="Brian"
)

# Default transcriber config
default_transcriber_config = DeepgramTranscriberConfig(
    api_key=DEEPGRAM_API_KEY,
    model="nova-2-phonecall",
    language="en",
    sampling_rate=8000,
    audio_encoding="mulaw",
    chunk_size=320,
    endpointing_config=PunctuationEndpointingConfig(),
    downsampling=1,
)

# Twilio config
twilio_config = TwilioConfig(
    account_sid=TWILIO_ACCOUNT_SID,
    auth_token=TWILIO_AUTH_TOKEN
)

# Telephony server with custom factories and events manager
telephony_server = TelephonyServer(
    base_url=BASE_URL,
    config_manager=config_manager,
    inbound_call_configs=[
        TwilioInboundCallConfig(
            url="/inbound_call",
            twilio_config=twilio_config,
            agent_config=default_agent_config,
            synthesizer_config=default_synthesizer_config,
            transcriber_config=default_transcriber_config,
            record=True,
            status_callback=f"https://{BASE_URL}/call_status",
            recording_status_callback=f"https://{BASE_URL}/recording_status"
        )
    ],
    agent_factory=CustomAgentFactory(CONVERSATION_STORE),
    synthesizer_factory=CustomSynthesizerFactory(),
    events_manager=ProductionEventsManager(CONVERSATION_STORE, ACTIVE_CALLS, METRICS)
)

# Include telephony routes
app.include_router(telephony_server.get_router())




@app.get("/health")
async def health_check():
    """
    Public health check endpoint
    No authentication required - used by load balancers and monitoring
    """
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "2.0.0",
        "active_calls": len(ACTIVE_CALLS)
    }

@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {    
        "service": "AI Calling System",
        "version": "2.0.0",
        "status": "running",
        "documentation": "/docs",
        "health": "/health"
    }

# ============================================
# RUN APPLICATION
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        access_log=True
    )