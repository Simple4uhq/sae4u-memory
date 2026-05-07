# Tick protocol

`hooks/memory-tick.sh` is a Claude Code `UserPromptSubmit` hook that
fires every 10 minutes (configurable). It does NOT write memory itself —
it injects a system reminder telling the AI to do a brief review.

## Why

Reactive-only memory writes leave gaps. The AI may judge something
unimportant in the moment that turns out to matter later. The tick
gives a forced moment to capture borderline observations before they
fall out of conversation context.

## What happens at a tick

1. The hook calculates how long since the last tick (stored in
   `~/.sae4u-memory/.last_tick`).
2. If the elapsed time is below the interval (default 600s), the
   hook exits silently — no extra context, no impact.
3. Otherwise, the hook returns a JSON `hookSpecificOutput` whose
   `additionalContext` field contains an instruction.
4. The AI receives that instruction along with the user's prompt
   and silently:
   - Reviews the last ~10 min of conversation
   - Classifies new facts/decisions/preferences into 4 types
   - Appends to the day's tick log
     (`~/.sae4u-memory/tick/YYYY-MM-DD.md`)
   - For foundational items (architecture, strategy, naming,
     identity, or items the user explicitly flagged), writes
     directly to permanent memory and updates MEMORY.md
   - Updates `~/.sae4u-memory/.last_tick`
5. THEN the AI answers the user normally. The tick is silent —
   the user doesn't see it.

## Tick log entry format

```markdown
## HH:MM — [type] short title

Body. One paragraph is enough. Pointer to permanent file if this
got promoted.
```

Tick log files are NOT indexed in MEMORY.md. They're sorted through
periodically by `/memory-distill` (see `commands/memory-distill.md`).

## When tick writes to permanent memory directly

Three cases:

1. **User explicit signal** — they said "remember this for the long
   term", "this is important", "in soul" or similar.
2. **Foundational decision** — architecture, strategy, naming, core
   identity, anything that changes how future work is framed.
3. **Supersedes existing permanent memory** — the new fact contradicts
   or refines an existing permanent file.

In all three cases, add `critical: true` to the frontmatter if the
item is foundational.

For everything else: tick log first, distill later.

## Tuning

Configure interval and home dir via environment:

```bash
# Override tick interval (seconds). Default 600.
# (Edit hooks/memory-tick.sh to change at hook level.)

# Override memory home. Default ~/.sae4u-memory.
export SAE4U_MEMORY_HOME=/path/to/your/memory
```

## Common gotchas

- **Empty ticks are valid.** If nothing meaningful emerged in the
  10-min window, the AI just updates the timestamp.
- **The tick is a review, not a write.** The instruction is to
  consider, classify, and write only if there's substance. Lower
  the importance threshold so borderline items get into the tick
  log — they get distilled later.
- **Don't write a "session log".** Always classify into the 4
  types. Session-state recap belongs in the context-transfer
  note (see `prompts/session-close.md`), not in tick logs.
- **Don't mention the tick to the user.** The protocol is silent.
