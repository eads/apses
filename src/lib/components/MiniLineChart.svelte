<script>
  import { LayerCake, Svg } from 'layercake';

  import Line from '$lib/components/Line.svelte';

  export let data = undefined;
  export let xKey = 'myX';
  export let yKey = 'myY';
  export let height = 100;
  export let stroke = '#ab00d6';
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
    padding={{ top: 20, right: 40, bottom: 30, left: 40 }}
    x={xKey}
    y={yKey}
    yDomain={[0, null]}
    {data}
  >
    <Svg>
      <Line {stroke} />
    </Svg>
  </LayerCake>
</div>