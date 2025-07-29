import os
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Centralized application settings management using Pydantic.
    Settings are loaded from environment variables or a .env file.
    """
    
    # --- Core Application Settings ---
    APP_NAME: str = Field("SQES Data API", description="The name of the application.")
    APP_VERSION: str = Field("0.0.1", description="The version of the application.")
    ENVIRONMENT: str = Field("development", description="The deployment environment (e.g., 'development', 'staging', 'production').")
    LOG_LEVEL: str = Field("INFO", description="Logging level for the application.")

    # --- API Documentation ---
    SHOW_DOCS: bool = Field(True, description="Flag to enable/disable API docs (Swagger, ReDoc). Should be False in production.")

    # --- Security Settings ---
    CORS_ORIGINS: List[str] = Field(default=["*"], description="List of allowed CORS origins.")
    ENABLE_DEBUG_BYPASS_TOKEN: bool = Field(False, description="Enable a debug bypass token for development. MUST be False in production.")

    # --- Database URLs ---
    DATABASE_URL_MYSQL: str = Field(..., description="Full connection string for the primary MySQL database.")
    DATABASE_URL_PG: str = Field(..., description="Full connection string for the primary PostgreSQL database.")

    # --- Firebase ---
    FIREBASE_SERVICE_ACCOUNT_KEY_PATH: str = Field(..., description="File path to the Firebase service account JSON key.")

    # --- Feature-specific Settings ---
    HEALTH_CHECK_CACHE_DURATION_SECONDS: int = Field(60, description="Cache duration for health check results.")
    ENABLE_HEALTH_CHECK_CACHE: bool = Field(True, description="Flag to enable/disable health check caching.")
    IMAGE_STORAGE_BASE_PATH: str = Field("/home/geo2sqes/SQESDATA", description="Base filesystem path for storing images.")
    PSD_IMAGE_SUBDIR: str = Field("PDFimage", description="Subdirectory for PSD images.")
    SIGNAL_IMAGE_SUBDIR: str = Field("signal", description="Subdirectory for signal images.")

    # --- Debugging and Development Settings ---
    DEBUG_BYPASS_TOKEN: str = Field("your-super-secret-debug-token", description="The token to bypass auth in debug mode. Should be complex.")

    model_config = SettingsConfigDict(
        env_file=".env_dev",
        env_file_encoding='utf-8',
        extra="ignore"
    )

# Create a single, importable instance of the settings
settings = Settings()

# --- Environment-specific Overrides ---
if settings.ENVIRONMENT == "production":
    settings.SHOW_DOCS = False
    settings.LOG_LEVEL = "WARNING"
    if settings.ENABLE_DEBUG_BYPASS_TOKEN:
        raise ValueError("CRITICAL SECURITY RISK: Debug bypass token cannot be enabled in a production environment.")
