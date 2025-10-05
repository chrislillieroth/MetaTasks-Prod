/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './apps/ui/templates/**/*.{html,js}',
    './apps/ui/components/**/*.{html,js}',
    './apps/ui/layouts/**/*.{html,js}',
    './apps/ui/partials/**/*.{html,js}',
  ],
  theme: {
    extend: {
      colors: {
        accent: 'var(--color-accent)',
        danger: 'var(--color-danger)',
        surface: 'var(--color-surface)',
      },
      spacing: {
        '18': '4.5rem',
      },
    },
  },
  safelist: [
    { pattern: /bg-(green|red|yellow|blue)-(100|500|700)/ },
    { pattern: /text-(green|red|yellow|blue)-(600|800)/ },
  ],
  plugins: [
    require('@tailwindcss/forms'),
  ],
};
