---
name: project-config-in-project-dir
description: ROBO_NEXT だけの決まり（robo_system の文書・コード・ADR の運用、vlm_test の計測）は ~/ROBO_NEXT/.claude/。ADR 駆動やロボット開発に使える汎用のスキル・エージェント・ルールは ~/.claude/
metadata:
  node_type: memory
  type: feedback
  originSessionId: 02b41f30-973c-4d10-b939-fac9081c4ba5
  modified: 2026-11-04T09:38:19.953Z
---

Claude Code の設定は、中身が ROBO_NEXT だけの決まりか、ほかのプロジェクトでも使えるかで置き場所を分ける。

| 置き場所 | 置くもの（2026-11-04 の配置） |
|---|---|
| `~/ROBO_NEXT/.claude/` | ルール `robo-system-code.md`、`robo-system-docs.md`、`robo-system-adr.md`、`vlm-test-measurement.md`。エージェント `report-summarizer`。スキル `code-edit-check` とフック `hooks/code_edit_guard.py`（登録は `settings.json`）。目的を書いた `CLAUDE.md` |
| `~/.claude/` | 汎用のもの。スキル `adr`、`adr-context`、`adr-lint`、エージェント `adr-reviewer`、`design-consistency-checker`、`robotics-architecture-reviewer`、ルール `robotics-runtime.md`、フック `hooks/adr_lint.py`、`adr_session_context.py`。Python と日本語のルール、`python-coding`、`ja-revise` など |

**Why:** 2026-11-04 にユーザーが「robo_systemは現在開発中のパッケージに過ぎないのでわざわざ全てのパッケージで効果を発揮する場所に設定を書かないで下さい」と指示し、Claude がすべてをプロジェクトに移した。その直後にユーザーが「結構汎用性があるスキルやエージェントがROBONEXT固有のものとなってしまっていますね。…本当にROBO_NEXT固有のものって少ないと思ってます。adr駆動開発も他のプロジェクトで実践する予定ですし、ロボット関連の開発を行いますから」と言い、汎用のものだけを ~/.claude/ に戻した（ユーザーが選んだ）。

**How to apply:**
- 新しく作るときは「ほかのプロジェクト（ADR 駆動の開発、ロボットの開発）でも使うか」で決める。使うなら `~/.claude/`、ROBO_NEXT の決まりだけなら `~/ROBO_NEXT/.claude/`。
- `~/.claude/` の汎用のものに ROBO_NEXT の例外や決まりを書き足さない。例外はプロジェクトのルールに書き、汎用のほうには「プロジェクトのルールにも従う」とだけ書く。
- 汎用に戻したもの（adr 系のスキルとフック、エージェント）には、まだ `robo_system/ADR` などの決め打ちが残っている。ほかのプロジェクトで使うときに、プロジェクトの CLAUDE.md から場所を読む形に直す（2026-11-04 時点で未対応）。
- `~/ROBO_NEXT/.claude/` は `.gitignore` で git の管理の外。
- `~/.claude/` はワークスペースの外なので、参照や編集の前にユーザーの承認を得る。`~/.claude/settings.json` と `~/.claude/hooks/` は社内の設定で Read できない（直すにはユーザーの `/add-dir` が要る）。

関連: [[managed-settings-block-user-hooks]]
