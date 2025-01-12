import { useCallback } from "react";
import { useSearchParams } from "react-router";
import { useNavigate, useLocation } from "react-router";

export const useTimeRangeQueryState = (defaultStart, defaultEnd) => {
	const [searchParams, setSearchParams] = useSearchParams();

	const setTimeRange = useCallback(
		(newStart, newEnd) => {
			searchParams.set("start", newStart.getTime());
			searchParams.set("end", newEnd.getTime());
			setSearchParams(searchParams, { replace: true });
		},
		[]
	);

	const queryStart = new Date(parseInt(searchParams.get("start")));
	const queryEnd = new Date(parseInt(searchParams.get("end")));

	// @ts-ignore
	const start = isNaN(queryStart) ? defaultStart : queryStart;
	// @ts-ignore
	const end = isNaN(queryEnd) ? defaultEnd : queryEnd;

	return [
		start,
		end,
		setTimeRange,
	];
};
