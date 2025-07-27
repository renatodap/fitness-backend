// components/home/Footer.tsx

import Link from "next/link";

export default function Footer() {
  return (
    <footer className="mt-32 px-6 py-12 text-sm text-neutral-500 bg-white border-t border-neutral-200">
      <div className="max-w-4xl mx-auto flex flex-col sm:flex-row justify-between gap-6 sm:items-center">
        {/* Left side: Copyright */}
        <div>
          © {new Date().getFullYear()} Renato DAP. All rights reserved.
        </div>

        {/* Right side: Contact Links */}
        <div className="flex gap-4 sm:gap-6">
          <Link
            href="mailto:renato@example.com"
            className="hover:text-neutral-900 transition-colors"
          >
            Email
          </Link>
          <Link
            href="https://github.com/renatodap"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-neutral-900 transition-colors"
          >
            GitHub
          </Link>
          <Link
            href="https://www.linkedin.com/in/renatodap"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-neutral-900 transition-colors"
          >
            LinkedIn
          </Link>
        </div>
      </div>
    </footer>
  );
}
