'use client'

export default function PortfolioSummary() {
  return (
    <div className="trading-card lg:col-span-2">
      <div className="mb-2 text-gray-400 text-sm">Portfolio Value</div>
      <div className="text-3xl font-bold mb-4">$125,450.00</div>
      <div className="space-y-2 text-sm">
        <div className="flex justify-between">
          <span className="text-gray-400">Daily P&L:</span>
          <span className="text-green-400 font-semibold">+$2,150.00 (+1.74%)</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-400">Total P&L:</span>
          <span className="text-green-400 font-semibold">+$25,450.00 (+25.45%)</span>
        </div>
      </div>
    </div>
  )
}