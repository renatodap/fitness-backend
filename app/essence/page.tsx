// app/essence/page.tsx

import UniversalHero from '../components/shared/UniversalHero';
import Button from "../components/button";

export default function Essence() {
  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section with Tennis Video */}
      <UniversalHero
        theme="essence"
        title="What Shapes the Systems"
        subtitle="Behind every line of code and creative decision lies a foundation built through discipline, education, and values. This is what grounds both the logic and the rhythm."
        videoSrc="/essence.mp4"
        mobileVideoSrc="/essence.mp4"
        buttons={[
          { href: "#discipline", label: "See the Foundation", variant: "solid" },
          { href: "#philosophy", label: "Read Philosophy", variant: "outline" }
        ]}
      />

      {/* Tennis - Discipline & Rhythm */}
      <section className="py-16 px-4 sm:px-6 bg-orange-50 border-t border-orange-100">
        <div className="max-w-6xl mx-auto">
          <div className="text-center space-y-4 mb-12">
            <h2 className="text-4xl font-bold tracking-tight">Discipline & Rhythm</h2>
            <p className="text-neutral-600 text-lg max-w-2xl mx-auto">
              Tennis taught me that excellence isn't about talent—it's about showing up every day with intention
            </p>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-6">
              <div className="space-y-4">
                <h3 className="text-2xl font-semibold">Rose-Hulman Men's Tennis Captain</h3>
                <p className="text-lg text-neutral-700 leading-relaxed">
                  Leading a team isn't about being the best player—it's about creating an environment 
                  where everyone can perform at their peak. The same principles that guide my code: 
                  clear communication, consistent execution, and always improving the system.
                </p>
              </div>
              
              <div className="bg-white rounded-xl p-6 border border-orange-200">
                <h4 className="font-semibold mb-3">Training Philosophy</h4>
                <ul className="space-y-2 text-neutral-700">
                  <li>• 6 days a week, rain or shine</li>
                  <li>• Mental resilience through physical challenge</li>
                  <li>• Team-first leadership approach</li>
                  <li>• Constant iteration and improvement</li>
                </ul>
              </div>
            </div>
            
            <div className="aspect-[4/3] bg-neutral-100 rounded-xl overflow-hidden">
              <img 
                src="/tennis.JPG" 
                alt="Tennis action shot"
                className="w-full h-full object-cover"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Education - Foundation */}
      <section className="py-16 px-4 sm:px-6 bg-white">
        <div className="max-w-6xl mx-auto">
          <div className="text-center space-y-4 mb-12">
            <h2 className="text-4xl font-bold tracking-tight">Foundation</h2>
            <p className="text-neutral-600 text-lg max-w-2xl mx-auto">
              Rose-Hulman doesn't just teach computer science—it teaches you how to think like an engineer
            </p>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="bg-orange-50 rounded-xl p-8 border border-orange-200">
              <h3 className="text-xl font-semibold mb-4">Computer Science Major</h3>
              <p className="text-neutral-700 mb-4">
                Class of 2026, focused on systems thinking and practical problem-solving
              </p>
              <div className="space-y-2 text-sm text-neutral-600">
                <p>• Data Structures & Algorithms</p>
                <p>• Software Design & Architecture</p>
                <p>• Artificial Intelligence (Fall 2025)</p>
                <p>• Deep Learning (Fall 2025)</p>
              </div>
            </div>
            
            <div className="bg-white rounded-xl p-8 border border-neutral-200">
              <h3 className="text-xl font-semibold mb-4">Engineering Mindset</h3>
              <p className="text-neutral-700 mb-4">
                Rose-Hulman's hands-on approach shapes how I approach every problem
              </p>
              <div className="space-y-2 text-sm text-neutral-600">
                <p>• Build first, optimize later</p>
                <p>• Test assumptions early and often</p>
                <p>• Collaborate across disciplines</p>
                <p>• Focus on real-world impact</p>
              </div>
            </div>
            
            <div className="bg-orange-50 rounded-xl p-8 border border-orange-200">
              <h3 className="text-xl font-semibold mb-4">Beyond the Classroom</h3>
              <p className="text-neutral-700 mb-4">
                Learning happens everywhere—from tennis courts to music studios
              </p>
              <div className="space-y-2 text-sm text-neutral-600">
                <p>• Leadership through athletics</p>
                <p>• Creative expression through music</p>
                <p>• Technical skills through projects</p>
                <p>• Communication through teaching</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Values & Philosophy */}
      <section className="py-16 px-4 sm:px-6 bg-orange-50 border-t border-orange-100">
        <div className="max-w-4xl mx-auto text-center space-y-8">
          <h2 className="text-3xl font-bold tracking-tight">Philosophy</h2>
          <div className="space-y-8 text-lg text-neutral-700 leading-relaxed">
            <div className="bg-white rounded-xl p-8 border border-orange-200">
              <h3 className="text-xl font-semibold mb-4 text-orange-600">Systems with Rhythm and Logic</h3>
              <p>
                "I create systems with rhythm and logic." This isn't just a tagline—it's how I approach everything. 
                Whether I'm debugging code, leading a tennis team, or improvising on stage, the best solutions 
                emerge when analytical thinking dances with creative intuition.
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white rounded-xl p-6 border border-orange-200">
                <h4 className="font-semibold mb-3 text-orange-600">Logic</h4>
                <p className="text-base">
                  Clear thinking, systematic approaches, and evidence-based decisions. 
                  Every line of code should have a purpose, every strategy should be testable.
                </p>
              </div>
              
              <div className="bg-white rounded-xl p-6 border border-orange-200">
                <h4 className="font-semibold mb-3 text-orange-600">Rhythm</h4>
                <p className="text-base">
                  Intuition, flow states, and the human element. 
                  The best technical solutions feel natural, like a song that makes you move.
                </p>
              </div>
            </div>
            
            <div className="bg-white rounded-xl p-8 border border-orange-200">
              <h3 className="text-xl font-semibold mb-4 text-orange-600">What Matters</h3>
              <p>
                Building things that solve real problems for real people. Leading by example, not by authority. 
                Staying curious, staying humble, and always asking "How can this be better?" 
                The goal isn't to be the smartest person in the room—it's to make the room smarter.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Navigation to Other Pages */}
      <section className="py-16 px-4 sm:px-6 bg-white text-center">
        <div className="max-w-4xl mx-auto space-y-8">
          <h2 className="text-3xl font-bold tracking-tight">Explore the Work</h2>
          <p className="text-xl text-neutral-600 leading-relaxed">
            Now that you know what shapes the systems, see them in action.
          </p>
          <div className="flex flex-col sm:flex-row justify-center items-center gap-4 pt-6">
            <Button href="/engineer" variant="solid">
              Engineer - Logic in Action
            </Button>
            <Button href="/creator" variant="outline">
              Creator - Rhythm in Motion
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
}