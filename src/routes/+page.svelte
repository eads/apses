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
</script>

    {#await data.app.stateData}
        <p>waiting...</p>
    {:then stateData}

<div class="p-2 bg-gray-700">
    <h1 class="font-bold text-xl text-white mb-1">State employment explorer</h1> 
    
    <p class="text-white mb-5">From the <a href="https://observablehq.com/@themarshallproject/census-labor-data-release">Annual Survey of Public Employment & Payroll</a>, 2000-2022.</p>
    <div>
        <select id="state-selector" bind:value={stateValue} class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
            {#each stateData.state_names as name}
            <option value={name}>{name}</option>
            {/each}
        </select>
        <select id="measure-selector" bind:value={measureValue} class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
            <option value="ft_employment">Full time employment</option>
            <option value="ft_pay">Full time pay</option>
        </select>
    </div>
</div>
<div class="p-4">
    <h1 class="text-4xl mt-10 uppercase">{stateValue}</h1>
    <LineChart
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
        padding={{ top: 0, bottom: 28, left: 35, right: 200 }}
    />
</div>
    {:catch error}

    {/await}

<style>
  :global(*){
    box-sizing: border-box;
  }
</style>