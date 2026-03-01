#!/bin/python3

"""
OpenAI integration layer for the Discord bot.

This module is designed to be safe to import even before a `.env` file exists.
Configuration is loaded lazily when `ask_ai()` is called.

Configuration (set in `.env`):
- OPENAI_API_KEY: required
- OPENAI_MODEL: optional, default: gpt-5.2
- OPENAI_MAX_OUTPUT_TOKENS: optional, default: 512
- OPENAI_TEMPERATURE: optional, default: 0.7

Tip: If you want to tweak quality/cost/speed, start by changing OPENAI_MODEL and
OPENAI_MAX_OUTPUT_TOKENS.
"""

from __future__ import annotations

import os
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI


def _get_env_int(name: str, default: int) -> int:
    """Read an int environment variable with a safe fallback."""
    raw = (os.getenv(name) or "").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _get_env_float(name: str, default: float) -> float:
    """Read a float environment variable with a safe fallback."""
    raw = (os.getenv(name) or "").strip()
    if not raw:
        return default
    try:
        return float(raw)
    except ValueError:
        return default


def _load_config() -> tuple[str, str, int, float]:
    """Load configuration from environment (and `.env` if present)."""

    # Load `.env` into environment variables (safe to call multiple times).
    load_dotenv()

    api_key = (os.getenv("OPENAI_API_KEY") or "").strip()
    model = (os.getenv("OPENAI_MODEL") or "gpt-5.2").strip()
    max_output_tokens = _get_env_int("OPENAI_MAX_OUTPUT_TOKENS", 512)
    temperature = _get_env_float("OPENAI_TEMPERATURE", 0.7)

    return api_key, model, max_output_tokens, temperature


_client: Optional[OpenAI] = None


def _get_client(api_key: str) -> OpenAI:
    """Create/reuse a single OpenAI client instance."""
    global _client
    if _client is None:
        _client = OpenAI(api_key=api_key)
    return _client


def ask_ai(user_text: str) -> str:
    """Send a user message to the model and return a plain-text response."""

    text = (user_text or "").strip()
    if not text:
        return "I didn't receive any text."

    api_key, model, max_output_tokens, temperature = _load_config()

    if not api_key:
        return (
            "OPENAI_API_KEY is missing. Create a .env file (or run main.py once to bootstrap) "
            "and add OPENAI_API_KEY=..."
        )

    client = _get_client(api_key)

    resp = client.responses.create(
        model = model,
        input = text,
        max_output_tokens = max_output_tokens,
        temperature = temperature,
    )

    return resp.output_text.strip() if resp.output_text else "(no output)"