# Python の docstring（すべてのプロジェクトのためのルール）

- すべての関数、メソッド、クラスに、docstring を書く。
  - 理由: 2026-11-03 に、ユーザーが「関数には、docstring も必須です」と指示した。
- docstring には、まず、その関数やクラスの **目的** を書く。目的を明記することが、最も大事である。
  - 目的とは、「なぜ、この関数やクラスがあるのか」「何のためにあるのか」である。
  - 「何をするか」（処理の手順）だけで終わらせない。手順は、コードを読めば分かる。目的は、コードからは分からない。
  - 理由: 2026-11-03 に、ユーザーが「その関数やクラスの“目的”を意識した docstring はとても重要です。特に目的を明記することが大事」と強調した。
- 目的のあとに、必要に応じて、次のことを書く。
  - 引数と戻り値の意味（型ヒントで分かること以上の意味。例: `None` は何を表すか）。
  - 投げる例外。
  - スレッドとの関係（どのスレッドが呼ぶか、共有するデータに触るか）。
- 例（目的が分かる docstring と、分からない docstring）

  ```python
  # 目的が分からない（処理を言い換えているだけ）
  def _update_seat(...) -> tuple[bool, int]:
      '''Take one judgment and return the new values.'''

  # 目的が分かる
  def _update_seat(...) -> tuple[bool, int]:
      '''
      Purpose: change "seated" only after several judgments in a row agree,
      so that one wrong answer of the VLM does not change the system state.
      '''
  ```

- コードのレビューで、docstring のない関数やクラス、目的が書かれていない docstring を見つけたら、ファイル、行、目的の案を添えて指摘する。
