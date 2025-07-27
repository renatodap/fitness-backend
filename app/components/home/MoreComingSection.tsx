// components/home/MoreComingSection.tsx

'use client';

import Button from '../button';
import Image from 'next/image';

export default function MoreComingSection() {
  return (
    <section className="bg-white py-16 overflow-hidden text-center flex flex-col items-center">
      {/* SVG Icon */}
      <div className="mb-6">
        <Image
          src="/future-icon.svg"
          alt="Future Icon"
          width={64}
          height={64}
          className="opacity-80"
        />
      </div>

      {/* Text Content */}
      <h3 className="text-2xl sm:text-3xl font-semibold text-neutral-900 mb-3">
        More Coming Soon
      </h3>
      <p className="text-neutral-600 max-w-md text-base sm:text-lg mb-6">
        I update this site every trimester. New experiments, ideas, and builds — all focused on leveling up what I can make and how I think.
      </p>

      <Button href="/software" variant="solid">
        See All Projects
      </Button>
    </section>
  );
}
