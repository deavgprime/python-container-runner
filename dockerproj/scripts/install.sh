#!/bin/sh
set -eu
APP_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$APP_DIR"
if [ -f requirements.txt ]; then
  python -m pip install --no-cache-dir -r requirements.txt
elif [ -f pyproject.toml ] && [ -f poetry.lock ]; then
  command -v poetry >/dev/null 2>&1 || { echo 'Poetry is required for this project.' >&2; exit 1; }
  poetry config virtualenvs.create false
  poetry install --only main --no-root --no-interaction
else
  echo 'Provide pinned requirements.txt or pyproject.toml with poetry.lock.' >&2
  exit 1
fi
