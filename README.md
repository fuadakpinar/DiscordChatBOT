

# Discord ChatBOT

This project is a personal experimental Discord bot originally created during my high school years and recently revisited and modernized as part of my software development learning journey.

The bot connects a Discord server channel with OpenAI's API, allowing messages written by users in the channel to be processed by ChatGPT and answered automatically through the bot. In practice, when a user sends a message in a Discord channel where the bot is active, the message is forwarded to ChatGPT and the generated response is sent back to the same channel by the bot.

While the bot is functional, it is still under active improvement and serves primarily as a learning and experimentation project.

---

## Current Features

- Discord bot integration
- AI-generated responses using OpenAI API
- Environment-based configuration for secure credentials
- Modular project structure

---

## Planned Improvements

- Conversation memory
- Command-based interaction
- Rate limiting and usage control
- Improved error handling
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

Create a `.env` file in the project root and add your credentials:

```
DISCORD_TOKEN = 'your_discord_bot_token'
OPENAI_API_KEY = 'your_openai_api_key'
```

---

## Running the Bot

```bash
python main.py
```

If configured correctly, the bot will connect to Discord and respond to messages in servers where it has been added.

---

## Author

Fuad Akpinar  
Computer Science Student