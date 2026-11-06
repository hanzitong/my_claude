---
description: ADR の案や書き換えを、adr-reviewer エージェントでレビューする。指摘を一覧にして示し、どれを直すかはユーザーが決める。
argument-hint: "<ADR の ID。例: ADR-0012。省略すると、状態が提案の ADR>"
disable-model-invocation: true
---

次の ADR をレビューしてください: $ARGUMENTS

1. adr-reviewer エージェントに、対象の ADR のレビューを頼む。ユーザーが対象を指定していなければ、INDEX.md で状態が「提案」の ADR を対象にする。
2. adr-reviewer エージェントが返した指摘を、一覧にしてユーザーに示す。Claude の判断で指摘を削らない。Claude が推した方法への指摘も、そのまま示す。
3. ADR はまだ直さない。どの指摘を直すかを、ユーザーに尋ねる。
