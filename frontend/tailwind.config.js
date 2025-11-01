/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
        colors: {
            cielo_1: "#55A9E6",
            cielo_2: "#8CC5EE",
            cielo_3: "#A7D3F2",
            lila_4: "#ABA7F2",
            lila_5: "#918CEE",
            lila_6: "#5D55E6",
            gris_7: "#959595",
            rey_8: "#0909AC",
            crema_9: "#E2F3FB",
        }
    },
  },
  plugins: [],
}
