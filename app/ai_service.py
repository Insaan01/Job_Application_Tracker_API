import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
AI_ENABLED = HF_API_KEY is not None

MODEL_URL = "https://router.huggingface.co/hf-inference/models/google/gemma-2b-it"

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json",
}

def _call_hf(prompt: str) -> str:
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 256,
            "temperature": 0.3,
        },
    }

    response = requests.post(
        MODEL_URL,
        headers=HEADERS,
        json=payload,
        timeout=60
    )

    if response.status_code != 200:
        raise RuntimeError(response.text)

    result = response.json()

    if isinstance(result, list) and "generated_text" in result[0]:
        return result[0]["generated_text"]

    return str(result)



def summarize_job_search(applications: list) -> str:
    if not AI_ENABLED:
        return "AI is disabled. No Hugging Face API key configured."

    try:
        prompt = f"""
You are a career assistant.

Summarize the user's job search progress based on the data below.
Highlight patterns, progress, and concerns.

Data:
{applications}

Keep the response concise and practical.
"""

        return _call_hf(prompt)

    except Exception as e:
        return f"AI service unavailable: {str(e)}"


def suggest_followups(stuck_apps: list) -> str:
    if not AI_ENABLED:
        return "AI is disabled. No Hugging Face API key configured."

    if not stuck_apps:
        return "No stuck applications. No follow-ups needed."

    try:
        prompt = f"""
You are a career coach.

Based on the following stuck job applications,
suggest clear and actionable follow-up steps.

Data:
{stuck_apps}

Keep it short and practical.
"""

        return _call_hf(prompt)

    except Exception as e:
        return f"AI service unavailable: {str(e)}"
