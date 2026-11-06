---
name: fix-stale-info-when-found
description: robo_system の古い記述・間違った情報は、見つけたらその場で直し、直したことを報告する（報告だけで止めない）
metadata:
  node_type: memory
  type: feedback
  originSessionId: 02b41f30-973c-4d10-b939-fac9081c4ba5
  modified: 2026-11-04T09:38:34.791Z
---

**Why:** 2026-11-04 にユーザーが「古い記述は見つけ次第、修正して下さい。特に間違った情報は見つけ次第修正して下さい」と指示した。それまでの「見つけたら報告だけ」を上書きする。

**How to apply:**
- コードは、コメントと docstring だけ。振る舞いは変えない。code-edit-check は変わらず実行する。
- ADR を直したら INDEX に行を足し、adr_lint を実行する。

詳細は `~/ROBO_NEXT/.claude/rules/robo-system-docs.md`（プロジェクトのルール）。関連: [[keep-system-description-updated]]、[[do-not-modify-code]]
