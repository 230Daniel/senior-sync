import { useQuery } from "react-query";
import { useParams, useSearchParams } from "react-router";

import { useCallback, useEffect, useState } from "react";

import { DateRangePicker, DefaultStartValue, DefaultEndValue } from "../components/DateRangePicker";
import MetricGraph from "../components/MetricGraph";

import { getSensor } from "../api/api";

export default function MetricPage() {

	const { metricId } = useParams();

	const { data: metric, isLoading, isError } = useQuery([metricId],
		async () => {
			return await getSensor(metricId);
		}
	);

	const [searchParams, setSearchParams] = useSearchParams();

	// timeRange is initialised to the query parameters
	// startTime and endTime if they're set, or default values for today if not.
	const [timeRange, internalSetTimeRange] = useState(() => {
		const paramsStartTime = parseInt(searchParams.get("startTime"));
		const paramsEndTime = parseInt(searchParams.get("endTime"));

		return [
			paramsStartTime ? new Date(paramsStartTime) : DefaultStartValue,
			paramsEndTime ? new Date(paramsEndTime) : DefaultEndValue,
		];
	});

	// Handling for the date picker sometimes using 999ms and sometimes 0ms.
	// Just set startTime to always use 0ms and endTime to always use 999ms.
	const setTimeRange = useCallback(([startTime, endTime]) => {
		startTime.setMilliseconds(0);
		endTime.setMilliseconds(999);
		internalSetTimeRange([startTime, endTime]);
	}, []);

	// This code looks absolutely atrocious, but it works great.
	// It sets the startTime and endTime query parameters if they're not the default.
	useEffect(() => {
		if (!timeRange
			|| (
				timeRange[0].getTime() == DefaultStartValue.getTime()
				&& timeRange[1].getTime() == DefaultEndValue.getTime()
			)) {
			searchParams.delete("startTime");
			searchParams.delete("endTime");
		} else {
			searchParams.set("startTime", timeRange[0].getTime().toString());
			searchParams.set("endTime", timeRange[1].getTime().toString());
		}

		setSearchParams(searchParams);
	}, [timeRange]);

	if (isLoading) return "loading";
	if (isError) return "error";

	return (
		<>
			<h1>{metric.friendly_name}</h1>

			<DateRangePicker value={timeRange} onChange={setTimeRange} />

			<MetricGraph metricId={metricId} timeRange={timeRange} />
		</>
	);
}
