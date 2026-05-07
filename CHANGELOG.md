# Changelog

## 0.2.0 — 2026-05-07 — Memory architecture release

**Renamed** from `simple4u-memory` to `sae4u-memory` to align with
the [SAE4U OSS family](https://github.com/Simple4uhq) (sister project:
[`sae4u-agent`](https://github.com/Simple4uhq/sae4u-agent)).

### Added — full memory architecture export
- `hooks/memory-tick.sh` — UserPromptSubmit hook that fires every
  10 min and forces a brief memory review. Catches borderline
  observations before they fall out of context.
- `rules/` — 10 universal feedback rules:
  - `memory-tick-protocol.md` — the 10-min review pattern
  - `memory-cleanup-interactive.md` — never auto-forget
  - `memory-architecture-minimalist.md` — don't tier prematurely
  - `no-session-state-confabulation.md` — don't BS recent work
  - `session-open-mirror-handoff.md` — mirror first, suggest after
  - `verify-evidence-before-citing.md` — don't fake authority
  - `grep-before-asking.md` — search before asking the user
  - `no-hardcode.md` — surface failures, never inline placeholders
  - `post-write-review.md` — self-review pass after non-trivial
    code writes
  - `agents-no-delete-features.md` — preserve existing structure
- `prompts/session-open.md`, `prompts/session-close.md` — opinionated
  session-boundary prompts paired with the architecture.
- `templates/` — `MEMORY.md`, feedback-rule, project-fact, tick-log.
- `docs/` — architecture, tick-protocol, persona-customization,
  episodic-bridge.
- `commands/memory-distill.md` — weekly distill ritual.

### Added — persona
- Default persona renamed from "Working Rules" (no character) to
  **Simple**: a named, generic peer-level coder friend with
  persistent memory awareness. Identity, voice, values, and
  4-type memory architecture awareness baked in. Edit
  `~/.sae4u-memory/persona.md` to customize.

### Added — `init --code-full`
- New flag for Claude Code users: in addition to the standard MCP
  wiring, copies `memory-tick.sh` to `~/.claude/hooks/`, registers
  it in `~/.claude/settings.json` under `hooks.UserPromptSubmit`,
  scaffolds `~/.sae4u-memory/MEMORY.md`, and drops default rules
  into `~/.sae4u-memory/rules/`.

### Changed
- Package name: `simple4u-memory` → `sae4u-memory`.
- Module name: `simple4u_memory` → `sae4u_memory`.
- Data directory: `~/.simple4u-memory/` → `~/.sae4u-memory/`.
- Env vars: `SIMPLE4U_MEMORY_HOME` → `SAE4U_MEMORY_HOME`,
  `SIMPLE4U_MARKDOWN_ROOTS` → `SAE4U_MARKDOWN_ROOTS`.
- CLAUDE.md guidance block markers: `<!-- simple4u-memory:start -->`
  → `<!-- sae4u-memory:start -->`.
- `markdown_memory.py`: hardcoded user-slug path removed from
  defaults — Claude Code auto-memory dirs now discovered via glob
  `~/.claude/projects/*/memory/`.
- `MemoryStore.recall()` and `list_memories()` documentation:
  category list now reflects the architecture (`user`, `feedback`,
  `project`, `reference`, `general`).

### Notes for v0.1.x users
The PyPI package `simple4u-memory@0.1.3` is no longer maintained.
There is no in-place upgrade path; install fresh from this repo:

```bash
git clone https://github.com/Simple4uhq/sae4u-memory
cd sae4u-memory
pip install -e .
sae4u-memory init
```

Your existing `~/.simple4u-memory/` data is not auto-migrated —
copy or move the contents to `~/.sae4u-memory/` if you want to
keep them.

---

## 0.1.3 — 2026-04-15 (under previous name `simple4u-memory`)
- DEFAULT_PERSONA rewritten as working rules — no character, no
  name. Ships discipline (no-hardcode, verify-before-citing,
  no-silent-rewrites, post-write review). Existing
  `~/.simple4u-memory/persona.md` files never overwritten.

## 0.1.2 — 2026-04-15
- Two-corpus `recall()` — search both SQLite facts and markdown
  files in one call. New module `markdown_memory.py`. Env var
  `SIMPLE4U_MARKDOWN_ROOTS`. New `sources` param on `recall()`.

## 0.1.1 — 2026-04-13
- First public release on PyPI. `init` and `uninstall` CLI
  subcommands. Cross-platform (macOS / Windows / Linux).

## 0.1.0
- Initial internal build.
