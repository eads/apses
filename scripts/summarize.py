import json
import click
import openai
import os
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from random import randint

RANKING_THRESHOLD = 10  # Number of top government functions to include article details
MAX_RETRIES = 5         # Maximum number of retries for rate-limiting errors or search errors
BING_API_KEY = os.getenv("BING_API_KEY")  # Set Bing API key as an environment variable


# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Static assistant prompt
ASSISTANT_PROMPT = (
    "You are someone who explains data to a savvy but broad audience, summarizing government "
    "employment and pay data for a data visualization web app. Your tone is informative and friendly, with a little self-skepticism."
)

# User prompt templates
PROMPT_WITH_ARTICLE = """
Analyze the government employment and pay data for the "{gov_function}" function in {state_code} from 2003 to 2022.

Here is the data:
{state_data}

Write a two-sentence summary focusing on employment and pay trends over time, major leaps or dips, and how the category compares to national averages for pay per employee. Please include real-world context. Return nothing but the sentences in plaintext with HTML formatted links.
"""

PROMPT_NO_ARTICLE = """
Analyze the government employment and pay data for the "{gov_function}" function in {state_code} from 2003 to 2022.

Here is the data:
{state_data}

Write a two-sentence summary focusing on employment and pay trends over time, major leaps or dips, and how the category compares to national averages for pay per employee. Return nothing but the sentences in plaintext.

For example, in Washington state in 2022, in the hospital government function, pay per employee was about $800/month more than the national average. That's the case for most years since 2003. 

State - Total Employment: 12747, State - Pay per Employee: 6820
National Average - Total Employment: 7706, National Average - Pay per Employee: 6024

You'd say: "From 2003 to 2022, Washington's government employment in the "hospitals" function showed a steady increase, with a notable leap from 2016 to 2022. Washington state consistently pays its employees more than the national average, with a difference of about $800 per month in 2022, this trend has been consistent since 2003."

Here's the opposite case. In South Carolina, pay per employee in the higher educational instructional sector was consistently less than the national average, but overall employment jumped quite a bit around 2017. In 2022:

State - Total Employment: 9777, State - Pay per Employee: 7940
National Average - Total Employment: 9506, National Average - Pay per Employee: 9126

You'd say: "From 2003 to 2022, South Carolina's higher education instructional employment grew steadily. Workers in this sector in South Carolina have consistently earned less than the national average, with a widening gap in recent years."

When considering what to say about total employment, think about whether the trend line is stable, fluctuates, or shows a specific trend up or down. Similarly, with 
avg pay, consider whether the gap is widening, narrowing, or about the same over time.
"""

def fetch_reliable_article(query):
    """Fetch a single reliable article using Bing Web Search API."""
    retries = 0
    while retries < MAX_RETRIES:
        try:
            headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
            params = {"q": query, "count": 5}  # Return only one result
            response = requests.get("https://api.bing.microsoft.com/v7.0/search", headers=headers, params=params)
            response.raise_for_status()  # Raise an error for HTTP codes >= 400
            results = response.json()

            # Extract URL from the search results
            if "webPages" in results and results["webPages"]["value"]:
                return results["webPages"]["value"][randint(0, 4)]["url"]

            return None  # No results found
        except requests.exceptions.RequestException as e:
            wait_time = 10 * (retries + 1)
            click.echo(f"Error fetching article: {e}. Retrying in {wait_time}s...")
            time.sleep(wait_time)
            retries += 1
    return None    

def generate_content_with_retries(gpt_assistant_prompt: str, gpt_user_prompt: str, article_query: str, include_articles: bool) -> dict:
    """Send a prompt to OpenAI with retry logic and include a reliable article fetched from Google."""
    retries = 0
    while retries < MAX_RETRIES:
        try:
            # Fetch article
            if include_articles:
                article_url = fetch_reliable_article(article_query)
                gpt_user_prompt += f"\n\nInclude an html formatted link (<a href=\"...\">learn more/find out more/check out this article for context/other variations</a>) to this article to learn more (or find out more, or go deeper...): {article_url}"
                if not article_url:
                    raise Exception("Failed to fetch article: No results found.")
            else:
                article_url = None

            # Generate content with OpenAI
            messages = [
                {"role": "assistant", "content": gpt_assistant_prompt},
                {"role": "user", "content": gpt_user_prompt},
            ]
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.7,
                top_p=0.4,
                max_tokens=1500,
                frequency_penalty=0.1,
            )
            response_text = response.choices[0].message.content
            tokens_used = response.usage.total_tokens

            return {"response": response_text, "tokens_used": tokens_used}
        except (openai.RateLimitError, Exception) as e:
            wait_time = 15 + randint(0, 8) * (retries + 1)
            click.echo(f"Error: {e}. Retrying in {wait_time}s...")
            time.sleep(wait_time)
            retries += 1
    raise Exception(f"Failed after {MAX_RETRIES} retries for OpenAI or Google.")

def process_government_function(index, gov_function, item, state_code):
    """Prepare the prompt, send it to OpenAI, and fetch articles."""
    state_data_lines = [
        f"Year {row['year']}:"
        f" State - Total Employment: {int(row['ft_employment'])}, State - Pay per Employee: {int(row['ft_pay_per_ft_employee'])}."
        f" National Average - Total Employment: {int(row['national_avg_employment'])}, National Average - Pay per Employee: {int(row['national_avg_pay_per_employee'])}."
        for row in item["timeseries"]
    ]
    state_data = "\n".join(state_data_lines)

    # Choose appropriate prompt template
    if index == 0 or index > RANKING_THRESHOLD:
        include_articles = False
        user_prompt = PROMPT_NO_ARTICLE.format(gov_function=gov_function, state_code=state_code, state_data=state_data)
    else:
        include_articles = False
        user_prompt = PROMPT_NO_ARTICLE.format(gov_function=gov_function, state_code=state_code, state_data=state_data)
        # user_prompt = PROMPT_WITH_ARTICLE.format(gov_function=gov_function, state_code=state_code, state_data=state_data)

    # Query for article search
    article_query = f"{state_code} state government employment in the {gov_function} sector since 2020"

    try:
        response_data = generate_content_with_retries(ASSISTANT_PROMPT, user_prompt, article_query, include_articles)
        return {
            "index": index,
            "gov_function": gov_function,
            "article_query": article_query,
            "assistant_prompt": ASSISTANT_PROMPT,
            "user_prompt": user_prompt,
            "summary": response_data["response"],
        }
    except Exception as e:
        return {
            "index": index,
            "gov_function": gov_function,
            "article_query": article_query,
            "assistant_prompt": ASSISTANT_PROMPT,
            "user_prompt": user_prompt,
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
    with ThreadPoolExecutor(max_workers=3) as executor:
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


# import json
# import click
# import openai
# import os
# import time
# from concurrent.futures import ThreadPoolExecutor, as_completed
# from googlesearch import search  # For fetching topical articles

# RANKING_THRESHOLD = 10  # Number of top government functions to include article details
# MAX_RETRIES = 5         # Maximum number of retries for rate-limiting errors
# ARTICLE_RESULTS = 2     # Number of articles to fetch per query

# # Initialize OpenAI client
# client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# # Static assistant prompt
# ASSISTANT_PROMPT = (
#     "You are someone who explains data to a savvy but broad audience, summarizing government "
#     "employment and pay data for a data visualization web app. Your tone is informative but friendly and creative."
# )

# # User prompt templates
# PROMPT_WITH_ARTICLE = """
# Analyze the government employment and pay data for the "{gov_function}" function in {state_code} from 2003 to 2022.

# Here is the data:
# {state_data}

# Write a three-sentence summary focusing on employment and pay trends over time, major leaps or dips, and how the category compares to national averages for pay per employee. Please include real-world context. Return nothing but the sentences in plaintext.
# """

# PROMPT_NO_ARTICLE = """
# Analyze the government employment and pay data for the "{gov_function}" function in {state_code} from 2003 to 2022.

# Here is the data:
# {state_data}

# Write a two-sentence summary focusing on employment and pay trends over time, major leaps or dips, and how the category compares to national averages for pay per employee. Return nothing but the sentences in plaintext.
# """

# def fetch_reliable_articles(query, num_results=ARTICLE_RESULTS):
#     """Fetch topical articles using Google Search."""
#     try:
#         return [url for url in search(query, num_results=num_results)]
#     except Exception as e:
#         click.echo(f"Error fetching articles: {e}")
#         return []

# def generate_content_with_retries(gpt_assistant_prompt: str, gpt_user_prompt: str) -> dict:
#     """Send a prompt to OpenAI with retry logic for rate-limiting errors."""
#     retries = 0
#     while retries < MAX_RETRIES:
#         try:
#             messages = [
#                 {"role": "assistant", "content": gpt_assistant_prompt},
#                 {"role": "user", "content": gpt_user_prompt},
#             ]
#             response = client.chat.completions.create(
#                 model="gpt-4o",
#                 messages=messages,
#                 temperature=0.7,
#                 top_p=0.5,
#                 max_tokens=1500,
#                 frequency_penalty=0.1,
#             )
#             response_text = response.choices[0].message.content
#             tokens_used = response.usage.total_tokens
#             return {"response": response_text, "tokens_used": tokens_used}
#         except openai.RateLimitError as e:
#             wait_time = 5 ** retries
#             click.echo(f"Rate limit exceeded. Retrying in {wait_time}s...")
#             time.sleep(wait_time)
#             retries += 1
#         except openai.OpenAIError as e:
#             raise Exception(f"OpenAI API error: {e}")
#     raise Exception(f"Failed to generate content after {MAX_RETRIES} retries due to rate limiting.")

# def process_government_function(index, gov_function, item, state_code):
#     """Prepare the prompt, send it to OpenAI, and fetch articles."""
#     state_data_lines = [
#         f"{row['year']}: State employment: {int(row['ft_employment'])}, State pay: {int(row['ft_pay'])}"
#         f" | National avg employment: {int(row['national_avg_employment'])}, National avg pay per employee: {int(row['national_avg_pay_per_employee'])}"
#         for row in item["timeseries"]
#     ]
#     state_data = "\n".join(state_data_lines)

#     # Choose appropriate prompt template
#     if index == 0 or index > RANKING_THRESHOLD:
#         user_prompt = PROMPT_NO_ARTICLE.format(gov_function=gov_function, state_code=state_code, state_data=state_data)
#     else:
#         user_prompt = PROMPT_WITH_ARTICLE.format(gov_function=gov_function, state_code=state_code, state_data=state_data)

#     try:
#         # Generate summary
#         response_data = generate_content_with_retries(ASSISTANT_PROMPT, user_prompt)
#         summary = response_data["response"]

#         # Fetch articles for top government functions
#         articles = []
#         if index > 0 and index <= RANKING_THRESHOLD:
#             query = f"{gov_function} government employment trends {state_code}"
#             articles = fetch_reliable_articles(query)

#         if articles:
#             summary += "\n\nTopical articles:\n" + "\n".join(articles)

#         return {
#             "index": index,  # Preserve the original order
#             "gov_function": gov_function,
#             "summary": summary,
#         }
#     except Exception as e:
#         return {
#             "index": index,
#             "gov_function": gov_function,
#             "summary": f"Error generating summary: {str(e)}",
#         }

# @click.command()
# @click.option(
#     "--input-file",
#     type=click.Path(exists=True),
#     required=True,
#     help="Path to the state JSON data file.",
# )
# @click.option(
#     "--output-file",
#     type=click.Path(),
#     required=True,
#     help="Path to save the consolidated JSON file.",
# )
# def summarize(input_file, output_file):
#     click.echo(f"Summarizing data from {input_file}")
#     state_code = input_file.split("/")[-1].replace("_", " ").replace("data.json", "").title()

#     with open(input_file, "r") as file:
#         data = json.load(file)

#     # Process data in parallel
#     results = []
#     with ThreadPoolExecutor() as executor:
#         future_to_function = {
#             executor.submit(process_government_function, index, gov_function, item, state_code): index
#             for index, (gov_function, item) in enumerate(data.items())
#         }

#         for future in as_completed(future_to_function):
#             result = future.result()
#             results.append(result)
#             click.echo(f"Processed {result['gov_function']}")

#     # Reconstitute original rank order
#     results.sort(key=lambda x: x["index"])
#     for result in results:
#         result.pop("index")  # Remove the index key for cleaner output

#     # Write consolidated JSON output
#     with open(output_file, "w") as outfile:
#         json.dump(results, outfile, indent=2)

#     click.echo(f"Consolidated summaries saved to {output_file}")


# if __name__ == "__main__":
#     summarize()
