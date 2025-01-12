import { useCallback, useEffect, useState } from "react";
import { useSearchParams } from "react-router";

export const useTimeRangeQueryState = (defaultStart, defaultEnd) => {
	const [searchParams, setSearchParams] = useSearchParams();

	const queryStart = new Date(parseInt(searchParams.get("start")));
	const queryEnd = new Date(parseInt(searchParams.get("end")));

	// @ts-ignore
	const [start, setStart] = useState(isNaN(queryStart) ? defaultStart : queryStart);
	// @ts-ignore
	const [end, setEnd] = useState(isNaN(queryEnd) ? defaultEnd : queryEnd);

	const setTimeRange = useCallback(
		(newStart, newEnd) => {
			setStart(newStart);
			setEnd(newEnd);
		},
		[searchParams]
	);

	useEffect(() => {
		searchParams.set("start", start.getTime());
		searchParams.set("end", end.getTime());
		history.replaceState("", "", `?${searchParams.toString()}`);

	}, [searchParams, start, end]);

	return [
		start,
		end,
		setTimeRange,
	];
};
