const colors = {
  onyx: '#111827',
  slate: '#1f2937',
  obsidian: '#0b1220',
  neon: '#22d3ee'
};

/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: ['./src/**/*.{svelte,ts}'],
  theme: {
    extend: {
      colors: {
        background: colors.obsidian,
        surface: colors.slate,
        outline: '#374151',
        accent: colors.neon,
        muted: '#9ca3af'
      },
      boxShadow: {
        glow: '0 20px 60px rgba(34, 211, 238, 0.15)'
      },
      animation: {
        shimmer: 'shimmer 1.8s infinite'
      },
      keyframes: {
        shimmer: {
          '0%': { backgroundPosition: '-700px 0' },
          '100%': { backgroundPosition: '700px 0' }
        }
      }
    }
  },
  plugins: []
};
