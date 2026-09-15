"""Tests for Agent Base Classes"""
import pytest
from app.agents.base import BaseAgent, SignalType

class MockAgent(BaseAgent):
    """Mock agent for testing"""
    
    async def analyze(self, asset: str, timeframe: str, market_data: dict, **kwargs):
        return self._create_signal(
            asset=asset,
            timeframe=timeframe,
            signal=SignalType.BUY,
            confidence=0.8,
            reasoning="Test signal",
            key_factors=["Factor1"],
            risks=["Risk1"],
            data_quality=0.9
        )

@pytest.fixture
def mock_agent():
    return MockAgent(name="TestAgent", agent_type="analyzer")

@pytest.mark.asyncio
async def test_agent_creates_valid_signal(mock_agent):
    """Test that agent creates valid signal format"""
    signal = await mock_agent.analyze(
        asset="BTC/USD",
        timeframe="1h",
        market_data={}
    )
    
    # Check required fields
    assert signal["agent"] == "TestAgent"
    assert signal["asset"] == "BTC/USD"
    assert signal["timeframe"] == "1h"
    assert signal["signal"] == "BUY"
    assert 0 <= signal["confidence"] <= 1
    assert 0 <= signal["data_quality"] <= 1
    assert "timestamp" in signal
    assert "reasoning_summary" in signal

def test_agent_tracks_stats(mock_agent):
    """Test that agent tracks performance statistics"""
    assert mock_agent.total_signals == 0
    assert mock_agent.successful_signals == 0
    assert mock_agent.failed_signals == 0
    
    # Simulate signals
    mock_agent._create_signal(
        asset="BTC/USD",
        timeframe="1h",
        signal=SignalType.BUY,
        confidence=0.8,
        reasoning="test",
        key_factors=[],
        risks=[],
        data_quality=0.9
    )
    
    assert mock_agent.total_signals == 1
    assert mock_agent.average_confidence == 0.8

def test_agent_records_signal_results(mock_agent):
    """Test that agent records whether signals were correct"""
    mock_agent.record_signal_result(was_correct=True)
    assert mock_agent.successful_signals == 1
    assert mock_agent.failed_signals == 0
    
    mock_agent.record_signal_result(was_correct=False)
    assert mock_agent.successful_signals == 1
    assert mock_agent.failed_signals == 1

def test_agent_performance_stats(mock_agent):
    """Test that agent performance stats are calculated correctly"""
    # Record some results
    for _ in range(8):
        mock_agent.record_signal_result(was_correct=True)
    for _ in range(2):
        mock_agent.record_signal_result(was_correct=False)
    
    stats = mock_agent.get_performance_stats()
    
    assert stats["name"] == "TestAgent"
    assert stats["successful_signals"] == 8
    assert stats["failed_signals"] == 2
    assert stats["accuracy"] == 0.8

def test_agent_no_trade_signal(mock_agent):
    """Test creating NO_TRADE signal for invalid data"""
    signal = mock_agent._create_no_trade(
        asset="INVALID",
        timeframe="1h",
        reason="Missing market data",
        data_quality=0.0
    )
    
    assert signal["signal"] == "NO_TRADE"
    assert signal["confidence"] == 0.0
    assert signal["data_quality"] == 0.0
    assert signal["reasoning_summary"] == "Missing market data"
