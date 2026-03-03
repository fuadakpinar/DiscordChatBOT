# Discord ChatBOT

This project is a personal experimental Discord bot originally created during my high school years and recently revisited and modernized as part of my software development learning journey.

The bot connects a Discord server with OpenAI's API using modern slash commands. Instead of responding to every message in a channel, the bot now operates through structured commands (e.g., `/cb chat`). When a user invokes a slash command, the message is forwarded to OpenAI and the generated response is sent back to Discord.

While the bot is functional, it is still under active improvement and serves primarily as a learning and experimentation project.

---

## Current Features

- Slash command architecture (`/cb chat`)
- Public prompt echo with optional private mode (`--private` / `-p`)
- AI-generated responses using OpenAI API
- Automatic `.env` bootstrap on first run
- Environment-based configuration for secure credentials
- Modular project structure (separated Discord and AI layers)

---

## Planned Improvements

- Conversation memory (user-based context)
- `/cb help` command
- Token usage limits and guardrails
- Logging system
- Deployment and hosting support

---

## Requirements

- Python 3.9+
- Discord Developer Account
- OpenAI API Key

---

## Setup & Installation

Clone the repository:

```bash
git clone https://github.com/fuadakpinar/DiscordChatBOT.git
cd DiscordChatBOT
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```


---

## First-Run Configuration (Automatic Setup)

You no longer need to manually create a `.env` file.

When you run the bot for the first time:

```bash
python main.py
```

If no `.env` file is found, the application will automatically:

- Prompt you for your `DISCORD_TOKEN`
- Prompt you for your `OPENAI_API_KEY`
- Generate a `.env` file locally with safe default configuration values

Your secrets are stored locally and are excluded from Git via `.gitignore`.

Advanced users can later modify `.env` to tune:

- `OPENAI_MODEL`
- `OPENAI_MAX_OUTPUT_TOKENS`
- `OPENAI_TEMPERATURE`

---

---

## Running the Bot

```bash
python main.py
```

If configured correctly, the bot will connect to Discord and respond to messages in servers where it has been added.

---

## Slash Command Usage

The bot now operates exclusively via slash commands.

Main command namespace:

```
/cb
```

Chat with the bot:

```
/cb chat your message here
```

Private response (only visible to you):

```
/cb chat --private your message here
```

The bot will echo your prompt publicly unless `--private` (or `-p`) is used.

---

## Author

Fuad Akpinar  
Computer Science Student

---

## Recent Updates

- Migrated from message-based responses to slash-command architecture
- Introduced `/cb chat` command namespace
- Added optional `--private` flag support
- Public prompt echo for improved UX
- Automatic `.env` bootstrap on first run
- Refactored AI layer with lazy configuration loading
- Cleaner modular architecture and improved code readability