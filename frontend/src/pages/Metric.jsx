import { useQuery } from "react-query";
import { useParams } from "react-router";

import { useState } from "react";

import { DateRangePicker, DateRangePickerDefaultValue } from "../components/DateRangePicker";
import MetricGraph from "../components/MetricGraph";

import { getSensor } from "../api/api";

export default function MetricPage() {

	const { metricId } = useParams();

	const { data: metric, isLoading, isError } = useQuery([metricId],
		async () => {
			return await getSensor(metricId);
		}
	);

	const [timeRange, setTimeRange] = useState(DateRangePickerDefaultValue);

	return (
		<>
			<h1>Metric: {metric?.friendly_name}</h1>

			<DateRangePicker value={timeRange} onChange={setTimeRange} />

			<MetricGraph metricId={metricId} timeRange={timeRange} />
		</>
	);
}
