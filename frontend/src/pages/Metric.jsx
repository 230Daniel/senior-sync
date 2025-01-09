import { useQuery } from "react-query";
import { useParams } from "react-router";

import { getMetricHistory } from "../api/api";

import DateRangePicker from "../components/DateRangePicker";

function Metric() {

	const { metricId } = useParams();

	const { data, error, isLoading } = useQuery("data", async () => {
		return await getMetricHistory(metricId, new Date("2021-01-01"), new Date("2025-02-03"));
	});

	if (isLoading) {
		return "loading";
	}

	if (error) {
		return "error";
	}

	return (
		<>
			<h1>Metric: {metricId}</h1>
			<DateRangePicker />
			<p>
				{JSON.stringify(data)}
			</p>
		</>
	);
}

export default Metric;
