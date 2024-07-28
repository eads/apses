<script>
    import { Scale, Position } from '@unovis/ts'
    import { VisXYContainer, VisLine, VisAxis, VisBulletLegend, VisCrosshair, VisTooltip, VisStackedBar } from '@unovis/svelte'

    export let data;
    let value = 'alabama';

    const stateNames = data.app.stateData.then((groups) => {
        console.log(groups);
    })

    const x = d => d.year; 
    const y = d => d.ft_employment;

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
    {#each stateData.names as name}
        <option value={name}>{name}</option>
    {/each}
</select>

<h1>{value}</h1>

<VisBulletLegend items={stateData.gov_functions}/>
<VisXYContainer data={stateData.rows.filter(d => d.state === value)} height={500} xScale={Scale.scaleLinear()} yScale={Scale.scaleSqrt()}>
  <VisStackedBar {x} {y} />
  <VisAxis type="x" label="Date" numTicks={6} tickFormat={(value) => value}/>
  <VisAxis type="y" label="FT employment"/>
  <VisCrosshair template={tooltipTemplate}/>
  <VisTooltip verticalShift={500} horizontalPlacement={Position.Center}/>
</VisXYContainer>

{/await}

<style>
  :global(*){
    box-sizing: border-box;
  }
</style>