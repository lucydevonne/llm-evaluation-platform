"""
Database Models Module
"""
from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func
from app.db.database import Base

class Experiment(Base):
    """Experiment table definition"""
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(String, nullable=False)
    responses = Column(JSON, nullable=False, default=list)
    models = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Experiment(id={self.id}, prompt={self.prompt})>"