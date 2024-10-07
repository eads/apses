<script>
    import MiniLineChart from '$lib/components/MiniLineChart.svelte';
    export let selectedData;
    export let stateValue;
    export let measureValue;
</script>

<div class="p-4">
    <h1 class="text-4xl mt-10 uppercase">{stateValue}</h1>
    <MiniLineChart
        height={600}
        data={selectedData}
        xKey="year"
        yKey={measureValue}
        zKey="gov_function"
        labels="all"
        selected={['education - higher education other']}
        hover={true}
        snapTicks={false}
        animation={false}
        padding={{ top: 0, bottom: 28, left: 10, right: 100 }}
    />
</div>
