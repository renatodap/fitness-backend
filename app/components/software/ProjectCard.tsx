// app/components/software/ProjectCard.tsx

'use client';

import { motion } from 'framer-motion';
import { Project } from '@/app/engineer/projects';
import Button from '../button';
import { Tag } from '@/app/components/software/Tag';
import { AnimatedIcons } from './AnimatedIcons';

interface ProjectCardProps {
  project: Project;
}

export function ProjectCard({ project }: ProjectCardProps) {
  const cardVariants = {
    hidden: { opacity: 0, y: 50 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.5, ease: [0.22, 1, 0.36, 1] as const } },
  };

  return (
    <motion.div
      variants={cardVariants}
      className="group relative w-full bg-white border border-neutral-200/80 rounded-3xl p-6 sm:p-8 overflow-hidden shadow-lg shadow-neutral-100/50 transition-all duration-300 hover:shadow-2xl hover:border-neutral-300"
    >
      <AnimatedIcons iconType={project.iconType} />
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
        {/* Left side: Media */}
        <motion.div 
          className="relative aspect-video rounded-xl overflow-hidden border border-neutral-200 transition-transform duration-500 ease-[cubic-bezier(0.22,1,0.36,1)] group-hover:scale-105"
        >
          {project.media[0].type === 'video' ? (
            <iframe
              src={project.media[0].src}
              title={project.media[0].alt}
              className="w-full h-full"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            ></iframe>
          ) : (
            <img
              src={project.media[0].src}
              alt={project.media[0].alt}
              className="w-full h-full object-cover"
            />
          )}
        </motion.div>

        {/* Right side: Details */}
        <div className="flex flex-col h-full">
          <h3 className="text-2xl font-heading font-bold text-neutral-800 mb-2">{project.title}</h3>
          <p className="font-body text-neutral-600 leading-relaxed mb-4">{project.description}</p>

          <div className="flex flex-wrap gap-2 mb-4">
            {project.tags.map(tag => (
              <Tag key={tag} text={tag} />
            ))}
          </div>

          <div className="mt-auto pt-4 flex flex-wrap gap-3">
            {project.links?.page && (
              <Button href={project.links.page} variant="solid" size="sm">
                Case Study
              </Button>
            )}
            {project.links?.github && (
              <Button href={project.links.github} variant="outline" size="sm">
                GitHub
              </Button>
            )}
            {project.links?.video && (
              <Button href={project.links.video} variant="outline" size="sm">
                Watch Video
              </Button>
            )}
          </div>
        </div>
      </div>
    </motion.div>
  );
}
