# Claude Code Commands Cheat Sheet

A free, plain-English cheat sheet of Claude Code commands, checked against the official Anthropic docs. One new command is added every episode.

**Download:** [claude-code-cheat-sheet.pdf](claude-code-cheat-sheet.pdf)

## Commands so far

| Command | What it does |
|---|---|
| `/doctor prompt-audit` | Checks your CLAUDE.md, skills, and rules for outdated or conflicting instructions, and proposes edits you approve. |
| `/context` | Shows what's filling Claude's context window as a colored grid by category. It deletes nothing. |
| `/model` | Switches the model and its effort. Press Enter to make it your default, or `s` for this session only. |
| `/permissions` | Shows and edits the allow, ask and deny rules every tool call is checked against. |
| `/clear` | Starts a fresh conversation. The old one is kept, and `/resume` brings it back. |
| `/login` | Sets who pays: a Claude subscription, API billing through the Console, or a platform like Amazon Bedrock. |
| `/goal` | Gives Claude a finish line. A separate model checks it after every turn, and Claude keeps going until it's met. |

The PDF is printed from [`cheat-sheet.html`](cheat-sheet.html) in Chrome (US Letter).

## Kept current

Every other Monday, [`scripts/docs_check.py`](scripts/docs_check.py) compares each card against the official [Claude Code commands reference](https://code.claude.com/docs/en/commands.md) and the pages it links to. A Gemini checker (via the `agy` CLI) flags any claim the docs now contradict. Drift opens a ticket. `--dry-run` prints the findings instead.

## Get the next command

New commands land in the Rue Athena Dispatch newsletter first: [dispatch.rueathena.com](https://dispatch.rueathena.com)

Made by [Ted Sandico](https://rueathena.com), GTM engineer at Rue Athena.

Built with Grok Bot.
