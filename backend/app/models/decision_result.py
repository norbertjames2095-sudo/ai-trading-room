from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float, Integer, JSON
from app.database import Base
import uuid

class DecisionResult(Base):
    __tablename__ = "decision_results"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    asset = Column(String(20), nullable=False, index=True)
    timeframe = Column(String(10), nullable=False)
    final_signal = Column(String(20), nullable=False)  # BUY, SELL, HOLD, NO_TRADE
    opportunity_score = Column(Float, nullable=False)  # 0-100
    chief_trader_reasoning = Column(String(2000))
    agent_signals_count = Column(Integer)
    agent_signals = Column(JSON)  # Summary of all agent signals
    risk_manager_approval = Column(String(50))  # APPROVED, REJECTED, NEEDS_REVIEW
    risk_manager_reasoning = Column(String(1000))
    red_team_concerns = Column(JSON)  # Red team findings
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<DecisionResult {self.asset}:{self.final_signal}:{self.opportunity_score}>"
