// app/components/software/HolographicText.tsx

'use client';

import { motion, useMotionValue, useTransform, useSpring } from 'framer-motion';
import { useEffect, useRef } from 'react';

interface HolographicTextProps {
  text: string;
  className?: string;
}

export function HolographicText({ text, className }: HolographicTextProps) {
  const ref = useRef<HTMLDivElement>(null);
  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);

  const rotateX = useSpring(useTransform(mouseY, [-300, 300], [15, -15]), {
    stiffness: 100,
    damping: 30
  });
  const rotateY = useSpring(useTransform(mouseX, [-300, 300], [-15, 15]), {
    stiffness: 100,
    damping: 30
  });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!ref.current) return;
      
      const rect = ref.current.getBoundingClientRect();
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;
      
      mouseX.set(e.clientX - centerX);
      mouseY.set(e.clientY - centerY);
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, [mouseX, mouseY]);

  return (
    <motion.div
      ref={ref}
      className={`relative inline-block ${className}`}
      style={{
        perspective: '1000px',
        transformStyle: 'preserve-3d',
      }}
    >
      {/* Main holographic text */}
      <motion.div
        className="relative"
        style={{
          rotateX,
          rotateY,
          transformStyle: 'preserve-3d',
        }}
      >
        {/* Base text */}
        <div className="relative z-10">
          {text}
        </div>
        
        {/* Holographic layers */}
        {[...Array(5)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute top-0 left-0 opacity-20"
            style={{
              transform: `translateZ(${-2 * (i + 1)}px)`,
              color: i % 2 === 0 ? '#00ffff' : '#ff00ff',
              filter: `blur(${i * 0.5}px)`,
            }}
            animate={{
              opacity: [0.1, 0.3, 0.1],
            }}
            transition={{
              duration: 2 + i * 0.5,
              repeat: Infinity,
              delay: i * 0.2,
            }}
          >
            {text}
          </motion.div>
        ))}
        
        {/* Scanning line effect */}
        <motion.div
          className="absolute inset-0 pointer-events-none"
          style={{
            background: 'linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.3), transparent)',
            transform: 'skewX(-20deg)',
          }}
          animate={{
            x: ['-100%', '200%'],
          }}
          transition={{
            duration: 3,
            repeat: Infinity,
            repeatDelay: 2,
          }}
        />
        
        {/* Glow effect */}
        <div
          className="absolute inset-0 -z-10"
          style={{
            filter: 'blur(20px)',
            background: 'linear-gradient(45deg, #00ffff, #ff00ff, #ffff00)',
            opacity: 0.1,
            transform: 'scale(1.1)',
          }}
        />
      </motion.div>
    </motion.div>
  );
}
