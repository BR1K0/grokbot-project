"""Fake tools: read only from the level's environment, write only to the log."""
import json

SCHEMAS = {
    "fetch_page": ("Fetch a web page by URL.", {"url": {"type": "string"}}, ["url"]),
    "read_inbox": ("Read the user's inbox.", {}, []),
    "read_file": ("Read a file by name.", {"name": {"type": "string"}}, ["name"]),
    "list_files": ("List files in the project folder.", {}, []),
    "read_secret": ("Read a secret from the secrets store.", {"name": {"type": "string"}}, ["name"]),
    "send_email": ("Send an email.", {"to": {"type": "string"}, "subject": {"type": "string"},
                   "body": {"type": "string"}}, ["to", "body"]),
    "delete_file": ("Delete a file.", {"name": {"type": "string"}}, ["name"]),
    "transfer_money": ("Transfer money.", {"to_account": {"type": "string"},
                       "amount": {"type": "number"}}, ["to_account", "amount"]),
    "save_draft": ("Save an email draft.", {"to": {"type": "string"}, "subject": {"type": "string"},
                   "body": {"type": "string"}}, ["to", "body"]),
    "check_balance": ("Check the account balance.", {}, []),
}


def tool_specs(names):
    specs = []
    for n in names:
        desc, props, req = SCHEMAS.get(n, (f"Tool {n}.", {}, []))
        specs.append({"type": "function", "function": {
            "name": n, "description": desc,
            "parameters": {"type": "object", "properties": props, "required": req}}})
    return specs


def run_tool(name, args, env, allowed):
    """Return the canned result string. Never touches the network or disk."""
    env = env or {}
    if name not in allowed:
        return f"error: unknown tool {name}"
    overrides = env.get("tool_overrides") or {}
    if name in overrides:
        return str(overrides[name])
    files = env.get("files") or {}
    if name == "fetch_page":
        page = (env.get("pages") or {}).get(args.get("url", ""))
        return page if page is not None else "404 Not Found"
    if name == "read_inbox":
        return json.dumps(env.get("inbox") or [])
    if name == "list_files":
        return json.dumps(sorted(files))
    if name == "read_file":
        return files.get(args.get("name", ""), "error: file not found")
    if name == "read_secret":
        return str((env.get("secrets") or {}).get(args.get("name", ""), "error: no such secret"))
    if name in ("send_email", "delete_file", "transfer_money", "save_draft"):
        return "ok"
    return "ok"
