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

<div class="min-h-screen bg-white p-4 sm:p-6 lg:p-8">
  <p class="mb-8 italic text-gray-700">
    This will be a note about the state if there is a note.
  </p>

  {#each Object.keys(groupedByGovFunction) as gov_function}
    <div class="category-row mb-12">
      <h2 class="text-xl font-medium uppercase mb-4 text-gray-800">
        {gov_function}
      </h2>

      <!-- Container for Charts -->
      <div
        class="flex md:grid md:grid-cols-3 gap-4 overflow-x-auto md:overflow-visible snap-x snap-mandatory hide-scrollbar"
        use:swipe={handleSwipe}
      >
        {#each categories as category, index}
          <div
            class="flex-shrink-0 w-full md:w-auto p-2 snap-start"
            in:fly={{ x: 100, duration: 300 }}
            out:fly={{ x: -100, duration: 300 }}
          >
            <MiniLineChart
              data={groupedByGovFunction[gov_function]}
              xKey="year"
              yKey={category}
              height={150}
            />
            <h3 class="mt-2 text-md font-normal text-gray-700">
              {category}
            </h3>
          </div>
        {/each}
      </div>
    </div>
  {/each}
</div>

<style>
  /* Hide scrollbar for a cleaner look */
  .hide-scrollbar::-webkit-scrollbar {
    display: none;
  }
  .hide-scrollbar {
    -ms-overflow-style: none; /* IE and Edge */
    scrollbar-width: none; /* Firefox */
  }
</style>