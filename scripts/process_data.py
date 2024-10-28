import json
import click
from pathlib import Path

REJECT_THRESHOLD = 3  # Minimum number of data points required to include in output
MIN_YEAR = 2003

@click.command()
@click.option('--input-file', type=click.Path(exists=True), required=True, help='Path to the JSON data file.')
@click.option('--output-dir', type=click.Path(), default="output", help='Directory to save state JSON files.')
def process_data(input_file, output_dir):
    click.echo(f"Processing data from {input_file}")  
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Group data by state
    state_data = {}
    for entry in data:
        if entry['state'] is None:
            continue
        state = entry['state'].replace(' ', '_')
        state_data.setdefault(state, []).append(entry)
    
    # Filter and save each state's data
    for state, entries in state_data.items():
        # Count non-zero employment/pay values per government function
        gov_function_counts = {}
        non_zero_tracker = {}

        for entry in entries:
            function = entry['gov_function']
            year = entry['year']
            if year < MIN_YEAR:
                continue
            
            ft_employment = entry['ft_employment']
            ft_pay = entry.get('ft_pay', 0)
            
            if function not in non_zero_tracker:
                non_zero_tracker[function] = {'employment': 0, 'pay': 0}
            
            if ft_employment and ft_employment > 0:
                non_zero_tracker[function]['employment'] += 1
            
            if ft_pay and ft_pay > 0:
                non_zero_tracker[function]['pay'] += 1
            
            # Count valid years for threshold
            gov_function_counts.setdefault(function, 0)
            gov_function_counts[function] += 1

        # Filter functions that meet the REJECT_THRESHOLD and have any non-zero values in both columns
        filtered_entries = [
            entry for entry in entries
            if entry['year'] >= MIN_YEAR
            and gov_function_counts.get(entry['gov_function'], 0) > REJECT_THRESHOLD
            and (
                non_zero_tracker[entry['gov_function']]['employment'] > 0
                or non_zero_tracker[entry['gov_function']]['pay'] > 0
            )
        ]
        
        # Save filtered data to JSON
        output_path = Path(output_dir) / f"{state}_data.json"
        
        click.echo(f"Saving {len(filtered_entries)} entries to {output_path}")
        with open(output_path, 'w') as out_f:
            json.dump(filtered_entries, out_f, indent=2)

if __name__ == '__main__':
    process_data()


# import json
# import click
# from pathlib import Path

# REJECT_THRESHOLD = 3 # Minimum number of data points required to include in output
# MIN_YEAR = 2003

# @click.command()
# @click.option('--input-file', type=click.Path(exists=True), required=True, help='Path to the JSON data file.')
# @click.option('--output-dir', type=click.Path(), default="output", help='Directory to save state JSON files.')
# def process_data(input_file, output_dir):
#     click.echo(f"Processing data from {input_file}")  
#     Path(output_dir).mkdir(parents=True, exist_ok=True)
    
#     with open(input_file, 'r') as f:
#         data = json.load(f)

#     # Group data by state
#     state_data = {}
#     for entry in data:
#         if entry['state'] is None:
#             continue
#         state = entry['state'].replace(' ', '_')
#         state_data.setdefault(state, []).append(entry)
    
#     # Filter and save each state's data
#     for state, entries in state_data.items():
#         # Filter government functions based on employment criteria
#         filtered_entries = []
#         gov_function_counts = {}
        
#         for entry in entries:
#             function = entry['gov_function']
#             ft_employment = entry['ft_employment']
#             if ft_employment and ft_employment > 0:
#                 gov_function_counts.setdefault(function, 0)
#                 gov_function_counts[function] += 1

#         for entry in entries:
#             function = entry['gov_function']
#             if gov_function_counts.get(function, 0) <= REJECT_THRESHOLD and entry['year'] >= MIN_YEAR:
#                 filtered_entries.append(entry)
        
#         # Save filtered data to JSON
#         output_path = Path(output_dir) / f"{state}_data.json"
        
#         click.echo(f"Saving {len(filtered_entries)} entries to {output_path}")
#         with open(output_path, 'w') as out_f:
#             json.dump(filtered_entries, out_f, indent=2)

# if __name__ == '__main__':
#     process_data()
