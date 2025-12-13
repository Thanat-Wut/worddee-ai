
import type { Metadata } from 'next'
import Link from 'next/link'
import './globals.css'

export const metadata: Metadata = {
  title: 'Worddee.ai - AI-Powered English Practice',
  description: 'Practice English vocabulary with AI-powered feedback',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <nav className="nav">
          <div className="nav-content">
            <Link href="/" className="nav-title">
              ✍️ Worddee.ai
            </Link>
            <div className="nav-links">
              <Link href="/" className="nav-link">
                Practice
              </Link>
              <Link href="/dashboard" className="nav-link">
                Dashboard
              </Link>
            </div>
          </div>
        </nav>
        <main className="container">
          {children}
        </main>
        <footer style={{ 
          textAlign: 'center', 
          color: 'white', 
          padding: '2rem',
          opacity: 0.8,
          fontSize: '0.875rem'
        }}>
          <p>© 2025 Worddee.ai - Powered by AI</p>
        </footer>
      </body>
    </html>
  )
}
