---
name: adr-context
description: robo_system の ADR のうち、状態が「採用」と「提案」のものの一覧を、管理台帳（INDEX.md）から読み込む。robo_system について、アーキテクチャの相談、ADR の作業、仕様書の作業、設計書の作業のどれかを、セッションの中で最初に始めるときに使う。/clear や文脈の圧縮のあとにも使う。社内の設定でフックが動かないため、SessionStart フックの代わりに使う。
---

# ADR の一覧の読み込み（フックの代わり）

本来は、セッションの開始時に、フック（SessionStart）が `~/.claude/hooks/adr_session_context.py` を自動で実行し、一覧を Claude に渡す。しかし、社内の管理設定（`allowManagedHooksOnly`）があるため、ユーザーのフックは動かない。そのため、このスキルで同じことを行う。社内の管理設定が変わってフックが動くようになったら、このスキルは要らなくなる。

## 手順

1. 次のコマンドを、Bash でそのまま実行する。ほかのコマンドとつながない。

   ```bash
   python3 /home/nachi_ai/.claude/hooks/adr_session_context.py /home/nachi_ai/ROBO_NEXT
   ```

2. スクリプトが出力した一覧を、作業の前提にする。

状態が「採用」の ADR と矛盾する提案をするときは、どの ADR を変えることになるかを、あわせて示す。

一覧は、スクリプトを実行した時点のものである。そのあとで、別のセッションが INDEX.md を更新していることがある。そのため、次のことをする前に、`robo_system/ADR/INDEX.md` を Read で読み直す。

- ADR の番号を決める
- 関係する ADR を読む
