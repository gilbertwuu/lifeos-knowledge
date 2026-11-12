# Weekly Skill review

## Configure

Choose the previous complete week in an IANA time zone, the daily Markdown ledgers or an automated evidence export, the actual task outputs you can access, the relevant existing Skills, and a report path. Suggested schedule: Monday at 09:30, after the last daily audit has written its results.

| Mode | What to do |
| --- | --- |
| Scheduled | Set a scheduler to run the prompt below. Give it access to the selected ledgers, task evidence, and Skills and permission to write the report. It can generate a proposal and flag gaps. Review adoption yourself. |
| Manual | Give your Agent the completed daily ledgers, original task excerpts, and existing Skills or their relevant procedures. Run the same prompt. If write access is unavailable, save the returned report yourself. |

## Prompt

> Use the LifeOS weekly review Skill for <week or previous complete week> in <time zone>. Vault <path>. Daily evidence <files or export>. Original tasks and existing Skills <scope>. Check what dates are covered and report the cutoff. Verify which methods recurred across independent tasks using the actual outputs. Compare the method against current Skills. Write a report to <path> with evidence, proposed treatment, scope, acceptance checks, and decisions pending. Keep Skill changes for a separate decision.

## Optional collector export

If daily statistics use the bundled Codex collector, run its weekly export with the same vault, state directory and time zone. The Skill can work from its JSON output and the underlying task evidence.

```sh
python3 '<reuse script path>' --vault '<vault path>' --timezone America/New_York week --week 2026-W46
```

## Verify

Check at least two independent cases before treating a method as repeated. Review the actual steps, outputs, current Skill coverage, and missing days. The first scheduled run should use the intended week and evidence paths and produce a report where expected. The report can conclude that the current evidence is insufficient.
