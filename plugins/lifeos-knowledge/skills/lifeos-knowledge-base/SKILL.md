---
name: lifeos-knowledge-base
description: 'Initialize, save, deduplicate, and use knowledge in a local Markdown vault. Use for durable notes, finding relevant knowledge, or connecting a vault to Obsidian.'
---

# Build and use a knowledge base

Identify the vault from the user's chosen path, current vault, or active project instructions. Surface path conflicts and permission gaps. Follow the vault's `AGENTS.md` and `MEMORY.md`.

## Initialize

Copy the contents of `assets/vault/` into the chosen destination, filling only missing files. If Python 3.11+ and script execution are available, `scripts/init_vault.py` can perform that copy. Check `AGENTS.md`, `MEMORY.md`, `INDEX.md`, and the example. Return the vault path, the [setup guide](assets/vault/SETUP.md), and the copyable instruction for the active global or project instruction file. For an existing vault with an older guide, use this Skill's current copy. If the user requests setup in a named instruction file, read it and append the smallest applicable change.

## Capture

1. Read the vault instructions and index. Inspect the source material.
2. Check lasting value and existing notes. Compare the actual claim, evidence, scope, and use case.
3. Skip duplicates with no new value. Prefer extending an existing note with meaningful evidence. Put source material, tentative ideas, and reusable knowledge in Sources, Notes, and Wiki respectively.
4. Record the claim, source, applicable conditions, and relevant links. Save confirmed preferences within the user's scope.
5. Verify the note, sources, index, and any attachments. Report what changed and what remains unresolved.

See [daily capture](references/daily-capture.md) for manual and scheduled runs. Images are optional. Embed only an image that exists.

## Use

Search `INDEX.md` for directly relevant notes, read the body, and trace important claims to their sources when needed. Apply what fits the current task and keep checking current facts. If nothing fits, proceed with the task. Read collaboration preferences only when relevant.

When reuse tracking is requested, provide the date, task identifier or link, vault-relative note path, and how the note contributed. Include the original read identifier or evidence location when available. A note found in the index is a lead. Confirm its body was read and used before reporting reuse.
