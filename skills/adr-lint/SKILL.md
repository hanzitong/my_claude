---
name: adr-lint
description: robo_system の ADR と管理台帳（INDEX.md）の書式を、検査のスクリプトで確かめる。ADR や INDEX.md を書いたり直したりしたあとに、必ず使う。社内の設定でフックが動かないため、PostToolUse フックの代わりに使う。
---

# ADR の書式の検査（フックの代わり）

本来は、Claude が ADR を書き換えるたびに、フック（PostToolUse）が `~/.claude/hooks/adr_lint.py` を自動で実行する。しかし、社内の管理設定（`allowManagedHooksOnly`）があるため、ユーザーのフックは動かない。そのため、このスキルで同じ検査を行う。社内の管理設定が変わってフックが動くようになったら、このスキルは要らなくなる。

## 手順

1. 次のコマンドを、Bash でそのまま実行する。ほかのコマンドとつながない。

   ```bash
   python3 /home/nachi_ai/.claude/hooks/adr_lint.py /home/nachi_ai/ROBO_NEXT
   ```

2. 出力を見て、次のように扱う。
   - 「問題は見つかりませんでした」と出たとき: 作業を続ける。
   - 自分が書いた箇所に問題が出たとき: Edit で直し、問題がなくなるまで、手順 1 からやり直す。
   - ユーザーや別のセッションが書いた箇所に問題が出たとき: 直さずに、ユーザーに伝える。

検査の内容は、`~/.claude/hooks/README.md` にある。決まりそのものは、adr スキル（`~/.claude/skills/adr/SKILL.md`）に書いてある。検査と adr スキルが食い違うときは、adr スキルに従う。
