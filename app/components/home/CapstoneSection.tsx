// components/home/CapstoneSection.tsx

'use client';

import Button from '../button';
import { useEffect, useRef, useState } from 'react';

export default function CapstoneSection() {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const [canPlay, setCanPlay] = useState(false);

  useEffect(() => {
    if (videoRef.current) {
      const handleCanPlay = () => setCanPlay(true);
      videoRef.current.addEventListener('canplay', handleCanPlay);
      return () => videoRef.current?.removeEventListener('canplay', handleCanPlay);
    }
  }, []);

  return (
    <section className="relative bg-gradient-to-b from-white to-gray-50 py-24 px-6 sm:px-8 overflow-hidden">
      <div className="text-center space-y-6 max-w-3xl mx-auto z-10 relative">
        <h2 className="text-3xl sm:text-4xl font-semibold tracking-tight text-neutral-900">
          Capstone Project: AllAboutFood
        </h2>
        <p className="text-neutral-600 text-base sm:text-lg">
          An AI-powered recipe engine built for real users. It personalizes meals, adapts to dietary needs, and learns from preferences — all in a smooth, intuitive web experience.
        </p>
        <div className="flex flex-col sm:flex-row justify-center items-center gap-4 pt-4">
          <Button
            href="https://youtube.com/your-capstone-video"
            variant="solid"
          >
            Watch Demo
          </Button>
          <Button
            href="https://github.com/renatodap/allaboutfood"
            variant="outline"
          >
            View Code
          </Button>
        </div>
      </div>

      {/* Visual media — video with fallback */}
      <div className="mt-16 flex justify-center items-center">
        {canPlay ? (
          <video
            ref={videoRef}
            className="rounded-xl drop-shadow-xl max-w-[640px] w-full h-auto"
            autoPlay
            muted
            loop
            playsInline
            preload="auto"
            poster="/allaboutfood.png"
          >
            <source src="/allaboutfood.mp4" type="video/mp4" />
          </video>
        ) : (
          <img
            src="/allaboutfood.png"
            alt="AllAboutFood UI"
            className="max-w-[300px] sm:max-w-[400px] w-full h-auto drop-shadow-xl rounded-xl"
          />
        )}
      </div>
    </section>
  );
}
