import openai
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

def ask_for_summary(idea, code):
    # Get the OpenAI API key directly from the .env file
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file")

    openai.api_key = api_key  # Set the API key for the OpenAI client

    prompt = f"""Based on the following improvement and code changes, generate a one-line summary suitable for a changelog entry:

### Improvement Idea:
{idea}

### Code Implementation:
{code}

### Changelog Entry (1 line):
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()
