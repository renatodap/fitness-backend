// app/components/Header.tsx
"use client";

import { useState, useEffect } from "react";
import Link from "next/link";

export default function Header() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [isVisible, setIsVisible] = useState(true);
  const [lastScrollY, setLastScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      const currentScrollY = window.scrollY;
      
      // Hide header when scrolling down, show when scrolling up
      if (currentScrollY > lastScrollY && currentScrollY > 100) {
        setIsVisible(false);
      } else {
        setIsVisible(true);
      }
      
      setLastScrollY(currentScrollY);
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, [lastScrollY]);

  return (
    <header className={`w-full flex justify-center py-4 sticky top-0 bg-black/90 backdrop-blur-md border-b border-neutral-800/50 z-50 transition-all duration-300 ease-in-out ${isVisible ? 'translate-y-0' : '-translate-y-full'}`}>
      <nav className="max-w-6xl w-full flex flex-col lg:flex-row lg:justify-between items-center text-sm font-medium px-4 sm:px-6">
        <div className="flex justify-between w-full lg:w-auto items-center">
          <Link href="/" className="font-heading text-lg sm:text-xl font-bold text-white hover:text-teal-400 transition-colors duration-200">
            renato.dap
          </Link>
          <button
            className="lg:hidden text-white hover:text-teal-400 transition-colors duration-200 p-2"
            onClick={() => setMenuOpen(!menuOpen)}
            aria-label="Toggle menu"
          >
            <div className="w-6 h-6 flex flex-col justify-center items-center">
              <span className={`block w-5 h-0.5 bg-current transition-all duration-200 ${menuOpen ? 'rotate-45 translate-y-1' : ''}`} />
              <span className={`block w-5 h-0.5 bg-current mt-1 transition-all duration-200 ${menuOpen ? 'opacity-0' : ''}`} />
              <span className={`block w-5 h-0.5 bg-current mt-1 transition-all duration-200 ${menuOpen ? '-rotate-45 -translate-y-1' : ''}`} />
            </div>
          </button>
        </div>

        <div className={`${menuOpen ? "flex" : "hidden"} lg:flex flex-col lg:flex-row lg:space-x-8 w-full lg:w-auto mt-4 lg:mt-0 space-y-2 lg:space-y-0 text-center lg:text-left bg-black/95 lg:bg-transparent rounded-lg lg:rounded-none p-4 lg:p-0 border border-neutral-800 lg:border-none`}>
          <Link href="/about" className="font-body text-neutral-300 hover:text-white transition-colors duration-200 py-2 lg:py-0">about</Link>
          <Link href="/software" className="font-body text-neutral-300 hover:text-white transition-colors duration-200 py-2 lg:py-0">software</Link>
          <Link href="/music" className="font-body text-neutral-300 hover:text-white transition-colors duration-200 py-2 lg:py-0">music</Link>
          <Link href="/photo" className="font-body text-neutral-300 hover:text-white transition-colors duration-200 py-2 lg:py-0">photo</Link>
          <Link href="/tennis" className="font-body text-neutral-300 hover:text-white transition-colors duration-200 py-2 lg:py-0">tennis</Link>
          <Link href="/education" className="font-body text-neutral-300 hover:text-white transition-colors duration-200 py-2 lg:py-0">education</Link>
          <Link href="/professional" className="font-body text-neutral-300 hover:text-white transition-colors duration-200 py-2 lg:py-0">professional</Link>
        </div>
      </nav>
    </header>
  );
}
