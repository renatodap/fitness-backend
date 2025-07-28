// app/components/software/FloatingCode.tsx

'use client';

import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';

const codeSnippets = [
  'fn main() {',
  'const [state, setState]',
  'SELECT * FROM',
  'git commit -m',
  'docker run -d',
  'npm install',
  'cargo build',
  'async/await',
  'useState()',
  'blockchain.verify()',
  'AI.predict()',
  'db.query()',
  'React.memo',
  'useEffect()',
  'match pattern',
  'impl Trait',
  'pub struct',
  'let mut',
  'HashMap::new()',
  'Vec<T>',
  'Result<T, E>',
  'Option<T>',
  'Box<dyn>',
  'Arc<Mutex<>>',
  'tokio::spawn',
  'serde::Serialize',
  'clap::Parser',
  'reqwest::get',
  'sqlx::query',
  'tracing::info',
];

interface FloatingCodeProps {
  count?: number;
}

export function FloatingCode({ count = 15 }: FloatingCodeProps) {
  const [snippets, setSnippets] = useState<Array<{
    id: number;
    text: string;
    x: number;
    y: number;
    duration: number;
    delay: number;
    opacity: number;
  }>>([]);

  useEffect(() => {
    const generateSnippets = () => {
      const newSnippets = Array.from({ length: count }, (_, i) => ({
        id: i,
        text: codeSnippets[Math.floor(Math.random() * codeSnippets.length)],
        x: Math.random() * 100,
        y: Math.random() * 100,
        duration: 15 + Math.random() * 10, // 15-25 seconds
        delay: Math.random() * 5, // 0-5 second delay
        opacity: 0.1 + Math.random() * 0.3, // 0.1-0.4 opacity
      }));
      setSnippets(newSnippets);
    };

    generateSnippets();
    
    // Regenerate snippets periodically
    const interval = setInterval(generateSnippets, 30000); // Every 30 seconds
    
    return () => clearInterval(interval);
  }, [count]);

  return (
    <div className="absolute inset-0 pointer-events-none overflow-hidden">
      {snippets.map((snippet) => (
        <motion.div
          key={`${snippet.id}-${snippet.text}`}
          className="absolute font-mono text-sm text-teal-400/60 whitespace-nowrap"
          initial={{
            x: `${snippet.x}vw`,
            y: `${snippet.y}vh`,
            opacity: 0,
            rotate: Math.random() * 20 - 10,
          }}
          animate={{
            y: [`${snippet.y}vh`, `${snippet.y - 120}vh`],
            x: [
              `${snippet.x}vw`,
              `${snippet.x + (Math.random() * 20 - 10)}vw`,
              `${snippet.x + (Math.random() * 40 - 20)}vw`,
            ],
            opacity: [0, snippet.opacity, snippet.opacity, 0],
            rotate: [
              Math.random() * 20 - 10,
              Math.random() * 30 - 15,
              Math.random() * 20 - 10,
            ],
          }}
          transition={{
            duration: snippet.duration,
            delay: snippet.delay,
            repeat: Infinity,
            ease: "linear",
          }}
        >
          {snippet.text}
        </motion.div>
      ))}
    </div>
  );
}
