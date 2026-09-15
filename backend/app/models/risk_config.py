from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float, Integer, Boolean
from app.database import Base
import uuid

class RiskConfig(Base):
    __tablename__ = "risk_configs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), unique=True, nullable=False)
    max_risk_per_trade = Column(Float, default=0.02)  # 2%
    max_exposure_per_asset = Column(Float, default=0.10)  # 10%
    max_total_exposure = Column(Float, default=0.80)  # 80%
    max_daily_loss = Column(Float, default=0.05)  # 5%
    max_drawdown = Column(Float, default=0.20)  # 20%
    max_positions = Column(Integer, default=20)
    min_liquidity_ratio = Column(Float, default=2.0)
    max_slippage_bps = Column(Float, default=50)  # 50 bps
    max_correlation = Column(Float, default=0.95)
    volatility_limit = Column(Float, default=0.15)  # 15%
    kill_switch_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<RiskConfig {self.user_id}>"
