<script>
  export let data = [];
  export let categories = [];
  import { currentIndex } from '$lib/store.js';

  // Border colors based on index
  export let borderColors;
  
  // Table labels
  export let labels = {
    ft_eq_employment: 'FTE employment',
    pay_per_fte: 'Pay per FTE', 
    total_pay: 'Total pay',
  };
  
  let index;
  const lastVal = data[data.length - 1];

  currentIndex.subscribe(value => {
    index = value;
  });

  const formatPct = (value) => {
    if (value === null) return 'N/A';
    const sign = value >= 0 ? '+' : '';
    return `${sign}${(value * 100).toFixed(1)}%`;
  };

  const formatAbs = (value, isPayCategory) => {
    if (value === null) return '';
    const prefix = isPayCategory ? '$' : '';
    const sign = value >= 0 ? '+' : '';
    
    const num = Math.round(value);
    if (num >= 1000000) {
      return `${prefix}${sign}${Math.round(num / 1000000).toLocaleString()}M`;
    }
    if (num >= 1000) {
      return `${prefix}${sign}${Math.round(num / 1000).toLocaleString()}K`;
    }
    return `${prefix}${sign}${num.toLocaleString()}`;
  };

  const handleTableClick = (index) => {
    currentIndex.set(index);
  };
</script>

<div class="grid grid-cols-1 md:grid-cols-3 gap-2 mt-6 xl:gap-12 xl:mt-8">
  <!-- Mobile header -->
  <div class="flex md:hidden items-baseline text-xs text-gray-500 uppercase border-b border-gray-300">
    <span class="w-[110px] shrink-0 text-left">Category</span>
    <span class="w-[80px] shrink-0 text-right">1yr %</span>
    <span class="w-[60px] shrink-0 text-right hidden xl:block">1yr Δ</span>
    <span class="w-[80px] shrink-0 text-right">5yr %</span>
    <span class="w-[60px] shrink-0 text-right hidden xl:block">5yr Δ</span>
  </div>

  {#each categories as [state_cat, natl_cat], i}
    {@const isPayCategory = state_cat.includes('pay') || state_cat.includes('fte')}
    <div class="space-y-2 pt-1 pb-3 {i === index ? 'bg-gray-100 md:bg-transparent' : ''} border-l-[3px]" style="border-color: {borderColors[i]}" on:click={() => handleTableClick(i)}>
      <!-- Desktop header - now visible on lg breakpoint -->
      <div class="hidden xl:flex items-baseline text-xs text-gray-500 uppercase pb-1 px-2">
        <span class="w-[110px] shrink-0 text-left  border-b border-gray-300">Category</span>
        <span class="w-[80px] shrink-0 text-right border-b border-gray-300">1yr %</span>
        <span class="w-[60px] shrink-0 text-right border-b border-gray-300 xl:block">1yr Δ</span>
        <span class="w-[80px] shrink-0 text-right border-b border-gray-300">5yr %</span>
        <span class="w-[60px] shrink-0 text-right border-b border-gray-300 xl:block">5yr Δ</span>
      </div>

      <!-- State row -->
      <div class="flex items-center px-2">
        <span class="w-[110px] shrink-0 text-sm font-medium leading-tight">
          {labels[state_cat]}
        </span>
        <span class="w-[80px] shrink-0 text-lg font-semibold text-right {lastVal[state_cat + '_1yr_pct'] === null ? 'text-gray-400' : lastVal[state_cat + '_1yr_pct'] >= 0 ? 'text-green-600' : 'text-red-600'}">
          {formatPct(lastVal[state_cat + '_1yr_pct'])}
        </span>
        <span class="w-[60px] shrink-0 text-sm text-gray-500 text-right hidden xl:block">
          {formatAbs(lastVal[state_cat + '_1yr_abs'], isPayCategory)}
        </span>
        <span class="w-[80px] shrink-0 text-lg font-semibold text-right {lastVal[state_cat + '_5yr_pct'] === null ? 'text-gray-400' : lastVal[state_cat + '_5yr_pct'] >= 0 ? 'text-green-600' : 'text-red-600'}">
          {formatPct(lastVal[state_cat + '_5yr_pct'])}
        </span>
        <span class="w-[60px] shrink-0 text-sm text-gray-500 text-right hidden xl:block">
          {formatAbs(lastVal[state_cat + '_5yr_abs'], isPayCategory)}
        </span>
      </div>

      <!-- National row -->
      <div class="flex items-baseline px-2">
        <span class="w-[110px] shrink-0 text-sm text-gray-500">
          Nat'l avg
        </span>
        <span class="w-[80px] shrink-0 text-sm text-right {lastVal[natl_cat + '_1yr_pct'] === null ? 'text-gray-400' : lastVal[natl_cat + '_1yr_pct'] >= 0 ? 'text-green-600' : 'text-red-600'}">
          {formatPct(lastVal[natl_cat + '_1yr_pct'])}
        </span>
        <span class="w-[60px] shrink-0 text-sm text-gray-500 text-right hidden xl:block">
          {formatAbs(lastVal[natl_cat + '_1yr_abs'], isPayCategory)}
        </span>
        <span class="w-[80px] shrink-0 text-sm text-right {lastVal[natl_cat + '_5yr_pct'] === null ? 'text-gray-400' : lastVal[natl_cat + '_5yr_pct'] >= 0 ? 'text-green-600' : 'text-red-600'}">
          {formatPct(lastVal[natl_cat + '_5yr_pct'])}
        </span>
        <span class="w-[60px] shrink-0 text-sm text-gray-500 text-right hidden xl:block">
          {formatAbs(lastVal[natl_cat + '_5yr_abs'], isPayCategory)}
        </span>
      </div>
    </div>
  {/each}
</div>