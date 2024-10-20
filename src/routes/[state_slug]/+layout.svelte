<script>
  // Data passed from the layout or page load function
  export let data;

  // Access stateNames and state_slug from data
  const { stateNames, state_slug } = data || {};

  console.log('slug', state_slug);

  // Redirect user to the selected state's page
  function handleStateSelect(event) {
    const selectedState = event.target.value;
    if (selectedState) {
      window.location.href = `/${selectedState}`;
    }
  }
</script>

<nav class="navbar">
  <select on:change="{handleStateSelect}">
    {#each stateNames as state}
      <option value="{state.slug}" selected={state.slug === state_slug}>{state.state}</option>
    {/each}
  </select>
</nav>

<slot />
