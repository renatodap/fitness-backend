export default function Home() {
  return (
    <section className="text-center">
      <h1 className="text-4xl font-bold mb-4">Hey, I'm Renato DAP</h1>
      <p className="text-lg text-gray-600 max-w-xl mx-auto">
        I build tools and tell stories — at the intersection of logic, rhythm, and connection.
      </p>
      <div className="mt-8 space-x-4">
        <a
          href="/projects"
          className="bg-black text-white py-2 px-4 rounded hover:bg-gray-800"
        >
          View Projects
        </a>
        <a
          href="https://youtube.com/@renatodap"
          target="_blank"
          className="border border-black py-2 px-4 rounded hover:bg-gray-100"
        >
          Watch Videos
        </a>
      </div>
    </section>
  );
}
