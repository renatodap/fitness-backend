'use client';

import { motion, useScroll, useTransform } from 'framer-motion';
import { useRef } from 'react';
import Hero from './components/home/HeroSection';
import SectionBlock from './components/home/SectionBlock';
import Footer from './components/home/footer';

// Content config (images, text, etc.)
type Align = "center" | "left" | "right";
type Section = {
  id: string;
  title: string;
  description: string | React.ReactNode;
  ctas: Array<{ href: string; label: string; variant: 'solid' | 'outline' }>;
  // Or, if you prefer to import CTA type from SectionBlock:
  // import type { CTA } from './components/home/SectionBlock';
  // ctas: CTA[];
  image: string;
  align: Align;
  bgClass: string;
  overlaySvg?: React.ReactNode;
};

const SECTIONS: Section[] = [
  {
    id: 'aaf',
    title: 'All About Food',
    description: 'A full-stack AI-powered recipe engine that transforms images, PDFs, or text files into structured, searchable, voice-ready cooking instructions.',
    ctas: [
      { href: '/projects/allaboutfood', label: 'See Case Study', variant: 'solid' },
      { href: 'https://github.com/renatodap/allaboutfood', label: 'View Code', variant: 'outline' },
    ],
    image: '/all-about-food.png',
    align: 'left',
    bgClass: 'from-neutral-50 via-white to-teal-50/30',
  },
  {
    id: 'liteclient',
    title: 'Accumulate Lite Client',
    description: 'A lightweight blockchain verification client, built to bridge AI and secure decentralization. Designed, architected, and documented from scratch.',
    ctas: [
      { href: 'https://www.youtube.com/watch?v=your-liteclient-video', label: 'Watch the Video', variant: 'solid' },
      { href: 'https://github.com/renatodap/accumulate-liteclient', label: 'View Code', variant: 'outline' },
    ],
    image: '/acc-lite-client.png',
    align: 'right',
    bgClass: 'from-teal-50/30 via-white to-rose-50/30',
  },
  {
    id: 'ai',
    title: 'AI Coursework – Fall 2025',
    description: (
      <div className="space-y-4">
        <p>
          I'm studying the foundations that power modern AI: from deep learning theory to data-driven reasoning systems.
        </p>
        <ul className="list-disc pl-5 space-y-1 text-left">
          <li>
            <strong>CSSE 313 – Artificial Intelligence</strong>: Symbolic reasoning, pattern recognizers, and beneficial AI system design.
          </li>
          <li>
            <strong>CSSE/MA 416 – Deep Learning</strong>: CNNs, optimization, backpropagation, regularization, and transfer learning.
          </li>
        </ul>
      </div>
    ),
    ctas: [
      { href: '/ai-courses', label: 'See Course Plan', variant: 'solid' },
    ],
    image: '/ai-icon.svg',
    align: 'center',
    bgClass: 'from-rose-50/30 via-white to-orange-50/30',
    overlaySvg: (
      <svg
        viewBox="0 0 100 100"
        className="w-48 h-48 text-neutral-600"
        fill="none"
        stroke="currentColor"
        strokeWidth={1.2}
      >
        <circle cx="50" cy="50" r="45" />
        <path d="M50 10 L50 90 M10 50 L90 50" />
        <circle cx="50" cy="50" r="3" fill="currentColor" />
        <circle cx="25" cy="25" r="2" fill="currentColor" />
        <circle cx="75" cy="25" r="2" fill="currentColor" />
        <circle cx="25" cy="75" r="2" fill="currentColor" />
        <circle cx="75" cy="75" r="2" fill="currentColor" />
      </svg>
    ),
  },
  {
    id: 'tennis',
    title: 'Fall Tennis Season',
    description: 'I compete in NCAA tennis while training 6 days a week. It is how I stay sharp - physically, mentally, and emotionally.',
    ctas: [{ href: '/tennis', label: 'View Season Schedule', variant: 'solid' }],
    image: '/tennis.jpg',
    align: 'left',
    bgClass: 'from-orange-50/30 via-white to-neutral-50',
  },
  {
    id: 'music',
    title: 'Live Music & Open Mic',
    description: 'Performing live keeps me honest. Music gives me rhythm, presence, and the confidence to be fully seen - on stage or in front of a whiteboard.',
    ctas: [{ href: '/music', label: 'Watch a Performance', variant: 'solid' }],
    image: '/live.jpg',
    align: 'right',
    bgClass: 'from-neutral-50 to-white',
  },
];

export default function HomePage() {
  const containerRef = useRef<HTMLElement>(null);
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ['start start', 'end end']
  });

  const backgroundY = useTransform(scrollYProgress, [0, 1], ['0%', '100%']);
  const opacity = useTransform(scrollYProgress, [0, 0.2, 0.8, 1], [1, 0.8, 0.8, 1]);

  return (
    <main ref={containerRef} className="w-full min-h-screen overflow-x-hidden relative">
      {/* Subtle Background Elements */}
      <motion.div 
        className="fixed inset-0 z-[-1] pointer-events-none"
        style={{ y: backgroundY, opacity }}
      >
        <div className="absolute top-1/4 right-1/4 w-48 h-48 sm:w-80 sm:h-80 lg:w-96 lg:h-96 bg-gradient-to-br from-teal-500/5 to-transparent rounded-full blur-2xl sm:blur-3xl" />
        <div className="absolute bottom-1/4 left-1/4 w-40 h-40 sm:w-64 sm:h-64 lg:w-80 lg:h-80 bg-gradient-to-br from-rose-500/5 to-transparent rounded-full blur-2xl sm:blur-3xl" />
        <div className="absolute top-3/4 right-1/3 w-32 h-32 sm:w-48 sm:h-48 lg:w-64 lg:h-64 bg-gradient-to-br from-orange-500/5 to-transparent rounded-full blur-xl sm:blur-3xl" />
      </motion.div>

      {/* ===== HERO VIDEO SECTION ===== */}
      <Hero />

      {/* ===== SECTION SCROLL EXPERIENCE ===== */}
      <div className="relative z-10">
        {SECTIONS.map((section, i) => {
          const sectionY = useTransform(
            scrollYProgress,
            [i / SECTIONS.length, (i + 1) / SECTIONS.length],
            ['0%', '-5%']
          );
          
          return (
            <motion.div
              key={section.id}
              className={`relative bg-gradient-to-br ${section.bgClass} transition-all duration-1000 ease-in-out`}
              style={{ y: sectionY }}
            >
              {/* Section divider */}
              {i > 0 && (
                <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-neutral-200 to-transparent" />
              )}
              
              <SectionBlock
                title={section.title}
                description={section.description}
                image={section.image}
                align={section.align}
                ctas={section.ctas}
                overlaySvg={section.overlaySvg}
              />
            </motion.div>
          );
        })}
      </div>

      <Footer />
    </main>
  );
}
