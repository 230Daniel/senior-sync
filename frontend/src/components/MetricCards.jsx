import { useEffect, useState } from "react";
import MetricCard from "./MetricCard";

import { getCurrentMetrics } from "../api/api";

import classes from './metricCards.module.css';

function HealthMetrics() {

	const [metrics, setMetrics] = useState(null);

	function updateMetrics() {
		getCurrentMetrics().then(metrics => setMetrics(metrics));
	}

	useEffect(() => {
		updateMetrics();
		const intervalId = setInterval(updateMetrics, 10000);
		return () => clearInterval(intervalId);
	}, []);

	if (!metrics) {
		return <h2>Loading...</h2>;
	}

	return (
		<>
			<div className={classes.cards}>
				{
					metrics.map((metric, i) => (
						<MetricCard key={i} {...metric} />
					))
				}
			</div>
		</>
	);
}

export default HealthMetrics;
