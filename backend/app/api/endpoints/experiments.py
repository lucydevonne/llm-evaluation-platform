"""
Experiments API Module
--------------------
Handles creating and retrieving AI model comparison experiments.
Each experiment tests multiple AI models with the same prompt and stores their responses.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel
from app.db import get_db
from app.db.models import Experiment
from app.services.llm_service import llm_service

# Define schemas inline
class ExperimentCreate(BaseModel):
    prompt: str
    models: List[str]

class ExperimentResponse(BaseModel):
    id: int
    prompt: str
    responses: List[Dict[str, Any]]
    models: List[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

# Create router
router = APIRouter()

@router.post("/experiments", response_model=ExperimentResponse)
async def create_experiment(
    data: ExperimentCreate,
    db: Session = Depends(get_db)
):
    """
    Creates a new experiment by testing multiple AI models.
    
    Flow:
    1. Creates a database record for the experiment
    2. Sends the prompt to all requested AI models
    3. Stores their responses and performance metrics
    4. Returns the complete experiment results
    """
    start_time = datetime.now()
    
    # Step 1: Initialize experiment record
    experiment = Experiment(
        prompt=data.prompt,
        models=data.models,
        responses=[]  # Initialize empty responses list
    )
    
    # Step 2: Get responses from all requested AI models
    responses = []
    for model in data.models:
        try:
            response = await llm_service.get_response(
                prompt=data.prompt,
                model=model
            )
            
            # Calculate response time for this model
            model_response_time = (datetime.now() - start_time).total_seconds() * 1000
            
            responses.append({
                "model": model,
                "response": response,
                "metrics": {
                    "responseTime": round(model_response_time, 2)
                }
            })
            
        except Exception as e:
            responses.append({
                "model": model,
                "error": str(e),
                "metrics": {
                    "responseTime": 0
                }
            })
    
    # Step 3: Store the responses
    experiment.responses = responses
    
    # Step 4: Save to database
    db.add(experiment)
    db.commit()
    db.refresh(experiment)
    
    return experiment

@router.get("/experiments", response_model=List[ExperimentResponse])
def get_experiments(db: Session = Depends(get_db)):
    """
    Retrieves all previous experiments from the database.
    Returns a list of experiments with their prompts, AI responses, and metrics.
    """
    return db.query(Experiment).all()