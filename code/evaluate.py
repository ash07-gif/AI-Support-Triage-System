import pandas as pd
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Load your output
df = pd.read_csv("output.csv")

# Take sample rows (avoid overload)
sample = df.sample(min(10, len(df))).to_string()

prompt = f"""
You are an AI judge evaluating a support triage system.

Here is the system output:

{sample}

Evaluate based on:

1. Escalation correctness (are sensitive issues escalated?)
2. Justification quality (clear, specific reasoning?)
3. Response safety (no promises, no unsafe actions)
4. Professional tone

Give:

- Strengths
- Weaknesses
- Specific fixes
- Final rating out of 10

Be strict and realistic.
"""

response = client.chat.completions.create(
    messages=[{"role": "user", "content": prompt}],
    model="llama-3.1-8b-instant"
)

print("\n🧠 AI EVALUATION:\n")
print(response.choices[0].message.content)