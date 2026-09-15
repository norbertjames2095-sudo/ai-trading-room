from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float, Integer, Enum
from app.database import Base
from enum import Enum as PyEnum
import uuid

class OrderStatus(str, PyEnum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    EXECUTING = "EXECUTING"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    PARTIAL = "PARTIAL"

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    asset = Column(String(20), nullable=False)
    direction = Column(String(10), nullable=False)  # BUY or SELL
    quantity = Column(Float, nullable=False)
    entry_price = Column(Float)
    stop_price = Column(Float)
    target_price = Column(Float)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    decision_result_id = Column(String, ForeignKey("decision_results.id"))
    risk_manager_approved = Column(String, default="PENDING")
    manual_approved = Column(String, default="PENDING")
    trading_mode = Column(String(20), nullable=False)  # research, backtest, paper, live
    execution_price = Column(Float, nullable=True)
    execution_quantity = Column(Float, nullable=True)
    slippage_bps = Column(Float, default=0.0)
    commissions = Column(Float, default=0.0)
    pnl = Column(Float, nullable=True)
    pnl_percent = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    executed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Order {self.id}:{self.asset}:{self.direction}>"
