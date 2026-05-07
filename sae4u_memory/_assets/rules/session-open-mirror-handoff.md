---
name: Session-open — mirror the handoff card first, suggestions after
description: At session open, mirror the previous handoff card 1:1 (all items, same order, same accents) BEFORE any reinterpretation, additions, or recommendations. New material goes in a separate marked section.
type: feedback
critical: true
---

When opening a new session via a context-transfer note (or the final
assistant message of the prior session), **first** output the handoff
card from the previous session **verbatim**: same items, same order,
same emphasis, same closing line. **Then** layer your own suggestions
in a clearly-marked section.

**Why:** The handoff card is the closing artifact of the previous
session — it represents the state the user left for themselves.
Remixing it on reopen rewrites their own decision baseline before
they get to act on it. That's the same class of error as
session-state confabulation, one layer higher: the AI silently
edits the user's plan instead of resuming it.

Even subtle changes — dropping older items, reordering by importance,
adding a fork option drawn from an open question — break continuity.
The user has to mentally diff what they see vs what they wrote, before
they can get going.

**How to apply:**

1. **Step 1 — Mirror.** Reproduce the handoff card from the
   previous session's context-transfer (or final message) exactly.
   - Same items, same order, same emphasis, same closing line.
   - Don't drop items even if they look stale.
   - Don't reorder by your own sense of priority.
   - Don't expand single bullets into structured sections.

2. **Step 2 — Visual break.** Use `---` or a heading like `## My take`
   to separate the mirror from your own additions.

3. **Step 3 — Add your layer.** Suggestions, forks, "what if we
   tried X" go here. Mark explicitly as additions.

4. Open questions from the transfer (e.g. "When should we ship X?")
   stay as open questions in your mirror — never promote them to
   decided options inside Step 1.

5. If you want to flag something as outdated or worth reordering,
   do it in Step 3 as a proposal: "FYI item N feels stale — keep,
   archive, or update?"
