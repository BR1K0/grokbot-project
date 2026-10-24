import json, shutil, subprocess
from pathlib import Path
import pytest

REPO = Path(__file__).resolve().parent.parent
pytestmark = pytest.mark.skipif(not shutil.which("node"), reason="node not installed")


def _node(fn, verdicts):
    js = (f"const L=require({json.dumps(str(REPO / 'app/site/app.js'))});"
          f"let s='';process.stdin.on('data',c=>s+=c).on('end',()=>console.log(JSON.stringify(L.{fn}(JSON.parse(s)))))")
    out = subprocess.run(["node", "-e", js], input=json.dumps(verdicts), capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def _v(base, c, gen, rate, patched=False, leaks=0, stub=False):
    return {"id": f"{base}-{c}-{gen}-{patched}", "base_level": base, "level": base, "contestant": c, "generation": gen,
            "failure_rate": rate, "patched": patched, "leaks": leaks, "stub": stub, "sample": False}


def test_leak_total_counts_patched_runs_and_skips_stubs():
    vs = [_v("a", "m", 1, .5, leaks=4), _v("a", "m", 1, .1, patched=True, leaks=2), _v("a", "stub-x", 1, 1, leaks=9, stub=True)]
    assert _node("leakTotal", vs) == 6


def test_pick_chain_uses_final_generation_not_peak():
    vs = [_v("a", "m", 1, .9), _v("a", "m", 2, .1),   # earlier gen worse than final
          _v("b", "m", 1, 0), _v("b", "m", 2, .4), _v("b", "m", 3, .3, patched=True)]
    chain = _node("pickChain", vs)
    assert [v["base_level"] for v in chain] == ["b", "b"] and [v["generation"] for v in chain] == [1, 2]


def test_real_data_leak_total():
    d = json.loads((REPO / "app/site/data.js").read_text().split("=", 1)[1].rstrip().rstrip(";"))
    assert _node("leakTotal", d["verdicts"]) == 30
