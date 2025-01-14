import { Backend } from "../api/api";
import HealthMetrics from "../components/MetricCards";

function Home() {
    return (
        <>
            <h1>Senior Sync</h1>
            <p>The backend is {Backend}.</p>
            <h1 style={{ marginTop: "32px" }}>Health at a glance</h1>
            <HealthMetrics />
        </>
    );
}

export default Home;
