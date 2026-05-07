---
name: Memory cleanup is interactive — ask before forgetting
description: Before deleting or archiving stale memory entries, always ask the user "still relevant or forget?". Never auto-forget.
type: feedback
---

Memory cleanup is **interactive**, not automatic.

**Why:** Memory grows under the tick protocol (lower importance
threshold = more files). But auto-dedup or auto-archive risks deleting
context that is still mentally active for the user even if not
recently written. They should have agency over what gets forgotten.

**How to apply:**
- When running any memory cleanup (manual, command, or AI-suggested),
  identify candidate stale entries: files not updated in > N days,
  topics not referenced in recent conversations.
- **Before any delete/archive action**, present the list to the user
  with the framing: "we haven't discussed these topics in a while —
  still interesting, or forget?"
- Group by topic when possible — don't dump 40 individual questions.
- Three outcomes per entry:
  - **keep** — user still cares; leave as-is
  - **archive** — move to `~/.sae4u-memory/archive/` for historical reference
  - **delete** — truly gone
- Never auto-delete, never auto-archive. Always ask first.
- Cleanup is also a good moment to offer dedup: "these two files
  overlap, merge?"
