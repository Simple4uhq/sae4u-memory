# /memory-distill — weekly memory cleanup

A periodic ritual: read the rolling tick log, propose promotions to
permanent memory, and let the user confirm what to keep, archive,
or forget.

## When to run

- Weekly (e.g. Sunday evening or Monday morning).
- After heavy context-creation periods (a sprint close, a launch).
- When tick log files have piled up beyond what a quick scan can
  digest (~5+ days of unmerged ticks).

## What it does

1. **Read the tick logs** — all files under `~/.sae4u-memory/tick/`
   that haven't been distilled yet, plus any new permanent files
   added since last distill.
2. **Cluster** by topic (use the 4 types — user/feedback/project/
   reference — as a first cut, then group within type by topic).
3. **Propose actions** for each cluster. Three outcomes per item:
   - **Promote** to a permanent file (new or merge into existing).
     Update MEMORY.md.
   - **Drop** — was tick-only noise; not worth keeping.
   - **Keep in tick log** — borderline; see again next week.
4. **Surface for confirmation.** The user reviews the proposals
   and accepts / rejects each. Never auto-promote, never
   auto-forget — see `rules/memory-cleanup-interactive.md`.
5. **Apply** the confirmed actions:
   - Move tick entries to permanent files
   - Update MEMORY.md index
   - Archive distilled tick log file (e.g. rename to
     `tick/distilled/2026-05-07.md` or compress)
6. **Stale check** for permanent memory — entries not referenced
   in N weeks. Ask: "still interesting or forget?" Don't volunteer
   to delete; just surface the question.

## How the AI presents this

Group by topic, not by file. The user shouldn't have to read 40
individual proposals — bundle related ticks into "here are 5 things
about X, what shape do you want them in?"

Keep the proposals concrete:

> ### Topic: testing approach
>
> Across 4 ticks last week:
> - 2026-05-02 — "don't mock the database in integration tests"
> - 2026-05-04 — confirmed "TDD for new API endpoints"
> - 2026-05-05 — "use testcontainers for postgres in CI"
> - 2026-05-06 — "snapshot tests OK for component output"
>
> Propose: promote to `feedback_testing_approach.md` consolidating
> all four. Drop the per-tick entries from tick log.
>
> Accept / Reject?

## Implementation

This is a slash-command spec (Claude Code), not an automated job.
The AI reads it as guidance and runs through the steps interactively.

You can wire it into a routine:

```bash
# Weekly cron — reminds you to run distill in next session
0 18 * * SUN echo "/memory-distill" | tee -a ~/.sae4u-memory/distill-due.log
```

Or just rely on calendar / habit.
