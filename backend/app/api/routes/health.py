from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "AI Trading Room Backend"
    }

@router.get("/status")
async def status():
    """Detailed status endpoint"""
    return {
        "status": "online",
        "database": "connected",
        "cache": "connected",
        "timestamp": datetime.utcnow().isoformat()
    }