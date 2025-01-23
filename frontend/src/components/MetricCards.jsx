import MetricCard from "./MetricCard";

import { getAllMetrics } from "../api/api";

import classes from './metricCards.module.css';
import { useQuery } from "react-query";

function HealthMetrics() {

	const { data: metrics, isError, isLoading } = useQuery(
		[],
		getAllMetrics,
		{ refetchInterval: 1000 }
	);

	if (isLoading) {
		return <h2>Loading...</h2>;
	}

	if (isError) {
		return <h2>Error</h2>;
	}

	return (
		<>
			<div className={classes.cards}>
				{
					metrics.map((metric, i) => (
						<MetricCard key={i} metric={metric} />
					))
				}
			</div>
		</>
	);
}

export default HealthMetrics;
