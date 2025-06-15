import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")  # Set this env variable securely

def get_financial_advice(transactions_summary: str) -> str:
    prompt = f"""You are a helpful financial advisor. Given the following transaction summary, provide actionable advice to improve financial health:

    {transactions_summary}

    Advice:"""

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=300,
        temperature=0.7,
        n=1,
        stop=None,
    )

    advice = response.choices[0].text.strip()
    return advice
