<!--
	@component
	Generates an SVG line shape.
 -->
<script>
	import { getContext } from 'svelte';

	const { data, xGet, yGet, x, y } = getContext('LayerCake');

	/** @type {String} [stroke='#ab00d6'] – The shape's fill color. This is technically optional because it comes with a default value but you'll likely want to replace it with your own color. */
	export let stroke = '#ab00d6';

	$: path = 'M' + $data
		.map(d => {
			return $xGet(d) + ',' + $yGet(d);
		})
		.join('L');
  
  const formatNumber = (num) => {
    if (Math.round(num / 1000) > 1) {
      return Math.round(num / 1000).toFixed(0) + 'k';
    } else {
      return num.toFixed(0);
    }
  }
</script>

<text x={$xGet($data[0])} y={$yGet($data[0])} text-anchor="end" dx="-2" dy="3" font-size="12" fill={stroke}>{formatNumber($y($data[0]))}</text>
<path class='path-line' d='{path}' {stroke}></path>
<text x={$xGet($data[$data.length - 1])} y={$yGet($data[$data.length -1])} dx="2" dy="3" font-size="12" fill={stroke}>{formatNumber($y($data[$data.length - 1]))}</text>

<style>
	.path-line {
		fill: none;
		stroke-linejoin: round;
		stroke-linecap: round;
		stroke-width: 2;
	}
</style>


