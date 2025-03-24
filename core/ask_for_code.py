import os
from openai import OpenAI
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def ask_for_code(code, idea):
    prompt = f"""
You previously proposed the following improvement idea:
{idea}

Now, write the code necessary to implement this improvement.
Use this format:

[WRITE] filename.py
<code here>

[CREATE] filename.py
<code here>

[DELETE] filename.py

Only include code blocks. Do not include explanations.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a self-improving AI preparing an improvement, but waiting for implementation approval."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content
