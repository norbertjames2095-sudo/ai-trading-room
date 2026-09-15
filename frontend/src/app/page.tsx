'use client'

import Link from 'next/link'

export default function Home() {
  return (
    <main className="min-h-screen bg-dark-bg">
      {/* Navigation */}
      <nav className="bg-dark-card border-b border-dark-border">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="text-2xl font-bold text-blue-500">🤖 AI Trading Room</div>
          <div className="space-x-6">
            <Link href="/dashboard" className="hover:text-blue-400">Dashboard</Link>
            <Link href="/agents" className="hover:text-blue-400">Agents</Link>
            <Link href="/portfolio" className="hover:text-blue-400">Portfolio</Link>
            <Link href="/settings" className="hover:text-blue-400">Settings</Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="max-w-7xl mx-auto px-4 py-20 text-center">
        <h1 className="text-5xl font-bold mb-6">Professional AI Trading Platform</h1>
        <p className="text-xl text-gray-300 mb-8">
          Multi-agent system for research, backtesting, and paper trading
        </p>
        <div className="space-x-4">
          <Link href="/dashboard" className="trading-button-primary inline-block">
            Launch Dashboard
          </Link>
          <Link href="#features" className="trading-button inline-block bg-gray-700 hover:bg-gray-600">
            Learn More
          </Link>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="max-w-7xl mx-auto px-4 py-20">
        <h2 className="text-3xl font-bold mb-12 text-center">Platform Features</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            {
              title: '20 Specialized Agents',
              description: 'Market analysis, risk management, and decision coordination'
            },
            {
              title: 'Multiple Trading Modes',
              description: 'Research, Backtest, Paper Trading, and Live (controlled)'
            },
            {
              title: 'Professional Dashboard',
              description: 'Real-time market data, positions, P&L, and alerts'
            },
            {
              title: 'Risk Engine',
              description: 'Deterministic, immutable risk rules and Kill Switch'
            },
            {
              title: 'Backtesting',
              description: 'Historical testing with walk-forward validation'
            },
            {
              title: 'Complete Audit Trail',
              description: 'Every decision logged and auditable'
            },
          ].map((feature, i) => (
            <div key={i} className="trading-card">
              <h3 className="text-xl font-semibold mb-4 text-blue-400">{feature.title}</h3>
              <p className="text-gray-300">{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-dark-card border-t border-dark-border mt-20">
        <div className="max-w-7xl mx-auto px-4 py-8 text-center text-gray-400">
          <p>Built with precision. Designed for safety. Ready for scale.</p>
          <p className="mt-2 text-sm">© 2026 AI Trading Room. MIT License.</p>
        </div>
      </footer>
    </main>
  )
}