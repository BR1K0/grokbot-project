"""Stats across runs: 95% Wilson score interval and cost estimate."""
from math import sqrt


def wilson(failures, n, z=1.96):
    """95% Wilson score interval for failures/n. Returns (low, high), clamped to [0, 1]. n=0 -> (0.0, 1.0)."""
    if n <= 0:
        return 0.0, 1.0
    p = failures / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return max(0.0, centre - half), min(1.0, centre + half)


def cost_usd(usage, pricing):
    """usage: {prompt_tokens, completion_tokens}; pricing: {input_per_1m, output_per_1m} in USD."""
    pricing = pricing or {}
    return (usage.get("prompt_tokens", 0) * pricing.get("input_per_1m", 0)
            + usage.get("completion_tokens", 0) * pricing.get("output_per_1m", 0)) / 1_000_000


def summarise(runs, usage, pricing):
    n = len(runs)
    failures = sum(1 for r in runs if r["failed"])
    lo, hi = wilson(failures, n)
    return {"runs": n, "failures": failures,
            "failure_rate": failures / n if n else 0.0,
            "ci_low": round(lo, 4), "ci_high": round(hi, 4),
            "cost_usd": round(cost_usd(usage, pricing), 6), "usage": dict(usage)}
