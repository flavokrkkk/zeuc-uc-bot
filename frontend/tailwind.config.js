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
        green: {
          100: "#2C7549",
          200: "#65C58C",
        },
        ["gray-dark"]: {
          100: "#727975",
          200: "#2F3231",
        },
      },
      screens: {
        xs: "400px",
      },
    },
  },
  plugins: [],
};
