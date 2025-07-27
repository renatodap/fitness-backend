// app/page.tsx

'use client';

import { motion } from 'framer-motion';
import Link from "next/link";
import Image from "next/image";
import Button from "./components/button";
import CapstoneSection from './components/home/CapstoneSection';
import LiteClientSection from './components/home/LiteClientSection';
import AISection from './components/home/AISection';
import TennisSection from './components/home/TennisSection';
import MusicSection from './components/home/MusicSection';
import MoreComingSection from './components/home/MoreComingSection';
import Hero from './components/home/HeroSection';
import Footer from './components/home/footer';

export default function HomePage() {
  return (
    <main className="overflow-x-hidden  relative">
      {/* Background Gradient */}

      {/* Hero Section */}
      <section>
        <Hero/>
      </section>

      {/* Accumulate Lite Client - Featured Video */}
      <motion.section
        initial={{ opacity: 0, y: 50 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: 'easeOut' }}
        viewport={{ once: true }}
      >
        <LiteClientSection />
      </motion.section>

      {/* Capstone Project */}
      <motion.section
        initial={{ opacity: 0, y: 50 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: 'easeOut', delay: 0.1 }}
        viewport={{ once: true }}
      >
        <CapstoneSection />
      </motion.section>

      {/* Grid Sections */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 px-6">
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, ease: 'easeOut' }}
          viewport={{ once: true }}
        >
          <AISection />
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, ease: 'easeOut', delay: 0.05 }}
          viewport={{ once: true }}
        >
          <TennisSection />
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, ease: 'easeOut', delay: 0.1 }}
          viewport={{ once: true }}
        >
          <MusicSection />
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, ease: 'easeOut', delay: 0.15 }}
          viewport={{ once: true }}
        >
          <MoreComingSection />
        </motion.div>
      </div>

      {/* Footer */}
      <Footer />
    </main>
  );
}
