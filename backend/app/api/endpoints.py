"""
API Endpoints Module
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Experiment
from app.services.llm_service import LLMService
from typing import List, Dict, Any
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router without prefix 
router = APIRouter()
llm_service = LLMService()  # Initialize the LLM service

@router.post("/experiments")
async def create_experiment(request: Dict[str, Any], db: Session = Depends(get_db)):
    """Create and process a new experiment"""
    try:
        logger.info(f"Processing experiment with prompt: {request}")
        
        # Create experiment record
        db_experiment = Experiment(
            prompt=request["prompt"],
            responses=[],  
            models=request["models"]
        )
        
        # Get responses from each model
        responses = []
        for model in request["models"]:
            try:
                # Start timing for this model
                model_start_time = datetime.now()
                
                # Get response from model
                if "systemPrompt" in request:
                    response = await llm_service.get_response(
                        prompt=request["prompt"],
                        system_prompt=request["systemPrompt"],
                        model=model
                    )
                else:
                    response = await llm_service.get_response(
                        prompt=request["prompt"],
                        system_prompt="",
                        model=model
                    )
                
                # Calculate response time in milliseconds
                response_time = (datetime.now() - model_start_time).total_seconds() * 1000
                
                # Evaluate response quality
                accuracy, relevancy = llm_service._evaluate_response(response)
                
                # Add response with metrics 
                responses.append({
                    "model": model,
                    "response": response,
                    "metrics": {
                        "accuracy": accuracy,
                        "relevancy": relevancy,
                        "responseTime": round(response_time, 2)  # Round to 2 decimal places
                    }
                })
                
            except Exception as e:
                logger.error(f"Error getting response from {model}: {str(e)}")
                responses.append({
                    "model": model,
                    "response": f"Error: {str(e)}",
                    "metrics": {
                        "accuracy": 0,
                        "relevancy": 0,
                        "responseTime": 0  # Zero response time for failed requests
                    }
                })
        
        # Update experiment with responses
        db_experiment.responses = responses
        
        # Save to database
        db.add(db_experiment)
        db.commit()
        db.refresh(db_experiment)
        
        logger.info(f"Created experiment with ID: {db_experiment.id}")
        return db_experiment

    except Exception as e:
        logger.error(f"Error creating experiment: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/experiments")
def get_experiments(db: Session = Depends(get_db)):
    """Get all experiments"""
    try:
        experiments = db.query(Experiment).all()
        logger.info(f"Retrieved {len(experiments)} experiments")
        return experiments
    except Exception as e:
        logger.error(f"Error retrieving experiments: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))