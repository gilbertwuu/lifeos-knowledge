# Daily knowledge capture

## Configure

Choose a vault, an IANA time zone, the authorized conversations or exports, and a report or checkpoint path. Start with one useful source and one duplicate. Suggested schedule: daily at 23:50 in the chosen time zone.

| Mode | What to do |
| --- | --- |
| Scheduled | Put the prompt below in a scheduler that can invoke your Agent, access the selected messages or exports, and write to the vault and checkpoint. The run can screen, deduplicate, save, and report within the chosen scope. |
| Manual | Run the same prompt in a chat with access to the vault and the selected material. If the Agent lacks file-write access, ask it to return the proposed notes and index changes for you to save. If chat history is inaccessible, provide the authorized text or export. |

## Prompt

> Use the LifeOS knowledge base Skill to capture durable knowledge for <local date or today> in <IANA time zone>. Vault <path>. Authorized conversations or export files <scope>. Checkpoint <path>. Read MEMORY.md, INDEX.md, and the last checkpoint if present. Use timestamps to find new messages, including updates in older conversations. Read the visible text within scope. Screen for lasting value, deduplicate by substance, and save Sources, Notes, or Wiki entries under the vault rules. Verify notes, sources, and index. Report changes, coverage gaps, and what to revisit. If nothing qualifies, record the run outcome without adding notes.

## Verify

Check that the original source can be located, the duplicate was skipped or merged, and the checkpoint identifies the actual coverage. On the first scheduled run, verify that it fired in the chosen time zone and could access the same files.
