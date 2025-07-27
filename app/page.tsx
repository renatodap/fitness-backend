'use client';

import { motion } from 'framer-motion';
import Hero from './components/home/HeroSection';
import SectionBlock from './components/home/SectionBlock';
import Footer from './components/home/footer';

// Content config (images, text, etc.)
type Align = "center" | "left" | "right";
type Section = {
  id: string;
  title: string;
  description: string;
  ctas: Array<{ href: string; label: string; variant: 'solid' | 'outline' }>;
  // Or, if you prefer to import CTA type from SectionBlock:
  // import type { CTA } from './components/home/SectionBlock';
  // ctas: CTA[];
  image: string;
  align: Align;
  bgClass: string;
};

const SECTIONS: Section[] = [
  {
    id: 'aaf',
    title: 'All About Food',
    description:
      'A full-stack AI-powered recipe engine that transforms images, PDFs, or text files into structured, searchable, voice-ready cooking instructions.',
    ctas: [
      { href: '/projects/allaboutfood', label: 'See Case Study', variant: 'solid' },
      { href: 'https://github.com/renatodap/allaboutfood', label: 'View Code', variant: 'outline' },
    ],
    image: '/all-about-food.png',
    align: 'left',
    bgClass: 'from-white to-[#fef6f9]',
  },
  {
    id: 'liteclient',
    title: 'Accumulate Lite Client',
    description:
      'A lightweight blockchain verification client, built to bridge AI and secure decentralization. Designed, architected, and documented from scratch.',
    ctas: [
      { href: 'https://www.youtube.com/watch?v=your-liteclient-video', label: 'Watch the Video', variant: 'solid' },
      { href: 'https://github.com/renatodap/accumulate-liteclient', label: 'View Code', variant: 'outline' },
    ],
    image: '/acc-lite-client.png',
    align: 'right',
    bgClass: 'from-[#fef6f9] to-[#f3f8fc]',
  },
  {
    id: 'ai',
    title: 'AI Coursework – Fall 2025',
    description:
      'I’m diving deep into Machine Learning and AI Theory this fall. Real math, real models, real understanding — not just tools, but how they work.',
    ctas: [{ href: '/ai-courses', label: 'See Course Plan', variant: 'solid' }],
    image: '/ai-icon.svg',
    align: 'center',
    bgClass: 'from-[#f3f8fc] to-white',
  },
  {
    id: 'tennis',
    title: 'Fall Tennis Season',
    description:
      'I compete in NCAA tennis while training 6 days a week. It’s how I stay sharp — physically, mentally, and emotionally.',
    ctas: [{ href: '/tennis', label: 'View Season Schedule', variant: 'solid' }],
    image: '/tennis.jpg',
    align: 'left',
    bgClass: 'from-white to-[#f4f7f5]',
  },
  {
    id: 'music',
    title: 'Live Music & Open Mic',
    description:
      'Performing live keeps me honest. Music gives me rhythm, presence, and the confidence to be fully seen — on stage or in front of a whiteboard.',
    ctas: [{ href: '/music', label: 'Watch a Performance', variant: 'solid' }],
    image: '/live.jpg',
    align: 'right',
    bgClass: 'from-[#f4f7f5] to-[#fefefe]',
  },
];

export default function HomePage() {
  return (
    <main className="w-screen overflow-x-hidden relative">

      {/* ===== HERO VIDEO SECTION ===== */}
      <Hero />

      {/* ===== SECTION SCROLL EXPERIENCE ===== */}
      {SECTIONS.map((section, i) => (
        <div
          key={section.id}
          className={`relative bg-gradient-to-b ${section.bgClass} transition-colors duration-1000 ease-in-out`}
        >
          <motion.section
            initial={{ opacity: 0, y: 60 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: 'easeOut', delay: i * 0.05 }}
            viewport={{ once: true }}
          >
            <SectionBlock
              title={section.title}
              description={section.description}
              image={section.image}
              align={section.align}
              ctas={section.ctas}
            />
          </motion.section>
        </div>
      ))}

      <Footer />
    </main>
  );
}
