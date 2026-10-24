"""Load a patch file. Format (app/patches/<name>.md): markdown with `## Pattern`,
`## Patch` and `## Target levels` sections. Only the body of `## Patch` is the patch text."""
import hashlib
import re
from pathlib import Path

APP = Path(__file__).resolve().parent.parent
HEADER = "### Safety patch"   # marker line placed before the patch text in the system prompt


def load_patch(arg):
    p = Path(arg)
    if not p.exists():
        for cand in (APP / arg, APP / "patches" / arg, APP / "patches" / f"{arg}.md"):
            if cand.exists():
                p = cand
                break
        else:
            raise SystemExit(f"patch not found: {arg}")
    md = p.read_text()
    m = re.search(r"^##\s+Patch\s*$(.*?)(?=^##\s|\Z)", md, re.M | re.S)
    if not m or not m.group(1).strip():
        raise SystemExit(f"{p}: no '## Patch' section with text")
    text = m.group(1).strip()
    targets = re.findall(r"^\s*-\s*(\S+)", (re.search(r"^##\s+Target levels\s*$(.*?)(?=^##\s|\Z)", md, re.M | re.S) or [None, ""])[1] if re.search(r"^##\s+Target levels", md, re.M) else "", re.M)
    return {"name": p.stem, "file": str(p.resolve().relative_to(APP.parent)) if p.resolve().is_relative_to(APP.parent) else str(p),
            "sha256": hashlib.sha256(text.encode()).hexdigest(), "text": text, "target_levels": targets}


def build_system(level_system, safety_suffix=None, patch=None):
    """Order: level system prompt, then +safety suffix, then patch."""
    parts = [(level_system or "").rstrip()]
    if safety_suffix:
        parts.append(safety_suffix.rstrip())
    if patch:
        parts.append(f"{HEADER} ({patch['name']})\n{patch['text']}")
    return "\n\n".join(parts)
