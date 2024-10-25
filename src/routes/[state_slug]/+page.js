export async function load({ params, fetch }) {
  const { state_slug } = params;

  // Fetch the state-specific data
  const response = await fetch(`/files/${state_slug}.json`);
  const rawData = await response.json();
  const stateData = rawData
    .filter(d => d.year > 2003)
    .map(d => ({ 
        ...d,
        ft_pay_per_ft_employee: d.ft_pay / d.ft_employment,
        pt_pay_per_pt_employee: d.pt_pay / d.pt_employment,
      })
    );
  return {
    stateData
  };
}