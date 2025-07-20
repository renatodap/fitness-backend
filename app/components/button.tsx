"use client";

import Link from "next/link";
import React from "react";

type ButtonProps = {
  href: string;
  children: React.ReactNode;
  variant?: "solid" | "outline";
  className?: string;
};

export default function Button({
  href,
  children,
  variant = "solid",
  className = "",
}: ButtonProps) {
  const base =
    "px-6 py-2 rounded-md text-sm font-medium transition text-center";

  const solid =
    "bg-black text-white hover:opacity-90";
  const outline =
    "border border-black hover:bg-black hover:text-white";

  const style = `${base} ${
    variant === "solid" ? solid : outline
  } ${className}`;

  return (
    <Link href={href} className={style}>
      {children}
    </Link>
  );
}
