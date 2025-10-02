#!/usr/bin/env bash
set -euo pipefail
SESSION="om1-mujoco"
tmux new-session -d -s "$SESSION" './run_bridge.sh'
tmux split-window -h 'python scripts/demo_client.py; read -p "Enter untuk keluar..."'
tmux select-pane -L
tmux attach -t "$SESSION"
