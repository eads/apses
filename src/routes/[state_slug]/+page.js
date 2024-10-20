import fs from 'fs';
import path from 'path';

export const prerender = true;

// Provide a list of slugs to prerender
export async function entries() {
  // Directory where JSON data files are stored
  const dataDirectory = path.join(process.cwd(), 'src', 'data');

  // Read the filenames in the data directory
  const files = fs.readdirSync(dataDirectory);

  // Create an array of state_slug values by removing '.json' from each filename
  const slugs = files
    .filter(file => file.endsWith('.json'))
    .map(file => ({ state_slug: file.replace('.json', '') }));

  return slugs.map(slug => ({ params: { state_slug: slug.state_slug } }));
}

export async function load({ params }) {
  if (!import.meta.env.SSR) {
    return;
  }

  const { state_slug } = params;

  // Dynamically import 'fs' and 'path' only on the server side
  const fs = await import('fs');
  const path = await import('path');

  // Resolve the path within `src/data/`
  const stateDataFilePath = path.join(process.cwd(), 'src', 'data', `${state_slug.toLowerCase()}.json`);

  // Log the resolved path for debugging
  console.log(`Resolved file path: ${stateDataFilePath}`);

  // Check if the file exists
  if (!fs.existsSync(stateDataFilePath)) {
    return {
      status: 404,
      error: new Error('State data file not found')
    };
  }

  try {
    const stateData = JSON.parse(fs.readFileSync(stateDataFilePath, 'utf-8'));
    return { stateData };
  } catch (err) {
    console.error('Error reading or parsing state data:', err);
    return {
      status: 500,
      error: new Error('Error reading or parsing state data')
    };
  }
}

