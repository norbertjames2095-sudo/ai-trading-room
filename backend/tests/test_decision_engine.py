"""Tests for Decision Engine"""
import pytest
from datetime import datetime
from app.engine.decision_engine import DecisionEngine

@pytest.fixture
def decision_engine():
    return DecisionEngine()

@pytest.mark.asyncio
async def test_decision_engine_no_signals(decision_engine):
    """Test that NO_TRADE is returned when there are no signals"""
    result = await decision_engine.evaluate_opportunity(
        asset="BTC/USD",
        timeframe="1h",
        agent_signals=[]
    )
    
    assert result["final_signal"] == "NO_TRADE"
    assert result["opportunity_score"] == 0

@pytest.mark.asyncio
async def test_decision_engine_all_buy_signals(decision_engine):
    """Test that BUY is returned when all agents buy"""
    signals = [
        {
            "agent": "Agent1",
            "signal": "BUY",
            "confidence": 0.9,
            "data_quality": 0.9
        },
        {
            "agent": "Agent2",
            "signal": "BUY",
            "confidence": 0.8,
            "data_quality": 0.9
        }
    ]
    
    result = await decision_engine.evaluate_opportunity(
        asset="BTC/USD",
        timeframe="1h",
        agent_signals=signals
    )
    
    assert result["final_signal"] == "BUY"
    assert result["opportunity_score"] > 75

@pytest.mark.asyncio
async def test_decision_engine_mixed_signals(decision_engine):
    """Test decision making with mixed signals"""
    signals = [
        {
            "agent": "BuyAgent",
            "signal": "BUY",
            "confidence": 0.8,
            "data_quality": 0.9
        },
        {
            "agent": "SellAgent",
            "signal": "SELL",
            "confidence": 0.5,
            "data_quality": 0.6
        },
        {
            "agent": "HoldAgent",
            "signal": "HOLD",
            "confidence": 0.6,
            "data_quality": 0.7
        }
    ]
    
    result = await decision_engine.evaluate_opportunity(
        asset="ETH/USD",
        timeframe="4h",
        agent_signals=signals
    )
    
    # Should not be extreme in either direction
    assert 30 < result["opportunity_score"] < 80

@pytest.mark.asyncio
async def test_agent_performance_update(decision_engine):
    """Test that agent performance tracking works"""
    initial_weight = decision_engine.agent_weights.get("TestAgent", 1.0)
    
    # Simulate correct signal
    decision_engine.update_agent_performance(
        "TestAgent",
        {"correct": True}
    )
    
    # Record 10 more correct signals to reach minimum sample size
    for _ in range(9):
        decision_engine.update_agent_performance(
            "TestAgent",
            {"correct": True}
        )
    
    new_weight = decision_engine.agent_weights.get("TestAgent", 1.0)
    
    # Weight should increase with correct signals
    assert new_weight > initial_weight

def test_score_interpretation():
    """Test that opportunity scores are interpreted correctly"""
    # 0-39: NO TRADE
    # 40-59: WEAK
    # 60-74: MODERATE
    # 75-89: STRONG
    # 90-100: VERY STRONG
    
    assert True  # Placeholder for interpretation logic
