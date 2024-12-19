function get(endpoint) {
	return fetch(new URL(endpoint, __APP_BACKEND));
}

export async function getRoot() {
	const response = await get("");
	return await response.text();
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
	];
}
