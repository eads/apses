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
  let showArrows = false;
  let showDots = true;

  const updateParticlesToShow = () => {
    const width = window.innerWidth;
    if (width >= 1600) {
      particlesToShow = 6;
      particlesToScroll = 6;
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
    <div class="flex-shrink-0 w-[90%] md:w-[75%] lg:w-[60%] p-2"> <!-- Wider chart container -->
      <MiniLineChart
        data={data}
        categories={[category, nationalCategory]} 
        height={190}
      />
      <h3 class="text-xs text-center font-normal text-gray-700">
        {category}
      </h3>
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