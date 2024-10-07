<script>
    import { scrollTo, scrollRef} from 'svelte-scrolling';

    import StateSelector from '$lib/components/StateSelector.svelte';
    import MeasureSelector from '$lib/components/MeasureSelector.svelte';
    import ChartContainer from '$lib/components/ChartContainer.svelte';

    export let data;
    let stateValue = '';
    let measureValue = 'ft_pay_per_employee';
    let disabled = true;
    let selectedData = [];
    let stateData = null;

    // $: data.app.stateData.then((stateDataResp) => {
    //     stateData = stateDataResp;
    //     if (disabled) {
    //         let randomState = Math.floor(Math.random() * stateData.state_names.length);
    //         stateValue = stateData.state_names[randomState];
    //         disabled = false;
    //     }
    //     selectedData = stateData.rows.filter(d => d.state === stateValue && !d.gov_function.includes('total'));
    // });

</script>

<div use:scrollRef={'app'} class="flex flex-col h-dvh">
    <header class="bg-gray-800 text-white">
        <StateSelector {stateValue} {stateData} {disabled} />
        <MeasureSelector {measureValue} />
        <h1>Header w/ link to <a class="underline" use:scrollTo={'about'}>about section</a></h1>
    </header>
    <section class="flex-grow overflow-y-scroll bg-zinc-200">
        {#await data.app.stateData}
            <div class="p-8">
                <p>Loading...</p>
            </div>
        {:then stateData}
            <ChartContainer {selectedData} {stateValue} {measureValue} />
        {/await}
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
        <p>Lorem ipsum...</p>
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