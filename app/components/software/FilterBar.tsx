// app/components/software/FilterBar.tsx

'use client';

import { motion } from 'framer-motion';
import { Project } from '@/app/software/projects';
import { Tag } from './Tag';

interface FilterBarProps {
  projects: Project[];
  activeTag: string;
  onTagClick: (tag: string) => void;
}

export function FilterBar({ projects, activeTag, onTagClick }: FilterBarProps) {
  const allTags = ['All', ...Array.from(new Set(projects.flatMap(p => p.tags)))];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.05,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 },
  };

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="flex flex-wrap justify-center gap-2 sm:gap-3 py-8"
    >
      {allTags.map(tag => (
        <motion.div key={tag} variants={itemVariants}>
          <Tag
            text={tag}
            isActive={tag === activeTag}
            onClick={() => onTagClick(tag)}
          />
        </motion.div>
      ))}
    </motion.div>
  );
}
