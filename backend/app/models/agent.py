from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum, Float, Integer
from app.database import Base
from enum import Enum as PyEnum
import uuid

class SignalType(str, PyEnum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    NO_TRADE = "NO_TRADE"

class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(500))
    agent_type = Column(String(50), nullable=False)  # e.g., "analyzer", "manager", "coordinator"
    is_active = Column(String, default="online")  # online, offline, degraded, halted
    model_used = Column(String(50))  # e.g., "gpt-3.5-turbo", "gpt-4"
    last_signal_time = Column(DateTime, nullable=True)
    total_signals = Column(Integer, default=0)
    successful_signals = Column(Integer, default=0)
    failed_signals = Column(Integer, default=0)
    average_confidence = Column(Float, default=0.0)
    total_api_calls = Column(Integer, default=0)
    total_api_cost = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Agent {self.name}>"