// app/components/software/MatrixRain.tsx

'use client';

import { motion } from 'framer-motion';
import { useEffect, useState, useRef } from 'react';

interface MatrixRainProps {
  intensity?: 'low' | 'medium' | 'high';
  trigger?: boolean;
}

export function MatrixRain({ intensity = 'medium', trigger = false }: MatrixRainProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isActive, setIsActive] = useState(false);

  const characters = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン';
  
  const intensitySettings = {
    low: { columns: 20, speed: 50, opacity: 0.1 },
    medium: { columns: 40, speed: 30, opacity: 0.15 },
    high: { columns: 80, speed: 20, opacity: 0.2 }
  };

  const settings = intensitySettings[intensity];

  useEffect(() => {
    if (trigger) {
      setIsActive(true);
      const timeout = setTimeout(() => setIsActive(false), 3000); // 3 second burst
      return () => clearTimeout(timeout);
    }
  }, [trigger]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || !isActive) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const columns = Math.floor(canvas.width / 20);
    const drops: number[] = Array(columns).fill(1);

    const draw = () => {
      ctx.fillStyle = `rgba(0, 0, 0, ${1 - settings.opacity})`;
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      ctx.fillStyle = '#00ff41';
      ctx.font = '15px monospace';

      for (let i = 0; i < drops.length; i++) {
        const text = characters[Math.floor(Math.random() * characters.length)];
        ctx.fillText(text, i * 20, drops[i] * 20);

        if (drops[i] * 20 > canvas.height && Math.random() > 0.975) {
          drops[i] = 0;
        }
        drops[i]++;
      }
    };

    const interval = setInterval(draw, settings.speed);
    return () => clearInterval(interval);
  }, [isActive, settings]);

  if (!isActive) return null;

  return (
    <motion.canvas
      ref={canvasRef}
      className="fixed inset-0 pointer-events-none z-[100]"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.5 }}
    />
  );
}
