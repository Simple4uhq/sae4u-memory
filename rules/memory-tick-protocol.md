---
name: Memory tick protocol — 10-min forced review
description: A UserPromptSubmit hook fires every 10 minutes and forces a brief memory review. Lower importance threshold at tick time. Update .last_tick after each tick.
type: feedback
---

Memory writes happen on a **regular rhythm**, not only reactively.

**Why:** Reactive-only writing creates memory gaps — the AI may judge
something unimportant that later turns out to matter. The tick gives
you a forced moment to catch borderline observations.

**How it works:**
- A `UserPromptSubmit` hook (`hooks/memory-tick.sh` in this repo)
  runs on every user message.
- If >= 10 minutes have elapsed since the last tick (timestamp in
  `~/.sae4u-memory/.last_tick`), the hook injects a system-reminder
  via `hookSpecificOutput.additionalContext`.
- On receiving the tick reminder, the AI silently:
  1. Reviews the last ~10 min of conversation.
  2. Classifies new facts/decisions/preferences into 4 types
     (user / feedback / project / reference).
  3. Appends to the day's tick log
     (`~/.sae4u-memory/tick/YYYY-MM-DD.md`), or — only for
     foundational items — writes directly to permanent memory.
  4. Updates `~/.sae4u-memory/.last_tick` with the current epoch.
- The tick is NEVER mentioned to the user unless they ask.

**How to apply:**
- **Lower the importance threshold at tick time** — record borderline
  items too. Dedupe via `/memory-distill` later.
- If nothing meaningful emerged in the 10-min window, skip writes but
  still update the timestamp.
- The tick is a forced **review**, not a forced **write** — empty ticks
  are valid.
- Never write a "session log" — always classify into the 4 existing
  types. Session-state belongs in context-transfer notes (see the
  session-close prompt), not in tick logs or permanent memory.
