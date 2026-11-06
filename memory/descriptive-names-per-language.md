---
name: descriptive-names-per-language
description: 変数名と関数名は長くてよいので、一語を避けて性質や目的を表す。よい単語は残して「何の」を足す。レビューでも確かめる
metadata:
  node_type: memory
  type: feedback
  originSessionId: 02b41f30-973c-4d10-b939-fac9081c4ba5
  modified: 2026-11-02T09:40:35.000Z
---

変数名と関数名は長くてよいので、一語だけの名前を避け、性質や目的が分かる名前にする。元の単語が的確なら残し、「何の〜か」を前に足す（例: `streak` → `disagreeing_judgment_streak`）。略語は使わない。関数名は動詞と目的語で作る（例: `_care_once` → `_care_for_worker_once`）。ユーザーは「命名は非常に大事」と考えている。コードのレビューでも、名前を確かめて案を添えて指摘する。

**Why:** 2026-11-02 にユーザーが指示した。`streak` を `disagreeing_judgments_in_a_row` に言い換えたときに「streak はよく表していたので、何の streak かを明示してほしかった」と言われた。

**How to apply:** ルールは言語ごとに分けてある。Python は `~/.claude/rules/python-descriptive-names.md`、C++ は `~/.claude/rules/cpp-descriptive-names.md`、レビュー（共通）は `~/.claude/rules/code-review-names.md`。分け方の方針は [[split-files-by-topic]]。
