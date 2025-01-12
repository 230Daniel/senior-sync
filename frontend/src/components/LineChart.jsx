import { useState } from "react";
import { CartesianGrid, Line, LineChart, ReferenceArea, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import classes from "./metricGraph.module.css";

function getNumberOfTicksWithDivisor(start, end, divisor) {
	return Math.floor((end - start) / divisor) + 1;
}

function getTicksWithDivisor(start, end, divisor) {
	const ticks = Array.from(
		{ length: getNumberOfTicksWithDivisor(start, end, divisor) },
		(value, index) => start + index * divisor);

	ticks.push(end);
	return ticks;
}

function sum(arr) {
	return arr.reduce((a, b) => a * b, 1);
}

function getTicks(start, end, minTicks, maxTicks) {
	let multipliers = [
		1000, // seconds
		5, // 5 seconds,
		3, // 15 seconds,
		4, // minutes
		5, // 5 minutes,
		3, // 15 minutes,
		4, // hours,
		24, // days,
		365 // years
	];

	while (getNumberOfTicksWithDivisor(start, end, sum(multipliers)) < minTicks) {
		if (multipliers.length == 1) break;

		// Increase number of ticks by removing a multiplier.
		multipliers.pop();
	}

	multipliers[multipliers.length - 1] = multipliers[multipliers.length - 1] + 1;

	while (getNumberOfTicksWithDivisor(start, end, sum(multipliers)) > maxTicks) {
		multipliers[multipliers.length - 1] = multipliers[multipliers.length - 1] + 1;
	}

	const divisor = sum(multipliers);
	return [getTicksWithDivisor(start, end, divisor), divisor];
}

export default function MyLineChart({ data, timeRange, onTimeRangeSelected, unit }) {
	const start = timeRange[0].getTime();
	const end = timeRange[1].getTime();

	const [ticks, tickDivisor] = getTicks(start, end, 8, 8);

	const CustomizedTick = ({ x, y, stroke, payload }) => {
		const date = new Date(payload.value);

		const previousTickDay = new Date(payload.value - tickDivisor).toDateString();
		const thisTickDay = new Date(payload.value).toDateString();
		const newDay = thisTickDay != previousTickDay;

		const showDate = payload.value == start || payload.value == end || newDay;

		const showSeconds = date.getSeconds() > 0;

		const dateStr = date.toLocaleDateString();
		const timeStr = date.toLocaleTimeString([], {
			hour: '2-digit',
			minute: '2-digit',
			second: showSeconds ? '2-digit' : undefined
		});

		const lineOne = showDate ? dateStr : timeStr;
		const lineTwo = showDate ? timeStr : null;

		return (
			<g transform={`translate(${x},${y})`}>
				<text x={0} y={0} dy={16} fill="var(--theme-col-chart-axis)">
					<tspan textAnchor="middle" x="0">
						{lineOne}
					</tspan>
					{lineTwo &&
						<tspan textAnchor="middle" x="0" dy="20">
							{lineTwo}
						</tspan>
					}
				</text>
			</g>
		);
	};

	const [selectionLeft, setSelectionLeft] = useState(null);
	const [selectionRight, setSelectionRight] = useState(null);

	const [timeRangeHistory, setTimeRangeHistory] = useState([]);

	const includedData = data.filter((datapoint) => datapoint.timestamp >= start && datapoint.timestamp <= end);

	return <>
		<p>
			Left click and drag to zoom in, right click to zoom back out.
		</p>
		<ResponsiveContainer width="100%" height={400}>
			<LineChart
				data={includedData}
				onMouseDown={(chart, event) => {
					if (event.button == 0) {
						setSelectionLeft(chart.activeLabel);
					} else if (event.button == 2) {
						if (timeRangeHistory.length > 0) {
							const newTimeRange = timeRangeHistory[0];
							setTimeRangeHistory(timeRangeHistory.slice(1));
							onTimeRangeSelected(newTimeRange);
							return true;
						}
					}
				}}
				onMouseMove={(chart) => {
					if (selectionLeft) setSelectionRight(chart.activeLabel);
				}}
				onMouseUp={() => {
					setSelectionLeft(null);
					setSelectionRight(null);
					if (!selectionLeft || !selectionRight || selectionLeft >= selectionRight) return;

					setTimeRangeHistory([timeRange, ...timeRangeHistory]);
					const newTimeRange = [new Date(selectionLeft), new Date(selectionRight)];
					onTimeRangeSelected(newTimeRange);
				}}
				onContextMenu={(chart, event) => { event.preventDefault(); }}>
				<CartesianGrid
					horizontal={false}
					verticalValues={ticks.slice(1)}
					strokeDasharray="4"
					stroke="var(--theme-col-chart-grid)" />
				<Line
					type="monotone"
					dataKey="value"
					connectNulls={false}
					dot={includedData.length <= 128}
					animationDuration={300}
					stroke="var(--theme-col-primary)"
					strokeWidth={1.5}
				/>
				<XAxis
					dataKey="timestamp"
					type="number"
					domain={[start, end]}
					tick={CustomizedTick}
					ticks={ticks}
					interval={0}
					stroke="var(--theme-col-chart-axis)"
				/>
				<YAxis stroke="var(--theme-col-chart-axis)" />
				<Tooltip
					animationDuration={0}
					labelFormatter={(label, payload) => { return (new Date(label)).toLocaleString(); }}
					formatter={(value, name, props) => ["", `${value} ${unit}`]}
					separator=""
					wrapperClassName={classes.tooltip} />

				{selectionLeft && selectionRight && selectionRight > selectionLeft &&
					<ReferenceArea
						yAxisId="0"
						x1={selectionLeft.getTime()}
						x2={selectionRight.getTime()}
						fill="var(--theme-col-chart-brush)" />
				}
			</LineChart>
		</ResponsiveContainer>
	</>;
};
