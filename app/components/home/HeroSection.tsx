'use client';

import { motion } from 'framer-motion';
import Button from '../button';

export default function HeroSection() {
  return (
    <section className="relative w-full h-[420px] sm:h-[480px] md:h-[540px] lg:h-[600px] overflow-hidden flex items-center justify-center text-center">
      {/* Desktop Video */}
      <video
        autoPlay
        muted
        loop
        playsInline
        src="/hero-video.mp4"
        className="absolute inset-0 w-full h-full object-cover hidden sm:block z-[-2]"
        poster="/fallback-image.png"
      />
      {/* Mobile Video */}
      <video
        autoPlay
        muted
        loop
        playsInline
        preload="auto"
        src="/hero-video-square.mp4"
        className="absolute inset-0 w-full h-full object-cover sm:hidden z-[-2]"
        poster="/fallback-image-mobile.png"
        onLoadedMetadata={(e) => {
          // Force play on mobile after metadata loads
          const video = e.target as HTMLVideoElement;
          video.play().catch(() => {
            // Fallback if autoplay fails
            console.log('Autoplay blocked, user interaction required');
          });
        }}
      />

      {/* Gradient Overlay */}
      <div className="absolute inset-0 bg-gradient-to-b from-black/60 via-black/40 to-black/60 z-[-1]" />

      {/* Content */}
      <div className="z-10 max-w-2xl px-6">
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, ease: 'easeOut' }}
          className="text-4xl sm:text-5xl font-extrabold leading-tight tracking-tight text-white mb-4"
        >
          I build tools <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-rose-400 to-orange-400">
            with rhythm and logic.
          </span>
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: 'easeOut', delay: 0.2 }}
          className="text-lg text-neutral-200 mb-8"
        >
          I’m Renato DAP — I work at the intersection of creative energy and technical depth.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, ease: 'easeOut', delay: 0.4 }}
          className="flex flex-col sm:flex-row gap-4 justify-center"
        >
          <Button href="/software" variant="solid" color="white">
            View Projects
          </Button>
          <Button href="/photo" variant="solid" color="white">
            Watch Performances
          </Button>
        </motion.div>
      </div>
    </section>
  );
}
