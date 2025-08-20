from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.core.config import settings 

# --- MySQL Database Configuration ---
URL_DATABASE_MYSQL = settings.DATABASE_URL_MYSQL
engine_mysql = create_engine(
    URL_DATABASE_MYSQL,
    pool_size=10,        
    max_overflow=20,     
    pool_recycle=3600,   
    pool_pre_ping=True,  
    echo=False           
)
SessionLocal_mysql = sessionmaker(autocommit=False, autoflush=False, bind=engine_mysql)
Base_mysql = declarative_base() 

# --- PostgreSQL Database Configuration ---
URL_DATABASE_PG = settings.DATABASE_URL_PG
engine_pg = create_engine(
    URL_DATABASE_PG,
    pool_size=10,        
    max_overflow=20,     
    pool_recycle=3600,   
    pool_pre_ping=True,  
    echo=False           
)
SessionLocal_pg = sessionmaker(autocommit=False, autoflush=False, bind=engine_pg)
Base_pg = declarative_base() 