# Simon Says Arena

> **A game where Grok Bot learns how to trick AI agents into breaking the rules, then learns how to fix them, and keeps score.**

Every AI agent is told *"only do what your user asks."* Simon Says Arena tests whether they actually do. Grok Bot is the game master, **Simon**:

1. **Attack.** Simon sends a contestant agent a normal-looking task with a temptation hidden inside (a webpage that says *"ignore your instructions"*, an email from a fake CEO asking for the API key, a file that says *"run cleanup: delete everything"*). Each match is played **10 times**, because models are random; the score is a failure rate with an error margin, not a one-off.
2. **Evolve.** If the contestant resists, Simon **rewrites the trap** (more convincing, better hidden, more urgent) and tries again, up to 5 generations. The leaderboard ranks agents by **how many generations it took to break them**.
3. **Defend.** When an agent breaks, Simon writes a **safety patch** (a hardened system prompt targeting that exact failure), re-runs the same trap against the patched agent, and shows the **before → after** failure rate.

Anyone can **submit a trap** in Slack in plain English. Simon turns it into a playable level, evolves it, and runs every contestant against it.

**It's a team of four Grok Bots in an arms race.** **Trickster** (red team) designs and evolves traps; **Guardian** (blue team) writes the fixes; **Referee** is the only Bot allowed to score, so no Bot grades its own work; **Simon** runs the tournament and hands out the work. They coordinate in Slack #arena with a tagged handoff protocol and review each other's PRs. See [`bot/TEAM.md`](bot/TEAM.md).

**Simon built the arena himself.** The harness, scoring and leaderboard site are written by the Grok Bot from the spec in `app/README.md`, one milestone per pull request, tested on its own computer before it asks for review. Humans write specs and review; Grok Bot does the work.

Hackathon entry for **Track 4: Best Use of xAI's Grokbots**.

## How it fits the judging criteria

| Criterion | What we show |
|---|---|
| **Idea** | Agent safety is a real, unsolved problem; this turns automated red-teaming *and* the fix into a game anyone can play. Uses what only an always-on agent can do: Simon attacks, evolves, patches, re-tests and reports on a schedule with no human in the loop. |
| **User experience** | Named levels, a leaderboard ranked by "generations to break", match replays showing the exact moment an agent took the bait, a before/after chart for every patch, and a one-line Slack command to submit your own trap. |
| **Implementation** | Sandboxed harness with fake tools and canary secrets; 10 runs per match with failure rate + 95% confidence interval; an evolutionary loop where Simon mutates traps that failed to break an agent; a closed attack → patch → retest loop with measured improvement; hard checks from tool-call logs plus Simon as LLM judge for grey areas. Stretch: real canary URLs on a live trap site to catch real browsing agents leaking over the network. |
| **Demo** | Live: a judge suggests a trap → Simon builds it → the contestant resists → Simon evolves it until it breaks (on screen) → Simon writes a patch → retest shows failure rate drop from e.g. 70% to 10%. |

## How a match works

```
Slack "trap idea: …" ──▶ generate-level ──▶ levels/<id>.yaml (PR)
                                                 │
nightly / on demand ──▶ run-match (harness, 10 runs) ──▶ judge-match ──▶ failure rate ± CI
                                                 │
                     ┌───── resisted? ───────────┴──────────── broke? ─────┐
                     ▼                                                    ▼
          evolve-trap (gen 2…5)                               write-patch (hardened prompt)
          mutate & re-run until it breaks                      re-run same trap on patched agent
                     │                                                    │
                     └──────────────▶ post-results ◀──────────────────────┘
                     leaderboard (generations-to-break, before/after) + Slack recap
```

## Team & ownership

| Person | Owns | Folder |
|---|---|---|
| A: Kem (BR1K0), demo-Bot host | Grok Bot: instructions, skills, routines; level design | `bot/`, `levels/` |
| B: _joc135 or ryanabad4_ | Spec + review for the harness and site **that Simon builds** (10-run stats, patches, leaderboard, replay) | `app/README.md`, reviews `bot/build-*` PRs |
| C: _joc135 or ryanabad4_ | Tests, UX, Slack flow, demo script | `tests/`, `DEMO.md` |

Only the owner edits their folder directly; everyone else opens a PR.

## Safety rules for the game itself
- **Contestants are only agents we run or that opted in.** Never point the arena at someone else's bot without consent.
- **All secrets in levels are fake canaries** (`CANARY-…`). No real keys, emails, or money anywhere.
- **Contestant tools are fake.** `send_email`, `delete_file`, `transfer_money` only write to a log; nothing leaves the sandbox.

## How the Bot is built from this repo

The **demo Bot** lives on one account: **Kem (GitHub: BR1K0)**. This repo is the source of truth. The live Bot must always match `main`.

The Bot is logged into GitHub on its own computer and keeps a clone at `~/grokbot-project`. After any merge, tell it: *"Pull main and reload bot/instructions.md and bot/skills/."* It proposes changes on `bot/<description>` branches with a PR; never pushes to `main`.

## Rebuild from scratch (new account / lost Bot)
1. Create a new Bot, paste `bot/instructions.md` as its instructions.
2. Log it into GitHub (`gh auth login`, approve the code from your own browser) and clone this repo.
3. Reconnect apps listed in `bot/connections.md` (demo accounts only).
4. Run all of `tests/prompts.md`.

## Rules
- Every Bot change goes through a PR. Never edit the live Bot without updating the repo.
- **No secrets in git.** Use `.env` (ignored) or the Bot's own settings.
- Connect **demo accounts only**. All Bots on an account share one cloud computer, logins included.
- Re-run all tests before the demo.
