// PATCHED: SectionBlock.tsx

'use client';

import React from 'react';
import Image from 'next/image';
import { motion, useInView } from 'framer-motion';
import { useRef } from 'react';
import Button from '../button';

type CTA = {
  href: string;
  label: string;
  variant: 'solid' | 'outline';
};

type Props = {
  title: string;
  description: string | React.ReactNode;
  image: string;
  align: 'left' | 'right' | 'center';
  ctas: CTA[];
  overlaySvg?: React.ReactNode;
};

export default function SectionBlock({
  title,
  description,
  image,
  align,
  ctas,
  overlaySvg,
}: Props) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: '-100px' });

  const isCentered = align === 'center';
  const reverse = align === 'right';

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { duration: 0.8, staggerChildren: 0.2 },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 40 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.6 },
    },
  };

  const imageVariants = {
    hidden: { opacity: 0, scale: 0.8, y: 40 },
    visible: {
      opacity: 1,
      scale: 1,
      y: 0,
      transition: { duration: 0.8 },
    },
  };

  return (
    <motion.section
      ref={ref}
      className="py-32 px-6 sm:px-12 relative overflow-hidden"
      variants={containerVariants}
      initial="hidden"
      animate={isInView ? 'visible' : 'hidden'}
    >
      <div
        className={`max-w-7xl mx-auto relative z-10 flex flex-col ${
          isCentered ? 'items-center text-center' : reverse ? 'lg:flex-row-reverse' : 'lg:flex-row'
        } gap-16 lg:gap-20 items-center`}
      >
        {/* === Text Block === */}
        <motion.div
          className={`flex-1 ${isCentered ? 'max-w-4xl' : 'max-w-2xl'} ${
            isCentered ? '' : 'text-left'
          } space-y-8 relative`}
          variants={itemVariants}
        >
          {/* Optional Overlay SVG Behind Title */}
          {overlaySvg && (
            <div className="absolute -top-10 left-1/2 -translate-x-1/2 z-0 opacity-10 pointer-events-none">
              {overlaySvg}
            </div>
          )}

          {/* Title */}
          <motion.h2 className="text-4xl sm:text-5xl lg:text-6xl font-heading font-bold text-neutral-900 leading-tight tracking-tight relative z-10">
            {title.split(' ').map((word, index) => (
              <motion.span
                key={index}
                className="inline-block mr-3"
                whileHover={{
                  scale: 1.05,
                  color: '#14b8a6',
                  transition: { duration: 0.2 },
                }}
              >
                {word}
              </motion.span>
            ))}
          </motion.h2>

          {/* Description */}
          <motion.div
            className="text-neutral-600 text-lg sm:text-xl font-body leading-relaxed max-w-prose relative z-10"
            variants={itemVariants}
          >
            {description}
          </motion.div>

          {/* CTAs */}
          <motion.div
            className={`flex flex-wrap gap-4 sm:gap-6 ${isCentered ? 'justify-center' : ''}`}
            variants={itemVariants}
          >
            {ctas.map((cta, i) => (
              <motion.div key={i} whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                <Button
                  href={cta.href}
                  variant={cta.variant}
                  color={i === 0 ? 'gradient' : 'black'}
                  size="lg"
                  shimmer={i === 0}
                >
                  {cta.label}
                </Button>
              </motion.div>
            ))}
          </motion.div>
        </motion.div>

        {/* === Image Block === */}
        <motion.div
          className="flex-1 flex justify-center items-center relative z-10"
          variants={imageVariants}
        >
          <div className="relative group">
            {image.endsWith('.svg') ? (
              <motion.div className="p-12 bg-white rounded-3xl border shadow-xl">
                <Image
                  src={image}
                  alt={title}
                  width={120}
                  height={120}
                  className="w-24 h-24 sm:w-32 sm:h-32 opacity-80"
                />
              </motion.div>
            ) : (
              <img
                src={image}
                alt={title}
                className="rounded-2xl shadow-2xl max-w-full h-auto w-[min(100%,500px)]"
              />
            )}
          </div>
        </motion.div>
      </div>
    </motion.section>
  );
}
