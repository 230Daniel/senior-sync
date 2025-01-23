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

export async function getAllMetrics() {
	const response = await get(`metrics/all`);
	return await response.json();
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

export async function getAlerts() {
	const response = await get(`alerts`);
	return await response.json();
}
