// app/tennis/page.tsx

import Button from "../components/button";

export default function Tennis() {
  return (
    <div className="space-y-32 bg-white text-black">
      {/* Hero Section */}
      <section className="relative flex flex-col items-center justify-center min-h-screen px-4 sm:px-6">
        <div className="absolute inset-0 bg-gradient-to-br from-teal-100/20 via-white to-rose-100/20" />
        <div className="relative max-w-6xl mx-auto text-center space-y-12">
          <div className="space-y-6">
            <h1 className="font-heading text-6xl sm:text-8xl font-bold tracking-tight">
              Tennis
            </h1>
            <p className="font-body text-xl sm:text-2xl text-neutral-700 max-w-3xl mx-auto leading-relaxed">
              A tennis journey culminating in team leadership. From competitive play 
              to captaining the Rose-Hulman Men's Tennis Team in 2025-26.
            </p>
          </div>
          <div className="flex flex-col sm:flex-row gap-6 justify-center items-center pt-8">
            <Button href="#captain" variant="solid">
              Team Captain
            </Button>
            <Button href="#journey" variant="outline">
              Tennis Journey
            </Button>
          </div>
        </div>
      </section>

      {/* Current Leadership Role */}
      <section className="relative bg-gradient-to-b from-teal-50 to-white py-20 px-4 sm:px-6">
        <div className="max-w-5xl mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-3xl font-bold tracking-tight">Team Leadership</h2>
            <p className="text-neutral-600 text-lg max-w-2xl mx-auto">
              Leading by example on and off the court
            </p>
          </div>
          
          <div className="bg-white rounded-2xl p-8 shadow-sm border border-gray-100">
            <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-6 lg:space-y-0">
              <div className="space-y-4">
                <div className="space-y-2">
                  <h3 className="text-2xl font-bold">Team Captain</h3>
                  <p className="text-teal-600 font-semibold text-lg">Rose-Hulman Men's Tennis Team</p>
                  <p className="text-neutral-500">2025-26 Season • NCAA Division III</p>
                </div>
                
                <div className="space-y-3">
                  <p className="text-neutral-700 leading-relaxed">
                    Leading the Rose-Hulman Men's Tennis Team as captain, responsible for 
                    team coordination, mentoring younger players, and representing the 
                    program's values both on and off the court.
                  </p>
                  
                  <div className="flex items-center space-x-2">
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-teal-100 text-teal-800">
                      Current Captain
                    </span>
                    <span className="text-neutral-500 text-sm">2025-26 Academic Year</span>
                  </div>
                </div>
              </div>
              
              <div className="flex-shrink-0">
                <div className="w-24 h-24 bg-teal-100 rounded-full flex items-center justify-center">
                  <svg className="w-12 h-12 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
                  </svg>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Tennis Career Journey */}
      <section className="py-20 px-4 sm:px-6">
        <div className="max-w-5xl mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-3xl font-bold tracking-tight">Tennis Journey</h2>
            <p className="text-neutral-600 text-lg max-w-2xl mx-auto">
              The path from competitive player to team leader
            </p>
          </div>

          <div className="space-y-12">
            {/* Current Role */}
            <div className="relative pl-8 border-l-2 border-teal-500">
              <div className="absolute w-4 h-4 bg-teal-500 rounded-full -left-2 top-0"></div>
              <div className="space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
                  <div>
                    <h3 className="text-xl font-semibold">Team Captain</h3>
                    <p className="text-teal-600 font-medium">Rose-Hulman Men's Tennis</p>
                  </div>
                  <p className="text-neutral-500 text-sm">2025-26</p>
                </div>
                <p className="text-neutral-700 leading-relaxed">
                  Selected to lead the team as captain, overseeing team dynamics, 
                  strategy, and representing the program in various capacities.
                </p>
                <div className="flex flex-wrap gap-2">
                  <span className="px-2 py-1 bg-teal-100 text-teal-700 rounded text-xs">Leadership</span>
                  <span className="px-2 py-1 bg-teal-100 text-teal-700 rounded text-xs">Team Management</span>
                  <span className="px-2 py-1 bg-teal-100 text-teal-700 rounded text-xs">Mentoring</span>
                </div>
              </div>
            </div>

            {/* Previous Seasons */}
            <div className="relative pl-8 border-l-2 border-gray-200">
              <div className="absolute w-4 h-4 bg-gray-400 rounded-full -left-2 top-0"></div>
              <div className="space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
                  <div>
                    <h3 className="text-xl font-semibold">Varsity Player</h3>
                    <p className="text-teal-600 font-medium">Rose-Hulman Men's Tennis</p>
                  </div>
                  <p className="text-neutral-500 text-sm">[Previous Seasons]</p>
                </div>
                <p className="text-neutral-700 leading-relaxed">
                  [Details about previous seasons, achievements, and development as a player 
                  will be added as more information becomes available]
                </p>
                <div className="flex flex-wrap gap-2">
                  <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">Competitive Play</span>
                  <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">Team Contribution</span>
                </div>
              </div>
            </div>

            {/* Earlier Career */}
            <div className="relative pl-8 border-l-2 border-gray-200">
              <div className="absolute w-4 h-4 bg-gray-400 rounded-full -left-2 top-0"></div>
              <div className="space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
                  <div>
                    <h3 className="text-xl font-semibold">Competitive Development</h3>
                    <p className="text-teal-600 font-medium">[High School/Junior Tennis]</p>
                  </div>
                  <p className="text-neutral-500 text-sm">[Timeline]</p>
                </div>
                <p className="text-neutral-700 leading-relaxed">
                  [Early tennis career details and development pathway will be added]
                </p>
                <div className="flex flex-wrap gap-2">
                  <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">Skill Development</span>
                  <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">Tournament Play</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Leadership & Skills */}
      <section className="relative bg-black text-white py-20 px-4 sm:px-6">
        <div className="max-w-5xl mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-3xl font-bold tracking-tight">Leadership & Skills</h2>
            <p className="text-gray-300 text-lg max-w-2xl mx-auto">
              Qualities developed through competitive tennis and team leadership
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center space-y-4">
              <div className="w-16 h-16 bg-teal-500 rounded-full flex items-center justify-center mx-auto">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold">Team Leadership</h3>
              <p className="text-gray-300 text-sm">
                Guiding team strategy, fostering team unity, and mentoring teammates
              </p>
            </div>
            
            <div className="text-center space-y-4">
              <div className="w-16 h-16 bg-teal-500 rounded-full flex items-center justify-center mx-auto">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold">Mental Toughness</h3>
              <p className="text-gray-300 text-sm">
                Developing resilience, focus, and performance under pressure
              </p>
            </div>
            
            <div className="text-center space-y-4">
              <div className="w-16 h-16 bg-teal-500 rounded-full flex items-center justify-center mx-auto">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold">Strategic Thinking</h3>
              <p className="text-gray-300 text-sm">
                Match analysis, tactical planning, and adaptive game strategies
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Rose-Hulman Tennis Program */}
      <section className="py-20 px-4 sm:px-6">
        <div className="max-w-5xl mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-3xl font-bold tracking-tight">Rose-Hulman Tennis</h2>
            <p className="text-neutral-600 text-lg max-w-2xl mx-auto">
              Representing excellence in academics and athletics
            </p>
          </div>

          <div className="bg-gradient-to-r from-teal-50 to-blue-50 rounded-2xl p-8">
            <div className="text-center space-y-6">
              <div className="w-20 h-20 bg-teal-100 rounded-full flex items-center justify-center mx-auto">
                <span className="text-2xl font-bold text-teal-600">RHIT</span>
              </div>
              <div className="space-y-4">
                <h3 className="text-2xl font-bold">NCAA Division III Excellence</h3>
                <p className="text-neutral-700 leading-relaxed max-w-2xl mx-auto">
                  Rose-Hulman Institute of Technology combines rigorous academic standards 
                  with competitive athletics, fostering student-athletes who excel both 
                  in the classroom and on the court.
                </p>
                <div className="flex flex-wrap justify-center gap-2">
                  <span className="px-3 py-1 bg-white text-teal-700 rounded-full text-sm font-medium">NCAA Division III</span>
                  <span className="px-3 py-1 bg-white text-teal-700 rounded-full text-sm font-medium">Academic Excellence</span>
                  <span className="px-3 py-1 bg-white text-teal-700 rounded-full text-sm font-medium">Team Leadership</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-20 px-4 sm:px-6 text-center">
        <div className="max-w-3xl mx-auto space-y-8">
          <h2 className="text-3xl font-bold tracking-tight">Beyond the Court</h2>
          <p className="text-xl text-neutral-600 leading-relaxed">
            Tennis has shaped leadership skills, mental resilience, and strategic thinking 
            that extend far beyond the game itself.
          </p>
          <div className="flex flex-col sm:flex-row justify-center items-center gap-4 pt-4">
            <Button href="/education" variant="solid">
              Academic Journey
            </Button>
            <Button href="/professional" variant="outline">
              Professional Experience
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
}
