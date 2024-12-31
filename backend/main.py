"""
Main Application Entry Point
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.endpoints import router
from app.db import init_db 
from app.db.database import engine
from app.db.models import Base, Experiment 
import uvicorn
import logging
import os
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="LLM Evaluation Platform")

# Ensure database directory exists
db_dir = os.path.dirname(os.path.abspath(__file__))
logger.info(f"Database directory: {db_dir}")

# Initialize database during startup
init_db()

# Create database tables
logger.info("Creating database tables...")
try:
    Base.metadata.create_all(bind=engine)
    logger.info("✓ Database tables created successfully")
except Exception as e:
    logger.error(f"Database initialization error: {str(e)}", exc_info=True)
    error_details = {
        "error_type": type(e).__name__,
        "error_message": str(e),
        "suggestion": "Check database connection and permissions"
    }
    logger.error(f"Database initialization details: {error_details}")
    raise RuntimeError(f"Failed to initialize database: {str(e)}") from e

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Add root endpoint
@app.get("/")
async def root():
    return JSONResponse({
        "status": "ok",
        "message": "LLM Evaluation Platform API is running",
    })

# Include router with /api prefix
app.include_router(router, prefix="/api")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    error_response: Dict[str, Any] = {
        "status": "error",
        "message": str(exc)
    }
    
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response
        )
    
    # Log unexpected errors
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    error_response["message"] = "Internal server error"
    return JSONResponse(
        status_code=500,
        content=error_response
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )