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
  
    {/* === SECTION 1: AllAboutFood === */}
    <div className="bg-gradient-to-b from-[#fefbff] via-[#f4f1ff] to-[#f0ebff] transition-colors duration-1000 ease-in-out">
      <motion.section
        initial={{ opacity: 0, y: 60 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: 'easeOut' }}
        viewport={{ once: true }}
      >
        <AllAboutFoodSection />
      </motion.section>
    </div>
  
    {/* === SECTION 2: Lite Client === */}
    <div className="bg-gradient-to-b from-[#f0ebff] via-[#eef9ff] to-[#e1f3ff] transition-colors duration-1000 ease-in-out">
      <motion.section
        initial={{ opacity: 0, y: 60 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: 'easeOut', delay: 0.1 }}
        viewport={{ once: true }}
      >
        <LiteClientSection />
      </motion.section>
    </div>
  
    {/* === SECTION 3: Capstone Recap === */}
    <div className="bg-gradient-to-b from-[#e1f3ff] via-[#f9fbff] to-white transition-colors duration-1000 ease-in-out">
      <motion.section
        initial={{ opacity: 0, y: 60 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: 'easeOut', delay: 0.2 }}
        viewport={{ once: true }}
      >
        <CapstoneSection />
      </motion.section>
    </div>
  
    {/* === GRID SECTIONS: AI, Tennis, Music, More === */}
    <div className="bg-gradient-to-b from-white via-[#fefefe] to-[#f5f5fa]">
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
  
      {/* Footer stays on soft white */}
      <Footer />
    </div>
  </main>
  
  );
}
