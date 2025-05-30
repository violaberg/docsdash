/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#305F6D',
          dark: '#263037',
        },
        secondary: {
          DEFAULT: '#698C8E',
        },
        accent: {
          DEFAULT: '#BF6E15',
          light: '#C1884E',
        },
        background: {
          light: '#F8F9FA',
          dark: '#263037',
        }
      }
    },
  },
  plugins: [],
}