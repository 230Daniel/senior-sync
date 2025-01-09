import { useQuery } from "react-query";

import LineChart from "./LineChart";

import { getMetricHistory } from "../api/api";

export default function MetricGraph({ metricId, timeRange }) {
	const { data: dataPoints, error, isLoading } = useQuery(
		[metricId, timeRange],
		async () => {
			return await getMetricHistory(metricId, timeRange[0], timeRange[1]);
		},
		{
			refetchInterval: 10000
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
