'use client'

import { useState, useEffect } from 'react'
import Sidebar from '@/components/Sidebar'
import Header from '@/components/Header'
import MarketStatus from '@/components/dashboard/MarketStatus'
import Opportunities from '@/components/dashboard/Opportunities'
import PortfolioSummary from '@/components/dashboard/PortfolioSummary'
import RiskStatus from '@/components/dashboard/RiskStatus'
import AgentStatus from '@/components/dashboard/AgentStatus'

export default function Dashboard() {
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simulate data loading
    const timer = setTimeout(() => setLoading(false), 1000)
    return () => clearTimeout(timer)
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-dark-bg">
        <div className="text-xl text-gray-400">Loading...</div>
      </div>
    )
  }

  return (
    <div className="flex h-screen bg-dark-bg">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        <main className="flex-1 overflow-y-auto p-6 space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
            <PortfolioSummary />
            <RiskStatus />
            <AgentStatus />
          </div>
          <MarketStatus />
          <Opportunities />
        </main>
      </div>
    </div>
  )
}