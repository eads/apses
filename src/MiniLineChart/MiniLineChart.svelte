<script>
  import { LayerCake, Svg } from 'layercake';

  import Line from './Line.svelte';
  // import AxisX from './AxisX.svelte';

  export let data = undefined;
  export let xKey = 'myX';
  export let yKey = 'myY';
  export let height = 100;
  export let stroke = '#ab00d6';
  export let xDomain = [0, null];
  export let yDomain = [0, null];
</script>

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

<div class="chart-container" style="height: {height}px;">
  <LayerCake
    padding={{ top: 20, right: 50, bottom: 10, left: 10 }}
    x={xKey}
    y={yKey}
    {xDomain}
    {yDomain}
    {data}
  >
    <Svg>
      <Line {stroke} />
    </Svg>
  </LayerCake>
</div>