---
name: keep-system-description-updated
description: robo_system の新しい情報の書き先。specifications/ の4つの文書（基本仕様書、詳細仕様書、基本設計書、詳細設計書）と ADR に書き分ける。古い情報は残さない
metadata:
  type: project
---

`~/ROBO_NEXT/robo_system/` で、システムに関する新しい情報が出たら、頼まれなくても、次の場所に書き加える。

| 書く内容 | 書く先 |
|---|---|
| 何を満たすべきか（全体）: 目的、機能の一覧、動作環境、前提と制約 | `specifications/01_basic_specification.md`（基本仕様書） |
| どう実現するか（内部の作り）: API、共有するデータ、処理の流れ、関数の一覧、数値 | `specifications/04_detailed_design.md`（詳細設計書） |
| アーキテクチャレベルの決定と、その理由 | `ADR/`（`adr` スキルに従う。新旧と更新の記録は `ADR/INDEX.md`） |
| 実装して分かったこと、試験の記録、計測した値（まだ決定ではないこと） | `docs/implementation/05_implementation_notes.md`（実装の記録。2026-10-16 にユーザーが `docs/implementation/` で管理すると決めた） |

**Why:** 2026-10-07 にユーザーが「逐次、追加情報があったら書き加えるように」と指示した。2026-10-09 に、specifications 内の4ファイル（function_design.md、technical_design.md、system_description.md、system_requirements.md）を、この4つの文書に整理し直すよう指示された。

**How to apply:** プロセス、スレッド、通信方式などの内部の構造は、仕様書に書かない。迷ったら、各文書の冒頭の「この文書について」を読んで書く先を決める。どの文書にも、古い情報を残さない。設計が変わったら新しい内容に書き換え、以前の設計と変えた理由は ADR と管理台帳に残す。実測の結果と懸念点は、基本設計書の付録に、ユーザーがコメントアウトした状態のまま残してある。関連: [[system-specifications-location]], [[robo-system-code-outline-only]]
