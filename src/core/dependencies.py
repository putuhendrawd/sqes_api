# src/core/dependencies.py
import logging
from typing import Annotated, Generator
from fastapi import Depends
from sqlalchemy.orm import Session

from src.core.database import SessionLocal_mysql, SessionLocal_pg

logger = logging.getLogger(__name__)

def get_mysql_db() -> Generator[Session, None, None]:
    """
    Dependency to get a SQLAlchemy session for the MySQL database.
    Ensures the session is always closed after use.
    """
    db = SessionLocal_mysql()
    try:
        yield db
    finally:
        logger.debug("Closing MySQL database session.")
        db.close()

def get_pg_db() -> Generator[Session, None, None]:
    """
    Dependency to get a SQLAlchemy session for the PostgreSQL database.
    Ensures the session is always closed after use.
    """
    db = SessionLocal_pg()
    try:
        yield db
    finally:
        logger.debug("Closing PostgreSQL database session.")
        db.close()

# --- Annotated Dependencies for Cleaner Endpoints ---
DbMySQL = Annotated[Session, Depends(get_mysql_db)]
DbPg = Annotated[Session, Depends(get_pg_db)]
