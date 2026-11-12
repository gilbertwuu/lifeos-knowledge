# Compatibility

[简体中文](compatibility.zh-CN.md) · [LifeOS workflow](../README.md)

The vault is a folder of Markdown files. An Agent that can access it and follow persistent instructions can use the capture and lookup workflow. Give the Agent write access if you want it to update the vault. If you use a chat tool with uploads, attach the relevant notes for each task and apply updates yourself.

## Scheduling, reuse, and Skills

- Use the scheduling prompts with your Agent's scheduler if it supports the required file access and write scope. You can also run them manually.
- Keep a manual reuse record when the tool's traces are unavailable or use a different format. Record the date, task, note path, and how the note was used. Use those records and the actual outputs for a weekly review. The bundled collector specifically recognizes matching single-file `cat` reads in selected local Codex JSONL records.
- An Agent with Skill support can use the procedures through its own Skill mechanism. You can also supply the relevant procedure as task instructions. Check your tool's packaging and instruction format before installing or adapting it.

## Verified plugin installation

The current English plugin package has been verified in Codex. The vault initializer and reuse scripts require Python 3.11 or later.

```sh
codex plugin marketplace add gilbertwuu/lifeos-knowledge@v0.1.1
codex plugin add lifeos-knowledge@lifeos-knowledge
```

Open **LifeOS Knowledge** in Codex Desktop and start a new chat. For a local install, [download the ZIP](https://github.com/gilbertwuu/lifeos-knowledge/releases/download/v0.1.1/lifeos-knowledge-0.1.1.zip), extract it, and pass the extracted folder to the first command in place of the GitHub address.

If you added the 0.1.0 GitHub preview, run `codex plugin marketplace remove lifeos-knowledge` before the installation commands above. Your vault stays in the folder you chose.
