'use client';

import { motion, useScroll, useTransform, useMotionValue, useSpring } from 'framer-motion';
import { useRef, useState, useEffect } from 'react';
import Button from '../button';

export default function HeroSection() {
  const sectionRef = useRef<HTMLElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const mobileVideoRef = useRef<HTMLVideoElement>(null);
  const [isLoaded, setIsLoaded] = useState(true); // Start as loaded to avoid infinite loading
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  
  const { scrollY } = useScroll();
  const y = useTransform(scrollY, [0, 800], [0, 400]);
  const opacity = useTransform(scrollY, [0, 400], [1, 0]);
  const scale = useTransform(scrollY, [0, 400], [1, 1.1]);
  
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
      
      setMousePosition({ x, y });
      mouseX.set(x * 20);
      mouseY.set(y * 20);
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, [mouseX, mouseY]);

  // Enhanced video loading
  const handleVideoLoad = () => {
    setIsLoaded(true);
  };

  // Ensure loading state is set to true after component mounts
  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoaded(true);
    }, 1000);
    return () => clearTimeout(timer);
  }, []);

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        duration: 1.2,
        staggerChildren: 0.2
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 60, scale: 0.95 },
    visible: {
      opacity: 1,
      y: 0,
      scale: 1,
      transition: {
        duration: 0.8
      }
    }
  };

  return (
    <motion.section 
      ref={sectionRef}
      className="relative w-full h-[100vh] min-h-[600px] overflow-hidden flex items-center justify-center text-center"
      style={{ y, opacity }}
    >
      {/* Enhanced Video Background */}
      <motion.div 
        className="absolute inset-0 z-[-3]"
        style={{ scale }}
      >
        {/* Desktop Video */}
        <video
          ref={videoRef}
          autoPlay
          muted
          loop
          playsInline
          preload="metadata"
          src="/hero-video2.mp4"
          className="absolute inset-0 w-full h-full object-cover hidden sm:block hero-zoom"
          poster="/fallback-image.png"
          onLoadedData={handleVideoLoad}
          onCanPlay={handleVideoLoad}
          onLoadedMetadata={(e) => {
            const video = e.target as HTMLVideoElement;
            handleVideoLoad();
            video.play().catch(() => console.log('Desktop video autoplay blocked'));
          }}
        />
        
        {/* Mobile Video */}
        <video
          ref={mobileVideoRef}
          autoPlay
          muted
          loop
          playsInline
          preload="metadata"
          src="/hero-video-square2.mp4"
          className="absolute inset-0 w-full h-full object-cover sm:hidden hero-zoom"
          poster="/fallback-image-mobile.png"
          onLoadedData={handleVideoLoad}
          onCanPlay={handleVideoLoad}
          onLoadedMetadata={(e) => {
            const video = e.target as HTMLVideoElement;
            handleVideoLoad();
            video.play().catch(() => console.log('Mobile video autoplay blocked'));
          }}
        />
      </motion.div>

      {/* Dynamic Gradient Overlays */}
      <div className="absolute inset-0 z-[-2]">
        {/* Primary gradient */}
        <div className="absolute inset-0 bg-gradient-to-b from-black/70 via-black/30 to-black/70" />
        
        {/* Animated gradient accent */}
        <motion.div 
          className="absolute inset-0 bg-gradient-to-br from-teal-500/20 via-transparent to-rose-500/20"
          animate={{
            background: [
              'linear-gradient(to bottom right, rgba(20, 184, 166, 0.2), transparent, rgba(251, 113, 133, 0.2))',
              'linear-gradient(to bottom right, rgba(251, 113, 133, 0.2), transparent, rgba(251, 146, 60, 0.2))',
              'linear-gradient(to bottom right, rgba(251, 146, 60, 0.2), transparent, rgba(20, 184, 166, 0.2))'
            ]
          }}
          transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
        />
        
        {/* Vignette effect */}
        <div className="absolute inset-0 bg-radial-gradient from-transparent via-transparent to-black/40" />
      </div>

      {/* Floating Elements */}
      <motion.div 
        className="absolute top-1/4 left-1/4 w-2 h-2 bg-white/30 rounded-full blur-sm floating"
        style={{ x: springX, y: springY }}
      />
      <motion.div 
        className="absolute top-1/3 right-1/3 w-1 h-1 bg-teal-400/50 rounded-full blur-sm floating-slow"
        style={{ x: springX, y: springY }}
      />
      <motion.div 
        className="absolute bottom-1/3 left-1/3 w-1.5 h-1.5 bg-rose-400/40 rounded-full blur-sm floating"
        style={{ x: springX, y: springY }}
      />

      {/* Main Content */}
      <motion.div 
        className="relative z-10 max-w-4xl px-6 sm:px-8"
        variants={containerVariants}
        initial="hidden"
        animate={isLoaded ? "visible" : "hidden"}
        style={{
          x: useTransform(mouseX, [-1, 1], [-10, 10]),
          y: useTransform(mouseY, [-1, 1], [-10, 10])
        }}
      >
        {/* Main Headline */}
        <motion.h1
          variants={itemVariants}
          className="text-5xl sm:text-6xl lg:text-7xl font-heading font-bold leading-[0.9] tracking-tight text-white mb-6"
        >
          I build tools{' '}
          <br className="hidden sm:block" />
          <motion.span 
            className="gradient-text inline-block"
            whileHover={{ scale: 1.05 }}
            transition={{ type: "spring", stiffness: 400, damping: 17 }}
          >
            with rhythm and logic.
          </motion.span>
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          variants={itemVariants}
          className="text-xl sm:text-2xl text-neutral-200 mb-12 font-body max-w-2xl mx-auto leading-relaxed"
        >
          I'm{' '}
          <motion.span 
            className="text-white font-semibold"
            whileHover={{ color: "#2dd4bf" }}
            transition={{ duration: 0.2 }}
          >
            Renato DAP
          </motion.span>
          {' '}— I work at the intersection of creative energy and technical depth.
        </motion.p>

        {/* CTA Buttons */}
        <motion.div
          variants={itemVariants}
          className="flex flex-col sm:flex-row gap-6 justify-center items-center"
        >
          <Button 
            href="/software" 
            variant="solid" 
            color="gradient" 
            size="lg"
            shimmer={true}
          >
            View Projects
          </Button>
          <Button 
            href="/photo" 
            variant="outline" 
            color="white" 
            size="lg"
          >
            Watch Performances
          </Button>
        </motion.div>

        {/* Scroll Indicator */}
        <motion.div
          variants={itemVariants}
          className="absolute bottom-8 left-1/2 transform -translate-x-1/2"
        >
          <motion.div
            animate={{ y: [0, 10, 0] }}
            transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
            className="flex flex-col items-center text-white/60 hover:text-white/80 transition-colors cursor-pointer"
            onClick={() => window.scrollTo({ top: window.innerHeight, behavior: 'smooth' })}
          >
            <span className="text-sm font-medium mb-2">Scroll to explore</span>
            <div className="w-6 h-10 border-2 border-white/40 rounded-full flex justify-center">
              <motion.div
                animate={{ y: [0, 12, 0] }}
                transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
                className="w-1 h-3 bg-white/60 rounded-full mt-2"
              />
            </div>
          </motion.div>
        </motion.div>
      </motion.div>

      {/* Loading State */}
      {!isLoaded && (
        <motion.div
          className="absolute inset-0 bg-neutral-900 flex items-center justify-center z-20"
          exit={{ opacity: 0 }}
          transition={{ duration: 0.5 }}
        >
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
            className="w-8 h-8 border-2 border-teal-500 border-t-transparent rounded-full"
          />
        </motion.div>
      )}
    </motion.section>
  );
}
