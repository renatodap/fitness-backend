'use client';

import { motion, useScroll, useTransform, useInView } from 'framer-motion';
import { useRef } from 'react';
import Hero from './components/home/HeroSection';

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

      {/* ===== FEATURED SECTIONS ===== */}
      <section className="py-24 lg:py-32 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-white to-orange-25">
        <div className="max-w-6xl mx-auto">
          <CinematicSection className="text-center mb-16">
            <ParallaxText>
              <h2 className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight text-neutral-900 mb-6">
                Recent
                <br />
                <span className="bg-gradient-to-r from-orange-600 via-orange-500 to-orange-400 bg-clip-text text-transparent">
                  Work
                </span>
              </h2>
            </ParallaxText>
          </CinematicSection>

          <div className="space-y-28">
            {SECTIONS.map((section, index) => (
              <CinematicSection key={section.id} delay={index * 0.2}>
                <motion.div
                  className={`flex flex-col lg:flex-row items-center gap-14 ${index % 2 === 1 ? 'lg:flex-row-reverse' : ''}`}
                  initial={{ opacity: 0, x: index % 2 === 0 ? -80 : 80 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  transition={{ duration: 1.4, ease: 'easeOut' }}
                  viewport={{ once: true, margin: '-100px' }}
                >
                  <div className="w-full lg:w-1/2">
                    <FloatingCard index={index}>
                      <div className="relative aspect-video bg-gradient-to-br from-orange-50 to-neutral-50 rounded-3xl overflow-hidden border border-orange-100 shadow-2xl group">
                        {section.image ? (
                          <>
                            <Image
                              src={section.image}
                              alt={section.title}
                              fill
                              sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                              className="object-cover group-hover:scale-105 transition-transform duration-700"
                              priority={index < 2}
                            />
                            <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-60 group-hover:opacity-40 transition-opacity duration-500"></div>
                          </>
                        ) : (
                          <div className="absolute inset-0 flex items-center justify-center">
                            <div className="text-orange-300 text-8xl opacity-30 group-hover:opacity-50 transition-opacity duration-500">🏠</div>
                          </div>
                        )}
                        <div className="absolute top-6 left-6 right-6">
                          <div className="flex items-center justify-between">
                            <span className="bg-orange-100 text-orange-800 px-3 py-1 rounded-full text-xs font-medium">
                              Featured
                            </span>
                            <span className="bg-black/70 text-white px-2 py-1 rounded text-xs font-medium">
                              2024-2025
                            </span>
                          </div>
                        </div>
                        <div className="absolute bottom-6 left-6 right-6">
                          <div className="bg-white/95 backdrop-blur-sm rounded-2xl p-4 border border-white/20 shadow-lg">
                            <div className="flex items-center justify-between">
                              <div>
                                <p className="text-sm font-semibold text-neutral-800">{section.title}</p>
                                <p className="text-xs text-neutral-600">Featured Project</p>
                              </div>
                              <div className="flex gap-2">
                                {section.ctas.map((cta, ctaIndex) => (
                                  <div key={ctaIndex} className="w-8 h-8 bg-neutral-100 rounded-full flex items-center justify-center">
                                    <span className="text-xs">🔗</span>
                                  </div>
                                ))}
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </FloatingCard>
                  </div>
                  
                  <div className="w-full lg:w-1/2 space-y-6">
                    <div className="space-y-4">
                      <h3 className="text-3xl font-bold text-neutral-900">{section.title}</h3>
                      <div className="text-neutral-600 leading-relaxed text-lg">{section.description}</div>
                    </div>
                    
                    <div className="flex flex-wrap gap-3">
                      {section.ctas.map((cta, ctaIndex) => (
                        <a
                          key={ctaIndex}
                          href={cta.href}
                          className={`px-6 py-3 rounded-2xl font-medium transition-all duration-300 ${
                            cta.variant === 'solid'
                              ? 'bg-orange-600 text-white hover:bg-orange-700 hover:shadow-lg'
                              : 'border-2 border-orange-300 text-orange-700 hover:border-orange-600 hover:text-orange-800'
                          }`}
                        >
                          {cta.label}
                        </a>
                      ))}
                    </div>
                  </div>
                </motion.div>
              </CinematicSection>
            ))}
          </div>
        </div>
      </section>

      {/* ===== FINALE: THE INVITATION ===== */}
      <section className="py-24 lg:py-32 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-orange-25 to-orange-50 text-center">
        <div className="max-w-3xl mx-auto">
          <CinematicSection>
            <ParallaxText>
              <h2 className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight text-neutral-900 mb-6">
                Let's
                <br />
                <span className="bg-gradient-to-r from-orange-600 via-orange-500 to-orange-400 bg-clip-text text-transparent">
                  Connect
                </span>
              </h2>
            </ParallaxText>
            <p className="text-base sm:text-lg text-neutral-600 leading-relaxed max-w-2xl mx-auto mb-8">
              Interested in collaborating, discussing ideas, or just saying hello? I'd love to hear from you.
            </p>
            
            <div className="flex flex-row justify-center items-center gap-5 mb-8">
              <motion.a 
                href="https://linkedin.com/in/renatodap" 
                target="_blank" 
                rel="noopener noreferrer" 
                aria-label="LinkedIn" 
                className="group"
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.95 }}
              >
                <svg className="w-6 h-6 text-neutral-600 group-hover:text-orange-600 transition-colors duration-200" fill="currentColor" viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.761 0 5-2.239 5-5v-14c0-2.761-2.239-5-5-5zm-11 19h-3v-10h3v10zm-1.5-11.268c-.966 0-1.75-.784-1.75-1.75s.784-1.75 1.75-1.75 1.75.784 1.75 1.75-.784 1.75-1.75 1.75zm13.5 11.268h-3v-5.604c0-1.337-.025-3.063-1.868-3.063-1.869 0-2.156 1.459-2.156 2.967v5.7h-3v-10h2.881v1.367h.041c.401-.761 1.381-1.563 2.841-1.563 3.041 0 3.602 2.002 3.602 4.604v5.592z" /></svg>
              </motion.a>
              <motion.a 
                href="https://open.spotify.com/artist/3VZ8V9XhQ9oZb5XnZ9g8yB" 
                target="_blank" 
                rel="noopener noreferrer" 
                aria-label="Spotify" 
                className="group"
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.95 }}
              >
                <svg className="w-6 h-6 text-neutral-600 group-hover:text-orange-600 transition-colors duration-200" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0C5.371 0 0 5.371 0 12s5.371 12 12 12 12-5.371 12-12S18.629 0 12 0zm5.363 17.463c-.221.364-.691.482-1.055.262-2.891-1.764-6.543-2.16-10.824-1.18-.418.096-.844-.162-.94-.576-.096-.418.162-.844.576-.94 4.663-1.08 8.727-.641 11.947 1.262.364.22.482.69.262 1.055zm1.504-2.67c-.276.447-.854.59-1.301.314-3.309-2.04-8.362-2.635-12.284-1.44-.51.158-1.055-.117-1.213-.627-.158-.51.117-1.055.627-1.213 4.406-1.361 9.927-.709 13.722 1.578.447.276.59.854.314 1.301zm.146-2.835C15.06 9.684 8.924 9.5 5.934 10.384c-.623.182-1.283-.159-1.464-.783-.181-.624.159-1.283.783-1.464 3.417-.99 10.184-.785 14.047 2.016.527.389.642 1.135.254 1.662-.389.527-1.135.643-1.662.254z" /></svg>
              </motion.a>
              <motion.a 
                href="https://www.youtube.com/@RenatoDAP" 
                target="_blank" 
                rel="noopener noreferrer" 
                aria-label="YouTube" 
                className="group"
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.95 }}
              >
                <svg className="w-6 h-6 text-neutral-600 group-hover:text-orange-600 transition-colors duration-200" fill="currentColor" viewBox="0 0 24 24"><path d="M23.498 6.186a2.994 2.994 0 0 0-2.112-2.117C19.257 3.5 12 3.5 12 3.5s-7.257 0-9.386.569A2.994 2.994 0 0 0 .502 6.186C0 8.313 0 12 0 12s0 3.687.502 5.814a2.994 2.994 0 0 0 2.112 2.117C4.743 20.5 12 20.5 12 20.5s7.257 0 9.386-.569a2.994 2.994 0 0 0 2.112-2.117C24 15.687 24 12 24 12s0-3.687-.502-5.814zM9.75 15.5v-7l6.5 3.5-6.5 3.5z" /></svg>
              </motion.a>
            </div>
            
            <div className="flex justify-center">
              <motion.a 
                href="mailto:renatodaprado@gmail.com" 
                className="inline-flex items-center justify-center px-8 py-4 border border-orange-300 text-sm font-semibold rounded-xl text-neutral-900 bg-white hover:bg-orange-50 hover:border-orange-400 transition-all duration-300 shadow-lg hover:shadow-xl"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <span className="mr-2"></span>
                Get in Touch
              </motion.a>
            </div>
          </CinematicSection>
        </div>
      </section>


    </main>
  );
}
