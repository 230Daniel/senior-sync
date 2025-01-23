import { MdOutlineArrowRightAlt } from "react-icons/md";

import classes from './metricCards.module.css';
import { NavLink } from "react-router";

function MetricCard({ metric }) {

	const isStale = new Date(metric.value.timestamp) > new Date(Date.now() - 60 * 1000);
	const value = isStale ? "No data" : metric.value.value;
	const unit = isStale ? "" : metric.unit;
	const status = "green"; // TODO: Use actual value

	const textLength = String(value).length;
	const fontSize = (3 - Math.max(textLength - 3, 0) * 0.25) + "em";

	return (
		<>
			<NavLink to={`/metric/${metric.id}`} className={classes.card} style={{
				// @ts-ignore
				"--col-card-status": `var(--theme-col-status-${status})`
			}}>
				<span className={classes.metricName}>{metric.friendly_name}</span>
				<div className={classes.cardRow}>
					<span className={classes.metricValue} style={{ fontSize: fontSize }}>{value}</span>
					<span className={classes.metricUnit}>{unit}</span>
				</div>
				<div className={classes.corner}>
					<div className={classes.cornerArrow}>
						<MdOutlineArrowRightAlt size={25} />
					</div>
				</div>
			</NavLink >
		</>
	);
}

export default MetricCard;
