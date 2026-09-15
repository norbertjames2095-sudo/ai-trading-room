'use client'

export default function Opportunities() {
  const opportunities = [
    { symbol: 'BTC/EUR', score: 78, signal: 'BUY', risk: 'MODERATE' },
    { symbol: 'ETH/USD', score: 42, signal: 'HOLD', risk: 'LOW' },
    { symbol: 'EUR/USD', score: 81, signal: 'BUY', risk: 'MODERATE' },
  ]

  return (
    <div className="trading-card">
      <h2 className="text-xl font-semibold mb-4">Trading Opportunities</h2>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-dark-border">
              <th className="text-left py-2 px-4">Asset</th>
              <th className="text-left py-2 px-4">Score</th>
              <th className="text-left py-2 px-4">Signal</th>
              <th className="text-left py-2 px-4">Risk</th>
              <th className="text-left py-2 px-4">Action</th>
            </tr>
          </thead>
          <tbody>
            {opportunities.map((opp) => (
              <tr key={opp.symbol} className="border-b border-dark-border hover:bg-dark-bg">
                <td className="py-3 px-4 font-semibold">{opp.symbol}</td>
                <td className="py-3 px-4">
                  <div className="font-bold text-lg text-blue-400">{opp.score}/100</div>
                </td>
                <td className="py-3 px-4">
                  <span className={`px-3 py-1 rounded text-xs font-semibold ${
                    opp.signal === 'BUY' ? 'bg-green-900 text-green-200' :
                    opp.signal === 'SELL' ? 'bg-red-900 text-red-200' :
                    'bg-yellow-900 text-yellow-200'
                  }`}>
                    {opp.signal}
                  </span>
                </td>
                <td className="py-3 px-4">
                  <span className={`text-xs font-semibold ${
                    opp.risk === 'LOW' ? 'text-green-400' :
                    opp.risk === 'MODERATE' ? 'text-yellow-400' :
                    'text-red-400'
                  }`}>
                    {opp.risk}
                  </span>
                </td>
                <td className="py-3 px-4">
                  <button className="text-blue-400 hover:text-blue-300">View Details</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}