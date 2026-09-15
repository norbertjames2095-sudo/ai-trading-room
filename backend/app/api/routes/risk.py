from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from pydantic import BaseModel

router = APIRouter()

class RiskStatus(BaseModel):
    daily_loss: float
    daily_loss_limit: float
    exposure: float
    exposure_limit: float
    drawdown: float
    drawdown_limit: float
    kill_switch: bool

@router.get("/status", response_model=RiskStatus)
async def get_risk_status(db: AsyncSession = Depends(get_db)):
    """
    Get current risk status
    """
    return {
        "daily_loss": 0,
        "daily_loss_limit": 5000,
        "exposure": 0,
        "exposure_limit": 80000,
        "drawdown": 0,
        "drawdown_limit": 20000,
        "kill_switch": False
    }

@router.post("/kill-switch")
async def activate_kill_switch(db: AsyncSession = Depends(get_db)):
    """
    Activate the kill switch (emergency stop)
    """
    return {"message": "Kill switch activated"}

@router.get("/config")
async def get_risk_config(db: AsyncSession = Depends(get_db)):
    """
    Get risk configuration
    """
    return {}