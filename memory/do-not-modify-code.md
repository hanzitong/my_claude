---
name: do-not-modify-code
description: ROBO_NEXT ではコードを変更しない。2026-10-13 のセッション以降、ユーザーが自分でコードを書く
metadata:
  node_type: memory
  type: feedback
  originSessionId: 6ada08a0-fc01-4a4a-8963-a42c532027e5
  modified: 2026-10-13T04:01:19.778Z
---

`~/ROBO_NEXT/` では、コード（`.py` など）を変更しない。読む、解説する、指摘する、提案する、までにとどめる。

**Why:** 2026-10-13 にユーザーが「このセッションからはコードを変更しないで下さい。覚えておいてください」と指示した。その時点で、ユーザーは `robo_system/src/robo_system/` のコードを自分で書き換えていて、その解説を求めていた。

**How to apply:** コードの修正が必要だと思ったら、場所と直し方を文章で伝え、ユーザーに直してもらう。文書（ADR、仕様書、設計書）を変えてよいかは、この指示には含まれていない（Claude の解釈）。迷ったら、変える前に尋ねる。関連: [[robo-system-code-outline-only]], [[no-unrequested-convenience-additions]]
