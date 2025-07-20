// app/layout.tsx
import './globals.css';
import Link from 'next/link';

export const metadata = {
  title: 'Renato DAP',
  description: 'Portfolio of Renato DAP',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-white text-gray-900 font-sans">
        <header className="sticky top-0 z-50 bg-white shadow-md">
          <nav className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
            <span className="text-xl font-bold tracking-tight">Renato DAP</span>
            <ul className="flex space-x-6 text-sm font-medium">
              <li><Link href="/">Home</Link></li>
              <li><Link href="/music">Music</Link></li>
              <li><Link href="/photo">Photo/Video</Link></li>
              <li><Link href="/tennis">Tennis</Link></li>
              <li><Link href="/coding">Coding</Link></li>
              <li><Link href="/timeline">Timeline</Link></li>
              <li><Link href="/personal">Personal</Link></li>
            </ul>
          </nav>
        </header>

        <main className="max-w-3xl mx-auto px-6 py-20">{children}</main>

        <footer className="text-center text-xs text-gray-500 py-10">
          © {new Date().getFullYear()} Renato DAP. All rights reserved.
        </footer>
      </body>
    </html>
  );
}
