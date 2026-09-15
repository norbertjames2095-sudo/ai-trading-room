'use client'

export default function RiskStatus() {
  return (
    <div className="trading-card">
      <div className="mb-2 text-gray-400 text-sm">Daily Risk Usage</div>
      <div className="text-2xl font-bold mb-4">45%</div>
      <div className="w-full bg-dark-bg rounded h-2 overflow-hidden">
        <div className="h-full bg-yellow-500" style={{width: '45%'}}></div>
      </div>
      <div className="mt-4 text-xs text-gray-400">
        $4,500 / $10,000 limit
      </div>
    </div>
  )
}