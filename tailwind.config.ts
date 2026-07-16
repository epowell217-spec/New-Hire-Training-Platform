import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}', './lib/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          500: '#2c7be5',
          600: '#1f66c2',
          700: '#1a549d',
        },
      },
    },
  },
  plugins: [],
};

export default config;
