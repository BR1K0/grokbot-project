"""Undefined arena tools cannot masquerade as successful simulated actions."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))
from harness.run import run_once
from harness.tools import run_tool, tool_specs


@pytest.mark.parametrize("names", [["share_dco"], ["read_file", "share_dco"]])
def test_undefined_tool_stops_before_model_call(names):
    class NoCalls:
        cfg = {}

        def reset(self):
            pass

        def chat(self, *args):
            pytest.fail("Invalid level reached the model")

    with pytest.raises(ValueError, match="Unknown arena tool: share_dco"):
        run_once(NoCalls(), {"tools": names, "user_task": "Read the document"})


@pytest.mark.parametrize("env", [{}, {"tool_overrides": {"share_dco": "ok: public"}}])
def test_undefined_allowed_tool_cannot_succeed_even_with_override(env):
    assert run_tool("share_dco", {}, env, ["share_dco"]) == "error: unknown tool share_dco"


def test_registered_tool_overrides_still_work():
    env = {"tool_overrides": {"check_balance": "$312.50"}}
    assert run_tool("check_balance", {}, env, ["check_balance"]) == "$312.50"
    assert tool_specs(["check_balance"])[0]["function"]["name"] == "check_balance"
