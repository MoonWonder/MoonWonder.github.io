#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="content/posts"
timestamp="$(TZ=Asia/Shanghai date +"%Y-%m-%dT%H:%M:%S%:z")"

# export LASTMOD_TIMESTAMP="$timestamp"

find "$BASE_DIR" -type f -name "*.md" | while IFS= read -r file; do
  timestamp=""
  if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    timestamp="$(git log -1 --format=%cI -- "$file" 2>/dev/null || true)"
  fi
  if [[ -z "$timestamp" ]]; then
    timestamp="$(date -r "$file" +"%Y-%m-%dT%H:%M:%S%:z")"
  fi

  LASTMOD_TIMESTAMP="$timestamp" python3 - "$file" <<'PY'
import os
import sys

path = sys.argv[1]
timestamp = os.environ["LASTMOD_TIMESTAMP"]

with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

if not lines:
    sys.exit(0)

first_line = lines[0].strip()
if first_line not in ("---", "+++"):
    sys.exit(0)

delimiter = first_line
fm_end = None
for idx in range(1, len(lines)):
    if lines[idx].strip() == delimiter:
        fm_end = idx
        break

if fm_end is None:
    sys.exit(0)

has_lastmod = False
is_index = path.endswith("_index.md")

for idx in range(1, fm_end):
    stripped = lines[idx].lstrip()
    if stripped.startswith("lastmod:"):
        lines[idx] = f"lastmod: {timestamp}\n"
        has_lastmod = True
    elif is_index and stripped.startswith("date:"):
        indent = lines[idx][:len(lines[idx]) - len(stripped)]
        lines[idx] = f"{indent}lastmod: {timestamp}\n"
        has_lastmod = True

if not has_lastmod:
    lines.insert(fm_end, f"lastmod: {timestamp}\n")
    fm_end += 1

with open(path, "w", encoding="utf-8") as f:
    f.writelines(lines)
PY
done