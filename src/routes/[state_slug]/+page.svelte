<script>
  import { groupBy } from 'micro-dash';
  import Slider from '$lib/components/Slider.svelte';

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
    // Prune empty categories for this gov_function
    if (Object.keys(acceptedGroups[gov_function]).length === 0) {
      delete acceptedGroups[gov_function];
    }
  });

  console.log('Accepted groups:', acceptedGroups);
</script>

<div class="min-h-screen bg-white p-4 sm:p-6 lg:p-8">
  <p class="mb-8 italic text-gray-700">
    This will be a note about the state if there is a note.
  </p>

  {#each Object.keys(acceptedGroups) as gov_function}
    <div class="category-row mb-12">
      <h2 class="text-xl font-medium uppercase mb-4 text-gray-800">
        {gov_function}
      </h2>
      <Slider
        data={acceptedGroups[gov_function]}
        categories={categories}
      />
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