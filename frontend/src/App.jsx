import { useEffect, useState } from "react";
import { Link } from "react-router";

import { getRoot } from "./api/api";

function App() {

    const [content, setContent] = useState(null);

    useEffect(() => {
        getRoot()
            .then(text => setContent(text))
            .catch(() => setContent("nothing, it threw an error!"));
    }, []);

    return (
        <>
            <h1>Senior Sync</h1>
            <Link to="/something">Go to something</Link>
            <p>The backend is {__APP_BACKEND}.</p>
            <p>The backend says {content ? content : "..."}</p>
        </>
    );
}

export default App;
