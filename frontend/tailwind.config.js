/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        base: "#F8FAFC", 
        glass: {
          bg: "rgba(255, 255, 255, 0.65)",
          border: "rgba(255, 255, 255, 0.8)",
        },
        pastel: {
          blue: "#e0f2fe",
          cyan: "#cffafe",
          emerald: "#d1fae5",
        }
      },
      boxShadow: {
        'glass': '0 8px 32px 0 rgba(31, 38, 135, 0.1)',
      },
      backdropBlur: {
        'glass': '12px',
      },
      fontFamily: {
        sans: ['"Segoe UI"', 'Tahoma', 'Geneva', 'Verdana', 'sans-serif'],
      }
    },
  },
  plugins: [],
}