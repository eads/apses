<script>
    export let measureValue;
</script>

<select id="measure-selector" bind:value={measureValue} class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
    <option value="ft_pay_per_employee">Full time pay per full time employee</option>
    <option value="ft_employment">Full time employment</option>
    <option value="ft_pay">Full time pay</option>
</select>