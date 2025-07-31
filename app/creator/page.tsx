'use client';

import UniversalHero from '@/app/components/shared/UniversalHero';
import { motion, useInView, useScroll, useTransform } from 'framer-motion';
import { useRef, useEffect, useState } from 'react';
import Image from 'next/image';

// === CINEMATIC DATA STRUCTURES ===

const instrumentJourney = [
  {
    name: "Guitar", essence: "The Entry Point", years: "13 years", 
    image: "/guitar.jpg",
    story: "My entry point to music at 9 years old. Through experimenting with this instrument, I learned most of the fundamental music theory I know now. It's the one I can express myself the best with—six strings that became my voice before I found my actual voice.",
    philosophy: "Every musician needs that first door into the world of sound. Guitar was mine."
  },
  {
    name: "Piano", essence: "The Spark", years: "Since childhood",
    image: "/piano.jpg",
    story: "There was an old piano at my grandma's house in the countryside of Brazil, in Dracena. And another at my grandpa's farm in Minas Gerais. I used to play with them since I was very young—maybe 3 or 4 years old—even though I knew nothing about how they worked. It definitely sparked my interest in music. Throughout my life, I kept trying to replicate my guitar knowledge to piano until I decided to actually learn some of it during COVID.",
    philosophy: "Sometimes the most profound connections happen before we understand what we're connecting to."
  },
  {
    name: "Drums", essence: "The Dream", years: "4 years",
    image: "/drums.JPG",
    story: "Man, I always wanted to play drums but it's one of those dreams I never thought would come true. And it did. Maybe. I'm not very good. But although most of the time playing drums is just hitting some stuff, it taught me a sense of rhythm that translates to how I listen to and play music and how I live life. I'm not very good at drums, but the kind of loose connection and passion I feel for it is unmatched.",
    philosophy: "Sometimes it's not about being good—it's about the rhythm you find in your soul."
  },
  {
    name: "Bass", essence: "The Missing Piece", years: "4 years",
    image: "/bass.jpg",
    story: "Every guitarist can play bass until they try to play bass. And I'm glad I tried. My luck is I studied some classical guitar during COVID, so when I picked up the bass, the technique for plucking strings was actually somewhat similar. But in all seriousness, it felt like the missing piece for me to feel like a full band, and I'm glad I took the time to practice. Even though I already loved playing basslines on guitar before I bought my own.",
    philosophy: "The foundation isn't flashy, but without it, everything else falls apart."
  },
  {
    name: "Singing", essence: "The Discovery", years: "1 year (still learning!)",
    image: "/singing.jpg",
    story: "OK, this one even more than drums—I thought I would never be good at singing ever. And now I'm certain about it. Jokes aside, expressing myself through my voice has been my discovery of the last year. Even though I'm still at the very beginning of my vocal journey, it brings me so much joy.",
    philosophy: "The most vulnerable instrument is your own voice, but it's also the most honest."
  },
  {
    name: "Harmonica", essence: "The Question Mark", years: "Occasional",
    image: "/harmonica.jpg",
    story: "I don't actually play harmonica except a few songs here and there. But how hard is harmonica anyway? It's that instrument that sits in your pocket, waiting for the perfect campfire moment or quiet evening when you just want to make some sound without thinking too hard about it.",
    philosophy: "Not every instrument needs to be mastered—some just need to be enjoyed."
  },
  {
    name: "Ukulele", essence: "The Connector", years: "2 years",
    image: "/ukulele.jpg",
    story: "I bought it during a trip to Florida, and it was a highlight of the trip for me—playing with friends, meeting new people, and playing for them. It became my portable way to connect with people through music. Four strings of instant friendship.",
    philosophy: "The best instruments are the ones that bring people together."
  }
];

const originalMusic = [
  {
    title: "Be Aware", 
    type: "Single", 
    year: "2020",
    featured: true,
    hasVideo: true,
    cover: "/be-aware.webp",
    essence: "Sometimes the best way to express a feeling is through composing music—and it doesn't always come easy, especially with 10,000 other occupations.",
    platforms: [
      { name: "Spotify", url: "https://open.spotify.com/album/78YPuJu8EM9hR32tukVQh3", icon: "🎵", color: "bg-green-500" },
      { name: "Apple Music", url: "https://music.apple.com/br/album/be-aware-single/1525671917", icon: "🍎", color: "bg-gray-900" },
      { name: "Watch Video", url: "https://www.youtube.com/watch?v=012eud4qjHE", icon: "📺", color: "bg-red-500" }
    ]
  },
  {
    title: "Achilles Trilogy", 
    type: "EP", 
    year: "2021-2022",
    featured: true,
    cover: "/achilles.jpg",
    essence: "A three-part journey through sound—orchestral arrangements, guitar solos, piano, drums, bass. My favorite is Achilles II.",
    favoriteTrack: {
      name: "Achilles II",
      description: "Features a sweeping orchestra section (MIDI), intricate guitar solos, and layered instrumentation.",
      spotifyUrl: "https://open.spotify.com/track/5HTADgrwluGLT6afFzzDhk?si=9c3c45e868764c54",
      youtubeUrl: "https://m.youtube.com/watch?v=FsTZcHcS6Jc"
    },
    platforms: [
      { name: "Spotify", url: "https://open.spotify.com/album/6OItgP0pqkhhrKn0BRer0b", icon: "🎵", color: "bg-green-500" },
      { name: "Apple Music", url: "https://music.apple.com/br/album/achilles-trilogy-single/1604464244", icon: "🍎", color: "bg-gray-900" },
      { name: "YouTube Music", url: "https://m.youtube.com/playlist?list=OLAK5uy_mh1aVOb3eOiKEF7ZTSHmbTt6Nr3iffT1g", icon: "📺", color: "bg-red-500" }
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
  const [isClient, setIsClient] = useState(false);
  
  useEffect(() => {
    setIsClient(true);
  }, []);
  
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ['start end', 'end start']
  });
  const y = useTransform(scrollYProgress, [0, 1], [offset, -offset]);
  
  if (!isClient) {
    return (
      <div ref={ref}>
        {children}
      </div>
    );
  }
  
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
        videoSrc="/creator.mp4"
        mobileVideoSrc="/creator.mp4"
      />

      {/* === ACT I: THE LANGUAGES I SPEAK === */}
      <section className="py-12 sm:py-18 lg:py-24 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-6xl mx-auto">
          <CinematicSection className="text-center mb-16 sm:mb-20">
            <ParallaxText>
              <h2 className="text-2xl sm:text-3xl lg:text-4xl xl:text-5xl font-bold tracking-tight text-neutral-900 mb-5">
                Six Languages,
                <br />
                <span className="bg-gradient-to-r from-rose-600 via-rose-500 to-rose-400 bg-clip-text text-transparent">
                  One Voice
                </span>
              </h2>
            </ParallaxText>
            <p className="text-base sm:text-lg lg:text-xl text-neutral-600 max-w-2xl mx-auto leading-relaxed">
              Each instrument taught me a different way to think, to feel, to express what words cannot capture.
            </p>
          </CinematicSection>

          <div className="space-y-16 sm:space-y-20 lg:space-y-24">
            {instrumentJourney.map((instrument, index) => (
              <CinematicSection key={instrument.name} delay={index * 0.1}>
                <motion.div
                  className={`flex flex-col lg:flex-row items-center gap-8 sm:gap-12 lg:gap-16 ${index % 2 === 1 ? 'lg:flex-row-reverse' : ''}`}
                  initial={{ opacity: 0, y: 40 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.8, ease: [0.25, 0.1, 0.25, 1] }}
                  viewport={{ once: true, margin: '-50px' }}
                >
                  <div className="w-full lg:w-1/2">
                    <div className="relative aspect-[4/3] bg-gradient-to-br from-rose-50 to-neutral-50 rounded-2xl lg:rounded-3xl overflow-hidden border border-rose-100 shadow-xl group hover:shadow-2xl transition-shadow duration-500">
                      {instrument.image ? (
                        <>
                          <Image 
                            src={instrument.image} 
                            alt={`${instrument.name} - ${instrument.essence}`}
                            fill
                            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                            className="object-cover group-hover:scale-105 transition-transform duration-700"
                            priority={index < 2}
                          />
                          <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-60 group-hover:opacity-40 transition-opacity duration-500"></div>
                        </>
                      ) : (
                        <div className="absolute inset-0 flex items-center justify-center">
                          <div className="text-rose-300 text-9xl opacity-30 group-hover:opacity-50 transition-opacity duration-500">♪</div>
                        </div>
                      )}
                      <div className="absolute bottom-6 left-6 right-6">
                        <div className="bg-white/95 backdrop-blur-sm rounded-2xl p-4 border border-white/20 shadow-lg">
                          <p className="text-sm text-neutral-600 font-medium">{instrument.years} of stories</p>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="w-full lg:w-1/2 space-y-5 lg:space-y-6">
                    <div>
                      <div className="inline-flex items-center px-3 py-1.5 sm:px-4 sm:py-2 bg-rose-100 text-rose-800 text-xs sm:text-sm font-semibold rounded-full mb-3 sm:mb-4 border border-rose-200 hover:bg-rose-200 transition-colors duration-300">
                        {instrument.essence}
                      </div>
                      <h3 className="text-xl sm:text-2xl lg:text-3xl font-bold text-neutral-900 mb-3 sm:mb-4">{instrument.name}</h3>
                    </div>
                    
                    <p className="text-base text-neutral-600 leading-relaxed mb-6">
                      {instrument.story}
                    </p>
                    
                    <blockquote className="border-l-4 border-rose-300 pl-6 py-3 bg-rose-50/50 rounded-r-2xl">
                      <p className="italic text-neutral-700 text-sm font-medium">
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
      {/* === ACT II: ORIGINAL MUSIC === */}
      <section className="py-32 lg:py-40 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-white to-rose-25">
        <div className="max-w-7xl mx-auto">
          <CinematicSection className="text-center mb-24">
            <ParallaxText>
              <h2 className="text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight text-neutral-900 mb-8">
                Original
                <br />
                <span className="bg-gradient-to-r from-rose-600 via-rose-500 to-rose-400 bg-clip-text text-transparent">
                  Compositions
                </span>
              </h2>
            </ParallaxText>
            <p className="text-xl sm:text-2xl text-neutral-600 max-w-4xl mx-auto leading-relaxed italic">
              "Sometimes the best way to express a feeling is through composing music."
            </p>
          </CinematicSection>

          {/* Music Showcase Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 max-w-6xl mx-auto">
            
            {/* Be Aware - Featured with Video */}
            <CinematicSection className="lg:col-span-2">
              <motion.div
                className="relative group"
                initial={{ opacity: 0, scale: 0.95 }}
                whileInView={{ opacity: 1, scale: 1 }}
                transition={{ duration: 1.2 }}
                viewport={{ once: true }}
              >
                <div className="relative bg-gradient-to-br from-neutral-900 via-neutral-800 to-neutral-700 rounded-3xl overflow-hidden shadow-2xl">
                  {/* Album Cover Background */}
                  <div className="absolute inset-0">
                    <Image
                      src="/be-aware.webp"
                      alt="Be Aware Album Cover"
                      fill
                      className="object-cover opacity-30 group-hover:opacity-40 transition-opacity duration-700"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent" />
                  </div>
                  
                  {/* Content */}
                  <div className="relative p-12 lg:p-16 min-h-[400px] flex flex-col justify-between">
                    <div>
                      <div className="flex items-center gap-4 mb-6">
                        <span className="px-3 py-1 bg-red-500 text-white text-sm font-medium rounded-full">🎬 Music Video</span>
                        <span className="px-3 py-1 bg-white/20 text-white text-sm font-medium rounded-full backdrop-blur-sm">2020</span>
                      </div>
                      <h3 className="text-4xl lg:text-5xl font-bold text-white mb-4">Be Aware</h3>
                      <p className="text-white/90 text-lg lg:text-xl leading-relaxed max-w-2xl">
                        A journey through sound and vision—my first single with a full music video.
                      </p>
                    </div>
                    
                    <div className="flex flex-wrap gap-4 mt-8">
                      <motion.a
                        href="https://www.youtube.com/watch?v=012eud4qjHE"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-3 px-6 py-4 bg-red-500 text-white rounded-xl font-semibold text-lg hover:bg-red-600 transition-colors shadow-lg hover:shadow-xl"
                        whileHover={{ scale: 1.05, y: -2 }}
                        whileTap={{ scale: 0.95 }}
                      >
                        <span className="text-xl">📺</span>
                        Watch Video
                      </motion.a>
                      <motion.a
                        href="https://open.spotify.com/album/78YPuJu8EM9hR32tukVQh3"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-3 px-6 py-4 bg-green-500 text-white rounded-xl font-semibold text-lg hover:bg-green-600 transition-colors shadow-lg hover:shadow-xl"
                        whileHover={{ scale: 1.05, y: -2 }}
                        whileTap={{ scale: 0.95 }}
                      >
                        <span className="text-xl">🎵</span>
                        Spotify
                      </motion.a>
                      <motion.a
                        href="https://music.apple.com/br/album/be-aware-single/1525671917"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-3 px-6 py-4 bg-gray-900 text-white rounded-xl font-semibold text-lg hover:bg-gray-800 transition-colors shadow-lg hover:shadow-xl"
                        whileHover={{ scale: 1.05, y: -2 }}
                        whileTap={{ scale: 0.95 }}
                      >
                        <span className="text-xl">🍎</span>
                        Apple Music
                      </motion.a>
                    </div>
                  </div>
                </div>
              </motion.div>
            </CinematicSection>

            {/* Achilles Trilogy */}
            <CinematicSection>
              <motion.div
                className="relative group h-full"
                initial={{ opacity: 0, x: -50 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 1.0, delay: 0.2 }}
                viewport={{ once: true }}
              >
                <div className="relative bg-gradient-to-br from-neutral-100 to-neutral-50 rounded-2xl overflow-hidden shadow-xl hover:shadow-2xl transition-shadow duration-500 h-full">
                  {/* Album Cover */}
                  <div className="relative h-64 overflow-hidden">
                    <Image
                      src="/achilles.jpg"
                      alt="Achilles Trilogy Album Cover"
                      fill
                      className="object-cover group-hover:scale-105 transition-transform duration-700"
                    />
                    <div className="absolute top-4 left-4">
                      <span className="px-3 py-1 bg-black/80 text-white text-sm font-medium rounded-full backdrop-blur-sm">EP • 2021-2022</span>
                    </div>
                  </div>
                  
                  {/* Content */}
                  <div className="p-8">
                    <h3 className="text-3xl font-bold text-neutral-900 mb-4">Achilles Trilogy</h3>
                    <p className="text-neutral-600 text-lg leading-relaxed mb-6">
                      A three-part journey through orchestral arrangements, guitar solos, piano, drums, and bass.
                    </p>
                    
                    {/* Favorite Track Highlight */}
                    <div className="bg-rose-50 border-l-4 border-rose-400 p-4 rounded-r-xl mb-6">
                      <p className="text-rose-800 font-semibold text-sm mb-1">✨ Personal Favorite</p>
                      <p className="text-rose-700 font-medium">Achilles II</p>
                      <p className="text-rose-600 text-sm">Features sweeping MIDI orchestra and intricate guitar work</p>
                    </div>
                    
                    <div className="space-y-3">
                      <motion.a
                        href="https://open.spotify.com/track/5HTADgrwluGLT6afFzzDhk?si=9c3c45e868764c54"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-3 w-full px-4 py-3 bg-green-500 text-white rounded-xl font-medium hover:bg-green-600 transition-colors"
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                      >
                        <span>🎵</span>
                        Play Achilles II
                      </motion.a>
                      <motion.a
                        href="https://open.spotify.com/album/6OItgP0pqkhhrKn0BRer0b"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-3 w-full px-4 py-3 border-2 border-neutral-200 text-neutral-700 rounded-xl font-medium hover:border-rose-300 hover:bg-rose-50 transition-colors"
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                      >
                        <span>🎼</span>
                        Full Trilogy
                      </motion.a>
                    </div>
                  </div>
                </div>
              </motion.div>
            </CinematicSection>

            {/* Streaming Stats & Call to Action */}
            <CinematicSection>
              <motion.div
                className="relative group h-full"
                initial={{ opacity: 0, x: 50 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 1.0, delay: 0.4 }}
                viewport={{ once: true }}
              >
                <div className="bg-gradient-to-br from-rose-500 to-rose-600 rounded-2xl p-8 text-white shadow-xl hover:shadow-2xl transition-shadow duration-500 h-full flex flex-col justify-between">
                  <div>
                    <h3 className="text-2xl font-bold mb-6">Available Everywhere</h3>
                    <p className="text-rose-100 text-lg leading-relaxed mb-8">
                      From late-night compositions to full orchestral arrangements—experience the complete musical journey.
                    </p>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <motion.a
                        href="https://music.apple.com/br/album/achilles-trilogy-single/1604464244"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center justify-center gap-2 px-4 py-3 bg-white/20 backdrop-blur-sm rounded-xl font-medium hover:bg-white/30 transition-colors"
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                      >
                        <span>🍎</span>
                        Apple
                      </motion.a>
                      <motion.a
                        href="https://m.youtube.com/playlist?list=OLAK5uy_mh1aVOb3eOiKEF7ZTSHmbTt6Nr3iffT1g"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center justify-center gap-2 px-4 py-3 bg-white/20 backdrop-blur-sm rounded-xl font-medium hover:bg-white/30 transition-colors"
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                      >
                        <span>📺</span>
                        YouTube
                      </motion.a>
                    </div>
                    
                    <motion.a
                      href="https://open.spotify.com/artist/3VZ8V9XhQ9oZb5XnZ9g8yB"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center justify-center gap-3 w-full px-6 py-4 bg-white text-rose-600 rounded-xl font-bold text-lg hover:bg-rose-50 transition-colors shadow-lg"
                      whileHover={{ scale: 1.05, y: -2 }}
                      whileTap={{ scale: 0.95 }}
                    >
                      <span className="text-xl">🎧</span>
                      Follow on Spotify
                    </motion.a>
                  </div>
                </div>
              </motion.div>
            </CinematicSection>
          </div>
        </div>
      </section>

      {/* === ACT III: YOUTUBE HIGHLIGHTS === */}
      <section className="relative py-32 lg:py-40 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-white via-rose-25/30 to-white overflow-hidden">
        {/* Background Elements */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute top-1/4 -left-32 w-96 h-96 bg-gradient-to-r from-rose-200/20 to-transparent rounded-full blur-3xl" />
          <div className="absolute bottom-1/4 -right-32 w-96 h-96 bg-gradient-to-l from-rose-200/20 to-transparent rounded-full blur-3xl" />
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-gradient-radial from-rose-100/10 to-transparent rounded-full" />
        </div>

        <div className="relative max-w-7xl mx-auto">
          <CinematicSection className="text-center mb-32">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 1.2 }}
              viewport={{ once: true }}
              className="relative"
            >
              {/* Floating YouTube Icon */}
              <motion.div
                className="absolute -top-16 left-1/2 -translate-x-1/2"
                initial={{ opacity: 0, scale: 0, rotate: -180 }}
                whileInView={{ opacity: 1, scale: 1, rotate: 0 }}
                transition={{ duration: 1.5, delay: 0.3, type: "spring", bounce: 0.4 }}
                viewport={{ once: true }}
              >
                <div className="w-20 h-20 bg-gradient-to-br from-red-500 to-red-600 rounded-2xl flex items-center justify-center shadow-2xl shadow-red-500/25">
                  <svg className="w-10 h-10 text-white" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                  </svg>
                </div>
              </motion.div>

              <ParallaxText>
                <h2 className="text-6xl sm:text-7xl lg:text-8xl font-bold tracking-tight text-neutral-900 mb-8">
                  <motion.span
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8, delay: 0.2 }}
                    viewport={{ once: true }}
                    className="block"
                  >
                    Visual
                  </motion.span>
                  <motion.span
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8, delay: 0.4 }}
                    viewport={{ once: true }}
                    className="block bg-gradient-to-r from-red-600 via-rose-500 to-rose-400 bg-clip-text text-transparent"
                  >
                    Stories
                  </motion.span>
                </h2>
              </ParallaxText>
              
              <motion.p
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.6 }}
                viewport={{ once: true }}
                className="text-xl sm:text-2xl text-neutral-600 max-w-4xl mx-auto leading-relaxed mb-12"
              >
                Where creativity meets technology—curated highlights from my YouTube journey.
              </motion.p>

              {/* Channel Stats */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.8 }}
                viewport={{ once: true }}
                className="flex flex-wrap justify-center gap-8 text-center"
              >
                <div className="bg-white/60 backdrop-blur-sm rounded-2xl px-6 py-4 border border-rose-100 shadow-lg">
                  <div className="text-2xl font-bold text-neutral-900">50+</div>
                  <div className="text-sm text-neutral-600">Videos Created</div>
                </div>
                <div className="bg-white/60 backdrop-blur-sm rounded-2xl px-6 py-4 border border-rose-100 shadow-lg">
                  <div className="text-2xl font-bold text-neutral-900">10K+</div>
                  <div className="text-sm text-neutral-600">Total Views</div>
                </div>
                <div className="bg-white/60 backdrop-blur-sm rounded-2xl px-6 py-4 border border-rose-100 shadow-lg">
                  <div className="text-2xl font-bold text-neutral-900">3</div>
                  <div className="text-sm text-neutral-600">Categories</div>
                </div>
              </motion.div>
            </motion.div>
          </CinematicSection>

          {/* Featured Video Spotlight */}
          <motion.div
            initial={{ opacity: 0, y: 60 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 1.2, delay: 0.2 }}
            viewport={{ once: true }}
            className="mb-24"
          >
            <div className="text-center mb-12">
              <h3 className="text-3xl font-bold text-neutral-900 mb-4">Featured Video</h3>
              <p className="text-lg text-neutral-600">The video that started it all</p>
            </div>
            
            <motion.a
              href={bestVideos[0]?.url}
              target="_blank"
              rel="noopener noreferrer"
              className="group block max-w-4xl mx-auto"
              whileHover={{ scale: 1.02 }}
              transition={{ duration: 0.3 }}
            >
              <div className="relative bg-gradient-to-br from-neutral-900 to-neutral-800 rounded-3xl overflow-hidden shadow-2xl">
                <div className="aspect-video relative">
                  {/* Video Thumbnail Placeholder */}
                  <div className="absolute inset-0 bg-gradient-to-br from-neutral-700 to-neutral-800 flex items-center justify-center">
                    <motion.div
                      className="w-24 h-24 bg-red-600 rounded-full flex items-center justify-center shadow-2xl"
                      whileHover={{ scale: 1.1 }}
                      transition={{ duration: 0.3 }}
                    >
                      <svg className="w-10 h-10 text-white ml-1" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M8 5v14l11-7z"/>
                      </svg>
                    </motion.div>
                  </div>
                  
                  {/* Overlay Effects */}
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />
                  <div className="absolute inset-0 bg-red-600/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                  
                  {/* Video Info Overlay */}
                  <div className="absolute bottom-6 left-6 right-6">
                    <div className="flex items-center gap-3 mb-3">
                      <span className="bg-red-600 text-white px-3 py-1 rounded-full text-sm font-medium">
                        {bestVideos[0]?.category}
                      </span>
                      <span className="bg-black/70 text-white px-3 py-1 rounded-full text-sm">
                        {bestVideos[0]?.duration}
                      </span>
                    </div>
                    <h4 className="text-2xl font-bold text-white mb-2">
                      {bestVideos[0]?.title}
                    </h4>
                    <p className="text-neutral-200 text-sm opacity-90">
                      {bestVideos[0]?.views} views
                    </p>
                  </div>
                </div>
              </div>
            </motion.a>
          </motion.div>

          {/* Video Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {bestVideos.slice(1).map((video, index) => (
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
                whileHover={{ y: -8, scale: 1.02 }}
              >
                <div className="bg-white/80 backdrop-blur-sm rounded-2xl overflow-hidden border border-rose-100 shadow-lg group-hover:shadow-2xl group-hover:shadow-rose-500/10 transition-all duration-500">
                  <div className="relative aspect-video bg-gradient-to-br from-neutral-100 to-neutral-50">
                    {/* Animated Play Button */}
                    <div className="absolute inset-0 flex items-center justify-center">
                      <motion.div
                        className="w-16 h-16 bg-gradient-to-br from-red-500 to-red-600 rounded-full flex items-center justify-center shadow-xl opacity-80 group-hover:opacity-100"
                        whileHover={{ scale: 1.1, rotate: 5 }}
                        transition={{ duration: 0.3 }}
                      >
                        <svg className="w-6 h-6 text-white ml-0.5" fill="currentColor" viewBox="0 0 24 24">
                          <path d="M8 5v14l11-7z"/>
                        </svg>
                      </motion.div>
                    </div>
                    
                    {/* Category and Duration */}
                    <div className="absolute top-4 left-4 right-4 flex justify-between items-start">
                      <motion.span
                        className={`px-3 py-1.5 rounded-full text-xs font-medium backdrop-blur-sm ${
                          video.category === 'Tech' ? 'bg-blue-500/90 text-white' :
                          video.category === 'Music' ? 'bg-rose-500/90 text-white' :
                          video.category === 'Photography' ? 'bg-purple-500/90 text-white' :
                          'bg-neutral-500/90 text-white'
                        }`}
                        whileHover={{ scale: 1.05 }}
                      >
                        {video.category}
                      </motion.span>
                      <span className="bg-black/80 text-white px-3 py-1.5 rounded-full text-xs font-medium backdrop-blur-sm">
                        {video.duration}
                      </span>
                    </div>
                    
                    {/* Hover Stats */}
                    <motion.div
                      className="absolute bottom-4 left-4 right-4 opacity-0 group-hover:opacity-100 transition-all duration-300"
                      initial={{ y: 10 }}
                      whileHover={{ y: 0 }}
                    >
                      <div className="bg-black/80 text-white px-3 py-2 rounded-lg text-sm font-medium backdrop-blur-sm">
                        {video.views} views
                      </div>
                    </motion.div>
                    
                    {/* Gradient Overlay */}
                    <div className="absolute inset-0 bg-gradient-to-t from-black/20 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                  </div>
                  
                  <div className="p-6">
                    <h4 className="text-lg font-bold text-neutral-900 mb-3 group-hover:text-rose-600 transition-colors line-clamp-2">
                      {video.title}
                    </h4>
                    <p className="text-neutral-600 text-sm leading-relaxed line-clamp-3">
                      {video.description}
                    </p>
                    
                    {/* Watch Now CTA */}
                    <motion.div
                      className="mt-4 flex items-center text-rose-600 text-sm font-medium opacity-0 group-hover:opacity-100 transition-all duration-300"
                      initial={{ x: -10 }}
                      whileHover={{ x: 0 }}
                    >
                      <span>Watch Now</span>
                      <svg className="w-4 h-4 ml-2 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </motion.div>
                  </div>
                </div>
              </motion.a>
            ))}
          </div>

          {/* Call to Action */}
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 1, delay: 0.3 }}
            viewport={{ once: true }}
            className="text-center mt-20"
          >
            <motion.a
              href="https://youtube.com/@RenatoDAP"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-3 bg-gradient-to-r from-red-600 to-rose-500 text-white px-8 py-4 rounded-2xl font-bold text-lg shadow-2xl shadow-red-500/25 hover:shadow-red-500/40 transition-all duration-300"
              whileHover={{ scale: 1.05, y: -2 }}
              whileTap={{ scale: 0.98 }}
            >
              <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
              </svg>
              Subscribe on YouTube
            </motion.a>
          </motion.div>
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
