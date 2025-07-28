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

// Priority order: Most important projects first
export const projects: Project[] = [
  {
    id: 'accumulate-lite-client',
    title: 'Accumulate Lite Client',
    category: 'Internship',
    description:
      'A zero-knowledge-based light client for the Accumulate protocol, enabling trust-minimized state validation without full node data. Critical infrastructure for blockchain scalability.',
    timeframe: 'Summer 2024',
    role: 'Lead Developer (Internship, Solo)',
    status: 'Complete',
    tech: ['Rust', 'ZK Proofs', 'Protocol Buffers', 'CLI'],
    tags: ['Blockchain', 'Rust'],
    iconType: 'crypto',
    media: [
      {
        type: 'video',
        src: 'https://www.youtube.com/embed/your-video-id',
        alt: 'Video walkthrough of the Accumulate Lite Client',
      },
    ],
    links: {
      github: 'https://github.com/renatodap/accumulate-liteclient',
      video: 'https://youtube.com/your-video-link',
      page: '/software/accumulate-lite-client',
    },
  },
  {
    id: 'all-about-food-ai',
    title: 'All About Food AI',
    category: 'Capstone',
    description:
      'An AI-powered recipe recommendation system that analyzes user preferences and dietary restrictions to suggest personalized meal plans.',
    timeframe: 'Fall 2024 - Spring 2025',
    role: 'Team Lead (Capstone Project)',
    status: 'In Progress',
    tech: ['Python', 'TensorFlow', 'React', 'FastAPI', 'PostgreSQL'],
    tags: ['AI/ML', 'Capstone'],
    iconType: 'ai',
    media: [
      {
        type: 'image',
        src: '/images/food-ai-screenshot.png',
        alt: 'Screenshot of the All About Food AI interface',
      },
    ],
    links: {
      github: 'https://github.com/renatodap/all-about-food-ai',
    },
  },
  {
    id: 'os-design',
    title: 'Operating System Design',
    category: 'Academic',
    description:
      'A custom operating system kernel built from scratch, implementing process scheduling, memory management, and file system operations.',
    timeframe: 'Spring 2024',
    role: 'Solo Project (Academic)',
    status: 'Complete',
    tech: ['C', 'Assembly', 'QEMU', 'GDB'],
    tags: ['Systems', 'C'],
    iconType: 'system',
    media: [
      {
        type: 'image',
        src: '/images/os-terminal.png',
        alt: 'Terminal showing custom OS boot sequence',
      },
    ],
    links: {
      github: 'https://github.com/renatodap/custom-os',
    },
  },
  {
    id: 'comp-arch-design',
    title: 'Computer Architecture Design',
    category: 'Academic',
    description:
      'A RISC-V processor implementation with pipelining, hazard detection, and cache optimization. Includes performance analysis and benchmarking.',
    timeframe: 'Fall 2023',
    role: 'Solo Project (Academic)',
    status: 'Complete',
    tech: ['Verilog', 'RISC-V', 'ModelSim', 'FPGA'],
    tags: ['Hardware', 'Verilog'],
    iconType: 'hardware',
    media: [
      {
        type: 'image',
        src: '/images/processor-diagram.png',
        alt: 'Block diagram of the RISC-V processor design',
      },
    ],
    links: {
      github: 'https://github.com/renatodap/riscv-processor',
    },
  },
  {
    id: 'java-linter',
    title: 'Java Design Linter',
    category: 'Academic',
    description:
      'A static analysis tool for Java that detects violations of SOLID principles, design patterns, and code quality metrics using AST parsing.',
    timeframe: 'Spring 2024',
    role: 'Team of 2 (Lead Developer)',
    status: 'Complete',
    tech: ['Java', 'ANTLR', 'AST', 'Maven'],
    tags: ['Static Analysis', 'Java'],
    iconType: 'code',
    media: [
      {
        type: 'video',
        src: 'https://www.youtube.com/embed/your-linter-video-id',
        alt: 'Demo of the Java linter detecting design violations',
      },
    ],
    links: {
      github: 'https://github.com/renatodap/java-design-linter',
      video: 'https://youtube.com/your-linter-video',
    },
  },
  {
    id: 'digital-media-library',
    title: 'Digital Media Library',
    category: 'Academic',
    description:
      'A comprehensive database system for managing digital media collections with advanced search, tagging, and metadata extraction capabilities.',
    timeframe: 'Fall 2023',
    role: 'Team of 3 (Database Lead)',
    status: 'Complete',
    tech: ['PostgreSQL', 'Python', 'SQLAlchemy', 'Flask'],
    tags: ['Database', 'Python'],
    iconType: 'database',
    media: [
      {
        type: 'image',
        src: '/images/media-library-ui.png',
        alt: 'Screenshot of the digital media library interface',
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
      'A full-stack MERN application for gamers to track their backlog, rate games, and discover new titles with social features and recommendations.',
    timeframe: 'Fall 2024',
    role: 'Team of 3 (Backend Lead)',
    status: 'Complete',
    tech: ['MongoDB', 'Express', 'React', 'Node.js'],
    tags: ['Full Stack', 'MERN'],
    iconType: 'web',
    media: [
      {
        type: 'video',
        src: 'https://www.youtube.com/embed/your-gametracker-video-id',
        alt: 'Walkthrough of the Game Tracker application',
      },
    ],
    links: {
      github: 'https://github.com/renatodap/game-tracker-web',
      video: 'https://youtube.com/your-game-tracker-video',
    },
  },
  {
    id: 'jetpack-joyride',
    title: 'Jetpack Joyride Clone',
    category: 'Academic',
    description:
      'A Java-based recreation of the popular mobile game featuring object-oriented design patterns, collision detection, and smooth animations.',
    timeframe: 'Spring 2023',
    role: 'Solo Project (Academic)',
    status: 'Complete',
    tech: ['Java', 'JavaFX', 'OOP Design Patterns'],
    tags: ['Game Dev', 'Java'],
    iconType: 'game',
    media: [
      {
        type: 'image',
        src: '/images/jetpack-gameplay.png',
        alt: 'Screenshot of Jetpack Joyride clone gameplay',
      },
    ],
    links: {
      github: 'https://github.com/renatodap/jetpack-joyride-clone',
    },
  },
  {
    id: 'personal-website',
    title: 'This Website',
    category: 'Personal',
    description:
      'The design and development of this personal portfolio, built with Next.js and Framer Motion for a modern, interactive experience that showcases my work.',
    timeframe: 'Ongoing',
    role: 'Solo Project',
    status: 'In Progress',
    tech: ['Next.js', 'React', 'TypeScript', 'TailwindCSS', 'Framer Motion'],
    tags: ['Design', 'Portfolio'],
    iconType: 'design',
    media: [
      {
        type: 'image',
        src: '/images/website-screenshot.png',
        alt: 'Screenshot of the personal website homepage',
      },
    ],
    links: {
      github: 'https://github.com/renatodap/personalwebsite',
    },
  },
];
