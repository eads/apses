<script>
  import Slider from '$lib/components/Slider.svelte';

  export let data;
 
  let categories = [
    ['ft_employment', 'national_avg_employment'],
    ['ft_pay_per_ft_employee', 'national_avg_pay_per_employee'],
    ['ft_pay', 'national_avg_pay'],
  ]; // Data categories to show

  console.log(data);

  // const { stateData, stateSlug, stateNames, summaries } = data;
  // const stateName = stateNames.find(state => state.postalCode === stateSlug).state;

  // console.log(data);

  // const nonSummaries = Object.entries(stateData).slice(9);
</script>

<div class="min-h-screen bg-white p-1 sm:p-1 lg:px-4 lg:py-6">
 
  <h1 class="text-3xl font-bold text-gray-800 mb-4">
    {stateName}
  </h1>

  {#each summaries as row, idx}
  <div class="flex flex-col md:flex-row gap-4 lg:gap-12 mb-12">
    <div class="flex-1">
      <h1 class="text-md font-bold">{row.gov_function}</h1>
      <Slider
        data={stateData[row.gov_function].timeseries}
        categories={categories}
      />
      {#if idx === 0}
        <div class="sm:hidden flex justify-center items-center text-zinc-500 text-xs font-semibold px-3 py-1 rounded-full mx-auto w-fit my-2">
          <span>← SWIPE TO SEE OTHER VARIABLES →</span>
        </div>
      {/if}
    </div>
    <div class="md:mb-0 md:mt-8 xl:w-2/6">
      <p class="text-sm [&>a]:text-blue [&>a]:underline">
        {@html row.summary}
      </p>
    </div>
  </div>
  {/each}
  {#each nonSummaries as [gov_function, row]}
  <div class="flex flex-col md:flex-row gap-4 lg:gap-12 mb-12">
    <div class="flex-1">
      <h1 class="text-md font-bold">{gov_function}</h1>
      <Slider
        data={row.timeseries}
        categories={categories}
      />
    </div>
    <div class="md:mb-0 md:mt-10 lg:w-2/6">
      <p class="text-center text-xs md:text-sm">
        ——
      </p>
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