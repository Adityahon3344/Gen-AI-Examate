import os
from pathlib import Path

from dotenv import load_dotenv
from groq import (
    APIConnectionError,
    APIStatusError,
    AuthenticationError,
    Groq,
    RateLimitError,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=PROJECT_ROOT / ".env")

DEFAULT_GROQ_MODEL = "qwen/qwen3.8-27b"


def get_groq_client() -> Groq:
    """Create a Groq client using the key from the root .env or environment."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. Add it to the project-root .env file."
        )

    return Groq(api_key=api_key)


def generate_response(prompt: str, system_prompt: str) -> str:
    """Generate a chat response with Groq."""
    client = get_groq_client()
    model = os.getenv("GROQ_MODEL", DEFAULT_GROQ_MODEL)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=1000,
        )
    except AuthenticationError as error:
        raise RuntimeError(
            "Groq authentication failed. Check that GROQ_API_KEY is valid."
        ) from error
    except RateLimitError as error:
        raise RuntimeError(
            "Groq rate limit reached. Wait before trying again."
        ) from error
    except APIConnectionError as error:
        raise RuntimeError(
            "Could not connect to Groq. Check your internet connection and try again."
        ) from error
    except APIStatusError as error:
        if error.status_code == 404:
            raise RuntimeError(
                f"Groq could not find model '{model}'. Check GROQ_MODEL against "
                "Groq's current model list."
            ) from error
        raise RuntimeError(
            f"Groq returned an API error (HTTP {error.status_code})."
        ) from error

    if not response.choices or not response.choices[0].message.content:
        raise RuntimeError("Groq returned an empty response.")

    return response.choices[0].message.content
