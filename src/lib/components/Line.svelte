<!--
	@component
	Generates an SVG line shape.
 -->
<script>
  import { getContext } from 'svelte';
  import { line, curveLinear } from 'd3-shape';

  const { data, xGet, yGet, zGet } = getContext('LayerCake');

  /** @type {Function} [curve=curveLinear] - An optional D3 interpolation function. See [d3-shape](https://github.com/d3/d3-shape#curves) for options. Pass this function in uncalled, i.e. without the open-close parentheses. */
  export let curve = curveLinear;

  $: path = line().x($xGet).y($yGet).curve(curve);
  // .defined($y)
</script>

<g class="line-group">
  {#each $data as group, i}
    <path class="path-line path-line-{i}" d={path(group.values)} stroke={$zGet(group)}></path>
  {/each}
</g>

<style>
  .path-line {
    fill: none;
    stroke-linejoin: round;
    stroke-linecap: round;
    stroke-width: 4px;
  }
	.path-line-1 {
		stroke-width: 2px;
	}
</style>