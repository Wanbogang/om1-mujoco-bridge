#!/usr/bin/env bash
set -euo pipefail
export OM1_BRIDGE_HOST="${OM1_BRIDGE_HOST:-0.0.0.0}"
export OM1_BRIDGE_PORT="${OM1_BRIDGE_PORT:-8765}"
export OM1_MODEL="${OM1_MODEL:-assets/simple_arm.xml}"
python -m om1_bridge.bridge
