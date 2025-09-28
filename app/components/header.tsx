// app/components/Header.tsx
"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Header() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [isVisible, setIsVisible] = useState(true);
  const [lastScrollY, setLastScrollY] = useState(0);
  const pathname = usePathname();

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

  // Career Fair Version: Navigation items hidden
  const navItems: { href: string, label: string, accent: string }[] = [
    // { href: "/engineer", label: "Engineer", accent: "teal" },
    // { href: "/creator", label: "Creator", accent: "rose" },
    // { href: "/essence", label: "Essence", accent: "orange" }
  ];

  const getAccentColor = (accent: string, isActive: boolean) => {
    if (isActive) {
      switch (accent) {
        case 'teal': return 'text-teal-500';
        case 'rose': return 'text-rose-500';
        case 'orange': return 'text-orange-500';
        default: return 'text-teal-500';
      }
    }
    return 'text-neutral-600 hover:text-neutral-900';
  };

  return (
    <header className={`w-full flex justify-center py-4 sticky top-0 bg-white/90 backdrop-blur-md border-b border-neutral-200/50 z-50 transition-all duration-300 ease-in-out ${isVisible ? 'translate-y-0' : '-translate-y-full'}`}>
      <nav className="max-w-6xl w-full flex flex-col lg:flex-row lg:justify-between items-center text-sm font-medium px-4 sm:px-6">
        <div className="flex justify-between w-full lg:w-auto items-center h-12">
          <Link href="/" className="font-heading text-lg sm:text-xl font-bold text-black hover:text-teal-600 transition-colors duration-200 flex items-center h-full">
            Renato DAP
          </Link>
          {navItems.length > 0 && (
            <button
              className="lg:hidden text-black hover:text-teal-600 transition-colors duration-200 p-2"
              onClick={() => setMenuOpen(!menuOpen)}
              aria-label="Toggle menu"
            >
            <div className="w-6 h-6 flex flex-col justify-center items-center">
              <span className={`block w-5 h-0.5 bg-current transition-all duration-200 ${menuOpen ? 'rotate-45 translate-y-1' : ''}`} />
              <span className={`block w-5 h-0.5 bg-current mt-1 transition-all duration-200 ${menuOpen ? 'opacity-0' : ''}`} />
              <span className={`block w-5 h-0.5 bg-current mt-1 transition-all duration-200 ${menuOpen ? '-rotate-45 -translate-y-1' : ''}`} />
            </div>
          </button>
          )}
        </div>

        {navItems.length > 0 && (
          <div className={`${menuOpen ? "flex" : "hidden"} lg:flex flex-col lg:flex-row lg:space-x-8 w-full lg:w-auto mt-4 lg:mt-0 space-y-2 lg:space-y-0 text-center lg:text-left bg-white/95 lg:bg-transparent rounded-lg lg:rounded-none p-4 lg:p-0 border border-neutral-200 lg:border-none`}>
          {navItems.map((item) => (
            <Link 
              key={item.href}
              href={item.href} 
              className={`font-body transition-colors duration-200 py-2 lg:py-0 ${
                getAccentColor(item.accent, pathname === item.href)
              }`}
              onClick={() => setMenuOpen(false)}
            >
              {item.label}
            </Link>
          ))}
        </div>
        )}
      </nav>
    </header>
  );
}
