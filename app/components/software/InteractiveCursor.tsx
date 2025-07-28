// app/components/software/InteractiveCursor.tsx

'use client';

import { motion, useMotionValue, useSpring } from 'framer-motion';
import { useEffect, useState } from 'react';

export function InteractiveCursor() {
  const [cursorType, setCursorType] = useState<'default' | 'hover' | 'click' | 'code'>('default');
  const [isVisible, setIsVisible] = useState(false);
  
  const cursorX = useMotionValue(-100);
  const cursorY = useMotionValue(-100);
  
  const springConfig = { damping: 25, stiffness: 700 };
  const cursorXSpring = useSpring(cursorX, springConfig);
  const cursorYSpring = useSpring(cursorY, springConfig);

  useEffect(() => {
    const moveCursor = (e: MouseEvent) => {
      cursorX.set(e.clientX - 16);
      cursorY.set(e.clientY - 16);
      setIsVisible(true);
    };

    const handleMouseEnter = () => setIsVisible(true);
    const handleMouseLeave = () => setIsVisible(false);

    // Detect hover states
    const handleMouseOver = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      
      if (target.tagName === 'BUTTON' || target.closest('button') || target.closest('a')) {
        setCursorType('hover');
      } else if (target.closest('code') || target.closest('pre') || target.classList.contains('font-mono')) {
        setCursorType('code');
      } else {
        setCursorType('default');
      }
    };

    const handleMouseDown = () => setCursorType('click');
    const handleMouseUp = () => setCursorType('hover');

    window.addEventListener('mousemove', moveCursor);
    window.addEventListener('mouseover', handleMouseOver);
    window.addEventListener('mouseenter', handleMouseEnter);
    window.addEventListener('mouseleave', handleMouseLeave);
    window.addEventListener('mousedown', handleMouseDown);
    window.addEventListener('mouseup', handleMouseUp);

    return () => {
      window.removeEventListener('mousemove', moveCursor);
      window.removeEventListener('mouseover', handleMouseOver);
      window.removeEventListener('mouseenter', handleMouseEnter);
      window.removeEventListener('mouseleave', handleMouseLeave);
      window.removeEventListener('mousedown', handleMouseDown);
      window.removeEventListener('mouseup', handleMouseUp);
    };
  }, [cursorX, cursorY]);

  const getCursorVariant = () => {
    switch (cursorType) {
      case 'hover':
        return {
          scale: 1.5,
          backgroundColor: 'rgba(20, 184, 166, 0.8)',
          border: '2px solid rgba(20, 184, 166, 1)',
        };
      case 'click':
        return {
          scale: 0.8,
          backgroundColor: 'rgba(244, 63, 94, 0.8)',
          border: '2px solid rgba(244, 63, 94, 1)',
        };
      case 'code':
        return {
          scale: 1.2,
          backgroundColor: 'rgba(34, 197, 94, 0.8)',
          border: '2px solid rgba(34, 197, 94, 1)',
          borderRadius: '4px',
        };
      default:
        return {
          scale: 1,
          backgroundColor: 'rgba(255, 255, 255, 0.8)',
          border: '2px solid rgba(255, 255, 255, 1)',
        };
    }
  };

  return (
    <motion.div
      className="fixed top-0 left-0 w-8 h-8 pointer-events-none z-[9999] mix-blend-difference"
      style={{
        x: cursorXSpring,
        y: cursorYSpring,
      }}
      animate={{
        opacity: isVisible ? 1 : 0,
        ...getCursorVariant(),
      }}
      transition={{
        opacity: { duration: 0.2 },
        scale: { duration: 0.2 },
        backgroundColor: { duration: 0.2 },
      }}
    >
      {/* Cursor dot */}
      <div className="w-full h-full rounded-full" />
      
      {/* Cursor trail effect */}
      <motion.div
        className="absolute inset-0 rounded-full"
        animate={{
          scale: cursorType === 'hover' ? [1, 1.5, 1] : 1,
          opacity: cursorType === 'hover' ? [0.5, 0, 0.5] : 0,
        }}
        transition={{
          duration: 1,
          repeat: cursorType === 'hover' ? Infinity : 0,
        }}
        style={{
          border: '1px solid rgba(20, 184, 166, 0.5)',
        }}
      />
    </motion.div>
  );
}
