"use client";

import React, { useState } from "react";
import Link from "next/link";

const HeroImage = () => {
  const [tapped, setTapped] = useState(false);

  const handleTap = () => {
    setTapped(true);
    setTimeout(() => setTapped(false), 300);
  };

  return (
    <Link href="/about">
      <div
        onClick={handleTap}
        className="relative inline-block group cursor-pointer"
      >
        {/* Pulsing image only — no ring */}
        <img
          src="/dap.png"
          alt="Renato DAP"
          className={`w-28 sm:w-36 h-auto mb-6 transition-transform duration-300 ease-in-out drop-shadow-xl animate-[pulseScale_2.5s_ease-in-out_infinite] ${
            tapped ? "rotate-3 scale-105" : ""
          } sm:group-hover:rotate-3 sm:group-hover:scale-105`}
        />
      </div>
    </Link>
  );
};

export default HeroImage;
