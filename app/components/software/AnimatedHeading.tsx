// app/components/software/AnimatedHeading.tsx

'use client';

import { motion } from 'framer-motion';

interface AnimatedHeadingProps {
  text: string;
  className?: string;
}

const sentenceVariants = {
  hidden: { opacity: 1 },
  visible: {
    opacity: 1,
    transition: {
      delay: 0.5,
      staggerChildren: 0.08,
    },
  },
};

const letterVariants = {
  hidden: { opacity: 0, y: 50 },
  visible: { opacity: 1, y: 0 },
};

export function AnimatedHeading({ text, className }: AnimatedHeadingProps) {
  return (
    <motion.h1
      className={className}
      variants={sentenceVariants}
      initial="hidden"
      animate="visible"
      aria-label={text}
    >
      {text.split('').map((char, index) => (
        <motion.span
          key={`${char}-${index}`}
          variants={letterVariants}
          className="inline-block"
        >
          {char === ' ' ? '\u00A0' : char} 
        </motion.span>
      ))}
    </motion.h1>
  );
}
