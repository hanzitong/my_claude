---
name: robo-system-code-location-branch
description: robo_system のコードは feat/system-design にだけコミットされている。統合ブランチ integrate/sound_and_vlm には作業ツリーへ展開しただけ（2026-10-15、未コミット）
metadata:
  type: project
---

2026-10-15 時点で、robo_system のコード（`src/`、`docker/`、`script/`、`README.md`）は `feat/system-design`（7be45bd）にだけコミットされている。統合用の `integrate/sound_and_vlm` には無かったので、`git archive feat/system-design ... | tar -x` で作業ツリーに展開し、その上に音声の統合（asr と tts）を実装した。コミットもステージもしていない。ADR/ と specifications/ は git の管理外。

**Why:** ブランチの扱い（マージ、コミット）はユーザーが決める。Claude は頼まれていないコミットをしない。

**How to apply:** 作業の前に `git status` と `git log` で、この状態が続いているか確かめる。統合ブランチへ正式に取り込むなら、先に変更を退避（`git stash -u` など）してから `feat/system-design` をマージし、変更を戻す、という順番をユーザーに示す。記録は `robo_system/docs/voice_io_integration_issues.md` の P1。

関連: [[robo-system-run-environment]]
