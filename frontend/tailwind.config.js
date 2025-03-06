/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        terminal: ["Meslo", "Consolas", "Monaco", "monospace"],
      },
    },
  },
  plugins: [],
};
