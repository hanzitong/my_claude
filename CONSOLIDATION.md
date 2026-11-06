# 重複した決まりの集約の記録

## この文書について

- 何の記録か: 2026-11-06 に、Claude が `~/my-claude` の中で、内容が全く同じ決まりを1つに集約した記録である。
- `~/my-claude` とは: ユーザーが Claude Code に追加した設定（スキル、エージェント、ルール、フック、自動メモリーなど）を、棚卸しのために写した場所である。元の `~/.claude` と `~/ROBO_NEXT/.claude` は、変えていない。
- 集約のやり方: 同じ決まりが2か所以上にあるとき、Claude は1か所を残し、ほかの場所からその行を消した。残す側は、`rules/`、`claude-md/`、`memory/`、スキル・エージェント・エージェントのメモリーの順で選んだ。
- 「全く同じ」の基準: 決まりの中身（何をするか、しないか、範囲、例外、例）が同じで、違うのは書式、言い回し、frontmatter だけのもの。片方にだけ例、理由、例外、日付があるものは「ほぼ同じ」として、消していない。
- 行番号: 消す前の行番号である。

## 消した行と、残した行

| # | 消した行 | 残した行 | 決まりの中身 |
|---|---|---|---|
| 1 | `skills/python-coding/SKILL.md` L14〜16、`memory/python-coding-priorities.md` L14〜15 | `rules/python-descriptive-names.md` L5〜7 | 命名規則の3つ（動詞を含む変数名、名詞だけの変数名、ファイルの中だけで使う関数の `_`） |
| 2 | `memory/split-files-by-topic.md` L15 の2文 | `rules/split-files-by-topic.md` L6〜7 | 既存の分け方に合わせる。合うファイルがなければ新しく作る |
| 3 | `agents/ja-reviewer.md` L63〜66 | `skills/ja-revise/references/checklist.md` L171〜174 | 修正案の書き方と、「いまの文」の引用の仕方 |
| 4 | `agents/ja-reviewer.md` L79、`agent-memory/ja-reviewer/MEMORY.md` L7 | `skills/ja-revise/SKILL.md` L121〜123 | ja-reviewer はメモリーを読むだけで、書き足すのは ja-revise を使う Claude |
| 5 | `claude-md/ROBO_NEXT-CLAUDE.md` L9、L25、L27、L28 | `rules/vlm-test-measurement.md` L8、`rules/robo-system-docs.md` L9〜11、L14、L31 | vlm_test の役割、仕様書と設計書の書き分け、実装の記録の置き場所、書く先の決め方 |
| 6 | `memory/keep-system-description-updated.md` L13〜14 と L19 の1文 | `claude-md/ROBO_NEXT-CLAUDE.md` の表、`rules/robo-system-docs.md` L10〜11 | 文書の役割（詳細仕様書と基本設計書）、仕様書と設計書の定義 |
| 7 | `memory/robo-system-code-outline-only.md` L8 と L12 の1文目 | `claude-md/ROBO_NEXT-CLAUDE.md` L33、`rules/robo-system-code.md` L19 | コードは外観だけを書く。外観とは何か |
| 8 | `memory/do-not-modify-code.md` L15 の最後の文 | `rules/robo-system-code.md` L15 | 改めて頼まれたら、頼まれた範囲だけ変える |
| 9 | `skills/code-edit-check/SKILL.md` L10 | `rules/robo-system-code.md` L12 | 2026-10-13 から、コードはユーザーが書く |
| 10 | `memory/fix-stale-info-when-found.md` L11、L16、L17 | `rules/robo-system-docs.md` L19〜23 | 古い記述はその場で直す。決められない食い違いは伝える。試験の記録は書き換えない |
| 11 | `memory/managed-settings-block-user-hooks.md` L13 の1文 | `hooks/README.md` L10 | 組織の設定が変わると、登録したフックが動き出す |
| 12 | `agent-memory/robotics-architecture-reviewer/MEMORY.md` L23 | `memory/robo-system-run-environment.md` L8 | 5つのプロセスを1つのコンテナで動かす（ADR-0015） |

## 消さなかった行

- `agent-memory/design-consistency-checker/MEMORY.md` L26「ユーザーと、別のセッションの Claude が、同じ文書を同時に更新している。」
  - 理由: 残す側の `rules/robo-system-docs.md` L33 は「更新していることがある」と書いている。いつも起きることか、ときどき起きることかが違うので、Claude は「ほぼ同じ」と判断した。

## 集約のあとで、Claude が直した行

#1 で行を消したため、「特に次の3つを指す」が指すものがなくなった。Claude は、次の2か所を、残した側を指す文に直した。

- `skills/python-coding/SKILL.md` L13: 「特に次の3つを指す。」→「特に `~/.claude/rules/python-descriptive-names.md` の冒頭に書いた3つを指す。」
- `memory/python-coding-priorities.md` L13: 「特に次の3つを指す（…）。」→「特に `~/.claude/rules/python-descriptive-names.md` の冒頭に書いた3つを指す（…）。次の点も守る。」

## 集約で失われたかもしれない情報

- #5 の vlm_test の役割: 残した `rules/vlm-test-measurement.md` は、`vlm_test/**` を扱うときにだけ読み込まれる。そのため、元の場所に戻して使うと、robo_system の作業中には、この決まりが Claude に届かない。
- #6 の「ユーザーの定義では」という出どころ: 残した側には、ユーザーが定義したことが書かれていない。
