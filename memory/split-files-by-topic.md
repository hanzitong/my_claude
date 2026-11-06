---
name: split-files-by-topic
description: 文書を作る・直すときは、理由なく別々の話題を1つのファイルにまとめない（言語ごと・話題ごとの既存の分け方に合わせる）
metadata:
  node_type: memory
  type: feedback
  originSessionId: 02b41f30-973c-4d10-b939-fac9081c4ba5
  modified: 2026-11-02T08:58:36.491Z
---

文書（ルール、スキル、エージェント、CLAUDE.md、仕様書、設計書、README など）を作る・直すときは、理由なく別々の話題を1つのファイルにまとめない。共通する内容だけは1つにまとめ、各話題のファイルから参照する。

**Why:** 2026-11-02、Python と C++ の名前のルールを1つのファイル（code-naming.md）にまとめたところ、ユーザーから「コーディングの注意点は言語ごとに分けていたので分けてほしい」と言われた。今後の文書の作成と修正でも大事にしてほしい、と指示された。

**How to apply:** 詳しくは `~/.claude/rules/split-files-by-topic.md`。名前のルールの分け方の例は [[descriptive-names-per-language]]。
