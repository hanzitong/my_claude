# スレッド、キュー、HTTP、プロセスでよくある誤解

添削の前に、ユーザーの説明に当てはまるものがないかを見る。
当てはまったら、正しい動きと、その根拠の文書を示す。
この一覧の誤解は、研究で集めたものではない。一覧は、Python などの公式の文書の記述と照らして作ったものである。

| よくある誤解 | 実際の動き | 根拠 |
|---|---|---|
| start() したスレッドが終わってから、次の行に進む | start() はすぐに戻る。そのあと、新しいスレッドは、start() を呼んだスレッドと並行に動く。どちらが先に進むかは決まっていない | threading |
| Lock を取れば、そのデータが守られる | 同じ Lock を取るコードの間でしか、排他されない。Lock を取らずに触るコードがあれば、守られない | threading |
| `x += 1` は1つの命令なので、スレッドの間で安全である | 読む、足す、書く、の途中で、ほかのスレッドに切り替わることがある | 一般的な知識 |
| `queue.get()` は、空なら None を返す | 既定では、要素が来るまで待つ。timeout を付けると、その秒数まで待ち、要素が来なければ queue.Empty が出る。block=False にすると、待たずに queue.Empty が出る | queue |
| `qsize()` や `empty()` で、いまの状態が分かる | おおよその値である。直後の put() や get() が待たない保証はない | queue |
| daemon のスレッドは、プログラムの終了時に、後始末をしてから止まる | 急に止まる。開いたファイルなどの資源が、正しく解放されないことがある | threading |
| `join(timeout)` が戻れば、スレッドは止まっている | timeout が過ぎると、join() は、スレッドが動いていても戻る。join() は常に None を返すので、止まったかは is_alive() で確かめる | threading |
| 子スレッドで例外が起きると、プログラム全体が止まる | 既定では、例外の内容が標準エラーに出るだけで、ほかのスレッドは動き続ける | threading |
| シグナル（Ctrl+C など）は、それを受けたスレッドで処理される | Python のシグナルのハンドラは、常にメインスレッドで動く | signal |
| 別のプロセスとも、グローバル変数を共有できる | プロセスは、メモリが別である。やりとりには、HTTP や、プロセスの間で使えるキュー（multiprocessing.Queue など）の通信が要る | 一般的な知識 |
| `requests.get()` は、相手が返事をしなければ、そのうち諦める | timeout を指定しないと、待ち続ける。timeout は、呼び出し全体の時間の上限ではない | requests |
| クライアントが要求しなくても、HTTP のサーバーが値を送ってくる | 要求と応答の形では、サーバーは要求に応えるだけである | 一般的な知識 |
| FastAPI のエンドポイントは、1つずつ順に動く | def で書いたエンドポイントは、スレッドプールで動く。複数の呼び出しが同時に動き、プログラムが自分で作ったスレッドとも同時に動く | FastAPI |
| `time.time()` の差で、経過時間を正しく測れる | OS や NTP がシステムの時計を合わせ直すと、値が戻ることがある。経過時間は time.monotonic() か time.perf_counter() で測る | time |

## 根拠の文書

- threading: https://docs.python.org/3/library/threading.html
- queue: https://docs.python.org/3/library/queue.html
- signal: https://docs.python.org/3/library/signal.html
- time: https://docs.python.org/3/library/time.html
- requests: https://requests.readthedocs.io/en/latest/user/advanced/#timeouts
- FastAPI: https://fastapi.tiangolo.com/async/
