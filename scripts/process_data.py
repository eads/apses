import click
import pandas as pd
import simplejson
from pathlib import Path

@click.command()
@click.option('--input-file', type=click.Path(exists=True), required=True, help='Path to the JSON data file.')
@click.option('--output-dir', type=click.Path(), default="output", help='Directory to save state JSON files.')
def process_data(input_file, output_dir):
    click.echo(f"Processing data from {input_file}")  
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Load data into a DataFrame
    data = pd.read_json(input_file)
    
    # Group data by state and structure output by government function
    for state, state_data in data.groupby('state code'):
        output = {}
        
        # Replace NaNs with None in the DataFrame before converting to dict
        for gov_function, function_data in state_data.groupby('gov_function'):
            cleaned_data = function_data[[
                'year', 
                'ft_eq_employment', 
                'total_pay', 
                'pay_per_fte',
                'ft_eq_employment_1yr_pct',
                'ft_eq_employment_5yr_pct',
                'total_pay_1yr_pct',
                'total_pay_5yr_pct',
                'pay_per_fte_1yr_pct',
                'pay_per_fte_5yr_pct',
                'ft_eq_employment_1yr_abs',
                'ft_eq_employment_5yr_abs',
                'total_pay_1yr_abs',
                'total_pay_5yr_abs',
                'pay_per_fte_1yr_abs',
                'pay_per_fte_5yr_abs',
            ]]
            
            output[gov_function] = {
                "timeseries": cleaned_data.to_dict(orient='records')
            }
        

        # Write output to a JSON file for each state
        output_path = Path(output_dir) / f"{state.lower()}_data.json"
        with open(output_path, 'w') as f:
            simplejson.dump(output, f, indent=2, ignore_nan=True)
        click.echo(f"Saved processed data for {state} to {output_path}")

if __name__ == '__main__':
    process_data()
