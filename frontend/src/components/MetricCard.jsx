import { MdOutlineArrowRightAlt } from "react-icons/md";

import classes from './metricCards.module.css';
import { NavLink } from "react-router";

function MetricCard({ id, name, value, unit, status }) {

	const textLength = String(value).length;
	const fontSize = (3 - Math.max(textLength - 3, 0) * 0.25) + "em";

	return (
		<>
			<NavLink to={`/metric/${id}`} className={classes.card} style={{
				// @ts-ignore
				"--col-card-status": `var(--col-status-${status})`
			}}>
				<span className={classes.metricName}>{name}</span>
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
