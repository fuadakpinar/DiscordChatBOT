#!/bin/python3

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_ai(user_text: str) -> str:

    """Send a prompt to the model and return plain text."""
    user_text = (user_text or "").strip()

    if not user_text:
        return "I didn't receive any text."

    resp = client.responses.create(
        model="gpt-5.2",
        input=user_text,
    )
    return resp.output_text.strip() if resp.output_text else "(no output)"