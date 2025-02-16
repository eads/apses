<script>
  import { LayerCake, Svg, groupLonger, flatten } from 'layercake';
  import { scaleOrdinal } from 'd3-scale';
  import { format } from 'd3-format';
  import Line from '$lib/components/Line.svelte';
  import AxisX from '$lib/components/AxisX.svelte';
  import AxisY from '$lib/components/AxisY.svelte';

  export let data = [];  // Default to empty array instead of undefined
  export let categories = ['ft_employment', 'national_ft_employment'];
  export let height = 150;

  const xKey = 'year';
  const yKey = 'value';
  const zKey = 'category';
  
  // Validate data before processing
  $: validData = Array.isArray(data) ? data.filter(d => 
    d && typeof d === 'object' && 
    categories.some(cat => d[cat] !== undefined && d[cat] !== null) &&
    d[xKey] !== undefined && d[xKey] !== null && d[xKey] >= 2008
  ) : [];

  const formatLabelX = d => d ? `'${String(d - 2000).padStart(2, '0')}` : '';
  
  let formatLabelY;

  if (categories[0].endsWith("pct")) {
    formatLabelY = d => d !== null && d !== undefined ? format(`.1%`)(d) : '';
  } 
  else if (categories[0].startsWith("pay")) {
    formatLabelY = d => d !== null && d !== undefined ? format(`$~s`)(d) : '';
  } else {
    formatLabelY = d => d !== null && d !== undefined ? format(`~s`)(d) : '';
  }

  // POtential pallette
  export let colors = ["#4e79a7","#f28e2c","#e15759","#76b7b2","#59a14f","#edc949","#af7aa1","#ff9da7","#9c755f","#bab0ab"]
  
  $: groupedData = validData.length > 0 ? groupLonger(validData, categories, {
    groupTo: zKey,
    valueTo: yKey
  }) : [];

  // Define styles as objects to ensure consistent application
  const seriesStyles = categories.reduce((acc, cat) => {
    acc[cat] = {
      color: cat.startsWith('national_') ? '#888888' : '#ff6600',
      strokeWidth: cat.startsWith('national_') ? 1.8 : 3
    };
    return acc;
  }, {});

  // Compute valid y domain based on existing data
  $: yDomain = validData.length > 0 
    ? (() => {
        const values = validData.flatMap(d => 
          categories.map(cat => d[cat]).filter(v => v !== null && v !== undefined)
        );
        const minValue = Math.min(...values);
        const maxValue = Math.max(...values);
        
        // If all values are positive, start at 0
        return minValue >= 0 
          ? [0, maxValue]
          : [minValue, maxValue];
      })()
    : [0, 100]; // Default to positive-only fallback domain
</script>

<div class="chart-container" style="height: {height}px;">
  {#if validData.length > 0}
    <LayerCake
      padding={{ top: 20, right: 10, bottom: 20, left: 32 }}
      x={xKey}
      y={yKey}
      z={zKey}
      yDomain={yDomain}
      xDomain={[2008, 2023]}
      zScale={scaleOrdinal()}
      zRange={categories.map(cat => seriesStyles[cat].color)}
      flatData={flatten(groupedData, 'values')}
      data={groupedData}
    >
      <Svg>
        <AxisX
          format={formatLabelX} 
          gridlines={false}
          ticks={5}
        />
        <AxisY 
          format={formatLabelY} 
          ticks={3} 
        />
        <Line {seriesStyles} />
      </Svg>
    </LayerCake>
  {:else}
    <div class="no-data">No valid data available</div>
  {/if}
</div>

<style>
  .chart-container {
    width: 100%;
    position: relative;
  }
  .no-data {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #666;
    font-style: italic;
  }
</style>