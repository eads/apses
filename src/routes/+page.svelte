<script>
    import { LineChart } from "@onsvisual/svelte-charts";

    export let data;
    let stateValue = '';
    let measureValue = 'ft_pay_per_employee';
    let disabled = true;
    let selectedData = [];

    $: data.app.stateData.then((stateData) => {
        if (disabled) {
            let randomState = Math.floor(Math.random() * stateData.state_names.length);
            stateValue = stateData.state_names[randomState];
            disabled = false;
        }
        selectedData = stateData.rows.filter(d => d.state === stateValue && !d.gov_function.includes('total'));
    })
</script>

<div class="p-2 bg-gray-700">
    <h1 class="font-bold text-xl text-white mb-1">State employment explorer</h1> 
    
    <p class="text-white mb-5">From the <a class="underline" href="https://observablehq.com/@themarshallproject/census-labor-data-release">Annual Survey of Public Employment & Payroll</a>, 2000-2022.</p>
    <div>
        <select id="state-selector" {disabled} bind:value={stateValue} class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
            {#await data.app.stateData}
                <option value="">Loading...</option>
            {:then stateData}
                {#each stateData.state_names as name}
                <option class="uppercase" value={name}>{name}</option>
                {/each}
            {/await}
        </select>
        <select id="measure-selector" bind:value={measureValue} class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
            {#await data.app.stateData}
                <option value="">Loading...</option>
            {:then stateData}
                <option value="ft_pay_per_employee">Full time pay per full time employee</option>
                <option value="ft_employment">Full time employment</option>
                <option value="ft_pay">Full time pay</option>
            {/await}
        </select>
    </div>
</div>

{#await data.app.stateData}
    <div class="p-8">
        <p>Loading...</p>
    </div>
{:then stateData}
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
            padding={{ top: 0, bottom: 28, left: 10, right: 100 }}
        />
    </div>
{/await}

<div class="p-4 text-lg mx-auto max-w-2xl [&>p>a]:underline">
    <p class="mb-8 italic">By David Eads / July 30, 2024</p>
    <p class="mb-4">These charts show the <a href="https://www.census.gov/programs-surveys/apes.html">Annual Survey of Public Employment & Payroll</a>, <a href="https://observablehq.com/@themarshallproject/census-labor-data-release">aggregated by state and government sector</a>, 2004-2022, based on the <a href="https://www.themarshallproject.org/2024/07/25/how-to-investigate-the-trend-of-declining-prison-staff-and-deteriorating-conditions-behind-bars">toolkit released by The Marshall Project</a>.</p>
    <p class="mb-4">2004 was chosen as the starting point to avoid odd spikes in 2001-2002 that appear to be the result of a category that came and went.</p>
</div>

<style>
  :global(*){
    box-sizing: border-box;
  }
</style>