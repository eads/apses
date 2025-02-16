<script>
  import Slider from '$lib/components/Slider.svelte';
  import SummaryStats from '$lib/components/SummaryStats.svelte';
  import { currentIndex } from '$lib/store.js';
  
  export let data;
 
  let categories = [
    ['ft_eq_employment', 'national_ft_eq_employment'],
    ['pay_per_fte', 'national_pay_per_fte'],
    ['total_pay', 'national_total_pay'],
  ]; // Data categories to show


  const { stateData, stateSlug, stateNames } = data;
  const stateName = stateNames.find(state => state.postalCode.toLowerCase() === stateSlug).state;

  const govFunctions = Object.entries(stateData).slice(4);

</script>

<div class="min-h-screen bg-white p-1 sm:p-1 lg:px-4 lg:py-6">
 
  <h1 class="text-3xl font-bold text-gray-800 mb-8">
    {stateName}
  </h1>

  {#each govFunctions as [gov_function, row], idx}
  <div class="flex flex-col md:flex-row gap-4 lg:gap-12 mb-12">
    <div class="flex-1">
      <h1 class="text-md font-bold">{gov_function}</h1>
      <Slider
        data={row.timeseries}
        categories={categories}
      />
      {#if idx === 0}
        <div class="sm:hidden flex justify-center items-center text-zinc-500 text-xs font-semibold px-3 py-1 rounded-full mx-auto w-fit my-2">
          <span>← SWIPE TO SEE OTHER CHARTS →</span>
        </div>
      {/if}
      <SummaryStats 
        data={row.timeseries}
        categories={categories}
      />
    </div>
  </div>
  {/each}
</div>

<style>
  a {
    color: #3182ce !important;
    text-decoration: underline;
  }
</style>