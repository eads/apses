export async function load({ fetch, params }) {
  // Fetch the list of states (could be from a static JSON file)
  const response = await fetch('/static/state_names.json');
  const stateNames = await response.json();
  return {
    stateNames, state_slug: params.state_slug
  };
}
