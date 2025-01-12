import { useState } from "react";
import { CartesianGrid, Line, LineChart, ReferenceArea, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

function getNumberOfTicksWithDivisor(start, end, divisor) {
	return (end - start) / divisor + 1;
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

	let ticks;
	for (let i = 0; i < multipliers.length; i++) {
		ticks = getNumberOfTicksWithDivisor(start, end, sum(multipliers));
		if (ticks >= minTicks) break;

		// Increase number of ticks by removing a multiplier.
		multipliers.pop();
	}

	do {
		multipliers[multipliers.length - 1] = multipliers[multipliers.length - 1] + 1;
	} while (getNumberOfTicksWithDivisor(start, end, sum(multipliers)) > maxTicks);

	const divisor = sum(multipliers);
	return [getTicksWithDivisor(start, end, divisor), divisor];
}

export default function MyLineChart({ data, timeRange, onTimeRangeSelected }) {
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
				<text x={0} y={0} dy={16} fill="#666">
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

	return <>
		<ResponsiveContainer width="100%" height={400}>
			<LineChart
				data={data}
				onMouseDown={(chart, event) => {
					if (event.button == 0) {
						setSelectionLeft(chart.activeLabel);
					} else if (event.button == 2) {
						// restore history
					}
				}}
				onMouseMove={(chart) => {
					if (selectionLeft) setSelectionRight(chart.activeLabel);
				}}
				onMouseUp={() => {
					setSelectionLeft(null);
					setSelectionRight(null);
					if (!selectionLeft || !selectionRight || selectionLeft >= selectionRight) return;
					onTimeRangeSelected([new Date(selectionLeft), new Date(selectionRight)]);
				}}>
				<CartesianGrid strokeDasharray="4" horizontal={false} verticalValues={ticks} />
				<Line type="monotone" dataKey="value" dot={false} />
				<XAxis
					dataKey="timestamp"
					type="number"
					domain={[start, end]}
					tick={CustomizedTick}
					ticks={ticks}
					interval={0} />
				<YAxis />
				<Tooltip
					animationDuration={0}
					labelFormatter={(label, payload) => { return (new Date(label)).toLocaleString(); }} />

				{selectionLeft && selectionRight && selectionRight > selectionLeft &&
					<ReferenceArea yAxisId="0" x1={selectionLeft} x2={selectionRight} />
				}
			</LineChart>
		</ResponsiveContainer>
	</>;
};

