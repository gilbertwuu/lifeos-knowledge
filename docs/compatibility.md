# Install and configure LifeOS

[简体中文](compatibility.zh-CN.md) · [LifeOS workflow](../README.md)

## Use the same download in your Agent

1. Extract the [LifeOS ZIP](https://github.com/gilbertwuu/lifeos-knowledge/releases/download/v0.2.0/lifeos-knowledge-0.2.0.zip). Under [plugins/lifeos-knowledge/skills](../plugins/lifeos-knowledge/skills), each Skill is an independent directory following the [Agent Skills format](https://agentskills.io/specification). Keep the directory name and all of its files together.
2. Copy the three folders to the location your Agent scans, or import each folder using its Skill manager. For example, a project can use `.agents/skills/` if the tool scans that location. Claude Code supports `.claude/skills/` in a project. When an importer requires a per-Skill ZIP, compress the corresponding Skill folder from the same download. If the tool has no Skill loader, use its `SKILL.md` and linked resources as task instructions. [Claude Code project Skills](https://code.claude.com/docs/en/skills)
3. Start a new session and invoke `lifeos-knowledge-base` to initialize a test vault. Follow its [setup rule](../plugins/lifeos-knowledge/skills/lifeos-knowledge-base/assets/vault/SETUP.md) using your Agent's persistent instruction settings. Give the Agent read access to the vault and write access for changes it should save. With an upload-only tool, attach the relevant files and save returned changes yourself.

## Configure scheduling and evidence

| Workflow | Inputs and output | Run options |
| --- | --- | --- |
| [Daily capture](../plugins/lifeos-knowledge/skills/lifeos-knowledge-base/references/daily-capture.md) | Selected messages or exports → notes, index and checkpoint | Schedule with file and history access, or supply the material when running manually. |
| [Daily reuse](../plugins/lifeos-knowledge/skills/lifeos-wiki-reuse/references/daily-reuse.md) | Actual read and use evidence → daily Markdown ledger or reviewed collector output | A scheduled Agent can review accessible evidence. If logs are unavailable, provide original excerpts or track reuse as you work. |
| [Weekly review](../plugins/lifeos-knowledge/skills/lifeos-skill-review/references/weekly-review.md) | Daily ledgers or a collector export, tasks and existing Skills → proposal report | Run after the daily audits. Approve actual Skill changes separately. |

Set the IANA time zone, source scope, vault path and output paths in each prompt. Verify one manual run before adding the same prompt to your tool's scheduler. Then check the first real trigger and whether the scheduled environment can reach the same files. Installing the Skills creates no schedules.

The Markdown ledger works without scripts. The optional collector needs Python 3.11+ on a POSIX system and selected local Codex JSONL records. It detects explicit single-file `cat` reads with matching note content. A reviewer confirms use before counts are written.

## Optional Codex marketplace installation

```sh
codex plugin marketplace add gilbertwuu/lifeos-knowledge@v0.2.0
codex plugin add lifeos-knowledge@lifeos-knowledge
```

For a local install, pass the extracted folder to the first command instead of the GitHub address. If an earlier GitHub release is already registered, first run `codex plugin marketplace remove lifeos-knowledge`. This removes the marketplace registration. Your vault stays in the folder you chose.
