#!/bin/bash
# memory-tick.sh — Claude Code UserPromptSubmit hook for sae4u-memory.
#
# Fires on every user prompt. If >= INTERVAL_SECONDS have elapsed since the
# last tick, injects a system-reminder instructing the AI to silently review
# the last ~10 minutes of conversation, classify any new facts/decisions/
# preferences into 4 types, and append to the day's tick log (or, only when
# explicitly foundational, write directly to permanent memory).
#
# This implements the "tick protocol": memory writes happen on a regular
# rhythm, not only reactively, with a lower importance threshold at tick
# time so borderline items get captured for later distillation.
#
# Always exits 0 so it never blocks user prompts.

set +e

# === CONFIG ============================================================

# Time between forced memory reviews (seconds).
INTERVAL_SECONDS=600

# Where ~/.sae4u-memory lives. Override with SAE4U_MEMORY_HOME env var.
MEMORY_DIR="${SAE4U_MEMORY_HOME:-$HOME/.sae4u-memory}"

# Where the timestamp file lives.
TICK_FILE="${MEMORY_DIR}/.last_tick"

# === LOGIC =============================================================

mkdir -p "$MEMORY_DIR" 2>/dev/null
mkdir -p "${MEMORY_DIR}/tick" 2>/dev/null

if [[ -f "$TICK_FILE" ]]; then
    LAST_TICK=$(cat "$TICK_FILE" 2>/dev/null || echo 0)
else
    LAST_TICK=0
fi

if ! [[ "$LAST_TICK" =~ ^[0-9]+$ ]]; then
    LAST_TICK=0
fi

NOW=$(date +%s)
ELAPSED=$((NOW - LAST_TICK))

if (( ELAPSED < INTERVAL_SECONDS )); then
    exit 0
fi

MINUTES=$((ELAPSED / 60))
TODAY=$(date +%Y-%m-%d)

cat <<JSON
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "MEMORY TICK — ${MINUTES} min since last tick.\n\nBEFORE answering the user, do this silently:\n\n1. Review the last ~10 min of conversation.\n2. For each new fact/decision/preference, classify by 4 types (user/feedback/project/reference).\n3. DEFAULT destination: append to tick log ${MEMORY_DIR}/tick/${TODAY}.md. Use format:\n   ## HH:MM — [type] short title\n   Body.\n   If file doesn't exist, create with a single-line header: # Tick log ${TODAY}\n4. EXCEPTION — write DIRECTLY to permanent memory (and update MEMORY.md index) ONLY when:\n   - The user explicitly said it's important / 'remember this for the long term' / 'in soul'\n   - It's a foundational decision (architecture, strategy, naming, core identity)\n   - It corrects/overrides an existing permanent memory file\n   When writing to a permanent file, add 'critical: true' to frontmatter if it's foundational.\n5. LOWER importance threshold in tick log — record borderline items there. The /memory-distill command will sort through them later.\n6. If nothing meaningful emerged, just update the timestamp.\n7. ALWAYS end the tick with: echo \$(date +%s) > ${MEMORY_DIR}/.last_tick\n\nTick log does NOT get indexed in MEMORY.md. Do NOT mention the tick to the user unless asked. Stay silent, then answer the user's prompt."
  }
}
JSON

exit 0
