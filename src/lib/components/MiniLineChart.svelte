<script>
  import { LayerCake, Svg, Html, groupLonger, flatten } from 'layercake';

  import { scaleOrdinal } from 'd3-scale';
  import { format } from 'd3-format';

  import Line from '$lib/components/Line.svelte';
  import AxisX from '$lib/components/AxisX.svelte';
  import AxisY from '$lib/components/AxisY.svelte';

  export let data = undefined;
  export let categories = ['ft_employment', 'national_ft_employment'];
  export let seriesColors = ['#ffe4b8', '#aaaaaa'];
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
</script>

<div class="chart-container" style="height: {height}px;">
  <LayerCake
    padding={{ top: 20, right: 10, bottom: 20, left: 32 }}
    x={xKey}
    y={yKey}
    z={zKey}
    yDomain={[-100, null]}
    zScale={scaleOrdinal()}
    zRange={seriesColors}
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
  /*
    The wrapper div needs to have an explicit width and height in CSS.
    It can also be a flexbox child or CSS grid element.
    The point being it needs dimensions since the <LayerCake> element will
    expand to fill it.
  */
  .chart-container {
    width: 100%;
  }
</style>