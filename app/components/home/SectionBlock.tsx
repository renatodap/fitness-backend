'use client';

import Image from 'next/image';
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
  const isCentered = align === 'center';
  const reverse = align === 'right';

  return (
    <section className="py-24 px-6 sm:px-12">
      <div
        className={`max-w-[1600px] mx-auto w-[clamp(70%,90%,100%)] flex flex-col ${
          isCentered ? 'items-center text-center' : reverse ? 'md:flex-row-reverse' : 'md:flex-row'
        } gap-12 items-center`}
      >
        {/* === Text Block === */}
        <div className={`flex-1 ${isCentered ? '' : 'text-left'} space-y-6`}>
          <h2 className="text-3xl sm:text-4xl font-semibold text-neutral-900 font-heading">
            {title}
          </h2>
          <p className="text-neutral-600 text-base sm:text-lg font-body max-w-prose">
            {description}
          </p>
          <div className={`flex flex-wrap gap-4 ${isCentered ? 'justify-center' : ''}`}>
            {ctas.map((cta, i) => (
              <Button key={i} href={cta.href} variant={cta.variant}>
                {cta.label}
              </Button>
            ))}
          </div>
        </div>

        {/* === Image Block === */}
        <div className="flex-1 flex justify-center items-center">
          {image.endsWith('.svg') ? (
            <Image
              src={image}
              alt={title}
              width={100}
              height={100}
              className="w-20 h-20 sm:w-28 sm:h-28 opacity-80"
            />
          ) : (
            <img
              src={image}
              alt={title}
              className="rounded-xl shadow-lg max-w-full h-auto w-[min(100%,500px)]"
            />
          )}
        </div>
      </div>
    </section>
  );
}
