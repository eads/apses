export async function load({ params, fetch }) {
  const { state_slug: slug } = params;

  const dataResponse = await fetch(`/files/data/${slug.toLowerCase()}_data.json`);
  const stateData = await dataResponse.json();

  return {
    stateData,
    stateSlug: slug,
  };
}