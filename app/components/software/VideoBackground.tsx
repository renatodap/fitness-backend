// app/components/software/VideoBackground.tsx

'use client';

import { motion } from 'framer-motion';

interface VideoBackgroundProps {
  src: string;
}

export function VideoBackground({ src }: VideoBackgroundProps) {
  return (
    <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10">
      <motion.video
        key={src} // Re-trigger animation on src change
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1.5, ease: 'easeInOut' }}
        className="absolute top-1/2 left-1/2 min-w-full min-h-full w-auto h-auto object-cover transform -translate-x-1/2 -translate-y-1/2"
        autoPlay
        loop
        muted
        playsInline
        src="/software.mp4"
      />

    </div>
  );
}
