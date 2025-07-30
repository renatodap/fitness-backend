'use client';

import UniversalHero from '@/app/components/shared/UniversalHero';
import { motion, useInView, useScroll, useTransform } from 'framer-motion';
import { useRef } from 'react';

// === CINEMATIC DATA STRUCTURES ===

const instrumentJourney = [
  {
    name: "Violin", essence: "First Voice", years: "15 years",
    story: "Where it all began. At seven, I held this wooden box and discovered I could make it sing. Every scratch, every screech, every breakthrough taught me that beauty lives on the other side of struggle.",
    philosophy: "The violin taught me that music is not about perfection—it's about truth."
  },
  {
    name: "Guitar", essence: "The Storyteller", years: "12 years", 
    story: "Six strings became my diary. From bedroom recordings to campfire circles, the guitar taught me that every song is a conversation waiting to happen.",
    philosophy: "In every chord progression lives a story. In every melody lives a memory."
  },
  {
    name: "Piano", essence: "The Architect", years: "10 years",
    story: "88 keys unlocked the mathematics of music. Here I learned that harmony isn't just sound—it's the art of making different voices sing together.",
    philosophy: "The piano showed me that complexity and simplicity can dance together beautifully."
  },
  {
    name: "Drums", essence: "The Heartbeat", years: "8 years",
    story: "Behind the kit, I discovered that rhythm isn't just about keeping time—it's about creating the space where magic happens.",
    philosophy: "Every song needs a pulse. Every story needs a rhythm."
  },
  {
    name: "Bass", essence: "The Foundation", years: "6 years",
    story: "Four strings that hold everything together. The bass taught me that sometimes the most important voice is the one you feel rather than hear.",
    philosophy: "True power comes from knowing when not to play."
  },
  {
    name: "Ukulele", essence: "Pure Joy", years: "4 years",
    story: "Four strings of sunshine. When music gets too serious, the ukulele reminds me why I started—for the simple, infectious joy of making sound.",
    philosophy: "Sometimes the smallest instruments carry the biggest smiles."
  }
];

const originalMusic = [
  {
    title: "Echoes of Tomorrow", featured: true,
    story: "Written during a sleepless night in college, this song captures the anxiety and hope of not knowing what comes next. It became my most personal piece.",
    platforms: [
      { name: "Spotify", url: "https://open.spotify.com/track/example", icon: "🎵", color: "bg-green-500" },
      { name: "Apple Music", url: "https://music.apple.com/track/example", icon: "🍎", color: "bg-gray-900" },
      { name: "YouTube", url: "https://youtube.com/watch?v=example", icon: "📺", color: "bg-red-500" }
    ]
  },
  {
    title: "Code & Coffee",
    story: "A love letter to late-night programming sessions. This instrumental piece blends acoustic guitar with subtle electronic elements—just like my life.",
    platforms: [
      { name: "Spotify", url: "https://open.spotify.com/track/example2", icon: "🎵", color: "bg-green-500" },
      { name: "Apple Music", url: "https://music.apple.com/track/example2", icon: "🍎", color: "bg-gray-900" },
      { name: "YouTube", url: "https://youtube.com/watch?v=example2", icon: "📺", color: "bg-red-500" }
    ]
  },
  {
    title: "Hometown Memories",
    story: "A nostalgic journey through childhood streets and forgotten dreams. This song took three years to finish because some stories need time to breathe.",
    platforms: [
      { name: "Spotify", url: "https://open.spotify.com/track/example3", icon: "🎵", color: "bg-green-500" },
      { name: "Apple Music", url: "https://music.apple.com/track/example3", icon: "🍎", color: "bg-gray-900" },
      { name: "YouTube", url: "https://youtube.com/watch?v=example3", icon: "📺", color: "bg-red-500" }
    ]
  }
];

const bestVideos = [
  {
    title: "Building My First Web App | 48-Hour Challenge",
    description: "Watch me code, debug, and deploy a full-stack application in two days. Raw, unfiltered development process with all the coffee breaks and breakthrough moments.",
    views: "127K", category: "Tech", url: "https://youtube.com/watch?v=example1", duration: "24:15"
  },
  {
    title: "Acoustic Sessions Vol. 1 | Original Songs",
    description: "An intimate performance of my original compositions. Just me, my guitar, and the stories that needed to be told.",
    views: "89K", category: "Music", url: "https://youtube.com/watch?v=example2", duration: "18:42"
  },
  {
    title: "The Art of Code Reviews | Developer Philosophy",
    description: "Why code reviews are about more than finding bugs—they're about building better teams and better software.",
    views: "156K", category: "Tech", url: "https://youtube.com/watch?v=example3", duration: "15:33"
  },
  {
    title: "Street Photography in São Paulo | Visual Stories",
    description: "Exploring the vibrant streets of my hometown through the lens. Every corner tells a story, every face holds a universe.",
    views: "73K", category: "Photography", url: "https://youtube.com/watch?v=example4", duration: "12:28"
  },
  {
    title: "From Idea to Algorithm | Problem-Solving Process",
    description: "Breaking down complex problems into elegant solutions. A deep dive into how I approach algorithmic thinking.",
    views: "203K", category: "Tech", url: "https://youtube.com/watch?v=example5", duration: "21:07"
  },
  {
    title: "Violin to Code | My Unexpected Journey",
    description: "How classical music training shaped my approach to software development. The surprising connections between composition and coding.",
    views: "94K", category: "Story", url: "https://youtube.com/watch?v=example6", duration: "16:54"
  }
];

const filmingHistory = [
  {
    period: "2008-2012", title: "The Curious Kid",
    description: "Armed with a basic digital camera, I started capturing family gatherings and school events. Every video was an experiment, every mistake a lesson.",
    milestone: "First camera", keyLearning: "Storytelling begins with curiosity"
  },
  {
    period: "2013-2016", title: "The Student Filmmaker", 
    description: "High school brought better equipment and bigger dreams. I made short films for class projects, learning that constraints breed creativity.",
    milestone: "First short film", keyLearning: "Limitations are creative catalysts"
  },
  {
    period: "2017-2019", title: "The Technical Explorer",
    description: "College years meant diving deep into editing software, color grading, and sound design. I discovered that post-production is where stories truly come alive.",
    milestone: "First professional edit", keyLearning: "Magic happens in the details"
  },
  {
    period: "2020-2022", title: "The Digital Storyteller",
    description: "The pandemic pushed me online. I learned to create compelling content for digital platforms, adapting cinematic techniques for shorter formats.",
    milestone: "First viral video", keyLearning: "Every platform has its own language"
  },
  {
    period: "2023-Present", title: "The Integrated Creator",
    description: "Now I blend my technical background with visual storytelling, creating content that bridges the gap between code and creativity.",
    milestone: "Tech + Film fusion", keyLearning: "The best stories connect different worlds"
  }
];

const photographyCollections = [
  { title: "Urban Symphonies", story: "Cities breathe in rhythms—morning rush, evening calm, the dance of light through glass and steel.", count: "47 images" },
  { title: "Human Connections", story: "In candid moments and genuine expressions, I find the universal language of being human.", count: "32 images" },
  { title: "Natural Compositions", story: "Every landscape tells a story of time, weather, and the quiet persistence of beauty.", count: "28 images" },
  { title: "Architectural Poetry", story: "Buildings are frozen music—each structure a composition of line, light, and intention.", count: "35 images" }
];

// === CINEMATIC COMPONENTS ===

function CinematicSection({ children, className = '', delay = 0 }: { children: React.ReactNode; className?: string; delay?: number }) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: '-50px' });
  
  return (
    <motion.div
      ref={ref}
      className={className}
      initial={{ opacity: 0, y: 60 }}
      animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 60 }}
      transition={{ duration: 1.2, ease: 'easeOut', delay }}
    >
      {children}
    </motion.div>
  );
}

function ParallaxText({ children, offset = 50 }: { children: React.ReactNode; offset?: number }) {
  const ref = useRef(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ['start end', 'end start']
  });
  const y = useTransform(scrollYProgress, [0, 1], [offset, -offset]);
  
  return (
    <motion.div ref={ref} style={{ y }}>
      {children}
    </motion.div>
  );
}

export default function CreatorPage() {
  return (
    <main className="relative w-full bg-white text-black overflow-x-hidden">
      {/* === OPENING FRAME === */}
      <UniversalHero
        theme="creator"
        title="Stories in Rhythm"
        subtitle="Where music meets motion, where code meets creativity, where every frame tells a truth."
        videoSrc="/guitar.mp4"
        mobileVideoSrc="/guitar.mp4"
      />

      {/* === ACT I: THE LANGUAGES I SPEAK === */}
      <section className="py-32 lg:py-40 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-7xl mx-auto">
          <CinematicSection className="text-center mb-24">
            <ParallaxText>
              <h2 className="text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight text-neutral-900 mb-8">
                Six Languages,
                <br />
                <span className="bg-gradient-to-r from-rose-600 via-rose-500 to-rose-400 bg-clip-text text-transparent">
                  One Voice
                </span>
              </h2>
            </ParallaxText>
            <p className="text-xl sm:text-2xl text-neutral-600 max-w-4xl mx-auto leading-relaxed">
              Each instrument taught me a different way to think, to feel, to express what words cannot capture.
            </p>
          </CinematicSection>

          <div className="space-y-32">
            {instrumentJourney.map((instrument, index) => (
              <CinematicSection key={instrument.name} delay={index * 0.2}>
                <motion.div
                  className={`flex flex-col lg:flex-row items-center gap-16 ${index % 2 === 1 ? 'lg:flex-row-reverse' : ''}`}
                  initial={{ opacity: 0, x: index % 2 === 0 ? -80 : 80 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  transition={{ duration: 1.4, ease: 'easeOut' }}
                  viewport={{ once: true, margin: '-100px' }}
                >
                  <div className="lg:w-1/2">
                    <div className="relative aspect-[4/3] bg-gradient-to-br from-rose-50 to-neutral-50 rounded-3xl overflow-hidden border border-rose-100 shadow-2xl group">
                      <div className="absolute inset-0 flex items-center justify-center">
                        <div className="text-rose-300 text-9xl opacity-30 group-hover:opacity-50 transition-opacity duration-500">♪</div>
                      </div>
                      <div className="absolute bottom-6 left-6 right-6">
                        <div className="bg-white/95 backdrop-blur-sm rounded-2xl p-4 border border-white/20 shadow-lg">
                          <p className="text-sm text-neutral-600 font-medium">{instrument.years} of stories</p>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="lg:w-1/2 space-y-8">
                    <div>
                      <div className="inline-flex items-center px-4 py-2 bg-rose-100 text-rose-800 text-sm font-semibold rounded-full mb-6 border border-rose-200">
                        {instrument.essence}
                      </div>
                      <h3 className="text-4xl sm:text-5xl font-bold text-neutral-900 mb-6">{instrument.name}</h3>
                    </div>
                    
                    <p className="text-lg text-neutral-600 leading-relaxed mb-8">
                      {instrument.story}
                    </p>
                    
                    <blockquote className="border-l-4 border-rose-300 pl-8 py-4 bg-rose-50/50 rounded-r-2xl">
                      <p className="italic text-neutral-700 text-lg font-medium">
                        "{instrument.philosophy}"
                      </p>
                    </blockquote>
                  </div>
                </motion.div>
              </CinematicSection>
            ))}
          </div>
        </div>
      </section>

      {/* === ACT II: ORIGINAL CREATIONS === */}
      <section className="py-32 lg:py-40 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-white to-rose-25">
        <div className="max-w-7xl mx-auto">
          <CinematicSection className="text-center mb-24">
            <ParallaxText>
              <h2 className="text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight text-neutral-900 mb-8">
                Original
                <br />
                <span className="bg-gradient-to-r from-rose-600 via-rose-500 to-rose-400 bg-clip-text text-transparent">
                  Creations
                </span>
              </h2>
            </ParallaxText>
            <p className="text-xl sm:text-2xl text-neutral-600 max-w-4xl mx-auto leading-relaxed">
              The songs that carry pieces of my soul, now available across all platforms.
            </p>
          </CinematicSection>

          {/* Featured Music Video */}
          <CinematicSection className="mb-20">
            <div className="max-w-5xl mx-auto">
              <div className="relative aspect-video bg-gradient-to-br from-neutral-900 to-neutral-700 rounded-3xl overflow-hidden shadow-2xl group">
                <div className="absolute inset-0 flex items-center justify-center">
                  <motion.div 
                    className="text-white text-8xl opacity-80 group-hover:opacity-100 transition-opacity cursor-pointer"
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    ▶
                  </motion.div>
                </div>
                <div className="absolute bottom-8 left-8 right-8">
                  <h3 className="text-white text-3xl font-bold mb-3">{originalMusic[0].title}</h3>
                  <p className="text-white/90 text-lg mb-4">{originalMusic[0].story}</p>
                  <div className="flex flex-wrap gap-3">
                    {originalMusic[0].platforms.map((platform) => (
                      <motion.a
                        key={platform.name}
                        href={platform.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className={`inline-flex items-center gap-2 px-4 py-2 ${platform.color} text-white rounded-full text-sm font-medium hover:opacity-90 transition-opacity`}
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                      >
                        <span>{platform.icon}</span>
                        {platform.name}
                      </motion.a>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </CinematicSection>

          {/* Other Tracks */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 max-w-6xl mx-auto">
            {originalMusic.slice(1).map((track, index) => (
              <motion.div
                key={track.title}
                className="bg-white rounded-2xl p-8 border border-rose-100 shadow-lg hover:shadow-xl transition-shadow"
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: index * 0.1 }}
                viewport={{ once: true }}
                whileHover={{ y: -4 }}
              >
                <h4 className="text-2xl font-bold text-neutral-900 mb-4">{track.title}</h4>
                <p className="text-neutral-600 mb-6 leading-relaxed">{track.story}</p>
                <div className="flex flex-wrap gap-2">
                  {track.platforms.map((platform) => (
                    <motion.a
                      key={platform.name}
                      href={platform.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-2 px-3 py-2 border border-neutral-200 rounded-full text-sm font-medium hover:border-rose-300 hover:bg-rose-50 transition-colors"
                      whileHover={{ scale: 1.05 }}
                    >
                      <span>{platform.icon}</span>
                      {platform.name}
                    </motion.a>
                  ))}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* === ACT III: YOUTUBE HIGHLIGHTS === */}
      <section className="py-32 lg:py-40 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-7xl mx-auto">
          <CinematicSection className="text-center mb-24">
            <ParallaxText>
              <h2 className="text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight text-neutral-900 mb-8">
                Best of
                <br />
                <span className="bg-gradient-to-r from-rose-600 via-rose-500 to-rose-400 bg-clip-text text-transparent">
                  YouTube
                </span>
              </h2>
            </ParallaxText>
            <p className="text-xl sm:text-2xl text-neutral-600 max-w-4xl mx-auto leading-relaxed">
              Curated highlights from my creative journey, spanning tech, music, and visual storytelling.
            </p>
          </CinematicSection>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {bestVideos.map((video, index) => (
              <motion.a
                key={video.title}
                href={video.url}
                target="_blank"
                rel="noopener noreferrer"
                className="group block"
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: index * 0.1 }}
                viewport={{ once: true }}
                whileHover={{ y: -4 }}
              >
                <div className="bg-white rounded-2xl overflow-hidden border border-neutral-200 shadow-lg group-hover:shadow-xl transition-all duration-300">
                  <div className="relative aspect-video bg-gradient-to-br from-neutral-100 to-neutral-50">
                    <div className="absolute inset-0 flex items-center justify-center">
                      <div className="text-neutral-400 text-6xl opacity-30 group-hover:opacity-80 transition-all duration-300">▶</div>
                    </div>
                    <div className="absolute top-4 left-4 right-4 flex justify-between items-start">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        video.category === 'Tech' ? 'bg-blue-100 text-blue-800' :
                        video.category === 'Music' ? 'bg-rose-100 text-rose-800' :
                        video.category === 'Photography' ? 'bg-purple-100 text-purple-800' :
                        'bg-neutral-100 text-neutral-800'
                      }`}>
                        {video.category}
                      </span>
                      <span className="bg-black/70 text-white px-2 py-1 rounded text-xs font-medium">
                        {video.duration}
                      </span>
                    </div>
                    <div className="absolute bottom-4 left-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                      <div className="text-white text-sm font-medium">{video.views} views</div>
                    </div>
                  </div>
                  
                  <div className="p-6">
                    <h4 className="text-lg font-bold text-neutral-900 mb-3 group-hover:text-rose-700 transition-colors">
                      {video.title}
                    </h4>
                    <p className="text-neutral-600 text-sm leading-relaxed">
                      {video.description}
                    </p>
                  </div>
                </div>
              </motion.a>
            ))}
          </div>
        </div>
      </section>

      {/* === ACT IV: FILMMAKING EVOLUTION === */}
      <section className="py-32 lg:py-40 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-rose-25 to-white">
        <div className="max-w-7xl mx-auto">
          <CinematicSection className="text-center mb-24">
            <ParallaxText>
              <h2 className="text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight text-neutral-900 mb-8">
                The Filmmaker's
                <br />
                <span className="bg-gradient-to-r from-rose-600 via-rose-500 to-rose-400 bg-clip-text text-transparent">
                  Evolution
                </span>
              </h2>
            </ParallaxText>
            <p className="text-xl sm:text-2xl text-neutral-600 max-w-4xl mx-auto leading-relaxed">
              From curious kid with a camera to integrated creator—the visual journey of learning to see.
            </p>
          </CinematicSection>

          <div className="space-y-20">
            {filmingHistory.map((era, index) => (
              <CinematicSection key={era.period} delay={index * 0.2}>
                <motion.div
                  className={`flex flex-col lg:flex-row items-center gap-16 ${index % 2 === 1 ? 'lg:flex-row-reverse' : ''}`}
                  initial={{ opacity: 0, y: 60 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 1.2, delay: index * 0.1 }}
                  viewport={{ once: true, margin: '-100px' }}
                >
                  <div className="lg:w-1/2">
                    <div className="relative aspect-[4/3] bg-gradient-to-br from-neutral-100 to-neutral-50 rounded-3xl overflow-hidden border border-neutral-200 shadow-2xl group">
                      <div className="absolute inset-0 flex items-center justify-center">
                        <div className="text-neutral-400 text-8xl opacity-40 group-hover:opacity-60 transition-opacity">🎥</div>
                      </div>
                      <div className="absolute bottom-6 left-6 right-6">
                        <div className="bg-white/95 backdrop-blur-sm rounded-2xl p-4 border border-white/20 shadow-lg">
                          <p className="text-sm font-semibold text-neutral-800">{era.milestone}</p>
                          <p className="text-xs text-neutral-600 mt-1">{era.period}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="lg:w-1/2 space-y-6">
                    <div>
                      <div className="inline-block px-4 py-2 bg-rose-100 text-rose-800 text-sm font-semibold rounded-full mb-4">
                        {era.period}
                      </div>
                      <h3 className="text-3xl sm:text-4xl font-bold text-neutral-900 mb-4">{era.title}</h3>
                    </div>
                    <p className="text-lg text-neutral-600 leading-relaxed mb-6">
                      {era.description}
                    </p>
                    <div className="bg-rose-50 border-l-4 border-rose-300 p-4 rounded-r-lg">
                      <p className="text-rose-800 font-medium text-sm">Key Learning:</p>
                      <p className="text-rose-700 italic">"{era.keyLearning}"</p>
                    </div>
                  </div>
                </motion.div>
              </CinematicSection>
            ))}
          </div>
        </div>
      </section>

      {/* === ACT V: PHOTOGRAPHY & FINALE === */}
      <section className="py-32 lg:py-40 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-7xl mx-auto">
          <CinematicSection className="text-center mb-24">
            <ParallaxText>
              <h2 className="text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight text-neutral-900 mb-8">
                Frozen
                <br />
                <span className="bg-gradient-to-r from-rose-600 via-rose-500 to-rose-400 bg-clip-text text-transparent">
                  Moments
                </span>
              </h2>
            </ParallaxText>
            <p className="text-xl sm:text-2xl text-neutral-600 max-w-4xl mx-auto leading-relaxed italic">
              "In stillness, I find motion. In silence, I hear the story."
            </p>
          </CinematicSection>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-32">
            {photographyCollections.map((collection, index) => (
              <motion.div
                key={collection.title}
                className="group relative aspect-square bg-gradient-to-br from-neutral-100 to-neutral-50 rounded-xl overflow-hidden border border-neutral-200 hover:border-rose-200 transition-all duration-300 cursor-pointer shadow-lg hover:shadow-xl"
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.8, delay: index * 0.1 }}
                viewport={{ once: true }}
                whileHover={{ scale: 1.02 }}
              >
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="text-neutral-400 text-6xl opacity-30">📸</div>
                </div>
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                  <div className="absolute bottom-6 left-6 right-6">
                    <h4 className="text-white font-bold text-lg mb-2">{collection.title}</h4>
                    <p className="text-white/80 text-sm italic mb-2">{collection.story}</p>
                    <p className="text-white/60 text-xs">{collection.count}</p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>

          {/* === FINALE: LET'S CREATE === */}
          <CinematicSection className="text-center">
            <ParallaxText>
              <h2 className="text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight text-neutral-900 mb-8">
                Let's Make Something
                <br />
                <span className="bg-gradient-to-r from-rose-600 via-rose-500 to-rose-400 bg-clip-text text-transparent">
                  Worth Remembering
                </span>
              </h2>
            </ParallaxText>
            <p className="text-xl sm:text-2xl text-neutral-600 leading-relaxed max-w-3xl mx-auto mb-12">
              Every story deserves to be told with intention, authenticity, and heart. 
              Ready to create something that matters?
            </p>
            
            <div className="flex flex-col sm:flex-row justify-center items-center gap-6">
              <motion.a 
                href="https://youtube.com/@renatodap" 
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center justify-center px-10 py-5 border border-transparent text-lg font-semibold rounded-xl text-white bg-neutral-900 hover:bg-neutral-800 transition-all duration-300 shadow-lg hover:shadow-xl"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                Watch My Journey
              </motion.a>
              <motion.a 
                href="mailto:renatodaprado@gmail.com" 
                className="inline-flex items-center justify-center px-10 py-5 border border-rose-300 text-lg font-semibold rounded-xl text-neutral-900 bg-white hover:bg-rose-50 hover:border-rose-400 transition-all duration-300 shadow-lg hover:shadow-xl"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                Let's Collaborate
              </motion.a>
            </div>
          </CinematicSection>
        </div>
      </section>
    </main>
  );
}
