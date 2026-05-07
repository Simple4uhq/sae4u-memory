---
name: No session-state confabulation
description: When the user asks about "recent changes", "yesterday's work", "what's new" — never answer from semantic memory. Check real artifacts (git, files, backlog) first. Admission > confabulation.
type: feedback
critical: true
---

When the user asks about recent / latest / yesterday's work — **never**
answer from semantic memory. Semantic memory holds identity and
decisions, not events. Use it for "who", "why", "how" — never for
"what happened".

**Examples that trigger this rule:**
- "What did we change yesterday?"
- "What's your take on the recent work?"
- "How did the last session go?"
- "Look at what I did since you saw it last."

**Why:** Confabulation about session state is one of the worst AI
failure modes — it sounds authoritative, has zero ground truth, and
poisons trust. Plausible-sounding BS from general project context
will fool you AND the user.

**How to apply.** Before commenting on recent / latest / yesterday
work, verify:

1. `git log --oneline -30` on any active repo.
2. `ls -lat` on relevant directories — what files were touched and
   when.
3. Any project tracker — backlog, issue queue, kanban, calendar.
4. If a previous-session context-transfer or backup exists, read it.

**If none of those return actionable context, state explicitly:**

> I only have semantic memory — what we did yesterday isn't loaded.
> I checked X, Y, Z — empty. Tell me, or let's walk through the
> artifacts together.

NEVER fill the gap with vibes. Admission > confabulation.

Related rules:
- `verify-evidence-before-citing.md` — don't cite specifics without
  reading them
- `grep-before-asking.md` — search first, then ask
- `session-open-mirror-handoff.md` — at session open, mirror the
  prior handoff card before adding interpretation
