import json
import click
import openai
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from random import randint

MAX_RETRIES = 5  # Maximum number of retries for rate-limiting errors
N_FUNCTIONS = 8  # Limit to top N government functions

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Static assistant prompt
ASSISTANT_PROMPT = (
    "You explain government employment and pay data to a savvy but broad audience for a "
    "data visualization web app. Your tone is informative and friendly, making complex data "
    "approachable while acknowledging its limitations."
)

# User prompt template
PROMPT_TEMPLATE = """
Here are some figures for {state_code}'s state government employment in the "{gov_function}" function.

Employment: {ft_eq_employment} (1yr: {ft_eq_employment_1yr_pct}% ({ft_eq_employment_1yr_abs}), 5yr: {ft_eq_employment_5yr_pct}% ({ft_eq_employment_5yr_abs}))
Total Pay: {total_pay} (1yr: {total_pay_1yr_pct}% ({total_pay_1yr_abs}), 5yr: {total_pay_5yr_pct}% ({total_pay_5yr_abs}))
Pay per FTE: {pay_per_fte} (1yr: {pay_per_fte_1yr_pct}% ({pay_per_fte_1yr_abs}), 5yr: {pay_per_fte_5yr_pct}% ({pay_per_fte_5yr_abs}))

Nationally, these trends were observed:
Employment: {national_ft_eq_employment} (1yr: {national_ft_eq_employment_1yr_pct}%, 5yr: {national_ft_eq_employment_5yr_pct}%)
Total Pay: {national_total_pay} (1yr: {national_total_pay_1yr_pct}%, 5yr: {national_total_pay_5yr_pct}%)
Pay per FTE: {national_pay_per_fte} (1yr: {national_pay_per_fte_1yr_pct}%, 5yr: {national_pay_per_fte_5yr_pct}%)

Please summarize the most notable trends in the state in three sentences, prioritizing:

1. The largest percentage changes in any of the state's categories over the 1-year and 5-year periods.
2. Significant deviations from national trends, especially where state changes move in the opposite direction from national changes.
3. Situations where the state shows stability while national trends fluctuate significantly.

Avoid repeating the state name unnecessarily. Use "the state" or omit the reference entirely when the context is clear. Ensure comparisons are accurate, particularly when state figures are lower than national ones.

Examples of notable summaries:
In 2023, higher education employment was 20% lower than five years prior, contrasting with a slight national increase in the same sector.
Corrections employment dropped 10% from 2022 to 2023, a sharper decline than the national average.
While national total pay for healthcare rose by 15% over the last five years, the state saw only a 5% increase, indicating slower growth.

Don't use too many adjectives to describe percentage change differences unless they're more than about 5 percentage points. For example, if pay growth was 25% compared to national pay growth of 18%, you could say "pay growth significantly outpaced the national average by 7 percentage points." But if growth was 20% compared to 18% nationally, you could say "pay growth was 2 percentage points higher than the national average."

Focus on percentage changes over absolute numbers unless the absolute figures are exceptionally large. Ensure clarity and relevance by highlighting trends that most directly impact employment and pay shifts in the state.

Note: Round all percentage values to the nearest whole number before inserting into the template.
"""

def generate_summary(gpt_assistant_prompt: str, gpt_user_prompt: str) -> dict:
    """Send a prompt to OpenAI with retry logic."""
    retries = 0
    while retries < MAX_RETRIES:
        try:
            # click.echo(f"Sending prompt to OpenAI:\n{gpt_user_prompt}", err=True)
            messages = [
                {"role": "assistant", "content": gpt_assistant_prompt},
                {"role": "user", "content": gpt_user_prompt},
            ]
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.8,
                top_p=0.5,
                max_tokens=500,
                frequency_penalty=0.1,
            )
            summary = response.choices[0].message.content
            click.echo(f"Received response from OpenAI:\n{summary}\n\n", err=True)
            return {"response": summary}
        except (openai.RateLimitError, Exception) as e:
            wait_time = 15 + randint(0, 8) * (retries + 1)
            click.echo(f"Error: {e}. Retrying in {wait_time}s...", err=True)
            time.sleep(wait_time)
            retries += 1
    raise Exception(f"Failed after {MAX_RETRIES} retries.")

def process_government_function(index, gov_function, timeseries, state_code):
    """Prepare the prompt and send it to OpenAI."""
    latest_data = timeseries["timeseries"][-1]  # Assuming latest data is the last item in the list

    user_prompt = PROMPT_TEMPLATE.format(
        state_code=state_code,
        gov_function=gov_function,
        current_year=latest_data['year'],
        ft_eq_employment=latest_data['ft_eq_employment'],
        total_pay=latest_data['total_pay'],
        pay_per_fte=latest_data['pay_per_fte'],
        ft_eq_employment_1yr_pct=latest_data['ft_eq_employment_1yr_pct'],
        ft_eq_employment_1yr_abs=latest_data['ft_eq_employment_1yr_abs'],
        total_pay_1yr_pct=latest_data['total_pay_1yr_pct'],
        total_pay_1yr_abs=latest_data['total_pay_1yr_abs'],
        pay_per_fte_1yr_pct=latest_data['pay_per_fte_1yr_pct'],
        pay_per_fte_1yr_abs=latest_data['pay_per_fte_1yr_abs'],
        ft_eq_employment_5yr_pct=latest_data['ft_eq_employment_5yr_pct'],
        ft_eq_employment_5yr_abs=latest_data['ft_eq_employment_5yr_abs'],
        total_pay_5yr_pct=latest_data['total_pay_5yr_pct'],
        total_pay_5yr_abs=latest_data['total_pay_5yr_abs'],
        pay_per_fte_5yr_pct=latest_data['pay_per_fte_5yr_pct'],
        pay_per_fte_5yr_abs=latest_data['pay_per_fte_5yr_abs'],
        national_ft_eq_employment=latest_data['national_ft_eq_employment'],
        national_total_pay=latest_data['national_total_pay'],
        national_pay_per_fte=latest_data['national_pay_per_fte'],
        national_ft_eq_employment_1yr_pct=latest_data['national_ft_eq_employment_1yr_pct'],
        national_total_pay_1yr_pct=latest_data['national_total_pay_1yr_pct'],
        national_pay_per_fte_1yr_pct=latest_data['national_pay_per_fte_1yr_pct'],
        national_ft_eq_employment_5yr_pct=latest_data['national_ft_eq_employment_5yr_pct'],
        national_total_pay_5yr_pct=latest_data['national_total_pay_5yr_pct'],
        national_pay_per_fte_5yr_pct=latest_data['national_pay_per_fte_5yr_pct'],
    )

    click.echo(f"Processing {gov_function} for {state_code}", err=True)

    try:
        response_data = generate_summary(ASSISTANT_PROMPT, user_prompt)
        timeseries["summary"] = response_data["response"]  # Attach summary to the original record
        return {
            "index": index,
            "gov_function": gov_function,
            "summary": response_data["response"],
        }
    except Exception as e:
        click.echo(f"Error processing {gov_function}: {str(e)}", err=True)
        timeseries["summary"] = f"Error generating summary: {str(e)}"
        return {
            "index": index,
            "gov_function": gov_function,
            "summary": f"Error generating summary: {str(e)}",
        }

@click.command()
@click.option("--input-file", type=click.Path(exists=True), required=True, help="Path to the state JSON data file.")
@click.option("--output-file", type=click.Path(), required=True, help="Path to save the consolidated JSON file.")
@click.option("--modified-file", type=click.Path(), required=True, help="Path to save the modified original JSON file.")
def summarize(input_file, output_file, modified_file):
    click.echo(f"Summarizing data from {input_file}", err=True)
    state_code = os.path.basename(input_file).replace("_data.json", "").title()

    with open(input_file, "r") as file:
        data = json.load(file)

    # Limit to top N government functions
    limited_data = dict(list(data.items())[:N_FUNCTIONS])
    click.echo(f"Processing top {N_FUNCTIONS} government functions.", err=True)

    # Process data in parallel
    results = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_to_function = {
            executor.submit(process_government_function, index, gov_function, timeseries, state_code): index
            for index, (gov_function, timeseries) in enumerate(limited_data.items())
        }

        for future in as_completed(future_to_function):
            result = future.result()
            results.append(result)
            click.echo(f"Processed {result['gov_function']}", err=True)

    # Sort results by original order
    results.sort(key=lambda x: x["index"])
    for result in results:
        result.pop("index")

    # Write output to consolidated JSON
    with open(output_file, "w") as outfile:
        json.dump(results, outfile, indent=2)

    click.echo(f"Consolidated summaries saved to {output_file}", err=True)

    # Write modified original data back to file
    with open(modified_file, "w") as modfile:
        json.dump(data, modfile, indent=2)

    click.echo(f"Modified data with summaries saved to {modified_file}", err=True)

if __name__ == "__main__":
    summarize()
