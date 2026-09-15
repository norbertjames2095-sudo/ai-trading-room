from typing import Optional, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class NewsProvider:
    """
    Abstract base class for news providers.
    """
    
    async def get_news(self, query: str, limit: int = 10) -> Optional[List[dict]]:
        raise NotImplementedError

class NewsAPIProvider(NewsProvider):
    """
    NewsAPI provider for financial news.
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2"
    
    async def get_news(self, query: str, limit: int = 10) -> Optional[List[dict]]:
        # Placeholder implementation
        logger.info(f"Fetching news for {query}")
        return []

class NewsCache:
    """
    Cache for news items.
    """
    
    def __init__(self):
        self.cache = {}
        self.ttl_seconds = 300  # Cache news for 5 minutes
    
    async def get_or_fetch(
        self,
        query: str,
        fetch_fn,
        force_refresh: bool = False
    ) -> Optional[List[dict]]:
        """
        Get news from cache or fetch if expired.
        """
        cache_key = f"news:{query}"
        
        if not force_refresh and cache_key in self.cache:
            cached_data = self.cache[cache_key]
            if self._is_fresh(cached_data):
                return cached_data["data"]
        
        # Fetch new data
        data = await fetch_fn(query)
        if data:
            self.cache[cache_key] = {
                "data": data,
                "timestamp": datetime.utcnow()
            }
        
        return data
    
    def _is_fresh(self, cached_entry: dict) -> bool:
        """Check if cached data is still fresh"""
        age = (datetime.utcnow() - cached_entry["timestamp"]).total_seconds()
        return age < self.ttl_seconds
