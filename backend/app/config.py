from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache
import os

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://trading:trading_password@localhost:5432/trading_room"
    DATABASE_ECHO: bool = False
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_URL: str = "redis://localhost:6379/1"
    
    # Backend
    BACKEND_URL: str = "http://localhost:8000"
    BACKEND_PORT: int = 8000
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_WORKERS: int = 4
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    CORS_CREDENTIALS: bool = True
    CORS_ALLOW_HEADERS: str = "*"
    CORS_ALLOW_METHODS: str = "*"
    
    # AI Models
    AI_PROVIDER: str = "openai"
    AI_FAST_MODEL: str = "gpt-3.5-turbo"
    AI_POWERFUL_MODEL: str = "gpt-4"
    OPENAI_API_KEY: str = ""
    OPENAI_FAST_MODEL: str = "gpt-3.5-turbo"
    OPENAI_POWERFUL_MODEL: str = "gpt-4"
    ANTHROPIC_API_KEY: str = ""
    
    # Market Data
    MARKET_DATA_PROVIDER: str = "alpha-vantage"
    ALPHA_VANTAGE_API_KEY: str = ""
    
    # Risk Engine
    RISK_MAX_PER_TRADE: float = 0.02
    RISK_MAX_EXPOSURE_PER_ASSET: float = 0.10
    RISK_MAX_TOTAL_EXPOSURE: float = 0.80
    RISK_MAX_DAILY_LOSS: float = 0.05
    RISK_MAX_DRAWDOWN: float = 0.20
    RISK_MAX_POSITIONS: int = 20
    RISK_MIN_LIQUIDITY_RATIO: float = 2.0
    RISK_MAX_SLIPPAGE_BPS: float = 50
    RISK_MAX_CORRELATION: float = 0.95
    RISK_VOLATILITY_LIMIT: float = 0.15
    
    # AI Cost Management
    AI_BUDGET_MONTHLY_USD: float = 1000.0
    AI_BUDGET_ALERT_PERCENT: int = 80
    AI_TRACK_PER_MODEL: bool = True
    AI_TRACK_PER_AGENT: bool = True
    
    # Trading Modes
    TRADING_MODE: str = "paper"
    REQUIRE_MANUAL_APPROVAL: bool = True
    LIVE_MODE_ENABLED: bool = False
    LIVE_MODE_REQUIRES_2FA: bool = True
    
    # Security
    SESSION_TIMEOUT_MINUTES: int = 30
    TWO_FA_ENABLED: bool = True
    PASSWORD_MIN_LENGTH: int = 12
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCK_TIMEOUT_MINUTES: int = 15
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # Environment
    DEBUG: bool = False
    TESTING: bool = False
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()