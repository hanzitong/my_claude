# C++ の getter と setter（すべてのプロジェクトのためのルール）

- getter や setter（private なメンバーを読み書きするだけのメソッド）を使っているコードは、見直しが要るものとして扱う。
  - 理由: 2026-11-02 に、ユーザーが「getter, setter を使っている時点で、コードの見直しを必要ということにしましょう。Core Guidelines に従います」と指示した。
- 見直すときは、C++ Core Guidelines に従う。
  - C.131: 中身のない getter と setter は避ける。メンバーに守るべき条件がなければ、メンバーを public にする（`struct` にする）。
  - C.2: メンバーに守るべき条件（不変条件）があるときは `class` にして、メンバーを private にする。メンバーが互いに関係なく変わってよいときは `struct` にする。
- Claude がコードを書くときも、getter と setter を作らない。この項は Claude の解釈であり、ユーザーには確かめていない。
- コードのレビューで getter や setter を見つけたら、ファイル、行、Core Guidelines に沿った直し方の案を添えて指摘する。
- 出典: C++ Core Guidelines https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines
