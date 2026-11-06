---
name: language-japanese-replies-english-code
description: 返答と ADR・文書は日本語、コードの中（コメント、docstring、print）は英語で書く
metadata:
  node_type: memory
  type: feedback
  originSessionId: 286814cd-87de-42d3-bbfb-86128f47bcc2
  modified: 2026-10-29T08:27:18.763Z
---

ユーザーへの返答は日本語で書く。ADR、仕様書、設計書などの文書も日本語で書く。コードの中（コメント、docstring、ログの文字列）は英語で書く。

**Why:** 2026-10-29 に、Claude の返答が途中から英語になったとき、ユーザーが「日本語で良いですよ。コード内は英語のほうが良いですが。ADRは日本語が良いです。」と指示した。

同じ日に、記録したあとでも、返答が英語に戻ったことが2回あり、そのたびにユーザーが指摘した（「私との会話では日本語でお願いします。」）。ツールの出力が英語のとき（ログ、エラー）に、つられて英語になりやすい。

**How to apply:** 会話が長くなっても、ツールの出力が英語でも、返答を英語に切り替えない。ツールを呼ぶ合間の短い説明も、日本語で書く。コードを書くときは、既存のコードに合わせて英語のコメントにする。関連: [[robo-system-code-outline-only]]
