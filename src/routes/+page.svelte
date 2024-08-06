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
    let sharedScale = true;
    let mobileMax = 0;
    let mobileChartField = 'ft_employment';

    const itemSize = 100;
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
        mobileMax = Math.max(...selectedData.map(d => d[mobileChartField]));
        govFunctions = selectedData.length ? [...new Set(selectedData.map(d => d.gov_function))] : [];
    }
</script>

<div id="app" class="flex flex-col h-screen">
    <div class="px-4 py-2">
        <div class="flex items-baseline font-bold text-sm md:text-lg">
            <select id="state-selector" bind:value={stateValue} class="w-1/3 md:w-40 text-sm text-sky-400 border-b-2 border-sky-400">
                {#await data.app.stateData}
                    <option value="">Loading...</option>
                {:then stateData}
                    {#each stateData.state_names as name}
                    <option class="text-black" value={name}>{name.toUpperCase()}</option>
                    {/each}
                {/await}
            </select> 
            <h1 class="ml-2">Employment Explorer</h1>
        </div> 
    </div>
    <div class="flex items-center bg-zinc-200 px-4 py-2 md:text-md">
        <select id="mobileChart-selector" bind:value={mobileChartField} class="w-1/2 md:hidden bg-gray-50 border border-gray-300 text-gray-900 text-xs rounded-md py-1">
            <option value="ft_employment">Full time employees</option>
            <option value="ft_pay_per_employee">Monthly pay per full time employee</option>
            <option value="ft_pay">Monthly full time pay (total)</option>
        </select>
        
        <label class="pl-5 text-sm md:text-base">
            <input name="scale-selector" type="checkbox" bind:checked={sharedScale} /> Shared scale?
        </label>
    </div>
        {#await data.app.stateData}
            <div class="flex-1">
                <div class="p-8">
                    <p>Loading...</p>
                </div>
            </div>
        {:then stateData}
            <div class="flex border-b border-blue-900 bg-zinc-600 text-zinc-50 text-xs md:text-sm" let:index let:style {style}>
                <div class="flex-none w-1/4 md:w-48 mr-5 py-2.5 px-4">Gov function</div>
                <div class="flex-1 hidden md:flex">
                    <div class="flex-initial pl-5 w-80 py-2.5">FT employees</div>
                    <div class="flex-initial pl-5 w-80 py-2.5">Monthly pay per FT employee</div>
                    <div class="flex-initial pl-5 w-80 py-2.5">Monthly FT pay (total)</div>
                </div>
                <div class="flex-initial md:hidden py-2.5">{mobileChartField}</div>
            </div>
            <div class="w-full">
                <VirtualList width="100%" height={itemSize * itemCount} itemCount={govFunctions.length} {itemSize}>
                    <div slot="item" class="flex items-center border-b border-zinc-500" let:index let:style {style}>
                        <div class="flex-none w-1/4 md:w-48 uppercase text-xs md:text-sm px-2">
                            {govFunctions[index]}
                        </div>
                        <div class="flex-1 hidden md:flex">
                            <div class="flex-initial pl-5 w-80">
                                <MiniLineChart
                                    height={itemSize}
                                    data={selectedData.filter(d => d.gov_function === govFunctions[index])}
                                    {xDomain}
                                    yDomain = {[0, sharedScale ? maxFtEmployment : null]}
                                    xKey="year"
                                    yKey="ft_employment"
                                    stroke="steelblue"
                                />
                            </div>
                            <div class="flex-initial pl-5 w-80">
                                <MiniLineChart
                                    height={itemSize}
                                    data={selectedData.filter(d => d.gov_function === govFunctions[index])}
                                    {xDomain}
                                    yDomain = {[0, sharedScale ? maxFtPayPerEmployee : null]}
                                    xKey="year"
                                    yKey="ft_pay_per_employee"
                                    stroke="seagreen"
                                />
                            </div>
                            <div class="flex-initial pl-5 w-80">
                                <MiniLineChart
                                    height={itemSize}
                                    data={selectedData.filter(d => d.gov_function === govFunctions[index])}
                                    {xDomain}
                                    yDomain = {[0, sharedScale ? maxFtPay : null]}
                                    xKey="year"
                                    yKey="ft_pay"
                                    stroke="mediumvioletred"
                                />
                            </div>
                        </div>
                        <div class="flex-1 md:hidden pl-5 pr-14">
                            <MiniLineChart
                                height={itemSize}
                                data={selectedData.filter(d => d.gov_function === govFunctions[index])}
                                {xDomain}
                                yDomain = {[0, sharedScale ? mobileMax : null]}
                                xKey="year"
                                yKey={mobileChartField}
                                stroke="steelblue"
                            />
                        </div>
                    </div>
                </VirtualList>
            </div>
        {/await}
</div>


<div id="about" class="p-4 h-screen text-base md:text-lg mx-auto w-full md:max-w-2xl [&>p>a]:underline">
    <p class="mb-8"><a href="#app">Back to explorer!</a></p>
    <p class="mb-8 italic">By David Eads, first published July 30, 2024</p>
    <p class="mb-4">These charts show the <a href="https://www.census.gov/programs-surveys/apes.html">Annual Survey of Public Employment & Payroll</a>, <a href="https://observablehq.com/@themarshallproject/census-labor-data-release">aggregated by state and government sector</a>, 2004-2022, based on the <a href="https://www.themarshallproject.org/2024/07/25/how-to-investigate-the-trend-of-declining-prison-staff-and-deteriorating-conditions-behind-bars">toolkit released by The Marshall Project</a>.</p>
    <p class="mb-4">2004 was chosen as the starting point to avoid odd spikes in 2001-2002 that appear to be the result of a category that came and went.</p>
</div>

<style>
  :global(*){
    box-sizing: border-box;
  }
  :global(.virtual-list-wrapper) {
    flex: 1 1 0%;
  }

</style>