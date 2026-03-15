#!/bin/bash
# Radar scanner cron job
# Runs at minute 0 of every hour

LOG_DIR="/home/bilal/.openclaw/workspace/logs"
mkdir -p "$LOG_DIR"

export PATH="/home/bilal/.local/bin:/usr/local/bin:/usr/bin:$PATH"

cd /home/bilal/Documents/radar
source .venv/bin/activate

python -m radar.scanner --db radar.db >> "$LOG_DIR/scanner.log" 2>&1

echo "[$(date -Iseconds)] Scanner completed" >> "$LOG_DIR/scanner.log"