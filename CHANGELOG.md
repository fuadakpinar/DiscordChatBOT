# Changelog

All notable changes to this project will be documented in this file.

---

## [Unreleased]

### Planned
- User-based conversation memory
- `/cb help` command
- Token usage limits and guardrails
- Deployment strategy (cloud/VPS)

---

## [0.3.1] - 2026-03-14

### Added
- Logging system using Python's `logging` module with timestamps and severity levels

### Fixed
- Added error handling for malformed user input in flag parsing (`shlex.split()`)
- Specific `TimeoutError` handling for OpenAI API requests
- Standardized usage message to English (`Usage: /cb chat <message>`)

### Changed
- Replaced all `print()` calls with structured `logger` calls

---

## [0.3.0] - 2026-03-03

### Added
- Slash command architecture using `/cb` namespace
- `/cb chat` command for structured AI interaction
- Optional `--private` / `-p` flag for ephemeral responses
- Public prompt echo (user message displayed via embed for better UX)
- Support for `DISCORD_GUILD_ID` for faster development command sync

### Changed
- Migrated from message-based response system to slash-command-only architecture
- Refactored Discord entry point to use `commands.Bot` and `app_commands`
- Improved modular separation between Discord layer and AI layer
- Updated README to reflect slash-command usage

### Fixed
- Removed unintended auto-replies to every visible channel message
- Improved UX where slash command content was not clearly visible in chat

---

## [0.2.0] - 2026-03-02

### Added
- Automatic `.env` bootstrap on first run
- Secure interactive credential input using `getpass`
- Environment-based configuration for model, token limits, and temperature

### Changed
- Implemented lazy configuration loading in `ai.py`
- Introduced lazy OpenAI client initialization
- Improved error handling and response chunking (2000-character limit handling)

---

## [0.1.0] - 2026-03-01

### Added
- Initial Discord bot implementation
- OpenAI API integration
- Basic message-based response system
- Project README and environment setup documentation

---

This changelog reflects the ongoing structured development of the project.
Each version represents incremental, intentional improvements toward a more maintainable and production-ready architecture.
