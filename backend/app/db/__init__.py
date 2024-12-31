"""
Database Package
--------------
This package handles all database operations and models for the LLM Evaluation Platform.
Includes database initialization, session management, and models.
"""

import os
import logging
from pathlib import Path
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .models import Experiment

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Version of the database package
__version__ = '1.0.0'

# Database initialization
SQLALCHEMY_DATABASE_URL = "sqlite:///./data/app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DatabaseInitializationError(Exception):
    """Custom exception for database initialization errors"""
    pass

def init_db(force: bool = False) -> None:
    """
    Initialize the database and create all tables.
    
    Args:
        force (bool): If True, recreates the database even if it exists
    """
    try:
        db_path = Path("./data")
        db_file = db_path / "app.db"
        
        # Create data directory if it doesn't exist
        db_path.mkdir(parents=True, exist_ok=True)
        
        # Handle existing database
        if db_file.exists():
            if force:
                logger.warning(f"Removing existing database: {db_file}")
                db_file.unlink()
            else:
                logger.info(f"Database already exists at: {db_file}")
                return
        
        # Create new database and tables
        logger.info("Creating new database and tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("✓ Database initialized successfully!")
        logger.info(f"Database location: {db_file}")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}", exc_info=True)
        raise DatabaseInitializationError(f"Database initialization failed: {str(e)}")

def get_db():
    """
    Get database session with automatic closing.
    To be used in FastAPI dependency injection.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define public exports
__all__ = [
    'engine',
    'SessionLocal',
    'Base',
    'Experiment',
    'init_db',
    'get_db',
    'DatabaseInitializationError'
]

# Initialize database if this file is run directly
if __name__ == "__main__":
    init_db()