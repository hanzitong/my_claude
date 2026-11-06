---
name: robo-system-primitives-file-and-parallel-sessions
description: robo_system の基礎関数は robot_primitives.py と speaker_primitives.py（機器ごと、ADR-0020）が正。別のセッションの Claude も ADR や設計書を更新するので、作業の前に現状を読み直す
metadata:
  node_type: memory
  type: project
  originSessionId: b2479693-5335-429c-b2cb-bbfb5b479b9c
  modified: 2026-11-04T09:31:24.795Z
---

基礎関数を定義した正のファイルは、機器ごとの2つである（2026-11-04、ADR-0020。ユーザーが決めた）。
- `~/ROBO_NEXT/robo_system/src/robo_system/robot_primitives.py`: ロボットの機器のクラスをすべて置く。モックの `NachiRobot`（システムが使う）、組立作業支援デモの `NachiOpenNR`（仮の名前）、コーヒーデモの `NachiCFDsNR`。もとの3つのファイル（`mock_robot_primitives.py`、`opennr_robot_primitives.py`、`robot_primitives_coffee_demo.py`）から移しただけで、クラスの名前とデザインパターンは、ユーザーがあとで決める。
- `~/ROBO_NEXT/robo_system/src/robo_system/speaker_primitives.py`: `Speaker`（tts-api を呼ぶ）と、tts-api の宛先と JSON の形。

機器ごとのシングルトンクラスで、クラス変数 `function_instructions`（VLM に見せる説明書）と `primitive_names`（VLM が呼べるメソッド名）を持つ。仕様書や設計書の基礎関数の一覧は、このファイルに合わせる。

ユーザーは、同じリポジトリで、別のセッションの Claude にも ADR、仕様書、設計書、コードを更新させている。ユーザー自身も、作業の途中でコミットやブランチの切り替えをする。

**Why:** 2026-10-09 にユーザーが「基礎関数を定義したファイルです。これを優先して下さい。別のセッションで claude によって ADR などを更新しているので確認してください」と指示した（当時の名前は mock_robot_primitives_han.py）。それ以前にも、別のセッションが作った ADR と番号が重なったことがある（2026-10-08）。

**How to apply:** `robo_system` で作業を始める前に、`ADR/INDEX.md` の更新の記録、`ADR/` の一覧、`src/robo_system/` の一覧、`git status` と `git log` を読み直す。記憶や、この会話の中の以前の内容を前提にしない。基礎関数のファイルは、頼まれない限り書き換えない。食い違いを見つけたら、このファイルの内容を正として、ほかを合わせる。関連: [[robo-system-code-outline-only]], [[keep-system-description-updated]]
