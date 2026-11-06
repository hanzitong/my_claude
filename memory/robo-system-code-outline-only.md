---
name: robo-system-code-outline-only
description: robo_system のコードは外観だけを書く。関数とスレッド関連の処理の骨組みまでで、詳細実装には進まない
metadata:
  type: feedback
---

**Why:** 2026-10-09 にユーザーが「コードは基本的に全部書き切る必要はないです。むしろ、外観だけ知りたいので具体的な詳細実装には進まないでください。関数と、スレッド関連の処理の外観がわかればよいのです」と指示した。いまはアーキテクチャを検討している段階で、ユーザーが見たいのは構造である。

**How to apply:** カメラの読み出し、エンコード、VLM への問い合わせ、JSON の検証、HTTP の送受信、モック関数の中身などは、`raise NotImplementedError` の関数として置く。動作確認は、import できることと、構造の確認にとどめる。設計は `specifications/03_basic_design.md` と `04_detailed_design.md`、アーキテクチャレベルの決定は `ADR/` に書く。関連: [[no-unrequested-convenience-additions]], [[system-specifications-location]]
