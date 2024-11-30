/** @type {import('tailwindcss').Config} */
export default {
  content: [
	"./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
		backgroundColor: {
			'l-blue': '#4F7CAC',
		},
		fontFamily: {
			mooli: ['Mooli', 'sans-serif']
		},
		colors: {
			'yellow': '#FFE6A5'
		}
	},
  },
  plugins: [],
}

