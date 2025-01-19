/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        dark: {
          100: "#090A0A",
          200: "#1C1E1D",
        },
      },
    },
  },
  plugins: [],
};
