/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                'mindmate-dark': '#0E1117',
                'mindmate-secondary': '#1A202C',
                'mindmate-accent': '#667EEA',
                'mindmate-text': '#E0E0E0',
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
            },
        },
    },
    plugins: [],
}
