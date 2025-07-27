// app/components/Header.tsx
"use client";

import { useState } from "react";
import Link from "next/link";

export default function Header() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="w-full flex justify-center border-b border-gray-200 py-4 sticky top-0 bg-white z-50">
      <nav className="max-w-5xl w-full flex flex-col lg:flex-row lg:justify-between items-center text-sm font-medium px-6">
        <div className="flex justify-between w-full lg:w-auto items-center">
          <Link href="/" className="font-semibold text-lg tracking-tight">Renato DAP</Link>
          <button
            className="lg:hidden text-2xl"
            onClick={() => setMenuOpen(!menuOpen)}
            aria-label="Toggle menu"
          >
            ☰
          </button>
        </div>

        <div className={`flex-col lg:flex lg:flex-row lg:space-x-6 ${menuOpen ? "flex" : "hidden"} lg:items-center w-full lg:w-auto text-center lg:text-left`}>
          <Link href="/about" className="py-2 sm:py-0">About</Link>
          <Link href="/software" className="py-2 sm:py-0">Software</Link>
          <Link href="/music" className="py-2 sm:py-0">Music</Link>
          <Link href="/photo" className="py-2 sm:py-0">Photo</Link>
          <Link href="/tennis" className="py-2 sm:py-0">Tennis</Link>
          <Link href="/education" className="py-2 sm:py-0">Education</Link>
          <Link href="/professional" className="py-2 sm:py-0">Professional</Link>
        </div>
      </nav>
    </header>
  );
}
