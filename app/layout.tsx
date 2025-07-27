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
    <html lang="en" className="light">
      <body className={inter.className + " bg-black text-white overflow-x-hidden"}>
        <Header />
        <main className="w-full pb-12">{children}</main>
      </body>
    </html>
  );
}
