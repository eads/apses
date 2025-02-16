<script>
 export let data = [];
 export let categories = [];
 export let selected = false;
 export let labels = {
   ft_eq_employment: 'Full-time equivalent employment',
   pay_per_fte: 'Pay per full-time equivalent', 
   total_pay: 'Total pay',
 };
 const lastVal = data[data.length - 1];

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
</script>

<div class="grid grid-cols-1 md:grid-cols-3 gap-2">
  <!-- Headers -->
  <div class="flex md:hidden items-baseline text-xs text-gray-500 uppercase border-b border-gray-300 pb-1">
    <span class="w-[160px] shrink-0 text-left">Category</span>
    <span class="w-[90px] shrink-0 text-right">1yr %</span>
    <span class="w-[70px] shrink-0 text-right hidden md:block">1yr Δ</span>
    <span class="w-[90px] shrink-0 text-right">5yr %</span>
    <span class="w-[70px] shrink-0 text-right hidden md:block">5yr Δ</span>
  </div>

 {#each categories as [state_cat, natl_cat], i}
   {@const isPayCategory = state_cat.includes('pay') || state_cat.includes('fte')}
     <div class="space-y-2 mb-3">
       <!-- State row -->
       <div class="flex items-center">
         <span class="w-[160px] shrink-0 text-sm font-medium leading-tight">
           {labels[state_cat]}
         </span>
         <span class="w-[90px] shrink-0 text-lg font-semibold text-right {lastVal[state_cat + '_1yr_pct'] === null ? 'text-gray-400' : lastVal[state_cat + '_1yr_pct'] >= 0 ? 'text-green-600' : 'text-red-600'}">
           {formatPct(lastVal[state_cat + '_1yr_pct'])}
         </span>
         <span class="w-[70px] shrink-0 text-sm text-gray-500 text-right hidden md:block">
           {formatAbs(lastVal[state_cat + '_1yr_abs'], isPayCategory)}
         </span>
         <span class="w-[90px] shrink-0 text-lg font-semibold text-right {lastVal[state_cat + '_5yr_pct'] === null ? 'text-gray-400' : lastVal[state_cat + '_5yr_pct'] >= 0 ? 'text-green-600' : 'text-red-600'}">
           {formatPct(lastVal[state_cat + '_5yr_pct'])}
         </span>
         <span class="w-[70px] shrink-0 text-sm text-gray-500 text-right hidden md:block">
           {formatAbs(lastVal[state_cat + '_5yr_abs'], isPayCategory)}
         </span>
       </div>

       <!-- National row -->
       <div class="flex items-baseline">
         <span class="w-[160px] shrink-0 text-sm text-gray-500">
           Nat'l avg
         </span>
         <span class="w-[90px] shrink-0 text-sm text-right {lastVal[natl_cat + '_1yr_pct'] === null ? 'text-gray-400' : lastVal[natl_cat + '_1yr_pct'] >= 0 ? 'text-green-600' : 'text-red-600'}">
           {formatPct(lastVal[natl_cat + '_1yr_pct'])}
         </span>
         <span class="w-[70px] shrink-0 text-sm text-gray-500 text-right hidden md:block">
           {formatAbs(lastVal[natl_cat + '_1yr_abs'], isPayCategory)}
         </span>
         <span class="w-[90px] shrink-0 text-sm text-right {lastVal[natl_cat + '_5yr_pct'] === null ? 'text-gray-400' : lastVal[natl_cat + '_5yr_pct'] >= 0 ? 'text-green-600' : 'text-red-600'}">
           {formatPct(lastVal[natl_cat + '_5yr_pct'])}
         </span>
         <span class="w-[70px] shrink-0 text-sm text-gray-500 text-right hidden md:block">
           {formatAbs(lastVal[natl_cat + '_5yr_abs'], isPayCategory)}
         </span>
       </div>
   </div>
 {/each}
</div>