<script>
  import Slider from '$lib/components/Slider.svelte';

  export let data;
 
  let categories = [
    ['ft_eq_employment', 'national_ft_eq_employment'],
    // ['ft_eq_employment_1yr_abs', 'national_ft_eq_employment_1yr_abs'],
    // ['ft_eq_employment_5yr_abs', 'national_ft_eq_employment_5yr_abs'],
    ['pay_per_fte', 'national_pay_per_fte'],
    // ['pay_per_fte_1yr_pct', 'national_pay_per_fte_1yr_pct'],
    // ['pay_per_fte_5yr_pct', 'national_pay_per_fte_5yr_pct'],
    ['total_pay', 'national_total_pay'],
  ]; // Data categories to show


  const { stateData, stateSlug, stateNames } = data;
  const stateName = stateNames.find(state => state.postalCode.toLowerCase() === stateSlug).state;

  const govFunctions = Object.entries(stateData) //.filter(d => d[1] && d[1].timeseries && d[1].timeseries.length > 0);
  console.log(govFunctions);
  // const govFunctions = [];
</script>

<div class="min-h-screen bg-white p-1 sm:p-1 lg:px-4 lg:py-6">
 
  <h1 class="text-3xl font-bold text-gray-800 mb-4">
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
          <span>← SWIPE TO SEE OTHER VARIABLES →</span>
        </div>
      {/if}
    </div>
    <div class="md:mb-0 md:mt-8 xl:w-2/6">
      {#if row.summary}
        <p class="text-sm [&>a]:text-blue [&>a]:underline">{@html row.summary}</p>
      {:else}
        <p class="text-sm [&>a]:text-blue [&>a]:underline">No summary generated.</p>
      {/if}
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