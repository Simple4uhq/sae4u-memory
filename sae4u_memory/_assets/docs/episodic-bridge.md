# Optional: episodic bridge for remote dev boxes

If your work spans more than one machine — e.g. you have a remote
build server, a production droplet, or a dedicated dev box —
`sae4u-memory` semantic memory (markdown + SQLite) only knows what
you told it from your local machine. Episodic state on the remote
box (last cron run, last deploy, last service health check, last
backlog edit) is invisible to it.

This doc describes a pattern for bridging that gap **without**
sending PII or session state through the AI's semantic memory.

## The pattern

On the remote machine, maintain three things:

1. **A backlog file** — single source of truth for open work,
   updated by you (or your tooling) as items move.
2. **A session-open script** — emits a digest: services running,
   memory/disk state, last activity timestamps, top P0 items.
3. **A previous-session-backup directory** — at the end of each
   session, your session-close prompt drops a context-transfer
   note in there, dated.

At session open, run the script and `cat` the backup. Feed the
output to the AI. Now the AI has actual artifacts (not vibes) to
ground "what changed since last time" answers.

## Suggested layout (on the remote box)

```
/path/to/your/state/
├── BACKLOG.md
├── scripts/
│   └── session_open.sh         # emits the digest
├── previous_session_backup/
│   └── context_transfer_2026-05-07.md
└── session-log.md              # optional: chronological log
```

## Suggested session-open script (template)

```bash
#!/usr/bin/env bash
# session_open.sh — emits session digest for the AI to ingest at start.
set -e

cat <<HEADER
=================================================================
SESSION OPEN — $(date '+%Y-%m-%d %H:%M %Z')
=================================================================

SERVICES
HEADER

# Replace with your actual checks
systemctl status myapp | head -3 || true

cat <<DIVIDER

SYSTEM
  Memory: $(free -h | awk '/^Mem:/ {print $3 "/" $2}')
  Disk:   $(df -h / | awk 'NR==2 {print $5 " (" $3 "/" $2 ")"}')

LAST SESSION
DIVIDER

ls -1t previous_session_backup/context_transfer_*.md 2>/dev/null \
    | head -1 | xargs -I {} head -10 {}

echo
echo "P0 BACKLOG"
grep -E '^\s*-\s*\[ \].*\*\*BL-' BACKLOG.md 2>/dev/null | head -5

cat <<FOOTER

=================================================================
Ready.
=================================================================
FOOTER
```

## At session open

In Claude Code, your session-open prompt invokes the script:

```
ssh <remote-host> '/path/to/your/state/scripts/session_open.sh'
ssh <remote-host> 'cat /path/to/your/state/BACKLOG.md'

Read the latest context_transfer in previous_session_backup/.

Then mirror the prior handoff card 1:1 (per
rules/session-open-mirror-handoff.md), then add your suggestions
in a separate marked block.
```

## At session close

Drop a context-transfer note for next time:

```
ssh <remote-host> 'cp /path/to/your/state/context_transfer_$(date +%F).md \
    /path/to/your/state/previous_session_backup/'
```

## What to keep in semantic memory vs episodic bridge

- **Semantic memory** (markdown + SQLite): identity, decisions,
  rules, project facts, preferences. Stable across sessions.
- **Episodic bridge** (remote artifacts): session state, current
  service health, last touched file, today's commits, this week's
  backlog churn. Volatile, refreshed per session.

Don't let episodic state leak into semantic memory. If it's
"yesterday I deployed X", that goes in a context-transfer note,
not in MEMORY.md. Permanent memory is for things that will still
be true in three weeks.
