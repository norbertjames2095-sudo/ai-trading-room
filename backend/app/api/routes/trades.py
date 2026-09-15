from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from pydantic import BaseModel
from typing import List
from enum import Enum

router = APIRouter()

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"

class TradeResponse(BaseModel):
    id: str
    asset: str
    direction: str
    quantity: float
    status: OrderStatus

@router.get("/", response_model=List[TradeResponse])
async def list_trades(db: AsyncSession = Depends(get_db)):
    """
    List all trades/orders
    """
    return []

@router.post("/")
async def create_trade(db: AsyncSession = Depends(get_db)):
    """
    Create a new trade (manual or auto)
    """
    return {"message": "Trade created"}

@router.get("/{trade_id}")
async def get_trade(trade_id: str, db: AsyncSession = Depends(get_db)):
    """
    Get trade details
    """
    return {}