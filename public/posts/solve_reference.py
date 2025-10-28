#!/usr/bin/env python3
"""Regenerate config.json entries for post aliases and references.

The FixIt theme uses a small JSON manifest (config.json) to keep track of
aliases and custom ``@import"..."`` references inside Markdown documents.  This
script scans the ``content/posts`` tree, collects the relevant metadata, and
writes the refreshed manifest.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List

try:  # pragma: no cover - tooling guard
    import yaml
except ImportError as exc:  # pragma: no cover - tooling guard
    raise SystemExit("PyYAML is required to parse front matter") from exc

CONTENT_ROOT = Path(__file__).resolve().parent
CONFIG_PATH = CONTENT_ROOT / "config.json"
IMPORT_PATTERN = re.compile(r"@import\s+\"([^\"]+)\"")


def split_front_matter(text: str) -> Dict:
    if not text.lstrip().startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    data = yaml.safe_load(parts[1]) or {}
    if not isinstance(data, dict):
        return {}
    return data


def relative_key(path: Path) -> str:
    rel = path.relative_to(CONTENT_ROOT)
    return f"./{rel.as_posix()}"


def collect_metadata() -> Dict[str, Dict[str, List[str]]]:
    manifest: Dict[str, Dict[str, List[str]]] = {"alias": {}, "refrence": {}}

    for path in sorted(CONTENT_ROOT.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        front_matter = split_front_matter(text)
        key = relative_key(path)

        aliases = front_matter.get("alias")
        if isinstance(aliases, str):
            manifest["alias"][key] = [aliases]
        elif isinstance(aliases, list) and aliases:
            manifest["alias"][key] = [str(item) for item in aliases]

        references = set(IMPORT_PATTERN.findall(text))
        if references:
            manifest["refrence"][key] = sorted(references)

    return manifest


def main() -> int:
    manifest = collect_metadata()
    CONFIG_PATH.write_text(
        json.dumps(manifest, indent=4, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
