<!--
	@component
	Generates an SVG line shape.
 -->
<script>
	import { getContext } from 'svelte';

	const { data, xGet, yGet, x, y, height } = getContext('LayerCake');

	/** @type {String} [stroke='#ab00d6'] – The shape's fill color. This is technically optional because it comes with a default value but you'll likely want to replace it with your own color. */
	export let stroke = '#ab00d6';

	/** @type {String} - The year label color */
	export let textcolor = '#888888';

	$: path = 'M' + $data
		.map(d => {
			return $xGet(d) + ',' + $yGet(d);
		})
		.join('L');
  
  const formatNumber = (num) => {
    if (Math.round(num / 1000000) >= 1) {
      return (Math.round(num / 100000) / 10).toFixed(1) + 'm';
    } else if (Math.round(num / 1000) >= 1) {
      return (Math.round(num / 100) / 10).toFixed(1) + 'k';
    } else {
      return num.toFixed(0);
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
<text x={$xGet($data[$data.length - 1])} y={$yGet($data[$data.length -1])} dx="4" dy="20" font-size="10" fill={stroke}>{formatPct(($y($data[$data.length - 1]) - $y($data[0])) / $y($data[0]))}</text>
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


