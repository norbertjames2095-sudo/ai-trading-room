from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float, Integer, JSON, ForeignKey
from app.database import Base
import uuid

class AgentSignal(Base):
    __tablename__ = "agent_signals"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id = Column(String, ForeignKey("agents.id"), nullable=False)
    asset = Column(String(20), nullable=False)  # e.g., "BTC/USD"
    timeframe = Column(String(10), nullable=False)  # e.g., "1h", "4h"
    signal = Column(String(20), nullable=False)  # BUY, SELL, HOLD, NO_TRADE
    confidence = Column(Float, nullable=False)
    reasoning_summary = Column(String(1000))
    key_factors = Column(JSON)  # List of factors
    risks = Column(JSON)  # List of risks
    data_quality = Column(Float)
    recommended_entry = Column(Float, nullable=True)
    recommended_stop = Column(Float, nullable=True)
    recommended_target = Column(Float, nullable=True)
    model_used = Column(String(50))
    api_cost = Column(Float, default=0.0)
    latency_ms = Column(Integer)  # API call latency
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<AgentSignal {self.agent_id}:{self.asset}:{self.signal}>"