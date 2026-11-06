---
paths:
  - "robo_system/src/**/*.py"
  - "robo_system/specifications/03_basic_design.md"
  - "robo_system/specifications/04_detailed_design.md"
  - "robo_system/ADR/**"
---

# ロボットのシステムの並行処理、時間、安全（ROBO_NEXT のためのルール）

このルールは、コードの解説、設計の相談、ADR の選択肢の比較で使う事実と観点をまとめたものである。出典は末尾にある。
確かめる観点を示すためのものであり、製品化のための作り込み（エラー処理の細部、テストの充実など）は求めない。

## 並行処理

- FastAPI のエンドポイントは、アプリケーションのコードが作ったスレッドと同時に動き、共有するデータに同時に触れることがある。
  - 理由: def で書いたエンドポイントはフレームワークが管理するスレッドプールで、async def で書いたエンドポイントはイベントループのスレッドで動く。
- def で書いた FastAPI のエンドポイントは、同時に来た要求ごとに、別々のスレッドで同時に動く。
- Lock は、同じ Lock を取るコードの間でしか排他しない。
- Lock を持ったまま、HTTP の呼び出しや推論のような、時間の読めない待ちをしない。
- スレッドを止めるときは、停止の Event を立ててから join する。
  - 理由: daemon のスレッドは、止めないままプログラムが終わると、急に止まり、資源が正しく解放されないことがある。
- join(timeout) のあとは、スレッドが止まったかを is_alive() で確かめる。
  - 理由: join(timeout) は、スレッドが止まったかどうかに関係なく、常に None を返す。
- 周期で回すスレッドは、time.sleep の代わりに Event.wait(周期) で待つと、停止の合図にすぐ気づける。
- 子スレッドの中で捕まえなかった例外は、既定では標準エラーに出るだけで、ほかのスレッドは動き続ける。
- queue.Queue の get() は、既定では、要素が来るまで待つ。
- queue.Queue の qsize()、empty()、full() は、直後の put() や get() が待たずに済むかの判断には使えない。
  - 理由: この3つが返すのは、おおよその値である。
- queue.Queue が maxsize に達すると、put() が待つ。
- queue.Queue が満杯のときに、待つか、断るか、古いものを捨てるかは、ユーザーが設計で決める。
- シグナルのハンドラは、どのスレッドでシグナルを受けても、メインスレッドで動く。
- シグナルのハンドラは、フラグを立てるだけにする。
- requests は、timeout を指定しないと、相手を待ち続ける。
- requests の timeout は、(接続, 読み取り) の組で指定する。
- requests の読み取りの timeout は、サーバーからデータが届かないまま待つ時間の上限である（呼び出し全体にかかる時間の上限ではない）。

## 時間

- 周期、タイムアウト、データの古さは、time.monotonic() で測る。
- time.time() は、ログに残す時刻にだけ使う。
  - 理由: time.time() は、時計の変更で戻ることがある。
- 処理時間は、time.perf_counter() で測る。
- 計測では、平均だけでなく、最大とばらつきを見る。
  - 理由: 実時間のシステムで大事なのは、平均の速さではなく、遅れが決まった範囲に収まること（決定性）である。
- 時間の読めない処理（相手を待つこと、ディスクに書き込むこと、大きなメモリを確保すること）を、周期の処理と同じスレッドに置くと、周期が乱れる。

## データの渡し方を比べる言葉（ROS 2 の QoS の考え方）

| 言葉 | 意味 | この構成の例 |
|---|---|---|
| 最新の値だけ | 古い値は捨ててよい | カメラの画像、監視の結果 |
| 順番を保って全部 | 1つも落とさず、順番も保つ | 基礎関数の依頼、入力の文字列 |
| 寿命（lifespan） | これより古いデータは使わない | 判断に使ってよい画像の古さ |
| 期限（deadline） | 次のデータが来るまでの、最大の間隔 | 画像が更新される間隔 |
| 生存の確かめ（liveliness） | 相手が生きていることを、一定時間ごとに確かめる | 各プロセスの死活 |

## 安全と VLM の出力

- 非常停止をどこが受け持つかを、アーキテクチャの前提として確かめる。
  - 理由: ソフトウェアからの停止は「停止の依頼」であり、非常停止（安全機能）ではない。
- 通信が切れたとき、時間切れになったとき、プロセスが止まったときに、ロボットへの新しい依頼を止める側に倒れる設計かを確かめる。
- VLM の出力は、信頼しない入力として扱う（OWASP LLM05）。
- VLM の出力を受けて基礎関数を実行する側は、基礎関数の名前を、許可の一覧と完全一致で照らす。
- VLM の出力を受けて基礎関数を実行する側は、引数を、型と範囲で検査してから実行する。
- VLM の出力を、eval や exec に渡さない。
- VLM にできることを、最小にする（OWASP LLM06）。
- 使わない基礎関数を、許可の一覧に残さない。
- 許可の判断を VLM に任せず、VLM の出力を受けて基礎関数を実行する側でも行う。
- 影響の大きい動作に人の承認を挟むかを、ユーザーが設計で決める。
- VLM の出力と、実行する側が許可したか却下したかを、記録する。
- 人のそばで動くロボットの安全は、規格（ISO 10218-1/-2:2025 など）と安全の担当者の判断による（このルールは、その代わりにならない）。

## 出典

- FastAPI の def とスレッドプール: https://fastapi.tiangolo.com/async/
- Python の threading: https://docs.python.org/3/library/threading.html
- Python の queue: https://docs.python.org/3/library/queue.html
- Python の signal: https://docs.python.org/3/library/signal.html
- Python の time: https://docs.python.org/3/library/time.html
- requests のタイムアウト: https://requests.readthedocs.io/en/latest/user/advanced/#timeouts
- ROS 2 のリアルタイムの設計: https://design.ros2.org/articles/realtime_background.html
- ROS 2 の QoS: https://docs.ros.org/en/rolling/Concepts/Intermediate/About-Quality-of-Service-Settings.html
- OWASP LLM05: https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/
- OWASP LLM06: https://genai.owasp.org/llmrisk/llm062025-excessive-agency/
