// app/engineer/page.tsx

'use client';

import UniversalHero from '@/app/components/shared/UniversalHero';
import { projects } from './projects';
import { motion, useInView, useScroll, useTransform } from 'framer-motion';
import { useRef } from 'react';

// === THE ENGINEERING PHILOSOPHY ===

const engineeringPrinciples = [
  {
    principle: "Elegant Simplicity",
    description: "The best solutions are often the simplest ones. Every line of code should have a purpose, every feature should solve a real problem.",
    icon: "⚡"
  },
  {
    principle: "Systems Thinking",
    description: "Understanding how components interact, anticipating edge cases, and designing for scale from day one.",
    icon: "🔗"
  },
  {
    principle: "User-Centric Design",
    description: "Technology serves people. Every technical decision should ultimately improve the human experience.",
    icon: "👥"
  },
  {
    principle: "Continuous Learning",
    description: "The field evolves rapidly. Staying curious, experimenting with new technologies, and learning from failures.",
    icon: "📚"
  }
];

const technicalSkills = {
  languages: ['Python', 'TypeScript', 'Go', 'Java', 'C', 'SQL', 'Verilog'],
  frameworks: ['React', 'Next.js', 'Flask', 'TensorFlow', 'Express.js'],
  tools: ['Docker', 'Git', 'PostgreSQL', 'MongoDB', 'AWS', 'QEMU'],
  concepts: ['Machine Learning', 'Blockchain', 'Systems Programming', 'Web Architecture']
};

// === CINEMATIC COMPONENTS ===

function CinematicSection({ children, className = '', delay = 0 }: { 
  children: React.ReactNode; 
  className?: string; 
  delay?: number;
}) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: '-50px' });
  
  return (
    <motion.div
      ref={ref}
      className={className}
      initial={{ opacity: 0, y: 60 }}
      animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 60 }}
      transition={{ duration: 1.2, ease: 'easeOut', delay }}
    >
      {children}
    </motion.div>
  );
}

function ParallaxText({ children, offset = 50 }: { children: React.ReactNode; offset?: number }) {
  const ref = useRef(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ['start end', 'end start']
  });
  const y = useTransform(scrollYProgress, [0, 1], [offset, -offset]);
  
  return (
    <motion.div ref={ref} style={{ y }}>
      {children}
    </motion.div>
  );
}

function FloatingCard({ children, index = 0 }: { children: React.ReactNode; index?: number }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 40, rotateX: 10 }}
      whileInView={{ opacity: 1, y: 0, rotateX: 0 }}
      transition={{ duration: 0.8, delay: index * 0.1, ease: 'easeOut' }}
      viewport={{ once: true, margin: '-50px' }}
      whileHover={{ y: -8, scale: 1.02 }}
      className="transform-gpu"
    >
      {children}
    </motion.div>
  );
}

export default function EngineerPage() {
  return (
    <main className="relative w-full bg-white text-black overflow-x-hidden">
      {/* === OPENING FRAME === */}
      <UniversalHero
        theme="engineer"
        title="Meet What I've Built"
        subtitle="What I build reflects how I think — structured, honest, and iterative."
        videoSrc="/software.mp4"
        mobileVideoSrc="/software.mp4"
      />

      {/* === ACT I: FEATURED PROJECTS === */}
      <section className="py-32 lg:py-40 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-white to-teal-25">
        <div className="max-w-7xl mx-auto">
          <CinematicSection className="text-center mb-24">
            <ParallaxText>
              <h2 className="text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight text-neutral-900 mb-8">
                Featured
                <br />
                <span className="bg-gradient-to-r from-teal-600 via-teal-500 to-teal-400 bg-clip-text text-transparent">
                  Projects
                </span>
              </h2>
            </ParallaxText>
          </CinematicSection>

          <div className="space-y-32">
            {projects.map((project, index) => (
              <CinematicSection key={project.id} delay={index * 0.2}>
                <motion.div
                  className={`flex flex-col lg:flex-row items-center gap-16 ${index % 2 === 1 ? 'lg:flex-row-reverse' : ''}`}
                  initial={{ opacity: 0, x: index % 2 === 0 ? -80 : 80 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  transition={{ duration: 1.4, ease: 'easeOut' }}
                  viewport={{ once: true, margin: '-100px' }}
                >
                  <div className="lg:w-1/2">
                    <FloatingCard index={index}>
                      <div className="relative aspect-video bg-gradient-to-br from-teal-50 to-neutral-50 rounded-3xl overflow-hidden border border-teal-100 shadow-2xl group">
                        <div className="absolute inset-0 bg-gradient-to-t from-black/20 via-transparent to-transparent"></div>
                        <div className="absolute inset-0 flex items-center justify-center">
                          <div className="text-teal-300 text-8xl opacity-30 group-hover:opacity-50 transition-opacity duration-500">⚡</div>
                        </div>
                        <div className="absolute top-6 left-6 right-6">
                          <div className="flex items-center justify-between">
                            <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                              project.category === 'AI/ML' ? 'bg-purple-100 text-purple-800' :
                              project.category === 'Blockchain' ? 'bg-orange-100 text-orange-800' :
                              project.category === 'Web Development' ? 'bg-blue-100 text-blue-800' :
                              project.category === 'Database Systems' ? 'bg-green-100 text-green-800' :
                              project.category === 'Full Stack' ? 'bg-indigo-100 text-indigo-800' :
                              'bg-teal-100 text-teal-800'
                            }`}>
                              {project.category}
                            </span>
                            <span className="bg-black/70 text-white px-2 py-1 rounded text-xs font-medium">
                              {project.timeframe}
                            </span>
                          </div>
                        </div>
                        <div className="absolute bottom-6 left-6 right-6">
                          <div className="bg-white/95 backdrop-blur-sm rounded-2xl p-4 border border-white/20 shadow-lg">
                            <div className="flex items-center justify-between">
                              <div>
                                <p className="text-sm font-semibold text-neutral-800">{project.title}</p>
                                <p className="text-xs text-neutral-600">{project.status === 'In Progress' ? 'In Development' : 'Completed'}</p>
                              </div>
                              <div className="flex gap-2">
                                {project.links?.github && (
                                  <div className="w-8 h-8 bg-neutral-100 rounded-full flex items-center justify-center">
                                    <span className="text-xs">🔗</span>
                                  </div>
                                )}
                                {project.links?.live && (
                                  <div className="w-8 h-8 bg-teal-100 rounded-full flex items-center justify-center">
                                    <span className="text-xs">🚀</span>
                                  </div>
                                )}
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </FloatingCard>
                  </div>
                  
                  <div className="lg:w-1/2 space-y-8">
                    <div>
                      <div className="inline-flex items-center px-4 py-2 bg-teal-100 text-teal-800 text-sm font-semibold rounded-full mb-6 border border-teal-200">
                        {project.category}
                      </div>
                      <h3 className="text-4xl sm:text-5xl font-bold text-neutral-900 mb-6">{project.title}</h3>
                    </div>
                    
                    <p className="text-lg text-neutral-600 leading-relaxed mb-8">
                      {project.description}
                    </p>
                    
                    <div className="bg-teal-50/50 border-l-4 border-teal-300 pl-8 py-4 rounded-r-2xl mb-8">
                      <p className="text-teal-800 font-medium text-sm mb-2">Tech Stack:</p>
                      <div className="flex flex-wrap gap-2">
                        {project.tech.map((tech: string) => (
                          <span key={tech} className="px-3 py-1 bg-white text-teal-700 text-sm rounded-full border border-teal-200 font-medium">
                            {tech}
                          </span>
                        ))}
                      </div>
                    </div>
                    
                    <div className="flex gap-4">
                      {project.links?.github && (
                        <motion.a
                          href={project.links.github}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center gap-2 px-6 py-3 border border-neutral-300 text-neutral-700 rounded-xl hover:border-teal-300 hover:bg-teal-50 transition-colors font-medium"
                          whileHover={{ scale: 1.05 }}
                          whileTap={{ scale: 0.95 }}
                        >
                          <span>🔗</span>
                          View Code
                        </motion.a>
                      )}
                      {project.links?.live && (
                        <motion.a
                          href={project.links.live}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center gap-2 px-6 py-3 bg-teal-600 text-white rounded-xl hover:bg-teal-700 transition-colors font-medium shadow-lg hover:shadow-xl"
                          whileHover={{ scale: 1.05 }}
                          whileTap={{ scale: 0.95 }}
                        >
                          <span>🚀</span>
                          Live Demo
                        </motion.a>
                      )}
                    </div>
                  </div>
                </motion.div>
              </CinematicSection>
            ))}
          </div>
        </div>
      </section>

      {/* === FINALE: THE INVITATION === */}
      <section className="py-32 lg:py-40 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-teal-25 to-teal-50 text-center">
        <div className="max-w-4xl mx-auto">
          <CinematicSection>
            <ParallaxText>
              <h2 className="text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight text-neutral-900 mb-8">
                Let's
                <br />
                <span className="bg-gradient-to-r from-teal-600 via-teal-500 to-teal-400 bg-clip-text text-transparent">
                  Connect
                </span>
              </h2>
            </ParallaxText>
            <p className="text-xl sm:text-2xl text-neutral-600 leading-relaxed max-w-3xl mx-auto mb-12">
              If something here resonates with you — a project, an approach, a shared curiosity — 
              I'd love to hear your thoughts. The best ideas emerge from conversation.
            </p>
            
            <div className="flex justify-center">
              <motion.a 
                href="mailto:renatodaprado@gmail.com" 
                className="inline-flex items-center justify-center px-12 py-6 border border-teal-300 text-lg font-semibold rounded-xl text-neutral-900 bg-white hover:bg-teal-50 hover:border-teal-400 transition-all duration-300 shadow-lg hover:shadow-xl"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <span className="mr-3">✉️</span>
                Reach Out
              </motion.a>
            </div>
          </CinematicSection>
        </div>
      </section>
    </main>
  );
}
