<script>
    import { onMount } from 'svelte';
    import { scrollTo, scrollRef} from 'svelte-scrolling';

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
    let sharedScale = false;
    let mobileMax = 0;
    let mobileChartField = 'ft_employment';

    const itemSize = 120;
    const itemCount = 5;
    const xDomain = [2004, 2022];
    const strokes = {
        ft_employment: 'steelblue',
        ft_pay_per_employee: 'seagreen',
        ft_pay: 'mediumvioletred',
    }

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

      const items = Array.from({ length: 1000 });

</script>

<div use:scrollRef={'app'} class="flex flex-col h-dvh justify-between">
    <header class="bg-gray-800 text-white">
        <h1>Header w/ link to <a class="underline" use:scrollTo={'about'}>about section</a></h1>
    </header>
    <section class="flex-grow overflow-y-scroll bg-zinc-200">
        <p>Main</p>
        <ul>
        {#each items as _, index}
            <li>{index + 1}</li>
        {/each}
        </ul>
    </section>
    <footer class="bg-green-900 text-white">
        <h1>Footer</h1>
    </footer>
</div>

<div use:scrollRef={'about'} class="h-dvh">
    <header class="bg-red-800 text-white">
        <h1>Header w/ link to <a class="underline" use:scrollTo={'app'}>app section</a></h1>
    </header>
    <section class="flex-grow overflow-y-scroll bg-zinc-200">
        {#each items as _, index}
            <p>{index + 1}</p>
        {/each}
    </section>
</div>

<style>
  :global(*) {
    box-sizing: border-box;
  }
  :global(.virtual-list-wrapper) {
    flex: 1 1 0%;
  }

</style>