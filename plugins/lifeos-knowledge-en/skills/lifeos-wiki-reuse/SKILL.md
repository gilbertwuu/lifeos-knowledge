---
name: lifeos-wiki-reuse
description: 'Verify local Wiki reads for a selected date and preview or update counts in INDEX.md. Use for daily reuse audits and duplicate-count checks.'
---

# Track knowledge reuse

Confirm the vault, time zone, date, authorized record paths, and write scope. Read the vault instructions and `INDEX.md`. Run this Skill's `scripts/reuse.py` with Python 3.11+. See `guides/02-daily-reuse-statistics.md` in the plugin root for examples.

1. Run `collect` on the selected local Codex JSONL files or directories. Group reads by response time and record evidence and coverage gaps. Candidates are observed reads.
2. Check the original task, request, and returned note body. Put verified uses in a review JSON file as `{"candidate_id": "concrete use in the task"}`. When a task spans records or turns, use `{"purpose": "concrete use", "task": "verified task ID"}` as the value. Leave uncertain events pending and exclude audit replays.
3. Run `review` for a preview. Use `--apply` for an authorized update to the ledger and index. Count each real read once, including separate real reads of the same note.
4. Report new events, per-note uses and totals, and coverage gaps. Provide the original record locations where available.

The collector covers matching single-file `cat` requests with a note body returned. Compressed records, other tool formats, other hosts, and records for changed notes require separate review. If existing index counts have no matching ledger, start with an isolated vault or migrate the existing ledger.
