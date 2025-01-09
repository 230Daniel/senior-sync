import { useQuery } from "react-query";
import { useParams } from "react-router";

import { getMetricHistory } from "../api/api";

import { useState } from "react";

import LineChart from "../components/LineChart";
import { DateRangePicker, DateRangePickerDefaultValue } from "../components/DateRangePicker";

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
	const { data: dataPoints, error, isLoading } = useQuery(
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

	const dataToPlot = dataPoints.map((dataPoint) => {
		return {
			timestamp: new Date(dataPoint.timestamp),
			value: dataPoint.value
		};
	});

	if (dataToPlot.length) {

	}

	return <>
		<LineChart
			series={[{ dataKey: 'value', color: "var(--theme-col-primary)" }]}
			dataset={dataToPlot}
			xAxis={[{ dataKey: 'timestamp', scaleType: "utc", min: timeRange[0], max: timeRange[1] }]}
			yAxis={[{
				min: dataToPlot.length
					? dataToPlot.reduce((prev, curr) => prev.value < curr.value ? prev : curr).value - 10
					: null,
				max: dataToPlot.length
					? dataToPlot.reduce((prev, curr) => prev.value > curr.value ? prev : curr).value + 10
					: null
			}]}
			height={300}
		/>
	</>;
}
