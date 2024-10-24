export async function load({ params, fetch }) {
  const { state_slug } = params;

  // Fetch the state-specific data
  const response = await fetch(`/files/${state_slug}.json`);
  const stateData = await response.json();

  return {
    stateData
  };
}