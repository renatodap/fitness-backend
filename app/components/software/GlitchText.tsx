// app/components/software/GlitchText.tsx

'use client';

import { motion, useAnimation } from 'framer-motion';
import { useEffect, useState } from 'react';

interface GlitchTextProps {
  text: string;
  className?: string;
  glitchIntensity?: 'low' | 'medium' | 'high';
}

export function GlitchText({ text, className, glitchIntensity = 'medium' }: GlitchTextProps) {
  const [isGlitching, setIsGlitching] = useState(false);
  const [glitchText, setGlitchText] = useState(text);
  const controls = useAnimation();

  const glitchChars = '!@#$%^&*()_+-=[]{}|;:,.<>?`~1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
  
  const intensitySettings = {
    low: { frequency: 8000, duration: 150, corruption: 0.1 },
    medium: { frequency: 5000, duration: 200, corruption: 0.2 },
    high: { frequency: 3000, duration: 300, corruption: 0.3 }
  };

  const settings = intensitySettings[glitchIntensity];

  const triggerGlitch = async () => {
    if (isGlitching) return;
    
    setIsGlitching(true);
    
    // Create corrupted version of text
    const corruptedText = text.split('').map(char => {
      if (char === ' ') return ' ';
      return Math.random() < settings.corruption 
        ? glitchChars[Math.floor(Math.random() * glitchChars.length)]
        : char;
    }).join('');
    
    // Glitch animation sequence
    setGlitchText(corruptedText);
    
    await controls.start({
      x: [0, -2, 2, -1, 1, 0],
      y: [0, 1, -1, 0],
      skewX: [0, -2, 2, 0],
      transition: { duration: settings.duration / 1000, ease: "easeInOut" }
    });
    
    // Restore original text
    setTimeout(() => {
      setGlitchText(text);
      setIsGlitching(false);
    }, settings.duration / 2);
  };

  useEffect(() => {
    const interval = setInterval(triggerGlitch, settings.frequency);
    return () => clearInterval(interval);
  }, [settings.frequency]);

  return (
    <motion.div
      animate={controls}
      className={`relative inline-block ${className}`}
      style={{
        filter: isGlitching ? 'hue-rotate(90deg) saturate(150%)' : 'none',
      }}
    >
      {/* Main text */}
      <span className="relative z-10">
        {glitchText}
      </span>
      
      {/* Glitch layers */}
      {isGlitching && (
        <>
          <span 
            className="absolute top-0 left-0 z-0 text-red-500 opacity-70"
            style={{ 
              transform: 'translate(-1px, 0)',
              mixBlendMode: 'multiply'
            }}
          >
            {glitchText}
          </span>
          <span 
            className="absolute top-0 left-0 z-0 text-cyan-400 opacity-70"
            style={{ 
              transform: 'translate(1px, 0)',
              mixBlendMode: 'multiply'
            }}
          >
            {glitchText}
          </span>
          <span 
            className="absolute top-0 left-0 z-0 text-green-400 opacity-50"
            style={{ 
              transform: 'translate(0, 1px)',
              mixBlendMode: 'multiply'
            }}
          >
            {glitchText}
          </span>
        </>
      )}
      
      {/* Scanline effect */}
      {isGlitching && (
        <motion.div
          className="absolute inset-0 z-20 pointer-events-none"
          initial={{ opacity: 0 }}
          animate={{ opacity: [0, 0.3, 0] }}
          transition={{ duration: settings.duration / 1000, repeat: 2 }}
          style={{
            background: 'repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255,255,255,0.1) 2px, rgba(255,255,255,0.1) 4px)',
          }}
        />
      )}
    </motion.div>
  );
}
