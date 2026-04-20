#!/usr/bin/env bash
# alert.sh — Alert Dispatcher
# Receives alert level, metric, and value from monitor.py (or CLI)
# Logs to file and simulates sending to Slack/PagerDuty
#
# Usage:
#   ./alert.sh <LEVEL> <METRIC> <VALUE> <THRESHOLD>
#   ./alert.sh WARNING CPU 82.3 75
#
# TODO: Add real Slack webhook integration (use $SLACK_WEBHOOK_URL from .env)
# TODO: Add PagerDuty integration for CRITICAL alerts only
# TODO: Add alert deduplication (don't spam same alert within 5 minutes)

set -euo pipefail

# --- Config ---
LOG_DIR="logs"
ALERT_LOG="${LOG_DIR}/alerts.log"
RUNBOOK_URL="https://github.com/yourorg/devops-incident-dashboard/blob/main/docs/runbook.md"

# --- Ensure log directory exists ---
mkdir -p "$LOG_DIR"

# --- Input validation ---
if [[ $# -lt 4 ]]; then
    echo "Usage: $0 <LEVEL> <METRIC> <VALUE> <THRESHOLD>"
    echo "Example: $0 CRITICAL CPU 92.5 90"
    exit 1
fi

LEVEL="$1"
METRIC="$2"
VALUE="$3"
THRESHOLD="$4"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
HOSTNAME=$(hostname)

# --- Validate alert level ---
if [[ "$LEVEL" != "WARNING" && "$LEVEL" != "CRITICAL" ]]; then
    echo "ERROR: LEVEL must be WARNING or CRITICAL. Got: $LEVEL"
    exit 1
fi

# --- Build alert message ---
MESSAGE="[${TIMESTAMP}] [${LEVEL}] HOST=${HOSTNAME} METRIC=${METRIC} VALUE=${VALUE}% THRESHOLD=${THRESHOLD}%"

# --- Log to file ---
echo "$MESSAGE" >> "$ALERT_LOG"
echo "[alert.sh] Logged: $MESSAGE"

# --- Simulate Slack notification ---
# TODO: Replace this echo with a real curl to $SLACK_WEBHOOK_URL
echo "[alert.sh] Simulating Slack notification..."
echo "  → Would send to #ops-alerts: ${LEVEL} | ${METRIC} = ${VALUE}% (threshold: ${THRESHOLD}%)"
echo "  → Runbook: ${RUNBOOK_URL}"

# --- Simulate PagerDuty escalation for CRITICAL alerts ---
if [[ "$LEVEL" == "CRITICAL" ]]; then
    echo "[alert.sh] Simulating PagerDuty escalation..."
    # TODO: Replace with real PagerDuty Events API v2 call
    echo "  → Would trigger PagerDuty incident for: ${METRIC} CRITICAL"
fi

echo "[alert.sh] Done. Alert logged to ${ALERT_LOG}
exit 0
