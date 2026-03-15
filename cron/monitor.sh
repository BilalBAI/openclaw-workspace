#!/bin/bash
# Radar monitor cron job
# Runs at minute 5 of every hour

LOG_DIR="/home/bilal/.openclaw/workspace/logs"
mkdir -p "$LOG_DIR"

export PATH="/home/bilal/.local/bin:/usr/local/bin:/usr/bin:$PATH"

cd /home/bilal/Documents/radar
source .venv/bin/activate

python run_monitor.py --db radar.db >> "$LOG_DIR/monitor.log" 2>&1

echo "[$(date -Iseconds)] Monitor completed" >> "$LOG_DIR/monitor.log"