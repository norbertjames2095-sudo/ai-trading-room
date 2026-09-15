'use client'

export default function MarketStatus() {
  const markets = [
    { symbol: 'BTC/USD', price: 42500, change: 2.5, status: '📈' },
    { symbol: 'ETH/USD', price: 2250, change: -1.2, status: '📉' },
    { symbol: 'EUR/USD', price: 1.0850, change: 0.3, status: '➡️' },
    { symbol: 'S&P 500', price: 4720, change: 1.8, status: '📈' },
  ]

  return (
    <div className="trading-card">
      <h2 className="text-xl font-semibold mb-4">Market Status</h2>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {markets.map((market) => (
          <div key={market.symbol} className="bg-dark-bg rounded p-4">
            <div className="flex justify-between items-start">
              <div>
                <div className="font-semibold text-blue-400">{market.symbol}</div>
                <div className="text-2xl font-bold mt-2">{market.price}</div>
              </div>
              <div className="text-2xl">{market.status}</div>
            </div>
            <div className={`mt-3 text-sm ${market.change >= 0 ? 'text-green-400' : 'text-red-400'}`}>
              {market.change > 0 ? '+' : ''}{market.change}%
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}