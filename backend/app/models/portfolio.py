from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float, Integer, JSON
from app.database import Base
import uuid

class Portfolio(Base):
    __tablename__ = "portfolios"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), unique=True, nullable=False)
    initial_capital = Column(Float, nullable=False)
    current_equity = Column(Float)
    available_cash = Column(Float)
    total_positions = Column(Integer, default=0)
    total_exposure = Column(Float, default=0.0)
    daily_pnl = Column(Float, default=0.0)
    daily_pnl_percent = Column(Float, default=0.0)
    total_pnl = Column(Float, default=0.0)
    total_pnl_percent = Column(Float, default=0.0)
    max_drawdown = Column(Float, default=0.0)
    current_drawdown = Column(Float, default=0.0)
    risk_exposure = Column(Float, default=0.0)
    sector_exposure = Column(JSON)  # Dict of sector: exposure
    asset_exposure = Column(JSON)  # Dict of asset: exposure
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Portfolio {self.user_id}>"
