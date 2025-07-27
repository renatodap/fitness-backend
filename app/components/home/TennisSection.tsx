// components/home/TennisSection.tsx

'use client';

import Button from '../button';
import Image from 'next/image';

export default function TennisSection() {
  return (
    <section className="bg-white py-16 overflow-hidden text-center flex flex-col items-center">
      {/* SVG Icon */}
      <div className="mb-6">
        <Image
          src="/tennis-icon.svg"
          alt="Tennis Icon"
          width={64}
          height={64}
          className="opacity-80"
        />
      </div>

      {/* Text Content */}
      <h3 className="text-2xl sm:text-3xl font-semibold text-neutral-900 mb-3">
        Fall Tennis Season
      </h3>
      <p className="text-neutral-600 max-w-md text-base sm:text-lg mb-6">
        I compete in NCAA tennis while training 6 days a week. It's how I stay sharp — physically, mentally, and emotionally.
      </p>

      <Button href="/tennis" variant="solid">
        View Season Schedule
      </Button>
    </section>
  );
}
