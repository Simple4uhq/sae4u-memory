---
name: Never hardcode data — not even in demos
description: AI must never inline fake/placeholder/sample values in code, templates, dashboards, or UIs. If a real source is missing, surface the gap explicitly. Hidden hardcode destroys trust.
type: feedback
---

**Rule:** Never hardcode data values in any code written for the user —
not in templates, dashboards, demos, fallback paths, or "just for now"
prototypes. If a value can't come from a real source right now, the AI
must either (a) compute it from the real source, or (b) surface the
gap explicitly: empty state, "N/A", "data source unavailable", a
visible warning.

**Why:** Fake data hides failure. The user thinks they have telemetry,
they actually have decoration. Hidden hardcode destroys trust the
moment it's discovered — which is usually after a decision has
already been made on the false signal.

A typical anti-pattern: a dashboard widget shows "SEO Health 65,
Performance 100" — the user can't tell which numbers are computed
and which are inlined as design placeholders that never got wired up.

**How to apply:**

- For every data value rendered in HTML / Markdown / JSON / any
  output: trace it to a source. If there's no source, do NOT write
  a number — write empty state or surface the error.
- "Just a demo" is not an exception. Demos shown to a stakeholder
  are treated as production.
- Placeholder strings like `{{DATE}}`, `87`, `TODO`, `XXX` in
  committed code are forbidden.
- If a cron / API is broken and would normally supply a value, render
  "—" or "no data" plus a visible warning — never invent a plausible
  substitute.
- When writing a new template or generator, FIRST list every data
  field and its source. If any field has no source, ask the user
  before writing fake values.
