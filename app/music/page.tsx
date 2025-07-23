// app/music/page.tsx

import Button from "../components/button";

export default function Music() {
  return (
    <div className="space-y-32">
      {/* Hero Section */}
      <section className="relative flex flex-col items-center text-center pt-8 pb-16">
        <div className="max-w-4xl mx-auto space-y-8">
          <h1 className="text-5xl font-bold tracking-tight">Music</h1>
          <p className="text-xl text-neutral-600 max-w-2xl mx-auto leading-relaxed">
            Creating original music and covers across multiple instruments. 
            From bedroom recordings to live performances, exploring rhythm and melody.
          </p>
        </div>
      </section>

      {/* Streaming Platforms */}
      <section className="relative bg-gradient-to-b from-teal-50 to-white py-20 px-4 sm:px-6">
        <div className="max-w-5xl mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-3xl font-bold tracking-tight">Listen Now</h2>
            <p className="text-neutral-600 text-lg max-w-2xl mx-auto">
              Original music and covers available on streaming platforms
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 gap-8">
            {/* Spotify */}
            <div className="bg-white rounded-2xl p-8 shadow-sm border border-gray-100">
              <div className="flex items-center space-x-4 mb-6">
                <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center">
                  <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.42 1.56-.299.421-1.02.599-1.559.3z"/>
                  </svg>
                </div>
                <div>
                  <h3 className="text-xl font-bold">Spotify</h3>
                  <p className="text-teal-600 font-medium">Renato DAP</p>
                </div>
              </div>
              <p className="text-neutral-700 mb-6">
                Original compositions and instrumental pieces available for streaming.
              </p>
              <Button href="https://open.spotify.com/artist/renatodap" variant="solid">
                Listen on Spotify
              </Button>
            </div>

            {/* YouTube */}
            <div className="bg-white rounded-2xl p-8 shadow-sm border border-gray-100">
              <div className="flex items-center space-x-4 mb-6">
                <div className="w-16 h-16 bg-red-500 rounded-full flex items-center justify-center">
                  <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                  </svg>
                </div>
                <div>
                  <h3 className="text-xl font-bold">YouTube</h3>
                  <p className="text-teal-600 font-medium">Renato DAP</p>
                </div>
              </div>
              <p className="text-neutral-700 mb-6">
                Music covers, live performances, and behind-the-scenes content.
              </p>
              <Button href="https://youtube.com/@renatodap" variant="solid">
                Watch on YouTube
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Instruments */}
      <section className="py-20 px-4 sm:px-6">
        <div className="max-w-5xl mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-3xl font-bold tracking-tight">Instruments</h2>
            <p className="text-neutral-600 text-lg max-w-2xl mx-auto">
              Multi-instrumentalist exploring different sounds and musical expressions
            </p>
          </div>

          <div className="grid md:grid-cols-3 lg:grid-cols-4 gap-6">
            {/* Primary Instruments */}
            <div className="bg-white rounded-xl p-6 border border-gray-200 text-center">
              <div className="w-12 h-12 bg-teal-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🥁</span>
              </div>
              <h3 className="font-semibold mb-2">Drums</h3>
              <p className="text-sm text-neutral-600">Rhythm foundation</p>
            </div>
            
            <div className="bg-white rounded-xl p-6 border border-gray-200 text-center">
              <div className="w-12 h-12 bg-teal-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🎸</span>
              </div>
              <h3 className="font-semibold mb-2">Guitar</h3>
              <p className="text-sm text-neutral-600">Acoustic & electric</p>
            </div>
            
            <div className="bg-white rounded-xl p-6 border border-gray-200 text-center">
              <div className="w-12 h-12 bg-teal-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🎹</span>
              </div>
              <h3 className="font-semibold mb-2">Piano</h3>
              <p className="text-sm text-neutral-600">Keys & composition</p>
            </div>
            
            <div className="bg-white rounded-xl p-6 border border-gray-200 text-center">
              <div className="w-12 h-12 bg-teal-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🎸</span>
              </div>
              <h3 className="font-semibold mb-2">Bass</h3>
              <p className="text-sm text-neutral-600">Low-end groove</p>
            </div>
            
            <div className="bg-white rounded-xl p-6 border border-gray-200 text-center">
              <div className="w-12 h-12 bg-teal-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🎵</span>
              </div>
              <h3 className="font-semibold mb-2">Vocals</h3>
              <p className="text-sm text-neutral-600">Learning to sing</p>
            </div>
            
            <div className="bg-white rounded-xl p-6 border border-gray-200 text-center">
              <div className="w-12 h-12 bg-teal-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🎺</span>
              </div>
              <h3 className="font-semibold mb-2">Harmonica</h3>
              <p className="text-sm text-neutral-600">Blues & folk</p>
            </div>
            
            <div className="bg-white rounded-xl p-6 border border-gray-200 text-center">
              <div className="w-12 h-12 bg-teal-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🎶</span>
              </div>
              <h3 className="font-semibold mb-2">Recorder</h3>
              <p className="text-sm text-neutral-600">Classical wind</p>
            </div>
            
            <div className="bg-white rounded-xl p-6 border border-gray-200 text-center">
              <div className="w-12 h-12 bg-teal-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🎸</span>
              </div>
              <h3 className="font-semibold mb-2">Ukulele</h3>
              <p className="text-sm text-neutral-600">Portable melodies</p>
            </div>
          </div>
        </div>
      </section>

      {/* Live Performances */}
      <section className="relative bg-black text-white py-20 px-4 sm:px-6">
        <div className="max-w-5xl mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-3xl font-bold tracking-tight">Live Performances</h2>
            <p className="text-gray-300 text-lg max-w-2xl mx-auto">
              Capturing the energy of live music through recordings and performances
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {/* Live Performance Video Placeholder */}
            <div className="space-y-4">
              <div className="bg-gray-800 rounded-xl aspect-video flex items-center justify-center">
                <div className="text-center space-y-3">
                  <div className="w-16 h-16 bg-teal-500 rounded-full flex items-center justify-center mx-auto">
                    <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <p className="text-gray-300">Live Performance Video</p>
                </div>
              </div>
              <h3 className="text-lg font-semibold">[Performance Title]</h3>
              <p className="text-gray-300 text-sm">[Venue/Event] • [Date]</p>
            </div>
            
            <div className="space-y-4">
              <div className="bg-gray-800 rounded-xl aspect-video flex items-center justify-center">
                <div className="text-center space-y-3">
                  <div className="w-16 h-16 bg-teal-500 rounded-full flex items-center justify-center mx-auto">
                    <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <p className="text-gray-300">Studio Session</p>
                </div>
              </div>
              <h3 className="text-lg font-semibold">[Recording Session]</h3>
              <p className="text-gray-300 text-sm">[Studio/Location] • [Date]</p>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-20 px-4 sm:px-6 text-center">
        <div className="max-w-3xl mx-auto space-y-8">
          <h2 className="text-3xl font-bold tracking-tight">Follow the Journey</h2>
          <p className="text-xl text-neutral-600 leading-relaxed">
            Stay updated with new releases, covers, and live performances across platforms.
          </p>
          <div className="flex flex-col sm:flex-row justify-center items-center gap-4 pt-4">
            <Button href="https://open.spotify.com/artist/renatodap" variant="solid">
              Spotify
            </Button>
            <Button href="https://youtube.com/@renatodap" variant="outline">
              YouTube Channel
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
}
