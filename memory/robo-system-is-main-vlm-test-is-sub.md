---
name: robo-system-is-main-vlm-test-is-sub
description: 共通のコードは robo_system に集約し、vlm_test（検証用のサブ）がそれを import する。人手での写しは避ける
metadata:
  node_type: memory
  type: project
  originSessionId: 19b7cc71-3c78-46d8-a237-f3cc68ba589f
  modified: 2026-11-04T09:49:22.953Z
---

robo_system と vlm_test で共通に使うコードは、robo_system に1つだけ置き、vlm_test がそれを import する（2026-11-04、ユーザーの決定。最初の例は `vlm_strategy.py`）。

**Why:** ユーザーの発言。「人手の介入は避けたい」「vlm_test はあくまで検証目的であって主では無く、サブの役割」「robo_system に集約しましょう」。2つの写しを人が揃える形（Claude が勧めた形）は、採用しなかった。

**How to apply:**
- 共通のコードの置き場所を相談されたら、robo_system を元にする案を先に出す。
- vlm_test のコンテナは `vlm_test/` だけをマウントしている。robo_system のコードを読ませるには、vlm_test の compose ファイルに `../../robo_system/src:/robo_system/src:ro` のマウントが要る（4つの compose ファイルに足し済み）。
- robo_system の `vlm_strategy.py` を変えると、vlm_test の検証スクリプトにも影響する。`infer()` の引数を変えるとき（画像の時系列を扱うときなど）は、vlm_test の呼び出し側も確かめる。
- 関連: [[robo-system-code-outline-only]]
