# src/modules/health/routing.py
import logging 
from fastapi import APIRouter, HTTPException, status, Request
from typing import Dict, Any, Union
import firebase_admin
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, SQLAlchemyError
import time
from datetime import datetime, timezone
from src.core.config import settings
from src.core.database import SessionLocal_mysql, SessionLocal_pg

# Get a logger instance for this module
logger = logging.getLogger(__name__)

router = APIRouter()

# --- Health Check Caching Configuration ---
_cached_ready_result: Union[Dict[str, Any], None] = None
_last_ready_check_time: float = 0.0
# Cache duration should ideally come from settings for easy configuration
CACHE_DURATION_SECONDS: int = settings.HEALTH_CHECK_CACHE_DURATION_SECONDS

# --- Helper Function for Database Connectivity Check ---
def _check_database_connectivity(
    db_session_factory, 
    component_name: str
) -> Dict[str, Any]:
    """
    Checks connectivity to a database using the provided session factory.

    Args:
        db_session_factory: A callable (e.g., SessionLocal_mysql or SessionLocal_pg)
                            that returns a context manager yielding a SQLAlchemy Session.
        component_name: The name of the database component (e.g., "mysql_database").

    Returns:
        A dictionary with "status" ("UP" or "DOWN") and a "message" for the component.
    """
    try:
        with db_session_factory() as db_session:
            db_session.execute(text("SELECT 1")).scalar()
            logger.info(f"Database connectivity check for {component_name}: UP. Successfully connected.")
            return {
                "status": "UP",
                "message": f"Successfully connected to {component_name.replace('_', ' ').title()}."
            }
    except (OperationalError, SQLAlchemyError) as e:
        error_message_full = str(e)
        display_message = error_message_full.split('\n', 1)[0]
        if " on '" in display_message:
            display_message = display_message.split(" on '")[0]
        
        logger.error(f"Database connectivity check for {component_name}: DOWN. Error: {display_message}", exc_info=False) 
        return {
            "status": "DOWN",
            "message": f"Failed to connect to {component_name.replace('_', ' ').title()}: {display_message}"
        }

# --- Root Health Check Endpoint ---
@router.get("/", status_code=status.HTTP_200_OK, response_model=Dict[str, Any])
async def health_api_root() -> Dict[str, Any]:
    """
    Root endpoint for the health API module.
    Provides a general overview and directs to specific health check endpoints.
    """
    current_time_utc = datetime.now(timezone.utc)
    timestamp = current_time_utc.isoformat(timespec='milliseconds') + 'Z'

    logger.info("Health API root accessed.")
    return {
        "service": "SQES API 2025 Health Module",
        "message": "Welcome to the Health API module! Check /live or /ready for status.",
        "version": settings.APP_VERSION,
        "timestamp_utc": timestamp,
        "endpoints": {
            "/live": "Liveness probe: checks if the application is running.",
            "/ready": "Readiness probe: checks if the application is ready to serve requests (including external dependencies)."
        },
        "status": "HEALTH_API_ROOT_UP"
    }

# --- Liveness Check Endpoint ---
@router.get("/live", status_code=status.HTTP_200_OK, response_model=Dict[str, Any])
async def liveness_check(request: Request) -> Dict[str, Any]:
    """
    API Liveness Check Endpoint.

    Provides a simple check to indicate if the application process is running and responsive.
    This endpoint does not check external dependencies (like databases).
    """
    current_time_utc = datetime.now(timezone.utc)
    timestamp = current_time_utc.isoformat(timespec='milliseconds') + 'Z'

    # Safely get uptime from app.state (set in main.py lifespan)
    uptime_seconds = 0
    if hasattr(request.app.state, 'start_time'):
        uptime_seconds = int(time.time() - request.app.state.start_time)
    else:
        logger.warning("Application startup time (app.state.start_time) not set. Uptime will be 0.")

    logger.info("Liveness check endpoint accessed. Status: UP.")
    return {
        "service": "SQES API 2025",
        "status": "UP",
        "version": settings.APP_VERSION,
        "timestamp_utc": timestamp,
        "uptime_seconds": uptime_seconds,
        "message": "Application is live and responsive."
    }

# --- Readiness Check Endpoint ---
@router.get("/ready", status_code=status.HTTP_200_OK, response_model=Dict[str, Any])
async def readiness_check(request: Request) -> Dict[str, Any]:
    """
    API Readiness Check Endpoint.

    Provides a comprehensive overview of the application's health,
    including connectivity to core services like MySQL and PostgreSQL databases.
    Returns 200 OK if all critical components are operational,
    otherwise returns 503 Service Unavailable (via HTTPException).
    """
    global _cached_ready_result, _last_ready_check_time

    start_request_time = time.time()
    current_time_utc = datetime.now(timezone.utc)
    timestamp = current_time_utc.isoformat(timespec='milliseconds') + 'Z'

    # --- Check Cache ---
    if settings.ENABLE_HEALTH_CHECK_CACHE and (start_request_time - _last_ready_check_time < CACHE_DURATION_SECONDS):
        if _cached_ready_result:
            # Update timestamp and response_time for the cached result
            cached_result = _cached_ready_result.copy()
            cached_result["timestamp_utc"] = timestamp
            cached_result["response_time_ms"] = round((start_request_time - _last_ready_check_time) * 1000, 2)
            logger.info("Returning cached readiness check result.")
            
            # If cached result indicates degradation/down, still raise 503
            if cached_result["status"] in ["DEGRADED", "DOWN"]:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=cached_result
                )
            return cached_result

    # --- Perform Actual Health Checks if cache is stale or empty ---
    service_status = "UP"
    components_status: Dict[str, Dict[str, Any]] = {}

    # Check MySQL Database Connectivity
    mysql_status = _check_database_connectivity(SessionLocal_mysql, "mysql_database")
    components_status["mysql_database"] = mysql_status
    if mysql_status["status"] == "DOWN":
        service_status = "DEGRADED" 

    # Check PostgreSQL Database Connectivity
    pg_status = _check_database_connectivity(SessionLocal_pg, "postgresql_database")
    components_status["postgresql_database"] = pg_status
    if pg_status["status"] == "DOWN":
        service_status = "DEGRADED" 
    
    # Optional: Add other critical component checks (e.g., Firebase, external APIs)
    # Firebase is already initialized, but you could add a test connection if needed.
    if not firebase_admin._apps: # Basic check
        components_status["firebase_admin_sdk"] = {"status": "DOWN", "message": "Firebase Admin SDK not initialized."}
        service_status = "DEGRADED"
    else:
        components_status["firebase_admin_sdk"] = {"status": "UP", "message": "Firebase Admin SDK initialized."}


    end_request_time = time.time()
    response_time_ms = round((end_request_time - start_request_time) * 1000, 2)

    # Get uptime from app.state, which is set during lifespan startup
    uptime_seconds = 0
    if hasattr(request.app.state, 'start_time'):
        uptime_seconds = int(end_request_time - request.app.state.start_time)
    else:
        logger.warning("request.app.state.start_time is not set. Uptime will be 0.")

    health_response = {
        "service": "SQES API 2025",
        "status": service_status,
        "version": settings.APP_VERSION, # Use version from central settings
        "timestamp_utc": timestamp,
        "response_time_ms": response_time_ms,
        "uptime_seconds": uptime_seconds,
        "components": components_status
    }

    # Cache the result
    _cached_ready_result = health_response
    _last_ready_check_time = end_request_time

    # Always return 503 for critical failures for readiness probes
    # If any critical component is DOWN, the overall status should be 503
    # If it's DEGRADED, it might still return 200, but the status will reflect degradation.
    # The logic here is: if the overall 'service_status' is "DEGRADED" or "DOWN",
    # the HTTP status code should be 503. Otherwise, 200.
    if service_status in ["DEGRADED", "DOWN"]:
        logger.warning(f"Readiness check: Service status is {service_status}. Returning 503.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=health_response
        )

    logger.info(f"Readiness check: Service status is {service_status}. Returning 200.")
    return health_response