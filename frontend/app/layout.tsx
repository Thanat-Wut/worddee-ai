/**
 * ════════════════════════════════════════════════════════════════
 * Root Layout
 * ════════════════════════════════════════════════════════════════
 */
import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Worddee.ai - English Practice',
  description: 'AI-powered English sentence practice',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <header>
          <h1>��� Worddee.ai</h1>
          <nav>
            <a href="/">Practice</a>
            <a href="/dashboard">Dashboard</a>
          </nav>
        </header>
        <main>{children}</main>
      </body>
    </html>
  );
}
