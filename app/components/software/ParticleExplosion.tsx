// app/components/software/ParticleExplosion.tsx

'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { useState, useEffect } from 'react';

interface Particle {
  id: number;
  x: number;
  y: number;
  vx: number;
  vy: number;
  color: string;
  size: number;
  life: number;
}

interface ParticleExplosionProps {
  trigger: boolean;
  x: number;
  y: number;
  color?: string;
  particleCount?: number;
}

export function ParticleExplosion({ 
  trigger, 
  x, 
  y, 
  color = '#00ffff', 
  particleCount = 30 
}: ParticleExplosionProps) {
  const [particles, setParticles] = useState<Particle[]>([]);

  useEffect(() => {
    if (!trigger) return;

    const colors = [color, '#ff00ff', '#ffff00', '#00ff00', '#ff6600'];
    
    const newParticles: Particle[] = Array.from({ length: particleCount }, (_, i) => ({
      id: Date.now() + i,
      x,
      y,
      vx: (Math.random() - 0.5) * 400,
      vy: (Math.random() - 0.5) * 400,
      color: colors[Math.floor(Math.random() * colors.length)],
      size: Math.random() * 6 + 2,
      life: 1,
    }));

    setParticles(newParticles);

    // Clear particles after animation
    const timeout = setTimeout(() => {
      setParticles([]);
    }, 2000);

    return () => clearTimeout(timeout);
  }, [trigger, x, y, color, particleCount]);

  return (
    <div className="fixed inset-0 pointer-events-none z-[200]">
      <AnimatePresence>
        {particles.map((particle) => (
          <motion.div
            key={particle.id}
            className="absolute rounded-full"
            style={{
              backgroundColor: particle.color,
              width: particle.size,
              height: particle.size,
              boxShadow: `0 0 10px ${particle.color}`,
            }}
            initial={{
              x: particle.x,
              y: particle.y,
              scale: 1,
              opacity: 1,
            }}
            animate={{
              x: particle.x + particle.vx,
              y: particle.y + particle.vy,
              scale: 0,
              opacity: 0,
            }}
            transition={{
              duration: 2,
              ease: 'easeOut',
            }}
            exit={{ opacity: 0 }}
          />
        ))}
      </AnimatePresence>
    </div>
  );
}
