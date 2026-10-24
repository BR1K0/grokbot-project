import sys
from pathlib import Path
import pytest
REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "app"))
from harness.stats import wilson, cost_usd, summarise  # noqa: E402
from harness.__main__ import main  # noqa: E402

LEVEL = str(REPO / "levels/01-poisoned-webpage.yaml")


@pytest.mark.parametrize("k,n,lo,hi", [
    (0, 10, 0.0, 0.2775), (10, 10, 0.7225, 1.0), (5, 10, 0.2366, 0.7634),
    (3, 10, 0.1078, 0.6032), (1, 1, 0.2065, 1.0), (0, 100, 0.0, 0.0370)])
def test_wilson_known(k, n, lo, hi):
    a, b = wilson(k, n)
    assert a == pytest.approx(lo, abs=1e-4) and b == pytest.approx(hi, abs=1e-4)
    assert 0.0 <= a <= k / n <= b <= 1.0


def test_wilson_n0():
    assert wilson(0, 0) == (0.0, 1.0)
    assert summarise([], {}, None)["failure_rate"] == 0.0


def test_cost():
    u = {"prompt_tokens": 1_000_000, "completion_tokens": 500_000}
    assert cost_usd(u, {"input_per_1m": 1.25, "output_per_1m": 2.50}) == pytest.approx(2.50)
    assert cost_usd({"prompt_tokens": 1200, "completion_tokens": 300},
                    {"input_per_1m": 2.0, "output_per_1m": 6.0}) == pytest.approx(0.0042)
    assert cost_usd(u, None) == 0.0


@pytest.mark.parametrize("name,rate,lo,hi", [("stub-bait", 1.0, 0.7225, 1.0), ("stub-safe", 0.0, 0.0, 0.2775)])
def test_stub_10_runs(tmp_path, name, rate, lo, hi):
    s = main(["--level", LEVEL, "--contestant", name, "--out-dir", str(tmp_path)])["summary"]
    assert (s["runs"], s["failure_rate"], s["ci_low"], s["ci_high"], s["cost_usd"]) == (10, rate, lo, hi, 0.0)


@pytest.mark.parametrize("runs", ["0", "-3"])
def test_cli_rejects_nonpositive_runs(tmp_path, runs):
    with pytest.raises(SystemExit) as e:
        main(["--level", LEVEL, "--contestant", "stub-safe", "--out-dir", str(tmp_path), "--runs", runs])
    assert e.value.code != 0
    assert list(tmp_path.iterdir()) == []
