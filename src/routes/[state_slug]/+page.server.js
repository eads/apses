export async function load({ params, fetch }) {
  const { state_slug: slug } = params;

  // Fetch Markdown as static file
  const summaryResponse = await fetch(`/files/summaries/${slug}_summary.json`);

  const summaries = await summaryResponse.json();

  // Fetch state data as usual
  const dataResponse = await fetch(`/files/data/${slug}_data.json`);
  const stateData = await dataResponse.json();

  return {
    summaries,
    stateData,
    stateSlug: slug,
  };
}