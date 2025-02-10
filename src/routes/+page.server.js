// src/routes/+page.server.js
import { redirect } from '@sveltejs/kit';

export async function load({ fetch }) {
  const response = await fetch('/files/data/state_names.json');
  const stateNames = await response.json();
  const randomState = stateNames[Math.floor(Math.random() * stateNames.length)];
  throw redirect(302, `/${randomState.postalCode.toLowerCase()}`);
}
