---
name: Don't delete existing features when refactoring
description: When refactoring or fixing code, preserve all existing sections and features. Never remove functionality without explicit confirmation. Catalog before, verify after.
type: feedback
---

When analyzing, refactoring, or fixing code, the AI must NOT delete
or remove existing sections, features, or data that was already
working. If a section needs to be rewritten, the replacement must
include all the content from the original.

**Why:** Refactor agents often remove sections they don't understand
the purpose of, assuming dead code or unused features. The result
is silent data loss that the user only catches later — sometimes
much later.

A typical anti-pattern: an agent fixing a dashboard generator removes
the "Keyword Research" and "Seed Keywords" sections from the template
because they don't see how those sections are populated, not realizing
those are read by a different cron job that runs later.

**How to apply:**

- **Before modifying any file**, catalog ALL existing sections,
  functions, features, data fields. List them.
- **After modification**, verify the same sections exist in the
  output. Diff against the catalog.
- If a section can't be preserved due to a needed refactor,
  flag it explicitly and ask for confirmation BEFORE removing.
- Never assume a section is "dead" or "unnecessary" — it may be
  there for a reason that's not visible from this file.
- This applies to HTML templates, Python generators, config files,
  CSS, and any production code.
- For consumed files (cron output, bot input), the consumer's
  expectations determine what must be preserved — even content
  that looks like noise from inside the writer's view.
