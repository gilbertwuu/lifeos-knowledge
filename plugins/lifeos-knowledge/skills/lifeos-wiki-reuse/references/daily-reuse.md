# Daily reuse statistics

## Configure

Choose a vault, an IANA time zone, authorized task records, and a state directory. Suggested schedule: daily at 09:00, reviewing the previous complete local calendar day.

| Available evidence | Can run automatically | Needs manual work |
| --- | --- | --- |
| Task records with accessible evidence and stable read IDs | A scheduled Agent can check the selected evidence and update the Markdown ledger within an approved write scope. | Set source scope and inspect ambiguous or missing evidence. Provide excerpts if the Agent cannot reach the original records. |
| Matching local Codex JSONL records | The optional collector can discover candidates. Reviewed events can be written to the index and ledger in an authorized run. | Verify actual use before applying. Unmatched tools, missing bodies, and inaccessible records need separate review. |
| Task notes or links supplied by hand | The Agent can summarize the submitted evidence. | Save the evidence as you work or provide it when you run the audit. Copy back the resulting ledger if file writing is unavailable. |

## Portable Markdown ledger

Keep one file per local day, for example `.lifeos/reuse/2026-11-13.md`. The evidence link can be a task URL, a local relative path, or a source name and exact location. Use only evidence you may store in that vault.

| Event key | Task ID or link | Wiki path | Actual use | Evidence location |
| --- | --- | --- | --- | --- |
| run-17/read-2 | task-17 | `03_Wiki/Methods/observations.md` | Distinguished observations from candidate explanations | task-17, read 2 and final response |

Use the original read ID when available. Otherwise keep one stable key per verified occurrence, for example a stable task ID plus note path. Count additional reads in the same task only when distinct evidence exists. Before updating the daily file, load it and merge by event key. Keep pending items and missing source ranges below the table. Report counts from verified rows and independent tasks from task IDs. A repeat audit over the same evidence should add zero rows.

The Markdown ledger can be used with no script. It feeds the weekly review directly. Keep its totals separate from the collector's INDEX column when records overlap. To produce one combined total, reconcile by original read evidence first.

## Prompt

> Run the LifeOS daily reuse audit for <date> in <time zone>. Vault <path>. Authorized task records <paths, links, or excerpts>. Use <Markdown ledger or Codex collector>. Verify each note body was read and used in the original task. Merge only verified reads into <output path> within the approved write scope. Report new reads, counts and uses by note, independent task IDs, and coverage gaps. Exclude audit replays. If evidence is unavailable, report the gap and give the user a ready-to-fill ledger.

## Codex collector

Run the optional `scripts/reuse.py` with Python 3.11+ on a POSIX system. Replace the example paths and date. Repeat `--record` for specific JSONL files or use `--sessions` for an authorized directory. If needed, put `--state-dir '<state directory>'` before the subcommand. Use the same vault, state directory, and time zone for all runs.

```sh
python3 '<script path>' --vault '<vault path>' --timezone America/New_York collect --day 2026-11-13 --record '<record.jsonl>' --out '<candidates.json>'
python3 '<script path>' --vault '<vault path>' --timezone America/New_York review '<candidates.json>' '<review.json>'
python3 '<script path>' --vault '<vault path>' --timezone America/New_York review '<candidates.json>' '<review.json>' --apply
```

Write the review JSON from verified candidates, for example `{"candidate_id": "How the note was used in the task"}`. Preview should leave the index intact. Applying requires the configured write scope. A repeat run with the same reads should add zero. Inspect both the returned note body and original task output. Use one writer per vault for scheduled updates.
