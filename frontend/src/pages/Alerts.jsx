import { useQuery } from "react-query";
import { getAlerts } from "../api/api";

import classes from "./alerts.module.css";
import { NavLink } from "react-router";

export default function Alerts() {
    const { data: alerts, isLoading, isError } = useQuery([], getAlerts);

    if (isLoading) return <h1>Loading...</h1>;
    if (isError) return <h1>Sorry, something went wrong.</h1>;

    return (
        <div>
            <h1>Active Alerts</h1>
            {alerts.length == 0
                ? <h2>There are no active alerts.</h2>
                : alerts.map((alert, i) =>
                    <NavLink key={i} to={`/metric/${alert.sensor_id}`} className={classes.alert}>
                        <strong>{new Date(alert.timestamp).toLocaleString()}</strong>
                        {alert.message}
                    </NavLink>
                )}
        </div>
    );
};
