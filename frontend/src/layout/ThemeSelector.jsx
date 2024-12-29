import { useEffect, useState } from "react";

import { MdLightMode, MdDarkMode, MdOutlineContrast } from "react-icons/md";
import { useCookies } from "react-cookie";

import classes from "./themes.module.css";

export default function ThemeSelector() {
	const Themes = [
		{
			"name": "Dark Mode",
			"className": classes.dark,
			"icon": MdDarkMode
		},
		{
			"name": "Light Mode",
			"className": classes.light,
			"icon": MdLightMode
		},
		{
			"name": "High Contrast Mode",
			"className": classes.highContrast,
			"icon": MdOutlineContrast
		}
	];

	// Initialise themeIndex state to the value of the themeIndex cookie if set, or 0.
	const [cookies, setCookie] = useCookies(["themeIndex"]);
	const [themeIndex, setThemeIndex] = useState(cookies.themeIndex ?? 0);

	// Effect to set themeIndex cookie whenever themeIndex state changes.
	useEffect(() => {
		setCookie("themeIndex", themeIndex, { expires: new Date("9999-01-01") });
	}, [themeIndex]);

	const nextThemeIndex = themeIndex + 1 >= Themes.length ? 0 : themeIndex + 1;
	const nextTheme = Themes[nextThemeIndex];

	return (
		<>
			{/* Render a div with the current theme class, this will set variables on :root due to the CSS :root:has(.theme). */}
			<div className={Themes[themeIndex].className} />
			<button className={classes.selector} onClick={() => setThemeIndex(nextThemeIndex)}>
				<nextTheme.icon title={nextTheme.name} />
			</button>
		</>
	);
}
