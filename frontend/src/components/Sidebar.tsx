'use client'

import Link from 'next/link'
import { BarChart3, TrendingUp, AlertCircle, Settings } from 'lucide-react'

export default function Sidebar() {
  const menuItems = [
    { icon: BarChart3, label: 'Dashboard', href: '/dashboard' },
    { icon: TrendingUp, label: 'Opportunities', href: '/opportunities' },
    { icon: 'position-icon', label: 'Positions', href: '/positions' },
    { icon: 'trades-icon', label: 'Trades', href: '/trades' },
    { icon: 'agents-icon', label: 'Agents', href: '/agents' },
    { icon: AlertCircle, label: 'Alerts', href: '/alerts' },
    { icon: Settings, label: 'Settings', href: '/settings' },
  ]

  return (
    <aside className="w-64 bg-dark-card border-r border-dark-border">
      <div className="p-6">
        <h1 className="text-2xl font-bold text-blue-500">🤖 ATRM</h1>
      </div>
      <nav className="space-y-2 px-4">
        {menuItems.map((item, i) => {
          const Icon = typeof item.icon === 'function' ? item.icon : null
          return (
            <Link
              key={i}
              href={item.href}
              className="flex items-center space-x-3 px-4 py-2 rounded-lg hover:bg-dark-bg transition-colors"
            >
              {Icon && <Icon size={20} />}
              <span>{item.label}</span>
            </Link>
          )
        })}
      </nav>
    </aside>
  )
}