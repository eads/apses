<script>
  import { scrollTo, scrollRef} from 'svelte-scrolling';
  
  // Data passed from the layout or page load function
  export let data;

  // Access stateNames and state_slug from data
  const { stateNames, state_slug } = data || {};

  // Redirect user to the selected state's page
  function handleStateSelect(event) {
    const selectedState = event.target.value;
    if (selectedState) {
      window.location.href = `/${selectedState}`;
    }
  }
</script>

<nav class="navbar">
</nav>

<div use:scrollRef={'app'} class="flex flex-col h-dvh">
    <header class="bg-gray-800">
      <select on:change="{handleStateSelect}">
        {#each stateNames as state}
          <option value="{state.slug}" selected={state.slug === state_slug}>{state.state}</option>
        {/each}
      </select>
      <h1 class="text-white"><a class="underline" use:scrollTo={'about'}>Learn more</a></h1>
    </header>
    <section class="flex-grow overflow-y-scroll bg-zinc-200">
      <slot></slot>
    </section>
    <footer class="bg-green-900 text-white">
        <h1>Footer</h1>
    </footer>
</div>

<div use:scrollRef={'about'} class="h-dvh">
    <header class="bg-red-800 text-white">
        <h1><a class="underline" use:scrollTo={'app'}>Back to data</a></h1>
    </header>
    <section class="flex-grow overflow-y-scroll bg-zinc-200">
        <h1>About</h1>
        <slot name="state_notes"></slot>
        <p>About copy goes here.</p>
    </section>
</div>

<style>
  :global(*) {
    box-sizing: border-box;
  }
  :global(.virtual-list-wrapper) {
    flex: 1 1 0%;
  }

</style>


