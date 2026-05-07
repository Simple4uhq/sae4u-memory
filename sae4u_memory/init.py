"""Init subcommand — configure Claude Desktop/Code to use sae4u-memory.

Two install profiles:
- `init` (default) — registers the MCP server with Claude Desktop and/or Claude Code.
  Cross-client, minimal install. Good for users who just want persistent memory.
- `init --code-full` — Claude Code-specific full install: MCP wiring + memory-tick.sh
  hook + scaffolds ~/.sae4u-memory/MEMORY.md + drops default rules into
  ~/.sae4u-memory/rules/. Required for the full architecture (tick reviews + rule files
  + MEMORY.md index).
"""

from __future__ import annotations

import argparse
import json
import platform
import shutil
import sys
from pathlib import Path


MARKER_START = "<!-- sae4u-memory:start -->"
MARKER_END = "<!-- sae4u-memory:end -->"

CLAUDE_MD_BLOCK = f"""
{MARKER_START}
## sae4u-memory

Persistent memory across sessions via MCP tools. Use them actively, not only when asked.

- `get_persona()` — call at session start to load identity + user context
- `recall(query, limit, sources)` — search BOTH corpora:
    1. SQLite facts saved via `remember`
    2. Markdown files in Claude Code auto-memory dirs + sae4u-memory home
       (~/.claude/projects/<slug>/memory/*.md, tick logs, permanent files in
       ~/.sae4u-memory/)
  Call this at the start of any substantive request — before answering, pull
  the relevant prior context (feedback rules, project state, recent ticks).
- `remember(text, category)` — save facts. Categories:
  `user`, `feedback`, `project`, `reference`, `general`.
- `journal(text)` — end-of-session recap after significant work
- `list_memories(category)` — browse SQLite-stored memories
- `forget(memory_id)` — remove wrong/outdated SQLite memories

At session start: `get_persona()`.
Before answering a non-trivial request: `recall(topic)` first, then respond.
Whenever something surprising or non-obvious comes up: `remember()` it immediately.
{MARKER_END}
"""

# Path to repo assets (hooks/, rules/, templates/) bundled with the package.
# At install time these live in <repo-root>/ alongside the simple4u_memory package dir.
PKG_ROOT = Path(__file__).resolve().parent.parent


def claude_desktop_config() -> Path | None:
    system = platform.system()
    home = Path.home()
    if system == "Darwin":
        return home / "Library/Application Support/Claude/claude_desktop_config.json"
    if system == "Windows":
        return home / "AppData/Roaming/Claude/claude_desktop_config.json"
    if system == "Linux":
        return home / ".config/Claude/claude_desktop_config.json"
    return None


def claude_code_settings() -> Path:
    return Path.home() / ".claude" / "settings.json"


def claude_code_md() -> Path:
    return Path.home() / ".claude" / "CLAUDE.md"


def claude_code_hooks_dir() -> Path:
    return Path.home() / ".claude" / "hooks"


def sae4u_home() -> Path:
    return Path.home() / ".sae4u-memory"


def ensure_mcp_config(config_path: Path, dry_run: bool) -> str:
    """Add sae4u-memory to mcpServers. Idempotent. Returns status label."""
    existing: dict = {}
    if config_path.exists():
        try:
            existing = json.loads(config_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return f"skipped (invalid JSON): {config_path}"

    servers = existing.setdefault("mcpServers", {})
    entry = servers.get("sae4u-memory")
    if isinstance(entry, dict) and entry.get("command") == "sae4u-memory":
        return f"already set: {config_path}"

    servers["sae4u-memory"] = {"command": "sae4u-memory"}

    if dry_run:
        return f"[dry-run] would write: {config_path}"

    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")
    return f"wrote: {config_path}"


def ensure_claude_md(md_path: Path, dry_run: bool) -> str:
    """Append memory guidance block to CLAUDE.md. Idempotent via markers."""
    existing = md_path.read_text(encoding="utf-8") if md_path.exists() else ""
    if MARKER_START in existing:
        return f"already set: {md_path}"

    new_content = existing.rstrip() + "\n" + CLAUDE_MD_BLOCK

    if dry_run:
        return f"[dry-run] would write: {md_path}"

    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(new_content, encoding="utf-8")
    return f"wrote: {md_path}"


def ensure_hook(dry_run: bool) -> str:
    """Copy hooks/memory-tick.sh into ~/.claude/hooks/. Idempotent (checksum compare)."""
    src = PKG_ROOT / "hooks" / "memory-tick.sh"
    if not src.exists():
        return f"hook source not found in package: {src}"

    dst_dir = claude_code_hooks_dir()
    dst = dst_dir / "memory-tick.sh"

    if dst.exists():
        if dst.read_bytes() == src.read_bytes():
            return f"already set: {dst}"
        if dry_run:
            return f"[dry-run] would update (changed): {dst}"
        dst.write_bytes(src.read_bytes())
        dst.chmod(0o755)
        return f"updated: {dst}"

    if dry_run:
        return f"[dry-run] would write: {dst}"

    dst_dir.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(src.read_bytes())
    dst.chmod(0o755)
    return f"wrote: {dst}"


def ensure_hook_registered(settings_path: Path, dry_run: bool) -> str:
    """Register memory-tick.sh in Claude Code settings.json hooks block."""
    existing: dict = {}
    if settings_path.exists():
        try:
            existing = json.loads(settings_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return f"skipped (invalid JSON): {settings_path}"

    hook_command = "$HOME/.claude/hooks/memory-tick.sh"
    hooks_block = existing.setdefault("hooks", {})
    submit_hooks = hooks_block.setdefault("UserPromptSubmit", [])

    for matcher_block in submit_hooks:
        for hk in matcher_block.get("hooks", []):
            if hk.get("command") == hook_command:
                return f"already registered in: {settings_path}"

    submit_hooks.append(
        {
            "matcher": "*",
            "hooks": [{"type": "command", "command": hook_command}],
        }
    )

    if dry_run:
        return f"[dry-run] would register hook in: {settings_path}"

    settings_path.parent.mkdir(parents=True, exist_ok=True)
    settings_path.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")
    return f"registered hook in: {settings_path}"


def scaffold_home(dry_run: bool) -> str:
    """Create ~/.sae4u-memory/MEMORY.md, rules/, tick/ if missing.

    Copies bundled rule defaults (rules/*.md from the package) into
    ~/.sae4u-memory/rules/ on first run. Existing files are never overwritten.
    """
    home = sae4u_home()

    actions: list[str] = []

    memory_md = home / "MEMORY.md"
    if not memory_md.exists():
        if dry_run:
            actions.append(f"[dry-run] would create {memory_md}")
        else:
            home.mkdir(parents=True, exist_ok=True)
            template_path = PKG_ROOT / "templates" / "MEMORY.md.template"
            if template_path.exists():
                memory_md.write_text(template_path.read_text(encoding="utf-8"), encoding="utf-8")
            else:
                memory_md.write_text(
                    "# MEMORY index\n\n"
                    "<!-- One line per memory file. Format: -->\n"
                    "<!-- - [Title](file.md) — one-line hook (under ~150 chars) -->\n",
                    encoding="utf-8",
                )
            actions.append(f"created {memory_md}")

    tick_dir = home / "tick"
    if not tick_dir.exists():
        if dry_run:
            actions.append(f"[dry-run] would create {tick_dir}")
        else:
            tick_dir.mkdir(parents=True, exist_ok=True)
            actions.append(f"created {tick_dir}")

    rules_dir = home / "rules"
    src_rules = PKG_ROOT / "rules"
    if src_rules.exists() and src_rules.is_dir():
        if not rules_dir.exists():
            if dry_run:
                actions.append(f"[dry-run] would copy rules/ → {rules_dir}")
            else:
                shutil.copytree(src_rules, rules_dir)
                actions.append(f"copied rules/ → {rules_dir}")
        else:
            actions.append(f"rules/ already present: {rules_dir}")

    return " | ".join(actions) if actions else f"already scaffolded: {home}"


def remove_mcp_config(config_path: Path, dry_run: bool) -> str:
    """Remove sae4u-memory from mcpServers. Returns status label."""
    if not config_path.exists():
        return f"not found: {config_path}"
    try:
        existing = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return f"skipped (invalid JSON): {config_path}"

    servers = existing.get("mcpServers") or {}
    if "sae4u-memory" not in servers:
        return f"not configured: {config_path}"

    del servers["sae4u-memory"]
    if dry_run:
        return f"[dry-run] would remove from: {config_path}"

    config_path.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")
    return f"removed from: {config_path}"


def remove_claude_md(md_path: Path, dry_run: bool) -> str:
    """Remove memory guidance block from CLAUDE.md."""
    if not md_path.exists():
        return f"not found: {md_path}"
    existing = md_path.read_text(encoding="utf-8")
    if MARKER_START not in existing or MARKER_END not in existing:
        return f"not configured: {md_path}"

    start = existing.find(MARKER_START)
    end = existing.find(MARKER_END) + len(MARKER_END)
    cleaned = (existing[:start].rstrip() + "\n" + existing[end:].lstrip()).strip() + "\n"

    if dry_run:
        return f"[dry-run] would clean: {md_path}"

    md_path.write_text(cleaned, encoding="utf-8")
    return f"cleaned: {md_path}"


def cmd_init(args: argparse.Namespace) -> int:
    do_desktop = args.desktop or not (args.code or args.code_full)
    do_code = args.code or args.code_full or not args.desktop
    do_full = args.code_full

    print("Setting up sae4u-memory.\n")

    if do_desktop:
        print("Claude Desktop:")
        desktop = claude_desktop_config()
        if desktop is None:
            print(f"  unsupported platform: {platform.system()}")
        else:
            print(f"  {ensure_mcp_config(desktop, args.dry_run)}")
        print()

    if do_code:
        print("Claude Code:")
        print(f"  {ensure_mcp_config(claude_code_settings(), args.dry_run)}")
        print()

    if not args.no_claude_md:
        print("Session guidance (CLAUDE.md):")
        print(f"  {ensure_claude_md(claude_code_md(), args.dry_run)}")
        print()

    if do_full:
        print("Memory-tick hook (UserPromptSubmit):")
        print(f"  {ensure_hook(args.dry_run)}")
        print(f"  {ensure_hook_registered(claude_code_settings(), args.dry_run)}")
        print()

        print("Memory home scaffolding:")
        print(f"  {scaffold_home(args.dry_run)}")
        print()

    if args.dry_run:
        print("Dry run complete. Re-run without --dry-run to apply.")
    else:
        print("Done. Restart Claude Desktop/Code for changes to take effect.")
        if do_full:
            print(
                "\nTip: read docs/architecture.md and docs/tick-protocol.md in the "
                "sae4u-memory repo for how the full architecture works."
            )
    return 0


def cmd_uninstall(args: argparse.Namespace) -> int:
    print("Removing sae4u-memory from Claude Desktop/Code configs.\n")

    print("Claude Desktop:")
    desktop = claude_desktop_config()
    if desktop:
        print(f"  {remove_mcp_config(desktop, args.dry_run)}")
    print()

    print("Claude Code:")
    print(f"  {remove_mcp_config(claude_code_settings(), args.dry_run)}")
    print()

    print("Session guidance (CLAUDE.md):")
    print(f"  {remove_claude_md(claude_code_md(), args.dry_run)}")
    print()

    print(
        "Config cleaned. Data directory (~/.sae4u-memory/) and the memory-tick hook\n"
        "in ~/.claude/hooks/ are left intact in case you reinstall.\n"
        "To remove fully:\n"
        "  rm ~/.claude/hooks/memory-tick.sh\n"
        "  rm -rf ~/.sae4u-memory\n"
        "  pip uninstall sae4u-memory"
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sae4u-memory",
        description="Persistent memory architecture for Claude.",
    )
    sub = parser.add_subparsers(dest="command")

    init = sub.add_parser("init", help="Configure Claude Desktop/Code to use sae4u-memory")
    init.add_argument("--desktop", action="store_true", help="Configure Claude Desktop only")
    init.add_argument("--code", action="store_true", help="Configure Claude Code only (MCP only)")
    init.add_argument(
        "--code-full",
        action="store_true",
        help="Claude Code full install: MCP + memory-tick hook + MEMORY.md scaffold + rules",
    )
    init.add_argument("--no-claude-md", action="store_true", help="Skip CLAUDE.md guidance block")
    init.add_argument("--dry-run", action="store_true", help="Preview changes without applying")
    init.set_defaults(func=cmd_init)

    uninstall = sub.add_parser("uninstall", help="Remove sae4u-memory config from Claude")
    uninstall.add_argument("--dry-run", action="store_true", help="Preview changes without applying")
    uninstall.set_defaults(func=cmd_uninstall)

    return parser


def run_cli(argv: list[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 1
    return args.func(args)
