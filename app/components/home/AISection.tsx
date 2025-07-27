// components/home/AISection.tsx

'use client';

import Button from '../button';
import Image from 'next/image';

export default function AISection() {
  return (
    <section className="py-16 overflow-hidden text-center flex flex-col items-center">
      {/* SVG or Icon */}
      <div className="mb-6">
        <Image
          src="/ai-icon.svg"
          alt="AI Icon"
          width={64}
          height={64}
          className="opacity-80"
        />
      </div>

      {/* Text Content */}
      <h3 className="text-2xl sm:text-3xl font-semibold text-neutral-900 mb-3">
        AI Coursework – Fall 2025
      </h3>
      <p className="text-neutral-600 max-w-md text-base sm:text-lg mb-6">
        I’m diving deep into Machine Learning and AI Theory this fall. Real math, real models, real understanding — not just tools, but how they work.
      </p>

      <Button href="/ai-courses" variant="solid">
        See Course Plan
      </Button>
    </section>
  );
}
