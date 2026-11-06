---
name: python-coding-priorities
description: Python を書くときは python-coding スキルに従う。命名規則を厳しく、型ヒントは必須、すべての関数とクラスに目的を明記した docstring
metadata:
  node_type: memory
  type: feedback
  originSessionId: 02b41f30-973c-4d10-b939-fac9081c4ba5
  modified: 2026-11-04T05:08:43.538Z
---

Python のコードを書くとき、直すとき、レビューするときは、`python-coding` スキル（`~/.claude/skills/python-coding/SKILL.md`）に従う。ユーザーが特に重く見ているのは、次の3つ。

- 名前の付け方を厳しく守る。目的は可読性。ユーザーの言う「命名規則」は、特に `~/.claude/rules/python-descriptive-names.md` の冒頭に書いた3つを指す（[[descriptive-names-per-language]]）。次の点も守る。
  - 1つのファイルの中でしか使わない関数と定数の先頭に `_` を付ける（定数は、そのファイルの中に定義する。2026-11-04）。
  - 処理の手順より、文脈の上で大事な意味（値がどこから来たか。例: 別サーバーから HTTP で取得した文は `dequeued_prompts` ではなく `fetched_prompts`）を名前にする。
  - 注意: 情報を足しすぎて名詞や動詞の名前を文にしない（例: `vlm_selected_function` → `selected_function_by_vlm`）。真偽値の名前だけは文でもよい。
- 型ヒントを必ず付ける（`~/.claude/rules/python-type-hints.md`）。
- すべての関数、メソッド、クラスに docstring を書き、その「目的」を明記する（`~/.claude/rules/python-docstrings.md`）。

**Why:** 2026-11-03 にユーザーが「Python コードを書く際は命名規則を厳しく意識して下さい。必ず型ヒントもつけて下さい」「関数には docstring も必須です。…特に目的を明記することが大事」と指示した。

**How to apply:** Python のコードを書き始める前にスキルを開き、書き終えたら「書いたあとの点検」の項目で自分で見直す。決まりの中身は各ルールファイルを正とする。
