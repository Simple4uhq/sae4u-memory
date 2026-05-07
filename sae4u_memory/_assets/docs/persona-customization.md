# Persona customization

The default persona ships as **Simple** — a peer-level coder friend
with persistent memory. It's deliberately generic. Edit
`~/.sae4u-memory/persona.md` to make it yours.

## What's editable

The full persona document. The default is a working-rules style with:

- Identity (name = Simple, role = peer-level dev pal)
- Core values (Honesty > Comfort, Shipped > Perfect, etc.)
- Voice (terse, direct, match user register)
- Never do / Always do lists
- Memory discipline (which tools to call when)
- Memory architecture awareness (4 types)

You can rewrite any of these. Common customizations:

- **Change the name** — "Simple" is the default. Keep it, or rename.
- **Add domain context** — what stack you work in, what languages,
  what products you build, what your role is.
- **Add behavior modes** — "in code review mode, do X. In
  brainstorm mode, do Y." Modes can be mood-triggered ("when I
  swear or panic, switch to crisis mode").
- **Adjust the language default** — match your primary language.
  The default works in English; the rules are language-agnostic.
- **Adjust verbosity** — the default leans terse. If you want more
  explanation, say so explicitly.

## What's loaded at session start

`get_persona()` returns:

1. The full content of `~/.sae4u-memory/persona.md`.
2. All `*.md` files under `~/.sae4u-memory/user/`, in alphabetical
   order, concatenated as "User Context".

So you can split things logically:

```
~/.sae4u-memory/
├── persona.md              # behavior rules
└── user/
    ├── identity.md         # who you are
    ├── projects.md         # what you work on
    ├── preferences.md      # how you like to collaborate
    └── stack.md            # what tech you use
```

`get_persona()` returns all of it as one block. Order matters
(alphabetical) — name files accordingly.

## What NOT to put in persona

- Live project state — use `remember()` and `recall()` for that.
- Per-task instructions — those belong in the prompt, not persona.
- Sensitive secrets — persona is plaintext on disk. Don't put API
  keys there.
- Long histories — persona is loaded every session, so it costs
  tokens. Keep it tight; push history to per-topic memory files.

## Example: adding domain context

```markdown
## Stack

- Backend: Python 3.12, FastAPI, PostgreSQL, Redis
- Frontend: React + TypeScript, Tailwind
- Infra: AWS (ECS), GitHub Actions, Terraform
- Editor: Cursor

When I ask for code, default to these unless I say otherwise.
```

Add this to `~/.sae4u-memory/user/stack.md` and `get_persona()` will
load it automatically next session.
