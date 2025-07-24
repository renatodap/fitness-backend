// app/about/page.tsx

import Button from "../components/button";

export default function About() {
  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <section className="relative w-full flex flex-col items-center text-center pt-0 pb-0 mb-16">
        <div className="w-full h-64 md:h-96 relative mb-8">
          <img
            src="/about-picture.jpg"
            alt="Renato DAP portrait"
            className="object-cover w-full h-full rounded-none shadow-lg"
            style={{ maxHeight: '40rem', objectPosition: '50% 45%' }}
          />
        </div>
        <div className="max-w-4xl mx-auto space-y-6">
          <h1 className="text-5xl font-bold tracking-tight">Software Engineer & Creative Mind</h1>
          <p className="text-xl text-neutral-700 max-w-3xl mx-auto leading-relaxed">
            I'm a Computer Science student at Rose-Hulman, focused on building software tools
            that solve real problems, producing music and video that tell meaningful stories,
            and leading as captain of the men's varsity tennis team. I work across code, creativity,
            and competition—always looking to make things that matter.
          </p>
        </div>
      </section>

      {/* What I Do */}
      <section className="py-16 px-4 sm:px-6 bg-teal-50 border-t border-teal-100 mb-16">
        <div className="max-w-4xl mx-auto">
          <div className="text-center space-y-4 mb-12">
            <h2 className="text-4xl font-bold tracking-tight">What I Do</h2>
            <p className="text-neutral-600 text-lg max-w-2xl mx-auto">
              Four core areas where I invest my time and energy
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Software Card */}
            <div className="flex flex-col items-center bg-white border border-neutral-200 rounded-xl p-8 shadow-sm hover:shadow-lg transition min-h-[280px]">
              <div className="mb-4">
                <div className="bg-teal-200 rounded-lg flex items-center justify-center w-12 h-12">
                  <span className="text-black text-xl font-mono">{'</>'}</span>
                </div>
              </div>
              <h3 className="text-lg font-semibold mb-2">Software</h3>
              <p className="text-sm text-neutral-600 mb-4 text-center flex-1">Building blockchain infrastructure, web applications, and tools that solve real problems</p>
              <Button href="/software" variant="outline" className="w-full mt-auto">View Projects</Button>
            </div>
            {/* Music Card */}
            <div className="flex flex-col items-center bg-white border border-neutral-200 rounded-xl p-8 shadow-sm hover:shadow-lg transition min-h-[280px]">
              <div className="mb-4">
                <span className="text-black text-3xl">🎵</span>
              </div>
              <h3 className="text-lg font-semibold mb-2">Music</h3>
              <p className="text-sm text-neutral-600 mb-4 text-center flex-1">Multi-instrumentalist creating original music and covers across drums, guitar, piano, and more</p>
              <Button href="/music" variant="outline" className="w-full mt-auto">Listen Now</Button>
            </div>
            {/* Photo & Video Card */}
            <div className="flex flex-col items-center bg-white border border-neutral-200 rounded-xl p-8 shadow-sm hover:shadow-lg transition min-h-[280px]">
              <div className="mb-4">
                <span className="text-black text-3xl">🎥</span>
              </div>
              <h3 className="text-lg font-semibold mb-2">Photo & Video</h3>
              <p className="text-sm text-neutral-600 mb-4 text-center flex-1">Photography portfolio and video creation showcasing technical and creative skills</p>
              <Button href="/photo" variant="outline" className="w-full mt-auto">View Portfolio</Button>
            </div>
            {/* Tennis Card */}
            <div className="flex flex-col items-center bg-white border border-neutral-200 rounded-xl p-8 shadow-sm hover:shadow-lg transition min-h-[280px]">
              <div className="mb-4">
                <span className="text-black text-3xl">⚡</span>
              </div>
              <h3 className="text-lg font-semibold mb-2">Tennis</h3>
              <p className="text-sm text-neutral-600 mb-4 text-center flex-1">Team captain of Rose-Hulman Men's Tennis, leading through competitive excellence</p>
              <Button href="/tennis" variant="outline" className="w-full mt-auto">Athletic Journey</Button>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-16 px-4 sm:px-6 text-center">
        <div className="max-w-3xl mx-auto space-y-8">
          <h2 className="text-3xl font-bold tracking-tight">Let's Connect</h2>
          <p className="text-xl text-neutral-600 leading-relaxed">
            Interested in collaborating, discussing ideas, or just saying hello? I'd love to hear from you.
          </p>
          <div className="flex flex-row justify-center items-center gap-6 pt-4">
            <a href="https://linkedin.com/in/renatodap" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn">
              <svg className="w-7 h-7 text-black hover:text-teal-600 transition" fill="currentColor" viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.761 0 5-2.239 5-5v-14c0-2.761-2.239-5-5-5zm-11 19h-3v-10h3v10zm-1.5-11.268c-.966 0-1.75-.784-1.75-1.75s.784-1.75 1.75-1.75 1.75.784 1.75 1.75-.784 1.75-1.75 1.75zm13.5 11.268h-3v-5.604c0-1.337-.025-3.063-1.868-3.063-1.869 0-2.156 1.459-2.156 2.967v5.7h-3v-10h2.881v1.367h.041c.401-.761 1.381-1.563 2.841-1.563 3.041 0 3.602 2.002 3.602 4.604v5.592z" /></svg>
            </a>
            <a href="https://open.spotify.com/artist/3VZ8V9XhQ9oZb5XnZ9g8yB" target="_blank" rel="noopener noreferrer" aria-label="Spotify">
              <svg className="w-7 h-7 text-black hover:text-teal-600 transition" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0C5.371 0 0 5.371 0 12s5.371 12 12 12 12-5.371 12-12S18.629 0 12 0zm5.363 17.463c-.221.364-.691.482-1.055.262-2.891-1.764-6.543-2.16-10.824-1.18-.418.096-.844-.162-.94-.576-.096-.418.162-.844.576-.94 4.663-1.08 8.727-.641 11.947 1.262.364.22.482.69.262 1.055zm1.504-2.67c-.276.447-.854.59-1.301.314-3.309-2.04-8.362-2.635-12.284-1.44-.51.158-1.055-.117-1.213-.627-.158-.51.117-1.055.627-1.213 4.406-1.361 9.927-.709 13.722 1.578.447.276.59.854.314 1.301zm.146-2.835C15.06 9.684 8.924 9.5 5.934 10.384c-.623.182-1.283-.159-1.464-.783-.181-.624.159-1.283.783-1.464 3.417-.99 10.184-.785 14.047 2.016.527.389.642 1.135.254 1.662-.389.527-1.135.643-1.662.254z" /></svg>
            </a>
            <a href="https://www.youtube.com/@RenatoDAP" target="_blank" rel="noopener noreferrer" aria-label="YouTube">
              <svg className="w-7 h-7 text-black hover:text-teal-600 transition" fill="currentColor" viewBox="0 0 24 24"><path d="M23.498 6.186a2.994 2.994 0 0 0-2.112-2.117C19.257 3.5 12 3.5 12 3.5s-7.257 0-9.386.569A2.994 2.994 0 0 0 .502 6.186C0 8.313 0 12 0 12s0 3.687.502 5.814a2.994 2.994 0 0 0 2.112 2.117C4.743 20.5 12 20.5 12 20.5s7.257 0 9.386-.569a2.994 2.994 0 0 0 2.112-2.117C24 15.687 24 12 24 12s0-3.687-.502-5.814zM9.75 15.5v-7l6.5 3.5-6.5 3.5z" /></svg>
            </a>
          </div>
          <div className="flex flex-col sm:flex-row justify-center items-center gap-4 pt-6">
            <Button href="/professional" variant="solid">
              Professional Experience
            </Button>
            <Button href="mailto:renatodaprado@gmail.com" variant="outline">
              Get in Touch
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
}