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
      <section className="min-h-screen flex items-center justify-center bg-gradient-to-br from-neutral-50 via-white to-neutral-100">
        <div className="text-center space-y-8 px-6 sm:px-10">
          <h2 className="text-4xl sm:text-6xl font-heading font-black text-neutral-900">
            Ready to build something legendary?
          </h2>
          <p className="text-xl text-neutral-600 font-body max-w-2xl mx-auto">
            These projects represent my journey in software engineering. Each one taught me something new about building systems that scale, solve real problems, and make an impact.
          </p>
          <div className="flex flex-wrap justify-center gap-4 pt-8">
            <a 
              href="/professional" 
              className="px-8 py-4 bg-teal-500 text-white font-heading font-bold rounded-full hover:bg-teal-600 transition-colors"
            >
              View My Experience
            </a>
            <a 
              href="mailto:your-email@example.com" 
              className="px-8 py-4 border border-neutral-300 text-neutral-700 font-heading font-bold rounded-full hover:bg-neutral-100 transition-colors"
            >
              Let's Connect
            </a>
          </div>
        </div>
      </section>
    </main>
  );
}
