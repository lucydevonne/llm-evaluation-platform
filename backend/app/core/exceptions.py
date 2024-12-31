"""
Custom Exceptions Module
----------------------
Defines custom error types for the LLM Evaluation Platform.
These exceptions help provide clear error messages and appropriate HTTP status codes
when something goes wrong during AI model interactions.
"""

from fastapi import HTTPException
from typing import Any, Dict, Optional

class LLMServiceError(HTTPException):
    """
    Base Exception for LLM Service
    -----------------------------
    Parent class for all LLM-related errors. Extends FastAPI's HTTPException
    to ensure proper error handling in the API.
    
    Attributes:
        detail: Human-readable error description
        status_code: HTTP status code (default 500)
        headers: Optional HTTP headers to include in response
    """
    def __init__(
        self,
        detail: str,
        status_code: int = 500,
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.headers = headers

class ModelNotFoundError(LLMServiceError):
    """
    Model Not Found Exception
    ------------------------
    Raised when trying to use an AI model that doesn't exist or isn't configured.
    Returns HTTP 404 status code.
    
    Example:
        Trying to use "gpt-4" when it's not in our available models list.
    
    Args:
        model: Name of the model that wasn't found
    """
    def __init__(self, model: str):
        super().__init__(
            status_code=404,
            detail=f"Model {model} not found or not available"
        )

class EvaluationError(LLMServiceError):
    """
    Model Evaluation Exception
    ------------------------
    Raised when an AI model fails to process a prompt.
    Returns HTTP 500 status code.
    
    Examples:
        - API timeout
        - Invalid response format
        - Model overloaded
    
    Args:
        model: Name of the model that failed
        reason: Detailed explanation of what went wrong
    """
    def __init__(self, model: str, reason: str):
        super().__init__(
            status_code=500,
            detail=f"Evaluation failed for model {model}: {reason}"
        ) 