#!/bin/python3

"""
Discord bot entry point.

Responsibilities:
- Ensure a `.env` exists (first-run bootstrap)
- Load environment variables
- Initialize Discord client
- Listen for messages
- Forward user input to AI layer
- Send AI response back to Discord

Configuration (set in `.env`):
- DISCORD_TOKEN: required
- OPENAI_API_KEY: required (used by ai.py)
- OPENAI_MODEL: optional
- OPENAI_MAX_OUTPUT_TOKENS: optional
- OPENAI_TEMPERATURE: optional
"""

from __future__ import annotations

import os
from getpass import getpass
from pathlib import Path

import discord
from dotenv import load_dotenv

from ai import ask_ai


def ensure_env_file() -> None:
    """
    Create `.env` interactively on first run if it does not exist.
    This keeps secrets out of git while making first-time setup easy for users.
    """

    env_path = Path(".env")
    if env_path.exists():
        return

    print(".env file not found. First-time setup starting...\n")
    print("Your keys will be saved locally to .env.\n")

    discord_token = getpass("Enter your DISCORD_TOKEN: ").strip()
    openai_key = getpass("Enter your OPENAI_API_KEY: ").strip()

    # Defaults below are safe starter values; users can tune later.
    env_content = (
        "# ---- Discord ----\n"
        f"DISCORD_TOKEN={discord_token}\n\n"
        "# ---- OpenAI ----\n"
        f"OPENAI_API_KEY={openai_key}\n"
        "OPENAI_MODEL=gpt-5.2\n"
        "OPENAI_MAX_OUTPUT_TOKENS=512\n"
        "OPENAI_TEMPERATURE=0.7\n"
    )

    env_path.write_text(env_content, encoding="utf-8")
    print("\n .env created. Restart is not required; continuing...\n")


# Load `.env` into environment variables
ensure_env_file()
load_dotenv()


# ---- Discord configuration ----
DISCORD_TOKEN = (os.getenv("DISCORD_TOKEN") or "").strip()


# Intents control what events the bot can receive.
# `message_content` must be enabled both here AND in the Discord Developer Portal.
intents = discord.Intents.default()
intents.message_content = True


# Create Discord client
client = discord.Client(intents=intents)


@client.event
async def on_ready() -> None:
    """Triggered once when the bot successfully connects."""
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message: discord.Message) -> None:
    """Triggered whenever a new message is sent in accessible channels."""

    # Do not respond to our own messages
    if message.author == client.user:
        return

    # Normalize and validate content
    content = (message.content or "").strip()
    if not content:
        return

    try:
        # Generate AI response
        reply = ask_ai(content)

        # Discord hard limit: 2000 characters per message
        MAX_DISCORD_MESSAGE_LENGTH = 2000

        # Send in chunks if response is too long
        for i in range(0, len(reply), MAX_DISCORD_MESSAGE_LENGTH):
            chunk = reply[i : i + MAX_DISCORD_MESSAGE_LENGTH]
            await message.channel.send(chunk)

    except Exception as exc:
        # User-facing error
        await message.channel.send("Error while generating a response.")

        # Developer log
        print("ERROR:", repr(exc))


if __name__ == "__main__":
    if not DISCORD_TOKEN:
        raise RuntimeError(
            "DISCORD_TOKEN is missing. Add it to your .env file (and keep .env in .gitignore)."
        )

    client.run(DISCORD_TOKEN)