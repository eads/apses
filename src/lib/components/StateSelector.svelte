<script>
    export let data;
    let stateData = data.stateData;
</script>

<select id="state-selector" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
    {#if stateData}
        {#each stateData.state_names as name}
            <option class="uppercase" value={name}>{name}</option>
        {/each}
    {:else}
        <option value="">Loading...</option>
    {/if}
</select>