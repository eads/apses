<script>
  import Carousel from 'svelte-carousel';
  import MiniLineChart from '$lib/components/MiniLineChart.svelte';
  import { currentIndex } from '$lib/store.js';

  export let data = {};
  export let categories = [];

  let index;
  let carousel;

  // Subscribe to currentIndex store
  currentIndex.subscribe(value => {
    index = value;
    if (carousel) {
      carousel.goTo(index);
    }
  });

  // Update store whenever the Carousel's page changes
  function handlePageChange(event) {
    currentIndex.set(event.detail);
    // No need to call carousel.goTo here
  }
</script>

<Carousel
  bind:this={carousel}
  on:pageChange={handlePageChange}
  infinite={false}
>
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