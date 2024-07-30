<script>
    import { LineChart } from "@onsvisual/svelte-charts";

    export let data;
    let stateValue = 'maryland'; // iowa good too
    let measureValue = 'ft_employment';
    let selectedData = [];

    $: data.app.stateData.then((stateData) => {
        const out = stateData.rows.filter(d => d.state === stateValue && !d.gov_function.includes('total'));
        console.log(out);
        selectedData = out || [];
    })
  
    // let hover = true;
    // let hovered = null;

</script>

{#await data.app.stateData}
<p>waiting...</p>
{:then stateData}

<select bind:value={stateValue}>
    {#each stateData.state_names as name}
    <option value={name}>{name}</option>
    {/each}
</select>

<select bind:value={measureValue}>
    <option value="ft_employment">Full time employment</option>
    <option value="ft_pay">Full time pay</option>
</select>

<h1>{stateValue}</h1>

<p>chart</p>

<LineChart
    height={600}
    data={selectedData}
    xKey="year"
    yKey={measureValue}
    zKey="gov_function"
    labels="hover"
    color="gray"
    selected={['education - higher education other']}
    hover={true}
    snapTicks={false}
    animation={false}
    padding={{ top: 0, bottom: 28, left: 35, right: 200 }}
/>

{:catch error}

{/await}

<style>
  :global(*){
    box-sizing: border-box;
  }
</style>