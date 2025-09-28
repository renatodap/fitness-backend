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
    title: 'AllAboutFood - Voice-Controlled Culinary AI Assistant',
    description: (
      <div className="space-y-3">
        <p className="text-lg font-medium text-neutral-800">
          Senior Capstone Project (Sep 2025 - May 2026) • Full-Stack Lead Developer
        </p>
        <p>
          Leading development of a <span className="font-semibold text-orange-600">hands-free culinary platform</span> that processes recipes from
          any format (Word, PDF, images, URLs) using GPT-4 Vision & OCR. Achieved <span className="font-semibold">95% extraction accuracy</span>
          while reducing cloud costs by 20x through strategic optimization.
        </p>
        <div className="flex flex-wrap gap-2 pt-2">
          <span className="bg-orange-100 text-orange-800 px-3 py-1 rounded-full text-xs font-semibold">React/Next.js</span>
          <span className="bg-orange-100 text-orange-800 px-3 py-1 rounded-full text-xs font-semibold">GPT-4 Vision API</span>
          <span className="bg-orange-100 text-orange-800 px-3 py-1 rounded-full text-xs font-semibold">Voice Interfaces</span>
          <span className="bg-orange-100 text-orange-800 px-3 py-1 rounded-full text-xs font-semibold">Stripe Payments</span>
          <span className="bg-orange-100 text-orange-800 px-3 py-1 rounded-full text-xs font-semibold">PostgreSQL</span>
        </div>
        <div className="mt-3 p-3 bg-gradient-to-r from-orange-50 to-amber-50 rounded-lg border-l-4 border-orange-500">
          <p className="text-sm">
            <span className="font-bold text-green-700">💰 Infrastructure:</span> $1,000 → $50/month (20x reduction) •
            <span className="font-bold text-blue-700"> 🎯 Impact:</span> 500-1000 concurrent users • 3-sec voice response
          </p>
        </div>
      </div>
    ),
    ctas: [
      { href: 'https://allaboutfood.cafe', label: '🌐 Live Platform', variant: 'solid' },
      { href: 'https://github.com/renatodap/allaboutfood', label: 'View Code', variant: 'outline' },
    ],
    image: 'phone-mockup', // Special case for custom component
    align: 'left',
    bgClass: 'bg-white border-b border-neutral-100',
  },
  {
    id: 'liteclient',
    title: 'KYA (Know Your Agent) - Blockchain Identity for AI',
    description: (
      <div className="space-y-3">
        <p className="text-lg font-medium text-neutral-800">
          Blockchain Engineering Internship (Jun - Aug 2025) • DeFi Devs / Genialt.ai
        </p>
        <p>
          Designed and built <span className="font-semibold text-orange-600">cryptographic identity system for AI agents</span> enabling
          verifiable provenance on-chain. Implemented <span className="font-semibold">8,000+ lines of production Go</span> creating
          a lightweight client that gives any AI its own blockchain-backed identity.
        </p>
        <div className="flex flex-wrap gap-2 pt-2">
          <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-xs font-semibold">Go (Golang)</span>
          <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-xs font-semibold">Merkle Trees</span>
          <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-xs font-semibold">AI Supply Chain</span>
          <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-xs font-semibold">Edge Computing</span>
          <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-xs font-semibold">Cryptography</span>
        </div>
        <div className="mt-3 p-3 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border-l-4 border-blue-500">
          <p className="text-sm">
            <span className="font-bold text-purple-700">🔐 Innovation:</span> Human-readable ADIs (adi://genialt/trading-bot/v3.1) •
            <span className="font-bold text-indigo-700"> ⚡ Impact:</span> Immutable audit trails for debugging & forensics
          </p>
        </div>
      </div>
    ),
    ctas: [
      { href: 'https://www.youtube.com/watch?v=mcVZXHcuO70', label: '🎥 Watch Demo', variant: 'solid' },
      { href: 'https://github.com/renatodap/accumulate-liteclient', label: 'View Code', variant: 'outline' },
    ],
    image: 'youtube-embed', // Special case for YouTube video
    align: 'right',
    bgClass: 'bg-neutral-25 border-b border-neutral-100',
  },
  {
    id: 'fitness',
    title: 'Wagner Coach - AI Personal Fitness Platform',
    description: (
      <div className="space-y-3">
        <p className="text-lg font-medium text-neutral-800">
          In Development • RAG-Powered Fitness Assistant
        </p>
        <p>
          Building a <span className="font-semibold text-orange-600">Retrieval-Augmented Generation (RAG) system</span> that provides
          personalized AI coaching based on user's complete fitness history. Natural language input enables
          quick unified tracking of workouts, nutrition, and progress metrics.
        </p>
        <div className="flex flex-wrap gap-2 pt-2">
          <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-xs font-semibold">LangChain</span>
          <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-xs font-semibold">Vector Databases</span>
          <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-xs font-semibold">NLP Processing</span>
          <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-xs font-semibold">React Native</span>
          <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-xs font-semibold">Supabase</span>
        </div>
        <div className="mt-3 p-3 bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg border-l-4 border-green-500">
          <p className="text-sm">
            <span className="font-bold text-green-700">🤖 AI Features:</span> Context-aware coaching from historical data •
            <span className="font-bold text-emerald-700"> 📊 Smart Tracking:</span> Natural language workout logging
          </p>
        </div>
      </div>
    ),
    ctas: [
      { href: 'https://github.com/renatodap/wagner-coach', label: 'View Project', variant: 'solid' },
      { href: 'https://wagner-coach.vercel.app', label: 'Live Demo', variant: 'outline' },
    ],
    image: '/wagner-icon.svg',
    align: 'left',
    bgClass: 'bg-white border-b border-neutral-100',
  },
  {
    id: 'recycling',
    title: 'Terre Haute AI Recycling Assistant',
    description: (
      <div className="space-y-3">
        <p className="text-lg font-medium text-neutral-800">
          Civic Tech Initiative • Computer Vision for Sustainability
        </p>
        <p>
          Developing a <span className="font-semibold text-orange-600">computer vision PWA</span> that identifies waste items and provides
          disposal instructions. Achieving <span className="font-semibold">85-90% accuracy</span> across 30+ waste categories
          using multi-label classification and transfer learning techniques.
        </p>
        <div className="flex flex-wrap gap-2 pt-2">
          <span className="bg-teal-100 text-teal-800 px-3 py-1 rounded-full text-xs font-semibold">TensorFlow</span>
          <span className="bg-teal-100 text-teal-800 px-3 py-1 rounded-full text-xs font-semibold">Computer Vision</span>
          <span className="bg-teal-100 text-teal-800 px-3 py-1 rounded-full text-xs font-semibold">PWA</span>
          <span className="bg-teal-100 text-teal-800 px-3 py-1 rounded-full text-xs font-semibold">MobileNet</span>
          <span className="bg-teal-100 text-teal-800 px-3 py-1 rounded-full text-xs font-semibold">React</span>
        </div>
        <div className="mt-3 p-3 bg-gradient-to-r from-teal-50 to-cyan-50 rounded-lg border-l-4 border-teal-500">
          <p className="text-sm">
            <span className="font-bold text-teal-700">♻️ Environmental Impact:</span> Reducing contamination in recycling streams •
            <span className="font-bold text-cyan-700"> 📱 Accessibility:</span> Works offline on any mobile device
          </p>
        </div>
      </div>
    ),
    ctas: [
      { href: 'https://github.com/renatodap/recycling-th', label: 'View Code', variant: 'solid' },
      { href: 'https://recycling-th.vercel.app', label: 'Try App', variant: 'outline' },
    ],
    image: '/recycling-icon.png',
    align: 'right',
    bgClass: 'bg-neutral-25 border-b border-neutral-100',
  },
  {
    id: 'ai',
    title: 'Deep Learning & AI Research',
    description: (
      <div className="space-y-3">
        <p className="text-lg font-medium text-neutral-800">
          Rose-Hulman Institute of Technology • Computer Science • GPA: 3.58
        </p>
        <p>
          Currently enrolled in <span className="font-semibold text-orange-600">advanced AI and deep learning courses</span>, building
          expertise in neural network architectures, optimization algorithms, and practical ML deployment.
          Graduation: May 2026.
        </p>
        <div className="flex flex-wrap gap-2 pt-2">
          <span className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-xs font-semibold">PyTorch</span>
          <span className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-xs font-semibold">CNNs</span>
          <span className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-xs font-semibold">Transfer Learning</span>
          <span className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-xs font-semibold">Backpropagation</span>
          <span className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-xs font-semibold">Transformers</span>
        </div>
        <div className="mt-3 p-3 bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg border-l-4 border-purple-500">
          <p className="text-sm">
            <span className="font-bold text-purple-700">📚 Coursework:</span> CSSE 313 (AI) & CSSE/MA 416 (Deep Learning) •
            <span className="font-bold text-pink-700"> 🎓 TA Experience:</span> Object-Oriented Software Development
          </p>
        </div>
        <p className="text-xs text-neutral-500 italic mt-2">
          Suggested image: Neural network visualization with interconnected nodes, gradient colors from purple to orange
        </p>
      </div>
    ),
    ctas: [
      { href: 'https://linkedin.com/in/renatodap', label: 'LinkedIn', variant: 'solid' },
      { href: 'https://github.com/renatodap', label: 'GitHub', variant: 'outline' },
    ],
    image: 'ai-visualization', // Placeholder for AI-generated image
    align: 'center',
    bgClass: 'bg-white',
  },
];

export default function HomePage() {
  return (
    <main className="relative w-full bg-white text-black overflow-x-hidden">

      {/* ===== HERO VIDEO SECTION ===== */}
      <Hero />

      {/* ===== FEATURED SECTIONS ===== */}
      <section className="py-24 lg:py-32 px-4 sm:px-6 lg:px-8">
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
                      {section.image === 'phone-mockup' ? (
                        // Phone mockup for AllAboutFood
                        <div className="relative flex justify-center items-center py-8">
                          <div className="relative w-[280px] h-[580px] bg-black rounded-[40px] p-2 shadow-2xl">
                            <div className="w-full h-full bg-white rounded-[32px] overflow-hidden">
                              <div className="h-14 bg-gradient-to-r from-orange-500 to-orange-600 flex items-center px-4">
                                <span className="text-white font-bold text-lg">AllAboutFood</span>
                                <span className="ml-auto text-white/80 text-xs">AI Assistant</span>
                              </div>
                              <div className="p-4 space-y-4">
                                <div className="bg-orange-50 rounded-2xl p-3">
                                  <p className="text-xs text-orange-800 font-medium mb-1">🎤 Voice Command</p>
                                  <p className="text-sm">"Hey Alexa, start cooking lasagna"</p>
                                </div>
                                <div className="bg-gray-50 rounded-2xl p-3">
                                  <p className="text-xs text-gray-600 font-medium mb-1">📋 Recipe Loaded</p>
                                  <p className="text-sm">Classic Lasagna - 45 mins</p>
                                </div>
                                <div className="bg-blue-50 rounded-2xl p-3">
                                  <p className="text-xs text-blue-800 font-medium mb-1">👨‍🍳 Current Step</p>
                                  <p className="text-sm">Layer noodles, then meat sauce...</p>
                                </div>
                                <div className="flex gap-2 mt-4">
                                  <div className="flex-1 bg-green-100 rounded-xl p-2 text-center">
                                    <span className="text-xs">Next Step →</span>
                                  </div>
                                  <div className="flex-1 bg-yellow-100 rounded-xl p-2 text-center">
                                    <span className="text-xs">← Previous</span>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      ) : section.image === 'youtube-embed' ? (
                        // YouTube embed for Accumulate/KYA
                        <div className="relative aspect-video bg-black rounded-3xl overflow-hidden shadow-2xl">
                          <iframe
                            src="https://www.youtube.com/embed/mcVZXHcuO70"
                            title="KYA Framework Demo"
                            className="w-full h-full"
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                            allowFullScreen
                          />
                        </div>
                      ) : section.image === 'ai-visualization' ? (
                        // AI visualization placeholder
                        <div className="relative aspect-video bg-gradient-to-br from-purple-600 via-pink-500 to-orange-400 rounded-3xl overflow-hidden shadow-2xl">
                          <div className="absolute inset-0 flex items-center justify-center">
                            <div className="text-center text-white">
                              <div className="text-6xl mb-4">🧠</div>
                              <p className="text-xl font-bold">Neural Networks</p>
                              <p className="text-sm opacity-80">Deep Learning Research</p>
                            </div>
                          </div>
                          <div className="absolute inset-0 bg-black/20"></div>
                        </div>
                      ) : section.image && !['phone-mockup', 'youtube-embed', 'ai-visualization'].includes(section.image) ? (
                        // Regular image display
                        <div className="relative aspect-video bg-gradient-to-br from-orange-50 to-neutral-50 rounded-3xl overflow-hidden border border-orange-100 shadow-2xl group">
                          <Image
                            src={section.image}
                            alt={section.title}
                            fill
                            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                            className="object-cover group-hover:scale-105 transition-transform duration-700"
                            priority={index < 2}
                          />
                          <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-60 group-hover:opacity-40 transition-opacity duration-500"></div>
                          <div className="absolute top-6 left-6 right-6">
                            <div className="flex items-center justify-between">
                              <span className="bg-orange-100 text-orange-800 px-3 py-1 rounded-full text-xs font-medium">
                                Featured
                              </span>
                              <span className="bg-black/70 text-white px-2 py-1 rounded text-xs font-medium">
                                2025-2026
                              </span>
                            </div>
                          </div>
                        </div>
                      ) : (
                        // Fallback for no image
                        <div className="relative aspect-video bg-gradient-to-br from-orange-50 to-neutral-50 rounded-3xl overflow-hidden border border-orange-100 shadow-2xl group">
                          <div className="absolute inset-0 flex items-center justify-center">
                            <div className="text-orange-300 text-8xl opacity-30 group-hover:opacity-50 transition-opacity duration-500">🚀</div>
                          </div>
                        </div>
                      )}
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
