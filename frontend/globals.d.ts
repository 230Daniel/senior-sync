// Allows us to import css modules without the IDE throwing a tantrum.
declare module '*.module.css' {
	const classes: { [key: string]: string };
	export default classes;
}

// Global constant for the backend URL, set by the APP_BACKEND environment variable at compile time.
declare const __APP_BACKEND: string;
