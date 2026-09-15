export const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
export const WS_URL = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000'

export const API_ENDPOINTS = {
  HEALTH: '/health',
  STATUS: '/status',
  LOGIN: '/api/v1/auth/login',
  LOGOUT: '/api/v1/auth/logout',
  CURRENT_USER: '/api/v1/users/me',
  AGENTS: '/api/v1/agents',
  TRADES: '/api/v1/trades',
  PORTFOLIO: '/api/v1/portfolio',
  RISK: '/api/v1/risk',
}

export const TRADING_MODES = {
  RESEARCH: 'research',
  BACKTEST: 'backtest',
  PAPER: 'paper',
  LIVE: 'live',
} as const

export const SIGNALS = {
  BUY: 'BUY',
  SELL: 'SELL',
  HOLD: 'HOLD',
  NO_TRADE: 'NO_TRADE',
} as const