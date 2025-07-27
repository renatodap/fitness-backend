"use client";

import Link from "next/link";
import React from "react";

type ButtonProps = {
  href: string;
  children: React.ReactNode;
  variant?: "solid" | "outline";
  color?: "black" | "white" | "teal";
  className?: string;
};

export default function Button({
  href,
  children,
  variant = "solid",
  color = "black",
  className = "",
}: ButtonProps) {
  const base =
    "px-6 py-2 rounded-md text-sm font-medium transition text-center";

  let solid = "";
  let outline = "";

  switch (color) {
    case "white":
      solid = "bg-white text-black hover:bg-neutral-100 border border-neutral-200";
      outline = "border border-white text-white hover:bg-white hover:text-black";
      break;
    case "teal":
      solid = "bg-teal-500 text-white hover:bg-teal-600";
      outline = "border border-teal-500 text-teal-500 hover:bg-teal-500 hover:text-white";
      break;
    default:
      solid = "bg-black text-white hover:opacity-90";
      outline = "border border-black text-black hover:bg-black hover:text-white";
      break;
  }

  const style = `${base} ${variant === "solid" ? solid : outline} ${className}`;

  return (
    <Link href={href} className={style}>
      {children}
    </Link>
  );
}

