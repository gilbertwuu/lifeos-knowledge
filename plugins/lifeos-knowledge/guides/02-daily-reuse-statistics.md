# Daily reuse statistics

Use 09:00 in your chosen time zone to review the previous full calendar day. Choose a state directory for audit files and reports. The default is `.lifeos/` inside the vault. Start with a real task that read a note and whose tool request and returned body are available.

## Copyable prompt

> Use the LifeOS reuse Skill to review reference reads in <vault path> for the previous full day in <time zone>. Scan only <authorized record paths>. Save the candidate file, review file, and daily details in <state directory>. Check the original task and actual returned note body. Record what each verified read contributed. Exclude reads performed for this audit. Deduplicate by original read event. Preview first and update the ledger and INDEX only within the approved write scope. Report per-note counts and uses, new entries, cumulative counts, and coverage gaps.

## Run manually and verify

Use the installed Skill's `scripts/reuse.py`. Replace the example paths and date. Repeat `--record` for specific JSONL files or use `--sessions` for an authorized directory. Add `--state-dir` before the subcommand for a custom state directory.

```sh
python3 '<script path>' --vault '<vault path>' --timezone America/New_York collect --day 2026-11-13 --record '<record.jsonl>' --out '<candidates.json>'
python3 '<script path>' --vault '<vault path>' --timezone America/New_York review '<candidates.json>' '<review.json>'
python3 '<script path>' --vault '<vault path>' --timezone America/New_York review '<candidates.json>' '<review.json>' --apply
```

Review JSON example `{"candidate_id": "How the note was used in the task"}`. Preview should leave the index intact. A repeat run with the same events should add zero. Leave records pending when the body is missing or the index alone was read. On the first scheduled run, verify the trigger, day, and vault.
