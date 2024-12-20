import { useParams } from "react-router";

function Metric() {

	const { metricId } = useParams();

	return (
		<>
			<h1>Metric: {metricId}</h1>
			<p>This page is not implemented yet, but it will display the history of the {metricId} metric.</p>
		</>
	);
}

export default Metric;
