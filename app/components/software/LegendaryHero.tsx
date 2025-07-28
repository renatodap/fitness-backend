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
      
      {/* Floating particles */}
      <div className="absolute inset-0 z-[1]">
        
        {/* Floating particles */}
        {[...Array(20)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-1 h-1 bg-teal-400/40 rounded-full"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
            animate={{
              y: [0, -100, 0],
              opacity: [0, 1, 0],
            }}
            transition={{
              duration: 3 + Math.random() * 2,
              repeat: Infinity,
              delay: Math.random() * 2,
            }}
          />
        ))}
      </div>

      <div className="relative z-10 text-center space-y-12 px-6 sm:px-10 max-w-4xl mx-auto">
        {/* Main title with staggered reveal */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1, delay: 0.5 }}
          className="space-y-4"
        >
          <motion.h1
            className="text-6xl sm:text-8xl font-heading font-black text-white leading-none tracking-tighter"
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1, delay: 1 }}
          >
            SOFTWARE
          </motion.h1>
          <motion.h1
            className="text-6xl sm:text-8xl font-heading font-black bg-gradient-to-r from-teal-400 via-rose-400 to-orange-400 bg-clip-text text-transparent leading-none tracking-tighter"
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1, delay: 1.3 }}
          >
            THAT THINKS
          </motion.h1>
        </motion.div>

        {/* Dynamic subtitle that changes */}
        <motion.div
          className="h-16 flex items-center justify-center"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1, delay: 2 }}
        >
          <motion.p
            key={currentPhase}
            className="text-xl sm:text-2xl text-white font-body"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.8 }}
          >
            {phases[currentPhase]}
          </motion.p>
        </motion.div>

        {/* What I'm Building Now - Reimagined */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1, delay: 3 }}
          className="relative"
        >
          <div className="absolute inset-0 bg-gradient-to-r from-teal-200/30 to-rose-200/30 rounded-2xl blur-xl" />
          <div className="relative bg-white border border-neutral-200 rounded-2xl p-8 shadow-lg">
            <motion.div
              className="flex items-center space-x-3 mb-4"
              animate={{ opacity: [0.5, 1, 0.5] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse" />
              <h2 className="text-lg font-heading font-bold text-black">CURRENTLY BUILDING</h2>
            </motion.div>
            <p className="text-neutral-700 font-body leading-relaxed">
              Deep-diving into AST-based tooling to build a linter that enforces SOLID principles. 
              Also architecting an AI-enabled system design guide that will revolutionize how students learn software architecture.
            </p>
          </div>
        </motion.div>


      </div>
    </motion.section>
  );
}
