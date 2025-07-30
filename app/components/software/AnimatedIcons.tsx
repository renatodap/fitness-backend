// app/components/software/AnimatedIcons.tsx

'use client';

import { motion } from 'framer-motion';
import { Project } from '@/app/engineer/projects';

interface AnimatedIconsProps {
  iconType: Project['iconType'];
}

export function AnimatedIcons({ iconType }: AnimatedIconsProps) {
  const renderIcons = () => {
    switch (iconType) {
      case 'crypto':
        return (
          <>
            {/* Bitcoin-style coin */}
            <motion.div
              className="absolute top-4 right-4 w-8 h-8"
              animate={{ rotate: 360, y: [0, -10, 0] }}
              transition={{ duration: 4, repeat: Infinity, ease: "linear" }}
            >
              <svg viewBox="0 0 24 24" className="w-full h-full text-orange-400">
                <circle cx="12" cy="12" r="10" fill="currentColor" opacity="0.8"/>
                <path d="M15.5 10.5c0-1.5-1-2.5-2.5-2.5h-2v5h2c1.5 0 2.5-1 2.5-2.5z" fill="white"/>
                <path d="M15 14c0-1.5-1-2.5-2.5-2.5h-2.5v5h2.5c1.5 0 2.5-1 2.5-2.5z" fill="white"/>
              </svg>
            </motion.div>
            
            {/* Blockchain links */}
            <motion.div
              className="absolute bottom-6 left-6 flex space-x-2"
              animate={{ x: [0, 5, 0] }}
              transition={{ duration: 3, repeat: Infinity }}
            >
              {[...Array(3)].map((_, i) => (
                <div key={i} className="w-3 h-3 bg-teal-400 rounded-sm opacity-70" />
              ))}
            </motion.div>
            
            {/* Key icon */}
            <motion.div
              className="absolute top-1/2 left-4 w-6 h-6"
              animate={{ rotate: [0, 15, 0] }}
              transition={{ duration: 2, repeat: Infinity, delay: 1 }}
            >
              <svg viewBox="0 0 24 24" className="w-full h-full text-yellow-400">
                <path d="M7 14c-1.66 0-3-1.34-3-3s1.34-3 3-3 3 1.34 3 3-1.34 3-3 3zm0-4c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1z" fill="currentColor"/>
                <path d="m12.65 10 1.41-1.41c.2-.2.2-.51 0-.71-.2-.2-.51-.2-.71 0L12 9.24l-1.35-1.35c-.2-.2-.51-.2-.71 0-.2.2-.2.51 0 .71L11.35 10H9v2h2.35l-1.41 1.41c-.2.2-.2.51 0 .71.1.1.23.15.35.15s.26-.05.35-.15L12 12.76l1.35 1.35c.1.1.23.15.35.15s.26-.05.35-.15c.2-.2.2-.51 0-.71L12.65 12H15v-2h-2.35z" fill="currentColor"/>
              </svg>
            </motion.div>
          </>
        );
        
      case 'ai':
        return (
          <>
            {/* Neural network nodes */}
            <motion.div
              className="absolute top-4 right-4"
              animate={{ scale: [1, 1.1, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              <svg viewBox="0 0 40 40" className="w-8 h-8 text-purple-400">
                <circle cx="10" cy="10" r="3" fill="currentColor"/>
                <circle cx="30" cy="10" r="3" fill="currentColor"/>
                <circle cx="20" cy="25" r="3" fill="currentColor"/>
                <line x1="10" y1="10" x2="20" y2="25" stroke="currentColor" strokeWidth="1"/>
                <line x1="30" y1="10" x2="20" y2="25" stroke="currentColor" strokeWidth="1"/>
              </svg>
            </motion.div>
            
            {/* Brain icon */}
            <motion.div
              className="absolute bottom-4 left-4 w-8 h-8"
              animate={{ opacity: [0.5, 1, 0.5] }}
              transition={{ duration: 3, repeat: Infinity }}
            >
              <svg viewBox="0 0 24 24" className="w-full h-full text-pink-400">
                <path d="M9,2A3,3 0 0,1 12,5A3,3 0 0,1 15,2A3,3 0 0,1 18,5C18,6.32 17.75,7.22 17.24,8.1C17.8,9.04 18,10.13 18,11.5C18,14.5 16.5,16 14.5,16H9.5C7.5,16 6,14.5 6,11.5C6,10.13 6.2,9.04 6.76,8.1C6.25,7.22 6,6.32 6,5A3,3 0 0,1 9,2M9,4A1,1 0 0,0 8,5C8,5.5 8.2,6.17 8.71,7.05L9.5,8.5L8.5,9.5C8.08,10.13 8,10.63 8,11.5C8,13.5 8.5,14 9.5,14H14.5C15.5,14 16,13.5 16,11.5C16,10.63 15.92,10.13 15.5,9.5L14.5,8.5L15.29,7.05C15.8,6.17 16,5.5 16,5A1,1 0 0,0 15,4A1,1 0 0,0 14,5A1,1 0 0,0 15,6H13A1,1 0 0,0 12,5A1,1 0 0,0 11,6H9A1,1 0 0,0 10,5A1,1 0 0,0 9,4Z" fill="currentColor"/>
              </svg>
            </motion.div>
          </>
        );
        
      case 'system':
        return (
          <>
            {/* Terminal cursor */}
            <motion.div
              className="absolute top-4 left-4 w-1 h-4 bg-green-400"
              animate={{ opacity: [1, 0, 1] }}
              transition={{ duration: 1, repeat: Infinity }}
            />
            
            {/* System processes */}
            <motion.div
              className="absolute bottom-4 right-4 space-y-1"
              animate={{ x: [0, 3, 0] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              {[...Array(4)].map((_, i) => (
                <div key={i} className={`h-1 bg-green-400 rounded`} style={{width: `${20 + i * 8}px`}} />
              ))}
            </motion.div>
          </>
        );
        
      case 'hardware':
        return (
          <>
            {/* CPU chip */}
            <motion.div
              className="absolute top-4 right-4 w-8 h-8"
              animate={{ rotate: [0, 90, 180, 270, 360] }}
              transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
            >
              <svg viewBox="0 0 24 24" className="w-full h-full text-blue-400">
                <rect x="6" y="6" width="12" height="12" fill="currentColor" opacity="0.8"/>
                <rect x="8" y="8" width="8" height="8" fill="white"/>
                <rect x="2" y="9" width="2" height="2" fill="currentColor"/>
                <rect x="2" y="13" width="2" height="2" fill="currentColor"/>
                <rect x="20" y="9" width="2" height="2" fill="currentColor"/>
                <rect x="20" y="13" width="2" height="2" fill="currentColor"/>
                <rect x="9" y="2" width="2" height="2" fill="currentColor"/>
                <rect x="13" y="2" width="2" height="2" fill="currentColor"/>
                <rect x="9" y="20" width="2" height="2" fill="currentColor"/>
                <rect x="13" y="20" width="2" height="2" fill="currentColor"/>
              </svg>
            </motion.div>
            
            {/* Circuit traces */}
            <motion.div
              className="absolute bottom-6 left-6"
              animate={{ opacity: [0.3, 1, 0.3] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              <svg viewBox="0 0 30 20" className="w-8 h-5 text-cyan-400">
                <path d="M0,10 L10,10 L15,5 L20,15 L30,10" stroke="currentColor" strokeWidth="2" fill="none"/>
              </svg>
            </motion.div>
          </>
        );
        
      case 'code':
        return (
          <>
            {/* Code brackets */}
            <motion.div
              className="absolute top-4 left-4 text-2xl font-mono text-green-400"
              animate={{ scale: [1, 1.1, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              {'</>'}
            </motion.div>
            
            {/* Bug icon */}
            <motion.div
              className="absolute bottom-4 right-4 w-6 h-6"
              animate={{ y: [0, -5, 0] }}
              transition={{ duration: 3, repeat: Infinity }}
            >
              <svg viewBox="0 0 24 24" className="w-full h-full text-red-400">
                <path d="M14,12H10V10H14M14,16H10V14H14M20,8H17.19C16.74,7.22 16.12,6.55 15.37,6.04L17,4.41L15.59,3L13.42,5.17C12.96,5.06 12.5,5 12,5C11.5,5 11.04,5.06 10.59,5.17L8.41,3L7,4.41L8.62,6.04C7.88,6.55 7.26,7.22 6.81,8H4V10H6.09C6.04,10.33 6,10.66 6,11V12H4V14H6V15C6,15.34 6.04,15.67 6.09,16H4V18H6.81C7.85,19.79 9.78,21 12,21C14.22,21 16.15,19.79 17.19,18H20V16H17.91C17.96,15.67 18,15.34 18,15V14H20V12H18V11C18,10.66 17.96,10.33 17.91,10H20V8Z" fill="currentColor"/>
              </svg>
            </motion.div>
          </>
        );
        
      case 'database':
        return (
          <>
            {/* Database cylinders */}
            <motion.div
              className="absolute top-4 right-4"
              animate={{ rotateY: [0, 180, 360] }}
              transition={{ duration: 4, repeat: Infinity }}
            >
              <svg viewBox="0 0 24 24" className="w-8 h-8 text-indigo-400">
                <ellipse cx="12" cy="5" rx="9" ry="3" fill="currentColor"/>
                <path d="M3 5v14c0 1.66 4.03 3 9 3s9-1.34 9-3V5" stroke="currentColor" strokeWidth="2" fill="none"/>
                <ellipse cx="12" cy="12" rx="9" ry="3" fill="currentColor" opacity="0.7"/>
              </svg>
            </motion.div>
            
            {/* Data flow */}
            <motion.div
              className="absolute bottom-6 left-6 flex space-x-1"
              animate={{ x: [0, 10, 0] }}
              transition={{ duration: 3, repeat: Infinity }}
            >
              {[...Array(3)].map((_, i) => (
                <div key={i} className="w-2 h-2 bg-purple-400 rounded-full" />
              ))}
            </motion.div>
          </>
        );
        
      case 'web':
        return (
          <>
            {/* HTML tag */}
            <motion.div
              className="absolute top-4 left-4 text-orange-400 font-mono text-sm"
              animate={{ rotate: [0, 5, -5, 0] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              {'<html>'}
            </motion.div>
            
            {/* Browser window */}
            <motion.div
              className="absolute bottom-4 right-4 w-8 h-6 border-2 border-blue-400 rounded"
              animate={{ scale: [1, 1.05, 1] }}
              transition={{ duration: 3, repeat: Infinity }}
            >
              <div className="flex space-x-1 p-1">
                <div className="w-1 h-1 bg-red-400 rounded-full"></div>
                <div className="w-1 h-1 bg-yellow-400 rounded-full"></div>
                <div className="w-1 h-1 bg-green-400 rounded-full"></div>
              </div>
            </motion.div>
          </>
        );
        
      case 'game':
        return (
          <>
            {/* Game controller */}
            <motion.div
              className="absolute top-4 right-4 w-8 h-6"
              animate={{ rotate: [0, 10, -10, 0] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              <svg viewBox="0 0 24 24" className="w-full h-full text-purple-500">
                <path d="M7.97,16L5,12.5C5,11.12 6.12,10 7.5,10H9.5C10.88,10 12,11.12 12,12.5L9.03,16H7.97M17,14A2,2 0 0,1 15,16A2,2 0 0,1 13,14A2,2 0 0,1 15,12A2,2 0 0,1 17,14M18.5,10C19.88,10 21,11.12 21,12.5L18.03,16H14.97L12,12.5C12,11.12 13.12,10 14.5,10H18.5Z" fill="currentColor"/>
              </svg>
            </motion.div>
            
            {/* Pixel particles */}
            <motion.div
              className="absolute bottom-4 left-4 grid grid-cols-3 gap-1"
              animate={{ opacity: [0.5, 1, 0.5] }}
              transition={{ duration: 1.5, repeat: Infinity }}
            >
              {[...Array(9)].map((_, i) => (
                <div key={i} className="w-1 h-1 bg-pink-400 rounded-sm" />
              ))}
            </motion.div>
          </>
        );
        
      case 'design':
        return (
          <>
            {/* Palette */}
            <motion.div
              className="absolute top-4 right-4 w-8 h-8"
              animate={{ rotate: [0, 360] }}
              transition={{ duration: 10, repeat: Infinity, ease: "linear" }}
            >
              <svg viewBox="0 0 24 24" className="w-full h-full text-rose-400">
                <path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22C13.11,22 14,21.11 14,20V18.76C14,18.32 14.69,17.65 15.14,17.2C15.59,16.75 16.26,16.07 16.7,15.62C17.14,15.17 17.81,14.5 18.26,14.05C18.71,13.6 19.38,12.93 19.82,12.48C20.27,12.03 20.94,11.36 21.39,10.91C21.84,10.46 22.5,9.78 22.95,9.33C23.4,8.88 24.07,8.21 24.52,7.76C24.97,7.31 25.64,6.64 26.09,6.19C26.54,5.74 27.21,5.07 27.66,4.62C28.11,4.17 28.78,3.5 29.23,3.05C29.68,2.6 30.35,1.93 30.8,1.48L12,2Z" fill="currentColor"/>
              </svg>
            </motion.div>
            
            {/* Design elements */}
            <motion.div
              className="absolute bottom-4 left-4 space-y-1"
              animate={{ x: [0, 2, 0] }}
              transition={{ duration: 4, repeat: Infinity }}
            >
              <div className="w-6 h-1 bg-teal-400 rounded"></div>
              <div className="w-4 h-1 bg-rose-400 rounded"></div>
              <div className="w-5 h-1 bg-orange-400 rounded"></div>
            </motion.div>
          </>
        );
        
      default:
        return null;
    }
  };

  return (
    <div className="absolute inset-0 pointer-events-none overflow-hidden">
      {renderIcons()}
    </div>
  );
}
