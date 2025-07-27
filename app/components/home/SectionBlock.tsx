// REFACTORED: SectionBlock.tsx

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
      transition: { duration: 0.8, staggerChildren: 0.15 },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.6 },
    },
  };

  const imageVariants = {
    hidden: { opacity: 0, scale: 0.9, y: 20 },
    visible: {
      opacity: 1,
      scale: 1,
      y: 0,
      transition: { duration: 0.7 },
    },
  };

  return (
    <motion.section
      ref={ref}
      className="py-16 sm:py-24 lg:py-32 px-4 sm:px-6 lg:px-8 relative overflow-hidden"
      variants={containerVariants}
      initial="hidden"
      animate={isInView ? 'visible' : 'hidden'}
    >
      {/* Background Elements */}
      <div className="absolute inset-0 pointer-events-none">
        <div className={`absolute w-96 h-96 rounded-full blur-3xl opacity-10 ${
          isCentered ? 'top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-teal-500' :
          reverse ? 'top-1/4 left-1/4 bg-rose-500' :
          'bottom-1/4 right-1/4 bg-orange-500'
        }`} />
      </div>

      <div className="max-w-7xl mx-auto relative z-10">
        <div className={`grid gap-12 lg:gap-16 items-center ${
          isCentered ? 'grid-cols-1 text-center' :
          'grid-cols-1 lg:grid-cols-2'
        } ${reverse && !isCentered ? 'lg:grid-flow-col-dense' : ''}`}>
          
          {/* === Text Block === */}
          <motion.div
            className={`space-y-6 sm:space-y-8 ${
              isCentered ? 'max-w-4xl mx-auto' : 
              reverse ? 'lg:col-start-2' : ''
            }`}
            variants={itemVariants}
          >
            {/* Optional Overlay SVG Behind Title */}
            {overlaySvg && (
              <div className={`absolute z-0 opacity-10 pointer-events-none ${
                isCentered ? 'left-1/2 -translate-x-1/2 -top-8' : '-top-4 -left-4'
              }`}>
                {overlaySvg}
              </div>
            )}

            {/* Title */}
            <motion.h2 
              className={`font-heading font-bold text-neutral-900 leading-tight relative z-10 ${
                isCentered ? 'text-3xl sm:text-4xl lg:text-5xl xl:text-6xl' :
                'text-2xl sm:text-3xl lg:text-4xl xl:text-5xl'
              }`}
              variants={itemVariants}
            >
              {title}
            </motion.h2>

            {/* Description */}
            <motion.div
              className={`text-neutral-600 font-body leading-relaxed relative z-10 ${
                isCentered ? 'text-base sm:text-lg lg:text-xl max-w-3xl mx-auto' :
                'text-sm sm:text-base lg:text-lg max-w-2xl'
              }`}
              variants={itemVariants}
            >
              {description}
            </motion.div>

            {/* CTAs */}
            <motion.div
              className={`flex flex-wrap gap-3 sm:gap-4 ${
                isCentered ? 'justify-center' : 'justify-start'
              }`}
              variants={itemVariants}
            >
              {ctas.map((cta, i) => (
                <motion.div 
                  key={i} 
                  whileHover={{ scale: 1.02 }} 
                  whileTap={{ scale: 0.98 }}
                >
                  <Button
                    href={cta.href}
                    variant={cta.variant}
                    color={i === 0 ? 'gradient' : 'black'}
                    size="md"
                    shimmer={i === 0}
                    className="text-sm sm:text-base"
                  >
                    {cta.label}
                  </Button>
                </motion.div>
              ))}
            </motion.div>
          </motion.div>

          {/* === Image Block === */}
          <motion.div
            className={`flex justify-center items-center ${
              reverse && !isCentered ? 'lg:col-start-1' : ''
            }`}
            variants={imageVariants}
          >
            <div className="relative group w-full max-w-lg">
              {image.endsWith('.svg') ? (
                <motion.div 
                  className="p-8 sm:p-12 bg-white rounded-2xl border border-neutral-200 shadow-2xl"
                  whileHover={{ scale: 1.02, borderColor: '#14b8a6' }}
                  transition={{ duration: 0.2 }}
                >
                  <Image
                    src={image}
                    alt={title}
                    width={120}
                    height={120}
                    className="w-16 h-16 sm:w-24 sm:h-24 lg:w-32 lg:h-32 opacity-80 mx-auto"
                  />
                </motion.div>
              ) : (
                <motion.img
                  src={image}
                  alt={title}
                  className="rounded-xl shadow-2xl w-full h-auto border border-neutral-200"
                  whileHover={{ scale: 1.02 }}
                  transition={{ duration: 0.3 }}
                />
              )}
            </div>
          </motion.div>
        </div>
      </div>
    </motion.section>
  );
}
