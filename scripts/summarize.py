import json
import click
import openai
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from googlesearch import search  # For fetching topical articles

RANKING_THRESHOLD = 10  # Number of top government functions to include article details
MAX_RETRIES = 5         # Maximum number of retries for rate-limiting errors
ARTICLE_RESULTS = 2     # Number of articles to fetch per query

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Static assistant prompt
ASSISTANT_PROMPT = (
    "You are someone who explains data to a savvy but broad audience, summarizing government "
    "employment and pay data for a data visualization web app. Your tone is informative but friendly and creative."
)

# User prompt templates
PROMPT_WITH_ARTICLE = """
Analyze the government employment and pay data for the "{gov_function}" function in {state_code} from 2003 to 2022.

Here is the data:
{state_data}

Write a three-sentence summary focusing on employment and pay trends over time, major leaps or dips, and how the category compares to national averages for pay per employee. Please include real-world context. Return nothing but the sentences in plaintext.
"""

PROMPT_NO_ARTICLE = """
Analyze the government employment and pay data for the "{gov_function}" function in {state_code} from 2003 to 2022.

Here is the data:
{state_data}

Write a two-sentence summary focusing on employment and pay trends over time, major leaps or dips, and how the category compares to national averages for pay per employee. Return nothing but the sentences in plaintext.
"""

def fetch_reliable_articles(query, num_results=ARTICLE_RESULTS):
    """Fetch topical articles using Google Search."""
    try:
        return [url for url in search(query, num_results=num_results)]
    except Exception as e:
        click.echo(f"Error fetching articles: {e}")
        return []

def generate_content_with_retries(gpt_assistant_prompt: str, gpt_user_prompt: str) -> dict:
    """Send a prompt to OpenAI with retry logic for rate-limiting errors."""
    retries = 0
    while retries < MAX_RETRIES:
        try:
            messages = [
                {"role": "assistant", "content": gpt_assistant_prompt},
                {"role": "user", "content": gpt_user_prompt},
            ]
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.7,
                top_p=0.5,
                max_tokens=1500,
                frequency_penalty=0.1,
            )
            response_text = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            return {"response": response_text, "tokens_used": tokens_used}
        except openai.RateLimitError as e:
            wait_time = 5 ** retries
            click.echo(f"Rate limit exceeded. Retrying in {wait_time}s...")
            time.sleep(wait_time)
            retries += 1
        except openai.OpenAIError as e:
            raise Exception(f"OpenAI API error: {e}")
    raise Exception(f"Failed to generate content after {MAX_RETRIES} retries due to rate limiting.")

def process_government_function(index, gov_function, item, state_code):
    """Prepare the prompt, send it to OpenAI, and fetch articles."""
    state_data_lines = [
        f"{row['year']}: State employment: {int(row['ft_employment'])}, State pay: {int(row['ft_pay'])}"
        f" | National avg employment: {int(row['national_avg_employment'])}, National avg pay per employee: {int(row['national_avg_pay_per_employee'])}"
        for row in item["timeseries"]
    ]
    state_data = "\n".join(state_data_lines)

    # Choose appropriate prompt template
    if index == 0 or index > RANKING_THRESHOLD:
        user_prompt = PROMPT_NO_ARTICLE.format(gov_function=gov_function, state_code=state_code, state_data=state_data)
    else:
        user_prompt = PROMPT_WITH_ARTICLE.format(gov_function=gov_function, state_code=state_code, state_data=state_data)

    try:
        # Generate summary
        response_data = generate_content_with_retries(ASSISTANT_PROMPT, user_prompt)
        summary = response_data["response"]

        # Fetch articles for top government functions
        articles = []
        if index > 0 and index <= RANKING_THRESHOLD:
            query = f"{gov_function} government employment trends {state_code}"
            articles = fetch_reliable_articles(query)

        if articles:
            summary += "\n\nTopical articles:\n" + "\n".join(articles)

        return {
            "index": index,  # Preserve the original order
            "gov_function": gov_function,
            "summary": summary,
        }
    except Exception as e:
        return {
            "index": index,
            "gov_function": gov_function,
            "summary": f"Error generating summary: {str(e)}",
        }

@click.command()
@click.option(
    "--input-file",
    type=click.Path(exists=True),
    required=True,
    help="Path to the state JSON data file.",
)
@click.option(
    "--output-file",
    type=click.Path(),
    required=True,
    help="Path to save the consolidated JSON file.",
)
def summarize(input_file, output_file):
    click.echo(f"Summarizing data from {input_file}")
    state_code = input_file.split("/")[-1].replace("_", " ").replace("data.json", "").title()

    with open(input_file, "r") as file:
        data = json.load(file)

    # Process data in parallel
    results = []
    with ThreadPoolExecutor() as executor:
        future_to_function = {
            executor.submit(process_government_function, index, gov_function, item, state_code): index
            for index, (gov_function, item) in enumerate(data.items())
        }

        for future in as_completed(future_to_function):
            result = future.result()
            results.append(result)
            click.echo(f"Processed {result['gov_function']}")

    # Reconstitute original rank order
    results.sort(key=lambda x: x["index"])
    for result in results:
        result.pop("index")  # Remove the index key for cleaner output

    # Write consolidated JSON output
    with open(output_file, "w") as outfile:
        json.dump(results, outfile, indent=2)

    click.echo(f"Consolidated summaries saved to {output_file}")


if __name__ == "__main__":
    summarize()
