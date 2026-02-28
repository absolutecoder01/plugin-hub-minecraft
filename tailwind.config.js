// Twój tailwind.config.js
export default {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      // Add theme colors from astro ui library
      colors: {
        "block-dirt": "#835432",
        "block-grass-side": "#5A7D3F",
        "block-grass-top": "#7FBF4F",
        // ... reszta kolorów
      },
      spacing: {
        block: "0.25rem",
        "6-block": "1.5rem",
        "9-block": "2.25rem",
      },
      fontFamily: {
        minecraft: ['"Minecraftia"', "monospace"],
      },
    },
  },
  plugins: [],
};
