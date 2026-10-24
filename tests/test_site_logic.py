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
    # independent sum: same notion of "real" as app.js (not stub, not sample; patched runs included)
    expected = sum(v.get("leaks") or 0 for v in d["verdicts"] if not v.get("stub") and not v.get("sample"))
    assert expected > 0
    assert _node("leakTotal", d["verdicts"]) == expected


def _call(fn, *args):
    js = (f"const L=require({json.dumps(str(REPO / 'app/site/app.js'))});"
          f"let s='';process.stdin.on('data',c=>s+=c).on('end',()=>console.log(JSON.stringify(L.{fn}(...JSON.parse(s)))))")
    out = subprocess.run(["node", "-e", js], input=json.dumps(list(args)), capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def test_referee_badge_only_on_referee_judgement_fields():
    v = {"verdict_by": "Referee", "referee_fields": ["moment", "reasoning", "failure_rate"],
         "moment": "m", "reasoning": "r", "defence": "d", "failure_rate": .5, "referee": {"failure_rate": .9}}
    assert _call("refereeCredit", v, "moment") and _call("refereeCredit", v, "reasoning")
    assert not _call("refereeCredit", v, "defence")          # not in referee_fields
    assert not _call("refereeCredit", v, "failure_rate")     # metrics never credited, even if listed
    assert not _call("refereeCredit", v, "outcome")
    assert _call("refereeJudgement", v) == [{"field": "moment", "text": "m"}, {"field": "reasoning", "text": "r"}]
    hc = dict(v, verdict_by="build_data.py")
    assert not _call("refereeCredit", hc, "moment") and _call("refereeJudgement", hc) == []
    assert _call("refereeJudgement", {"moment": "x"}) == []


def test_real_data_has_no_referee_badges_unless_referee_judged():
    d = json.loads((REPO / "app/site/data.js").read_text().split("=", 1)[1].rstrip().rstrip(";"))
    for v in d["verdicts"]:
        if v.get("verdict_by") != "Referee":
            assert _call("refereeJudgement", v) == []


def test_featured_intro_mentions_patched_rerun_only_with_a_patch():
    # Joel Choi's review: the intro promised "then a patched rerun" even when the chain had no patch
    chain = [_v("01", "m", 1, .2), _v("01", "m", 2, .9)]
    assert _call("featuredPatch", chain, chain) is None
    assert "patched rerun" not in _call("featuredIntro", chain, None)
    p = _v("01", "m", 1, 0.0, patched=True)
    vs = chain + [_v("01", "m", 1, 0.0, patched=True, stub=True)]
    assert _call("featuredPatch", chain, vs) is None                      # stub patches never count
    vs = chain + [p, dict(p, id="other-round", round="t14")]
    got = _call("featuredPatch", chain, vs)
    assert got["id"] == p["id"]                                          # same round (historical) only
    assert _call("featuredIntro", chain, got).endswith("then a patched rerun.")
    assert _call("featuredIntro", chain[:1], None) == "the recorded generation of this trap."


def test_round_stats_keep_n_and_ci_for_round_groups():
    v = {"round": "t14", "runs": 10, "ci_low": 0.7225, "ci_high": 1.0}
    assert _call("roundStats", v) == "n=10 · 95% CI 72.3–100.0%"
    assert _call("roundStats", dict(v, round=None)) == ""
