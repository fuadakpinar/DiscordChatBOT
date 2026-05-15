# Discord ChatBOT

A small, slash-command-driven Discord bot that bridges a Discord server with
OpenAI's API. Users invoke a structured command (e.g. `/cb chat your message`)
and the bot forwards the prompt to OpenAI, then posts the model's response
back into the channel — either publicly or as an ephemeral reply visible only
to the caller.

Originally written during high school as a message-listener bot; rewritten as
a clean, slash-command-only project with first-run setup, env-driven
configuration, and a clear separation between the Discord layer and the AI
layer. Maintained as a learning / portfolio project.

---

## Features

- **Slash command architecture** — exclusively `/cb chat`, no message
  scraping, no `message_content` intent required.
- **Public prompt echo** — the caller's prompt is re-rendered as an embed
  so other people in the channel can follow the conversation.
- **Private mode** — append `--private` (or `-p`) to make the reply
  ephemeral (only the caller sees it).
- **First-run `.env` bootstrap** — if no `.env` exists, the bot prompts
  for `DISCORD_TOKEN` and `OPENAI_API_KEY` via `getpass` and writes a safe
  template locally.
- **Env-driven OpenAI config** — model, max output tokens, and temperature
  are all overridable from `.env` without code changes.
- **Lazy AI client** — `ai.py` is safe to import before `.env` exists;
  the OpenAI client is created only on the first call to `ask_ai()`.
- **Long-response chunking** — responses over Discord's 2000-character
  limit are split across multiple follow-up messages.
- **Structured logging** — Python's `logging` module with timestamps and
  severity levels, no `print()` calls in the runtime path.

## Project structure

```
DiscordChatBOT/
├── README.md
├── CHANGELOG.md
├── LICENSE
├── requirements.txt
├── main.py            # Discord entry point: bootstrap, slash commands, /cb group
└── ai.py              # OpenAI integration: lazy config + ask_ai()
```

The two source files map cleanly onto the two layers of the bot:

- `main.py` knows about Discord (intents, slash commands, embeds, ephemeral
  replies) but not about how the AI response is produced.
- `ai.py` knows about OpenAI (model, tokens, temperature, client) but not
  about Discord.

## Requirements

- Python 3.9+
- A Discord application + bot token ([Discord Developer Portal](https://discord.com/developers/applications))
- An OpenAI API key

## Setup

```bash
git clone https://github.com/fuadakpinar/DiscordChatBOT.git
cd DiscordChatBOT

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

No manual `.env` step is needed — the first run handles it (see below).

## First-run configuration

On the very first launch, if no `.env` file is present, the bot will:

1. Prompt for your `DISCORD_TOKEN` (hidden input via `getpass`).
2. Prompt for your `OPENAI_API_KEY` (hidden input via `getpass`).
3. Write a `.env` file in the project root with sensible defaults.

Generated `.env` looks like:

```
# ---- Discord ----
DISCORD_TOKEN=...
# DISCORD_GUILD_ID=

# ---- OpenAI ----
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-5.2
OPENAI_MAX_OUTPUT_TOKENS=512
OPENAI_TEMPERATURE=0.7
```

`.env` is gitignored, so your secrets stay local.

## Running the bot

```bash
python main.py
```

If `DISCORD_TOKEN` is valid, the bot logs in and syncs its slash commands:

- If `DISCORD_GUILD_ID` is set in `.env`, commands sync **to that guild
  only** (recommended during development — they appear almost instantly).
- Otherwise, commands sync **globally**, which can take up to an hour to
  propagate to all servers.

## Configuration

All runtime configuration lives in `.env`. The bot reads it on startup
(`main.py`) and the AI layer re-reads it lazily on each call (`ai.py`), so
you can tweak values without restarting just to test — though for changes
to `DISCORD_TOKEN` / `DISCORD_GUILD_ID` a restart is still required.

| Variable                   | Required | Default   | Purpose                                                  |
| -------------------------- | -------- | --------- | -------------------------------------------------------- |
| `DISCORD_TOKEN`            | yes      | —         | Bot token from the Discord Developer Portal.             |
| `DISCORD_GUILD_ID`         | no       | (unset)   | If set, slash commands sync only to this guild (fast).   |
| `OPENAI_API_KEY`           | yes      | —         | OpenAI API key.                                          |
| `OPENAI_MODEL`             | no       | `gpt-5.2` | Model identifier passed to the Responses API.            |
| `OPENAI_MAX_OUTPUT_TOKENS` | no       | `512`     | Upper bound on output length for a single response.      |
| `OPENAI_TEMPERATURE`       | no       | `0.7`     | Sampling temperature.                                    |

## Slash command usage

The bot exposes a single command group, `/cb`, with one subcommand: `chat`.

Public reply (default — everyone in the channel sees both the prompt echo
and the response):

```
/cb chat your message here
```

Private reply (only the caller sees it; no public prompt echo):

```
/cb chat --private your message here
/cb chat -p your message here
```

Flags are parsed with `shlex.split`, so you can quote arguments that
contain spaces if needed.

## Behavior notes

- **Empty prompts** are rejected with an ephemeral usage hint
  (`Usage: /cb chat <message>`).
- **Long responses** are split into 2000-character chunks and sent as
  multiple follow-ups, preserving order.
- **API timeouts** are caught and reported to the user as
  `Request timed out. Please try again.` (ephemeral).
- **Other API errors** are logged with `repr(exc)` and surfaced to the
  user as a generic `Error while generating a response.` (ephemeral) —
  no internal details are leaked into the channel.

## Roadmap

- User-scoped conversation memory (multi-turn context).
- `/cb help` subcommand.
- Per-user token / rate guardrails.
- Deployment recipes (systemd unit, container, small VPS).

The [`CHANGELOG.md`](CHANGELOG.md) tracks what has actually shipped per
release.

## Status

This is a learning / portfolio project. It works end-to-end and is safe to
run, but it intentionally stays small: a single `/cb chat` command, two
source files, and one external dependency that matters
(`discord.py` + `openai`). New features are added deliberately rather than
in bulk.

## Security notes

- Credentials are never committed — `.env` is gitignored, and interactive
  setup reads secrets via `getpass` so they don't appear in shell history
  or terminal scrollback.
- The bot does **not** request the `message_content` privileged intent;
  it only reads what users explicitly send via slash commands.
- Error messages shown in Discord are intentionally generic; full
  exception details only go to the local log.

## License

[MIT](LICENSE) © Fuad AKPINAR
