from typing import Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class MarketDataProvider:
    """
    Abstract base class for market data providers.
    Allows swapping providers without changing the system.
    """
    
    async def get_current_price(self, asset: str) -> Optional[Dict]:
        raise NotImplementedError
    
    async def get_historical_data(self, asset: str, timeframe: str, limit: int) -> Optional[list]:
        raise NotImplementedError
    
    async def get_volume(self, asset: str) -> Optional[float]:
        raise NotImplementedError

class AlphaVantageProvider(MarketDataProvider):
    """
    Alpha Vantage market data provider.
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"
    
    async def get_current_price(self, asset: str) -> Optional[Dict]:
        # Placeholder implementation
        logger.info(f"Fetching current price for {asset} from Alpha Vantage")
        return {
            "asset": asset,
            "price": 0.0,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def get_historical_data(self, asset: str, timeframe: str, limit: int) -> Optional[list]:
        # Placeholder implementation
        return []
    
    async def get_volume(self, asset: str) -> Optional[float]:
        # Placeholder implementation
        return 0.0

class CoinGeckoProvider(MarketDataProvider):
    """
    CoinGecko crypto data provider (free tier).
    """
    
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
    
    async def get_current_price(self, asset: str) -> Optional[Dict]:
        # Placeholder implementation
        logger.info(f"Fetching current price for {asset} from CoinGecko")
        return {
            "asset": asset,
            "price": 0.0,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def get_historical_data(self, asset: str, timeframe: str, limit: int) -> Optional[list]:
        # Placeholder implementation
        return []
    
    async def get_volume(self, asset: str) -> Optional[float]:
        # Placeholder implementation
        return 0.0

class MarketDataCache:
    """
    Cache for market data to reduce API calls.
    """
    
    def __init__(self):
        self.cache = {}
        self.ttl_seconds = 60  # Cache for 1 minute
    
    async def get_or_fetch(
        self,
        asset: str,
        fetch_fn,
        force_refresh: bool = False
    ) -> Optional[Dict]:
        """
        Get data from cache or fetch if expired.
        """
        cache_key = f"price:{asset}"
        
        if not force_refresh and cache_key in self.cache:
            cached_data = self.cache[cache_key]
            if self._is_fresh(cached_data):
                return cached_data["data"]
        
        # Fetch new data
        data = await fetch_fn(asset)
        if data:
            self.cache[cache_key] = {
                "data": data,
                "timestamp": datetime.utcnow()
            }
        
        return data
    
    def _is_fresh(self, cached_entry: Dict) -> bool:
        """Check if cached data is still fresh"""
        age = (datetime.utcnow() - cached_entry["timestamp"]).total_seconds()
        return age < self.ttl_seconds
