// app/about/page.tsx

import Button from "../components/button";

export default function About() {
  return (
    <div className="space-y-32">
      {/* Hero Section */}
      <section className="relative flex flex-col items-center text-center pt-8 pb-16">
        <div className="max-w-4xl mx-auto space-y-8">
          <h1 className="text-5xl font-bold tracking-tight">About</h1>
          <p className="text-xl text-neutral-600 max-w-2xl mx-auto leading-relaxed">
            A polymath exploring the intersection of code, music, video, and sports. 
            Building systems that matter while creating art that resonates.
          </p>
        </div>
      </section>

      {/* Introduction */}
      <section className="relative bg-gradient-to-b from-teal-50 to-white py-20 px-4 sm:px-6">
        <div className="max-w-4xl mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-3xl font-bold tracking-tight">Hello, I'm Renato</h2>
            <p className="text-neutral-600 text-lg max-w-2xl mx-auto">
              Where logic meets rhythm, and connection bridges creativity
            </p>
          </div>
          
          <div className="prose prose-lg max-w-none text-neutral-700 leading-relaxed space-y-6">
            <p>
              I'm a computer science student at Rose-Hulman Institute of Technology, 
              class of 2026, where I balance rigorous academics with creative pursuits 
              and athletic leadership as the men's tennis team captain.
            </p>
            
            <p>
              My work spans from blockchain infrastructure development to music creation 
              across multiple instruments. I believe in building systems that solve real 
              problems while exploring the creative potential of technology.
            </p>
            
            <p>
              Whether I'm developing a lightweight blockchain client, recording a new 
              cover song, editing a video, or leading my tennis team, I approach each 
              endeavor with the same curiosity and commitment to excellence.
            </p>
          </div>
        </div>
      </section>

      {/* Core Areas */}
      <section className="py-20 px-4 sm:px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-3xl font-bold tracking-tight">What I Do</h2>
            <p className="text-neutral-600 text-lg max-w-2xl mx-auto">
              Four core areas where I invest my time and energy
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {/* Software */}
            <div className="text-center space-y-4">
              <div className="w-16 h-16 bg-teal-100 rounded-2xl flex items-center justify-center mx-auto">
                <svg className="w-8 h-8 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold">Software</h3>
              <p className="text-sm text-neutral-600">
                Building blockchain infrastructure, web applications, and tools that solve real problems
              </p>
              <Button href="/software" variant="outline" className="text-xs px-3 py-1">
                View Projects
              </Button>
            </div>
            
            {/* Music */}
            <div className="text-center space-y-4">
              <div className="w-16 h-16 bg-teal-100 rounded-2xl flex items-center justify-center mx-auto">
                <svg className="w-8 h-8 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold">Music</h3>
              <p className="text-sm text-neutral-600">
                Multi-instrumentalist creating original music and covers across drums, guitar, piano, and more
              </p>
              <Button href="/music" variant="outline" className="text-xs px-3 py-1">
                Listen Now
              </Button>
            </div>
            
            {/* Video */}
            <div className="text-center space-y-4">
              <div className="w-16 h-16 bg-teal-100 rounded-2xl flex items-center justify-center mx-auto">
                <svg className="w-8 h-8 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold">Photo & Video</h3>
              <p className="text-sm text-neutral-600">
                Photography portfolio and video creation showcasing technical and creative skills
              </p>
              <Button href="/photo" variant="outline" className="text-xs px-3 py-1">
                View Portfolio
              </Button>
            </div>
            
            {/* Tennis */}
            <div className="text-center space-y-4">
              <div className="w-16 h-16 bg-teal-100 rounded-2xl flex items-center justify-center mx-auto">
                <svg className="w-8 h-8 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold">Tennis</h3>
              <p className="text-sm text-neutral-600">
                Team captain of Rose-Hulman Men's Tennis, leading through competitive excellence
              </p>
              <Button href="/tennis" variant="outline" className="text-xs px-3 py-1">
                Athletic Journey
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Philosophy */}
      <section className="relative bg-black text-white py-20 px-4 sm:px-6">
        <div className="max-w-4xl mx-auto text-center space-y-8">
          <h2 className="text-3xl font-bold tracking-tight">Philosophy</h2>
          <div className="space-y-6 text-lg text-gray-300 leading-relaxed">
            <p>
              "True innovation happens at the intersection of disciplines. 
              The rhythm I find in music informs the patterns I see in code. 
              The strategic thinking from tennis shapes how I approach complex problems."
            </p>
            <p>
              "I believe in building things that matter—whether it's a piece of software 
              that solves a real problem, a song that resonates with someone, or 
              leading a team to achieve something greater than the sum of its parts."
            </p>
          </div>
        </div>
      </section>

      {/* Current Focus */}
      <section className="py-20 px-4 sm:px-6">
        <div className="max-w-4xl mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-3xl font-bold tracking-tight">What I'm Building Now</h2>
            <p className="text-neutral-600 text-lg max-w-2xl mx-auto">
              Current projects and areas of focus
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-gradient-to-br from-teal-50 to-blue-50 rounded-2xl p-6">
              <h3 className="text-xl font-semibold mb-3">Technical</h3>
              <ul className="space-y-2 text-neutral-700">
                <li>• Accumulate Lite Client development</li>
                <li>• Full-stack web applications</li>
                <li>• Blockchain infrastructure research</li>
                <li>• Open source contributions</li>
              </ul>
            </div>
            
            <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl p-6">
              <h3 className="text-xl font-semibold mb-3">Creative</h3>
              <ul className="space-y-2 text-neutral-700">
                <li>• New music releases on Spotify</li>
                <li>• YouTube video production</li>
                <li>• Photography projects</li>
                <li>• Tennis team leadership</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-20 px-4 sm:px-6 text-center">
        <div className="max-w-3xl mx-auto space-y-8">
          <h2 className="text-3xl font-bold tracking-tight">Let's Connect</h2>
          <p className="text-xl text-neutral-600 leading-relaxed">
            Interested in collaborating, discussing ideas, or just saying hello? 
            I'd love to hear from you.
          </p>
          <div className="flex flex-col sm:flex-row justify-center items-center gap-4 pt-4">
            <Button href="/professional" variant="solid">
              Professional Experience
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
