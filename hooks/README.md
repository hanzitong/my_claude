# hooks/

Claude Code のフックに使うスクリプトの置き場所です。

## いまの状態: 登録済みだが、動かない

3つのスクリプトを、`~/ROBO_NEXT/.claude/settings.json` にフックとして登録しています（2026-10-16）。
ただし、社内の管理設定で `allowManagedHooksOnly` が true になっているため、動きません。
この設定があると、組織が配るフックだけが動き、ユーザーの設定に書いたフックは無視されます。
社内の管理設定で `allowManagedHooksOnly` が true でなくなると、登録したフックがそのまま動き出します。

| スクリプト | フックの種類 | 何をするか |
|---|---|---|
| `adr_session_context.py` | SessionStart | 開始時、`/clear` のあと、文脈の圧縮のあとに、状態が「採用」と「提案」の ADR の一覧を Claude に渡す |
| `adr_lint.py` | PostToolUse（Edit、Write、MultiEdit、Bash） | Claude が ADR や INDEX.md を書き換えたあとに、書式を検査し、見つけた問題を Claude に返す |
| `code_edit_guard.py` | PreToolUse（Edit、Write、MultiEdit、NotebookEdit、Bash） | Claude が ROBO_NEXT のコードを書き換えようとしたら、確認画面を出す。書き換えを止めるかは、ユーザーが決める |

ADR のフックは、`robo_system/ADR` がないプロジェクトでは何もしません。
コードのフックは、`~/ROBO_NEXT` の中のコードのファイルだけを対象にします。

## いまの使い方: 手で実行する

```bash
python3 ~/ROBO_NEXT/.claude/hooks/adr_lint.py ~/ROBO_NEXT
python3 ~/ROBO_NEXT/.claude/hooks/adr_session_context.py ~/ROBO_NEXT
python3 ~/ROBO_NEXT/.claude/hooks/code_edit_guard.py --file ~/ROBO_NEXT/robo_system/src/robo_system/vlm_process.py
```

フックの代わりに、Claude が次のスキルに従って、同じスクリプトを実行します。

| スキル | 代わりをするフック | 実行するスクリプト |
|---|---|---|
| `adr-context` | SessionStart | `adr_session_context.py` |
| `adr-lint` | PostToolUse | `adr_lint.py` |
| `code-edit-check` | PreToolUse | `code_edit_guard.py` |

`adr_lint.py` の実行は、adr スキルの「書き終えたあとの確認」の節にも、`/adr-new` と `/adr-check` の手順にも入っています。
Claude がコードを変えない方針は、`~/ROBO_NEXT/.claude/rules/robo-system-code.md` にも書いてあります。
スキルもルールも、Claude が従うことに頼るので、フックほど確実ではありません。

## 検査の内容（adr_lint.py）

adr スキル（`~/ROBO_NEXT/.claude/skills/adr/SKILL.md`）の決まりに合わせています。スキルの決まりを変えたら、このスクリプトも直します。

- ADR のファイル名が、決まった形か
- 1行目の題名が、決まった形か
- 冒頭の行（ID、決定日、INDEX.md への案内）があるか
- 見出しの種類と順番（背景、選択肢、決定、理由、影響と残る課題。確かめ方は任意で、置くときは最後）が、決まりどおりか
- 選択肢が2つ以上あるか
- 採用した方法に「（採用）」が付いているか
  - 例外: 状態が「提案」の ADR では、adr_lint.py はこの点を検査しない。
- ADR のファイルに、状態の行がないか
- ADR のファイルに、「追記」「訂正」の印がないか
- 2026-10-16 以降の ADR に、冒頭の要約（1文）があるか
- 2026-10-16 以降の ADR に、理由の確信の度合い（高、中、低）があるか
- INDEX.md の一覧とファイルが、1対1で対応しているか
- INDEX.md の題名と決定日が、ファイルと一致しているか
- 状態、関係、更新の記録の種類に、決められた語を使っているか
- 「置き換え済み」の ADR に、置き換える側の ADR があるか
- 削除した番号のファイルが、残っていないか

## 確認画面を出す対象（code_edit_guard.py）

- Edit、Write、MultiEdit、NotebookEdit で、ROBO_NEXT の中のコードのファイルを書き換えるとき
- Bash のコマンドが、コードのファイルに書き込みそうなとき（リダイレクト、tee、sed -i、perl -i、cp、mv、rm、touch、truncate、dd）
- Bash の git のコマンドが、作業ツリーを書き換えそうなとき（checkout、switch、restore、reset --hard、stash、merge、rebase、pull など）

コードのファイルは、拡張子が .py、.sh、.ipynb などのものと、Dockerfile、compose の設定です。
`.claude`、`.venv`、`__pycache__`、`.git` の中は対象にしません。
Bash の判定は、コマンドの文字列からの推測です。python -c の中での書き込みなどは、見つけられません。
Claude がコードを変えない方針を、ユーザーがやめるときは、settings.json からこのフックを外します。あわせて、ルール（`~/ROBO_NEXT/.claude/rules/robo-system-code.md`）、code-edit-check スキル、メモリーも直します。

## 参考

- フックの仕組み: https://code.claude.com/docs/en/hooks
- 設定の項目（`allowManagedHooksOnly` など）: https://code.claude.com/docs/en/settings
