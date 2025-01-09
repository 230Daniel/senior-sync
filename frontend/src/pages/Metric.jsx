import { useQuery } from "react-query";
import { useParams } from "react-router";

import { getMetricHistory } from "../api/api";

import { DateRangePicker, DateRangePickerDefaultValue } from "../components/DateRangePicker";
import { useState } from "react";

export default function MetricPage() {

	const { metricId } = useParams();

	const [timeRange, setTimeRange] = useState(DateRangePickerDefaultValue);

	return (
		<>
			<h1>Metric: {metricId}</h1>

			<DateRangePicker value={timeRange} onChange={setTimeRange} />

			<MetricGraph metricId={metricId} timeRange={timeRange} />
		</>
	);
}

function MetricGraph({ metricId, timeRange }) {
	const { data, error, isLoading } = useQuery(
		[metricId, timeRange],
		async () => {
			return await getMetricHistory(metricId, timeRange[0], timeRange[1]);
		}
	);

	if (isLoading) {
		return "loading";
	}

	if (error) {
		return "error";
	}

	return <>
		<p>
			{data.map((value) => <>{value.timestamp} {value.value}<br /></>)}
		</p>
	</>;
}
