export interface Project {
  id: string;
  title: string;
  category: string;
  description: string;
  longDescription?: string[];
  timeframe: string;
  role: string;
  status: 'Complete' | 'In Progress';
  tech: string[];
  tags: string[];
  iconType: 'crypto' | 'ai' | 'system' | 'hardware' | 'code' | 'database' | 'web' | 'game' | 'design';
  media: {
    type: 'image' | 'video';
    src: string;
    alt: string;
  }[];
  links?: {
    page?: string;
    github?: string;
    video?: string;
    live?: string;
  };
}

// Priority order: User-specified order
export const projects: Project[] = [
  {
    id: 'all-about-food-ai',
    title: 'All About Food AI',
    category: 'Capstone',
    description:
      'Capstone AI platform: a voice-controlled recipe engine built to personalize food through machine learning and real-time speech interaction.',
    timeframe: 'Fall 2025 - Spring 2026',
    role: 'Team Lead (Capstone Project)',
    status: 'In Progress',
    tech: ['Python', 'TensorFlow', 'React', 'FastAPI', 'PostgreSQL'],
    tags: ['AI/ML', 'Capstone'],
    iconType: 'ai',
    media: [
      {
        type: 'image',
        src: '/all-about-food.PNG',
        alt: 'All About Food AI interface showing recipe recommendations',
      },
    ],
    links: {
      github: 'https://github.com/renatodap/all-about-food-ai',
    },
  },
  {
    id: 'accumulate-lite-client',
    title: 'Accumulate Lite Client',
    category: 'Internship',
    description:
      'Built during my Accumulate internship: a lightweight blockchain client giving edge-deployed AIs cryptographic identity and auditability through ADIs.',
    timeframe: 'Summer 2025',
    role: 'Lead Developer (Internship, Solo)',
    status: 'Complete',
    tech: ['Rust', 'ZK Proofs', 'Protocol Buffers', 'CLI'],
    tags: ['Blockchain', 'Rust'],
    iconType: 'crypto',
    media: [
      {
        type: 'image',
        src: '/acc-lite-client.png',
        alt: 'Accumulate Lite Client interface screenshot',
      },
    ],
    links: {
      github: 'https://github.com/renatodap/accumulate-liteclient',
      video: 'https://youtube.com/your-video-link',
      page: '/software/accumulate-lite-client',
    },
  },
  {
    id: 'personal-website',
    title: 'This Website',
    category: 'Personal',
    description:
      'A self-built, expressive portfolio showcasing systems, art, and identity — engineered with Next.js, Tailwind, and Framer Motion.',
    timeframe: 'Ongoing',
    role: 'Solo Project',
    status: 'In Progress',
    tech: ['Next.js', 'React', 'TypeScript', 'TailwindCSS', 'Framer Motion'],
    tags: ['Design', 'Portfolio'],
    iconType: 'design',
    media: [
      {
        type: 'image',
        src: '/dap.png',
        alt: 'Personal website homepage with hero section and project showcase',
      },
    ],
    links: {
      github: 'https://github.com/renatodap/personalwebsite',
    },
  },
  {
    id: 'digital-media-library',
    title: 'Digital Media Library',
    category: 'Academic',
    description:
      'A sample library database for musicians, built in SQL and Flask — with advanced tagging, stored procedures, and cascading integrity rules.',
    timeframe: 'Fall 2023',
    role: 'Team of 3 (Database Lead)',
    status: 'Complete',
    tech: ['PostgreSQL', 'Python', 'SQLAlchemy', 'Flask'],
    tags: ['Database', 'Python'],
    iconType: 'database',
    media: [
      {
        type: 'image',
        src: '/dap.png',
        alt: 'Digital Media Library interface with search and tagging features',
      },
    ],
    links: {
      github: 'https://github.com/renatodap/digital-media-library',
    },
  },
  {
    id: 'game-tracker',
    title: 'Game Tracker Web App',
    category: 'Academic',
    description:
      'Team-built MERN app to organize and review games — emphasizing teamwork, AI-assisted coding, and modern web architecture.',
    timeframe: 'Fall 2024',
    role: 'Team of 2 (Frontend Lead)',
    status: 'Complete',
    tech: ['SQLite', 'Express', 'React', 'Node.js'],
    tags: ['Full Stack', 'MERN'],
    iconType: 'web',
    media: [
      {
        type: 'image',
        src: '/dap.png',
        alt: 'Game Tracker web application showing game library and ratings',
      },
    ],
    links: {
      github: 'https://github.com/renatodap/game-tracker-web',
      video: 'https://youtube.com/your-game-tracker-video',
    },
  },
  {
    id: 'java-linter',
    title: 'Java Design Linter',
    category: 'Academic',
    description:
      'A static analysis engine that detects SOLID violations and design pattern misuse via bytecode parsing and AST traversal.',
    timeframe: 'Winter 2025',
    role: 'Team of 4',
    status: 'Complete',
    tech: ['Java', 'Maven'],
    tags: ['Static Analysis', 'Java'],
    iconType: 'code',
    media: [
      {
        type: 'image',
        src: '/dap.png',
        alt: 'Java Design Linter detecting code violations and suggestions',
      },
    ],
    links: {
      github: 'https://github.com/renatodap/java-design-linter',
      video: 'https://youtube.com/your-linter-video',
    },
  },
];
