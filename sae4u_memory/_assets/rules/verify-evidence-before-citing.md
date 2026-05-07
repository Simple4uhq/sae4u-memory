---
name: Verify evidence before citing as support
description: Before citing "X has N lines of Y" or any specific authoritative claim — actually read/grep to confirm. Specificity without verification creates false confidence more dangerous than vague claims.
type: feedback
---

Before citing specific evidence — line counts, file sizes, "N lines
of Y", function names, flag names — **verify the content actually
matches the claim**.

**Why:** Specificity sounds like you checked even when you didn't.
That false authority is more dangerous than vague hand-waving — the
user will reasonably trust a precise number, then build decisions on
top of it.

A common trap: inferring content from filename + size. "FILE.md has
467 lines" + "name implies it's about X" ≠ "FILE.md has 467 lines of
X". It could be 467 lines of architecture spec, roadmap notes, or
unrelated writing under that filename.

**How to apply:**

- Treat every authoritative-sounding claim as a hypothesis to check,
  not a proven fact, until you've grepped or read.
- Before asserting "doc X has N lines of Y" — actually grep/read
  to confirm Y is what's in there.
- Specificity + unverified = MORE dangerous than vague.
- Especially careful when building a recommendation on the claim:
  if you're about to argue "use approach A because file F supports it",
  verify F's content supports A before using it as evidence.
- If the verification is annoying, ask the user to confirm rather
  than guess.
