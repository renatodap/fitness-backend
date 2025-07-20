export default function Home() {
  return (
    <main className="min-h-screen bg-white px-6 py-12 text-black font-sans">
      <section className="max-w-4xl mx-auto text-center">
        <h1 className="text-5xl font-bold mb-4">
          Renato Dansieri
        </h1>
        <p className="text-xl text-gray-700 mb-8">
          I build tools and tell stories — at the intersection of logic, rhythm, and connection.
        </p>

        <div className="flex flex-col sm:flex-row justify-center gap-4 mb-12">
          <a href="/projects" className="px-6 py-3 border border-black rounded hover:bg-black hover:text-white transition">
            View Projects
          </a>
          <a href="/videos" className="px-6 py-3 border border-black rounded hover:bg-black hover:text-white transition">
            Watch Videos
          </a>
          <a href="/about" className="px-6 py-3 border border-black rounded hover:bg-black hover:text-white transition">
            About Me
          </a>
        </div>

        <div className="flex justify-center gap-6">
          <a href="https://www.youtube.com/c/RenatoDAP" target="_blank" rel="noopener noreferrer">
            <img src="/globe.svg" alt="YouTube" className="h-8" />
          </a>
          <a href="https://github.com/renatodap" target="_blank" rel="noopener noreferrer">
            <img src="/next.svg" alt="GitHub" className="h-8" />
          </a>
          <a href="mailto:renatodaprado@gmail.com">
            <img src="/file.svg" alt="Email" className="h-8" />
          </a>
        </div>
      </section>
    </main>
  )
}
