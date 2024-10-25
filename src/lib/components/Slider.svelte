<script>
  import Carousel from 'svelte-carousel';
  import MiniLineChart from '$lib/components/MiniLineChart.svelte';
  import { currentIndex } from '$lib/store.js';

  export let data = {};
  export let categories = [];

  // Subscribe to currentIndex store
  let index;
  currentIndex.subscribe(value => {
    index = value;
  });

  // Update store whenever currentPageIndex changes
  function handlePageChange(event) {
    console.log('event', event.detail.currentPageIndex);
    currentIndex.set(event.detail.currentPageIndex);
  }
</script>

<Carousel>
  {#each categories as category, i}
    <div class="flex-shrink-0 w-full md:w-auto p-2">
      <MiniLineChart
        data={data[category]}
        xKey="year"
        yKey={category}
        height={150}
      />
      <h3 class="mt-2 text-md font-normal text-gray-700">
        {category}
      </h3>
    </div>
  {/each}
</Carousel>
