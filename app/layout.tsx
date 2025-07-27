// app/layout.tsx
import "./globals.css";
import { Inter, JetBrains_Mono } from "next/font/google";
import Header from "./components/header"; // 👈 import client component

const inter = Inter({ 
  subsets: ["latin"],
  variable: '--font-inter',
  display: 'swap'
});

const jetbrainsMono = JetBrains_Mono({ 
  subsets: ["latin"],
  variable: '--font-jetbrains-mono',
  display: 'swap'
});

export const metadata = {
  title: "Renato DAP",
  description: "The digital home of Renato DAP — exploring logic, rhythm, and connection."
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="light">
      <body className={`${inter.variable} ${jetbrainsMono.variable} bg-white text-black overflow-x-hidden min-h-screen`}>
        <Header />
        <main className="w-full">{children}</main>
      </body>
    </html>
  );
}
