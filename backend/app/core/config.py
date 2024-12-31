"""
Configuration Module
------------------
Central configuration for the LLM Evaluation Platform.
Manages all application settings including API configuration, database settings,
and available AI models.
"""

from pydantic import BaseModel
from typing import List

class Settings(BaseModel):
    """
    Application Settings Class
    -------------------------
    Defines all configuration parameters for the application.
    Using Pydantic ensures all settings are properly typed and validated.
    """
    # Basic application information
    PROJECT_NAME: str = "LLM Evaluation Platform"    # Name of the application
    VERSION: str = "1.0.0"                          # Current version number
    API_V1_STR: str = ""                           # API version prefix (if needed)
    
    # CORS (Cross-Origin Resource Sharing) settings
    # Defines which frontend domains can access our API
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000"    # Default frontend development server
    ]
    
    # Database connection settings
    # SQLite database file location 
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # API Keys
    GROQ_API_KEY: str
    
    # List of AI models available for testing
    # These models can be selected in the frontend for comparison
    AVAILABLE_MODELS: List[str] = [
        "mixtral-8x7b",     # Using Groq's Mixtral-8x7b-32768
        "gpt-2"            # Using Hugging Face's GPT-2
    ]

# Create a single instance of settings to be used throughout the application
settings = Settings()

def get_settings() -> Settings:
    """
    Settings Getter
    --------------
    Returns the global settings instance.
    Used for dependency injection in FastAPI.
    """
    return settings