// app/professional/page.tsx

import Button from "../components/button";

export default function Professional() {
  return (
    <div className="space-y-32 bg-white text-black">
      {/* Hero Section */}
      <section className="relative flex flex-col items-center justify-center min-h-screen px-4 sm:px-6">
        <div className="absolute inset-0 bg-gradient-to-br from-teal-100/20 via-white to-rose-100/20" />
        <div className="relative max-w-6xl mx-auto text-center space-y-12">
          <div className="space-y-6">
            <h1 className="font-heading text-6xl sm:text-8xl font-bold tracking-tight">
              Professional
            </h1>
            <p className="font-body text-xl sm:text-2xl text-neutral-700 max-w-3xl mx-auto leading-relaxed">
              Crafting scalable solutions at the intersection of technology and innovation. From distributed systems to user experiences that matter.
            </p>
          </div>
          <div className="flex flex-col sm:flex-row gap-6 justify-center items-center pt-8">
            <Button href="#resume" variant="solid">
              View Resume
            </Button>
            <Button href="#experience" variant="outline">
              Explore Journey
            </Button>
          </div>
        </div>
      </section>

      {/* Resume Section */}
      <section id="resume" className="relative py-20 px-4 sm:px-6">
        <div className="max-w-5xl mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="font-heading text-4xl font-bold tracking-tight">Resume & Experience</h2>
            <p className="font-body text-neutral-600 text-lg max-w-2xl mx-auto">
              A comprehensive overview of my professional journey and technical expertise
            </p>
          </div>

          <div className="grid lg:grid-cols-2 gap-12">
            {/* Resume Download */}
            <div className="bg-white rounded-2xl p-8 border border-neutral-200 shadow">
              <div className="space-y-6">
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-teal-100 rounded-xl flex items-center justify-center">
                    <svg className="w-6 h-6 text-teal-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="font-heading text-xl font-semibold">Download Resume</h3>
                    <p className="text-neutral-500 text-sm">Latest version • Updated January 2025</p>
                  </div>
                </div>
                <p className="text-neutral-700 leading-relaxed">
                  Get the complete overview of my technical skills, work experience, and educational background in a clean, professional format.
                </p>
                <Button href="/resume.pdf" variant="solid" className="w-full">
                  Download PDF Resume
                </Button>
              </div>
            </div>

            {/* Quick Stats */}
            <div className="space-y-6">
              <div className="bg-white rounded-2xl p-6 border border-neutral-200 shadow">
                <h4 className="font-heading text-lg font-semibold mb-4">Quick Overview</h4>
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center">
                    <div className="font-heading text-2xl font-bold text-teal-600">4+</div>
                    <div className="text-neutral-500 text-sm">Years Experience</div>
                  </div>
                  <div className="text-center">
                    <div className="font-heading text-2xl font-bold text-teal-600">15+</div>
                    <div className="text-neutral-500 text-sm">Projects Built</div>
                  </div>
                  <div className="text-center">
                    <div className="font-heading text-2xl font-bold text-teal-600">8+</div>
                    <div className="text-neutral-500 text-sm">Technologies</div>
                  </div>
                  <div className="text-center">
                    <div className="font-heading text-2xl font-bold text-teal-600">2026</div>
                    <div className="text-neutral-500 text-sm">Graduation</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="relative py-20 px-4 sm:px-6">
        <div className="absolute inset-0 bg-gradient-to-br from-teal-100/20 via-white to-rose-100/20"></div>
        <div className="relative max-w-4xl mx-auto text-center space-y-8">
          <h2 className="font-heading text-4xl font-bold tracking-tight">Let's Build Something Amazing</h2>
          <p className="font-body text-xl text-neutral-700 leading-relaxed max-w-2xl mx-auto">
            Ready to collaborate on your next project? I'm always excited to work on challenging problems
            and create solutions that make a real impact.
          </p>
          <div className="flex flex-col sm:flex-row justify-center items-center gap-6 pt-8">
            <Button href="/software" variant="solid">
              View My Projects
            </Button>
            <Button href="mailto:contact@renatodap.com" variant="outline">
              Get In Touch
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
}
