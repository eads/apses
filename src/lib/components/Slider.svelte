<script>
  import { onMount } from 'svelte';
  import { currentIndex } from '$lib/store.js';
  import Carousel from 'svelte-carousel';
  import MiniLineChart from '$lib/components/MiniLineChart.svelte';

  export let data = {};
  export let categories = [];
  export let colors = ["#4e79a7","#f28e2c","#e15759","#76b7b2","#59a14f","#edc949","#af7aa1","#ff9da7","#9c755f","#bab0ab"]

  let index;
  let carousel;
  let particlesToShow = 1;
  let particlesToScroll = 1;

  const updateParticlesToShow = () => {
    const width = window.innerWidth;
    if (width >= 1600) {
      particlesToShow = 6;
      particlesToScroll = 6;
    } else if (width >= 768) {
      particlesToShow = 3;
      particlesToScroll = 3;
    } else {
      particlesToShow = 1;
      particlesToScroll = 1;
    }
  };

  onMount(() => {
    updateParticlesToShow();
    window.addEventListener('resize', updateParticlesToShow);
    return () => window.removeEventListener('resize', updateParticlesToShow);
  });

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
  }
</script>

<Carousel
  bind:this={carousel}
  on:pageChange={handlePageChange}
  particlesToShow={particlesToShow}
  particlesToScroll={particlesToScroll}
  infinite={false}
  duration={400}
>
  {#each categories as category, i}
    <div class="flex-shrink-0 w-[90%] md:w-[75%] lg:w-[60%] p-2"> <!-- Wider chart container -->
      {#if data.hasOwnProperty(category)}
      <MiniLineChart
        data={data[category]}
        xKey="year"
        yKey={category}
        xDomain={[2004, 2022]}
        height={120}
        stroke={colors[i]}
      />
      <h3 class="mt-2 text-sm text-center font-normal text-gray-700">
        {category}
      </h3>
      {:else}
        <p class="text-center">Missing data for <code>{category}</code>.</p>
      {/if}
    </div>
  {/each}
</Carousel>

<style>
/* Adjust paddle sizes */
.carousel__paddle {
  width: 24px; /* Smaller width */
  height: 24px; /* Smaller height */
  background-color: rgba(0, 0, 0, 0.3); /* Customize paddle color */
}
</style>