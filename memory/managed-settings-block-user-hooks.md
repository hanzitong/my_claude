---
name: managed-settings-block-user-hooks
description: 社内の管理設定で、ユーザーのフックと、ユーザーの権限ルールが効かない。フックの代わりにルールと手で実行するスクリプトを使う
metadata:
  node_type: memory
  type: project
  originSessionId: 57daed3f-8fde-452a-b3cd-3e8774f04524
  modified: 2026-11-04T09:38:31.230Z
---

社内の管理設定（`~/.claude/remote-settings.json`）で、`allowManagedHooksOnly` と `allowManagedPermissionRulesOnly` が true になっている（2026-10-16 に確認）。ユーザーの `~/.claude/settings.json`、プロジェクトの設定、エージェントやスキルのフロントマターに書いたフックは動かない。ユーザーが書いた権限のルール（allow、ask、deny）も効かない。

**Why:** 2026-10-16 に、ADR 駆動のためのフックを作る計画をユーザーが承認したあと、この設定が見つかった。ユーザーが選んだフックは「ADR の一覧と書式の検査」と「コード変更の確認」で、「cd の禁止」と「認証情報の検出」は選ばなかった。同じ日に、ユーザーが「動かなくても良いので作成しておいて」と言ったので、3つのフックを登録した。2026-11-04 から、ADR の2つのフック（`adr_lint.py`、`adr_session_context.py`）は `~/.claude/hooks/` にあり、`~/.claude/settings.json` に登録したまま。コードのフック（`code_edit_guard.py`）は ROBO_NEXT だけの決まりなので `~/ROBO_NEXT/.claude/hooks/` に移し、`~/ROBO_NEXT/.claude/settings.json` に登録した（[[project-config-in-project-dir]]）。

**How to apply:** 決まった動きを必ず起こしたいときも、ユーザー側のフックや権限のルールを提案しない。代わりに、パス指定のルールや、スキルの手順を使う。フックの代わりのスキルとして、adr-lint、adr-context、code-edit-check を 2026-10-16 に作った。adr-lint と adr-context は `~/.claude/skills/` にあり、`~/.claude/hooks/` のスクリプトを実行する。code-edit-check は `~/ROBO_NEXT/.claude/skills/` にあり、`~/ROBO_NEXT/.claude/hooks/code_edit_guard.py` を実行する。どれも1行のコマンドで実行する。組織の設定が変わったら、このメモを直す。

社内の設定（`blockReadsOutsideWorkingDirectories`）で、`~/.claude/settings.json` と `~/.claude/hooks/` は Read で読めず、Edit も使えない（2026-11-04 に確認）。`~/.claude/rules/`、`~/.claude/skills/`、`~/.claude/agents/` は読める。`~/.claude/hooks/` を直すときは、ユーザーに `/add-dir /home/nachi_ai/.claude/hooks` の入力を頼む。関連: [[project-config-in-project-dir]], [[do-not-modify-code]]
