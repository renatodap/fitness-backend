"use client";

import Link from "next/link";
import React, { useRef, useEffect } from "react";
import { motion } from "framer-motion";

type ButtonProps = {
  href: string;
  children: React.ReactNode;
  variant?: "solid" | "outline" | "ghost";
  color?: "black" | "white" | "teal" | "gradient";
  size?: "sm" | "md" | "lg";
  className?: string;
  magnetic?: boolean;
  shimmer?: boolean;
  disabled?: boolean;
};

export default function Button({
  href,
  children,
  variant = "solid",
  color = "black",
  size = "md",
  className = "",
  magnetic = true,
  shimmer = false,
  disabled = false,
}: ButtonProps) {
  const buttonRef = useRef<HTMLAnchorElement>(null);

  // Magnetic effect
  useEffect(() => {
    if (!magnetic || disabled) return;

    const button = buttonRef.current;
    if (!button) return;

    const handleMouseMove = (e: MouseEvent) => {
      const rect = button.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;
      
      const distance = Math.sqrt(x * x + y * y);
      const maxDistance = 100;
      
      if (distance < maxDistance) {
        const strength = (maxDistance - distance) / maxDistance;
        const moveX = (x / distance) * strength * 8;
        const moveY = (y / distance) * strength * 8;
        
        button.style.transform = `translate(${moveX}px, ${moveY}px) scale(1.02)`;
      } else {
        button.style.transform = 'translate(0, 0) scale(1)';
      }
    };

    const handleMouseLeave = () => {
      button.style.transform = 'translate(0, 0) scale(1)';
    };

    document.addEventListener('mousemove', handleMouseMove);
    button.addEventListener('mouseleave', handleMouseLeave);

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      button.removeEventListener('mouseleave', handleMouseLeave);
    };
  }, [magnetic, disabled]);

  // Base styles
  const baseStyles = "relative inline-flex items-center justify-center font-medium transition-all duration-300 ease-out overflow-hidden group focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed";
  
  // Size variants
  const sizeStyles = {
    sm: "px-4 py-2 text-sm rounded-lg",
    md: "px-6 py-3 text-base rounded-xl",
    lg: "px-8 py-4 text-lg rounded-2xl"
  };

  // Color and variant combinations
  let colorStyles = "";
  let hoverStyles = "";
  let focusStyles = "focus:ring-neutral-500";

  switch (color) {
    case "white":
      if (variant === "solid") {
        colorStyles = "bg-white text-neutral-900 border-2 border-neutral-300 shadow-xl font-semibold";
        hoverStyles = "hover:bg-neutral-50 hover:shadow-2xl hover:border-neutral-400 hover:scale-105";
        focusStyles = "focus:ring-neutral-400";
      } else if (variant === "outline") {
        colorStyles = "bg-white/10 backdrop-blur-sm text-white border-2 border-white font-semibold shadow-lg";
        hoverStyles = "hover:bg-white hover:text-neutral-900 hover:border-white hover:shadow-xl";
        focusStyles = "focus:ring-white";
      } else {
        colorStyles = "bg-white/20 backdrop-blur-sm text-white font-semibold";
        hoverStyles = "hover:bg-white/30";
        focusStyles = "focus:ring-white";
      }
      break;
      
    case "teal":
      if (variant === "solid") {
        colorStyles = "bg-gradient-to-r from-teal-500 to-teal-600 text-white shadow-lg shadow-teal-500/25";
        hoverStyles = "hover:from-teal-600 hover:to-teal-700 hover:shadow-xl hover:shadow-teal-500/40";
        focusStyles = "focus:ring-teal-500";
      } else if (variant === "outline") {
        colorStyles = "bg-transparent text-teal-500 border-2 border-teal-500";
        hoverStyles = "hover:bg-teal-500 hover:text-white hover:shadow-lg hover:shadow-teal-500/25";
        focusStyles = "focus:ring-teal-500";
      } else {
        colorStyles = "bg-transparent text-teal-500";
        hoverStyles = "hover:bg-teal-500/10";
        focusStyles = "focus:ring-teal-500";
      }
      break;
      
    case "gradient":
      if (variant === "solid") {
        colorStyles = "bg-gradient-to-r from-rose-400 via-teal-500 to-orange-400 text-white shadow-lg";
        hoverStyles = "hover:shadow-xl hover:scale-105";
        focusStyles = "focus:ring-teal-500";
      } else if (variant === "outline") {
        colorStyles = "bg-transparent text-transparent bg-clip-text bg-gradient-to-r from-rose-400 via-teal-500 to-orange-400 border-2 border-transparent bg-gradient-to-r from-rose-400 via-teal-500 to-orange-400";
        hoverStyles = "hover:shadow-lg";
        focusStyles = "focus:ring-teal-500";
      } else {
        colorStyles = "bg-transparent text-transparent bg-clip-text bg-gradient-to-r from-rose-400 via-teal-500 to-orange-400";
        hoverStyles = "hover:bg-gradient-to-r hover:from-rose-400/10 hover:via-teal-500/10 hover:to-orange-400/10";
        focusStyles = "focus:ring-teal-500";
      }
      break;
      
    default: // black
      if (variant === "solid") {
        colorStyles = "bg-neutral-900 text-white shadow-lg";
        hoverStyles = "hover:bg-neutral-800 hover:shadow-xl";
        focusStyles = "focus:ring-neutral-500";
      } else if (variant === "outline") {
        colorStyles = "bg-transparent text-neutral-900 border-2 border-neutral-900";
        hoverStyles = "hover:bg-neutral-900 hover:text-white hover:shadow-lg";
        focusStyles = "focus:ring-neutral-500";
      } else {
        colorStyles = "bg-transparent text-neutral-900";
        hoverStyles = "hover:bg-neutral-900/10";
        focusStyles = "focus:ring-neutral-500";
      }
      break;
  }

  const finalClassName = `
    ${baseStyles}
    ${sizeStyles[size]}
    ${colorStyles}
    ${hoverStyles}
    ${focusStyles}
    ${shimmer ? 'shimmer' : ''}
    ${className}
  `.trim().replace(/\s+/g, ' ');

  const buttonContent = (
    <>
      {/* Shimmer overlay */}
      {shimmer && (
        <div className="absolute inset-0 -top-px overflow-hidden rounded-xl">
          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000 ease-out" />
        </div>
      )}
      
      {/* Button content */}
      <span className="relative z-10 flex items-center gap-2">
        {children}
      </span>
      
      {/* Glow effect for gradient buttons */}
      {color === "gradient" && variant === "solid" && (
        <div className="absolute inset-0 bg-gradient-to-r from-rose-400 via-teal-500 to-orange-400 rounded-xl blur-xl opacity-0 group-hover:opacity-30 transition-opacity duration-300 -z-10" />
      )}
    </>
  );

  if (disabled) {
    return (
      <span className={`${finalClassName} cursor-not-allowed`}>
        {buttonContent}
      </span>
    );
  }

  return (
    <motion.div
      whileHover={{ scale: magnetic ? 1 : 1.02 }}
      whileTap={{ scale: 0.98 }}
      transition={{ type: "spring", stiffness: 400, damping: 17 }}
    >
      <Link
        ref={buttonRef}
        href={href}
        className={finalClassName}
        style={{
          transition: 'transform 0.3s cubic-bezier(0.23, 1, 0.32, 1)',
        }}
      >
        {buttonContent}
      </Link>
    </motion.div>
  );
}

