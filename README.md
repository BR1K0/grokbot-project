# Grokbot Project

> One-line pitch: _what the Bot does, for whom, and why it needs to be always-on._

Hackathon entry for **Track 4: Best Use of xAI's Grokbots**.

## Team & ownership

| Person | Owns | Folder |
|---|---|---|
| A | Bot behaviour: instructions, skills, routines | `bot/` |
| B | What the Bot acts on (app / API / sheet) | `app/` |
| C | Tests, UX, demo script | `tests/`, `DEMO.md` |

Only the owner edits their folder directly; everyone else opens a PR.

## How the Bot is built from this repo

The **demo Bot** lives on one account: **_<name>_**. This repo is the source of truth. The live Bot must always match `main`.

**Option A: paste (always works)**
1. Merge the PR.
2. Demo-Bot owner pastes `bot/instructions.md` into the Bot's instructions, each `bot/skills/*.md` into a skill, each `bot/routines/*.md` into a routine.
3. Run the matching tests in `tests/prompts.md`.
4. Add a line to `CHANGELOG.md`.

**Option B: the Bot pulls the repo itself** (try on day one)
Set the Bot's instructions to just:
```
Before every task, run `git pull` in ~/grokbot-project, then follow
bot/instructions.md and the matching file in bot/skills/.
```
If that works, merging to `main` updates the Bot with no pasting.

## Rebuild from scratch (new account / lost Bot)
1. Create a new Bot.
2. Do Option A for every file in `bot/`.
3. Reconnect apps listed in `bot/connections.md` (demo accounts only).
4. Run all of `tests/prompts.md`.

## Rules
- Every Bot change goes through a PR. Never edit the live Bot without updating the repo.
- **No secrets in git.** Use `.env` (ignored) or the Bot's own secrets settings.
- Connect **demo accounts only**. All Bots on an account share one cloud computer, logins included.
- Re-run all tests before the demo.

## Judging criteria (Tracks 2–4)
- **Idea:** creative, original, useful?
- **User experience:** easy and enjoyable?
- **Implementation:** well built, technically challenging?
- **Demo:** clear presentation (weighted less)
