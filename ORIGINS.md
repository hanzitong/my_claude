# 各ファイルの元の場所

## この文書について

- 何の一覧か: `~/my-claude` の各ファイルが、どこから写したものかの一覧である。
- 背景: 2026-11-06 に、Claude が、ユーザーの追加した Claude Code の設定を `~/my-claude` に写し、種類ごとのフォルダに組み替えた。組み替えたあとは、ファイルの場所から元の場所が分からないため、この一覧を残す。
- 写した元: `~/.claude`（ユーザーの階層。すべてのプロジェクトに効く）と、`~/ROBO_NEXT/.claude`（ROBO_NEXT のプロジェクトの階層）の2つである。元のファイルは、変えていない。
- 写さなかったもの: `~/.claude/skills/.trash/` と `~/.claude/skills/synced/`（Claude Code が自動で作ったもの）、`~/.claude/hooks/__pycache__/`（Python が自動で作ったもの）、`~/.claude.json`（認証にかかわる情報が入っている可能性があるもの）、`~/.claude/backup/`（古い版の写し）。

## 一覧

| `~/my-claude` の中の場所 | 元の場所 |
|---|---|
| `skills/adr/`、`adr-context/`、`adr-lint/`、`code-tutor/`、`ja-revise/`、`python-coding/` | `~/.claude/skills/` |
| `skills/code-edit-check/` | `~/ROBO_NEXT/.claude/skills/` |
| `agents/adr-reviewer.md`、`design-consistency-checker.md`、`ja-reviewer.md`、`robotics-architecture-reviewer.md` | `~/.claude/agents/` |
| `agents/report-summarizer.md` | `~/ROBO_NEXT/.claude/agents/` |
| `agent-memory/` | `~/.claude/agent-memory/` |
| `commands/` | `~/.claude/commands/` |
| `output-styles/` | `~/.claude/output-styles/` |
| `hooks/adr_lint.py`、`adr_session_context.py`、`README.md` | `~/.claude/hooks/` |
| `hooks/code_edit_guard.py` | `~/ROBO_NEXT/.claude/hooks/` |
| `rules/robo-system-adr.md`、`robo-system-code.md`、`robo-system-docs.md`、`vlm-test-measurement.md` | `~/ROBO_NEXT/.claude/rules/` |
| `rules/` の上記以外の14個 | `~/.claude/rules/` |
| `claude-md/user-CLAUDE.md` | `~/.claude/CLAUDE.md` |
| `claude-md/ROBO_NEXT-CLAUDE.md` | `~/ROBO_NEXT/.claude/CLAUDE.md` |
| `settings/user-settings.json` | `~/.claude/settings.json` |
| `settings/ROBO_NEXT-settings.json` | `~/ROBO_NEXT/.claude/settings.json` |
| `memory/MEMORY-root.md`、`feedback-use-subagents.md` | `~/.claude/projects/-/memory/`（`/` で起動したセッションの自動メモリー） |
| `memory/MEMORY-cpp-practice.md`、`throwaway-code-no-skills.md` | `~/.claude/projects/-home-nachi-ai-cpp-practice/memory/` |
| `memory/MEMORY-ROBO_NEXT.md` と、上記以外の `memory/` の17個 | `~/.claude/projects/-home-nachi-ai-ROBO-NEXT/memory/` |

`MEMORY-*.md` は、元はどれも `MEMORY.md`（自動メモリーの目次）という名前だった。名前が重なるので、Claude が元のプロジェクトの名前を付けた。
