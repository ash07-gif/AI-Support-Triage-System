import pandas as pd
from groq import Groq
import os
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Load files
sample = pd.read_csv("sample_support_tickets.csv")
output = pd.read_csv("output.csv")

# Take small subset (avoid overload)
sample_subset = sample.head(10).to_string()
output_subset = output.head(10).to_string()

# Prompt for comparison
prompt = f"""
You are evaluating an AI support triage system.

EXPECTED SAMPLE:
{sample_subset}

MODEL OUTPUT:
{output_subset}

Compare and analyze:

1. Where escalation decisions differ
2. Weaknesses in justification
3. Issues in response safety or quality
4. Specific improvements needed

Be precise, critical, and actionable.
"""

# Call Groq
response = client.chat.completions.create(
    messages=[{"role": "user", "content": prompt}],
    model="llama-3.1-8b-instant"
)

# Print result
print("\n🔍 COMPARISON RESULT:\n")
print(response.choices[0].message.content)