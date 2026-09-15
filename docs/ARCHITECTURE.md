# ARCHITECTURE OVERVIEW

## System Architecture

AI Trading Room is built on a modular, service-oriented architecture designed for:
- **Safety**: Multiple layers of risk management
- **Scalability**: Distributed agents and processing
- **Auditability**: Complete decision trail
- **Flexibility**: Pluggable providers and models

## Core Components

### 1. Frontend (Next.js 14)
- Professional dark-mode dashboard
- Real-time market data visualization
- Trading opportunity display
- Portfolio management interface
- Agent monitoring
- Risk controls

### 2. Backend (FastAPI)
- RESTful API
- WebSocket support for real-time updates
- PostgreSQL for persistent data
- Redis for caching and sessions
- Celery for async task processing

### 3. Agent Orchestration
- 20 specialized agents
- Each agent generates standardized signals
- Agents run independently and are fault-tolerant
- Performance tracking per agent

### 4. Decision Engine
- Analyzes all agent signals
- Weighted scoring (not majority vote)
- Generates opportunity scores (0-100)
- Produces final trading decisions
- Considers agent performance history

### 5. Risk Engine
- **DETERMINISTIC AND IMMUTABLE**
- No AI can modify rules
- Validates every trade
- Enforces hard limits:
  - Max risk per trade
  - Max exposure per asset
  - Max total exposure
  - Max daily loss
  - Max drawdown
  - Position limits
  - Liquidity requirements
  - Correlation checks
  - Volatility limits
- Kill switch for emergency stops

### 6. Market Data Layer
- Abstract provider interface
- Supports multiple providers:
  - Alpha Vantage (stocks, forex)
  - CoinGecko (crypto)
  - IEX Cloud (stocks)
  - Polygon.io (stocks)
- Caching to reduce API costs
- Data validation

### 7. Order Management
- Order flow: Signal → Risk Check → Approval → Execution
- Separate from trading decisions
- Full audit trail
- Support for manual approval

### 8. Backtesting Engine
- Historical data simulation
- Walk-forward validation
- Prevents look-ahead bias
- Realistic slippage/commission modeling
- Performance metrics calculation

### 9. Paper Trading
- Simulates real market conditions
- Real-time data
- Tracks simulated P&L
- Measures agent performance
- Mandatory before live trading

### 10. Monitoring & Observability
- Prometheus metrics
- Grafana dashboards
- Structured JSON logging
- Agent health monitoring
- API health checks
- Audit logging

## Data Flow

### Trading Decision Flow
```
1. Market Data Layer
   ↓
2. Individual Agents (analyze independently)
   ↓
3. Decision Engine (synthesize signals)
   ↓
4. Risk Engine (validate hard rules)
   ↓
5. Order Manager (execute if approved)
   ↓
6. Broker/Simulation
   ↓
7. Execution & Audit Trail
```

## Safety Mechanisms

### 1. Layered Risk Management
- Each agent has confidence/quality metrics
- Decision Engine weights by performance
- Risk Engine has hard, unmutable limits
- Kill switch for emergency

### 2. Data Validation
- Missing data → NO_TRADE
- Invalid data → NO_TRADE
- Stale data → NO_TRADE

### 3. Audit Trail
- Every signal captured
- Every decision logged
- Every order auditable
- Full reasoning recorded
- Cost tracking per model

### 4. Agent Isolation
- Agents fail independently
- System continues if agent fails
- Automatic agent restart
- Degraded mode operation

### 5. Operation Modes
- RESEARCH: Analysis only
- BACKTEST: Historical simulation
- PAPER: Real-time simulation
- LIVE: Requires explicit multi-step activation

## Database Schema

### Tables
- **users**: User accounts and authentication
- **agents**: Agent definitions and status
- **agent_signals**: Individual agent signals
- **decision_results**: Final trading decisions
- **orders**: Trade orders
- **portfolios**: Portfolio state
- **risk_configs**: Risk parameters
- **audit_logs**: Complete audit trail

## Deployment

### Development
- Docker Compose for local development
- All services in containers
- PostgreSQL and Redis included
- Automatic migration on startup

### Production
- Kubernetes-ready
- Horizontal scaling
- Load balancing
- Health checks
- Monitoring integration

## API Versioning
- Current: v1
- All endpoints: `/api/v1/*`
- Backward compatibility maintained

## Security
- JWT authentication
- 2FA support
- API key management
- CORS properly configured
- Rate limiting
- Input validation
- HTTPS in production

## Performance
- Redis caching for market data
- Async/await throughout
- Connection pooling
- Query optimization
- Monitoring with Prometheus

## Scaling
- Stateless backend design
- Horizontal scaling of API servers
- Distributed agents
- Message queue for async work
- Database read replicas for scaling
