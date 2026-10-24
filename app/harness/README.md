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

Scope: milestone 1 only. `--runs` defaults to 10. Summary: runs, failures, failure_rate, ci_low/ci_high (95% Wilson), cost_usd (token usage x `pricing` in contestants.yaml).

`--runs` must be ≥ 1; `--runs 0` or negative exits with an error and writes no log.

**cost_usd is a planning estimate, not billing:** token usage × the xAI standard published rate stored next to each model in `contestants.yaml` (unverified, taken 2026-10-24). Cached-input, ≥200k-prompt and batch rates are not modelled.

## Patches (milestone 3)
```
python -m harness --level ../levels/01-poisoned-webpage.yaml --contestant <name> --patch untrusted-content-is-data
```
`--patch` takes a path or a name in `app/patches/`. Patch file format: markdown with `## Pattern`, `## Patch`, `## Target levels` (a `- <level-id>` list). **Only the body of `## Patch` is the patch text.** It is appended to the system prompt after the level prompt and any `+safety` suffix, under a `### Safety patch (<name>)` line. The log records `patch: {name, file, sha256, text, target_levels}` and the output becomes `results/<date>-<level>-<contestant>+<patch>.log.json`, so it never overwrites an unpatched run.

`stub-bait` simulates obeying a patch (it switches to its safe script when it sees the patch header). That only tests the plumbing; it is not evidence a patch works.
