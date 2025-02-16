<script>
  import Slider from '$lib/components/Slider.svelte';
  import SummaryStats from '$lib/components/SummaryStats.svelte';
  
  export let data;
  
  let categories = [
    ['ft_eq_employment', 'national_ft_eq_employment'],
    ['pay_per_fte', 'national_pay_per_fte'],
    ['total_pay', 'national_total_pay'],
  ]; // Data categories to show

  const { stateData, stateSlug, stateNames } = data;
  const stateName = stateNames.find(state => state.postalCode.toLowerCase() === stateSlug).state;

  const govFunctions = Object.entries(stateData);

  const colors = ["#4e79a7","#f28e2c","#e15759","#76b7b2","#59a14f","#edc949","#af7aa1","#ff9da7","#9c755f","#bab0ab"];
</script>

<div class="min-h-screen bg-white p-1 sm:p-1 lg:px-4">
 
  <h1 class="text-3xl font-bold text-gray-800 mb-4">
    {stateName}
  </h1>

  <p class="text-sm italic">Sorted descending by 2023 employees.</p>

  {#each govFunctions as [gov_function, row], idx}
  <div class="flex flex-col md:flex-row gap-4 lg:gap-12 mb-8 lg:py-12">
    <div class="flex-1">
      <h1 class="text-md font-bold">{gov_function}</h1>
      <Slider
        data={row.timeseries}
        categories={categories}
        colors={colors}
      />
      <SummaryStats 
        data={row.timeseries}
        categories={categories}
        borderColors={colors}
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