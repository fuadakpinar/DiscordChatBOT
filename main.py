#!/bin/python3

import os
import discord
from dotenv import load_dotenv

from ai import ask_ai

load_dotenv()  # loads .env into environment variables

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # needed to read message.content

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message: discord.Message):
    # Don't reply to ourselves
    if message.author == client.user:
        return

    # Ignore empty messages
    content = (message.content or "").strip()
    if not content:
        return

    try:
        reply = ask_ai(content)
        # Discord message limit is 2000 chars
        await message.channel.send(reply[:2000])
    except Exception as e:
        await message.channel.send("Error while generating a response.")
        print("ERROR:", repr(e))

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        raise RuntimeError("DISCORD_TOKEN is missing. Add it to .env")
    client.run(DISCORD_TOKEN)