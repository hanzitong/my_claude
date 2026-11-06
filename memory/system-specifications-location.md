---
name: system-specifications-location
description: ロボットシステムの仕様書は ~/ROBO_NEXT/robo_system/specifications/ に書く（ユーザーが書く場所として指定）
metadata:
  type: project
---

ロボットシステムの仕様書は、`~/ROBO_NEXT/robo_system/specifications/` に書く。ユーザーが 2026-10-08 に「システムの仕様書を specifications に書きますので覚えておいて」と伝えた。ディレクトリはユーザーが作成済みで、その時点では空だった。

**Why:** システムの仕様を、ADR（アーキテクチャレベルの決定の記録）や `system_description.md`（全体の説明）とは別の場所にまとめるため。同じ日に、それまでの ADR は「初めての試み」としてすべて消され、`robo_system/ADR/` は空になった。

**How to apply:** システムの仕様を確かめるとき、設計の相談を受けたとき、実装するときは、まず `specifications/` の中を読む。ユーザーが自分で書いた文は、頼まれない限り、勝手に書き換えたり消したりしない。中の4つの文書（基本仕様書、詳細仕様書、基本設計書、詳細設計書）の役割分担は、[[keep-system-description-updated]] にある。文書の間で内容が食い違っていたら、黙ってどちらかに合わせず、ユーザーに伝える。関連: [[keep-system-description-updated]]
