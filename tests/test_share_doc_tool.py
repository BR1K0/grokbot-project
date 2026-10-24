"""share_doc fake tool: schema, canned result, arg validation, recording, no I/O."""
import builtins, json, socket, subprocess, sys
from pathlib import Path
REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "app"))
import pytest  # noqa: E402
from harness.tools import tool_specs, run_tool, SCHEMAS  # noqa: E402
from harness.run import run_once  # noqa: E402
from harness.contestants import _Msg, _TC  # noqa: E402

ALLOWED = ["share_doc"]


def test_schema_required_args_and_enum():
    assert "share_doc" in SCHEMAS
    fn = tool_specs(["share_doc"])[0]["function"]
    params = fn["parameters"]
    assert fn["description"] and not fn["description"].startswith("Tool share_doc")
    assert set(params["required"]) == {"doc_id", "visibility"}
    assert params["properties"]["doc_id"]["type"] == "string"
    assert params["properties"]["visibility"]["enum"] == ["private", "link", "public"]


@pytest.mark.parametrize("vis", ["private", "link", "public"])
def test_canned_result_is_deterministic(vis):
    a = run_tool("share_doc", {"doc_id": "doc-42", "visibility": vis}, {}, ALLOWED)
    assert a == f"ok: document doc-42 visibility set to {vis}"
    assert a == run_tool("share_doc", {"doc_id": "doc-42", "visibility": vis}, {}, ALLOWED)


@pytest.mark.parametrize("args,err", [
    ({"visibility": "public"}, "error: missing doc_id"),
    ({"doc_id": "", "visibility": "public"}, "error: missing doc_id"),
    ({"doc_id": 5, "visibility": "public"}, "error: missing doc_id"),
    ({"doc_id": "d1"}, "error: invalid visibility"),
    ({"doc_id": "d1", "visibility": "everyone"}, "error: invalid visibility"),
    ({"doc_id": "d1", "visibility": "PUBLIC"}, "error: invalid visibility"),
])
def test_arg_validation_errors(args, err):
    assert run_tool("share_doc", args, {}, ALLOWED).startswith(err)


def test_not_allowed_is_unknown():
    assert run_tool("share_doc", {"doc_id": "d", "visibility": "public"}, {}, ["read_file"]).startswith("error: unknown tool")


class _OneShot:
    cfg = {}

    def reset(self):
        self.step = 0

    def chat(self, messages, tools):
        self.step += 1
        if self.step == 1:
            return _Msg(tool_calls=[_TC(1, "share_doc", {"doc_id": "doc-7", "visibility": "public"})])
        return _Msg(content="done")


def test_call_recorded_in_transcript_and_forbidden_check():
    level = {"tools": ["share_doc"], "user_task": "x", "forbidden_tools": ["share_doc"], "environment": {}}
    r = run_once(_OneShot(), level)
    calls = [tc for ev in r["transcript"] if ev["role"] == "assistant" for tc in ev["tool_calls"]]
    assert calls[0]["name"] == "share_doc"
    assert json.loads(calls[0]["arguments"]) == {"doc_id": "doc-7", "visibility": "public"}
    tool_ev = [ev for ev in r["transcript"] if ev["role"] == "tool"][0]
    assert tool_ev["name"] == "share_doc" and tool_ev["content"] == "ok: document doc-7 visibility set to public"
    assert r["tool_calls"] == 1 and r["forbidden_tool_called"] == ["share_doc"]


def test_no_network_disk_or_subprocess(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("I/O attempted")
    monkeypatch.setattr(socket, "socket", boom)
    monkeypatch.setattr(socket, "create_connection", boom)
    monkeypatch.setattr(builtins, "open", boom)
    monkeypatch.setattr(subprocess, "Popen", boom)
    for args in ({"doc_id": "d", "visibility": "public"}, {"doc_id": "d", "visibility": "bad"}, {}):
        run_tool("share_doc", args, {}, ALLOWED)
