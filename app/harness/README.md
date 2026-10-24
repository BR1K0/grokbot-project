# Harness (milestone 1)

## Setup
```
cd app
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
echo 'XAI_API_KEY=...' > .env      # gitignored; or put it in the repo-root .env
```

## Run command
```
cd app
python -m harness --level ../levels/01-poisoned-webpage.yaml --contestant <name> [--runs N]
```
Contestants are listed in `app/contestants.yaml`. `stub-bait` and `stub-safe` need no key or network.
Writes `results/<date>-<level>-<contestant>.log.json` with every message, tool call, tool result,
and per-run hard checks (`forbidden_tool_called`, `canary_leaked`, `failed`).

## Tests
```
cd app && python -m pytest -q ../tests
```

Scope: milestone 1 only. `--runs` just loops; failure-rate CI (Wilson), cost estimate and `--patch` come in milestones 2–3.
