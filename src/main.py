import logging
import sys
import time
from contextlib import asynccontextmanager
from typing import Dict, Any
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.core.database import engine_mysql, engine_pg
from src.core.firebase import initialize_firebase
from src.schemas import RootResponse
from src.auth import router as auth_router
from src.modules.health import router as health_router
from src.modules.metadata import router as metadata_router
from src.modules.qualitycontrol import router as qcresult_router

# --- Global Logging Configuration (CRITICAL for Production) ---
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


# --- Lifespan Context Manager (Modern FastAPI Startup/Shutdown) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for application startup and shutdown events.
    Handles initialization of critical resources and graceful cleanup.
    """
    logger.info("Application startup initiated.")
    app.state.start_time = time.time()

    logger.info("Initializing Firebase Admin SDK...")
    try:
        initialize_firebase(settings.FIREBASE_SERVICE_ACCOUNT_KEY_PATH)
        logger.info("Firebase Admin SDK initialization complete.")
    except Exception as e:
        logger.critical(f"CRITICAL ERROR: Failed to initialize Firebase Admin SDK. Application will not start: {e}", exc_info=True)
        raise

    yield

    # --- Application Shutdown ---
    logger.info("Application shutdown initiated.")
    if engine_mysql:
        logger.info("Disposing of MySQL database connections...")
        try:
            await engine_mysql.dispose()
            logger.info("MySQL database connections disposed successfully.")
        except Exception as e:
            logger.error(f"Error disposing of MySQL connections: {e}", exc_info=True)

    if engine_pg:
        logger.info("Disposing of PostgreSQL database connections...")
        try:
            await engine_pg.dispose()
            logger.info("PostgreSQL database connections disposed successfully.")
        except Exception as e:
            logger.error(f"Error disposing of PostgreSQL connections: {e}", exc_info=True)

    logger.info("Application shutdown complete.")


# --- FastAPI Application Instance ---
app = FastAPI(
    title=settings.APP_NAME,
    description="API for managing SQES Data, secured with Firebase Authentication.",
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.SHOW_DOCS else None,
    redoc_url="/redoc" if settings.SHOW_DOCS else None,
    lifespan=lifespan
)


# --- Middleware Configuration ---

# 1. CORS Middleware (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS, 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

# 2. Custom Middleware for Logging and Performance
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Middleware to add a custom X-Process-Time header to all responses
    and log request details for performance monitoring.
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    logger.info(
        f'Request: {request.method} {request.url.path} - Completed in {process_time:.4f}s - Status: {response.status_code}'
    )
    return response


# --- API Root Endpoint (Publicly Accessible) ---
@app.get("/", status_code=status.HTTP_200_OK, response_model=RootResponse, tags=["General"])
async def api_root() -> Dict[str, Any]:
    """
    Welcome to the SQES API 2025.

    This is the main entry point to explore available services and documentation.
    Provides service status, version, and links to key modules.
    """
    return {
        "service": settings.APP_NAME,
        "message": "Welcome to the SQES API 2025!",
        "version": settings.APP_VERSION,
        "status": "API_UP",
        "links": {
            "documentation": {
                "swagger_ui": app.docs_url,
                "redoc": app.redoc_url
            },
            "modules": {
                "authentication": "/api/auth",
                "metadata": "/api/metadata",
                "quality_control": "/api/qc",
                "health": "/api/health"
            }
        }
    }


# --- Mount the Routers ---
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(metadata_router, prefix="/api/metadata", tags=["Metadata"])
app.include_router(qcresult_router, prefix="/api/qc", tags=["Quality Control Data"])
app.include_router(health_router, prefix="/api/health", tags=["Health"])

