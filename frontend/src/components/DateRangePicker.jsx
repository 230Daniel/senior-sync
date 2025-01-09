import { useContext } from 'react';
import { CustomProvider, DateRangePicker as RSuiteDateRangePicker } from 'rsuite';

import { ThemeContext } from "../layout/ThemeSelector";

import 'rsuite/DateRangePicker/styles/index.css';

function DateRangePicker(props) {
	const { theme } = useContext(ThemeContext);
	return <>
		<CustomProvider theme={theme.rsuiteId}>
			<RSuiteDateRangePicker
				showOneCalendar={true}
				format="MM/dd/yyyy HH:mm"
				{...props}
			/>
		</CustomProvider>

	</>;
}

export default DateRangePicker;
