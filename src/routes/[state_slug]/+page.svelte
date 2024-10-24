<script>
  import MiniLineChart from '$lib/components/MiniLineChart.svelte';
  import { groupBy, mapValues, reduce } from 'micro-dash';
  import { swipe } from 'svelte-gestures';
  import { currentVariableIndex, variables } from '$lib/store.js';
  import { get } from 'svelte/store';
  import { fly } from 'svelte/transition';

  function handleSwipe(event) {
    let index = get(currentVariableIndex);
    if (event.direction === 'LEFT') {
      index = (index + 1) % variables.length;
    } else if (event.direction === 'RIGHT') {
      index = (index - 1 + variables.length) % variables.length;
    }
    currentVariableIndex.set(index);
  }

  export let data;
  
  let categories = ['ft_employment', 'ft_pay']; // Data categories to show

  const { stateData } = data;

  const processedData = stateData.map(item => {
    const newItem = { ...item };
    categories.forEach(category => {
      if (newItem[category] === null || newItem[category] === undefined) {
        newItem[category] = 0;
      }
    });
    return newItem;
  });

  const threshold = 50; // Set your threshold here

  // Step 1: Group data by 'gov_function'
  const groupedByGovFunction = groupBy(processedData, item => item.gov_function);

  // Initialize the acceptedGroups object
  const acceptedGroups = {};
  const rejectedSubGroups = []; // Array to store rejected sub-groups

  // Step 2: Process each 'gov_function' group
  Object.entries(groupedByGovFunction).forEach(([gov_function, items]) => {
    acceptedGroups[gov_function] = {}; // Initialize object for this gov_function

    // Process each category within this gov_function
    categories.forEach(category => {
      // Filter items where the category value is not zero
      const categoryItems = items.filter(item => item[category] !== 0);

      // Calculate the total sum of the category over all items
      const totalSum = categoryItems.reduce((sum, item) => sum + item[category], 0);

      if (totalSum >= threshold) {
        // Include this sub-group in acceptedGroups
        acceptedGroups[gov_function][category] = categoryItems;
      } else {
        // Collect rejected sub-groups
        rejectedSubGroups.push({
          gov_function,
          category,
          items: categoryItems,
          totalSum,
        });
      }
    });
  });

</script>

<p class="mb-8 italic">This will be a note about the state if there is a note.</p>

<!-- Loop over the grouped object keys -->
{#each Object.keys(groupedByGovFunction) as gov_function}
<!-- Repeat for each category -->
<div class="category-row">
  <h2 class="uppercase">{gov_function}</h2>
  <div 
    class="grid grid-cols-1 md:grid-cols-3 gap-4"
    in:fly={{ x: 100 }} out:fly={{ x: -100 }}
    use:swipe
    onSwipe={handleSwipe}
  >
    {#each categories as category}
      <MiniLineChart
        data={groupedByGovFunction[gov_function]}
        xKey="year"
        yKey={category}
        height={100}
      />
    {/each}
  </div>
</div>
{/each}