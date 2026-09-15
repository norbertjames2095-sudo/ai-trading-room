import type { Metadata } from 'next'
import './styles/globals.css'

export const metadata: Metadata = {
  title: 'AI Trading Room',
  description: 'Professional Multi-Agent AI Trading Platform',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}