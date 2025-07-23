// app/professional/page.tsx

import Button from "../components/button";

export default function Professional() {
  return (
    <div className="space-y-32">
      {/* Hero Section */}
      <section className="relative flex flex-col items-center text-center pt-8 pb-16">
        <div className="max-w-4xl mx-auto space-y-8">
          <h1 className="text-5xl font-bold tracking-tight">Professional</h1>
          <p className="text-xl text-neutral-600 max-w-2xl mx-auto leading-relaxed">
            Building at the intersection of technology and innovation. 
            From blockchain infrastructure to full-stack development.
          </p>
        </div>
      </section>

      {/* Current Role Section */}
      <section className="relative bg-gradient-to-b from-teal-50 to-white py-20 px-4 sm:px-6">
        <div className="max-w-5xl mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-3xl font-bold tracking-tight">Current Focus</h2>
            <p className="text-neutral-600 text-lg max-w-2xl mx-auto">
              What I'm building and contributing to right now
            </p>
          </div>
          
          <div className="bg-white rounded-2xl p-8 shadow-sm border border-gray-100">
            <div className="space-y-6">
              <div className="flex items-start justify-between">
                <div className="space-y-2">
                  <h3 className="text-2xl font-semibold">Software Engineer</h3>
                  <p className="text-teal-600 font-medium">[Company Name]</p>
                  <p className="text-neutral-500">[Duration] • [Location]</p>
                </div>
                <div className="text-right">
                  <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-teal-100 text-teal-800">
                    Current
                  </span>
                </div>
              </div>
              
              <div className="space-y-4">
                <p className="text-neutral-700 leading-relaxed">
                  [Brief description of current role and key responsibilities]
                </p>
                <div className="flex flex-wrap gap-2">
                  <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm">Technology Stack</span>
                  <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm">Key Skills</span>
                  <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm">Domain Expertise</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Experience Timeline */}
      <section className="py-20 px-4 sm:px-6">
        <div className="max-w-5xl mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-3xl font-bold tracking-tight">Experience</h2>
            <p className="text-neutral-600 text-lg max-w-2xl mx-auto">
              A timeline of professional growth and contributions
            </p>
          </div>

          <div className="space-y-12">
            {/* Experience Item 1 */}
            <div className="relative pl-8 border-l-2 border-gray-200">
              <div className="absolute w-4 h-4 bg-teal-500 rounded-full -left-2 top-0"></div>
              <div className="space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
                  <div>
                    <h3 className="text-xl font-semibold">[Position Title]</h3>
                    <p className="text-teal-600 font-medium">[Company Name]</p>
                  </div>
                  <p className="text-neutral-500 text-sm">[Duration]</p>
                </div>
                <p className="text-neutral-700 leading-relaxed">
                  [Description of role, key achievements, and impact]
                </p>
                <div className="flex flex-wrap gap-2">
                  <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">Skill 1</span>
                  <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">Skill 2</span>
                  <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">Skill 3</span>
                </div>
              </div>
            </div>

            {/* Experience Item 2 */}
            <div className="relative pl-8 border-l-2 border-gray-200">
              <div className="absolute w-4 h-4 bg-gray-400 rounded-full -left-2 top-0"></div>
              <div className="space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
                  <div>
                    <h3 className="text-xl font-semibold">[Previous Position]</h3>
                    <p className="text-teal-600 font-medium">[Previous Company]</p>
                  </div>
                  <p className="text-neutral-500 text-sm">[Duration]</p>
                </div>
                <p className="text-neutral-700 leading-relaxed">
                  [Description of previous role and key contributions]
                </p>
                <div className="flex flex-wrap gap-2">
                  <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">Technology</span>
                  <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">Achievement</span>
                </div>
              </div>
            </div>

            {/* Add more experience items as needed */}
          </div>
        </div>
      </section>

      {/* Skills & Expertise */}
      <section className="relative bg-black text-white py-20 px-4 sm:px-6">
        <div className="max-w-5xl mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-3xl font-bold tracking-tight">Core Expertise</h2>
            <p className="text-gray-300 text-lg max-w-2xl mx-auto">
              Technical skills and domain knowledge developed through hands-on experience
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="space-y-4">
              <h3 className="text-xl font-semibold text-teal-400">Development</h3>
              <ul className="space-y-2 text-gray-300">
                <li>[Programming Language 1]</li>
                <li>[Programming Language 2]</li>
                <li>[Framework/Technology]</li>
                <li>[Development Practice]</li>
              </ul>
            </div>
            
            <div className="space-y-4">
              <h3 className="text-xl font-semibold text-teal-400">Infrastructure</h3>
              <ul className="space-y-2 text-gray-300">
                <li>[Cloud Platform]</li>
                <li>[DevOps Tool]</li>
                <li>[Database Technology]</li>
                <li>[System Architecture]</li>
              </ul>
            </div>
            
            <div className="space-y-4">
              <h3 className="text-xl font-semibold text-teal-400">Specialization</h3>
              <ul className="space-y-2 text-gray-300">
                <li>[Domain Expertise 1]</li>
                <li>[Domain Expertise 2]</li>
                <li>[Industry Knowledge]</li>
                <li>[Specialized Skill]</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-20 px-4 sm:px-6 text-center">
        <div className="max-w-3xl mx-auto space-y-8">
          <h2 className="text-3xl font-bold tracking-tight">Let's Build Something</h2>
          <p className="text-xl text-neutral-600 leading-relaxed">
            Interested in collaborating or learning more about my work? 
            Let's connect and explore opportunities.
          </p>
          <div className="flex flex-col sm:flex-row justify-center items-center gap-4 pt-4">
            <Button href="/software" variant="solid">
              View Projects
            </Button>
            <Button href="mailto:contact@renatodap.com" variant="outline">
              Get in Touch
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
}
