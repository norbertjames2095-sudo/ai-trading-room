# AI Trading Room

**Professional Multi-Agent AI Trading Platform**

A sophisticated, modular trading system featuring 20 specialized AI agents for market analysis, risk management, and decision-making. Designed for research, backtesting, and paper trading before enabling live trading.

## 🎯 Overview

### Core Principles

1. **No AI can guarantee profit**
2. **No AI can increase risk autonomously**
3. **Risk Engine is immutable and deterministic**
4. **All decisions are auditable**
5. **Live trading is disabled by default**

### Operation Modes

- **RESEARCH MODE**: Analysis only
- **BACKTEST MODE**: Historical data simulation
- **PAPER MODE**: Real-time simulation
- **LIVE MODE**: Real execution (explicit activation required)

## 🏗️ Architecture

### Frontend
- **Framework**: Next.js 14 with React
- **Styling**: TailwindCSS
- **Charts**: TradingView Lightweight Charts
- **Real-time**: WebSocket
- **State Management**: Zustand
- **Dark mode** professional trading interface

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Message Queue**: Celery + Redis
- **WebSocket**: FastAPI WebSocket
- **Logging**: Structured logging with JSON

### AI & Analysis
- **Orchestration**: Multi-agent system
- **Models**: 
  - Fast/economic models for simple tasks
  - Powerful models for complex analysis
  - Provider-agnostic architecture
- **Cost Tracking**: Per-agent, per-day, per-model

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack ready
- **Health Checks**: Automated service monitoring

## 🤖 20 Specialized Agents

1. **Market Scanner** - Opportunity detection
2. **Trend Analyst** - Trend identification
3. **Momentum Analyst** - Acceleration detection
4. **Mean Reversion** - Statistical deviations
5. **Breakout Analyst** - Support/resistance breaks
6. **Volume/Flow Analyst** - Volume analysis
7. **Volatility Analyst** - ATR, historical vol
8. **Price Action Analyst** - Candle patterns
9. **Quant Analyst** - Statistical models
10. **ML Researcher** - Model validation (no trading)
11. **Crypto Analyst** - BTC, ETH specialist
12. **Equity Analyst** - Stock specialist
13. **Forex Analyst** - Currency pairs
14. **Macro Analyst** - Economic indicators
15. **News Analyst** - Event monitoring
16. **Sentiment Analyst** - Market sentiment
17. **Portfolio Manager** - Position evaluation
18. **Risk Manager** - Critical risk validation
19. **Red Team** - Contrarian analysis
20. **Chief Trader** - Final decision coordinator

## 🎲 Decision Engine

- Analyzes all agent outputs
- Considers: confidence, data quality, performance history
- Generates opportunity score (0-100)
- **Not** a simple majority vote

**Score Interpretation**:
- 0-39: NO TRADE
- 40-59: WEAK
- 60-74: MODERATE
- 75-89: STRONG
- 90-100: VERY STRONG

## 🛡️ Risk Engine

**Deterministic and immutable. No AI can modify it.**

Configurable limits:
- Max risk per trade
- Max exposure per asset
- Max total exposure
- Max daily loss
- Max drawdown
- Max positions
- Volatility limits
- Liquidity limits
- Slippage limits
- Correlation limits

**Kill Switch**: Emergency control to halt all new orders

## 📊 Features

### Market Coverage
- Crypto (BTC, ETH, major altcoins)
- Stocks (US indices, individual equities)
- Forex (EUR/USD, GBP/USD, USD/JPY)
- Indexes (S&P 500, NASDAQ)
- Options (future phase)

### Backtesting Engine
- Historical data simulation
- Multiple timeframes
- Commissions & spread modeling
- Slippage simulation
- Latency simulation
- Walk-forward validation
- Out-of-sample testing
- Anti look-ahead bias

### Paper Trading
- Real-time market data
- Simulated execution
- Signal vs Result comparison
- Agent performance tracking

### Agent Performance Tracking
- Win rate
- Accuracy by asset/timeframe
- Regime-based performance
- Statistical significance validation
- Minimum sample size enforcement

### Audit Trail
- Every decision logged
- Models used tracked
- Costs recorded
- Timestamps precise
- Results auditable

## 📁 Project Structure

```
ai-trading-room/
├── frontend/                 # Next.js application
├── backend/                  # FastAPI application
├── agents/                   # AI agent implementations
├── engine/                   # Decision & Risk engines
├── data/                     # Market data providers
├── backtester/              # Backtesting engine
├── docker-compose.yml       # Local development
├── docs/                    # Architecture & API documentation
├── tests/                   # Test suites
└── scripts/                 # Utilities
```

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- PostgreSQL 15 (or via Docker)
- Redis 7 (or via Docker)

### Development Setup

```bash
# Clone repository
git clone https://github.com/norbertjames2095-sudo/ai-trading-room.git
cd ai-trading-room

# Start services
docker-compose up -d

# Backend setup
cd backend
cp .env.example .env
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
python -m pytest

# Frontend setup
cd ../frontend
npm install
npm run dev
```

Access:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Postgres**: localhost:5432
- **Redis**: localhost:6379

## 🔐 Security

- Autenticação com 2FA
- API key management (never in code)
- Encryption at rest and in transit
- Rate limiting
- Input validation
- CORS properly configured
- Secrets in `.env` files (not in Git)
- Automated backups

## 📈 Roadmap

### Phase 1: Foundation ✅
- [ ] Frontend basic dashboard
- [ ] Backend API structure
- [ ] Database schema
- [ ] Authentication system
- [ ] Market data integration

### Phase 2: Agents
- [ ] Implement all 20 agents

### Phase 3: Decision Engine
- [ ] Score calculation
- [ ] Agent weighting

### Phase 4: Risk Engine
- [ ] Rules implementation
- [ ] Kill switch

### Phase 5: Backtesting
- [ ] Engine development
- [ ] Signal simulation

### Phase 6: Paper Trading
- [ ] Simulation system
- [ ] Performance tracking

### Phase 7: Dashboard
- [ ] Professional UI
- [ ] Real-time updates

### Phase 8: Monitoring
- [ ] Observability stack
- [ ] Alerting system

### Phase 9: Security Audit
- [ ] Full audit
- [ ] Penetration testing

### Phase 10: Live Trading
- [ ] Activation protocol
- [ ] Manual approval workflow

## 📊 Monitoring & Observability

- **Metrics**: Prometheus
- **Visualization**: Grafana
- **Logs**: Structured JSON logging
- **Tracing**: OpenTelemetry ready
- **Alerts**: Multi-channel (email, Telegram)

## 💰 Cost Management

- Per-agent cost tracking
- Daily/weekly/monthly aggregation
- Per-model cost analysis
- Monthly budget limits
- Automatic cost optimization

## 📋 API Standard Response Format

All agents return standardized JSON:

```json
{
  "agent": "Agent Name",
  "timestamp": "2026-09-15T10:30:00Z",
  "asset": "BTC/USD",
  "timeframe": "1h",
  "signal": "BUY|SELL|HOLD|NO_TRADE",
  "confidence": 0.85,
  "reasoning_summary": "Clear trend with momentum confirmation",
  "key_factors": ["Factor 1", "Factor 2"],
  "risks": ["Risk 1", "Risk 2"],
  "data_quality": 0.95,
  "recommended_entry": 42500.00,
  "recommended_stop": 42000.00,
  "recommended_target": 43500.00
}
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/ -v

# Frontend tests
cd frontend
npm test
```

## 📚 Documentation

- `/docs/ARCHITECTURE.md` - Technical architecture
- `/docs/API.md` - API specifications
- `/docs/AGENTS.md` - Agent specifications
- `/docs/RISK_ENGINE.md` - Risk rules
- `/docs/DATABASE.md` - Schema documentation
- `/docs/DEPLOYMENT.md` - Production deployment

## ⚠️ Important Notes

**This is NOT a get-rich-quick scheme.**

- Backtests do not guarantee future performance
- Paper trading is mandatory before live trading
- Live mode must be explicitly activated
- All decisions must be auditable
- Risk management is non-negotiable

## 🤝 Contributing

This is a professional project. All code must:
- Follow PEP 8 (Python) and ESLint (JavaScript)
- Include tests
- Be documented
- Pass security checks

## 📄 License

MIT License - See LICENSE file

## 📞 Support

For issues, questions, or suggestions:
- Create an issue on GitHub
- Check documentation in `/docs`
- Review audit logs in the system

---

**Built with precision. Designed for safety. Ready for scale.**
