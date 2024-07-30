import { from } from 'arquero';

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
                        return { rows, state_names, gov_functions };
                    })
        }
    };
};
