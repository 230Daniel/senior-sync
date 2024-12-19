import { useEffect, useState } from "react";

import { getRoot } from "../api/api";
import HealthMetrics from "../components/MetricCards";

function Home() {

    const [content, setContent] = useState(null);

    useEffect(() => {
        getRoot()
            .then(text => setContent(text))
            .catch(() => setContent("nothing, it threw an error!"));
    }, []);

    return (
        <>
            <h1>Senior Sync</h1>
            <p>The backend is {__APP_BACKEND}.</p>
            <p>The backend says {content ? content : "..."}</p>
            <h1 style={{ marginTop: "32px" }}>Health At a glance</h1>
            <HealthMetrics />
        </>
    );
}

export default Home;
