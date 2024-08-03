<script>
    import { onMount } from 'svelte';
    import MiniLineChart from '../MiniLineChart/MiniLineChart.svelte';
    import VirtualList from 'svelte-tiny-virtual-list';

    export let data;
    
    let stateValue = '';
    let disabled = true;
    let fullData = [];
    let selectedData = [];
    let govFunctions = [];
    let maxFtPay = 0;
    let maxFtEmployment = 0;
    let maxFtPayPerEmployee = 0;
    let sharedScale = 'shared';

    const itemSize = 120;
    const itemCount = 6;
    const xDomain = [2004, 2022];

    onMount(() => {
        data.app.stateData.then((stateData) => {
            if (disabled) {
                let randomState = Math.floor(Math.random() * stateData.state_names.length);
                stateValue = stateData.state_names[randomState];
                disabled = false;
            }
            fullData = stateData;
        })
    });

    $: {
        selectedData = fullData.rows ? fullData.rows.filter(d => d.state === stateValue && !d.gov_function.includes('total')) : [];
        maxFtPay = Math.max(...selectedData.map(d => d.ft_pay));
        maxFtEmployment = Math.max(...selectedData.map(d => d.ft_employment));
        maxFtPayPerEmployee = Math.max(...selectedData.map(d => d.ft_pay_per_employee));
        govFunctions = selectedData.length ? [...new Set(selectedData.map(d => d.gov_function))] : [];
    }
</script>

<div class="p-2 bg-gray-700">
    <h1 class="font-bold text-xl text-white mb-1">State employment explorer</h1> 
    
    <p class="text-white mb-5">From the <a class="underline" href="https://observablehq.com/@themarshallproject/census-labor-data-release">Annual Survey of Public Employment & Payroll</a>, 2000-2022.</p>
    <div class="flex">
        <select id="state-selector" bind:value={stateValue} class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
            {#await data.app.stateData}
                <option value="">Loading...</option>
            {:then stateData}
                {#each stateData.state_names as name}
                <option class="uppercase" value={name}>{name}</option>
                {/each}
            {/await}
        </select>

        <fieldset class="ml-5">
            <legend class="text-white">Shared scale or absolute?</legend>
            <label class="text-white">
                <input name="scale-selector" type="radio" value="shared" bind:group={sharedScale} /> Shared
            </label>
            <label class="text-white">
                <input name="scale-selector" type="radio" value="independent" bind:group={sharedScale} /> Independent
            </label>
        </fieldset>
    </div>
</div>

{#await data.app.stateData}
    <div class="p-8">
        <p>Loading...</p>
    </div>
{:then stateData}

<div class="bg-zinc-100">
    <div class="flex border-b border-blue-900 bg-zinc-600 text-zinc-50" let:index let:style {style}>
        <div class="flex-none w-32 mr-5">Gov function</div>
        <div class="flex-initial ml-5 w-80">Full time employment</div>
        <div class="flex-initial ml-5 w-80">Full time pay (monthly total)</div>
        <div class="flex-initial ml-5 w-80">Full time pay / full time employees</div>
    </div>
    <VirtualList width="100%" height={itemSize * itemCount} itemCount={govFunctions.length} {itemSize}>
        <div slot="item" class="flex border-b border-zinc-500" let:index let:style {style}>
            <div class="flex-none w-32 mr-5 py-2 uppercase text-sm">{govFunctions[index]}</div>
            <div class="flex-initial ml-5 w-80">
                <MiniLineChart
                    height={itemSize}
                    data={selectedData.filter(d => d.gov_function === govFunctions[index])}
                    {xDomain}
                    yDomain = {[0, sharedScale === "shared" ? maxFtEmployment : null]}
                    xKey="year"
                    yKey="ft_employment"
                    stroke="steelblue"
                />
            </div>
            <div class="flex-initial ml-5 w-80">
                <MiniLineChart
                    height={itemSize}
                    data={selectedData.filter(d => d.gov_function === govFunctions[index])}
                    {xDomain}
                    yDomain = {[0, sharedScale === "shared" ? maxFtPay : null]}
                    xKey="year"
                    yKey="ft_pay"
                    stroke="mediumvioletred"
                />
            </div>
            <div class="flex-initial ml-5 w-80">
                <MiniLineChart
                    height={itemSize}
                    data={selectedData.filter(d => d.gov_function === govFunctions[index])}
                    {xDomain}
                    yDomain = {[0, sharedScale === "shared" ? maxFtPayPerEmployee : null]}
                    xKey="year"
                    yKey="ft_pay_per_employee"
                    stroke="seagreen"
                />
            </div>
        </div>
    </VirtualList>
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