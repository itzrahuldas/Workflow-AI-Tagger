"""
FastAPI application entry point.
Defines the app, CORS, and all HTTP routes.
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings, Settings
from app.schemas import TextInput, TagResult, HealthResponse
from app.services.tagger import TaggerService

# ── Logging ─────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


# ── Lifespan (startup / shutdown) ────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    logger.info(f"🚀 Workflow-AI-Tagger starting up — model: {settings.model_name}")
    yield
    logger.info("🛑 Workflow-AI-Tagger shutting down")


# ── App ──────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Workflow-AI-Tagger",
    description=(
        "AI-powered text tagging API. "
        "Pass any large text and get back structured Tags + Summary "
        "using Groq LLM function calling."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Dependency ───────────────────────────────────────────────────────────────
def get_tagger(settings: Settings = Depends(get_settings)) -> TaggerService:
    return TaggerService(settings)


# ── Routes ───────────────────────────────────────────────────────────────────
@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check(settings: Settings = Depends(get_settings)) -> HealthResponse:
    """Health check endpoint — confirms the server and config are working."""
    return HealthResponse(status="healthy", model=settings.model_name)


@app.post("/analyze", response_model=TagResult, tags=["AI Tagger"])
async def analyze_text(
    payload: TextInput,
    tagger: TaggerService = Depends(get_tagger),
) -> TagResult:
    """
    Analyze text and return structured tags + summary.

    - **text**: The input text (10–10,000 characters)
    - **max_tags**: How many tags to extract (1–20, default 5)
    """
    logger.info(f"📥 /analyze — text_len={len(payload.text)}, max_tags={payload.max_tags}")
    try:
        result = await tagger.tag(payload.text, payload.max_tags)
        logger.info(f"✅ Tagged successfully — tags={result.tags}")
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"❌ Tagger error: {e}")
        raise HTTPException(status_code=500, detail=f"AI tagging failed: {str(e)}")
