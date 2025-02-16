<!--
	@component
	Generates an SVG line shape.
 -->
<script>
  import { getContext } from 'svelte';
  import { line, curveLinear } from 'd3-shape';

  const { data, xGet, yGet, zGet } = getContext('LayerCake');

  /** @type {Function} [curve=curveLinear] - D3 interpolation function */
  export let curve = curveLinear;
  
  /** @type {Object} Styles for different series */
  export let seriesStyles = {};

  // Create a line generator that handles missing values
  $: path = line()
    .x(d => {
      const val = $xGet(d);
      return val !== null && val !== undefined ? $xGet(d) : null;
    })
    .y(d => {
      const val = $yGet(d);
      return val !== null && val !== undefined ? $yGet(d) : null;
    })
    .defined(d => {
      const x = $xGet(d);
      const y = $yGet(d);
      return x !== null && x !== undefined && y !== null && y !== undefined;
    })
    .curve(curve);

  // Filter out groups with no valid values
  $: validGroups = $data.filter(group => 
    group.values && 
    group.values.some(d => 
      $xGet(d) !== null && 
      $xGet(d) !== undefined && 
      $yGet(d) !== null && 
      $yGet(d) !== undefined
    )
  );
</script>

<g class="line-group">
  {#each validGroups as group}
    {@const style = seriesStyles[group.category] || {}}
    <path 
      class="path-line"
      class:national={group.category.startsWith('national_')}
      d={path(group.values)}
      style="
        stroke: {style.color || '#ff6600'};
        stroke-width: {style.strokeWidth || 2}px;
      "
    />
  {/each}
</g>

<style>
  .path-line {
    fill: none;
    stroke-linejoin: round;
    stroke-linecap: round;
  }
  .path-line.national {
    opacity: 0.8;
  }
</style>