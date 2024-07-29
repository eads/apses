<script>
    import { Scale, Position } from '@unovis/ts'
    import { VisXYContainer, VisLine, VisAxis, VisBulletLegend, VisCrosshair, VisTooltip, VisStackedBar } from '@unovis/svelte'

    export let data;
    let value = 'alabama';

    const statestate_names = data.app.stateData.then((groups) => {
        console.log(groups);
    })

    const x = d => d.year; 
    // const y = async (d) => {
        // const foo = await data.app.stateData;
        // console.log(foo);
        // foo.
    //  };
    const y = [
        d => d['air transportation'],
        d => d['corrections'],
        d => d['elementary and secondary education'],
        d => Math.random() * 100,
        // d => d['higher education'],
        // d => d['hospitals'],
        // d => d['human services'],
        // d => d['judicial and legal'],
        // d => d['natural resources'],
    ]

    function tooltipTemplate(d){
        return `
            <div>
                <div>${d.gov_function}</div>
                <div>${d.year}</div>
                <div>${d.ft_employment}</div>
            </div>
        `
    }
    
</script>

{#await data.app.stateData}
<p>waiting...</p>
{:then stateData}

<select bind:value={value}>
    {#each stateData.state_names as name}
        <option value={name}>{name}</option>
    {/each}
</select>

<h1>{value}</h1>

<VisXYContainer data={stateData.rows.filter(d => d.state === value)} height={500} xScale={Scale.scaleLinear()}>
    <VisLine {x} {y} /> 

    <!-- <VisLine {x} y={
        stateData.gov_functions.map((gov_function) => {
            return d => Math.random() * 100 ///d[gov_function]
        })
    } /> -->
  <VisAxis type="x" label="Date" numTicks={6} tickFormat={(value) => value}/>
  <VisAxis type="y" label="FT employment"/>
  <VisCrosshair template={tooltipTemplate}/>
  <VisTooltip verticalShift={400} horizontalPlacement={Position.Center}/>
</VisXYContainer>

{/await}

<style>
  :global(*){
    box-sizing: border-box;
  }
</style>