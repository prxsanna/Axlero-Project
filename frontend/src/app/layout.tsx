import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'MetricMind — Agentic Semantic BI Engine',
  description: 'Enterprise natural language business intelligence with governed semantic metrics and multi-step reasoning.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-dark-base text-gray-100 antialiased selection:bg-blue-600 selection:text-white">
        {children}
      </body>
    </html>
  )
}
