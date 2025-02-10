<script>
  import { LayerCake, Svg, groupLonger, flatten } from 'layercake';

  import { scaleOrdinal } from 'd3-scale';
  import { format } from 'd3-format';

  import Line from '$lib/components/Line.svelte';
  import AxisX from '$lib/components/AxisX.svelte';
  import AxisY from '$lib/components/AxisY.svelte';

  export let data = undefined;
  export let categories = ['ft_employment', 'national_ft_employment'];
  export let height = 150;

  const xKey = 'year';
  const yKey = 'value';
  const zKey = 'category';

  const formatLabelX = d => `'${String(d - 2000).padStart(2, '0')}`;
  const formatLabelY = (categories[0].includes("pay")) ? d => format(`$~s`)(d) : d => format(`~s`)(d);

  const groupedData = groupLonger(data, categories, {
    groupTo: zKey,
    valueTo: yKey
  });

  // Define styles as objects to ensure consistent application
  const seriesStyles = categories.reduce((acc, cat) => {
    acc[cat] = {
      color: cat.startsWith('national_') ? '#aaaaaa' : '#ff6600',
      strokeWidth: cat.startsWith('national_') ? 1 : 3
    };
    return acc;
  }, {});
</script>

<div class="chart-container" style="height: {height}px;">
  <LayerCake
    padding={{ top: 20, right: 10, bottom: 20, left: 32 }}
    x={xKey}
    y={yKey}
    z={zKey}
    yDomain={[0, null]}
    zScale={scaleOrdinal()}
    zRange={categories.map(cat => seriesStyles[cat].color)}
    flatData={flatten(groupedData, 'values')}
    data={groupedData}
  >
    <Svg>
      <AxisX
        format={formatLabelX} 
        gridlines={false}
        ticks={[2003, 2013, 2023]}
      />
      <AxisY 
        format={formatLabelY} 
        ticks={3} 
      />
      <Line />
    </Svg>
  </LayerCake>
</div>

<style>
  .chart-container {
    width: 100%;
  }
</style>
