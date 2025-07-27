// components/home/MusicSection.tsx

'use client';

import Button from '../button';
import Image from 'next/image';

export default function MusicSection() {
  return (
    <section className="py-16 overflow-hidden text-center flex flex-col items-center">
      {/* SVG Icon */}
      <div className="mb-6">
        <Image
          src="/music-icon.svg"
          alt="Music Icon"
          width={64}
          height={64}
          className="opacity-80"
        />
      </div>

      {/* Text Content */}
      <h3 className="text-2xl sm:text-3xl font-semibold text-neutral-900 mb-3">
        Live Music & Open Mic
      </h3>
      <p className="text-neutral-600 max-w-md text-base sm:text-lg mb-6">
        Performing live keeps me honest. Music gives me rhythm, presence, and the confidence to be fully seen — on stage or in front of a whiteboard.
      </p>

      <Button href="/music" variant="solid">
        Watch a Performance
      </Button>
    </section>
  );
}
