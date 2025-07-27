// components/home/LiteClientSection.tsx

'use client';

import Button from '../button';
import { useEffect, useRef, useState } from 'react';

export default function LiteClientSection() {
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
          Accumulate Lite Client
        </h2>
        <p className="text-neutral-600 text-base sm:text-lg">
          A lightweight blockchain verification client, built to bridge AI and secure decentralization. Designed, architected, and documented from scratch.
        </p>
        <div className="flex flex-col sm:flex-row justify-center items-center gap-4 pt-4">
          <Button
            href="https://www.youtube.com/watch?v=your-liteclient-video"
            variant="solid"
          >
            Watch the Video
          </Button>
          <Button href="https://github.com/renatodap/accumulate-liteclient" variant="outline">
            View Code
          </Button>
        </div>
      </div>

      {/* Video or Image */}
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
            poster="/acc-lite-client.png"
          >
            <source src="/acc-lite-client.mp4" type="video/mp4" />
          </video>
        ) : (
          <img
            src="/acc-lite-client.png"
            alt="Accumulate Lite Client Preview"
            className="max-w-[300px] sm:max-w-[400px] w-full h-auto drop-shadow-xl rounded-xl"
          />
        )}
      </div>
    </section>
  );
}
