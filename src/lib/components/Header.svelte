<script>
  import { scrollTo } from 'svelte-scrolling';
  export let stateNames = [];
  export let state_slug;

  // Redirect user to the selected state's page
  function handleStateSelect(event) {
    const selectedState = event.target.value;
    if (selectedState) {
      window.location.href = `/${selectedState}`;
    }
  }
</script>

<header class="bg-gradient-to-r from-indigo-800 to-purple-900 p-3 shadow-lg">
  <div class="flex justify-between items-center mb-2">
    <h1 class="text-white text-lg font-bold">State Employment Explorer</h1>
    <p class="text-white text-sm">
      <a class="underline decoration-dotted hover:decoration-solid transition ease-in-out" use:scrollTo={'about'}>Learn more</a>
    </p>
  </div>
  <select class="text-sm w-full p-1 bg-white text-gray-700 border border-gray-300 rounded-lg shadow-md hover:border-blue-500 focus:outline-none focus:border-blue-500 transition ease-in-out" on:change="{handleStateSelect}">
    {#each stateNames as state}
      <option value="{state.slug}" selected={state.slug === state_slug}>{state.state}</option>
    {/each}
  </select>
</header>
