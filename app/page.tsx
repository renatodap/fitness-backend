// page.tsx

import Link from "next/link";
import Button from "./components/button";
import HeroImage from "./components/heroimage"; // adjust path if needed

export default function Home() {
  return (
    <div className="space-y-20">
      {/* Hero Section */}
      <section className="relative flex flex-col items-center text-center pt-0 pb-0 px-2">
        {/* Hoverable, Clickable Image */}
        <Link href="/about">
          <HeroImage />
        </Link>

        {/* Text Content */}
        <h1 className="text-4xl font-semibold mb-4">Hey, I'm Renato DAP</h1>
        <p className="text-lg text-neutral-600 mb-6 max-w-xl">
          I work on projects where creativity meets technical depth.
        </p>
        <div className="flex gap-6">
          <div className="flex flex-col sm:flex-row gap-4 mt-4">
            <Button href="/software" variant="solid">
              View Projects
            </Button>
            <Button href="/photo" variant="outline">
              Watch Videos
            </Button>
          </div>
          </div>
      </section>


      {/* Featured Projects */}

      {/* Accumulate Lite Client Hero Section */}
      <section className="relative bg-gradient-to-b from-sky-50 to-white py-16 px-4 sm:px-6 overflow-hidden">
        <div className="text-center space-y-6 max-w-2xl mx-auto z-10 relative">
          <h2 className="text-2xl sm:text-3xl font-semibold tracking-tight">
            Accumulate Lite Client
          </h2>
          <p className="text-neutral-600 text-base sm:text-lg">
            Lightweight. Secure. Built for the future of blockchain validation.
          </p>
          <div className="flex flex-col sm:flex-row justify-center items-center gap-4 pt-4">
            <Button href="/software" variant="solid">
              Learn More
            </Button>
            <Button href="/software" variant="outline">
              View Code
            </Button>
          </div>
        </div>

        {/* Image */}
        <div className="mt-10 flex justify-center">
          <img
            src="/acc-lite-client.png"
            alt="Accumulate Lite Client Interface"
            className="max-w-[100px] sm:max-w-[250px] w-full h-auto drop-shadow-xl floating"
          />
        </div>
      </section>
    </div>
  );
}
