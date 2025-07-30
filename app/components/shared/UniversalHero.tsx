'use client';

import { motion, useScroll, useTransform, useMotionValue, useSpring } from 'framer-motion';
import { useRef, useState, useEffect } from 'react';
import Button from '../button';

interface HeroButton {
  href: string;
  label: string;
  variant: 'solid' | 'outline';
  color?: 'gradient' | 'black' | 'white' | 'teal';
}

interface UniversalHeroProps {
  theme: 'home' | 'engineer' | 'creator' | 'essence';
  title: string;
  subtitle: string;
  videoSrc: string;
  mobileVideoSrc?: string;
  buttons?: HeroButton[];
  overlayElements?: React.ReactNode;
}

const themeConfig = {
  home: {
    gradientText: 'bg-gradient-to-r from-teal-400 via-rose-400 to-orange-400 bg-clip-text text-transparent',
    overlay: 'bg-gradient-to-b from-black/40 via-black/20 to-black/60',
    particles: 'teal',
    accent: '#2dd4bf'
  },
  engineer: {
    gradientText: 'bg-gradient-to-r from-teal-400 via-teal-300 to-cyan-400 bg-clip-text text-transparent',
    overlay: 'bg-gradient-to-b from-teal-900/30 via-black/20 to-black/60',
    particles: 'teal',
    accent: '#2dd4bf'
  },
  creator: {
    gradientText: 'bg-gradient-to-r from-rose-400 via-pink-400 to-rose-500 bg-clip-text text-transparent',
    overlay: 'bg-gradient-to-b from-rose-900/30 via-black/20 to-black/60',
    particles: 'rose',
    accent: '#fb7185'
  },
  essence: {
    gradientText: 'bg-gradient-to-r from-orange-400 via-amber-400 to-orange-500 bg-clip-text text-transparent',
    overlay: 'bg-gradient-to-b from-orange-900/30 via-black/20 to-black/60',
    particles: 'orange',
    accent: '#fb923c'
  }
};

// Minimal floating particles component
const FloatingParticles = ({ theme, count = 8 }: { theme: keyof typeof themeConfig; count?: number }) => {
  const config = themeConfig[theme];
  const [isClient, setIsClient] = useState(false);
  const [particles, setParticles] = useState<Array<{id: number, initialX: number, initialY: number, animateX: number, animateY: number, duration: number, delay: number, left: number, top: number}>>([]);
  
  useEffect(() => {
    setIsClient(true);
    if (typeof window !== 'undefined') {
      const particleData = Array.from({ length: count }, (_, i) => ({
        id: i,
        initialX: Math.random() * window.innerWidth,
        initialY: Math.random() * window.innerHeight,
        animateX: Math.random() * window.innerWidth,
        animateY: Math.random() * window.innerHeight,
        duration: Math.random() * 20 + 15,
        delay: Math.random() * 5,
        left: Math.random() * 100,
        top: Math.random() * 100
      }));
      setParticles(particleData);
    }
  }, [count]);
  
  if (!isClient) {
    return <div className="absolute inset-0 pointer-events-none overflow-hidden" />;
  }
  
  return (
    <div className="absolute inset-0 pointer-events-none overflow-hidden">
      {particles.map((particle) => (
        <motion.div
          key={particle.id}
          className={`absolute w-1 h-1 rounded-full ${
            config.particles === 'teal' ? 'bg-teal-400/20' :
            config.particles === 'rose' ? 'bg-rose-400/20' :
            'bg-orange-400/20'
          }`}
          initial={{
            x: particle.initialX,
            y: particle.initialY,
            opacity: 0
          }}
          animate={{
            x: particle.animateX,
            y: particle.animateY,
            opacity: [0, 0.6, 0],
          }}
          transition={{
            duration: particle.duration,
            repeat: Infinity,
            ease: "linear",
            delay: particle.delay
          }}
          style={{
            left: `${particle.left}%`,
            top: `${particle.top}%`,
          }}
        />
      ))}
    </div>
  );
};

// Audio waveform component for creator page
const AudioWaveform = () => {
  return (
    <div className="absolute bottom-20 left-1/2 transform -translate-x-1/2 flex items-end space-x-1 opacity-30">
      {Array.from({ length: 12 }).map((_, i) => (
        <motion.div
          key={i}
          className="w-1 bg-rose-400 rounded-full"
          initial={{ height: 4 }}
          animate={{ 
            height: [4, Math.random() * 40 + 8, 4],
          }}
          transition={{
            duration: Math.random() * 1.5 + 0.5,
            repeat: Infinity,
            ease: "easeInOut",
            delay: Math.random() * 0.5
          }}
        />
      ))}
    </div>
  );
};

// Code brackets for engineer page
const CodeElements = () => {
  return (
    <div className="absolute inset-0 pointer-events-none overflow-hidden opacity-10">
      <motion.div
        className="absolute top-1/4 left-1/4 text-teal-400 font-mono text-4xl"
        initial={{ opacity: 0, scale: 0.5 }}
        animate={{ opacity: [0, 0.3, 0], scale: [0.5, 1, 0.5] }}
        transition={{ duration: 8, repeat: Infinity, delay: 2 }}
      >
        {'</>'}
      </motion.div>
      <motion.div
        className="absolute bottom-1/3 right-1/4 text-teal-400 font-mono text-2xl"
        initial={{ opacity: 0, scale: 0.5 }}
        animate={{ opacity: [0, 0.3, 0], scale: [0.5, 1, 0.5] }}
        transition={{ duration: 6, repeat: Infinity, delay: 4 }}
      >
        {'{}'}
      </motion.div>
    </div>
  );
};

// Tennis court lines for essence page
const TennisElements = () => {
  return (
    <div className="absolute inset-0 pointer-events-none overflow-hidden opacity-5">
      <motion.div
        className="absolute top-1/2 left-0 w-full h-px bg-orange-400"
        initial={{ scaleX: 0 }}
        animate={{ scaleX: [0, 1, 0] }}
        transition={{ duration: 12, repeat: Infinity, delay: 1 }}
      />
      <motion.div
        className="absolute top-1/2 left-1/2 w-px h-full bg-orange-400 transform -translate-x-1/2"
        initial={{ scaleY: 0 }}
        animate={{ scaleY: [0, 1, 0] }}
        transition={{ duration: 10, repeat: Infinity, delay: 3 }}
      />
    </div>
  );
};

export default function UniversalHero({ 
  theme, 
  title, 
  subtitle, 
  videoSrc, 
  mobileVideoSrc, 
  buttons = [],
  overlayElements 
}: UniversalHeroProps) {
  const sectionRef = useRef<HTMLElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const mobileVideoRef = useRef<HTMLVideoElement>(null);
  const [isLoaded, setIsLoaded] = useState(false);

  const config = themeConfig[theme];
  const { scrollY } = useScroll();
  const y = useTransform(scrollY, [0, 1200], [0, 600]);
  const opacity = useTransform(scrollY, [50, 800], [1, 0]);
  const scale = useTransform(scrollY, [0, 800], [1, 1.1]);

  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);
  const springX = useSpring(mouseX, { stiffness: 100, damping: 30 });
  const springY = useSpring(mouseY, { stiffness: 100, damping: 30 });

  // Mouse parallax effect
  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!sectionRef.current) return;
      const rect = sectionRef.current.getBoundingClientRect();
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;
      const x = (e.clientX - centerX) / rect.width;
      const y = (e.clientY - centerY) / rect.height;
      mouseX.set(x * 15);
      mouseY.set(y * 15);
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, [mouseX, mouseY]);

  const handleVideoLoad = () => setIsLoaded(true);

  useEffect(() => {
    const timer = setTimeout(() => setIsLoaded(true), 1000);
    return () => clearTimeout(timer);
  }, []);

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { duration: 1.2, staggerChildren: 0.2 }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 60, scale: 0.95 },
    visible: {
      opacity: 1,
      y: 0,
      scale: 1,
      transition: { duration: 0.8 }
    }
  };

  return (
    <motion.section
      ref={sectionRef}
      className="relative z-10 w-full h-[100vh] min-h-[500px] sm:min-h-[600px] overflow-hidden flex items-center justify-center text-center"
      style={{ y, opacity }}
    >
      {/* Video Background */}
      <motion.div
        className="absolute inset-0 z-[0] bg-black overflow-hidden"
        style={{ scale }}
      >
        {/* Desktop Video */}
        <div className="absolute inset-0 w-full h-full hidden sm:block">
          <video
            ref={videoRef}
            autoPlay
            muted
            loop
            playsInline
            preload="metadata"
            src={videoSrc}
            className="w-full h-full object-cover"
            onLoadedData={handleVideoLoad}
            onCanPlay={handleVideoLoad}
            onLoadedMetadata={(e) => {
              const video = e.target as HTMLVideoElement;
              handleVideoLoad();
              video.play().catch(() => console.log('Desktop video autoplay blocked'));
            }}
          />
        </div>

        {/* Mobile Video */}
        {mobileVideoSrc && (
          <div className="absolute inset-0 w-full h-full block sm:hidden">
            <video
              ref={mobileVideoRef}
              autoPlay
              muted
              loop
              playsInline
              preload="metadata"
              src={mobileVideoSrc}
              className="w-full h-full object-cover"
              onLoadedData={handleVideoLoad}
              onCanPlay={handleVideoLoad}
              onLoadedMetadata={(e) => {
                const video = e.target as HTMLVideoElement;
                handleVideoLoad();
                video.play().catch(() => console.log('Mobile video autoplay blocked'));
              }}
            />
          </div>
        )}

        {/* Theme-specific overlay */}
        <div className={`absolute inset-0 ${config.overlay}`} />
      </motion.div>

      {/* Theme-specific background elements */}
      <FloatingParticles theme={theme} count={6} />
      {theme === 'creator' && <AudioWaveform />}
      {theme === 'engineer' && <CodeElements />}
      {theme === 'essence' && <TennisElements />}
      {overlayElements}

      {/* Main Content */}
      <motion.div
        className="relative z-10 max-w-4xl px-4 sm:px-6 lg:px-8"
        variants={containerVariants}
        initial="hidden"
        animate={isLoaded ? "visible" : "hidden"}
        style={{
          x: useTransform(springX, [-20, 20], [-3, 3]),
          y: useTransform(springY, [-20, 20], [-3, 3])
        }}
      >
        {/* Main Headline */}
        <motion.h1
          variants={itemVariants}
          className="text-3xl xs:text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-heading font-bold leading-tight text-white mb-4 sm:mb-6"
        >
          {title.split(' ').map((word, index, array) => {
            const isLastTwoWords = index >= array.length - 2;
            return (
              <span key={index}>
                {isLastTwoWords ? (
                  <motion.span
                    className={`${config.gradientText} inline-block`}
                    whileHover={{ scale: 1.02 }}
                    transition={{ type: "spring", stiffness: 400, damping: 17 }}
                  >
                    {word}
                  </motion.span>
                ) : (
                  word
                )}
                {index < array.length - 1 && ' '}
                {index === array.length - 3 && <br className="hidden sm:block" />}
              </span>
            );
          })}
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          variants={itemVariants}
          className="text-sm sm:text-base md:text-lg lg:text-xl text-neutral-300 mb-8 sm:mb-12 font-body max-w-2xl mx-auto leading-relaxed px-4 sm:px-0"
        >
          {subtitle}
        </motion.p>


      </motion.div>
    </motion.section>
  );
}
