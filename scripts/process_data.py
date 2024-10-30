import click
import pandas as pd
from pathlib import Path

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
    data = data[(data['year'] >= MIN_YEAR) & data['state'].notna() & (data['state'].str.lower() != "united states")]
    
    # Replace spaces in state names with underscores
    data['state'] = data['state'].str.replace(' ', '_')

    # (Add this snippet inside process_data() after loading and cleaning the data)

    # Calculate ft_pay_per_ft_employee
    data['ft_pay_per_ft_employee'] = data.apply(
        lambda row: row['ft_pay'] / row['ft_employment'] if row['ft_employment'] > 0 else None,
        axis=1
    )

    # Calculate national statistics, including averages and medians of ft_pay_per_ft_employee
    national_stats = (
        data
        .groupby(['gov_function', 'year'])
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
   
    # Calculate counts of non-zero employment/pay values per government function and filter by REJECT_THRESHOLD
    valid_functions = (
        data.assign(
            non_zero_employment=data['ft_employment'] > 0,
            non_zero_pay=data['ft_pay'].fillna(0) > 0
        )
        .groupby(['state', 'gov_function'])
        .agg(
            employment_count=('non_zero_employment', 'sum'),
            pay_count=('non_zero_pay', 'sum'),
            year_count=('year', 'size')
        )
        .reset_index()
    )
    
    # Filter functions based on the threshold and non-zero criteria
    valid_functions = valid_functions[
        (valid_functions['year_count'] > REJECT_THRESHOLD) &
        ((valid_functions['employment_count'] > 0) | (valid_functions['pay_count'] > 0))
    ]
    
    # Merge back to retain only valid functions in the original data
    data = data.merge(
        valid_functions[['state', 'gov_function']],
        on=['state', 'gov_function'],
        how='inner'
    )
    
    # Reorder `gov_function` as per the specified order
    priority_order = [
        "total - all government functions",
        "corrections"
    ]
    
    # Use startswith for grouping functions
    data['priority'] = data['gov_function'].apply(lambda x: (
        1 if x == "total - all government employment functions" else
        2 if x == "corrections" else
        3 if x.startswith("education") else
        4 if x.startswith("health") else
        5 if x.startswith("police protection") else
        6  # Everything else
    ))

    # Sort based on `priority` and `ft_employment` in the latest year
    data['last_year_ft_employment'] = data.groupby(['state', 'gov_function'])['ft_employment'].transform(lambda x: x.iloc[-1] if len(x) > 0 else 0)
    data = data.sort_values(by=['priority', 'state', 'last_year_ft_employment'], ascending=[True, True, False])
    
    # Select and save required columns by state
    columns_to_save = ['year', 'state', 'gov_function', 'ft_pay', 'ft_employment', 
                       'national_avg_employment', 'national_median_employment', 
                       'national_avg_pay', 'national_median_pay', 'national_avg_pay_per_employee',
                       'national_median_pay_per_employee']
    for state, state_data in data.groupby('state'):
        output_path = Path(output_dir) / f"{state}_data.json"
        state_data[columns_to_save].to_json(output_path, orient='records', indent=2, lines=False)
        click.echo(f"Saving {len(state_data)} entries to {output_path}")

if __name__ == '__main__':
    process_data()


# import click
# import pandas as pd
# from pathlib import Path

# REJECT_THRESHOLD = 3  # Minimum number of data points required to include in output
# MIN_YEAR = 2003

# @click.command()
# @click.option('--input-file', type=click.Path(exists=True), required=True, help='Path to the JSON data file.')
# @click.option('--output-dir', type=click.Path(), default="output", help='Directory to save state JSON files.')
# def process_data(input_file, output_dir):
#     click.echo(f"Processing data from {input_file}")  
#     Path(output_dir).mkdir(parents=True, exist_ok=True)
    
#     # Load data into a DataFrame
#     data = pd.read_json(input_file)
    
#     # Filter data by year and non-null state values
#     data = data[(data['year'] >= MIN_YEAR) & data['state'].notna()]
    
#     # Replace spaces in state names with underscores
#     data['state'] = data['state'].str.replace(' ', '_')
    
#     # Calculate counts of non-zero employment/pay values per government function and filter by REJECT_THRESHOLD
#     valid_functions = (
#         data.assign(
#             non_zero_employment=data['ft_employment'] > 0,
#             non_zero_pay=data['ft_pay'].fillna(0) > 0
#         )
#         .groupby(['state', 'gov_function'])
#         .agg(
#             employment_count=('non_zero_employment', 'sum'),
#             pay_count=('non_zero_pay', 'sum'),
#             year_count=('year', 'size')
#         )
#         .reset_index()
#     )
    
#     # Filter functions based on the threshold and non-zero criteria
#     valid_functions = valid_functions[
#         (valid_functions['year_count'] > REJECT_THRESHOLD) &
#         ((valid_functions['employment_count'] > 0) | (valid_functions['pay_count'] > 0))
#     ]
    
#     # Merge back to retain only valid functions in the original data
#     data = data.merge(
#         valid_functions[['state', 'gov_function']],
#         on=['state', 'gov_function'],
#         how='inner'
#     )
    
#     # Reorder `gov_function` as per the specified order
#     priority_order = [
#         "total - all government functions",
#         "corrections"
#     ]
    
#     # Use startswith for grouping functions
#     data['priority'] = data['gov_function'].apply(lambda x: (
#         1 if x == "total - all government employment functions" else
#         2 if x == "corrections" else
#         3 if x.startswith("education") else
#         4 if x.startswith("health") else
#         5 if x.startswith("police protection") else
#         6  # Everything else
#     ))

#     # Sort based on `priority` and `ft_employment` in the latest year
#     data['last_year_ft_employment'] = data.groupby(['state', 'gov_function'])['ft_employment'].transform(lambda x: x.iloc[-1] if len(x) > 0 else 0)
#     data = data.sort_values(by=['priority', 'state', 'last_year_ft_employment'], ascending=[True, True, False])
    
#     # Select and save required columns by state
#     columns_to_save = ['year', 'state', 'gov_function', 'ft_pay', 'ft_employment']
#     for state, state_data in data.groupby('state'):
#         output_path = Path(output_dir) / f"{state}_data.json"
#         state_data[columns_to_save].to_json(output_path, orient='records', indent=2, lines=False)
#         click.echo(f"Saving {len(state_data)} entries to {output_path}")

# if __name__ == '__main__':
#     process_data()
