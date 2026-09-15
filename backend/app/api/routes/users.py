from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from pydantic import BaseModel

router = APIRouter()

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    role: str

@router.get("/me", response_model=UserResponse)
async def get_current_user(db: AsyncSession = Depends(get_db)):
    """
    Get current user info (placeholder)
    """
    return {"id": "1", "username": "user", "email": "user@example.com", "role": "trader"}

@router.get("/")
async def list_users(db: AsyncSession = Depends(get_db)):
    """
    List all users (admin only)
    """
    return []