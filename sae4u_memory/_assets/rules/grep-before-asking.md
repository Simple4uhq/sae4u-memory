---
name: Grep / read before asking the user for data
description: If the data is likely to exist in conversation files, codebase, or memory, search for it before asking the user to provide it. Only ask for truly external data (preferences, future picks).
type: feedback
---

Before asking the user to provide a value — API key, URL, ID, price,
config — **search the codebase, conversation files, and memory first**.
Half the time it's already there.

**Why:** Asking for data that the user already gave you (or that's
sitting in a file you read minutes ago) is a trust killer. It signals
you weren't paying attention. Worse, it makes interactive sessions
feel like data-entry forms.

**How to apply:**

- Before any user-facing question that requests data, run one
  grep/find pass on the relevant artifacts:
  - Repo files (`grep` for the keyword, `find` for filename hints)
  - Recent conversation context
  - Memory (`recall(query)` with related terms)
  - Project trackers (backlog, issues, README)
- The bar: only ask the user when the data is genuinely external
  to their working context — a preference they haven't expressed,
  a strategic pick that depends on future intent, an external system
  the AI cannot read.
- Strategic / preference questions (which approach, which target
  audience) are valid to ask. Lookup questions for data that exists
  somewhere in the repo are not.
