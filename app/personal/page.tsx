// app/personal/page.tsx

import Button from "../components/button";

export default function Personal() {
  return (
    <div className="space-y-32 bg-white text-black">
      {/* Hero Section */}
      <section className="relative flex flex-col items-center justify-center min-h-screen px-4 sm:px-6">
        <div className="absolute inset-0 bg-gradient-to-br from-teal-100/20 via-white to-rose-100/20" />
        <div className="relative max-w-6xl mx-auto text-center space-y-12">
          <div className="space-y-6">
            <h1 className="font-heading text-6xl sm:text-8xl font-bold tracking-tight">
              Personal
            </h1>
            <p className="font-body text-xl sm:text-2xl text-neutral-700 max-w-3xl mx-auto leading-relaxed">
              The stories, thoughts, and experiences that don't fit neatly into other categories. 
              Life beyond the code, music, and competition.
            </p>
          </div>
          <div className="flex flex-col sm:flex-row gap-6 justify-center items-center pt-8">
            <Button href="#philosophy" variant="solid">
              Life Philosophy
            </Button>
            <Button href="#values" variant="outline">
              Core Values
            </Button>
          </div>
        </div>
      </section>

      {/* Life Philosophy */}
      <section className="relative bg-gradient-to-b from-teal-50 to-white py-20 px-4 sm:px-6">
        <div className="max-w-4xl mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-3xl font-bold tracking-tight">Thoughts & Reflections</h2>
            <p className="text-neutral-600 text-lg max-w-2xl mx-auto">
              Personal insights and perspectives on life, learning, and growth
            </p>
          </div>
          
          <div className="space-y-8">
            <div className="bg-white rounded-2xl p-8 shadow-sm border border-gray-100">
              <h3 className="text-xl font-semibold mb-4">On Interdisciplinary Learning</h3>
              <p className="text-neutral-700 leading-relaxed">
                [Personal thoughts on how different disciplines inform each other - 
                music and programming, tennis strategy and problem-solving, etc.]
              </p>
            </div>
            
            <div className="bg-white rounded-2xl p-8 shadow-sm border border-gray-100">
              <h3 className="text-xl font-semibold mb-4">The Art of Balance</h3>
              <p className="text-neutral-700 leading-relaxed">
                [Reflections on managing academics, athletics, creative pursuits, 
                and personal growth simultaneously]
              </p>
            </div>
            
            <div className="bg-white rounded-2xl p-8 shadow-sm border border-gray-100">
              <h3 className="text-xl font-semibold mb-4">Leadership Lessons</h3>
              <p className="text-neutral-700 leading-relaxed">
                [Personal insights gained from tennis team captaincy and how they 
                apply to other areas of life]
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Interests & Hobbies */}
      <section className="py-20 px-4 sm:px-6">
        <div className="max-w-5xl mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-3xl font-bold tracking-tight">Beyond the Main Categories</h2>
            <p className="text-neutral-600 text-lg max-w-2xl mx-auto">
              Other interests, hobbies, and activities that shape who I am
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="text-center space-y-4">
              <div className="w-16 h-16 bg-teal-100 rounded-2xl flex items-center justify-center mx-auto">
                <svg className="w-8 h-8 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold">Reading</h3>
              <p className="text-sm text-neutral-600">
                [Books, articles, and topics of interest]
              </p>
            </div>
            
            <div className="text-center space-y-4">
              <div className="w-16 h-16 bg-teal-100 rounded-2xl flex items-center justify-center mx-auto">
                <svg className="w-8 h-8 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold">Travel</h3>
              <p className="text-sm text-neutral-600">
                [Places visited, cultural experiences, travel philosophy]
              </p>
            </div>
            
            <div className="text-center space-y-4">
              <div className="w-16 h-16 bg-teal-100 rounded-2xl flex items-center justify-center mx-auto">
                <svg className="w-8 h-8 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold">Community</h3>
              <p className="text-sm text-neutral-600">
                [Involvement in communities, volunteering, social activities]
              </p>
            </div>
            
            <div className="text-center space-y-4">
              <div className="w-16 h-16 bg-teal-100 rounded-2xl flex items-center justify-center mx-auto">
                <svg className="w-8 h-8 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold">Learning</h3>
              <p className="text-sm text-neutral-600">
                [Continuous learning, new skills, intellectual curiosity]
              </p>
            </div>
            
            <div className="text-center space-y-4">
              <div className="w-16 h-16 bg-teal-100 rounded-2xl flex items-center justify-center mx-auto">
                <svg className="w-8 h-8 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold">Wellness</h3>
              <p className="text-sm text-neutral-600">
                [Health, fitness, mental wellness, life balance]
              </p>
            </div>
            
            <div className="text-center space-y-4">
              <div className="w-16 h-16 bg-teal-100 rounded-2xl flex items-center justify-center mx-auto">
                <svg className="w-8 h-8 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold">Philosophy</h3>
              <p className="text-sm text-neutral-600">
                [Personal philosophy, values, worldview]
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Personal Timeline */}
      <section className="relative bg-black text-white py-20 px-4 sm:px-6">
        <div className="max-w-5xl mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-3xl font-bold tracking-tight">Life Moments</h2>
            <p className="text-gray-300 text-lg max-w-2xl mx-auto">
              Key experiences and milestones that have shaped my perspective
            </p>
          </div>

          <div className="space-y-8">
            <div className="bg-gray-900 rounded-2xl p-6">
              <div className="flex items-start space-x-4">
                <div className="w-3 h-3 bg-teal-500 rounded-full mt-2 flex-shrink-0"></div>
                <div>
                  <h3 className="text-lg font-semibold text-teal-400 mb-2">[Significant Experience]</h3>
                  <p className="text-gray-300 text-sm mb-2">[Time Period]</p>
                  <p className="text-gray-300 leading-relaxed">
                    [Description of a meaningful personal experience, lesson learned, 
                    or pivotal moment that contributed to personal growth]
                  </p>
                </div>
              </div>
            </div>
            
            <div className="bg-gray-900 rounded-2xl p-6">
              <div className="flex items-start space-x-4">
                <div className="w-3 h-3 bg-teal-500 rounded-full mt-2 flex-shrink-0"></div>
                <div>
                  <h3 className="text-lg font-semibold text-teal-400 mb-2">[Personal Achievement]</h3>
                  <p className="text-gray-300 text-sm mb-2">[Time Period]</p>
                  <p className="text-gray-300 leading-relaxed">
                    [Another significant personal milestone or achievement outside 
                    of the main professional/academic categories]
                  </p>
                </div>
              </div>
            </div>
            
            <div className="bg-gray-900 rounded-2xl p-6">
              <div className="flex items-start space-x-4">
                <div className="w-3 h-3 bg-teal-500 rounded-full mt-2 flex-shrink-0"></div>
                <div>
                  <h3 className="text-lg font-semibold text-teal-400 mb-2">[Learning Experience]</h3>
                  <p className="text-gray-300 text-sm mb-2">[Time Period]</p>
                  <p className="text-gray-300 leading-relaxed">
                    [A personal learning experience or challenge that contributed 
                    to character development or perspective shift]
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Values & Principles */}
      <section className="py-20 px-4 sm:px-6">
        <div className="max-w-4xl mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-3xl font-bold tracking-tight">Core Values</h2>
            <p className="text-neutral-600 text-lg max-w-2xl mx-auto">
              The principles that guide decisions and shape character
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            <div className="space-y-6">
              <div className="space-y-3">
                <h3 className="text-xl font-semibold text-teal-600">Authenticity</h3>
                <p className="text-neutral-700 leading-relaxed">
                  [Personal thoughts on being genuine and true to oneself across 
                  all endeavors and relationships]
                </p>
              </div>
              
              <div className="space-y-3">
                <h3 className="text-xl font-semibold text-teal-600">Growth Mindset</h3>
                <p className="text-neutral-700 leading-relaxed">
                  [Perspective on continuous learning, embracing challenges, 
                  and viewing failures as opportunities]
                </p>
              </div>
            </div>
            
            <div className="space-y-6">
              <div className="space-y-3">
                <h3 className="text-xl font-semibold text-teal-600">Connection</h3>
                <p className="text-neutral-700 leading-relaxed">
                  [Importance of meaningful relationships, community building, 
                  and collaborative achievement]
                </p>
              </div>
              
              <div className="space-y-3">
                <h3 className="text-xl font-semibold text-teal-600">Excellence</h3>
                <p className="text-neutral-700 leading-relaxed">
                  [Commitment to quality, attention to detail, and striving 
                  for mastery in chosen pursuits]
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-20 px-4 sm:px-6 text-center">
        <div className="max-w-3xl mx-auto space-y-8">
          <h2 className="text-3xl font-bold tracking-tight">The Full Picture</h2>
          <p className="text-xl text-neutral-600 leading-relaxed">
            This is just a glimpse into the personal side of the story. 
            The complete picture emerges through all the different facets of life and work.
          </p>
          <div className="flex flex-col sm:flex-row justify-center items-center gap-4 pt-4">
            <Button href="/about" variant="solid">
              Full Story
            </Button>
            <Button href="mailto:contact@renatodap.com" variant="outline">
              Let's Talk
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
}
