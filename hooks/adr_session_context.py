#!/usr/bin/env python3
"""SessionStart フック: robo_system の ADR の一覧を、セッションの文脈に入れる。

社内の設定でユーザーのフックが許されたときに使う（README.md を参照）。
手で実行すると、同じ一覧を表示する: python3 ~/ROBO_NEXT/.claude/hooks/adr_session_context.py <プロジェクトのディレクトリ>

管理台帳（robo_system/ADR/INDEX.md）の「一覧」の表から、状態が「採用」と「提案」の
ADR を読み、Claude に渡す。セッションの開始時、/clear のあと、文脈の圧縮のあとに動く。
管理台帳がないプロジェクトでは、何もしない。

入力: 標準入力の JSON（Claude Code が渡す）
出力: 標準出力の JSON（hookSpecificOutput.additionalContext）
"""
import json
import os
import re
import sys
from pathlib import Path

INDEX_RELPATH = Path("robo_system/ADR/INDEX.md")

# 「一覧」の表の行: | [ADR-0001](ファイル名) | 題名 | 状態 | 決定日 |
ROW = re.compile(
    r"^\|\s*\[(ADR-\d{4})\]\([^)]*\)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$"
)


def main() -> int:
    cli = len(sys.argv) > 1
    data = {}
    if not cli:
        try:
            data = json.load(sys.stdin)
        except Exception:
            data = {}
    project = Path(sys.argv[1]).expanduser() if cli else Path(
        os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd())
    index = project / INDEX_RELPATH
    if not index.is_file():
        return 0

    by_status = {"採用": [], "提案": []}
    others = 0
    for line in index.read_text(encoding="utf-8").splitlines():
        m = ROW.match(line)
        if not m:
            continue
        adr_id, title, status, _date = m.groups()
        if status in by_status:
            by_status[status].append(f"- {adr_id}: {title}")
        else:
            others += 1

    lines = [f"[ADR の一覧] {INDEX_RELPATH} の「一覧」より（このセッションの開始時点）"]
    for status, items in by_status.items():
        lines.append(f"状態が「{status}」の ADR: {len(items)} 件")
        lines.extend(items)
    if others:
        lines.append(f"状態が「置き換え済み」「廃止」の ADR: {others} 件（題名は INDEX.md を見る）")
    lines += [
        "- アーキテクチャの相談や設計の変更では、提案の前に INDEX.md と関係する ADR を読み、"
        "状態が「採用」の ADR と矛盾しないかを確かめる。",
        "- ADR と INDEX.md を書くとき、直すときは、adr スキルに従う。",
        "- 別のセッションやユーザーが更新していることがある。作業の前に INDEX.md を読み直す。",
    ]

    if cli:
        print("\n".join(lines))
        return 0
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": "\n".join(lines),
        }
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        # フックの失敗で、セッションを止めない。
        sys.exit(0)
