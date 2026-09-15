'use client'

import { Bell, Settings, LogOut } from 'lucide-react'

export default function Header() {
  return (
    <header className="bg-dark-card border-b border-dark-border px-6 py-4 flex justify-between items-center">
      <div className="text-xl font-semibold">AI Trading Room</div>
      <div className="flex items-center space-x-6">
        <button className="hover:text-blue-400 transition-colors">
          <Bell size={20} />
        </button>
        <button className="hover:text-blue-400 transition-colors">
          <Settings size={20} />
        </button>
        <button className="hover:text-red-400 transition-colors">
          <LogOut size={20} />
        </button>
      </div>
    </header>
  )
}