// app/components/software/Tag.tsx

'use client';

interface TagProps {
  text: string;
  isActive?: boolean;
  onClick?: () => void;
}

export function Tag({ text, isActive, onClick }: TagProps) {
  return (
    <button
      onClick={onClick}
      className={`
        px-3 py-1 text-sm font-medium rounded-full transition-all duration-200 
        ${onClick ? 'cursor-pointer' : ''}
        ${isActive
          ? 'bg-teal-500 text-white border-teal-500'
          : 'bg-neutral-100 text-neutral-700 border border-neutral-200 hover:bg-neutral-200/80'
        }
      `}
      disabled={!onClick}
    >
      {text}
    </button>
  );
}
