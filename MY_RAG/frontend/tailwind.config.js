/** @type {import('tailwindcss').Config} */
export default {
	content: [
		"./index.html", // Scan your main HTML file
		"./src/**/*.{js,jsx,ts,tsx}", // Scan all JS/TS/React files in src/
	],
	theme: {
		extend: {},
	},
	plugins: [],
};
