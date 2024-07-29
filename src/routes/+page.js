import { from, all, desc, op, table } from 'arquero';

export const load = ({ fetch }) => {
    return {  
        app: { 
            stateData: 
                fetch('https://s3.amazonaws.com/tmp-gfx-public-data/census_labor_data20230810/state_employment.json')
                    .then(response => response.json())
                    .then(rows => {
                        const dt = from(rows);
                        const state_names = dt.groupby('state').rollup().objects().map(d => d.state);
                        const gov_functions = dt.groupby('gov_function').rollup().objects().map(d => d.gov_function);
                        const chart_data = dt.groupby("state", "year").pivot('gov_function', { value: d => op.sum(d.ft_employment) }).orderby('state', 'year').objects();
                        return { rows, state_names, gov_functions, chart_data };
                    })
        }
    };
};
