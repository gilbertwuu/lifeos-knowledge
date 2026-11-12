# LifeOS Knowledge

Open LifeOS Knowledge in Codex Desktop and start a new chat. Use Python 3.11 or later for the vault and reuse scripts.

1. **Build and use your vault.** Ask Codex to initialize a folder you choose. Open the [setup guide](skills/lifeos-knowledge-base/assets/vault/SETUP.md) and add its knowledge rule to the active `AGENTS.md`. Use a global rule for all projects, or a project rule for one. Start a fresh chat with an ordinary task to verify the connection. Obsidian can open the same folder as a vault.
2. **Track knowledge reuse.** Specify a vault, time zone, date, and the Codex records Codex may read. Check the preview, then approve the update. Daily details and weekly evidence can live in the vault's `.lifeos/` directory or in a state directory you choose.
3. **Review Skill candidates.** Pick a week and compare methods repeated in real tasks with existing Skills. Review the proposed improvements and decide what to adopt.

## Scheduled task guides

- [Daily knowledge capture](guides/01-daily-knowledge-capture.md)
- [Daily reuse statistics](guides/02-daily-reuse-statistics.md)
- [Weekly Skill review](guides/03-weekly-skill-review.md)

Run each guide manually in a test vault before setting a schedule. The collector recognizes explicit single-file `cat` reads in selected Codex JSONL records. The weekly review verifies actual use and counts independent tasks separately from reads.
