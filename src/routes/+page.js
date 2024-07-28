import { from, all, desc, op, table } from 'arquero';

export const load = ({ fetch }) => {
    return {  
        app: { 
            stateData: 
                fetch('https://s3.amazonaws.com/tmp-gfx-public-data/census_labor_data20230810/state_employment.json')
                    .then(response => response.json())
                    .then(rows => {
                        // let grouped = rows.reduce((curr, val) => {
                        //     let group = curr.find(g => g.state === `${val.state}`);
                        //     if (group) {
                        //         group.values.push(val);
                        //     } else {
                        //         curr.push({ state: `${val.state}`, values: [ val ] }); 
                        //     }
                        //     return curr;
                        // }, []);

                        // // let names = grouped.map(g => g.state);
                        
                        // // let gov_functions = rows.reduce((curr, val) => {
                        // //     let group = curr.find(g => g.name === `${val.gov_function}`);
                        // //     if (!group) {
                        // //         curr.push({name:val.gov_function});
                        // //     } 
                        // //     return curr;
                        // // }, []);

                        const dt = from(rows);
                        const names = dt.groupby('state').rollup().objects();
                        const gov_functions = dt.groupby('gov_function').rollup().objects();

                        console

                        return { rows, grouped, names, gov_functions };
                    })
        }
    };
};
