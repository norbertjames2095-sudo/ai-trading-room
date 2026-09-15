'use client'

export default function AgentStatus() {
  return (
    <div className="trading-card">
      <div className="mb-2 text-gray-400 text-sm">Agents Status</div>
      <div className="text-2xl font-bold mb-4">20/20 Online</div>
      <div className="flex space-x-1">
        <div className="w-full h-2 bg-green-500 rounded"></div>
      </div>
      <div className="mt-4 text-xs text-gray-400">
        All systems operational
      </div>
    </div>
  )
}