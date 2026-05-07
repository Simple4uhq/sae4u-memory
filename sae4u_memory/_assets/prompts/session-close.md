# Session-close prompt

Use this at the end of a working session to capture everything before context evaporates.

```
Close the session.

0. Describe in detail what we did, where we stopped, and what we
   decided to start with next session.

1. Update any backlog/tracker:
   - close items we shipped (with a one-line note explaining what landed)
   - re-prioritize remaining items if anything shifted
   - add any new items uncovered today

2. Write today's context-transfer note covering:
   - Done — what we shipped (with commits/PRs/files)
   - Decided — non-obvious decisions and their reasons
   - Issues — blockers, known broken things, tech debt added today
   - Todo — what's next, in the same shape we'd want to read it back

3. If something foundational changed (architecture, strategy, naming,
   identity) — update permanent memory and the MEMORY.md index. If a
   prior permanent memory was superseded, mark the old one or remove
   from the index.

4. Show the summary: what's done, what's left, P0 for next session.

5. Make a backup of today's context-transfer somewhere durable
   (e.g. `previous_session_backup/context_transfer_YYYY-MM-DD.md`)
   so the next session can read it without losing context.
```

## Optional: end-of-session journal

Call `journal(text)` with a short narrative of the session. The journal
is human-readable Markdown under `~/.sae4u-memory/journals/YYYY-MM-DD.md`,
useful for retrospectives. It does not replace the context-transfer file —
the context-transfer is for the next session, the journal is for you.
