import { useQuery } from "react-query";

import { getMetricHistory } from "../api/api";

import classes from "./metricGraph.module.css";
import LineChart from "./LineChart";


export default function MetricGraph({ metricId, valueType, timeRange, onTimeRangeSelected }) {
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
