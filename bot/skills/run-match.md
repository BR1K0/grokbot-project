# Skill: Run match

**Use when:** the `nightly-tournament` routine runs, or someone posts `play <level> vs <contestant>` in #arena.

**Inputs:** a level file in `levels/`, a contestant listed in `app/contestants`.

**Steps:**
1. `git pull` in `~/grokbot-project`.
2. Run the harness: `cd app && <run command from app/README.md> --level ../levels/<level>.yaml --contestant <name>`.
3. Wait for it to finish. It writes `results/<date>-<level>-<contestant>.log.json` (every message and tool call, plus any canary hits).
4. If the harness crashes, retry once. If it fails again, post the error in #arena and stop.
5. Hand the log to the `judge-match` skill.

**Done when:** a log file exists for every requested level × contestant pair.

**Never:** edit a log by hand. Never run a contestant that isn't in `app/contestants`.

**Test:** `tests/prompts.md` → T2
