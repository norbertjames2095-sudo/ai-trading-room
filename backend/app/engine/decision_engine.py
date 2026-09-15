from typing import List, Dict
from datetime import datetime
import json
from app.models.agent_signal import AgentSignal
from app.models.decision_result import DecisionResult

class DecisionEngine:
    """
    Decision Engine - Coordinates agent signals and generates final trading decisions.
    Does NOT use simple majority voting.
    """
    
    def __init__(self):
        self.agent_weights = {}  # Will be populated based on performance
        self.performance_history = {}  # Track agent performance
    
    async def evaluate_opportunity(
        self,
        asset: str,
        timeframe: str,
        agent_signals: List[Dict]
    ) -> Dict:
        """
        Evaluate all agent signals and produce a decision.
        
        Args:
            asset: Trading pair (e.g., 'BTC/USD')
            timeframe: Chart timeframe (e.g., '1h')
            agent_signals: List of agent signal dictionaries
        
        Returns:
            Decision result with score and reasoning
        """
        
        # Validate input
        if not agent_signals:
            return self._create_no_trade_decision(asset, "No agent signals available")
        
        # Analyze agent signals
        signal_analysis = self._analyze_signals(agent_signals)
        
        # Calculate opportunity score (0-100)
        opportunity_score = self._calculate_opportunity_score(signal_analysis)
        
        # Determine final signal
        final_signal = self._determine_final_signal(opportunity_score, signal_analysis)
        
        # Generate decision reasoning
        reasoning = self._generate_reasoning(signal_analysis, opportunity_score, final_signal)
        
        return {
            "asset": asset,
            "timeframe": timeframe,
            "final_signal": final_signal,
            "opportunity_score": opportunity_score,
            "reasoning": reasoning,
            "agent_consensus": signal_analysis,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _analyze_signals(self, agent_signals: List[Dict]) -> Dict:
        """
        Analyze all agent signals considering:
        - Confidence levels
        - Data quality
        - Agent performance history
        - Timeframe alignment
        """
        signals_by_type = {
            "BUY": [],
            "SELL": [],
            "HOLD": [],
            "NO_TRADE": []
        }
        
        weighted_scores = {
            "BUY": 0,
            "SELL": 0,
            "HOLD": 0,
            "NO_TRADE": 0
        }
        
        total_weight = 0
        
        for signal in agent_signals:
            signal_type = signal.get("signal", "NO_TRADE")
            confidence = signal.get("confidence", 0.5)
            data_quality = signal.get("data_quality", 0.5)
            
            # Get agent weight (default 1.0)
            agent_name = signal.get("agent", "unknown")
            agent_weight = self.agent_weights.get(agent_name, 1.0)
            
            # Combined weight: agent performance * confidence * data quality
            combined_weight = agent_weight * confidence * data_quality
            
            signals_by_type[signal_type].append({
                "agent": agent_name,
                "confidence": confidence,
                "data_quality": data_quality,
                "weight": combined_weight
            })
            
            weighted_scores[signal_type] += combined_weight
            total_weight += combined_weight
        
        # Normalize scores
        if total_weight > 0:
            for signal_type in weighted_scores:
                weighted_scores[signal_type] = weighted_scores[signal_type] / total_weight * 100
        
        return {
            "signals_by_type": signals_by_type,
            "weighted_scores": weighted_scores,
            "total_signals": len(agent_signals)
        }
    
    def _calculate_opportunity_score(self, analysis: Dict) -> float:
        """
        Calculate final opportunity score (0-100).
        
        Score interpretation:
        - 0-39: NO TRADE
        - 40-59: WEAK
        - 60-74: MODERATE
        - 75-89: STRONG
        - 90-100: VERY STRONG
        """
        weighted_scores = analysis["weighted_scores"]
        
        # Calculate score based on signal distribution
        buy_weight = weighted_scores["BUY"]
        sell_weight = weighted_scores["SELL"]
        hold_weight = weighted_scores["HOLD"]
        no_trade_weight = weighted_scores["NO_TRADE"]
        
        # If Red Team (NO_TRADE) is dominant, reduce score
        if no_trade_weight > 40:
            return max(0, buy_weight - sell_weight) * 0.5
        
        # Calculate net sentiment
        net_sentiment = buy_weight - sell_weight
        
        # Adjust for consensus
        total_directional = buy_weight + sell_weight
        if total_directional > 0:
            consensus = max(buy_weight, sell_weight) / total_directional
        else:
            consensus = 0.5
        
        # Combine sentiment and consensus
        score = 50 + (net_sentiment * 0.5) * consensus
        
        # Clamp to 0-100
        return max(0, min(100, score))
    
    def _determine_final_signal(self, score: float, analysis: Dict) -> str:
        """
        Determine final trading signal based on score and analysis.
        """
        if score < 40:
            return "NO_TRADE"
        elif score < 60:
            return "HOLD"  # Weak signal
        elif score < 75:
            # Moderate: check if consensus is clear
            weighted_scores = analysis["weighted_scores"]
            if weighted_scores["BUY"] > weighted_scores["SELL"]:
                return "BUY"
            else:
                return "SELL"
        else:
            # Strong signal
            weighted_scores = analysis["weighted_scores"]
            if weighted_scores["BUY"] > weighted_scores["SELL"]:
                return "BUY"
            else:
                return "SELL"
    
    def _generate_reasoning(self, analysis: Dict, score: float, signal: str) -> str:
        """
        Generate human-readable reasoning for the decision.
        """
        total_signals = analysis["total_signals"]
        weighted_scores = analysis["weighted_scores"]
        
        reasoning = f"Decision based on {total_signals} agent signals. "
        reasoning += f"BUY consensus: {weighted_scores['BUY']:.1f}%, "
        reasoning += f"SELL consensus: {weighted_scores['SELL']:.1f}%, "
        reasoning += f"Score: {score:.0f}/100. "
        
        if score < 40:
            reasoning += "Insufficient evidence for trade."
        elif score < 75:
            reasoning += "Weak to moderate signal. Requires confirmation."
        else:
            reasoning += "Strong signal with good consensus among agents."
        
        return reasoning
    
    def _create_no_trade_decision(self, asset: str, reason: str) -> Dict:
        """
        Create a NO_TRADE decision.
        """
        return {
            "asset": asset,
            "final_signal": "NO_TRADE",
            "opportunity_score": 0,
            "reasoning": reason,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def update_agent_performance(self, agent_name: str, signal_result: Dict):
        """
        Update agent weight based on performance.
        Called after trade results are known.
        """
        if agent_name not in self.performance_history:
            self.performance_history[agent_name] = {
                "correct": 0,
                "incorrect": 0,
                "accuracy": 0.5
            }
        
        history = self.performance_history[agent_name]
        
        if signal_result.get("correct"):
            history["correct"] += 1
        else:
            history["incorrect"] += 1
        
        # Calculate accuracy
        total = history["correct"] + history["incorrect"]
        if total >= 10:  # Minimum sample size
            history["accuracy"] = history["correct"] / total
            # Weight based on accuracy (0.5 to 1.5)
            self.agent_weights[agent_name] = 0.5 + (history["accuracy"])
        else:
            self.agent_weights[agent_name] = 1.0
