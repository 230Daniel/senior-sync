import { useQuery } from "react-query";

import { getMetricHistory } from "../api/api";

import classes from "./metricGraph.module.css";
import LineChart from "./LineChart";
import { useEffect, useState } from "react";


export default function MetricGraph({ metricId, valueType, timeRange, onTimeRangeSelected }) {

	const [maxTimeRange, setMaxTimeRange] = useState(timeRange);

	useEffect(() => {
		const newMaxTimeRange = [
			timeRange[0] < maxTimeRange[0] ? timeRange[0] : maxTimeRange[0],
			timeRange[1] > maxTimeRange[1] ? timeRange[1] : maxTimeRange[1]
		];

		if (JSON.stringify(newMaxTimeRange) != JSON.stringify(maxTimeRange)) {
			setMaxTimeRange(timeRange);
		}
	}, [timeRange]);

	const { data: dataPoints, error, isLoading } = useQuery(
		[metricId, maxTimeRange],
		async () => {
			return await getMetricHistory(metricId, maxTimeRange[0], maxTimeRange[1]);
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
			timestamp: new Date(dataPoint.timestamp).getTime(),
			value: dataPoint.value,
			id: dataPoint._id
		};
	});

	if (valueType == "int" || valueType == "float") {
		return <>
			<LineChart data={dataToPlot} timeRange={timeRange} onTimeRangeSelected={onTimeRangeSelected} />
		</>;
	}

	if (valueType == "str") {
		return <>
			<p>This metric is not supported for graphing. Here's a table of datapoints instead.</p>
			<table className={classes.table}>
				<tr>
					<th>Timestamp</th>
					<th>Value</th>
				</tr>
				{dataToPlot.map((datapoint) => {
					return <tr key={datapoint.id}>
						<td>{datapoint.timestamp.toLocaleDateString()} {datapoint.timestamp.toLocaleTimeString()}</td>
						<td>{datapoint.value}</td>
					</tr>;
				})}
			</table>
		</>;
	}

	throw new Error(`Unknown valueType ${valueType}`);
}
