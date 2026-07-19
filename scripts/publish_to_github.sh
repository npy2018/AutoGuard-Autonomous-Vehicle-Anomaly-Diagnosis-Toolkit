#!/usr/bin/env bash
set -euo pipefail

REMOTE_URL="${1:-}"
if [[ -z "$REMOTE_URL" ]]; then
  echo "Usage: $0 https://github.com/<user>/<repo>.git" >&2
  exit 1
fi

if [[ ! -d .git ]]; then
  git init
fi

git branch -M main
git add .
if ! git diff --cached --quiet; then
  git commit -m "Initial AutoGuard AI MVP"
fi

if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "$REMOTE_URL"
else
  git remote add origin "$REMOTE_URL"
fi

git push -u origin main
