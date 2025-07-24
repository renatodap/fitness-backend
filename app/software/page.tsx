// app/software/page.tsx

import Button from "../components/button";

export default function Software() {
  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <section className="relative flex flex-col items-center text-center py-5">
        <div className="max-w-4xl mx-auto px-6 space-y-8">
          <h1 className="text-6xl font-bold tracking-tight">Software</h1>
          <p className="text-xl text-neutral-600 max-w-2xl mx-auto leading-relaxed">
            Building systems that matter. From blockchain infrastructure to full-stack applications, exploring the intersection of code and creativity.
          </p>
        </div>
      </section>

      {/* Featured Project - Accumulate Lite Client */}
      <section className="relative bg-gradient-to-b from-teal-50 to-white py-10 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-4xl font-bold tracking-tight">Featured Project</h2>
            <p className="text-neutral-600 text-xl max-w-2xl mx-auto">
              Deep dive into blockchain infrastructure and validation systems
            </p>
          </div>
          
          <div className="bg-white rounded-3xl overflow-hidden shadow-xl border border-gray-100">
            {/* Project Header */}
            <div className="p-10 border-b border-gray-100">
              <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y- lg:space-y-0">
                <div className="space-y-3">
                  <h3 className="text-3xl font-bold">Accumulate Lite Client</h3>
                  <p className="text-teal-600 font-medium text-lg">Blockchain Infrastructure • Go, Protocol Buffers</p>
                  <p className="text-sm text-neutral-500 font-medium">Summer 2024</p>
                </div>
              </div>
            </div>

            {/* Project Content */}
            <div className="p-10 space-y-10">
              <div className="prose prose-xl max-w-none">
                <p className="text-neutral-700 leading-relaxed text-lg">
                  A lightweight, secure blockchain validation client built for the future of distributed systems. The Accumulate Lite Client provides efficient block validation and state verification without requiring a full node setup. Developed as part of Genialt's KYA (Know Your Agent) identity framework for AI model traceability.
                </p>
              </div>

              {/* Video Section */}
              <div className="space-y-6">
                <h4 className="text-xl font-semibold">Building the Next Generation AI Deployment Platform with Blockchain</h4>
                <div className="relative w-full rounded-2xl overflow-hidden shadow-lg" style={{ paddingBottom: '56.25%' }}>
                  <iframe
                    className="absolute top-0 left-0 w-full h-full"
                    src="https://www.youtube.com/embed/mcVZXHcuO70"
                    title="Building the Next Generation AI Deployment Platform with Blockchain"
                    frameBorder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                    allowFullScreen
                  ></iframe>
                </div>
                <p className="text-neutral-500">
                  Explains the role of the Lite Client in cryptographic identity verification for AI agents.
                </p>
              </div>

              {/* Key Features */}
              <div className="grid md:grid-cols-2 gap-6">
                <div className="space-y-3">
                  <h4 className="text-lg font-semibold">Key Features</h4>
                  <ul className="space-y-2 text-neutral-700">
                    <li className="flex items-start space-x-2">
                      <svg className="w-5 h-5 text-teal-500 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                      <span>Lightweight block validation</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <svg className="w-5 h-5 text-teal-500 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                      <span>Efficient state verification</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <svg className="w-5 h-5 text-teal-500 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                      <span>Protocol buffer integration</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <svg className="w-5 h-5 text-teal-500 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                      <span>Secure cryptographic validation</span>
                    </li>
                  </ul>
                </div>
                
                <div className="space-y-3">
                  <h4 className="text-lg font-semibold">Technologies</h4>
                  <div className="flex flex-wrap gap-2">
                    <span className="px-3 py-1 bg-teal-100 text-teal-800 rounded-full text-sm font-medium">Go</span>
                    <span className="px-3 py-1 bg-teal-100 text-teal-800 rounded-full text-sm font-medium">Protocol Buffers</span>
                    <span className="px-3 py-1 bg-teal-100 text-teal-800 rounded-full text-sm font-medium">Blockchain</span>
                    <span className="px-3 py-1 bg-teal-100 text-teal-800 rounded-full text-sm font-medium">Cryptography</span>
                    <span className="px-3 py-1 bg-teal-100 text-teal-800 rounded-full text-sm font-medium">Distributed Systems</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Other Projects Grid */}
      <section className="py-6 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-4xl font-bold tracking-tight">Other Projects</h2>
            <p className="text-neutral-600 text-xl max-w-2xl mx-auto">
              A collection of applications, tools, and experiments across different domains
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Project 1: Digital Media Library Desktop App */}
            <div className="bg-white rounded-2xl p-8 border border-gray-200 hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
              <div className="space-y-6">
                <div className="w-14 h-14 bg-teal-100 rounded-xl flex items-center justify-center">
                  <svg className="w-7 h-7 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
                  </svg>
                </div>
                <div>
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="text-xl font-semibold">Digital Media Library Desktop App</h3>
                    <span className="text-sm text-neutral-500 font-medium">Fall 2023</span>
                  </div>
                  <p className="text-teal-600 text-sm font-medium mb-4">Cross-Platform Application • Python, PyQt5, SQL Server</p>
                  <p className="text-neutral-600 text-sm mb-4 leading-relaxed">
                    Built a desktop application for media storage and playback using Python and PyQt5. Implemented secure authentication, tabbed browsing UI, and robust CRUD operations with SQL Server stored procedures.
                  </p>
                  <div className="text-xs text-neutral-500 mb-4">
                    <span className="font-medium">Class:</span> CSSE333 — Database Systems | <span className="font-medium">Team:</span> Group of 3
                  </div>
                  <div className="flex flex-wrap gap-2">
                    <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-xs font-medium">Python</span>
                    <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-xs font-medium">PyQt5</span>
                    <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-xs font-medium">SQL Server</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Project 2: Game Tracker Web App */}
            <div className="bg-white rounded-2xl p-8 border border-gray-200 hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
              <div className="space-y-6">
                <div className="w-14 h-14 bg-teal-100 rounded-xl flex items-center justify-center">
                  <svg className="w-7 h-7 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                  </svg>
                </div>
                <div>
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="text-xl font-semibold">Game Tracker Web App</h3>
                    <span className="text-sm text-neutral-500 font-medium">Spring 2024</span>
                  </div>
                  <p className="text-teal-600 text-sm font-medium mb-4">Full-Stack Web App • React, JavaScript, HTML, CSS</p>
                  <p className="text-neutral-600 text-sm mb-4 leading-relaxed">
                    Developed a dynamic web application to track game sessions and display personalized stats. Integrated persistent client/server data flow and built with full frontend/backend separation.
                  </p>
                  <div className="text-xs text-neutral-500 mb-4">
                    <span className="font-medium">Class:</span> Front-End Web Development | <span className="font-medium">Team:</span> Group of 3
                  </div>
                  <div className="flex flex-wrap gap-2">
                    <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-xs font-medium">React</span>
                    <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-xs font-medium">JS</span>
                    <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-xs font-medium">CSS</span>
                    <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-xs font-medium">UX</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Project 3: Pipelined Processor Design */}
            <div className="bg-white rounded-2xl p-8 border border-gray-200 hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
              <div className="space-y-6">
                <div className="w-14 h-14 bg-teal-100 rounded-xl flex items-center justify-center">
                  <svg className="w-7 h-7 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
                  </svg>
                </div>
                <div>
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="text-xl font-semibold">Pipelined Processor Design</h3>
                    <span className="text-sm text-neutral-500 font-medium">Winter 2024</span>
                  </div>
                  <p className="text-teal-600 text-sm font-medium mb-4">Hardware Simulation • Verilog, RISC-V</p>
                  <p className="text-neutral-600 text-sm mb-4 leading-relaxed">
                    Designed a 5-stage pipelined RISC-V processor supporting branches, jumps, and memory instructions. Tested thoroughly using waveform analysis and Verilog testbenches.
                  </p>
                  <div className="text-xs text-neutral-500 mb-4">
                    <span className="font-medium">Class:</span> CSSE232 - Comp Arch I | <span className="font-medium">Team:</span> Team of 3
                  </div>
                  <div className="flex flex-wrap gap-2">
                    <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-xs font-medium">Verilog</span>
                    <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-xs font-medium">RISC-V</span>
                    <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-xs font-medium">Simulation</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Project 4: Java Linter & Static Analysis Tool */}
            <div className="bg-white rounded-2xl p-8 border border-gray-200 hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
              <div className="space-y-6">
                <div className="w-14 h-14 bg-teal-100 rounded-xl flex items-center justify-center">
                  <svg className="w-7 h-7 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                  </svg>
                </div>
                <div>
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="text-xl font-semibold">Java Linter & Static Analysis Tool</h3>
                    <span className="text-sm text-neutral-500 font-medium">Fall 2024</span>
                  </div>
                  <p className="text-teal-600 text-sm font-medium mb-4">Code Quality Engine • Java, Bytecode Analysis</p>
                  <p className="text-neutral-600 text-sm mb-4 leading-relaxed">
                    Created a configurable static analysis engine to enforce custom design rules, principles, and patterns for Java projects. Supported multi-file input, directory scanning, and extensible check definitions.
                  </p>
                  <div className="text-xs text-neutral-500 mb-4">
                    <span className="font-medium">Class:</span> CSSE374 — Software Design | <span className="font-medium">Team:</span> Team of 4
                  </div>
                  <div className="flex flex-wrap gap-2">
                    <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-xs font-medium">Java</span>
                    <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-xs font-medium">Linter</span>
                    <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-xs font-medium">Design Patterns</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Project 5: Placeholder Project */}
            <div className="bg-white rounded-2xl p-8 border border-gray-200 hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
              <div className="space-y-6">
                <div className="w-14 h-14 bg-gray-100 rounded-xl flex items-center justify-center">
                  <svg className="w-7 h-7 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                </div>
                <div>
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="text-xl font-semibold text-gray-400">[Project Title]</h3>
                    <span className="text-sm text-neutral-400 font-medium">[Duration]</span>
                  </div>
                  <p className="text-gray-400 text-sm font-medium mb-4">[Project Type] • [Technologies]</p>
                  <p className="text-gray-400 text-sm mb-4 leading-relaxed">
                    [Project description and key features will be added here]
                  </p>
                  <div className="text-xs text-gray-400 mb-4">
                    <span className="font-medium">Context:</span> [Class/Work/Personal] | <span className="font-medium">Team:</span> [Team Size]
                  </div>
                  <div className="flex flex-wrap gap-2">
                    <span className="px-3 py-1 bg-gray-50 text-gray-400 rounded-full text-xs font-medium">[Tech]</span>
                    <span className="px-3 py-1 bg-gray-50 text-gray-400 rounded-full text-xs font-medium">[Tech]</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Project 6: Placeholder Project */}
            <div className="bg-white rounded-2xl p-8 border border-gray-200 hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
              <div className="space-y-6">
                <div className="w-14 h-14 bg-gray-100 rounded-xl flex items-center justify-center">
                  <svg className="w-7 h-7 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                </div>
                <div>
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="text-xl font-semibold text-gray-400">[Project Title]</h3>
                    <span className="text-sm text-neutral-400 font-medium">[Duration]</span>
                  </div>
                  <p className="text-gray-400 text-sm font-medium mb-4">[Project Type] • [Technologies]</p>
                  <p className="text-gray-400 text-sm mb-4 leading-relaxed">
                    [Project description and key features will be added here]
                  </p>
                  <div className="text-xs text-gray-400 mb-4">
                    <span className="font-medium">Context:</span> [Class/Work/Personal] | <span className="font-medium">Team:</span> [Team Size]
                  </div>
                  <div className="flex flex-wrap gap-2">
                    <span className="px-3 py-1 bg-gray-50 text-gray-400 rounded-full text-xs font-medium">[Tech]</span>
                    <span className="px-3 py-1 bg-gray-50 text-gray-400 rounded-full text-xs font-medium">[Tech]</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Technical Stack */}
      <section className="relative bg-gradient-to-b from-gray-50 to-white py-16 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-4xl font-bold tracking-tight">Technical Stack</h2>
            <p className="text-neutral-600 text-xl max-w-2xl mx-auto">
              Languages, frameworks, and tools I work with regularly
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {/* Languages Card */}
            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-100 hover:shadow-xl transition-all duration-300">
              <div className="space-y-6">
                <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
                  <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                  </svg>
                </div>
                <div>
                  <h3 className="text-xl font-semibold mb-4">Languages</h3>
                  <div className="space-y-3">
                    <div className="flex flex-wrap gap-2">
                      <span className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm font-medium">Go</span>
                      <span className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm font-medium">Python</span>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      <span className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm font-medium">JavaScript</span>
                      <span className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm font-medium">Java</span>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      <span className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm font-medium">C++</span>
                      <span className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm font-medium">SQL</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Frontend Card */}
            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-100 hover:shadow-xl transition-all duration-300">
              <div className="space-y-6">
                <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
                  <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zM21 5a2 2 0 00-2-2h-4a2 2 0 00-2 2v12a4 4 0 004 4h4a2 2 0 002-2V5z" />
                  </svg>
                </div>
                <div>
                  <h3 className="text-xl font-semibold mb-4">Frontend</h3>
                  <div className="space-y-3">
                    <div className="flex flex-wrap gap-2">
                      <span className="px-3 py-1 bg-green-50 text-green-700 rounded-full text-sm font-medium">React</span>
                      <span className="px-3 py-1 bg-green-50 text-green-700 rounded-full text-sm font-medium">Next.js</span>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      <span className="px-3 py-1 bg-green-50 text-green-700 rounded-full text-sm font-medium">Tailwind CSS</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Backend Card */}
            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-100 hover:shadow-xl transition-all duration-300">
              <div className="space-y-6">
                <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center">
                  <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2" />
                  </svg>
                </div>
                <div>
                  <h3 className="text-xl font-semibold mb-4">Backend</h3>
                  <div className="space-y-3">
                    <div className="flex flex-wrap gap-2">
                      <span className="px-3 py-1 bg-purple-50 text-purple-700 rounded-full text-sm font-medium">Node.js</span>
                      <span className="px-3 py-1 bg-purple-50 text-purple-700 rounded-full text-sm font-medium">Express</span>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      <span className="px-3 py-1 bg-purple-50 text-purple-700 rounded-full text-sm font-medium">PostgreSQL</span>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      <span className="px-3 py-1 bg-purple-50 text-purple-700 rounded-full text-sm font-medium">SQL Server</span>
                      <span className="px-3 py-1 bg-purple-50 text-purple-700 rounded-full text-sm font-medium">Redis</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Tools Card */}
            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-100 hover:shadow-xl transition-all duration-300">
              <div className="space-y-6">
                <div className="w-12 h-12 bg-orange-100 rounded-xl flex items-center justify-center">
                  <svg className="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </div>
                <div>
                  <h3 className="text-xl font-semibold mb-4">Tools</h3>
                  <div className="space-y-3">
                    <div className="flex flex-wrap gap-2">
                      <span className="px-3 py-1 bg-orange-50 text-orange-700 rounded-full text-sm font-medium">Docker</span>
                      <span className="px-3 py-1 bg-orange-50 text-orange-700 rounded-full text-sm font-medium">AWS</span>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      <span className="px-3 py-1 bg-orange-50 text-orange-700 rounded-full text-sm font-medium">Git</span>
                      <span className="px-3 py-1 bg-orange-50 text-orange-700 rounded-full text-sm font-medium">Linux</span>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      <span className="px-3 py-1 bg-orange-50 text-orange-700 rounded-full text-sm font-medium">Protocol Buffers</span>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      <span className="px-3 py-1 bg-orange-50 text-orange-700 rounded-full text-sm font-medium">PyQt5</span>
                      <span className="px-3 py-1 bg-orange-50 text-orange-700 rounded-full text-sm font-medium">Verilog</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-4 px-6 text-center">
        <div className="max-w-4xl mx-auto space-y-8">
          <h2 className="text-4xl font-bold tracking-tight">Let's Build Something Together</h2>
          <p className="text-xl text-neutral-600 leading-relaxed max-w-2xl mx-auto">
            Interested in collaborating on a project, discussing technical ideas, or exploring opportunities? I'd love to connect.
          </p>
          <div className="flex flex-col sm:flex-row justify-center items-center gap-4 pt-4">
            <Button href="mailto:renatodaprado@gmail.com" variant="solid">
              Get in Touch
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
