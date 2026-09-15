"""Tests for Risk Engine"""
import pytest
from app.engine.risk_engine import RiskEngine

@pytest.fixture
def risk_engine():
    config = {
        "max_risk_per_trade": 0.02,
        "max_exposure_per_asset": 0.10,
        "max_total_exposure": 0.80,
        "max_daily_loss": 0.05,
        "max_drawdown": 0.20,
        "max_positions": 20,
        "min_liquidity_ratio": 2.0,
        "max_slippage_bps": 50,
        "max_correlation": 0.95,
        "volatility_limit": 0.15
    }
    return RiskEngine(config)

@pytest.mark.asyncio
async def test_kill_switch_blocks_trades(risk_engine):
    """Test that kill switch blocks all trades"""
    risk_engine.activate_kill_switch()
    
    decision = {
        "asset": "BTC/USD",
        "final_signal": "BUY",
        "recommended_entry": 42500,
        "recommended_stop": 42000,
        "recommended_target": 43500
    }
    
    portfolio = {
        "available_cash": 100000,
        "total_equity": 100000,
        "open_positions": 0,
        "daily_pnl": 0,
        "current_drawdown": 0
    }
    
    market_data = {"current_price": 42500, "daily_volume": 1000000}
    
    result = await risk_engine.validate_trade(decision, portfolio, market_data)
    
    assert result["approved"] == False
    assert "KILL_SWITCH" in result["rejection_reason"]

@pytest.mark.asyncio
async def test_no_trade_signal_rejected(risk_engine):
    """Test that NO_TRADE signals are rejected"""
    decision = {
        "asset": "BTC/USD",
        "final_signal": "NO_TRADE"
    }
    
    portfolio = {"available_cash": 100000, "total_equity": 100000}
    market_data = {}
    
    result = await risk_engine.validate_trade(decision, portfolio, market_data)
    
    assert result["approved"] == False

@pytest.mark.asyncio
async def test_insufficient_liquidity_rejected(risk_engine):
    """Test that trades with insufficient liquidity are rejected"""
    decision = {
        "asset": "ILLIQUID/USD",
        "final_signal": "BUY",
        "recommended_entry": 100,
        "recommended_stop": 95,
        "recommended_target": 110
    }
    
    portfolio = {
        "available_cash": 100000,
        "total_equity": 100000,
        "open_positions": 0,
        "estimated_trade_size": 1000,
        "daily_pnl": 0,
        "current_drawdown": 0,
        "asset_exposure": {},
        "total_exposure": 0,
        "initial_capital": 100000
    }
    
    market_data = {
        "current_price": 100,
        "daily_volume": 100  # Very low volume
    }
    
    result = await risk_engine.validate_trade(decision, portfolio, market_data)
    
    assert result["approved"] == False
    assert "LIQUIDITY" in result["rejection_reason"]

@pytest.mark.asyncio
async def test_max_positions_limit(risk_engine):
    """Test that max positions limit is enforced"""
    decision = {
        "asset": "BTC/USD",
        "final_signal": "BUY",
        "recommended_entry": 42500,
        "recommended_stop": 42000,
        "recommended_target": 43500
    }
    
    portfolio = {
        "available_cash": 100000,
        "total_equity": 100000,
        "open_positions": 20,  # At limit
        "daily_pnl": 0,
        "current_drawdown": 0,
        "asset_exposure": {},
        "total_exposure": 0,
        "initial_capital": 100000,
        "estimated_trade_size": 5000
    }
    
    market_data = {
        "current_price": 42500,
        "daily_volume": 1000000
    }
    
    result = await risk_engine.validate_trade(decision, portfolio, market_data)
    
    assert result["approved"] == False
    assert "MAX_POSITIONS" in result["rejection_reason"]

def test_risk_engine_initialization(risk_engine):
    """Test that risk engine initializes with correct values"""
    assert risk_engine.max_risk_per_trade == 0.02
    assert risk_engine.max_drawdown == 0.20
    assert risk_engine.max_positions == 20
    assert risk_engine.kill_switch_active == False

def test_kill_switch_activation(risk_engine):
    """Test kill switch activation and deactivation"""
    assert risk_engine.kill_switch_active == False
    
    risk_engine.activate_kill_switch()
    assert risk_engine.kill_switch_active == True
    assert risk_engine.kill_switch_activated_at is not None
    
    risk_engine.deactivate_kill_switch()
    assert risk_engine.kill_switch_active == False
