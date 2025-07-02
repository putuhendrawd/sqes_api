from pydantic import BaseModel, HttpUrl
from typing import Dict, Optional

# --- Pydantic models for structured, predictable API responses ---

class DocLinks(BaseModel):
    """Links to the API documentation."""
    swagger_ui: Optional[str]
    redoc: Optional[str]

class ModuleLinks(BaseModel):
    """Links to the primary API modules."""
    authentication: str
    metadata: str
    quality_control: str
    health: str

class AllLinks(BaseModel):
    """Container for all API links."""
    documentation: DocLinks
    modules: ModuleLinks

class RootResponse(BaseModel):
    """Defines the structure for the root API endpoint response."""
    service: str
    message: str
    version: str
    status: str
    links: AllLinks

