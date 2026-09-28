import os

import requests
from dotenv import load_dotenv


load_dotenv()


API_KEY = os.getenv(
    "HINDSIGHT_API_KEY"
)

BASE_URL = os.getenv(
    "HINDSIGHT_BASE_URL",
    "https://api.hindsight.vectorize.io",
).rstrip("/")

BANK_ID = os.getenv(
    "HINDSIGHT_BANK_ID",
    "resolveiq-v2",
)


def headers():
    if not API_KEY:
        raise RuntimeError(
            "HINDSIGHT_API_KEY is missing from .env"
        )

    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }


def ensure_bank():
    url = (
        f"{BASE_URL}"
        f"/v1/default/banks/{BANK_ID}"
    )

    response = requests.put(
        url,
        headers=headers(),
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
            f"{response.status_code}: "
            f"{response.text}"
        )

    return response.json()


def test_retain():
    url = (
        f"{BASE_URL}"
        f"/v1/default/banks/{BANK_ID}/memories"
    )

    response = requests.post(
        url,
        headers=headers(),
        json={
            "items": [
                {
                    "content": (
                        "ResolveIQ system test memory. "
                        "This memory is only for verifying "
                        "Hindsight connectivity."
                    )
                }
            ]
        },
        timeout=30,
    )

    print(
        "Status:",
        response.status_code,
    )

    print(
        response.text
    )


if __name__ == "__main__":

    print(
        "Testing Hindsight..."
    )

    result = ensure_bank()

    print(
        "Memory bank ready:",
        BANK_ID,
    )

    print(
        result
    )

    print(
        "\nTesting memory retain..."
    )

    test_retain()