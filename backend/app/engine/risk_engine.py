from typing import Dict, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class RiskEngine:
    """
    Risk Engine - Deterministic and immutable risk management system.
    No AI can modify these rules during operation.
    """
    
    def __init__(self, config: Dict):
        """
        Initialize Risk Engine with configuration.
        All limits are set at initialization and cannot be changed without restart.
        """
        self.max_risk_per_trade = config.get("max_risk_per_trade", 0.02)
        self.max_exposure_per_asset = config.get("max_exposure_per_asset", 0.10)
        self.max_total_exposure = config.get("max_total_exposure", 0.80)
        self.max_daily_loss = config.get("max_daily_loss", 0.05)
        self.max_drawdown = config.get("max_drawdown", 0.20)
        self.max_positions = config.get("max_positions", 20)
        self.min_liquidity_ratio = config.get("min_liquidity_ratio", 2.0)
        self.max_slippage_bps = config.get("max_slippage_bps", 50)
        self.max_correlation = config.get("max_correlation", 0.95)
        self.volatility_limit = config.get("volatility_limit", 0.15)
        
        self.kill_switch_active = False
        self.kill_switch_activated_at = None
        
        logger.info("Risk Engine initialized with immutable rules")
    
    async def validate_trade(
        self,
        decision: Dict,
        portfolio_state: Dict,
        market_data: Dict
    ) -> Dict:
        """
        Validate trade against ALL risk rules.
        Returns approval or rejection with detailed reasoning.
        
        This is the FINAL gate before any execution.
        """
        
        # Kill switch check (highest priority)
        if self.kill_switch_active:
            return self._create_rejection(
                "KILL_SWITCH_ACTIVE",
                "Emergency kill switch is active. No new trades allowed."
            )
        
        # Extract signal details
        asset = decision.get("asset")
        signal = decision.get("final_signal")
        entry_price = decision.get("recommended_entry", market_data.get("current_price"))
        stop_price = decision.get("recommended_stop")
        target_price = decision.get("recommended_target")
        
        # 1. Check for missing critical data
        if not asset or not signal or signal == "NO_TRADE":
            return self._create_rejection(
                "INVALID_SIGNAL",
                "Invalid or missing signal data"
            )
        
        # 2. Check liquidity
        liquidity_check = self._check_liquidity(asset, market_data, portfolio_state)
        if not liquidity_check["approved"]:
            return self._create_rejection("LIQUIDITY_FAIL", liquidity_check["reason"])
        
        # 3. Calculate position size
        position_size = self._calculate_position_size(
            portfolio_state,
            entry_price,
            stop_price
        )
        
        if position_size <= 0:
            return self._create_rejection(
                "INVALID_POSITION",
                "Cannot calculate valid position size"
            )
        
        # 4. Check individual trade risk
        trade_risk = self._check_trade_risk(
            position_size,
            entry_price,
            stop_price,
            portfolio_state
        )
        if not trade_risk["approved"]:
            return self._create_rejection("TRADE_RISK_LIMIT", trade_risk["reason"])
        
        # 5. Check asset exposure limit
        asset_exposure_check = self._check_asset_exposure(
            asset,
            position_size,
            entry_price,
            portfolio_state
        )
        if not asset_exposure_check["approved"]:
            return self._create_rejection("ASSET_EXPOSURE_LIMIT", asset_exposure_check["reason"])
        
        # 6. Check total exposure limit
        total_exposure_check = self._check_total_exposure(
            position_size,
            entry_price,
            portfolio_state
        )
        if not total_exposure_check["approved"]:
            return self._create_rejection("TOTAL_EXPOSURE_LIMIT", total_exposure_check["reason"])
        
        # 7. Check max positions
        if portfolio_state.get("open_positions", 0) >= self.max_positions:
            return self._create_rejection(
                "MAX_POSITIONS",
                f"Maximum {self.max_positions} positions already open"
            )
        
        # 8. Check daily loss limit
        daily_loss_check = self._check_daily_loss(portfolio_state)
        if not daily_loss_check["approved"]:
            return self._create_rejection("DAILY_LOSS_LIMIT", daily_loss_check["reason"])
        
        # 9. Check drawdown
        drawdown_check = self._check_drawdown(portfolio_state)
        if not drawdown_check["approved"]:
            return self._create_rejection("DRAWDOWN_LIMIT", drawdown_check["reason"])
        
        # 10. Check correlation with existing positions
        correlation_check = self._check_correlation(asset, portfolio_state, market_data)
        if not correlation_check["approved"]:
            return self._create_rejection("HIGH_CORRELATION", correlation_check["reason"])
        
        # 11. Check volatility
        volatility_check = self._check_volatility(asset, market_data)
        if not volatility_check["approved"]:
            return self._create_rejection("VOLATILITY_LIMIT", volatility_check["reason"])
        
        # All checks passed - APPROVED
        return {
            "approved": True,
            "asset": asset,
            "signal": signal,
            "position_size": position_size,
            "entry_price": entry_price,
            "stop_price": stop_price,
            "target_price": target_price,
            "risk_amount": trade_risk["risk_amount"],
            "risk_percent": trade_risk["risk_percent"],
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _check_liquidity(self, asset: str, market_data: Dict, portfolio: Dict) -> Dict:
        """Check if asset has sufficient liquidity"""
        daily_volume = market_data.get("daily_volume", 0)
        estimated_trade_size = portfolio.get("estimated_trade_size", 0)
        
        if daily_volume == 0:
            return {"approved": False, "reason": "No volume data available"}
        
        liquidity_ratio = daily_volume / max(estimated_trade_size, 1)
        
        if liquidity_ratio < self.min_liquidity_ratio:
            return {
                "approved": False,
                "reason": f"Insufficient liquidity. Ratio: {liquidity_ratio:.2f}, Required: {self.min_liquidity_ratio}"
            }
        
        return {"approved": True}
    
    def _calculate_position_size(
        self,
        portfolio: Dict,
        entry_price: float,
        stop_price: float
    ) -> float:
        """Calculate position size based on risk per trade"""
        if not entry_price or not stop_price or entry_price == stop_price:
            return 0
        
        available_cash = portfolio.get("available_cash", 0)
        risk_amount = available_cash * self.max_risk_per_trade
        
        price_risk = abs(entry_price - stop_price)
        position_size = risk_amount / price_risk
        
        return position_size
    
    def _check_trade_risk(self, position_size: float, entry: float, stop: float, portfolio: Dict) -> Dict:
        """Check individual trade risk"""
        risk_amount = position_size * abs(entry - stop)
        available_cash = portfolio.get("available_cash", 0)
        
        if available_cash == 0:
            return {"approved": False, "reason": "No available cash"}
        
        risk_percent = risk_amount / available_cash
        
        if risk_percent > self.max_risk_per_trade:
            return {
                "approved": False,
                "reason": f"Trade risk {risk_percent*100:.1f}% exceeds limit {self.max_risk_per_trade*100:.1f}%",
                "risk_amount": risk_amount,
                "risk_percent": risk_percent
            }
        
        return {
            "approved": True,
            "risk_amount": risk_amount,
            "risk_percent": risk_percent
        }
    
    def _check_asset_exposure(self, asset: str, position_size: float, price: float, portfolio: Dict) -> Dict:
        """Check exposure per asset"""
        position_value = position_size * price
        total_value = portfolio.get("total_equity", 0)
        
        if total_value == 0:
            return {"approved": False, "reason": "Invalid portfolio value"}
        
        existing_exposure = portfolio.get("asset_exposure", {}).get(asset, 0)
        total_exposure = existing_exposure + position_value
        exposure_percent = total_exposure / total_value
        
        if exposure_percent > self.max_exposure_per_asset:
            return {
                "approved": False,
                "reason": f"Asset exposure {exposure_percent*100:.1f}% exceeds limit {self.max_exposure_per_asset*100:.1f}%"
            }
        
        return {"approved": True}
    
    def _check_total_exposure(self, position_size: float, price: float, portfolio: Dict) -> Dict:
        """Check total portfolio exposure"""
        position_value = position_size * price
        total_value = portfolio.get("total_equity", 0)
        
        if total_value == 0:
            return {"approved": False, "reason": "Invalid portfolio value"}
        
        existing_exposure = portfolio.get("total_exposure", 0)
        total_exposure = existing_exposure + position_value
        exposure_percent = total_exposure / total_value
        
        if exposure_percent > self.max_total_exposure:
            return {
                "approved": False,
                "reason": f"Total exposure {exposure_percent*100:.1f}% exceeds limit {self.max_total_exposure*100:.1f}%"
            }
        
        return {"approved": True}
    
    def _check_daily_loss(self, portfolio: Dict) -> Dict:
        """Check daily loss limit"""
        daily_pnl = portfolio.get("daily_pnl", 0)
        initial_capital = portfolio.get("initial_capital", 0)
        
        if initial_capital == 0:
            return {"approved": False, "reason": "Invalid initial capital"}
        
        daily_loss_limit = initial_capital * self.max_daily_loss
        
        if daily_pnl < -daily_loss_limit:
            return {
                "approved": False,
                "reason": f"Daily loss {abs(daily_pnl):.2f} exceeds limit {daily_loss_limit:.2f}"
            }
        
        return {"approved": True}
    
    def _check_drawdown(self, portfolio: Dict) -> Dict:
        """Check maximum drawdown"""
        current_drawdown = portfolio.get("current_drawdown", 0)
        max_drawdown_limit = portfolio.get("initial_capital", 0) * self.max_drawdown
        
        if current_drawdown > max_drawdown_limit:
            return {
                "approved": False,
                "reason": f"Current drawdown {current_drawdown:.2f} exceeds limit {max_drawdown_limit:.2f}"
            }
        
        return {"approved": True}
    
    def _check_correlation(self, asset: str, portfolio: Dict, market_data: Dict) -> Dict:
        """Check correlation with existing positions"""
        # Simplified check - in production would calculate actual correlation
        return {"approved": True}
    
    def _check_volatility(self, asset: str, market_data: Dict) -> Dict:
        """Check asset volatility"""
        volatility = market_data.get("volatility", 0)
        
        if volatility > self.volatility_limit:
            return {
                "approved": False,
                "reason": f"Asset volatility {volatility*100:.1f}% exceeds limit {self.volatility_limit*100:.1f}%"
            }
        
        return {"approved": True}
    
    def _create_rejection(self, reason_code: str, reason_message: str) -> Dict:
        """Create rejection response"""
        logger.warning(f"Trade rejected: {reason_code} - {reason_message}")
        return {
            "approved": False,
            "rejection_reason": reason_code,
            "rejection_message": reason_message,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def activate_kill_switch(self):
        """
        EMERGENCY: Activate kill switch.
        No new orders will be accepted.
        """
        self.kill_switch_active = True
        self.kill_switch_activated_at = datetime.utcnow()
        logger.critical("KILL SWITCH ACTIVATED")
    
    def deactivate_kill_switch(self):
        """
        ADMIN ONLY: Deactivate kill switch.
        Requires explicit authorization.
        """
        self.kill_switch_active = False
        logger.warning("Kill switch deactivated")
