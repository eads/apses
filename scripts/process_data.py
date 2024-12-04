import click
import pandas as pd
from pathlib import Path
import json

REJECT_THRESHOLD = 3  # Minimum number of data points required to include in output
MIN_YEAR = 2003

@click.command()
@click.option('--input-file', type=click.Path(exists=True), required=True, help='Path to the JSON data file.')
@click.option('--output-dir', type=click.Path(), default="output", help='Directory to save state JSON files.')
def process_data(input_file, output_dir):
    click.echo(f"Processing data from {input_file}")  
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Load data into a DataFrame
    data = pd.read_json(input_file)
    
    # Filter data by year, non-null state values, and exclude "united states" rows
    data = data[(data['year'] >= MIN_YEAR) & data['state_lower'].notna() & (data['state_lower'].str.lower() != "united states") & (~data['gov_function'].str.endswith("total", na=False))]
    
    # Replace spaces in state names with underscores
    data['state_lower'] = data['state_lower'].str.replace(' ', '_')

    # Calculate ft_pay_per_ft_employee, setting it to 0 if ft_employment is zero
    data['ft_pay_per_ft_employee'] = data.apply(
        lambda row: row['ft_pay'] / row['ft_employment'] if row['ft_employment'] > 0 else 0,
        axis=1
    )
    
    # Calculate national statistics
    national_stats = (
        data.groupby(['gov_function', 'year'])
        .agg(
            national_avg_employment=('ft_employment', 'mean'),
            national_median_employment=('ft_employment', 'median'),
            national_avg_pay=('ft_pay', 'mean'),
            national_median_pay=('ft_pay', 'median'),
            national_avg_pay_per_employee=('ft_pay_per_ft_employee', 'mean'),
            national_median_pay_per_employee=('ft_pay_per_ft_employee', 'median')
        )
        .reset_index()
    )

    # Merge national statistics back into the main data
    data = data.merge(national_stats, on=['gov_function', 'year'], how='left')

    # Exclude "total - all government employment functions" for rankings
    ranking_data = data[data['gov_function'] != "total - all government employment functions"]
    
    # Filter for the most recent three years for each government function
    recent_years = ranking_data.groupby(['state_lower', 'gov_function'])['year'].transform(lambda x: x.nlargest(3))
    ranking_data = ranking_data[ranking_data['year'].isin(recent_years)]

    # Calculate averages for the most recent three years
    recent_averages = (
        ranking_data.groupby(['state_lower', 'gov_function'])
        .agg(
            avg_ft_employment=('ft_employment', 'mean'),
            avg_ft_pay=('ft_pay', 'mean')
        )
        .reset_index()
    )

    # Calculate ranks and quantiles within each state based on averages
    recent_averages['employment_rank'] = recent_averages.groupby('state_lower')['avg_ft_employment'].rank(ascending=False)
    recent_averages['employment_percentile'] = recent_averages.groupby('state_lower')['avg_ft_employment'].rank(pct=True) * 100
    recent_averages['pay_rank'] = recent_averages.groupby('state_lower')['avg_ft_pay'].rank(ascending=False)
    recent_averages['pay_percentile'] = recent_averages.groupby('state_lower')['avg_ft_pay'].rank(pct=True) * 100
    
    # Merge ranks and quantiles back to the main data
    data = data.merge(recent_averages, on=['state_lower', 'gov_function'], how='left')

    # Group data by state and structure output by government function
    for state, state_data in data.groupby('state_lower'):
        output = {}
        
        for gov_function, function_data in state_data.groupby('gov_function'):
            # If this is "total - all government employment functions", skip rank and quantile
            if gov_function == "total - all government employment functions":
                output[gov_function] = {
                    "employment_rank": 0,
                    "pay_rank": 0,
                    "timeseries": function_data[[
                        'year', 'ft_employment', 'ft_pay', 'ft_pay_per_ft_employee',
                        'national_avg_employment', 'national_median_employment',
                        'national_avg_pay', 'national_median_pay',
                        'national_avg_pay_per_employee', 'national_median_pay_per_employee'
                    ]].to_dict(orient='records')
                }
            else:
                # Select metadata for each government function
                metadata = recent_averages[
                    (recent_averages['state_lower'] == state) & 
                    (recent_averages['gov_function'] == gov_function)
                ].iloc[0]  # Assuming single row for the most recent three-year average data
                
                # Structure the output for the government function with ranks and quantiles
                output[gov_function] = {
                    "employment_rank": int(metadata['employment_rank']),
                    "employment_percentile": metadata['employment_percentile'],
                    "pay_rank": int(metadata['pay_rank']),
                    "pay_percentile": metadata['pay_percentile'],
                    "timeseries": function_data[[
                        'year', 'ft_employment', 'ft_pay', 'ft_pay_per_ft_employee',
                        'national_avg_employment', 'national_median_employment',
                        'national_avg_pay', 'national_median_pay',
                        'national_avg_pay_per_employee', 'national_median_pay_per_employee'
                    ]].to_dict(orient='records')
                }

        # Sort by rank in ascending order
        output = dict(sorted(output.items(), key=lambda item: item[1]["pay_rank"]))

        # Convert NaNs to None for JSON compatibility
        output = json.loads(json.dumps(output, default=lambda x: None))
        
        # Write output to a JSON file for each state
        output_path = Path(output_dir) / f"{state}_data.json"
        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2)
        click.echo(f"Saved processed data for {state} to {output_path}")

if __name__ == '__main__':
    process_data()
