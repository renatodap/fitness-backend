// app/photo/page.tsx

import Button from "../components/button";

export default function Photo() {
  return (
    <div className="space-y-32">
      {/* Hero Section */}
      <section className="relative flex flex-col items-center text-center pt-8 pb-16">
        <div className="max-w-4xl mx-auto space-y-8">
          <h1 className="text-5xl font-bold tracking-tight">Photo & Video</h1>
          <p className="text-xl text-neutral-600 max-w-2xl mx-auto leading-relaxed">
            Capturing moments through photography and bringing stories to life through 
            video creation and editing. Visual storytelling across multiple mediums.
          </p>
        </div>
      </section>

      {/* Video Creation Focus */}
      <section className="relative bg-gradient-to-b from-teal-50 to-white py-20 px-4 sm:px-6">
        <div className="max-w-5xl mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-3xl font-bold tracking-tight">Video Creation & Editing</h2>
            <p className="text-neutral-600 text-lg max-w-2xl mx-auto">
              Showcasing video making and editing skills through YouTube content
            </p>
          </div>
          
          <div className="bg-white rounded-2xl p-8 shadow-sm border border-gray-100">
            <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-6 lg:space-y-0 mb-8">
              <div className="space-y-4">
                <div className="flex items-center space-x-4">
                  <div className="w-16 h-16 bg-red-500 rounded-full flex items-center justify-center">
                    <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-2xl font-bold">YouTube Channel</h3>
                    <p className="text-teal-600 font-medium">Renato DAP</p>
                  </div>
                </div>
                <p className="text-neutral-700 leading-relaxed">
                  A showcase of video making and editing abilities through music content, 
                  tutorials, and creative projects. Demonstrating technical skills in 
                  post-production, storytelling, and visual composition.
                </p>
              </div>
              <div className="flex-shrink-0">
                <Button href="https://youtube.com/@renatodap" variant="solid">
                  Visit Channel
                </Button>
              </div>
            </div>

            {/* Featured Videos Grid */}
            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-3">
                <div className="bg-gray-100 rounded-xl aspect-video flex items-center justify-center">
                  <div className="text-center space-y-3">
                    <div className="w-12 h-12 bg-teal-500 rounded-full flex items-center justify-center mx-auto">
                      <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clipRule="evenodd" />
                      </svg>
                    </div>
                    <p className="text-neutral-600 text-sm">Music Video Production</p>
                  </div>
                </div>
                <h4 className="font-semibold">[Featured Music Video]</h4>
                <p className="text-sm text-neutral-600">Showcasing video editing and production skills</p>
              </div>
              
              <div className="space-y-3">
                <div className="bg-gray-100 rounded-xl aspect-video flex items-center justify-center">
                  <div className="text-center space-y-3">
                    <div className="w-12 h-12 bg-teal-500 rounded-full flex items-center justify-center mx-auto">
                      <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clipRule="evenodd" />
                      </svg>
                    </div>
                    <p className="text-neutral-600 text-sm">Creative Project</p>
                  </div>
                </div>
                <h4 className="font-semibold">[Creative Video Project]</h4>
                <p className="text-sm text-neutral-600">Demonstrating storytelling and editing techniques</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Photography Portfolio */}
      <section className="py-20 px-4 sm:px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-3xl font-bold tracking-tight">Photography Portfolio</h2>
            <p className="text-neutral-600 text-lg max-w-2xl mx-auto">
              Capturing moments and exploring visual composition through photography
            </p>
          </div>

          {/* Photo Categories */}
          <div className="grid md:grid-cols-3 gap-8 mb-16">
            <div className="text-center space-y-4">
              <div className="aspect-square bg-gray-100 rounded-2xl flex items-center justify-center">
                <div className="text-center space-y-3">
                  <div className="w-16 h-16 bg-teal-100 rounded-full flex items-center justify-center mx-auto">
                    <svg className="w-8 h-8 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                  </div>
                  <p className="text-neutral-600">Portrait Photography</p>
                </div>
              </div>
              <h3 className="text-lg font-semibold">Portraits</h3>
              <p className="text-sm text-neutral-600">[Number] photos</p>
            </div>
            
            <div className="text-center space-y-4">
              <div className="aspect-square bg-gray-100 rounded-2xl flex items-center justify-center">
                <div className="text-center space-y-3">
                  <div className="w-16 h-16 bg-teal-100 rounded-full flex items-center justify-center mx-auto">
                    <svg className="w-8 h-8 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                    </svg>
                  </div>
                  <p className="text-neutral-600">Landscape Photography</p>
                </div>
              </div>
              <h3 className="text-lg font-semibold">Landscapes</h3>
              <p className="text-sm text-neutral-600">[Number] photos</p>
            </div>
            
            <div className="text-center space-y-4">
              <div className="aspect-square bg-gray-100 rounded-2xl flex items-center justify-center">
                <div className="text-center space-y-3">
                  <div className="w-16 h-16 bg-teal-100 rounded-full flex items-center justify-center mx-auto">
                    <svg className="w-8 h-8 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                    </svg>
                  </div>
                  <p className="text-neutral-600">Event Photography</p>
                </div>
              </div>
              <h3 className="text-lg font-semibold">Events</h3>
              <p className="text-sm text-neutral-600">[Number] photos</p>
            </div>
          </div>

          {/* Sample Gallery Grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Array.from({ length: 8 }, (_, i) => (
              <div key={i} className="aspect-square bg-gray-100 rounded-lg flex items-center justify-center">
                <div className="text-center">
                  <div className="w-8 h-8 bg-teal-100 rounded-full flex items-center justify-center mx-auto mb-2">
                    <svg className="w-4 h-4 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <p className="text-xs text-neutral-500">Photo {i + 1}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Technical Skills */}
      <section className="relative bg-black text-white py-20 px-4 sm:px-6">
        <div className="max-w-5xl mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-3xl font-bold tracking-tight">Technical Skills</h2>
            <p className="text-gray-300 text-lg max-w-2xl mx-auto">
              Tools and techniques used in video production and photo editing
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-teal-400">Video Editing</h3>
              <ul className="space-y-2 text-gray-300 text-sm">
                <li>[Video Editing Software]</li>
                <li>[Motion Graphics]</li>
                <li>[Color Grading]</li>
                <li>[Audio Sync & Mixing]</li>
                <li>[Export Optimization]</li>
              </ul>
            </div>
            
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-teal-400">Photography</h3>
              <ul className="space-y-2 text-gray-300 text-sm">
                <li>[Photo Editing Software]</li>
                <li>[RAW Processing]</li>
                <li>[Composition Techniques]</li>
                <li>[Lighting Setup]</li>
                <li>[Post-Processing]</li>
              </ul>
            </div>
            
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-teal-400">Equipment</h3>
              <ul className="space-y-2 text-gray-300 text-sm">
                <li>[Camera Equipment]</li>
                <li>[Lens Collection]</li>
                <li>[Lighting Gear]</li>
                <li>[Audio Equipment]</li>
                <li>[Editing Hardware]</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-20 px-4 sm:px-6 text-center">
        <div className="max-w-3xl mx-auto space-y-8">
          <h2 className="text-3xl font-bold tracking-tight">Visual Storytelling</h2>
          <p className="text-xl text-neutral-600 leading-relaxed">
            Combining technical skills with creative vision to capture and create 
            compelling visual content across photography and video.
          </p>
          <div className="flex flex-col sm:flex-row justify-center items-center gap-4 pt-4">
            <Button href="https://youtube.com/@renatodap" variant="solid">
              YouTube Channel
            </Button>
            <Button href="/music" variant="outline">
              Music Videos
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
}
