'use client';

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
  description: string;
  image: string;
  align: 'left' | 'right' | 'center';
  ctas: CTA[];
};

export default function SectionBlock({ title, description, image, align, ctas }: Props) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: "-100px" });
  
  const isCentered = align === 'center';
  const reverse = align === 'right';

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        duration: 0.8,
        staggerChildren: 0.2
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 40 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.6
      }
    }
  };

  const imageVariants = {
    hidden: { opacity: 0, scale: 0.8, y: 40 },
    visible: {
      opacity: 1,
      scale: 1,
      y: 0,
      transition: {
        duration: 0.8
      }
    }
  };

  return (
    <motion.section 
      ref={ref}
      className="py-32 px-6 sm:px-12 relative overflow-hidden"
      variants={containerVariants}
      initial="hidden"
      animate={isInView ? "visible" : "hidden"}
    >
      {/* Background Elements */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-1/4 right-1/4 w-64 h-64 bg-gradient-to-br from-teal-500/5 to-rose-500/5 rounded-full blur-3xl" />
        <div className="absolute bottom-1/3 left-1/4 w-48 h-48 bg-gradient-to-br from-orange-500/5 to-teal-500/5 rounded-full blur-3xl" />
      </div>

      <div
        className={`max-w-7xl mx-auto relative z-10 flex flex-col ${
          isCentered ? 'items-center text-center' : reverse ? 'lg:flex-row-reverse' : 'lg:flex-row'
        } gap-16 lg:gap-20 items-center`}
      >
        {/* === Text Block === */}
        <motion.div 
          className={`flex-1 ${isCentered ? 'max-w-4xl' : 'max-w-2xl'} ${isCentered ? '' : 'text-left'} space-y-8`}
          variants={itemVariants}
        >
          {/* Title */}
          <motion.h2 
            className="text-4xl sm:text-5xl lg:text-6xl font-heading font-bold text-neutral-900 leading-tight tracking-tight"
            variants={itemVariants}
          >
            {title.split(' ').map((word, index) => (
              <motion.span
                key={index}
                className="inline-block mr-3"
                whileHover={{ 
                  scale: 1.05,
                  color: "#14b8a6",
                  transition: { duration: 0.2 }
                }}
              >
                {word}
              </motion.span>
            ))}
          </motion.h2>
          
          {/* Description */}
          <motion.p 
            className="text-neutral-600 text-lg sm:text-xl font-body leading-relaxed max-w-prose"
            variants={itemVariants}
          >
            {description}
          </motion.p>
          
          {/* CTAs */}
          <motion.div 
            className={`flex flex-wrap gap-4 sm:gap-6 ${isCentered ? 'justify-center' : ''}`}
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
                  color={i === 0 ? "gradient" : "black"}
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
          className="flex-1 flex justify-center items-center relative"
          variants={imageVariants}
        >
          <div className="relative group">
            {/* Glow effect */}
            <div className="absolute inset-0 bg-gradient-to-br from-teal-500/20 via-transparent to-rose-500/20 rounded-2xl blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 -z-10" />
            
            {image.endsWith('.svg') ? (
              <motion.div
                className="relative p-12 bg-gradient-to-br from-neutral-50 to-neutral-100 rounded-3xl shadow-2xl border border-neutral-200/50"
                whileHover={{ 
                  scale: 1.05,
                  rotateY: 5,
                  rotateX: 5
                }}
                transition={{ type: "spring", stiffness: 300, damping: 20 }}
              >
                <Image
                  src={image}
                  alt={title}
                  width={120}
                  height={120}
                  className="w-24 h-24 sm:w-32 sm:h-32 opacity-80 drop-shadow-lg"
                />
                
                {/* Floating elements around icon */}
                <motion.div
                  className="absolute -top-2 -right-2 w-4 h-4 bg-teal-400 rounded-full"
                  animate={{
                    scale: [1, 1.2, 1],
                    opacity: [0.7, 1, 0.7]
                  }}
                  transition={{
                    duration: 2,
                    repeat: Infinity,
                    ease: "easeInOut"
                  }}
                />
                <motion.div
                  className="absolute -bottom-1 -left-1 w-3 h-3 bg-rose-400 rounded-full"
                  animate={{
                    scale: [1, 1.3, 1],
                    opacity: [0.6, 1, 0.6]
                  }}
                  transition={{
                    duration: 2.5,
                    repeat: Infinity,
                    ease: "easeInOut",
                    delay: 1
                  }}
                />
              </motion.div>
            ) : (
              <motion.div
                className="relative overflow-hidden rounded-2xl shadow-2xl"
                whileHover={{ 
                  scale: 1.02,
                  rotateY: 2,
                  rotateX: 2
                }}
                transition={{ type: "spring", stiffness: 300, damping: 20 }}
              >
                <img
                  src={image}
                  alt={title}
                  className="w-full h-auto max-w-lg object-cover"
                />
                
                {/* Overlay gradient */}
                <div className="absolute inset-0 bg-gradient-to-t from-black/10 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                
                {/* Shimmer effect */}
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000 ease-out" />
              </motion.div>
            )}
          </div>
        </motion.div>
      </div>
    </motion.section>
  );
}
