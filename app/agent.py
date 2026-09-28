import json
import os

import requests
from dotenv import load_dotenv
from groq import Groq

from prompts import (
    SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE,
)


load_dotenv()


HINDSIGHT_API_KEY = os.getenv(
    "HINDSIGHT_API_KEY"
)

HINDSIGHT_BASE_URL = os.getenv(
    "HINDSIGHT_BASE_URL",
    "https://api.hindsight.vectorize.io",
).rstrip("/")

BANK_ID = os.getenv(
    "HINDSIGHT_BANK_ID",
    "resolveiq-v2",
)

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-120b",
)


def hindsight_headers():
    if not HINDSIGHT_API_KEY:
        raise RuntimeError(
            "HINDSIGHT_API_KEY is missing from .env"
        )

    return {
        "Authorization": f"Bearer {HINDSIGHT_API_KEY}",
        "Content-Type": "application/json",
    }


def ensure_memory_bank():
    url = (
        f"{HINDSIGHT_BASE_URL}"
        f"/v1/default/banks/{BANK_ID}"
    )

    response = requests.put(
        url,
        headers=hindsight_headers(),
        json={
            "name": "ResolveIQ Customer Support",
            "description": (
                "Long-term customer support memory "
                "for ResolveIQ."
            ),
        },
        timeout=30,
    )

    if response.status_code not in (
        200,
        201,
    ):

        raise RuntimeError(
            "Could not create/update Hindsight memory bank: "
            f"{response.status_code} {response.text}"
        )

    return response.json()


def retain_memory(content):
    if not content:
        return None

    url = (
        f"{HINDSIGHT_BASE_URL}"
        f"/v1/default/banks/{BANK_ID}/memories"
    )

    response = requests.post(
        url,
        headers=hindsight_headers(),
        json={
            "items": [
                {
                    "content": str(content)
                }
            ]
        },
        timeout=30,
    )

    if response.status_code not in (
        200,
        201,
    ):

        raise RuntimeError(
            "Hindsight retain failed: "
            f"{response.status_code} {response.text}"
        )

    return response.json()


def recall_memory(query):
    ensure_memory_bank()

    url = (
        f"{HINDSIGHT_BASE_URL}"
        f"/v1/default/banks/{BANK_ID}"
        f"/memories/recall"
    )

    response = requests.post(
        url,
        headers=hindsight_headers(),
        json={
            "query": query
        },
        timeout=30,
    )

    if response.status_code != 200:

        raise RuntimeError(
            "Hindsight recall failed: "
            f"{response.status_code} {response.text}"
        )

    data = response.json()

    if isinstance(data, dict):

        results = data.get(
            "results",
            []
        )

        if isinstance(results, list):
            return results

    return []


def _memory_text(memory):
    if isinstance(memory, str):
        return memory

    if not isinstance(memory, dict):
        return str(memory)

    return (
        memory.get("text")
        or memory.get("content")
        or memory.get("memory")
        or memory.get("summary")
        or ""
    )


def recall_customer_history(
    customer_name,
    customer_message="",
):
    query = (
        f"Customer: {customer_name}. "
        f"Current support issue: {customer_message}. "
        f"Find relevant previous support interactions, "
        f"failed troubleshooting steps, successful solutions, "
        f"open problems, and escalations for this customer."
    )

    results = recall_memory(query)

    customer_name_lower = (
        customer_name.lower()
    )

    filtered = []

    for item in results:

        text = _memory_text(item)

        if not text:
            continue

        # Customer isolation.
        # Keep memories explicitly mentioning the customer.
        if customer_name_lower in text.lower():

            filtered.append(item)

    # If Hindsight returns memories but customer name
    # is not present in the generated memory text,
    # keep only a small number rather than mixing everything.
    if not filtered:

        return []

    return filtered[:8]


def memory_for_prompt(
    customer_name,
    customer_message,
):
    memories = recall_customer_history(
        customer_name,
        customer_message,
    )

    if not memories:
        return (
            "No previous relevant memory was found."
        )

    parts = []

    for index, memory in enumerate(
        memories,
        start=1,
    ):

        text = _memory_text(memory)

        if text:

            parts.append(
                f"{index}. {text}"
            )

    if not parts:

        return (
            "No previous relevant memory was found."
        )

    return "\n".join(parts)


def generate_support_response(
    customer_name,
    customer_message,
    memory,
):
    if not GROQ_API_KEY:

        raise RuntimeError(
            "GROQ_API_KEY is missing from .env"
        )

    client = Groq(
        api_key=GROQ_API_KEY
    )

    user_prompt = USER_PROMPT_TEMPLATE.format(
        customer_name=customer_name,
        customer_message=customer_message,
        memory=memory,
    )

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
    )

    content = (
        response.choices[0]
        .message
        .content
        .strip()
    )

    # Remove accidental markdown fences.
    if content.startswith("```"):

        content = content.replace(
            "```json",
            "",
        ).replace(
            "```",
            "",
        ).strip()

    try:

        result = json.loads(
            content
        )

    except json.JSONDecodeError:

        result = {
            "message": content,
            "recommended_action": "",
            "reason": "",
            "needs_escalation": False,
        }

    return result


def resolve_customer_issue(
    customer_name,
    customer_message,
):
    ensure_memory_bank()

    memory = memory_for_prompt(
        customer_name,
        customer_message,
    )

    result = generate_support_response(
        customer_name,
        customer_message,
        memory,
    )

    result["memory"] = memory

    return result


def record_customer_outcome(
    customer_name,
    customer_issue,
    recommended_action,
    outcome,
):
    outcome = outcome.lower().strip()

    if outcome not in (
        "worked",
        "failed",
    ):

        return None

    content = (
        f"Customer {customer_name} "
        f"reported this support issue: "
        f"{customer_issue}. "
        f"ResolveIQ recommended: "
        f"{recommended_action}. "
        f"The customer confirmed that this action "
        f"{outcome}."
    )

    return retain_memory(
        content
    )


def remember_escalation(
    customer_name,
    customer_issue,
    ai_response="",
):
    content = (
        f"Customer {customer_name} "
        f"had a support issue: "
        f"{customer_issue}. "
        f"ResolveIQ escalated this case to human support. "
        f"AI response before escalation: "
        f"{ai_response}"
    )

    return retain_memory(
        content
    )


def list_memories(
    query="",
    limit=50,
):
    ensure_memory_bank()

    url = (
        f"{HINDSIGHT_BASE_URL}"
        f"/v1/default/banks/{BANK_ID}"
        f"/memories/list"
    )

    params = {
        "limit": limit,
        "offset": 0,
    }

    if query:
        params["q"] = query

    response = requests.get(
        url,
        headers=hindsight_headers(),
        params=params,
        timeout=30,
    )

    if response.status_code != 200:

        raise RuntimeError(
            "Hindsight memory list failed: "
            f"{response.status_code} {response.text}"
        )

    data = response.json()

    # IMPORTANT:
    # The Hindsight endpoint returns an object containing
    # items, total, limit, offset.
    # Do NOT iterate over the dictionary itself.
    if isinstance(data, dict):

        items = data.get(
            "items",
            []
        )

        if isinstance(items, list):
            return items

    if isinstance(data, list):
        return data

    return []


if __name__ == "__main__":

    print(
        "Testing ResolveIQ agent..."
    )

    ensure_memory_bank()

    result = resolve_customer_issue(
        "Arjun Kumar",
        "My Wi-Fi keeps disconnecting every 10 minutes.",
    )

    print("\nMemory:")
    print(result.get("memory"))

    print("\nResponse:")
    print(result.get("message"))

    print("\nRecommended action:")
    print(
        result.get(
            "recommended_action"
        )
    )

    print("\nReason:")
    print(
        result.get(
            "reason"
        )
    )

    print("\nEscalation:")
    print(
        result.get(
            "needs_escalation"
        )
    )