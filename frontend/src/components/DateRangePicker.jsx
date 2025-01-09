import { useContext } from 'react';
import { CustomProvider, DateRangePicker as RSuiteDateRangePicker } from 'rsuite';

import { ThemeContext } from "../layout/ThemeSelector";

import 'rsuite/DateRangePicker/styles/index.css';

let todayStart = new Date();
todayStart.setHours(0, 0, 0, 0);
let todayEnd = new Date();
todayEnd.setHours(23, 59, 59, 999);

export const DateRangePickerDefaultValue = [todayStart, todayEnd];

export function DateRangePicker(props) {
	const { theme } = useContext(ThemeContext);

	return <>
		<CustomProvider theme={theme.rsuiteId}>
			<RSuiteDateRangePicker
				showOneCalendar={true}
				format="dd/MM/yyyy HH:mm"
				shouldDisableDate={((date) => { return date > todayEnd; })}
				{...props}
			/>
		</CustomProvider>
	</>;
}
