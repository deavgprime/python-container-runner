#!/bin/sh
set -eu
APP_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$APP_DIR"
entry_point=${PYTHON_ENTRYPOINT:-src/main.py}
if [ ! -f "$entry_point" ]; then
  printf 'Python entry point not found: %s\n' "$entry_point" >&2
  exit 1
fi
exec python "$entry_point"
