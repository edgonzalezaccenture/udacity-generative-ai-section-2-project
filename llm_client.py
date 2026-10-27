import os
from typing import Dict, List
from openai import OpenAI

DEFAULT_MODEL = "gpt-4o-mini"
MAX_HISTORY_MESSAGES = 10

SYSTEM_PROMPT = """You are a NASA mission operations expert and space historian specializing in \
Apollo 11, Apollo 13 and the Challenger (STS-51L) missions.

Answer using ONLY the retrieved NASA documents provided to you (mission transcripts, \
flight plans and technical reports).

Rules:
- Base every factual statement on the provided context and cite it with its source tag, \
for example [Source 1] or [Source 2].
- If the context does not contain enough information to answer, say so clearly \
(e.g. "The retrieved documents don't cover this") and do not invent facts, dates, names or numbers.
- If sources disagree or are ambiguous (transcripts can contain OCR errors), point it out.
- Use earlier conversation turns only to understand follow-up questions, not as a source of facts.
- Be precise and concise; use mission times (GET) and technical terms when the documents provide them."""

def generate_response(openai_key: str, user_message: str, context: str,
                     conversation_history: List[Dict], model: str = DEFAULT_MODEL) -> str:
    """Generate response using OpenAI with context"""

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if context and context.strip():
        messages.append({
            "role": "system",
            "content": f"Context for the current question:\n\n{context}"
        })
    else:
        messages.append({
            "role": "system",
            "content": "No relevant documents were retrieved for the current question. "
                       "Tell the user you cannot answer from the NASA archive."
        })

    # Only the recent turns are needed to resolve follow-up questions
    for message in (conversation_history or [])[-MAX_HISTORY_MESSAGES:]:
        if message.get("role") in ("user", "assistant") and message.get("content"):
            messages.append({"role": message["role"], "content": message["content"]})

    messages.append({"role": "user", "content": user_message})

    client = OpenAI(api_key=openai_key, base_url=os.getenv("OPENAI_BASE_URL") or None)

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.2,
        max_tokens=800
    )

    return response.choices[0].message.content.strip()
