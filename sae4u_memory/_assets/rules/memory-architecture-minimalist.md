---
name: Memory architecture — minimalist until real bloat forces complexity
description: Keep memory architecture flat and minimal. Resist "fast/context/soul" tier proposals until MEMORY.md actually bloats. Use a critical flag in frontmatter for foundational items.
type: feedback
---

Keep memory architecture **minimalist** until real bloat forces complexity.

**Why:** A common temptation is to invent tiered memory systems
(fast / context / soul folders, keyword-routing layers, retrieval
indexes) before they pay for themselves. With ~20 files and a working
two-corpus recall, the marginal cost of a flat structure is near zero.
More categories = more misclassification, more tooling debt, slower
retrieval.

**Current minimalist design:**

1. **Tick writes go to `~/.sae4u-memory/tick/`** — raw append-only log,
   NOT indexed in MEMORY.md, does NOT load into session context.
   Keeps main memory clean.
2. **A weekly `/memory-distill` command** reads tick logs + current
   memory and proposes promotion candidates to the user. Remainder
   forgotten.
3. **"Critical" / "foundational" = `critical: true` flag** in
   frontmatter of existing files, NOT a separate folder. Note that
   most loaders don't sort by frontmatter fields — `critical: true`
   is currently a marker for the AI's internal understanding and
   cleanup protection (never auto-delete a critical file even if
   stale), not an actual priority-loading mechanism.
4. **Flat structure stays** — no fast/context/soul folders.
5. **Cleanup is interactive** — ask the user before forgetting
   (see `memory-cleanup-interactive.md`).

**Re-evaluation trigger:**
- After 1 month: if MEMORY.md index passes ~40 entries OR startup
  context noticeably bloats, reconsider tiering.
- Earlier if the user explicitly asks.

**What NOT to do:**
- Don't build keyword retrieval indexes — unreliable vs the existing
  FTS5 + markdown corpus.
- Don't create fast/context/soul folders proactively.
- Don't migrate existing files into a new structure on speculation.
