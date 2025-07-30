// app/components/software/ProjectShowcase.tsx

'use client';

import { motion, useScroll, useTransform } from 'framer-motion';
import { useRef } from 'react';
import { Project } from '@/app/engineer/projects';
import Button from '../button';

interface ProjectShowcaseProps {
  project: Project;
  index: number;
}

export function ProjectShowcase({ project, index }: ProjectShowcaseProps) {
  const ref = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start end", "end start"]
  });

  const y = useTransform(scrollYProgress, [0, 1], [100, -100]);
  const opacity = useTransform(scrollYProgress, [0, 0.2, 0.8, 1], [0, 1, 1, 0]);
  const scale = useTransform(scrollYProgress, [0, 0.2, 0.8, 1], [0.8, 1, 1, 0.8]);

  const isEven = index % 2 === 0;

  return (
    <motion.section
      ref={ref}
      style={{ opacity, scale }}
      className="min-h-screen flex items-center justify-center py-20 px-6 sm:px-10 relative overflow-hidden bg-white"
    >
      
      <div className="max-w-7xl mx-auto w-full">
        <div className={`grid grid-cols-1 lg:grid-cols-2 gap-16 items-center ${isEven ? '' : 'lg:grid-flow-col-dense'}`}>
          
          {/* Content Side */}
          <motion.div 
            style={{ y }}
            className={`space-y-8 ${isEven ? 'lg:order-1' : 'lg:order-2'}`}
          >
            <div className="space-y-4">
              <motion.div
                initial={{ opacity: 0, x: isEven ? -50 : 50 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.8, delay: 0.2 }}
                className="flex items-center space-x-4"
              >
                <span className="text-5xl font-heading font-black text-neutral-100">
                  {String(index + 1).padStart(2, '0')}
                </span>
                <div className="flex space-x-2">
                  {project.tags.slice(0, 2).map(tag => (
                    <span key={tag} className="px-3 py-1 text-xs font-medium bg-neutral-100 rounded-full text-neutral-700">
                      {tag}
                    </span>
                  ))}
                </div>
              </motion.div>

              <motion.h2
                initial={{ opacity: 0, x: isEven ? -50 : 50 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.8, delay: 0.3 }}
                className="text-4xl sm:text-5xl font-heading font-black text-neutral-900 leading-tight"
              >
                {project.title}
              </motion.h2>

              <motion.p
                initial={{ opacity: 0, x: isEven ? -50 : 50 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.8, delay: 0.4 }}
                className="text-lg text-neutral-600 font-body leading-relaxed max-w-lg"
              >
                {project.description}
              </motion.p>

              <motion.div
                initial={{ opacity: 0, x: isEven ? -50 : 50 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.8, delay: 0.5 }}
                className="flex flex-wrap gap-3 pt-4"
              >
                {project.links?.page && (
                  <Button href={project.links.page} variant="solid" className="bg-neutral-900 text-white hover:bg-neutral-800 transition-colors">
                    View Project
                  </Button>
                )}
                {project.links?.github && (
                  <Button href={project.links.github} variant="outline" className="border-neutral-200 text-neutral-600 hover:bg-neutral-50 transition-colors">
                    Code
                  </Button>
                )}
              </motion.div>
            </div>
          </motion.div>

          {/* Media Side */}
          <motion.div 
            style={{ y: useTransform(scrollYProgress, [0, 1], [50, -50]) }}
            className={`relative ${isEven ? 'lg:order-2' : 'lg:order-1'}`}
          >
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              whileInView={{ opacity: 1, scale: 1 }}
              transition={{ duration: 1, delay: 0.3 }}
              className="relative aspect-video rounded-xl overflow-hidden shadow-lg border border-neutral-100"
            >
              {project.media[0].type === 'video' ? (
                <iframe
                  src={project.media[0].src}
                  title={project.media[0].alt}
                  className="w-full h-full"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                />
              ) : (
                <img
                  src={project.media[0].src}
                  alt={project.media[0].alt}
                  className="w-full h-full object-cover"
                />
              )}
              

            </motion.div>
          </motion.div>
        </div>
      </div>
    </motion.section>
  );
}

function getProjectGradient(iconType: Project['iconType']): string {
  switch (iconType) {
    case 'crypto':
      return 'bg-gradient-to-br from-orange-50 to-yellow-50';
    case 'ai':
      return 'bg-gradient-to-br from-purple-50 to-pink-50';
    case 'database':
      return 'bg-gradient-to-br from-blue-50 to-indigo-50';
    case 'web':
      return 'bg-gradient-to-br from-teal-50 to-green-50';
    case 'design':
      return 'bg-gradient-to-br from-rose-50 to-pink-50';
    case 'code':
      return 'bg-gradient-to-br from-green-50 to-emerald-50';
    case 'system':
      return 'bg-gradient-to-br from-gray-50 to-slate-50';
    default:
      return 'bg-gradient-to-br from-neutral-50 to-gray-50';
  }
}

function renderProjectElements(iconType: Project['iconType']) {
  switch (iconType) {
    case 'crypto':
      return (
        <>
          <motion.div
            className="absolute -top-4 -right-4 w-16 h-16 bg-yellow-400/30 rounded-full"
            animate={{ rotate: 360, scale: [1, 1.2, 1] }}
            transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
          />
          <motion.div
            className="absolute -bottom-4 -left-4 w-12 h-12 bg-orange-400/30 rounded-full"
            animate={{ rotate: -360, scale: [1, 0.8, 1] }}
            transition={{ duration: 6, repeat: Infinity, ease: "linear" }}
          />
        </>
      );
    case 'ai':
      return (
        <>
          <motion.div
            className="absolute top-4 right-4 w-8 h-8 bg-purple-400/40 rounded-full"
            animate={{ opacity: [0.3, 1, 0.3], scale: [1, 1.5, 1] }}
            transition={{ duration: 3, repeat: Infinity }}
          />
          <motion.div
            className="absolute bottom-4 left-4 w-6 h-6 bg-pink-400/40 rounded-full"
            animate={{ opacity: [0.3, 1, 0.3], scale: [1, 1.3, 1] }}
            transition={{ duration: 2, repeat: Infinity, delay: 1 }}
          />
        </>
      );
    default:
      return null;
  }
}
