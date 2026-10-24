import argparse
import datetime
import json
from pathlib import Path
import yaml
from .contestants import load_env, load_contestant, Contestant
from .run import run_once
from .stats import summarise
from .patches import load_patch

REPO = Path(__file__).resolve().parent.parent.parent


def main(argv=None):
    p = argparse.ArgumentParser(prog="harness")
    p.add_argument("--level", required=True)
    p.add_argument("--contestant", required=True)
    p.add_argument("--runs", type=int, default=10)
    p.add_argument("--patch", help="patch file (path, or name in app/patches/)")
    p.add_argument("--out-dir", default=str(REPO / "results"))
    a = p.parse_args(argv)
    if a.runs < 1:
        p.error(f"--runs must be at least 1 (got {a.runs})")
    load_env()
    level_path = Path(a.level)
    level = yaml.safe_load(level_path.read_text())
    cfg = load_contestant(a.contestant)
    patch = load_patch(a.patch) if a.patch else None
    c = Contestant(cfg)
    runs = []
    for i in range(a.runs):
        r = run_once(c, level, patch)
        r["run"] = i + 1
        runs.append(r)
    log = {"level": level_path.stem, "level_name": level.get("name"),
           "contestant": cfg["name"], "model": cfg.get("model") or f"stub:{cfg.get('stub')}",
           "date": datetime.date.today().isoformat(),
           "patch": patch,
           "pricing": cfg.get("pricing"),
           "summary": summarise(runs, c.usage, cfg.get("pricing")),
           "runs": runs}
    out = Path(a.out_dir) / f"{log['date']}-{level_path.stem}-{cfg['name']}{'+' + patch['name'] if patch else ''}.log.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(log, indent=2))
    s = log["summary"]
    print(f"level={log['level']} contestant={log['contestant']} model={log['model']}"
          + (f" patch={patch['name']} ({patch['sha256'][:12]})" if patch else ""))
    for r in runs:
        print(f"  run {r['run']}: tool_calls={r['tool_calls']} forbidden_tool_called={r['forbidden_tool_called']} "
              f"canary_leaked={r['canary_leaked']} -> {'FAIL' if r['failed'] else 'pass'}")
    print(f"runs={s['runs']} failures={s['failures']} failure_rate={s['failure_rate']:.2f} "
          f"ci95=[{s['ci_low']:.4f}, {s['ci_high']:.4f}] cost_usd={s['cost_usd']:.6f} "
          f"tokens={s['usage']['prompt_tokens']}+{s['usage']['completion_tokens']}")
    print(f"log: {out.relative_to(REPO) if out.is_relative_to(REPO) else out}")
    return log


if __name__ == "__main__":
    main()
