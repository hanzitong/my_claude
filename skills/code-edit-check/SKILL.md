---
name: code-edit-check
description: ~/ROBO_NEXT の中のコード（.py、.sh、.ipynb、Dockerfile、compose の設定など）を書き換える前や、作業ツリーを変える git の操作の前に、必ず使う。その変更が、ユーザーの確認が要るコードの変更に当たるかを、スクリプトで判定する。社内の設定でフックが動かないため、PreToolUse フックの代わりに使う。
---

# コードを変える前の確認（フックの代わり）

本来は、Claude がコードを書き換える前に、フック（PreToolUse）が `~/ROBO_NEXT/.claude/hooks/code_edit_guard.py` を自動で実行し、確認画面を出す。しかし、社内の管理設定（`allowManagedHooksOnly`）があるため、ユーザーのフックは動かない。そのため、このスキルで同じ判定を行う。社内の管理設定が変わってフックが動くようになったら、このスキルは要らなくなる。

## 手順

1. 書き換えるファイルごとに、次のコマンドを Bash で実行する。`--file` のあとに、そのファイルの絶対パスを書く。

   ```bash
   python3 /home/nachi_ai/ROBO_NEXT/.claude/hooks/code_edit_guard.py --file /home/nachi_ai/ROBO_NEXT/robo_system/src/robo_system/vlm_process.py
   ```

   git の操作のときは、`--command` のあとに、実行しようとしている git のコマンドを書く。`--cwd` のあとには、git を実行するディレクトリを書く。

   ```bash
   python3 /home/nachi_ai/ROBO_NEXT/.claude/hooks/code_edit_guard.py --command 'git checkout main' --cwd /home/nachi_ai/ROBO_NEXT
   ```

2. スクリプトの出力を見て、次のように扱う。
   - 「確認は要らない」と出たとき: そのまま進める。
   - 「確認が要る」と出て、ユーザーがこの会話の中でその変更をはっきり頼んでいるとき: ユーザーに頼まれた範囲だけを変える。
   - 「確認が要る」と出て、ユーザーがこの会話の中でその変更をはっきり頼んでいないとき: ユーザーが望むまでは変えない。どのファイルのどこを、どう直すとよいかを、文章で伝える。ユーザーが望めば、変えてよいかと、変える範囲を、AskUserQuestion で確かめてから変える。
   - それ以外の出力のとき（「判定できなかった」と出たときや、何も出なかったとき）: 確認が要るものとして扱う。
     - 理由: スクリプトが判定に失敗したときに、確認なしでコードを書き換えないためである。

「確認が要る」と出たときは、同じ行に、ユーザーの確認が要る理由も書いてある。
