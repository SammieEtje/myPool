/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './static/js/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        // Main Color Palette
        primary: '#F64740',        // Red Salsa - Primary action color
        'primary-dark': '#A3333D', // Upsdell Red - Darker variant
        secondary: '#477998',      // Queen Blue - Secondary elements
        dark: '#291F1E',          // Licorice - Dark backgrounds
        light: '#C4D6B0',         // Tea Green - Light accents

        // Extended palette for UI elements
        accent: {
          sage: '#C4D6B0',        // Light sage for highlights
          blue: '#477998',        // Blue grey for info
          red: '#F64740',         // Coral red for actions
          'deep-red': '#A3333D',  // Deep red for warnings
        },

        // Semantic colors
        success: '#C4D6B0',
        info: '#477998',
        warning: '#F64740',
        danger: '#A3333D',

        // Podium colors for F1 theme
        podium: {
          gold: '#FFD700',
          silver: '#C0C0C0',
          bronze: '#CD7F32',
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        display: ['Rajdhani', 'sans-serif'],
      },
      backgroundImage: {
        'gradient-primary': 'linear-gradient(135deg, #F64740 0%, #A3333D 100%)',
        'gradient-secondary': 'linear-gradient(135deg, #477998 0%, #C4D6B0 100%)',
      },
    },
  },
  plugins: [],
}

