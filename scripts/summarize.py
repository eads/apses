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
        max_tokens=16000,
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
    state_code = input_file.split('/')[-1].replace('_', ' ')
    df = pd.read_json(input_file)

    # Calculate total employment across years for each function, then filter for top 30%
    total_employment_df = df.groupby('gov_function', as_index=False)['ft_employment'].sum()
    cutoff = total_employment_df['ft_employment'].quantile(0.6)
    top_functions = total_employment_df[total_employment_df['ft_employment'] >= cutoff]['gov_function']

    # Filter the original data for only high-employment functions
    top_data = df[df['gov_function'].isin(top_functions)]

    # Prepare prompt content: Organize data by year for each high-employment government function
    data_prompt = ""
    for function in top_functions:
        function_data = top_data[top_data['gov_function'] == function]
        function_data_lines = [f"{row['year']}: State employment: {row['ft_employment']}, State pay: {row['ft_pay']}\nNational median employment: {row['national_median_employment']}, National median pay: {row['national_median_pay']}, National median pay per employee: {row['national_median_pay_per_employee']}"
                               for _, row in function_data.iterrows()]
        data_prompt += f"\n\n{function}:\n" + "\n".join(function_data_lines)

    # Construct the prompt
    assistant_prompt = "You are someone who explains data to a broad audience, summarizing government employment and pay data as a small blurb in a data visualization web app."
    user_prompt = f"""
Analyze the following government employment and pay data for {state_code} from 2003 to 2022. It's broken out by government "function" (e.g., corrections, health, higher education) and includes special "total - all government employment" and "education total" functions that aggregate across categories and all government functions.

Here's the data:
{data_prompt}

You'll write three bullets for each government function that summarizes it (called $$summary$$ below), focusing on employment and pay trends over time, and how they compare to national medians. You'll also give mind to where this category ranks in the state. Then you'll spit out a little html snippet that can be embedded in a web app that includes a svelte component visualizing the data and your summary.

The bullet list of points should go in the $$summary$$ section of the output, you don't need _any_ frontmatter or summary beforehand. Just these rows of data.

Do not alter the function names or the order of the data.

Then write a series of html snippets that can be embedded in a web app to display the data and your summary like this. I've marked where the summary should go with $$summary$$ and where the government function should go with $$gov_function$$:

<h2>$$gov_function$$</h2>
<div class="flex flex-col md:flex-row gap-12">
  <div class="text-sm mb-6 md:mb-0 xl:w-2/6 [&_p]:mb-6">
    <ul> $$summary$$ </ul>
  </div>

  <div class="flex-1">
      <div class="category-row mb-12">
        <h2 class="text-xl font-medium uppercase mb-4 text-gray-800">
          $$gov_function$$
        </h2>
        <Slider
          data={{acceptedGroups["$$gov_function$$"]}}
          categories={{categories}}
        />
      </div>
  </div>
</div>
"""
    click.echo(f"PROMPT: {user_prompt}")

    # Generate summary with the OpenAI client
    response_data = generate_content(assistant_prompt, user_prompt)
    summary_text = response_data["response"]

    click.echo(f"SUMMARY: {summary_text}")
    click.echo(f"TOKENS USED: {response_data['tokens_used']}")

    # Write the summary to a markdown file
    with open(output_file, 'w') as md_file:
        click.echo(f"Saving summary to {output_file}")
        md_file.write(f"# Summary for {state_code}\n\n{summary_text}")

if __name__ == '__main__':
    summarize()
