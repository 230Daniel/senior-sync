// Makes VSCode happy that a .module.css exists.

declare module '*.module.css' {
	const classes: { [key: string]: string };
	export default classes;
}
