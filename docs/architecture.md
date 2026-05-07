# Architecture

`sae4u-memory` is built around five concepts:

1. **Two-corpus recall** — semantic-ish search over SQLite facts
   (written via `remember`) AND markdown files in your auto-memory
   dirs and `~/.sae4u-memory/`.
2. **MEMORY.md as the index** — a single table of contents pointing
   to per-topic files. Loaded into context at session start.
3. **4-type classification** — every memory is one of `user`,
   `feedback`, `project`, or `reference`. Each type has different
   handling and shelf life.
4. **Tick / permanent split** — borderline observations go to a
   day-rolling tick log (NOT indexed in MEMORY.md). Foundational
   items go directly to permanent files indexed in MEMORY.md.
5. **Persona at session start** — `get_persona()` returns a
   working-rules document plus user context, loaded fresh.

## File layout

```
~/.sae4u-memory/
├── memory.db               # SQLite facts written via remember()
├── persona.md              # AI's identity + rules (edit to customize)
├── MEMORY.md               # Index of permanent files (loaded at session start)
├── user/                   # User context loaded by get_persona()
│   ├── identity.md
│   ├── projects.md
│   └── preferences.md
├── tick/                   # Day-rolling tick log
│   └── 2026-05-07.md
├── archive/                # User-confirmed archived files (optional)
├── journals/               # End-of-session narratives
│   └── 2026-05-07.md
└── .last_tick              # Epoch timestamp of last memory tick
```

In Claude Code, the additional auto-memory dir lives at
`~/.claude/projects/<project-slug>/memory/` — `recall()` searches
that too, by default.

## The 4 types

### `user`
Facts about who the user is — role, goals, knowledge, responsibilities,
preferences. Helps tailor future behavior. Does NOT decay quickly.

> Example: "Senior backend engineer, 10 years Go, new to React.
> Prefers explanation in terms of backend analogues."

### `feedback`
Corrections AND validations. Every time the user pushes back ("don't
do X") OR confirms a non-obvious approach worked ("yes exactly,
keep doing that"). Lead with the rule, then **Why:** and
**How to apply:** lines.

> Example: see `rules/no-hardcode.md`

### `project`
Ongoing work, decisions, motivations, deadlines. **Decays fast** —
convert relative dates to absolute ones at write time
("Thursday" → "2026-03-05"). Re-evaluate periodically.

> Example: "Merge freeze begins 2026-03-05 for mobile release.
> Flag any non-critical PR scheduled after."

### `reference`
Pointers to external systems where information lives. Slack channels,
ticket queues, dashboards, documentation portals. Tells the AI where
to look — does not duplicate the content.

> Example: "Bugs tracked in Linear project INGEST. Check there for
> pipeline issues."

## What NOT to save

- Code patterns, conventions, file paths, project structure — these
  can be re-derived from reading the current state.
- Git history or recent changes — `git log` / `git blame` are
  authoritative.
- Debugging recipes — the fix is in the code; the commit message
  has the context.
- Anything already documented in CLAUDE.md.
- Ephemeral task state — that's what the conversation is for.

These exclusions apply even when the user explicitly asks. If they
ask for an "activity summary", ask what was *surprising* — that's
the part worth keeping.

## How recall works

`recall(query)` returns a merged stream from two sources:

1. **SQLite (FTS5):** facts written with `remember(text, category)`.
   Indexed by full-text search. Good for "recall what I told you about X".
2. **Markdown:** files under `~/.sae4u-memory/` and Claude Code
   auto-memory dirs. Ranked by weighted keyword scoring with a
   recency bonus for tick logs. Good for "what's the rule about Y"
   and "what did I write down recently".

Filter sources via `sources="sqlite"` or `sources="markdown"` if you
want only one corpus.

## Cleanup

Don't auto-forget. Use `/memory-distill` (see `commands/memory-distill.md`)
periodically. The user has agency over what gets archived or deleted.
