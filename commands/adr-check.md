---
description: ADR と INDEX.md の書式を検査し、仕様書、設計書、実装の記録、コードの外観との食い違いを一覧にする。どれを直すかはユーザーが決める。
disable-model-invocation: true
---

robo_system の ADR と文書の食い違いを調べてください。

1. 書式の検査を実行する: `python3 ~/.claude/hooks/adr_lint.py <プロジェクトのディレクトリ>`
2. design-consistency-checker エージェントに、文書の間の食い違いを調べてもらう。1 の結果も渡す。
3. 1 と 2 の結果を、1つの表にまとめてユーザーに示す。列は、場所、食い違い、根拠、直す先の候補とする。
4. 文書はまだ直さない。どれを直すかを、ユーザーに尋ねる。
