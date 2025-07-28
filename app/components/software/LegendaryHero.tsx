// app/components/software/LegendaryHero.tsx

'use client';

import { motion, useScroll, useTransform } from 'framer-motion';
import { useRef, useEffect, useState } from 'react';


export function LegendaryHero() {
  const ref = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start start", "end start"]
  });

  const y = useTransform(scrollYProgress, [0, 1], [0, -200]);
  const opacity = useTransform(scrollYProgress, [0, 0.8], [1, 0]);
  const scale = useTransform(scrollYProgress, [0, 1], [1, 0.8]);

  const [currentPhase, setCurrentPhase] = useState(0);

  useEffect(() => {
    const timer = setTimeout(() => {
      if (currentPhase < 3) {
        setCurrentPhase(currentPhase + 1);
      }
    }, 2000);
    return () => clearTimeout(timer);
  }, [currentPhase]);





  const phases = [
    "I build systems that matter.",
    "I solve problems that scale.",
    "I create software that thinks.",
    "This is my story."
  ];

  return (
    <motion.section
      ref={ref}
      style={{ y, opacity, scale }}
      className="relative min-h-screen flex items-center justify-center overflow-hidden"
    >


      {/* Video Background */}
      <div className="absolute inset-0 z-[0] bg-black overflow-hidden">
        <video
          autoPlay
          muted
          loop
          playsInline
          preload="metadata"
          src="/software.mp4"
          className="w-full h-full object-cover"
          onLoadedMetadata={(e) => {
            const video = e.target as HTMLVideoElement;
            video.play().catch(() => console.log('Video autoplay blocked'));
          }}
        />
      </div>
      


      <div className="relative z-10 text-center space-y-16 px-6 sm:px-10 max-w-5xl mx-auto">
        {/* Main title */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.3, ease: [0.22, 1, 0.36, 1] }}
          className="space-y-6"
        >
          <h1 className="text-6xl sm:text-8xl font-heading font-black text-white leading-none tracking-tighter">
            SOFTWARE
          </h1>
          <h2 className="text-6xl sm:text-8xl font-heading font-black bg-gradient-to-r from-teal-400 via-rose-400 to-orange-400 bg-clip-text text-transparent leading-none tracking-tighter">
            THAT THINKS
          </h2>
        </motion.div>

        {/* Clean subtitle */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6, ease: [0.22, 1, 0.36, 1] }}
        >
          <p className="text-2xl sm:text-3xl text-white/80 font-body font-light leading-relaxed">
            Building intelligent systems that solve real problems
          </p>
        </motion.div>

        {/* What I'm Building Now - Clean Version */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.9, ease: [0.22, 1, 0.36, 1] }}
          className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 sm:p-10 text-left max-w-3xl mx-auto"
        >
          <div className="space-y-6">
            <div className="flex items-center space-x-3">
              <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
              <h3 className="text-xl font-heading font-semibold text-white">
                Currently Building
              </h3>
            </div>
            <p className="text-lg text-white/90 leading-relaxed font-light">
              <span className="text-teal-400 font-medium">Accumulate Lite Client</span> — 
              A next-generation blockchain protocol enabling instant, secure transactions 
              with zero-knowledge proofs.
            </p>
            <div className="flex flex-wrap gap-2">
              <span className="px-3 py-1 bg-white/10 text-white/70 rounded-full text-sm">
                Blockchain
              </span>
              <span className="px-3 py-1 bg-white/10 text-white/70 rounded-full text-sm">
                Zero-Knowledge
              </span>
              <span className="px-3 py-1 bg-white/10 text-white/70 rounded-full text-sm">
                Go
              </span>
            </div>
          </div>
        </motion.div>
      </div>
    </motion.section>
  );
}
