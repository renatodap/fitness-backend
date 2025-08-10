'use client';

import UniversalHero from '@/app/components/shared/UniversalHero';
import { motion, useInView, useScroll, useTransform } from 'framer-motion';
import { useRef, useEffect, useState } from 'react';
import Image from 'next/image';

// === CREATOR DATA STRUCTURES ===

// Musical Journey - Refined instrument stories
const instrumentJourney = [
  {
    name: "Guitar", essence: "The Entry Point", years: "13 years", 
    image: "/guitar.jpg",
    story: "My entry point at 9 years old. Six strings that became my voice before I found my actual voice.",
    philosophy: "Every musician needs that first door into the world of sound. Guitar was mine."
  },
  {
    name: "Piano", essence: "The Spark", years: "Since childhood",
    image: "/piano.jpg",
    story: "Old pianos at grandma's house in Dracena and grandpa's farm in Minas Gerais. I played with them at 3-4 years old, knowing nothing but feeling everything.",
    philosophy: "Sometimes the most profound connections happen before we understand what we're connecting to."
  },
  {
    name: "Drums", essence: "The Dream", years: "4 years",
    image: "/drums.JPG",
    story: "Always dreamed of playing, never thought it would happen. I'm not very good, but the passion is unmatched. It taught me rhythm that translates to life.",
    philosophy: "Sometimes it's not about being good—it's about the rhythm you find in your soul."
  },
  {
    name: "Bass", essence: "The Missing Piece", years: "4 years",
    image: "/bass.jpg",
    story: "Every guitarist can play bass until they try. Classical guitar technique helped, but bass became the missing piece to feel like a full band.",
    philosophy: "The foundation isn't flashy, but without it, everything else falls apart."
  },
  {
    name: "Singing", essence: "The Discovery", years: "1 year",
    image: "/singing.jpg",
    story: "Thought I'd never be good at singing. Still certain about it. But expressing myself through my voice has been my discovery of the last year.",
    philosophy: "The most vulnerable instrument is your own voice, but it's also the most honest."
  },
  {
    name: "Harmonica", essence: "The Pocket Friend", years: "Occasional",
    image: "/harmonica.jpg",
    story: "How hard is harmonica anyway? That instrument in your pocket, waiting for the perfect campfire moment.",
    philosophy: "Not every instrument needs to be mastered—some just need to be enjoyed."
  },
  {
    name: "Ukulele", essence: "The Connector", years: "2 years",
    image: "/ukulele.jpg",
    story: "Bought in Florida, became my portable way to connect with people through music. Four strings of instant friendship.",
    philosophy: "The best instruments are the ones that bring people together."
  }
];

// YouTube Production Videos - Best cinematic work
const productionVideos = [
  {
    title: "HCAC Tennis Championship",
    url: "https://youtu.be/iQpksbH7_98",
    duration: "16:18",
    description: "Cinematic documentary of Rose-Hulman men's tennis team winning the HCAC tournament in 2024. Filmed everything, created cinematic montages and vlog-style content."
  },
  {
    title: "Florida 2025 Trailer",
    url: "https://youtu.be/wEr7aQhQyT8",
    duration: "2:30",
    description: "Trailer for the 2025 Rose-Hulman tennis team trip to Florida. High-energy preview of what's to come."
  },
  {
    title: "Why I Switched to CS",
    url: "https://youtu.be/KFIK0Z7Ynhc",
    duration: "7:15",
    description: "My journey from Mechanical Engineering to Computer Science. Growth mindset, instinct, and reinventing yourself in college."
  },
  {
    title: "Amazonia 2019",
    url: "https://youtu.be/X4T8BvJJbF0",
    duration: "12:45",
    description: "School trip to the Amazon with insane cinematics. Collaborative work with Andre Faria showcasing Brazil's natural beauty."
  },
  {
    title: "Jaboticabeiras - A Film by Renato DAP",
    url: "https://www.youtube.com/watch?v=rgCUhfJUGqE",
    duration: "8:30",
    description: "Cinematic vlog at my grandpa's coffee farm. Personal storytelling through visual narrative."
  }
];

// Cover Videos - Musical performances
const coverVideos = [
  {
    title: "Aquarela – Toquinho",
    url: "https://youtu.be/K0GJm90x8JQ",
    setup: "3-camera fingerstyle guitar",
    description: "Original arrangement of this emotional Brazilian classic I've loved since childhood."
  },
  {
    title: "Queen Tribute Medley",
    url: "https://youtu.be/4eyS1n_wDTg",
    setup: "Multi-instrument (bass, guitar, piano, drums)",
    description: "Another One Bites the Dust, Under Pressure, Don't Stop Me Now with visual effects."
  },
  {
    title: "James Bay Cover & Medley",
    url: "https://youtu.be/9cPRUFOc0Zg",
    setup: "Full band (bass, guitar, piano, drums)",
    description: "Instrumental showcase of versatility across multiple instruments."
  },
  {
    title: "Stand By Me (with Andre Faria)",
    url: "https://youtu.be/-v1uvO7y0oE",
    setup: "Bass & guitar solo, vocals & acoustic",
    description: "Collaborative performance blending instrumental and vocal elements."
  }
];

// Live Performances - Recent shows
const livePerformances = {
  recent: [
    {
      title: "Tennis Team ROFR 2025",
      url: "https://youtu.be/2hA1PzLpmNw",
      setup: "Guitar/vocals with Ephraim & Austin",
      songs: "Rocket Man, Vienna, Sweet Child O' Mine, Country Roads"
    },
    {
      title: "Charlie's June 19th",
      url: "https://www.youtube.com/watch?v=sZ9FGq-2yKk",
      setup: "Solo guitar & vocals",
      songs: "Yellow, Just The Way You Are, What A Wonderful World, Here Comes The Sun"
    }
  ],
  cacetaBand: [
    {
      title: "Comfortably Numb",
      url: "https://youtu.be/laVb5UwWuJY",
      date: "Jan 2025",
      role: "Drums"
    },
    {
      title: "Hotel California",
      url: "https://youtu.be/1A0IEPV1Hn4",
      date: "Jan 2025",
      role: "Drums"
    },
    {
      title: "War Pigs",
      url: "https://youtu.be/LgGu5TlZuHc",
      date: "2024",
      role: "Drums"
    }
  ]
};

// Original Music - Key releases
const originalMusic = [
  {
    title: "Be Aware", 
    type: "Single", 
    year: "2020",
    featured: true,
    hasVideo: true,
    cover: "/be-aware.webp",
    description: "Sonic exploration of consciousness, blending electronic and organic elements.",
    quote: "Sometimes the best way to express a feeling is through composing music.",
    links: [
      { name: "Watch Video", url: "https://www.youtube.com/watch?v=012eud4qjHE", icon: "📺", color: "bg-red-500" },
      { name: "Spotify", url: "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC", icon: "🎵", color: "bg-green-500" },
      { name: "Apple Music", url: "https://music.apple.com/album/1533243836?i=1533243838", icon: "🍎", color: "bg-neutral-900" },
      { name: "YouTube Music", url: "https://music.youtube.com/watch?v=v4amCfVbA_c", icon: "📺", color: "bg-red-500" }
    ]
  },
  {
    title: "Achilles Trilogy", 
    type: "EP", 
    year: "2021-2022",
    featured: true,
    cover: "/achilles.jpg",
    description: "Three-part journey exploring vulnerability, strength, and resilience through orchestral and guitar compositions.",
    favoriteTrack: "Achilles II",
    favoriteDescription: "My personal favorite—delicate balance of orchestral arrangements and intimate guitar work.",
    links: [
      { name: "Play Achilles II", url: "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC", icon: "▶️", color: "bg-green-500" },
      { name: "Spotify", url: "https://open.spotify.com/album/1abcdef", icon: "🎵", color: "bg-green-500" },
      { name: "Apple Music", url: "https://music.apple.com/album/achilles-trilogy", icon: "🍎", color: "bg-neutral-900" },
      { name: "YouTube Music", url: "https://m.youtube.com/playlist?list=OLAK5uy_mh1aVOb3eOiKEF7ZTSHmbTt6Nr3iffT1g", icon: "📺", color: "bg-red-500" }
    ]
  }
];

// Visual Stories - Video statistics and best examples
const videoStats = {
  total: "50+ videos",
  views: "10K+ total views",
  categories: ["Production", "Covers", "Vlogs"]
};

const bestVlogs = [
  {
    title: "What It Feels Like to Be Part of a College Tennis Team",
    url: "https://youtu.be/o741o1AkJg4",
    duration: "8:45",
    description: "Deep dive into college tennis culture, team integration, and focusing on process over results."
  },
  {
    title: "Day in My Life: ME Student and Tennis Player",
    url: "https://youtu.be/-Kbugu-h1s0",
    duration: "12:30",
    description: "Behind the scenes of balancing engineering studies with collegiate athletics."
  },
  {
    title: "My Freshman Year at Rose",
    url: "https://youtu.be/m_Fax7N-Fu0",
    duration: "15:20",
    description: "Reflection on the transformative first year of college—growth, challenges, and discoveries."
  },
  {
    title: "Santa Monica 2018",
    url: "https://youtu.be/JqF83bp1yU0",
    duration: "6:15",
    description: "Emotional farewell to the US, moving back to Brazil, and processing major life transitions."
  }
];

// Creator Philosophy
const creatorPhilosophy = {
  vlogMeaning: "Vlogs are how I connect with my past self. I put my memories in video form and when I watch them back I always get very emotional, not for the video that was made but because I'm able to teleport myself back to what I was thinking and feeling at the moment that the video was made.",
  approach: "Every story deserves to be told with intention, authenticity, and heart."
};

// Archive - Historical performances
const archivePerformances = [
  {
    title: "Master of Puppets Guitar Solo",
    url: "https://youtu.be/nzkoxVH_bqw",
    date: "Jun 2021",
    description: "Early guitar work showcasing technical development."
  },
  {
    title: "Anesthesia on Bass",
    url: "https://youtu.be/GwT2QrVj5-I",
    date: "May 2021",
    description: "My first day playing bass ever—documenting the beginning of a new instrument journey."
  },
  {
    title: "Jailhouse Rock Full Band",
    url: "https://www.youtube.com/watch?v=ewga3Ssf-Ck",
    date: "2020",
    description: "Creative multi-tracking before I had a full drum set or bass."
  }
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
                  <div className="text-2xl font-bold text-neutral-900">{videoStats.total}</div>
                  <div className="text-sm text-neutral-600">Videos Created</div>
                </div>
                <div className="bg-white/60 backdrop-blur-sm rounded-2xl px-6 py-4 border border-rose-100 shadow-lg">
                  <div className="text-2xl font-bold text-neutral-900">{videoStats.views}</div>
                  <div className="text-sm text-neutral-600">Total Views</div>
                </div>
                <div className="bg-white/60 backdrop-blur-sm rounded-2xl px-6 py-4 border border-rose-100 shadow-lg">
                  <div className="text-2xl font-bold text-neutral-900">{videoStats.categories.length}</div>
                  <div className="text-sm text-neutral-600">Categories</div>
                </div>
              </motion.div>
            </motion.div>
          </CinematicSection>

          {/* Production Videos Section */}
          <CinematicSection className="mb-24">
            <div className="text-center mb-12">
              <h3 className="text-4xl font-bold text-neutral-900 mb-4">Production Videos</h3>
              <p className="text-lg text-neutral-600 max-w-2xl mx-auto">
                Cinematic storytelling meets technical precision—my best production work.
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {productionVideos.map((video, index) => (
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
                      
                      <div className="absolute top-4 right-4">
                        <span className="bg-black/70 text-white px-3 py-1 rounded-full text-sm">
                          {video.duration}
                        </span>
                      </div>
                    </div>
                    
                    <div className="p-6">
                      <h4 className="text-xl font-bold text-neutral-900 mb-2 group-hover:text-rose-600 transition-colors">
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
          </CinematicSection>

          {/* Cover Videos Section */}
          <CinematicSection className="mb-24">
            <div className="text-center mb-12">
              <h3 className="text-4xl font-bold text-neutral-900 mb-4">Musical Covers</h3>
              <p className="text-lg text-neutral-600 max-w-2xl mx-auto">
                Multi-instrumental arrangements and collaborations showcasing musical versatility.
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {coverVideos.map((video, index) => (
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
                  whileHover={{ y: -4, scale: 1.01 }}
                >
                  <div className="bg-white/60 backdrop-blur-sm rounded-xl p-6 border border-rose-100 shadow-lg group-hover:shadow-xl transition-all duration-300">
                    <div className="flex items-start gap-4">
                      <div className="w-12 h-12 bg-gradient-to-br from-rose-500 to-rose-600 rounded-lg flex items-center justify-center flex-shrink-0">
                        <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
                          <path d="M8 5v14l11-7z"/>
                        </svg>
                      </div>
                      <div className="flex-1">
                        <h4 className="text-lg font-bold text-neutral-900 mb-1 group-hover:text-rose-600 transition-colors">
                          {video.title}
                        </h4>
                        <p className="text-sm text-rose-600 font-medium mb-2">
                          {video.setup}
                        </p>
                        <p className="text-neutral-600 text-sm leading-relaxed">
                          {video.description}
                        </p>
                      </div>
                    </div>
                  </div>
                </motion.a>
              ))}
            </div>
          </CinematicSection>

          {/* Best Vlogs Section */}
          <CinematicSection className="mb-24">
            <div className="text-center mb-12">
              <h3 className="text-4xl font-bold text-neutral-900 mb-4">Personal Stories</h3>
              <p className="text-lg text-neutral-600 max-w-3xl mx-auto italic">
                "{creatorPhilosophy.vlogMeaning}"
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {bestVlogs.map((video, index) => (
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
                  whileHover={{ y: -6, scale: 1.02 }}
                >
                  <div className="bg-white/80 backdrop-blur-sm rounded-2xl overflow-hidden border border-rose-100 shadow-lg group-hover:shadow-2xl group-hover:shadow-rose-500/10 transition-all duration-500">
                    <div className="relative aspect-video bg-gradient-to-br from-neutral-100 to-neutral-50">
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
                      
                      <div className="absolute top-4 right-4">
                        <span className="bg-black/70 text-white px-3 py-1 rounded-full text-sm">
                          {video.duration}
                        </span>
                      </div>
                    </div>
                    
                    <div className="p-6">
                      <h4 className="text-xl font-bold text-neutral-900 mb-2 group-hover:text-rose-600 transition-colors">
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
          </CinematicSection>

          {/* Live Performances Section */}
          <CinematicSection className="mb-24">
            <div className="text-center mb-12">
              <h3 className="text-4xl font-bold text-neutral-900 mb-4">Live Performances</h3>
              <p className="text-lg text-neutral-600 max-w-2xl mx-auto">
                From intimate acoustic sets to full band collaborations—music that connects.
              </p>
            </div>
            
            <div className="space-y-12">
              {/* Recent Performances */}
              <div>
                <h4 className="text-2xl font-bold text-neutral-900 mb-6">Recent Shows</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {livePerformances.recent.map((performance, index) => (
                    <motion.a
                      key={performance.title}
                      href={performance.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="group block"
                      initial={{ opacity: 0, y: 40 }}
                      whileInView={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.8, delay: index * 0.1 }}
                      viewport={{ once: true }}
                      whileHover={{ y: -4, scale: 1.01 }}
                    >
                      <div className="bg-white/60 backdrop-blur-sm rounded-xl p-6 border border-rose-100 shadow-lg group-hover:shadow-xl transition-all duration-300">
                        <div className="flex items-start gap-4">
                          <div className="w-12 h-12 bg-gradient-to-br from-orange-500 to-orange-600 rounded-lg flex items-center justify-center flex-shrink-0">
                            <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
                              <path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/>
                            </svg>
                          </div>
                          <div className="flex-1">
                            <h5 className="text-lg font-bold text-neutral-900 mb-1 group-hover:text-orange-600 transition-colors">
                              {performance.title}
                            </h5>
                            <p className="text-sm text-orange-600 font-medium mb-2">
                              {performance.setup}
                            </p>
                            <p className="text-neutral-600 text-sm leading-relaxed">
                              {performance.songs}
                            </p>
                          </div>
                        </div>
                      </div>
                    </motion.a>
                  ))}
                </div>
              </div>

              {/* Caceta Band */}
              <div>
                <h4 className="text-2xl font-bold text-neutral-900 mb-6">Caceta Band 2023-2025</h4>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  {livePerformances.cacetaBand.map((performance, index) => (
                    <motion.a
                      key={performance.title}
                      href={performance.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="group block"
                      initial={{ opacity: 0, y: 40 }}
                      whileInView={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.8, delay: index * 0.1 }}
                      viewport={{ once: true }}
                      whileHover={{ y: -4, scale: 1.01 }}
                    >
                      <div className="bg-white/60 backdrop-blur-sm rounded-xl p-6 border border-rose-100 shadow-lg group-hover:shadow-xl transition-all duration-300 text-center">
                        <div className="w-12 h-12 bg-gradient-to-br from-neutral-700 to-neutral-800 rounded-lg flex items-center justify-center mx-auto mb-4">
                          <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/>
                          </svg>
                        </div>
                        <h5 className="text-lg font-bold text-neutral-900 mb-1 group-hover:text-neutral-700 transition-colors">
                          {performance.title}
                        </h5>
                        <p className="text-sm text-neutral-600 font-medium mb-2">
                          {performance.role} • {performance.date}
                        </p>
                      </div>
                    </motion.a>
                  ))}
                </div>
              </div>
            </div>
          </CinematicSection>

        </div>
      </section>
    </main>
  );
}
