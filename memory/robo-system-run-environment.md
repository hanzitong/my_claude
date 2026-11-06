---
name: robo-system-run-environment
description: robo_system の動かし方。asr → tts → robo_system の順に compose up。robo_system は asr/tts の Docker ネットワークに参加する。ロード約7分。ホストで pkill -f は使わない
metadata:
  type: reference
---

robo_system は、1つの Docker コンテナ `robo_system` の中で5つのプロセスが動く（ADR-0015）。2026-10-15 から、入出力は音声（asr と tts）。

- 起動の順番: `cd asr && docker compose up -d` → `cd tts && docker compose up -d` → `cd robo_system && docker compose -f docker/compose.yaml up -d`。robo_system は外部ネットワーク `asr_default` と `tts-demo-frontend` に参加し、`http://mic-client:8080`（Pull）と `http://tts-api:8000`（/speak）を呼ぶ。
- 止める順番: robo_system → tts → asr（逆だと「Resource is still in use」でネットワークが残る。害は無い）。
- `asr/.env` と `tts/.env` は git の管理外。この PC では音声ソケット `/run/user/1000/pulse`、asr は `ASR_RESULT_MODE=pull`、`MIC_DEVICE=USB_2.0_Camera`（見本の `4` は HDMI の `.monitor` を選んでしまう）。
- 表示: `docker logs -f robo_system`。準備完了は `state: (start) -> 着座待ち`。`[prompt] heard:`、`[speaker] Chat with human:`、`[prompt] mic-client answers`。
- VLM 2つのロードに約7分。asr の文字起こしサーバーはロード約70秒（初回はモデル 4.5GB のダウンロードでヘルスチェックが切れ、mic-client が起動しない。待ってからもう一度 up）。回線は毎秒1MB前後のことがある。
- 人がいない試験: カメラは `ROBO_CAMERA_IMAGE_FILE=<パッケージ内の相対パス>`（画像は `vlm_test/pic/`）。マイクは、PC の音声サーバーに null-sink を作り（tts-demo-api イメージの pactl）、`MIC_DEVICE=robo_test_mic.monitor` にして paplay で実時間に再生する。`--input-wav` は終了時に結果を捨てるので、続けて流すと取りこぼす。試験のあとは元に戻す。
- ホストで `pkill -f <文字列>` を使うと、その文字列を含む自分のシェルも止まる（2026-10-15 にも再発）。PID を調べて kill する。
- `docker compose down` するとコンテナのログも消える。調べたいログは先に `docker logs -f -t robo_system > file` で残す。時刻で絞るときは `-t` の UTC の ISO 時刻で比べる（行頭の JST の 時:分:秒 と文字列比較しない）。
- HF のキャッシュ（`~/.cache/huggingface`）は、ホストからは権限がなく読めない。コンテナの中からは読める。asr のモデルは volume `asr_hf-cache` にある。

関連: [[robo-system-code-outline-only]]、[[robo-system-primitives-file-and-parallel-sessions]]、[[robo-system-code-location-branch]]
