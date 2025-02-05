import { useQuery } from "react-query";
import { getAlerts } from "../api/api";

import classes from "./alerts.module.css";
import { NavLink } from "react-router";
import { createContext, useContext } from "react";
import { FiAlertTriangle } from "react-icons/fi";

export const AlertsContext = createContext(null);

export function AlertsProvider({ children }) {
    const { data: alerts, isLoading, isError } = useQuery("getAlerts", getAlerts, { refetchInterval: 5000 });

    return <>
        <AlertsContext.Provider value={{ alerts: alerts, isLoading: isLoading, isError: isError }}>
            {children}
        </AlertsContext.Provider>
    </>;
}

export function AlertsIcon() {
    const { alerts, isLoading, isError } = useContext(AlertsContext);

    const isAlert = !isLoading && !isError && alerts.length > 0;

    return (
        <NavLink to="/alerts" style={{ color: isAlert ? "var(--theme-col-status-red)" : "unset" }}>
            <FiAlertTriangle title="Alerts" />
        </NavLink>
    );
}

export default function Alerts() {
    const { alerts, isLoading, isError } = useContext(AlertsContext);

    if (isLoading) return <h1>Loading...</h1>;
    if (isError) return <h1>Sorry, something went wrong.</h1>;

    return (
        <div>
            <h1>Active Alerts</h1>
            {alerts.length == 0
                ? <p>There are no active alerts.</p>
                : alerts.map((alert, i) =>
                    <NavLink key={i} to={`/metric/${alert.sensor_id}`} className={classes.alert}>
                        <strong>{new Date(alert.timestamp).toLocaleString()}</strong>
                        {alert.message}
                    </NavLink>
                )}
        </div>
    );
};
