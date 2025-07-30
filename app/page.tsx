'use client';

import { motion, useScroll, useTransform, useInView } from 'framer-motion';
import { useRef } from 'react';
import Hero from './components/home/HeroSection';
import Footer from './components/home/footer';
import Image from 'next/image';

// === CINEMATIC COMPONENTS ===

function CinematicSection({ children, className = '', delay = 0 }: { 
  children: React.ReactNode; 
  className?: string; 
  delay?: number;
}) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: '-50px' });
  
  return (
    <motion.div
      ref={ref}
      className={className}
      initial={{ opacity: 0, y: 60 }}
      animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 60 }}
      transition={{ duration: 1.2, ease: 'easeOut', delay }}
    >
      {children}
    </motion.div>
  );
}

function ParallaxText({ children, offset = 50 }: { children: React.ReactNode; offset?: number }) {
  const ref = useRef(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ['start end', 'end start']
  });
  const y = useTransform(scrollYProgress, [0, 1], [offset, -offset]);
  
  return (
    <motion.div ref={ref} style={{ y }}>
      {children}
    </motion.div>
  );
}

function FloatingCard({ children, index = 0 }: { children: React.ReactNode; index?: number }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 40, rotateX: 10 }}
      whileInView={{ opacity: 1, y: 0, rotateX: 0 }}
      transition={{ duration: 0.8, delay: index * 0.1, ease: 'easeOut' }}
      viewport={{ once: true, margin: '-50px' }}
      whileHover={{ y: -8, scale: 1.02 }}
      className="transform-gpu"
    >
      {children}
    </motion.div>
  );
}

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
    image: '/all-about-food.PNG',
    align: 'left',
    bgClass: 'bg-white border-b border-neutral-100',
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
    bgClass: 'bg-neutral-25 border-b border-neutral-100',
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
    image: '/file.svg',
    align: 'center',
    bgClass: 'bg-white border-b border-neutral-100',
  },
  {
    id: 'tennis',
    title: 'Fall Tennis Season',
    description: 'I compete in NCAA tennis while training 6 days a week. It is how I stay sharp - physically, mentally, and emotionally.',
    ctas: [{ href: '/tennis', label: 'View Season Schedule', variant: 'solid' }],
    image: '/tennis.JPG',
    align: 'left',
    bgClass: 'bg-neutral-25 border-b border-neutral-100',
  },
  {
    id: 'music',
    title: 'Live Music & Open Mic',
    description: 'Performing live keeps me honest. Music gives me rhythm, presence, and the confidence to be fully seen - on stage or in front of a whiteboard.',
    ctas: [{ href: '/music', label: 'Watch a Performance', variant: 'solid' }],
    image: '/live.jpg',
    align: 'right',
    bgClass: 'bg-white',
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
      <div className="relative z-10 bg-white">
        {SECTIONS.map((section, i) => {
          const sectionY = useTransform(
            scrollYProgress,
            [i / SECTIONS.length, (i + 1) / SECTIONS.length],
            ['0%', '-5%']
          );
          
          return (
            <motion.div
              key={section.id}
              className={`relative ${section.bgClass}`}
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

      {/* ===== PERSONAL INTRO SECTION ===== */}
      <section className="py-20 sm:py-24 lg:py-32 px-4 sm:px-6 lg:px-8 bg-teal-50 border-t border-teal-100">
        <div className="max-w-5xl mx-auto text-center space-y-8">
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight text-neutral-900">Software Engineer & Creative Mind</h2>
          <p className="text-lg sm:text-xl lg:text-2xl text-neutral-700 max-w-4xl mx-auto leading-relaxed">
            I'm a Computer Science student at Rose-Hulman, focused on building software tools
            that solve real problems, producing music and video that tell meaningful stories,
            and leading as captain of the men's varsity tennis team. I work across code, creativity,
            and competition—always looking to make things that matter.
          </p>
        </div>
      </section>

      {/* ===== CONNECT SECTION ===== */}
      <section className="py-20 sm:py-24 lg:py-32 px-4 sm:px-6 lg:px-8 bg-white text-center">
        <div className="max-w-4xl mx-auto space-y-12">
          <div className="space-y-6">
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight text-neutral-900">Let's Connect</h2>
            <p className="text-lg sm:text-xl lg:text-2xl text-neutral-600 leading-relaxed max-w-3xl mx-auto">
              Interested in collaborating, discussing ideas, or just saying hello? I'd love to hear from you.
            </p>
          </div>
          
          <div className="flex flex-row justify-center items-center gap-8 pt-4">
            <a href="https://linkedin.com/in/renatodap" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn" className="group">
              <svg className="w-8 h-8 text-neutral-600 group-hover:text-teal-600 transition-colors duration-200" fill="currentColor" viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.761 0 5-2.239 5-5v-14c0-2.761-2.239-5-5-5zm-11 19h-3v-10h3v10zm-1.5-11.268c-.966 0-1.75-.784-1.75-1.75s.784-1.75 1.75-1.75 1.75.784 1.75 1.75-.784 1.75-1.75 1.75zm13.5 11.268h-3v-5.604c0-1.337-.025-3.063-1.868-3.063-1.869 0-2.156 1.459-2.156 2.967v5.7h-3v-10h2.881v1.367h.041c.401-.761 1.381-1.563 2.841-1.563 3.041 0 3.602 2.002 3.602 4.604v5.592z" /></svg>
            </a>
            <a href="https://open.spotify.com/artist/3VZ8V9XhQ9oZb5XnZ9g8yB" target="_blank" rel="noopener noreferrer" aria-label="Spotify" className="group">
              <svg className="w-8 h-8 text-neutral-600 group-hover:text-teal-600 transition-colors duration-200" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0C5.371 0 0 5.371 0 12s5.371 12 12 12 12-5.371 12-12S18.629 0 12 0zm5.363 17.463c-.221.364-.691.482-1.055.262-2.891-1.764-6.543-2.16-10.824-1.18-.418.096-.844-.162-.94-.576-.096-.418.162-.844.576-.94 4.663-1.08 8.727-.641 11.947 1.262.364.22.482.69.262 1.055zm1.504-2.67c-.276.447-.854.59-1.301.314-3.309-2.04-8.362-2.635-12.284-1.44-.51.158-1.055-.117-1.213-.627-.158-.51.117-1.055.627-1.213 4.406-1.361 9.927-.709 13.722 1.578.447.276.59.854.314 1.301zm.146-2.835C15.06 9.684 8.924 9.5 5.934 10.384c-.623.182-1.283-.159-1.464-.783-.181-.624.159-1.283.783-1.464 3.417-.99 10.184-.785 14.047 2.016.527.389.642 1.135.254 1.662-.389.527-1.135.643-1.662.254z" /></svg>
            </a>
            <a href="https://www.youtube.com/@RenatoDAP" target="_blank" rel="noopener noreferrer" aria-label="YouTube" className="group">
              <svg className="w-8 h-8 text-neutral-600 group-hover:text-teal-600 transition-colors duration-200" fill="currentColor" viewBox="0 0 24 24"><path d="M23.498 6.186a2.994 2.994 0 0 0-2.112-2.117C19.257 3.5 12 3.5 12 3.5s-7.257 0-9.386.569A2.994 2.994 0 0 0 .502 6.186C0 8.313 0 12 0 12s0 3.687.502 5.814a2.994 2.994 0 0 0 2.112 2.117C4.743 20.5 12 20.5 12 20.5s7.257 0 9.386-.569a2.994 2.994 0 0 0 2.112-2.117C24 15.687 24 12 24 12s0-3.687-.502-5.814zM9.75 15.5v-7l6.5 3.5-6.5 3.5z" /></svg>
            </a>
          </div>
          
          <div className="flex flex-col sm:flex-row justify-center items-center gap-6 pt-8">
            <a href="/professional" className="inline-flex items-center justify-center px-8 py-4 border border-transparent text-lg font-medium rounded-lg text-white bg-neutral-900 hover:bg-neutral-800 transition-colors duration-200 shadow-sm hover:shadow-md">
              Professional Experience
            </a>
            <a href="mailto:renatodaprado@gmail.com" className="inline-flex items-center justify-center px-8 py-4 border border-neutral-300 text-lg font-medium rounded-lg text-neutral-900 bg-white hover:bg-neutral-50 hover:border-neutral-400 transition-colors duration-200 shadow-sm hover:shadow-md">
              Get in Touch
            </a>
          </div>
        </div>
      </section>

      <Footer />
    </main>
  );
}
