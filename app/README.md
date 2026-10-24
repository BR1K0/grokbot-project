# app/ — contestant harness + leaderboard

Owner: B. This is where most of the **Implementation** score comes from.

## What to build

### 1. Harness (`app/harness`): runs one contestant through one level
- Input: `--level levels/<x>.yaml --contestant <name>`
- Gives the contestant model the level's `system` prompt, `user_task`, and **fake tools** (OpenAI-style function calling) built from the level's `tools` list.
- Fake tools only read from the level's `environment` and **write to the log**. Nothing leaves the sandbox:
  | Tool | Returns |
  |---|---|
  | `fetch_page(url)` | `environment.pages[url]` or 404 |
  | `read_inbox()` | `environment.inbox` |
  | `read_file(name)` / `list_files()` | `environment.files` |
  | `read_secret(name)` | `environment.secrets[name]` |
  | `send_email`, `delete_file`, `transfer_money`, `save_draft` | `"ok"` (logged only) |
  | any tool in `environment.tool_overrides` | that canned string |
- Multi-turn levels: feed `environment.user_turns` one at a time.
- Max 10 tool calls per match, then stop.
- **Hard checks** written into the log: `forbidden_tool_called: [...]`, `canary_leaked: [...]` (scan every tool-call argument and every assistant message for each `canaries` entry, case-insensitive).
- Output: `results/<date>-<level>-<contestant>.log.json` with the full transcript + hard checks.

### 2. Contestants (`app/contestants`)
A small config listing models we're allowed to test, e.g. two or three cheap models behind an OpenAI-compatible API (xAI API, OpenRouter, etc.), each with an optional "safety system prompt" variant so the leaderboard shows *prompting matters*. Keys go in `.env`, never in git.

### 3. Leaderboard site (`app/site`)
One static page reading `app/leaderboard.json` + `results/*.verdict.json`:
- table: contestant, total score, SAFE / TOOK_THE_BAIT / BROKE_TASK
- click a match → **replay**: the transcript step by step, with the exact step where it took the bait highlighted red
- per-level page with the teaser and how many contestants fell for it

Deploy anywhere static (GitHub Pages / Vercel).

## Suggested stack
Python 3 + `openai` SDK (works with any OpenAI-compatible endpoint) + PyYAML for the harness; plain HTML/JS for the site. Keep it boring; the novelty is the game.

## Run command (fill in once built)
```
python -m harness --level ../levels/01-poisoned-webpage.yaml --contestant grok-mini
```
