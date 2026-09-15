from abc import ABC, abstractmethod
from typing import Optional, Dict
from datetime import datetime
from enum import Enum
import json

class SignalType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    NO_TRADE = "NO_TRADE"

class BaseAgent(ABC):
    """
    Base class for all trading agents.
    All agents must inherit from this and implement analyze().
    """
    
    def __init__(self, name: str, agent_type: str):
        self.name = name
        self.agent_type = agent_type
        self.last_signal_time = None
        self.total_signals = 0
        self.successful_signals = 0
        self.failed_signals = 0
        self.average_confidence = 0.0
        self.total_api_calls = 0
        self.total_api_cost = 0.0
    
    @abstractmethod
    async def analyze(
        self,
        asset: str,
        timeframe: str,
        market_data: Dict,
        **kwargs
    ) -> Dict:
        """
        Main analysis method. Must be implemented by each agent.
        
        Returns standardized signal format:
        {
            "agent": "Agent Name",
            "timestamp": "ISO timestamp",
            "asset": "BTC/USD",
            "timeframe": "1h",
            "signal": "BUY|SELL|HOLD|NO_TRADE",
            "confidence": 0.0-1.0,
            "reasoning_summary": "...",
            "key_factors": [...],
            "risks": [...],
            "data_quality": 0.0-1.0,
            "recommended_entry": float,
            "recommended_stop": float,
            "recommended_target": float
        }
        """
        pass
    
    def _create_signal(
        self,
        asset: str,
        timeframe: str,
        signal: SignalType,
        confidence: float,
        reasoning: str,
        key_factors: list,
        risks: list,
        data_quality: float,
        entry: Optional[float] = None,
        stop: Optional[float] = None,
        target: Optional[float] = None,
        model: Optional[str] = None,
        api_cost: float = 0.0,
        latency_ms: int = 0
    ) -> Dict:
        """
        Create standardized signal output.
        """
        # Validate inputs
        if not (0 <= confidence <= 1):
            confidence = 0.5
        if not (0 <= data_quality <= 1):
            data_quality = 0.5
        
        self.total_signals += 1
        self.total_api_calls += 1
        self.total_api_cost += api_cost
        self.average_confidence = (
            (self.average_confidence * (self.total_signals - 1) + confidence) / 
            self.total_signals
        )
        self.last_signal_time = datetime.utcnow()
        
        return {
            "agent": self.name,
            "timestamp": datetime.utcnow().isoformat(),
            "asset": asset,
            "timeframe": timeframe,
            "signal": signal.value,
            "confidence": round(confidence, 3),
            "reasoning_summary": reasoning,
            "key_factors": key_factors,
            "risks": risks,
            "data_quality": round(data_quality, 3),
            "recommended_entry": entry,
            "recommended_stop": stop,
            "recommended_target": target,
            "model_used": model,
            "api_cost": api_cost,
            "latency_ms": latency_ms
        }
    
    def _create_no_trade(
        self,
        asset: str,
        timeframe: str,
        reason: str,
        data_quality: float = 0.0
    ) -> Dict:
        """
        Create NO_TRADE signal (invalid or missing data).
        """
        return self._create_signal(
            asset=asset,
            timeframe=timeframe,
            signal=SignalType.NO_TRADE,
            confidence=0.0,
            reasoning=reason,
            key_factors=[],
            risks=["Insufficient data or invalid input"],
            data_quality=data_quality
        )
    
    def record_signal_result(self, was_correct: bool):
        """
        Record whether a signal was correct (after result is known).
        Used for agent performance tracking.
        """
        if was_correct:
            self.successful_signals += 1
        else:
            self.failed_signals += 1
    
    def get_performance_stats(self) -> Dict:
        """
        Get agent performance statistics.
        """
        total = self.successful_signals + self.failed_signals
        accuracy = (
            self.successful_signals / total if total > 0 else 0
        )
        
        return {
            "name": self.name,
            "type": self.agent_type,
            "total_signals": self.total_signals,
            "successful_signals": self.successful_signals,
            "failed_signals": self.failed_signals,
            "accuracy": round(accuracy, 3),
            "average_confidence": round(self.average_confidence, 3),
            "total_api_calls": self.total_api_calls,
            "total_api_cost": round(self.total_api_cost, 4),
            "average_cost_per_call": round(
                self.total_api_cost / max(self.total_api_calls, 1), 6
            ),
            "last_signal_time": self.last_signal_time.isoformat() if self.last_signal_time else None
        }

class MarketAnalyzerAgent(BaseAgent):
    """
    Base class for market analysis agents (trend, momentum, etc.)
    """
    pass

class PortfolioManagerAgent(BaseAgent):
    """
    Base class for portfolio management agents.
    """
    pass

class CoordinatorAgent(BaseAgent):
    """
    Base class for coordinator agents (Chief Trader, Risk Manager).
    """
    pass
