---
name: lifeos-wiki-reuse
description: 'Verify knowledge reuse for a day from task evidence. Use for daily reuse audits, maintaining a manual Markdown ledger, or running the optional local Codex log collector.'
---

# Track knowledge reuse

Confirm the vault, IANA time zone, date, selected records, and write scope. Read `INDEX.md`. Use the available original task output and read evidence to verify that a Wiki note's body was consulted and contributed to the work. Keep incomplete evidence pending and exclude audit replays.

## Manual or evidence supplied by another tool

Use [daily reuse](references/daily-reuse.md) for the portable Markdown ledger and review prompts. Reuse an existing event key for the same read. Record the actual purpose, retain evidence locations, and report pending items separately. Update the daily file only within the approved scope. Without write access, return a ready-to-save ledger and summary.

## Optional Codex collector

If the user selects the Codex path and has authorized local JSONL records, use [the collector commands](references/daily-reuse.md#codex-collector). The collector recognizes explicit single-file `cat` reads with a matching note body. Review candidate reads and their uses before applying counts. Other records can be reviewed using the portable ledger.

Report new events, per-note counts and uses, evidence and coverage. Use one counting source for the same event. Flag an overlap for reconciliation before reporting combined totals.
