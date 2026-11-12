# Weekly Skill review

Use Monday at 09:30 to review the previous full week in your chosen time zone. Use one scheduler. If you use Dots, verify it can reach the chosen vault, ledger, and task evidence and that its displayed time zone is correct.

## Copyable prompt

> Use the LifeOS weekly review Skill for the previous complete week in <time zone>. Vault <absolute path>. State directory <path>. Check which daily audits ran and state the cutoff and missing days. Use the ledger to find candidate cases, then inspect actual tasks, visible outputs, and relevant existing Skills. Identify methods repeated in independent tasks and genuine gaps in current Skills. Write a report to <report directory> with note links, usage evidence, rationale, proposed changes, acceptance checks, and decisions pending. Leave implementation for a separate user decision.

## Run manually and verify

```sh
python3 '<reuse script path>' --vault '<vault path>' --timezone America/New_York week --week 2026-W46
```

Use the weekly output to locate the original evidence and compare at least two independent tasks when assessing a repeated method. If the daily data is incomplete, report the dates actually covered. Revisit an earlier suggestion when new evidence changes it. On the first scheduled run, verify the runner, time zone, input ledger, and output path.
