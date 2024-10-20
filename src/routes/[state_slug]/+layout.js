export const prerender = true;

export async function load() {
  if (!import.meta.env.SSR) {
    return;
  }

  const fs = await import('fs');
  const path = await import('path');

  // Load state names from the file system (or wherever you store the JSON data)
  const allStatesDataFilePath = path.join(process.cwd(), 'static', 'state_employment.json');

  try {
    const data = JSON.parse(fs.readFileSync(allStatesDataFilePath, 'utf-8'));

    // Extract state names from the JSON data
    const stateNames = new Set(data.map(d => d.state));
    return { stateNames };
  } catch (err) {
    console.error('Error reading or parsing state employment data:', err);
    return {
      status: 500,
      error: new Error('Error reading or parsing state employment data')
    };
  }
}
