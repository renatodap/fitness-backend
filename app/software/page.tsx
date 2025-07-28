// app/software/page.tsx

'use client';

import { projects } from './projects';
import { LegendaryHero } from '../components/software/LegendaryHero';
import { ProjectShowcase } from '../components/software/ProjectShowcase';

// Only show the most important projects in priority order
const priorityProjects = projects.slice(0, 7); // Top 7 most important

export default function SoftwarePage() {
  return (
    <main className="relative w-full bg-white text-black overflow-x-hidden">
      {/* Revolutionary Hero Section */}
      <LegendaryHero />

      {/* Story-Driven Project Showcases */}
      {priorityProjects.map((project, index) => (
        <ProjectShowcase 
          key={project.id} 
          project={project} 
          index={index}
        />
      ))}

      {/* Final Call to Action */}
      <section className="min-h-screen flex items-center justify-center bg-white border-t border-neutral-100">
        <div className="text-center space-y-12 px-6 sm:px-10 max-w-4xl mx-auto">
          <div className="space-y-6">
            <h2 className="text-5xl sm:text-6xl font-heading font-black text-neutral-900 leading-tight">
              Let's build something
              <br />
              <span className="bg-gradient-to-r from-teal-600 to-rose-600 bg-clip-text text-transparent">
                extraordinary
              </span>
            </h2>
            <p className="text-xl text-neutral-500 font-body font-light leading-relaxed max-w-2xl mx-auto">
              Every project tells a story of problem-solving, innovation, and growth. 
              Ready to see what we can create together?
            </p>
          </div>
          
          <div className="flex flex-col sm:flex-row justify-center gap-4 pt-8">
            <a 
              href="/professional" 
              className="px-8 py-4 bg-neutral-900 text-white font-heading font-medium rounded-lg hover:bg-neutral-800 transition-all duration-200 hover:scale-105"
            >
              View My Experience
            </a>
            <a 
              href="mailto:your-email@example.com" 
              className="px-8 py-4 border border-neutral-200 text-neutral-700 font-heading font-medium rounded-lg hover:bg-neutral-50 hover:border-neutral-300 transition-all duration-200"
            >
              Get In Touch
            </a>
          </div>
          
          {/* Subtle decorative element */}
          <div className="pt-16">
            <div className="w-24 h-px bg-gradient-to-r from-transparent via-neutral-300 to-transparent mx-auto"></div>
          </div>
        </div>
      </section>
    </main>
  );
}
