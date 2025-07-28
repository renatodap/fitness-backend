// app/education/page.tsx

import Button from "../components/button";

export default function Education() {
  return (
    <div className="space-y-32">
      {/* Hero Section */}
      <section className="relative flex flex-col items-center justify-center min-h-screen px-4 sm:px-6">
        <div className="absolute inset-0 bg-gradient-to-br from-teal-500/5 via-transparent to-rose-500/5" />
        <div className="relative max-w-6xl mx-auto text-center space-y-12">
          <div className="space-y-6">
            <h1 className="font-heading text-6xl sm:text-8xl font-bold tracking-tight">
              Education
            </h1>
            <p className="font-body text-xl sm:text-2xl text-neutral-600 max-w-3xl mx-auto leading-relaxed">
              Formal education in computer science at Rose-Hulman, building a foundation in 
              algorithms, systems, and computational thinking while exploring AI and self-directed learning.
            </p>
          </div>
          <div className="flex flex-col sm:flex-row gap-6 justify-center items-center pt-8">
            <Button href="#rose-hulman" variant="solid">
              Rose-Hulman
            </Button>
            <Button href="#self-learning" variant="outline">
              Self-Directed Learning
            </Button>
          </div>
        </div>
      </section>

      {/* Current Education */}
      <section className="relative bg-gradient-to-b from-teal-50 to-white py-20 px-4 sm:px-6">
        <div className="max-w-5xl mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-3xl font-bold tracking-tight">Current Studies</h2>
            <p className="text-neutral-600 text-lg max-w-2xl mx-auto">
              Pursuing a comprehensive education in computer science and engineering
            </p>
          </div>
          
          <div className="bg-white rounded-2xl p-8 shadow-sm border border-gray-100">
            <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between space-y-6 lg:space-y-0">
              <div className="space-y-4">
                <div className="space-y-2">
                  <h3 className="text-2xl font-bold">Bachelor of Science in Computer Science</h3>
                  <p className="text-teal-600 font-semibold text-lg">Rose-Hulman Institute of Technology</p>
                  <p className="text-neutral-500">Class of 2026 • Terre Haute, Indiana</p>
                </div>
                
                <div className="space-y-3">
                  <p className="text-neutral-700 leading-relaxed">
                    Pursuing a rigorous computer science education at one of the nation's top 
                    undergraduate engineering schools, known for its hands-on approach and 
                    strong industry connections.
                  </p>
                  
                  <div className="flex items-center space-x-2">
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-teal-100 text-teal-800">
                      In Progress
                    </span>
                    <span className="text-neutral-500 text-sm">Expected Graduation: May 2026</span>
                  </div>
                </div>
              </div>
              
              <div className="flex-shrink-0">
                <div className="w-24 h-24 bg-teal-100 rounded-full flex items-center justify-center">
                  <span className="text-2xl font-bold text-teal-600">RHIT</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Coursework */}
      <section className="py-20 px-4 sm:px-6">
        <div className="max-w-5xl mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-3xl font-bold tracking-tight">Coursework</h2>
            <p className="text-neutral-600 text-lg max-w-2xl mx-auto">
              Core computer science curriculum and specialized electives
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {/* Core Courses */}
            <div className="space-y-6">
              <h3 className="text-xl font-semibold text-teal-600">Core Computer Science</h3>
              <div className="space-y-4">
                <div className="p-4 bg-gray-50 rounded-lg">
                  <h4 className="font-semibold">Data Structures & Algorithms</h4>
                  <p className="text-sm text-neutral-600 mt-1">
                    [Course details will be added as completed]
                  </p>
                </div>
                
                <div className="p-4 bg-gray-50 rounded-lg">
                  <h4 className="font-semibold">Computer Systems</h4>
                  <p className="text-sm text-neutral-600 mt-1">
                    [Course details will be added as completed]
                  </p>
                </div>
                
                <div className="p-4 bg-gray-50 rounded-lg">
                  <h4 className="font-semibold">Software Engineering</h4>
                  <p className="text-sm text-neutral-600 mt-1">
                    [Course details will be added as completed]
                  </p>
                </div>
                
                <div className="p-4 bg-gray-50 rounded-lg">
                  <h4 className="font-semibold">Database Systems</h4>
                  <p className="text-sm text-neutral-600 mt-1">
                    [Course details will be added as completed]
                  </p>
                </div>
              </div>
            </div>

            {/* Specialized Courses */}
            <div className="space-y-6">
              <h3 className="text-xl font-semibold text-teal-600">Specialized & Electives</h3>
              <div className="space-y-4">
                <div className="p-4 bg-gray-50 rounded-lg">
                  <h4 className="font-semibold">Machine Learning</h4>
                  <p className="text-sm text-neutral-600 mt-1">
                    [Course details will be added as completed]
                  </p>
                </div>
                
                <div className="p-4 bg-gray-50 rounded-lg">
                  <h4 className="font-semibold">Computer Networks</h4>
                  <p className="text-sm text-neutral-600 mt-1">
                    [Course details will be added as completed]
                  </p>
                </div>
                
                <div className="p-4 bg-gray-50 rounded-lg">
                  <h4 className="font-semibold">Cybersecurity</h4>
                  <p className="text-sm text-neutral-600 mt-1">
                    [Course details will be added as completed]
                  </p>
                </div>
                
                <div className="p-4 bg-gray-50 rounded-lg">
                  <h4 className="font-semibold">Advanced Topics</h4>
                  <p className="text-sm text-neutral-600 mt-1">
                    [Additional courses will be added]
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Academic Achievements */}
      <section className="relative bg-black text-white py-20 px-4 sm:px-6">
        <div className="max-w-5xl mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-3xl font-bold tracking-tight">Academic Highlights</h2>
            <p className="text-gray-300 text-lg max-w-2xl mx-auto">
              Recognition and achievements throughout my academic journey
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center space-y-4">
              <div className="w-16 h-16 bg-teal-500 rounded-full flex items-center justify-center mx-auto">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold">Academic Excellence</h3>
              <p className="text-gray-300 text-sm">
                [GPA and academic honors will be added]
              </p>
            </div>
            
            <div className="text-center space-y-4">
              <div className="w-16 h-16 bg-teal-500 rounded-full flex items-center justify-center mx-auto">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold">Research Projects</h3>
              <p className="text-gray-300 text-sm">
                [Undergraduate research opportunities]
              </p>
            </div>
            
            <div className="text-center space-y-4">
              <div className="w-16 h-16 bg-teal-500 rounded-full flex items-center justify-center mx-auto">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold">Leadership</h3>
              <p className="text-gray-300 text-sm">
                Tennis Team Captain, Student Organizations
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-20 px-4 sm:px-6 text-center">
        <div className="max-w-3xl mx-auto space-y-8">
          <h2 className="text-3xl font-bold tracking-tight">Academic Journey</h2>
          <p className="text-xl text-neutral-600 leading-relaxed">
            Following a rigorous curriculum while exploring the intersection of 
            computer science with music, sports, and creative expression.
          </p>
          <div className="flex flex-col sm:flex-row justify-center items-center gap-4 pt-4">
            <Button href="/software" variant="solid">
              View Projects
            </Button>
            <Button href="/tennis" variant="outline">
              Athletic Leadership
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
}
