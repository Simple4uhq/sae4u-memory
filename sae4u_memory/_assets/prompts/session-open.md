# Session-open prompt

Use this at the start of a working session to restore episodic context without confabulating.

```
Open the session.

1. Pull current project state from real artifacts — not from memory:
   - `git log --oneline -30` on whatever repo we're working on
   - `ls -lat` on the working directory(ies) we touched yesterday
   - any backlog/issue tracker URL or local file (e.g. BACKLOG.md, TODO.md)

2. If there's a previous-session backup or context-transfer note (e.g.
   `previous_session_backup/context_transfer_YYYY-MM-DD.md`), read it.
   Episodic memory restored without confabulation.

3. Mirror the prior session's handoff card 1:1 first — same items,
   same order, same accents, same closing line. Don't drop items even
   if they look stale; don't reorder; don't add suggestions inside the
   mirror.

4. THEN, in a separate clearly-marked block ("## My take" or similar),
   add your own suggestions, forks, and proposals. Mark explicitly as
   additions.

5. Open questions from the transfer ("Should we do X?") stay as open
   questions — never promote them to decided options inside the mirror.

Show me: what changed since last session, P0 items, what we do today.
```

## Why this shape

Without artifacts, "yesterday's work" is the most confabulation-prone class
of question — see `rules/no-session-state-confabulation.md`.

Without a 1:1 mirror, suggestions silently rewrite yesterday's decisions —
see `rules/session-open-mirror-handoff.md`.

## Optional: remote dev box

If you keep episodic state on a remote machine (a "session opener" pattern —
running scripts that emit a digest, with backups under
`previous_session_backup/`), drop your specific commands in step 1 and 2.
The defaults above assume a local-only setup.
