// app/software/page.tsx

import Button from "../components/button";

export default function Software() {
  return (
    <div className="space-y-32">
      {/* Hero Section */}
      <section className="relative flex flex-col items-center text-center pt-8 pb-16">
        <div className="max-w-4xl mx-auto space-y-8">
          <h1 className="text-5xl font-bold tracking-tight">Software</h1>
          <p className="text-xl text-neutral-600 max-w-2xl mx-auto leading-relaxed">
            Building systems that matter. From blockchain infrastructure to 
            full-stack applications, exploring the intersection of code and creativity.
          </p>
        </div>
      </section>

      {/* Featured Project - Accumulate Lite Client */}
      <section className="relative bg-gradient-to-b from-teal-50 to-white py-20 px-4 sm:px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-3xl font-bold tracking-tight">Featured Project</h2>
            <p className="text-neutral-600 text-lg max-w-2xl mx-auto">
              Deep dive into blockchain infrastructure and validation systems
            </p>
          </div>
          
          <div className="bg-white rounded-2xl overflow-hidden shadow-sm border border-gray-100">
            {/* Project Header */}
            <div className="p-8 border-b border-gray-100">
              <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
                <div className="space-y-2">
                  <h3 className="text-2xl font-bold">Accumulate Lite Client</h3>
                  <p className="text-teal-600 font-medium">Blockchain Infrastructure • Go, Protocol Buffers</p>
                </div>
                <div className="flex gap-3">
                  <Button href="#" variant="solid">View Code</Button>
                  <Button href="#" variant="outline">Live Demo</Button>
                </div>
              </div>
            </div>

            {/* Project Content */}
            <div className="p-8 space-y-8">
              <div className="prose prose-lg max-w-none">
                <p className="text-neutral-700 leading-relaxed">
                  A lightweight, secure blockchain validation client built for the future of 
                  distributed systems. The Accumulate Lite Client provides efficient block 
                  validation and state verification without requiring a full node setup.
                </p>
              </div>

              {/* Video Section */}
              <div className="space-y-4">
                <h4 className="text-lg font-semibold">Technical Deep Dive</h4>
                <div className="bg-gray-100 rounded-xl aspect-video flex items-center justify-center">
                  <div className="text-center space-y-3">
                    <div className="w-16 h-16 bg-teal-500 rounded-full flex items-center justify-center mx-auto">
                      <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clipRule="evenodd" />
                      </svg>
                    </div>
                    <p className="text-neutral-600">
                      [Video: Explaining the Accumulate Lite Client Architecture]
                    </p>
                    <p className="text-sm text-neutral-500">
                      Technical walkthrough and implementation details
                    </p>
                  </div>
                </div>
              </div>

              {/* Key Features */}
              <div className="grid md:grid-cols-2 gap-6">
                <div className="space-y-3">
                  <h4 className="text-lg font-semibold">Key Features</h4>
                  <ul className="space-y-2 text-neutral-700">
                    <li className="flex items-start space-x-2">
                      <span className="w-1.5 h-1.5 bg-teal-500 rounded-full mt-2 flex-shrink-0"></span>
                      <span>Lightweight block validation</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="w-1.5 h-1.5 bg-teal-500 rounded-full mt-2 flex-shrink-0"></span>
                      <span>Efficient state verification</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="w-1.5 h-1.5 bg-teal-500 rounded-full mt-2 flex-shrink-0"></span>
                      <span>Protocol buffer integration</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="w-1.5 h-1.5 bg-teal-500 rounded-full mt-2 flex-shrink-0"></span>
                      <span>Secure cryptographic validation</span>
                    </li>
                  </ul>
                </div>
                
                <div className="space-y-3">
                  <h4 className="text-lg font-semibold">Technologies</h4>
                  <div className="flex flex-wrap gap-2">
                    <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm">Go</span>
                    <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm">Protocol Buffers</span>
                    <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm">Blockchain</span>
                    <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm">Cryptography</span>
                    <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm">Distributed Systems</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Other Projects Grid */}
      <section className="py-20 px-4 sm:px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-3xl font-bold tracking-tight">Other Projects</h2>
            <p className="text-neutral-600 text-lg max-w-2xl mx-auto">
              A collection of applications, tools, and experiments across different domains
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Project Card 1 */}
            <div className="bg-white rounded-xl p-6 border border-gray-200 hover:shadow-lg transition-shadow">
              <div className="space-y-4">
                <div className="w-12 h-12 bg-teal-100 rounded-lg flex items-center justify-center">
                  <svg className="w-6 h-6 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
                <div>
                  <h3 className="text-lg font-semibold mb-2">[Project Name]</h3>
                  <p className="text-neutral-600 text-sm mb-3">
                    [Brief project description and key functionality]
                  </p>
                  <div className="flex flex-wrap gap-1 mb-4">
                    <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">Tech 1</span>
                    <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">Tech 2</span>
                  </div>
                  <div className="flex gap-2">
                    <Button href="#" variant="outline" className="text-xs px-3 py-1">Code</Button>
                    <Button href="#" variant="outline" className="text-xs px-3 py-1">Demo</Button>
                  </div>
                </div>
              </div>
            </div>

            {/* Project Card 2 */}
            <div className="bg-white rounded-xl p-6 border border-gray-200 hover:shadow-lg transition-shadow">
              <div className="space-y-4">
                <div className="w-12 h-12 bg-teal-100 rounded-lg flex items-center justify-center">
                  <svg className="w-6 h-6 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                  </svg>
                </div>
                <div>
                  <h3 className="text-lg font-semibold mb-2">[Web Application]</h3>
                  <p className="text-neutral-600 text-sm mb-3">
                    [Description of web application and its purpose]
                  </p>
                  <div className="flex flex-wrap gap-1 mb-4">
                    <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">React</span>
                    <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">Node.js</span>
                  </div>
                  <div className="flex gap-2">
                    <Button href="#" variant="outline" className="text-xs px-3 py-1">Code</Button>
                    <Button href="#" variant="outline" className="text-xs px-3 py-1">Live</Button>
                  </div>
                </div>
              </div>
            </div>

            {/* Project Card 3 */}
            <div className="bg-white rounded-xl p-6 border border-gray-200 hover:shadow-lg transition-shadow">
              <div className="space-y-4">
                <div className="w-12 h-12 bg-teal-100 rounded-lg flex items-center justify-center">
                  <svg className="w-6 h-6 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                  </svg>
                </div>
                <div>
                  <h3 className="text-lg font-semibold mb-2">[Tool/Utility]</h3>
                  <p className="text-neutral-600 text-sm mb-3">
                    [Description of tool or utility and its use case]
                  </p>
                  <div className="flex flex-wrap gap-1 mb-4">
                    <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">Python</span>
                    <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">CLI</span>
                  </div>
                  <div className="flex gap-2">
                    <Button href="#" variant="outline" className="text-xs px-3 py-1">Code</Button>
                    <Button href="#" variant="outline" className="text-xs px-3 py-1">Docs</Button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Technical Skills */}
      <section className="relative bg-black text-white py-20 px-4 sm:px-6">
        <div className="max-w-5xl mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-3xl font-bold tracking-tight">Technical Stack</h2>
            <p className="text-gray-300 text-lg max-w-2xl mx-auto">
              Languages, frameworks, and tools I work with regularly
            </p>
          </div>

          <div className="grid md:grid-cols-4 gap-8">
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-teal-400">Languages</h3>
              <ul className="space-y-2 text-gray-300 text-sm">
                <li>Go</li>
                <li>JavaScript/TypeScript</li>
                <li>Python</li>
                <li>Java</li>
                <li>C++</li>
              </ul>
            </div>
            
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-teal-400">Frontend</h3>
              <ul className="space-y-2 text-gray-300 text-sm">
                <li>React</li>
                <li>Next.js</li>
                <li>Tailwind CSS</li>
                <li>Vue.js</li>
              </ul>
            </div>
            
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-teal-400">Backend</h3>
              <ul className="space-y-2 text-gray-300 text-sm">
                <li>Node.js</li>
                <li>Express</li>
                <li>PostgreSQL</li>
                <li>MongoDB</li>
                <li>Redis</li>
              </ul>
            </div>
            
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-teal-400">Tools & Platforms</h3>
              <ul className="space-y-2 text-gray-300 text-sm">
                <li>Docker</li>
                <li>AWS</li>
                <li>Git</li>
                <li>Linux</li>
                <li>Protocol Buffers</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-20 px-4 sm:px-6 text-center">
        <div className="max-w-3xl mx-auto space-y-8">
          <h2 className="text-3xl font-bold tracking-tight">Explore More</h2>
          <p className="text-xl text-neutral-600 leading-relaxed">
            Interested in the technical details or want to collaborate on a project?
          </p>
          <div className="flex flex-col sm:flex-row justify-center items-center gap-4 pt-4">
            <Button href="https://github.com/renatodap" variant="solid">
              GitHub Profile
            </Button>
            <Button href="/professional" variant="outline">
              Professional Experience
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
}
