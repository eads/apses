<script>
  // `stateNames` is passed in from the layout's `load` function
  export let stateNames = [];

  console.log(stateNames)
  // Redirect user to the selected state's page
  function handleStateSelect(event) {
    const selectedState = event.target.value;
    if (selectedState) {
      window.location.href = `/${selectedState}`;
    }
  }
</script>

<nav class="navbar">
  <div class="navbar-title">
    <h1>Select a State</h1>
  </div>
  <div class="navbar-dropdown">
    <select on:change="{handleStateSelect}">
      <option value="" disabled selected>Select a state</option>
      {#each stateNames as state}
        <option value="{state}">{state}</option>
      {/each}
    </select>
  </div>
</nav>

<!-- Page content gets rendered here -->
<slot />

<style>
  .navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #333;
    color: white;
    padding: 1rem;
  }

  .navbar-title h1 {
    margin: 0;
  }

  .navbar-dropdown select {
    padding: 0.5rem;
    border: none;
    border-radius: 5px;
  }
</style>
