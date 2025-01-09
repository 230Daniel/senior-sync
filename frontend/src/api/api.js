import { QueryClient as ReactQueryClient } from "react-query";

// The absolute path to the backend. If APP_BACKEND is /api/ this will become https://current.domain/api/.
export const Backend = new URL(__APP_BACKEND, window.location.href).href;

export const QueryClient = new ReactQueryClient({
	defaultOptions: {
		queries: {
			retry: false,
			refetchOnWindowFocus: false
		},
	}
});

async function get(endpoint) {
	const response = await fetch(new URL(endpoint, Backend));
	if (!response.ok) {
		throw new Error(`HTTP response code ${response.status} for endpoint ${endpoint}.`);
	}
	return response;
}

export async function getCurrentMetrics() {
	// TODO: Make this use the real endpoint once it exists.
	// const response = await get("current_metrics");
	// return await response.json();

	// Example response for now after 150ms.

	await new Promise(r => setTimeout(r, 150));

	function random(min, max) {
		return Math.round(Math.random() * (max - min) + min);
	}

	return [
		{ "id": "heart-rate", "name": "Heart Rate", "value": random(85, 95), "unit": "BPM", "status": "green" },
		{ "id": "oxygen-level", "name": "Oxygen Levels", "value": random(96, 99), "unit": "%", "status": "green" },
		{ "id": "blood-sugar", "name": "Blood Sugar", "value": random(79, 81), "unit": "mg/dl", "status": "red" },
		{ "id": "blood-pressure", "name": "Blood Pressure", "value": "102/72", "unit": "mmhg", "status": "green" },
		{ "id": "respiratory-rate", "name": "Respiratory Rate", "value": random(14, 16), "unit": "RPM", "status": "amber" },
		{ "id": "body-temperature", "name": "Body Temperature", "value": random(36, 38), "unit": "°C", "status": "green" },
		{ "id": "vibe-index", "name": "Vibe Index", "value": "No Data", "unit": "", "status": "gray" },
	];
}

export async function getSensor(metricId) {
	const response = await get(`sensors/${metricId}`);
	return await response.json();
}

export async function getMetricHistory(metricId, startTime, endTime) {
	let query = `?start_time=${startTime.toISOString()}`;
	if (endTime) {
		query += `&end_time=${endTime?.toISOString()}`;
	}

	const response = await get(`metrics/${metricId}/history${query}`);
	return await response.json();
}
