# LifeOS Knowledge

[简体中文](README.zh-CN.md)

LifeOS is an AI-led knowledge workflow that grows through use. Save useful ideas in a local Markdown vault, let Codex draw on them in real work, and review recurring methods as candidates for reusable Skills.

## Install in Codex

Choose one edition. Run the commands below with the Codex CLI, then open the installed plugin in Codex Desktop and start a new chat. The vault and reuse scripts require Python 3.11 or later.

```sh
codex plugin marketplace add gilbertwuu/lifeos-knowledge@v0.1.0
codex plugin add lifeos-knowledge-en@lifeos-knowledge
```

See the [English plugin guide](plugins/lifeos-knowledge-en/README.md) for the three Skills and scheduled task setup. See the [releases page](https://github.com/gilbertwuu/lifeos-knowledge/releases) for downloadable packages.

If you download a ZIP, unzip it and pass the extracted folder to `codex plugin marketplace add` in place of the GitHub repository.

## Try the full workflow

1. **Capture.** Ask Codex to initialize a vault in an empty folder of your choice. Give it one useful idea with its source. It checks for duplicates, saves the material, and updates the index. Open the same folder in Obsidian to read the notes and see their links and backlinks.
2. **Use.** [Add the provided rule to `AGENTS.md`](plugins/lifeos-knowledge-en/skills/lifeos-knowledge-base/assets/vault/SETUP.md) and enter your vault path. In a fresh chat, give Codex an ordinary task related to a saved note. Check that it found the note and applied its method.
3. **Review.** Use the daily reuse Skill to verify and record reads from selected Codex records. Use the weekly Skill to check which methods recur across independent tasks, compare them with existing Skills, and propose a change for you to review.

The three scheduling guides cover daily knowledge capture, daily reuse statistics, and weekly Skill review. You choose the schedules, input scope, and vault. Version 0.1.0's reuse collector recognizes explicit single-file `cat` calls in selected local Codex JSONL records.
