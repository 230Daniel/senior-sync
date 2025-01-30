import { useQuery } from "react-query";
import { useParams } from "react-router";

import { useCallback } from "react";

import { DateRangePicker, DefaultStartValue, DefaultEndValue } from "../components/DateRangePicker";
import MetricGraph from "../components/MetricGraph";

import { Backend, getSensor } from "../api/api";
import { useTimeRangeQueryState } from "../hooks/useTimeRangeQueryState";

import classes from "./metric.module.css";

export default function MetricPage() {

	const { metricId } = useParams();

	const { data: metric, isLoading, isError } = useQuery(["getSensor", metricId],
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
			<div className={classes.row}>
				<h1>{metric.friendly_name} Sensor</h1>

				<DateRangePicker value={timeRange} onChange={setTimeRange} />
			</div>

			<MetricGraph
				metric={metric}
				valueType={metric.value_type}
				timeRange={timeRange}
				onTimeRangeSelected={setTimeRange} />


			<p className={classes.hint}>
				{metric.value_type != "str" && <>Click and drag the graph to zoom in, right click to zoom back out.<br /></>}
				Use the time range selector in the top-right corner to choose another date.
			</p>

			<div className={classes.exportcontainer}>
				<a className={classes.export}
					href={new URL(`metrics/${metric._id}/export`, Backend).toString()}
					download={`Export_${metric._id}.csv`}
				>
					Export to CSV
				</a>
			</div>
		</>
	);
}
