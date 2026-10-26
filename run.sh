#!/usr/bin/env bash
# Headless wrapper for one research cycle or a digest.
# Usage: ./run.sh <legal|technical|market|red-team|outreach|digest>
# Uses your Claude subscription login. Never add --bare (it ignores subscription login).
set -euo pipefail

usage() {
  echo "Usage: $0 <legal|technical|market|red-team|outreach|digest>" >&2
  exit 1
}

[ $# -eq 1 ] || usage
case "$1" in
  legal|technical|market|red-team|outreach) PROMPT="/cycle $1" ;;
  digest) PROMPT="/digest" ;;
  *) usage ;;
esac

# Subscription mode: drop any API key unless explicitly requested.
if [ "${USE_API_KEY:-}" != "1" ]; then
  unset ANTHROPIC_API_KEY
fi

cd "$(dirname "$0")"
mkdir -p logs
LOG="logs/$(date +%F)-$1.log"
echo "=== $(date '+%F %T') run.sh $1 ===" >> "$LOG"

claude -p "$PROMPT" \
  --model sonnet \
  --permission-mode acceptEdits \
  --allowedTools "Read,Write,Glob,Grep,WebSearch,WebFetch,Agent" \
  --max-turns 30 \
  --max-budget-usd 2 \
  2>&1 | tee -a "$LOG"
