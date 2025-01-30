import { useQuery } from "react-query";

import { getMetricHistory } from "../api/api";

import classes from "./metricGraph.module.css";
import LineChart from "./LineChart";
import { useEffect, useState } from "react";


export default function MetricGraph({ metric, valueType, timeRange, onTimeRangeSelected }) {

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
		["getMetricHistory", metric._id, maxTimeRange],
		async () => {
			return await getMetricHistory(metric._id, maxTimeRange[0], maxTimeRange[1]);
		},
		{
			refetchInterval: 10000
		}
	);

	if (isLoading) {
		return <div className={classes.placeholder}>
			Loading...
		</div>;
	}

	if (error) {
		return <div className={classes.placeholder}>
			Something went wrong.
		</div>;
	}

	const dataToPlot = new Array(0);
	let previousTimestamp = null;

	for (const dataPoint of dataPoints) {
		const timestamp = new Date(dataPoint.timestamp);

		const timeDifference = previousTimestamp
			? timestamp.getTime() - previousTimestamp.getTime()
			: 0;

		// Insert null point between this and the previous datapoint to create a gap.
		// if (timeDifference >= 60000 && valueType != "str") {
		// 	dataToPlot.push({
		// 		timestamp: new Date((timestamp.getTime() + previousTimestamp.getTime()) / 2),
		// 		value: null,
		// 		id: dataToPlot.length
		// 	});
		// }

		dataToPlot.push({
			timestamp: timestamp,
			value: dataPoint.value,
			id: dataPoint._id
		});

		previousTimestamp = timestamp;
	}

	if (valueType == "int" || valueType == "float") {
		return <>
			<LineChart data={dataToPlot} timeRange={timeRange} onTimeRangeSelected={onTimeRangeSelected} unit={metric.unit} />
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
