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
    <p><b>Warning:</b> This page is a work in progress. AI-generated copy may be inaccurate and more recent data is available. Please check back soon for updates.</p>
    <slot></slot> <!-- Default slot for main content -->
  </section>
</div>

<!-- About Section -->
<div bind:this={aboutSection} use:scrollRef={'about'} class="h-dvh bg-white z-10">
  <header class="bg-gradient-to-r from-pink-800 to-purple-900 p-3 shadow-lg">
    <h1 class="text-white text-right">
      <a class="underline text-white" use:scrollTo={'app'}>Back to data</a> 
    </h1>
  </header>
  <section class="flex-grow overflow-y-scroll p-4">
    <div class="max-w-prose mx-auto px-4 sm:px-6 lg:px-8">
      <h1 class="text-3xl mb-4">About the State Employment Explorer</h1>
      <p class="mb-8 italic">By David Eads / First created July 30, 2024; last updated {buildTime}.</p>
      <p class="mb-4">These charts show the <a href="https://www.census.gov/programs-surveys/apes.html">Annual Survey of Public Employment & Payroll</a>, <a href="https://observablehq.com/@themarshallproject/census-labor-data-release">aggregated by state and government sector</a>, 2004-2022, based on the <a href="https://www.themarshallproject.org/2024/07/25/how-to-investigate-the-trend-of-declining-prison-staff-and-deteriorating-conditions-behind-bars">toolkit released by The Marshall Project</a>.</p>
      <p class="mb-4">2003 was chosen as the starting point to avoid odd spikes in 2001-2002 that appear to be the result of a category that came and went.</p>
      <p class="mb-4">The code for this site is available on <a href="https://github.com/eads/apses/">Github</a>.</p>
      <p></p>
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
