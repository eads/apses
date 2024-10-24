// src/routes/+page.server.js
import { redirect } from '@sveltejs/kit';

// Replace with your ipdata.co API key
const IPDATA_API_KEY = 'your_ipdata_api_key_here';

const stateNames = ['alabama', 'alaska', 'arizona', 'arkansas', 'california', /* ...other states... */ ];

export async function load({ fetch }) {
  try {
    const response = await fetch(`https://api.ipdata.co?api-key=${IPDATA_API_KEY}`);
    const data = await response.json();

    // Check if a state is returned
    const state = data.region?.toLowerCase();

    if (state && stateNames.includes(state)) {
      // Redirect to the corresponding state page
      throw redirect(302, `/${state}`);
    } else {
      // Pick a random state if no state is found or valid
      const randomState = stateNames[Math.floor(Math.random() * stateNames.length)];
      throw redirect(302, `/${randomState}`);
    }
  } catch (error) {
    // Handle error and fallback to a random state
    const randomState = stateNames[Math.floor(Math.random() * stateNames.length)];
    throw redirect(302, `/${randomState}`);
  }
}
