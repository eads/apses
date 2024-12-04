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



 <!-- <script>
	import { getContext } from 'svelte';

	const { data, xGet, yGet, x, y, height } = getContext('LayerCake');

	/** @type {String} [stroke='#ab00d6'] – The shape's fill color. This is technically optional because it comes with a default value but you'll likely want to replace it with your own color. */
	export let stroke = '#ab00d6';

	/** @type {String} - The year label color */
	export let textcolor = '#888888';

	export let textPrefix = "";

	$: path = 'M' + $data
		.map(d => {
			return $xGet(d) + ',' + $yGet(d);
		})
		.join('L');
  
  const formatNumber = (num) => {
    if (Math.round(num / 1000000000) >= 1) {
      return textPrefix + (Math.round(num / 100000000) / 10).toFixed(1) + 'b';
		} else if (Math.round(num / 1000000) >= 1) {
      return textPrefix + (Math.round(num / 100000) / 10).toFixed(1) + 'm';
    } else if (Math.round(num / 1000) >= 1) {
      return textPrefix + (Math.round(num / 100) / 10).toFixed(1) + 'k';
    } else {
      return textPrefix + num.toFixed(0);
    }
  }

	const formatPct = (num) => {
		const prefix = num > 0 ? '+' : '';
		return prefix + '' + (num * 100).toFixed(0) + '%';
	}
</script>

<text x={$xGet($data[0])} y={$yGet($data[0])} text-anchor="end" dx="-6" dy="4" font-size="14" fill={stroke}>{formatNumber($y($data[0]))}</text>
<text x={$xGet($data[0])} y={$height} text-anchor="middle" dy="20" font-size="10" fill={textcolor}>{$x($data[0])}</text>
<line
	class="grid-line"
	stroke={textcolor}
	x1={$xGet($data[0])}
	x2={$xGet($data[0])}
	y1={$yGet($data[0])}
	y2={$height + 10}
/>

<path class='path-line' d='{path}' {stroke}></path>
<text x={$xGet($data[$data.length - 1])} y={$yGet($data[$data.length -1])} dx="4" dy="4" font-size="14" fill={stroke}>{formatNumber($y($data[$data.length - 1]))}</text>
<text x={$xGet($data[$data.length - 1])} y={$height} text-anchor="middle" dy="20" font-size="10" fill={textcolor}>{$x($data[$data.length - 1])}</text>
<line
	class="grid-line"
	stroke={textcolor}
	x1={$xGet($data[$data.length - 1])}
	x2={$xGet($data[$data.length - 1])}
	y1={$yGet($data[$data.length - 1])}
	y2={$height + 10}
/>


<style>
	.path-line {
		fill: none;
		stroke-linejoin: round;
		stroke-linecap: round;
		stroke-width: 4;
	}
	.grid-line {
		stroke-width: 1;
    stroke-dasharray: 2;
	}
</style>

 -->
