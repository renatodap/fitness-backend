// components/home/AllAboutFoodSection.tsx

'use client';

import Button from '../button';
import { useEffect, useRef, useState } from 'react';

export default function AllAboutFoodSection() {
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
    <section className="py-24 px-6 sm:px-8 overflow-hidden">
      <div className="text-center space-y-6 max-w-3xl mx-auto z-10 relative">
        <h2 className="text-3xl sm:text-4xl font-semibold tracking-tight text-neutral-900">
          All About Food
        </h2>
        <p className="text-neutral-600 text-base sm:text-lg">
          A full-stack AI-powered recipe engine that transforms images, PDFs, or text files into structured, searchable, voice-ready cooking instructions. Built with Flutter, AWS, OpenAI, and Alexa.
        </p>
        <div className="flex flex-col sm:flex-row justify-center items-center gap-4 pt-4">
          <Button href="/projects/allaboutfood" variant="solid">
            See Case Study
          </Button>
          <Button href="https://github.com/renatodap/allaboutfood" variant="outline">
            View Code
          </Button>
        </div>
      </div>

      {/* Media */}
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
