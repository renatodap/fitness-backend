// app/page.tsx

'use client';

import { motion } from 'framer-motion';
import Hero from './components/home/HeroSection';
import CapstoneSection from './components/home/CapstoneSection';
import LiteClientSection from './components/home/LiteClientSection';
import AISection from './components/home/AISection';
import TennisSection from './components/home/TennisSection';
import MusicSection from './components/home/MusicSection';
import MoreComingSection from './components/home/MoreComingSection';
import Footer from './components/home/footer';

export default function HomePage() {
  return (
    <main className="overflow-x-hidden w-screen">
      {/* ===== HERO  (edge‑to‑edge, no outer padding) ===== */}
      <Hero />

      {/* ===== FLOATING BADGE ===== */}
      <section className="relative z-10 -mt-12 sm:-mt-16">

        {/* Floating AllAboutFood badge */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: 'easeOut' }}
          className="absolute -top-8 sm:-top-12 left-6 sm:left-12 inline-flex items-center gap-2 px-5 py-3 backdrop-blur-md bg-white/70 rounded-full shadow-lg ring-1 ring-black/10"
        >
          <img src="/eggplant-icon.svg" alt="AllAboutFood" className="w-6 h-6" />
          <span className="text-sm font-semibold text-neutral-800">AllAboutFood</span>
        </motion.div>
      </section>

      {/* ===== SECTIONS ===== */}
      <motion.section
        initial={{ opacity: 0, y: 60 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: 'easeOut' }}
        viewport={{ once: true }}
      >
        <LiteClientSection />
      </motion.section>

      <motion.section
        initial={{ opacity: 0, y: 60 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: 'easeOut', delay: 0.1 }}
        viewport={{ once: true }}
      >
        <CapstoneSection />
      </motion.section>

      {/* grid WITHOUT side padding – full‑bleed */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-y-16 gap-x-0">
        {[AISection, TennisSection, MusicSection, MoreComingSection].map((Sec, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, ease: 'easeOut', delay: i * 0.05 }}
            viewport={{ once: true }}
          >
            <Sec />
          </motion.div>
        ))}
      </div>

      <Footer />
    </main>
  );
}
