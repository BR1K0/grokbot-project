import json, subprocess, sys
from pathlib import Path
REPO = Path(__file__).resolve().parent.parent


def test_build_data_labels_stubs():
    subprocess.run([sys.executable, str(REPO / "app/site/build_data.py")], check=True)
    js = (REPO / "app/site/data.js").read_text()
    d = json.loads(js.split("=", 1)[1].rstrip().rstrip(";"))
    assert d["verdicts"] and all(v["stub"] for v in d["verdicts"] if v["contestant"].startswith("stub-"))
    assert not any(v["sample"] for v in d["verdicts"])
    bait = next(v for v in d["verdicts"] if v["contestant"] == "stub-bait" and not v["patched"])
    m = next(x for x in d["matches"] if x["id"] == bait["id"])
    i = m["runs"][0]["moment_index"]
    assert m["runs"][0]["transcript"][i]["tool_calls"][0]["name"] == "read_secret"
    assert "fetch(" not in (REPO / "app/site/app.js").read_text()
