'use client';

import { motion } from 'framer-motion';
import Hero from './components/home/HeroSection';
import AllAboutFoodSection from './components/home/CapstoneSection';
import LiteClientSection from './components/home/LiteClientSection';
import CapstoneSection from './components/home/CapstoneSection';
import AISection from './components/home/AISection';
import TennisSection from './components/home/TennisSection';
import MusicSection from './components/home/MusicSection';
import MoreComingSection from './components/home/MoreComingSection';
import Footer from './components/home/footer';

export default function HomePage() {
  return (
    <main className="w-screen overflow-x-hidden relative">

      {/* ===== HERO VIDEO SECTION ===== */}
      <Hero />

      {/* ===== GRADIENT BACKGROUND SECTION STARTS ===== */}
      <div className="relative z-0 bg-gradient-to-b from-[#fefbff] via-[#f4f1ff] to-[#ecf5ff] transition-colors duration-[3000ms] ease-in-out">

        {/* === ALL ABOUT FOOD SECTION === */}
        <motion.section
          initial={{ opacity: 0, y: 60 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: 'easeOut' }}
          viewport={{ once: true }}
        >
          <AllAboutFoodSection />
        </motion.section>

        {/* === ACCUMULATE LITE CLIENT SECTION === */}
        <motion.section
          initial={{ opacity: 0, y: 60 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: 'easeOut', delay: 0.1 }}
          viewport={{ once: true }}
        >
          <LiteClientSection />
        </motion.section>

        {/* === CAPSTONE RECAP (Optional: keep or remove) === */}
        <motion.section
          initial={{ opacity: 0, y: 60 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: 'easeOut', delay: 0.2 }}
          viewport={{ once: true }}
        >
          <CapstoneSection />
        </motion.section>

        {/* === GRID SECTIONS BELOW === */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-y-16 gap-x-0 relative z-10">
          {[AISection, TennisSection, MusicSection, MoreComingSection].map((Sec, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 60 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.9, ease: 'easeOut', delay: i * 0.08 }}
              viewport={{ once: true }}
              className="relative"
            >
              <Sec />
            </motion.div>
          ))}
        </div>

        {/* === FOOTER === */}
        <Footer />
      </div>
    </main>
  );
}
