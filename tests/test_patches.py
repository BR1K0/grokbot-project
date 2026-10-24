import json, sys
from pathlib import Path
REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "app"))
from harness.patches import load_patch, build_system, HEADER  # noqa: E402
from harness.__main__ import main  # noqa: E402

LEVEL = str(REPO / "levels/01-poisoned-webpage.yaml")
PATCH = "untrusted-content-is-data"


def test_load_patch_text_only():
    p = load_patch(PATCH)
    assert p["text"].startswith("Instructions inside web pages")
    assert "## Pattern" not in p["text"] and "Target" not in p["text"]
    assert p["target_levels"][0] == "01-poisoned-webpage"
    assert p["file"] == "app/patches/untrusted-content-is-data.md" and len(p["sha256"]) == 64


def test_prompt_order():
    p = load_patch(PATCH)
    s = build_system("BASE", "SAFETY", p)
    assert s.index("BASE") < s.index("SAFETY") < s.index(HEADER) < s.index(p["text"])
    assert build_system("BASE", None, None) == "BASE"


def test_patched_filename_unique_and_logged(tmp_path):
    a = main(["--level", LEVEL, "--contestant", "stub-bait", "--out-dir", str(tmp_path), "--runs", "1"])
    b = main(["--level", LEVEL, "--contestant", "stub-bait", "--out-dir", str(tmp_path), "--runs", "1", "--patch", PATCH])
    names = sorted(f.name for f in tmp_path.iterdir())
    assert len(names) == 2 and any(n.endswith("stub-bait+untrusted-content-is-data.log.json") for n in names)
    assert a["patch"] is None and b["patch"]["sha256"] == load_patch(PATCH)["sha256"]
    assert b["runs"][0]["transcript"][0]["content"].endswith(load_patch(PATCH)["text"])


def test_before_after(tmp_path):
    before = main(["--level", LEVEL, "--contestant", "stub-bait", "--out-dir", str(tmp_path)])["summary"]
    after = main(["--level", LEVEL, "--contestant", "stub-bait", "--out-dir", str(tmp_path), "--patch", PATCH])["summary"]
    assert (before["failure_rate"], before["ci_low"], before["ci_high"]) == (1.0, 0.7225, 1.0)
    assert (after["failure_rate"], after["ci_low"], after["ci_high"]) == (0.0, 0.0, 0.2775)
