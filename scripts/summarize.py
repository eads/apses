import json
import click
import openai
import os
import pandas as pd

# Initialize the OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_content(gpt_assistant_prompt: str, gpt_user_prompt: str) -> dict:
    messages = [
        {"role": "assistant", "content": gpt_assistant_prompt},
        {"role": "user", "content": gpt_user_prompt}
    ]
    response = client.chat.completions.create(
        model="gpt-4o",  # Ensure correct model name is used
        messages=messages,
        temperature=0.3,
        max_tokens=4000,
        frequency_penalty=0.2
    )
    response_text = response.choices[0].message.content
    tokens_used = response.usage.total_tokens
    
    return {"response": response_text, "tokens_used": tokens_used}

@click.command()
@click.option('--input-file', type=click.Path(exists=True), required=True, help='Path to the state JSON data file.')
@click.option('--output-file', type=click.Path(), required=True, help='Path to save the markdown summary file.')
def summarize(input_file, output_file):
    click.echo(f"Summarizing data from {input_file}")
    state_code = input_file.split('/')[-1].split('_')[0]
    df = pd.read_json(input_file)

    # Calculate total employment across years for each function, then filter for top 30%
    total_employment_df = df.groupby('gov_function', as_index=False)['ft_employment'].sum()
    cutoff = total_employment_df['ft_employment'].quantile(0.7)
    top_functions = total_employment_df[total_employment_df['ft_employment'] >= cutoff]['gov_function']

    # Filter the original data for only high-employment functions
    top_data = df[df['gov_function'].isin(top_functions)]

    import ipdb; ipdb.set_trace()

    # Prepare prompt content: Organize data by year for each high-employment government function
    data_prompt = ""
    for function in top_functions:
        function_data = top_data[top_data['gov_function'] == function]
        function_data_lines = [f"{row['year']}: Employment: {row['ft_employment']}, Pay: {row['ft_pay']}"
                               for _, row in function_data.iterrows()]
        data_prompt += f"\n\n{function}:\n" + "\n".join(function_data_lines)

    # Construct the prompt
    assistant_prompt = "You are someone who explains data to a broad audience, summarizing government employment and pay data as a small blurb in a data visualization web app."
    user_prompt = f"""
Analyze the following government employment and pay data for {state_code} from 2003 to 2022.

Focus on high-employment government functions only (those above the median full-time employment across all government functions). Summarize the most notable changes in employment and pay for these government functions, highlighting notable shifts over three time periods: the past few years (including the COVID-19 pandemic), the medium-term (around 8–10 years back), and the full time range from 2000 to 2022. Focus on quantifiable changes, such as percentage increases or decreases in employment and pay, without speculating on causes. Pick out two or three gov functions to analyze. You don't need introductory language like "In this analysis of [state]" because the context will be clear from the user interface where this is used.

Your response should be two paragraphs long and markdown-formatted.

Example response for Florida:

*The data reveals significant shifts in employment and pay across high-employment government functions over nearly two decades. In corrections, employment has seen a major reduction, with full-time positions dropping by about 25% from 2000 to 2022, with the steepest decline occurring during the pandemic years (2019–2022). In this recent period, corrections employment decreased by about 12.4%, while per-capita pay continued to rise, totaling an 8% increase in pay from 2019 to 2022. Overall, pay in corrections grew by approximately 20% over the entire dataset, showing a consistent trend of rising costs per worker even as employment fell.

The health and higher education sectors experienced different dynamics. Health employment increased modestly by 15% since 2000, while pay rose by around 25%, indicating steady growth in both staff numbers and compensation. In higher education instructional roles, employment rose by about 10% from 2012 to 2020, but average pay increased more sharply, with a 15% rise over the same period. Other higher education roles saw even more pronounced growth, with employment expanding by around 30% and pay by 40% since 2000, reflecting a long-term upward trend in both staff size and compensation in the education sector.*

Here's the data:
{data_prompt}
"""

    # Generate summary with the OpenAI client
    response_data = generate_content(assistant_prompt, user_prompt)
    summary_text = response_data["response"]

    click.echo(f"PROMPT: {user_prompt}")
    click.echo(f"SUMMARY: {summary_text}")
    click.echo(f"TOKENS USED: {response_data['tokens_used']}")

    # Write the summary to a markdown file
    with open(output_file, 'w') as md_file:
        click.echo(f"Saving summary to {output_file}")
        md_file.write(f"# Summary for {state_code}\n\n{summary_text}")

if __name__ == '__main__':
    summarize()
