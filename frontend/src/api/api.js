export async function getRoot() {
	const response = await fetch(__APP_BACKEND);
	return await response.text();
}
