<script>
  import { onMount } from 'svelte';
  import { currentIndex } from '$lib/store.js';
  import Carousel from 'svelte-carousel';
  import MiniLineChart from '$lib/components/MiniLineChart.svelte';

  export let data = {};
  export let categories = [];
  
  export let colors = [];

  let index;
  let carousel;
  let particlesToShow = 1;
  let particlesToScroll = 1;
  let showArrows = false;
  let showDots = true;

  const updateParticlesToShow = () => {
    const width = window.innerWidth;
    if (width >= 1600) {
      particlesToShow = 3;
      particlesToScroll = 3;
      showDots = false;
      showArrows = false;
    } else if (width >= 768) {
      particlesToShow = 3;
      particlesToScroll = 3;
      showDots = false;
      showArrows = false;
    } else {
      particlesToShow = 1;
      particlesToScroll = 1;
      showDots = true;
      showArrows = false;
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
  
  const buttonLabels = ['Emp.', 'Pay/FTE', 'Tot. Pay'];
</script>

<Carousel
  bind:this={carousel}
  on:pageChange={handlePageChange}
  arrows={showArrows}
  dots={showDots}
  particlesToShow={particlesToShow}
  particlesToScroll={particlesToScroll}
  infinite={false}
  duration={400}
>
  {#each categories as [category, nationalCategory], i}
    <div class="flex-shrink-0 w-[90%] md:w-[75%] lg:w-[60%] md:pr-3 lg:pr-20 mt-4 mb-2"> <!-- Wider chart container -->
      <h3 class="text-xs font-normal text-gray-700">
        {category}
      </h3>
      <MiniLineChart
        data={data}
        categories={[category, nationalCategory]} 
        height={200}
        lineColor={colors[i]}
      />
    </div>
  {/each}

  <div slot="dots" class="custom-dots my-2">
    {#each categories as _, pageIndex (pageIndex)}
    <button
      class={`
        px-2 py-1 rounded-full text-sm font-medium mx-1 
        transition-all duration-200 focus:outline-none 
        focus:ring-2 focus:ring-offset-2 focus:ring-blue-500
        ${$currentIndex === pageIndex 
          ? 'bg-blue-600 text-white shadow-md hover:bg-blue-700' 
          : 'bg-gray-100 text-gray-600 hover:bg-gray-200 hover:text-gray-900'
        }
      `}
      class:selected={$currentIndex === pageIndex}
      on:click={() => carousel.goTo(pageIndex)}
    >
      {buttonLabels[pageIndex]}
    </button> 
    {/each}
  </div>

</Carousel>

<style>
/* Adjust paddle sizes */
.carousel__paddle {
  width: 24px; /* Smaller width */
  height: 24px; /* Smaller height */
  background-color: rgba(0, 0, 0, 0.3); /* Customize paddle color */
}
</style>