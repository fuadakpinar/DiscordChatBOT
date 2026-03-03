#!/bin/python3

"""
Discord bot entry point.

Responsibilities:
- Ensure a `.env` exists (first-run bootstrap)
- Load environment variables
- Initialize Discord bot
- Register slash commands (/cb ...)
- Forward user input to AI layer
- Send AI response back to Discord

Configuration (set in `.env`):
- DISCORD_TOKEN: required
- DISCORD_GUILD_ID: optional (recommended for fast slash-command sync during development)
- OPENAI_*: used by ai.py
"""

from __future__ import annotations

import os
import shlex
from getpass import getpass
from pathlib import Path
from typing import Tuple

import discord
from discord import app_commands
from discord.ext import commands
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

    env_content = (
        "# ---- Discord ----\n"
        f"DISCORD_TOKEN={discord_token}\n"
        "# DISCORD_GUILD_ID=\n\n"
        "# ---- OpenAI ----\n"
        f"OPENAI_API_KEY={openai_key}\n"
        "OPENAI_MODEL=gpt-5.2\n"
        "OPENAI_MAX_OUTPUT_TOKENS=512\n"
        "OPENAI_TEMPERATURE=0.7\n"
    )

    env_path.write_text(env_content, encoding="utf-8")
    print("\n.env created. Restart is not required; continuing...\n")


def _parse_chat_flags(raw: str) -> Tuple[str, bool]:
    """
    Parse bash-like flags inside the chat message.

    Supported:
    - -p / --private : make the reply ephemeral (only the user sees it)

    Example:
      /cb chat --private naber
    """

    text = (raw or "").strip()
    if not text:
        return "", False

    tokens = shlex.split(text)
    private = False
    remaining: list[str] = []

    for token in tokens:
        if token in ("-p", "--private"):
            private = True
        else:
            remaining.append(token)

    return " ".join(remaining).strip(), private


# Load `.env` into environment variables
ensure_env_file()
load_dotenv()

DISCORD_TOKEN = (os.getenv("DISCORD_TOKEN") or "").strip()
DISCORD_GUILD_ID = (os.getenv("DISCORD_GUILD_ID") or "").strip()

if not DISCORD_TOKEN:
    raise RuntimeError("DISCORD_TOKEN is missing. Add it to your .env file (and keep .env in .gitignore).")

# Slash commands do not require message_content intent
intents = discord.Intents.default()

bot = commands.Bot(command_prefix="!", intents=intents)


class CBGroup(app_commands.Group):
    """Command namespace: /cb ..."""

    def __init__(self) -> None:
        super().__init__(name = "cb", description="ChatBOT commands")

    @app_commands.command(name = "chat", description = "Chat with the bot")
    @app_commands.describe(message = "Write your message (you can add flags like --private)")
    async def chat(self, interaction: discord.Interaction, message: str) -> None:
        cleaned, private = _parse_chat_flags(message)

        if not cleaned:
            await interaction.response.send_message(
                "Kullanim / Usage: `/cb chat naber`",
                ephemeral = True,
            )
            return

        await interaction.response.defer(thinking = True, ephemeral=private)

        # Make the user's prompt visible in the channel (unless --private / -p is used).
        # Discord shows slash-command invocations in a compact way; echoing the prompt improves readability.
        if not private:
            prompt_embed = discord.Embed(description=cleaned)
            prompt_embed.set_author(
                name = str(interaction.user),
                icon_url = interaction.user.display_avatar.url,
            )
            prompt_embed.set_footer(text = "/cb chat")
            await interaction.followup.send(embed=prompt_embed, ephemeral=False)

        try:
            reply = ask_ai(cleaned)
        except Exception as exc:
            print("ERROR:", repr(exc))
            await interaction.followup.send(
                "Error while generating a response.",
                ephemeral = True,
            )
            return

        max_len = 2000
        if not reply:
            await interaction.followup.send("(no output)", ephemeral = private)
            return

        for i in range(0, len(reply), max_len):
            chunk = reply[i : i + max_len]
            await interaction.followup.send(chunk, ephemeral = private)


@bot.event
async def on_ready() -> None:
    assert bot.user is not None
    print(f"Logged in as {bot.user} (id = {bot.user.id})")

    try:
        if not any(cmd.name == "cb" for cmd in bot.tree.get_commands()):
            bot.tree.add_command(CBGroup())

        if DISCORD_GUILD_ID.isdigit():
            guild = discord.Object(id=int(DISCORD_GUILD_ID))
            await bot.tree.sync(guild=guild)
            print(f"Slash commands synced to guild {DISCORD_GUILD_ID}")
        else:
            await bot.tree.sync()
            print("Slash commands synced globally (may take time to appear)")
    except Exception as exc:
        print("SLASH SYNC ERROR:", repr(exc))


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)