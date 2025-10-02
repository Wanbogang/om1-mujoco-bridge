#!/usr/bin/env bash
set -euo pipefail
source .venv/bin/activate

python -m om1_bridge.bridge &
BRIDGE_PID=$!

cleanup() {
  kill "$BRIDGE_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

python -m om1_bridge.adapter
