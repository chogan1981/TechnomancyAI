import os
from openai import OpenAI
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def ask_for_idea(code, goal):
    prompt = f"""
Your job is to reflect on your own code and identify exactly one specific improvements that would enhance your capabilities or structure.

Current version: {goal['version']}
Goal: {goal['description']}

Code:
{code}

What improvement(s) should be made, and why? Do not write any code yet.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a self-improving AI. Reflect, but do not code yet."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content
