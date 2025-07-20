// app/layout.tsx
import "./globals.css";
import { Inter } from "next/font/google";
import Header from "./components/header"; // 👈 import client component

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "Renato DAP",
  description: "The digital home of Renato DAP — exploring logic, rhythm, and connection."
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={inter.className + " bg-white text-black overflow-x-hidden"}>
        <Header />
        <main className="w-full px-6 py-12">{children}</main>
      </body>
    </html>
  );
}
