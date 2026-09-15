from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float, JSON
from app.database import Base
import uuid

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), index=True)
    action = Column(String(100), index=True)  # e.g., "SIGNAL_GENERATED", "ORDER_CREATED"
    asset = Column(String(20))
    decision_result_id = Column(String, ForeignKey("decision_results.id"))
    order_id = Column(String, ForeignKey("orders.id"))
    details = Column(JSON)  # Full details of the action
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<AuditLog {self.action}:{self.timestamp}>"
