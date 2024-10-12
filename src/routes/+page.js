import { from } from 'arquero';

export const load = async ({ fetch }) => {
    // Fetch the local JSON file from the static folder
    const response = await fetch('/state_employment.json');
    const rows = await response.json();

    // Process the data using Arquero
    const dt = from(rows).filter(d => d.year > 2003 && d.ft_employment > 0).derive({
        ft_pay_per_employee: d => d.ft_pay / d.ft_employment
    });

    const state_names = dt.groupby('state').rollup().objects().map(d => d.state);
    const gov_functions = dt.groupby('gov_function').rollup().objects().map(d => d.gov_function);

    // Return the state data directly without nesting under `app`
    return {
        stateData: {
            rows: dt.objects(),
            state_names,
            gov_functions
        }
    };
};
