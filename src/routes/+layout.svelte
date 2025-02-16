<script>
  import "../app.css";
  import { scrollTo, scrollRef } from 'svelte-scrolling';
  import Header from '$lib/components/Header.svelte'; 

  export let data;
  const { stateNames, state_slug } = data || {};
  const buildTime = import.meta.env.BUILD_TIME;


  // Bind references to sections for scrolling
  let appSection;
  let aboutSection;
</script>

<!-- Main Section -->
<div bind:this={appSection} use:scrollRef={'app'} class="flex flex-col h-dvh">
  <Header {stateNames} {state_slug} />

  <section class="flex-grow overflow-y-scroll p-4">
    <slot></slot> <!-- Default slot for main content -->
  </section>
</div>

<!-- About Section -->
<div bind:this={aboutSection} use:scrollRef={'about'} class="h-dvh bg-white z-10">
  <header class="bg-white border-b border-slate-200 py-4 px-2">
    <h1 class="text-right">
      <a  
        class="ml-auto text-sm text-slate-600 hover:text-slate-900 transition-colors"
        use:scrollTo={'app'}>Back to data</a> 
    </h1>
  </header>
  <section class="flex-grow overflow-y-scroll p-4">
    <div class="max-w-prose mx-auto px-4 sm:px-6 lg:px-8 [&_a]:text-blue-600">
      <h1 class="text-3xl mb-4">About the ASPEP State Employment Explorer</h1>
      <p class="mb-8 italic">By David Eads / First created July 30, 2024; last updated {buildTime}.</p>
      <p class="mb-4">This data product visualizes the <a href="https://www.census.gov/programs-surveys/apes.html">Annual Survey of Public Employment & Payroll</a>, at the state level, broken down by <a href="https://observablehq.com/@themarshallproject/census-labor-data-release">government sector</a>, from 2003-2023, based on the <a href="https://www.themarshallproject.org/2024/07/25/how-to-investigate-the-trend-of-declining-prison-staff-and-deteriorating-conditions-behind-bars">toolkit released by The Marshall Project</a>.</p>
      <p class="mb-4">The code for this site is available on <a href="https://github.com/eads/apses/">Github</a>.</p>
      <p>

      <a  
        use:scrollTo={'app'}><b>Go back to the data.</b></a> 
      </p>
    </div>
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
