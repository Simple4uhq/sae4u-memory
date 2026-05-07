---
name: Post-write code review gate before showing the user
description: After any non-trivial code change, run a self-review pass (or spawn a reviewer agent) hunting for hardcode, deleted sections, dead regex, missing tracking. Fix before presenting.
type: feedback
---

After a non-trivial code-writing task — file creation, file rewrite,
refactor, template generator, config edit — run a **post-write review
gate** before presenting the result.

**Why:** Multiple repeat failure modes when "refactoring":
- Deleted sections silently because the writer didn't understand
  their purpose
- Dead regex / selectors that no longer match the actual content
- Missing tracking tags (`gtag`, `dataLayer`, `GTM-`, conversion
  events) silently dropped during HTML rewrites
- Frozen guards (`if 'foo' in html: skip`) that prevent re-rendering
  when source data changes
- Hardcoded fake values that look right but were never wired up

The writer often doesn't catch these because they're focused on the
specific change. A separate review pass with a narrow brief catches
them.

**How to apply:**

1. **Trigger:** Any task that writes or edits existing files,
   creates new code files, generates templates, or edits configs.
   Skip for pure research, reads, or trivial fixes (typo, comment).

2. **Review checklist** — read the diff with these questions:
   - **Hardcoded data:** any number, string, date, or metric that
     should come from a live source but is inlined? Flag and name
     the source it should have come from.
   - **Deleted / missing sections:** compared to the original file,
     what existed before and is now gone? If intentional, was it
     flagged? If not, that's a bug.
   - **Dead regex / selectors:** any `re.sub` / `querySelector` /
     similar that targets patterns not present in the actual file
     it operates on?
   - **Frozen guards:** logic that prevents re-rendering when
     source data changes — staleness risk.
   - **Preservation of unrelated code:** changes outside the scope
     the user asked for. Every diff line not required by the task
     is suspect.
   - **Tracking tags:** in any HTML touched, confirm `gtag`,
     `GTM-`, `dataLayer`, conversion tags, and any analytics
     events that existed before are still present.
   - **Hook compatibility:** if the file is consumed by another
     process (cron, bot, API), does the output still match what
     the consumer expects?

3. **If issues found:** fix them, re-review. Maximum 3 cycles
   before escalating.

4. **Pass through to the user only after PASS.** When presenting,
   mention the work went through review and summarize what was
   checked.

5. **Optional:** if the task is large or the writer is the same
   agent doing the review, spawn a separate reviewer with a narrow
   "find what the writer missed" brief instead of self-reviewing.
