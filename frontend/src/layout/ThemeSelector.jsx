import { createContext, useContext, useEffect, useState } from "react";

import { MdLightMode, MdDarkMode, MdOutlineContrast } from "react-icons/md";
import { useCookies } from "react-cookie";

import classes from "./themes.module.css";


export const Themes = [
	{
		name: "Dark Mode",
		className: classes.dark,
		icon: MdDarkMode,
		rsuiteId: "dark"
	},
	{
		name: "Light Mode",
		className: classes.light,
		icon: MdLightMode,
		rsuiteId: "light"
	},
	{
		name: "High Contrast Mode",
		className: classes.highContrast,
		icon: MdOutlineContrast,
		rsuiteId: "high-contrast"
	}
];

export const ThemeContext = createContext(null);

export function ThemeProvider({ children }) {

	// Initialise themeIndex state to the value of the themeIndex cookie if set, or 0.
	const [cookies, setCookie] = useCookies(["themeIndex"]);
	const [themeIndex, setThemeIndex] = useState(cookies.themeIndex ?? 0);

	// Effect to set themeIndex cookie whenever themeIndex state changes.
	useEffect(() => {
		setCookie("themeIndex", themeIndex, { expires: new Date("9999-01-01"), path: "/" });
	}, [themeIndex]);

	return <>
		<ThemeContext.Provider value={{ themeIndex: themeIndex, theme: Themes[themeIndex], setThemeIndex: setThemeIndex }}>
			{children}
		</ThemeContext.Provider>
	</>;
}

export function ThemeSelector() {
	const { themeIndex, theme, setThemeIndex } = useContext(ThemeContext);

	const nextThemeIndex = themeIndex + 1 >= Themes.length ? 0 : themeIndex + 1;
	const nextTheme = Themes[nextThemeIndex];

	return (
		<>
			{/* Render a div with the current theme class, this will set variables on :root due to the CSS :root:has(.theme). */}
			<button className={classes.selector} onClick={() => setThemeIndex(nextThemeIndex)}>
				<div className={theme.className} />
				<nextTheme.icon title={nextTheme.name} />
			</button>
		</>
	);
}
