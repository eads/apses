<!-- Header.svelte -->
<script>
  import { scrollTo } from 'svelte-scrolling';
  import { ChevronDown } from 'lucide-svelte';
  
  export let stateNames = [];
  export let state_slug;

  function handleStateSelect(event) {
    const selectedState = event.target.value;
    if (selectedState) {
      window.location.href = `/${selectedState}`;
    }
  }
</script>

<header class="bg-white border-b border-slate-200">
  <div class="w-full mx-auto px-4 py-2.5">
    <div class="flex items-center gap-4">
      <h1 class="text-slate-700 font-medium whitespace-nowrap text-sm md:text-base">ASPEP Explorer</h1>
      
      <div class="relative flex-1 max-w-xs">
        <select 
          class="w-full appearance-none bg-slate-50 text-slate-900 px-3 py-1.5 pr-8 rounded border border-slate-200 hover:border-slate-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 focus:outline-none transition-colors"
          on:change={handleStateSelect}
        >
          {#each stateNames as state}
            <option 
              value={state.postalCode.toLowerCase()} 
              selected={state.postalCode.toLowerCase() === state_slug}
            >
              {state.state}
            </option>
          {/each}
        </select>
        <ChevronDown class="absolute right-2.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 pointer-events-none" />
      </div>

      <a 
        use:scrollTo={'about'} 
        class="ml-auto text-sm text-slate-600 hover:text-slate-900 transition-colors"
      >
        Learn more
      </a>
    </div>
  </div>
</header>