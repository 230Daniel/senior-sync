import { useContext } from "react";

import { ThemeContext } from "../layout/ThemeSelector";
import { ThemeProvider } from "@mui/material";
import { LineChart as MuiLineChart } from "@mui/x-charts";

export default function LineChartx(props) {
	const { theme } = useContext(ThemeContext);

	return <>
		<ThemeProvider theme={theme.mui}>
			<MuiLineChart {...props} />
		</ThemeProvider>
	</>;
}
