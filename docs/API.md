# API DOCUMENTATION

## Overview
AI Trading Room provides a comprehensive REST API for managing multi-agent trading operations.

All endpoints are versioned: `/api/v1/*`

## Authentication

### Login
```
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "trader",
  "password": "secure_password"
}

Response:
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

### Using Token
Add to headers:
```
Authorization: Bearer <token>
```

## Endpoints

### Health & Status

#### Health Check
```
GET /health

Response:
{
  "status": "healthy",
  "timestamp": "2026-09-15T10:30:00.000Z",
  "service": "AI Trading Room Backend"
}
```

#### System Status
```
GET /status

Response:
{
  "status": "online",
  "database": "connected",
  "cache": "connected",
  "timestamp": "2026-09-15T10:30:00.000Z"
}
```

### Agents

#### List Agents
```
GET /api/v1/agents/

Response:
[
  {
    "id": "agent_1",
    "name": "Market Scanner",
    "description": "Detects trading opportunities",
    "status": "online"
  },
  ...
]
```

#### Get Agent Details
```
GET /api/v1/agents/{agent_id}

Response:
{
  "id": "agent_1",
  "name": "Market Scanner",
  "description": "Detects trading opportunities",
  "status": "online",
  "model_used": "gpt-3.5-turbo",
  "last_signal_time": "2026-09-15T10:30:00.000Z",
  "total_signals": 150,
  "successful_signals": 120,
  "average_confidence": 0.78
}
```

#### Get Agent Signals
```
GET /api/v1/agents/{agent_id}/signals?limit=20&offset=0

Response:
[
  {
    "timestamp": "2026-09-15T10:30:00.000Z",
    "asset": "BTC/USD",
    "signal": "BUY",
    "confidence": 0.85,
    "data_quality": 0.92
  },
  ...
]
```

### Trades/Orders

#### List Trades
```
GET /api/v1/trades/?status=all&limit=50

Response:
[
  {
    "id": "order_1",
    "asset": "BTC/USD",
    "direction": "BUY",
    "quantity": 0.5,
    "entry_price": 42500,
    "stop_price": 42000,
    "target_price": 43500,
    "status": "FILLED",
    "created_at": "2026-09-15T10:00:00.000Z",
    "executed_at": "2026-09-15T10:05:00.000Z",
    "pnl": 450.00,
    "pnl_percent": 2.12
  },
  ...
]
```

#### Get Trade Details
```
GET /api/v1/trades/{trade_id}

Response:
{
  "id": "order_1",
  "asset": "BTC/USD",
  "direction": "BUY",
  "quantity": 0.5,
  "entry_price": 42500,
  "stop_price": 42000,
  "target_price": 43500,
  "status": "FILLED",
  "risk_manager_approved": "APPROVED",
  "manual_approved": "APPROVED",
  "trading_mode": "paper",
  "execution_price": 42510,
  "execution_quantity": 0.5,
  "slippage_bps": 2.35,
  "commissions": 10.63,
  "pnl": 450.00,
  "pnl_percent": 2.12,
  "created_at": "2026-09-15T10:00:00.000Z",
  "executed_at": "2026-09-15T10:05:00.000Z"
}
```

### Portfolio

#### Portfolio Stats
```
GET /api/v1/portfolio/stats

Response:
{
  "total_equity": 125450.00,
  "cash": 50000.00,
  "positions": 3,
  "daily_pnl": 2150.00,
  "daily_pnl_percent": 1.74,
  "total_pnl": 25450.00,
  "total_pnl_percent": 25.45,
  "max_drawdown": 8500.00,
  "current_drawdown": 2000.00
}
```

#### Open Positions
```
GET /api/v1/portfolio/positions

Response:
[
  {
    "asset": "BTC/USD",
    "quantity": 0.5,
    "entry_price": 42500,
    "current_price": 43000,
    "unrealized_pnl": 250.00,
    "exposure_percent": 17.5
  },
  ...
]
```

#### Portfolio Exposure
```
GET /api/v1/portfolio/exposure

Response:
{
  "total_exposure": 85000.00,
  "exposure_percent": 67.7,
  "by_asset": {
    "BTC/USD": 35000.00,
    "ETH/USD": 30000.00,
    "EUR/USD": 20000.00
  },
  "by_sector": {
    "crypto": 65000.00,
    "forex": 20000.00
  }
}
```

### Risk Management

#### Risk Status
```
GET /api/v1/risk/status

Response:
{
  "daily_loss": -1500.00,
  "daily_loss_limit": -5000.00,
  "exposure": 85000.00,
  "exposure_limit": 80000.00,
  "drawdown": 2000.00,
  "drawdown_limit": 20000.00,
  "kill_switch": false,
  "risk_level": "MODERATE"
}
```

#### Kill Switch (EMERGENCY)
```
POST /api/v1/risk/kill-switch
Authorization: Bearer <admin_token>

Response:
{
  "message": "Kill switch activated",
  "timestamp": "2026-09-15T10:30:00.000Z",
  "active": true
}
```

#### Get Risk Config
```
GET /api/v1/risk/config

Response:
{
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
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters",
  "error_code": "INVALID_REQUEST"
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication required",
  "error_code": "UNAUTHORIZED"
}
```

### 403 Forbidden
```json
{
  "detail": "Insufficient permissions",
  "error_code": "FORBIDDEN"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found",
  "error_code": "NOT_FOUND"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error",
  "error_code": "INTERNAL_ERROR",
  "error": "Error message"
}
```

## Rate Limiting

API endpoints are rate limited:
- **Authenticated users**: 1000 requests per minute
- **Public endpoints**: 100 requests per minute

Rate limit headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 950
X-RateLimit-Reset: 1694687400
```

## WebSocket

Real-time updates via WebSocket:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws')

ws.onmessage = (event) => {
  const data = JSON.parse(event.data)
  // data can be:
  // - market_update
  // - trade_execution
  // - signal_generated
  // - risk_alert
}
```

## Pagination

List endpoints support pagination:
```
GET /api/v1/trades/?limit=50&offset=0

Response includes:
{
  "items": [...],
  "total": 150,
  "limit": 50,
  "offset": 0
}
```
