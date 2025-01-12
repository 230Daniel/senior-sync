import { useQuery } from "react-query";
import { useParams } from "react-router";

import { useCallback } from "react";

import { DateRangePicker, DefaultStartValue, DefaultEndValue } from "../components/DateRangePicker";
import MetricGraph from "../components/MetricGraph";

import { getSensor } from "../api/api";
import { useTimeRangeQueryState } from "../hooks/useTimeRangeQueryState";

export default function MetricPage() {

	const { metricId } = useParams();

	const { data: metric, isLoading, isError } = useQuery([metricId],
		async () => {
			return await getSensor(metricId);
		}
	);

	const [start, end, internalSetTimeRange] = useTimeRangeQueryState(DefaultStartValue, DefaultEndValue);
	const timeRange = [start, end];

	// Handling for the date picker sometimes using 999ms and sometimes 0ms.
	// Just set startTime to always use 0ms and endTime to always use 999ms.
	const setTimeRange = useCallback(([startTime, endTime]) => {
		startTime.setMilliseconds(0);
		endTime.setMilliseconds(999);
		internalSetTimeRange(startTime, endTime);
	}, []);

	if (isLoading) return "loading";
	if (isError) return "error";

	return (
		<>
			<h1>{metric.friendly_name}</h1>

			<DateRangePicker value={timeRange} onChange={setTimeRange} />

			<MetricGraph
				metricId={metricId}
				valueType={metric.value_type}
				timeRange={timeRange}
				onTimeRangeSelected={setTimeRange} />
		</>
	);
}
