import httpx
import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")


async def get_ai_recommendation(query: str, tenders: list) -> str:
    tender_text = "\n".join([
        f"- Title: {t.get('title', 'N/A')}, Department: {t.get('department', 'N/A')}, "
        f"Closing: {t.get('closing_date', 'N/A')}, Value: {t.get('tender_value', 'N/A')}"
        for t in tenders[:10]
    ])

    prompt = f"""Based on these tenders, recommend the best option for the user's query.

User Query: {query}

Available Tenders:
{tender_text}

Provide a concise recommendation with reasoning."""

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json().get("response", "No recommendation available")


async def chat_with_ai(message: str) -> str:
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": message,
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json().get("response", "No response available")
