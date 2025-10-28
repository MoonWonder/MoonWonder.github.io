#!/usr/bin/env bash
set -euo pipefail

# Generate a daily life diary entry following the post-migration structure.
# Usage: ./life.sh [YYYY-MM-DD]
# If no date is provided the current local date is used.

if [[ $# -ge 1 ]]; then
  TARGET_DATE="$1"
else
  TARGET_DATE="$(date +%Y-%m-%d)"
fi

if ! date -d "$TARGET_DATE" >/dev/null 2>&1; then
  echo "❌ Invalid date: $TARGET_DATE" >&2
  exit 1
fi

YEAR="${TARGET_DATE:0:4}"
BUNDLE_DIR="content/life/${YEAR}/${TARGET_DATE}"
FILE_PATH="${BUNDLE_DIR}/index.md"

echo "📅 Generating diary for ${TARGET_DATE}"

if [[ -e "$FILE_PATH" ]]; then
  echo "⚠️  ${FILE_PATH} already exists."
  read -rp "Overwrite? (y/N): " CONFIRM
  if [[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]]; then
    echo "Aborted."
    exit 0
  fi
fi

mkdir -p "$BUNDLE_DIR"

if hugo new "${FILE_PATH}" --kind=life > /dev/null; then
  echo "✅ Created ${FILE_PATH}"
else
  echo "❌ Failed to create ${FILE_PATH}" >&2
  exit 1
fi

read -rp "Open the file now? (y/N): " OPEN
if [[ "$OPEN" == "y" || "$OPEN" == "Y" ]]; then
  if command -v code >/dev/null 2>&1; then
    code "$FILE_PATH"
  elif command -v vim >/dev/null 2>&1; then
    vim "$FILE_PATH"
  elif command -v nano >/dev/null 2>&1; then
    nano "$FILE_PATH"
  else
    echo "Open ${FILE_PATH} in your preferred editor." >&2
  fi
fi
