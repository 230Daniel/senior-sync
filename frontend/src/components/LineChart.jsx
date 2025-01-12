
import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

export default function MyLineChart({ data, timeRange }) {
	const start = timeRange[0].getTime();
	const end = timeRange[1].getTime();
	const ticks = Array.from({ length: (end - start) / 3600000 + 1 }, (value, index) => start + index * 3600000);

	console.log(ticks);

	return <>
		<ResponsiveContainer width="100%" height={400}>
			<LineChart data={data}>
				<CartesianGrid strokeDasharray="4" horizontal={false} verticalValues={ticks} />
				<Line type="monotone" dataKey="value" dot={false} />
				<XAxis
					dataKey="timestamp"
					type="number"
					domain={[start, end]}
					tickFormatter={(date) => (new Date(date)).toLocaleString()}
					ticks={timeRange}
					interval="preserveStartEnd"
					scale="time" />
				<YAxis />
				<Tooltip />
			</LineChart>
		</ResponsiveContainer>
	</>;
};
