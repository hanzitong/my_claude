#!/usr/bin/env python3
"""ADR と管理台帳（INDEX.md）の書式を検査する。手で実行することも、フックとして使うこともできる。

手で実行する（いまの使い方）
    python3 ~/ROBO_NEXT/.claude/hooks/adr_lint.py <プロジェクトのディレクトリ>
    問題がなければ終了コード 0、問題があれば 1 を返す。

フックとして使う（社内の設定でユーザーのフックが許されたときの使い方。README.md を参照）
- PostToolUse で、Edit / Write / MultiEdit が robo_system/ADR/ の中のファイルを書き換えたあとに動く
- Bash のコマンドの中に「robo_system/ADR」「ADR-0000 の形の番号」「INDEX.md」のどれかが出てきたあとにも動く
- 問題がなければ、何も出力しない。robo_system/ADR がないプロジェクトでは、何もしない

何を検査するか（adr スキル ~/ROBO_NEXT/.claude/skills/adr/SKILL.md の決まりに合わせている）
- ADR のファイル名、1行目の題名、冒頭の3行（ID、決定日、INDEX.md への案内）
- 見出しの種類と順番: 背景、選択肢、決定、理由、影響と残る課題、確かめ方（確かめ方だけは任意）
- 選択肢が2つ以上あり、採用した方法に「（採用）」が付いている（状態が「提案」なら「（提案）」でもよい）
- ADR のファイルに、状態の行や、「追記」「訂正」の印を書いていない
- 2026-10-16 以降の ADR に、冒頭の要約（1文）と、理由の「確信の度合い」（高、中、低）がある
- INDEX.md の一覧とファイルが1対1で対応し、題名と決定日が一致している
- 状態、関係、更新の記録の種類が、決められた語である
- 「置き換え済み」の ADR には、置き換える側の ADR がある。削除した番号のファイルが残っていない
"""
import json
import os
import re
import sys
from pathlib import Path

ADR_RELDIR = Path("robo_system/ADR")
REQUIRED = ["背景", "選択肢", "決定", "理由", "影響と残る課題"]
ORDER = REQUIRED + ["確かめ方"]
STATUSES = {"提案", "採用", "置き換え済み", "廃止"}
RELATIONS = {"置き換える", "前提にする", "関連する"}
LOG_TYPES = {"新規", "追記", "訂正", "置き換え", "削除"}

FILENAME = re.compile(r"^ADR-(\d{4})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
H1 = re.compile(r"^# (ADR-\d{4}): (.+?)\s*$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ID = re.compile(r"^ADR-\d{4}$")
LINKED_ID = re.compile(r"^\[(ADR-\d{4})\]\(([^)]+)\)$")
MARK = re.compile(r"[【（(\[]\s*(?:追記|訂正)|(?:追記|訂正)\s*[（(]?\s*\d{4}-\d{2}-\d{2}")
STATUS_LINE = re.compile(r"^-\s*状態\s*[:：]")
BASH_HINT = re.compile(r"robo_system/ADR|\bADR-\d{4}|INDEX\.md")
INDEX_LINK_LINE = "- 状態と他の ADR との関係: [INDEX.md](INDEX.md) を参照"
# 要約と確信の度合いは、この日から書く。これより前の ADR には求めない。
NEW_FORMAT_SINCE = "2026-10-16"
FIRST_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
CONFIDENCE_LINE = re.compile(r"^-\s*確信の度合い\s*[:：]\s*(高|中|低)")
MAX_REPORT = 25


def strip_fences(lines):
    """コードブロックの中の行を除いて返す。"""
    out, fence = [], False
    for line in lines:
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if not fence:
            out.append(line)
    return out


def read_tables(text):
    """Markdown の表を、見出しの行をキーにして集める。{(列名, ...): [行, ...]}"""
    tables, rows = {}, []

    def flush():
        if len(rows) >= 2:
            header = tuple(rows[0])
            body = [r for r in rows[2:] if any(c for c in r)]
            tables.setdefault(header, []).extend(body)

    for line in text.splitlines():
        s = line.strip()
        if s.startswith("|") and s.endswith("|"):
            rows.append([c.strip() for c in s[1:-1].split("|")])
        else:
            flush()
            rows = []
    flush()
    return tables


def check_adr_file(path, problems):
    """1つの ADR のファイルを検査し、(番号, 題名, 決定日の値, 選択肢の見出し) を返す。"""
    name = path.name
    m = FILENAME.match(name)
    num = f"ADR-{m.group(1)}" if m else None
    if not m:
        problems.append(f"{name}: ファイル名が「ADR-<4桁の番号>-<英小文字とハイフンの名前>.md」の形ではない")

    lines = path.read_text(encoding="utf-8").splitlines()
    h1 = H1.match(lines[0]) if lines else None
    title = None
    if not h1:
        problems.append(f"{name}: 1行目が「# ADR-0000: 決定の内容」の形ではない")
    else:
        title = h1.group(2)
        if num and h1.group(1) != num:
            problems.append(f"{name}: 1行目の番号 {h1.group(1)} が、ファイル名の番号 {num} と違う")

    head = lines[1:10]
    if num and f"- ID: {num}" not in head:
        problems.append(f"{name}: 冒頭に「- ID: {num}」の行がない")
    date_line = next((l for l in head if l.startswith("- 決定日:")), None)
    date_value = date_line.split(":", 1)[1].strip() if date_line else None
    if not date_line:
        problems.append(f"{name}: 冒頭に「- 決定日: YYYY-MM-DD」の行がない（提案なら「未決定（YYYY-MM-DD に提案）」）")
    if INDEX_LINK_LINE not in head:
        problems.append(f"{name}: 冒頭に「{INDEX_LINK_LINE}」の行がない")
    for l in head:
        if STATUS_LINE.match(l):
            problems.append(f"{name}: 状態の行「{l.strip()}」がある。状態は INDEX.md にだけ書く")

    body = strip_fences(lines)
    headings = [l[3:].strip() for l in body if l.startswith("## ")]
    unknown = [h for h in headings if h not in ORDER]
    if unknown:
        problems.append(f"{name}: 決まっていない見出し {unknown} がある。使える見出しは {ORDER}")
    missing = [h for h in REQUIRED if h not in headings]
    if missing:
        problems.append(f"{name}: 見出し {missing} がない")
    known = [h for h in headings if h in ORDER]
    if len(known) != len(set(known)):
        problems.append(f"{name}: 同じ見出しが2回以上ある")
    elif known != sorted(known, key=ORDER.index):
        problems.append(f"{name}: 見出しの順番が {[h for h in ORDER if h in known]} になっていない")

    options, in_options = [], False
    for l in body:
        if l.startswith("## "):
            in_options = l[3:].strip() == "選択肢"
        elif in_options and l.startswith("### ") and "比較のまとめ" not in l:
            options.append(l[4:].strip())

    if len(options) < 2:
        problems.append(f"{name}: 「選択肢」に、方法が2つ以上ない（見出し ### で数えた）")

    first_date = FIRST_DATE.search(date_value or "")
    if first_date and first_date.group(0) >= NEW_FORMAT_SINCE:
        summary = next((l for l in head if l.startswith("- 要約:")), None)
        if not summary:
            problems.append(f"{name}: 冒頭に「- 要約: 〜」の行がない（{NEW_FORMAT_SINCE} 以降の ADR に必要）")
        elif summary.count("。") > 1:
            problems.append(f"{name}: 要約が2文以上になっている。1文にまとめる")
        in_reason, has_confidence = False, False
        for l in body:
            if l.startswith("## "):
                in_reason = l[3:].strip() == "理由"
            elif in_reason and CONFIDENCE_LINE.match(l):
                has_confidence = True
        if not has_confidence:
            problems.append(f"{name}: 「理由」に「- 確信の度合い: 高、中、低のどれか」の行がない（{NEW_FORMAT_SINCE} 以降の ADR に必要）")

    for l in body:
        if MARK.search(l):
            problems.append(f"{name}: 変更の印らしき「{l.strip()[:40]}」がある。変更の経緯は INDEX.md の更新の記録にだけ書く")
            break
    return num, title, date_value, options


def lint(adr_dir):
    problems = []
    adr_files = {}
    for path in sorted(adr_dir.glob("ADR-*.md")):
        num, title, date_value, options = check_adr_file(path, problems)
        if num:
            adr_files[num] = (path, title, date_value, options)

    index_path = adr_dir / "INDEX.md"
    if not index_path.is_file():
        problems.append("INDEX.md がない。adr スキルの assets/index-template.md をもとに作る")
        return problems
    tables = read_tables(index_path.read_text(encoding="utf-8"))
    listing = tables.get(("ID", "タイトル", "状態", "決定日"), [])
    deleted = tables.get(("ID", "書いてあった内容", "削除した理由"), [])
    relations = tables.get(("元", "関係", "先", "補足"), [])
    log = tables.get(("日付", "ID", "種類", "内容"), [])

    status_of = {}
    for row in listing:
        if len(row) != 4:
            problems.append(f"INDEX.md の一覧: 列の数が4ではない行がある: {row}")
            continue
        cell, title, status, date = row
        m = LINKED_ID.match(cell)
        if not m:
            problems.append(f"INDEX.md の一覧: ID の欄が「[ADR-0000](ファイル名)」の形ではない: {cell}")
            continue
        adr_id, link = m.groups()
        if adr_id in status_of:
            problems.append(f"INDEX.md の一覧: {adr_id} が2回ある")
        status_of[adr_id] = status
        if status not in STATUSES:
            problems.append(f"INDEX.md の一覧: {adr_id} の状態「{status}」は、決められた語 {sorted(STATUSES)} ではない")
        if status == "提案":
            if date != "未決定":
                problems.append(f"INDEX.md の一覧: 提案の {adr_id} の決定日は「未決定」にする（いまは「{date}」）")
        elif not DATE.match(date):
            problems.append(f"INDEX.md の一覧: {adr_id} の決定日「{date}」が YYYY-MM-DD の形ではない")
        if not (adr_dir / link).is_file():
            problems.append(f"INDEX.md の一覧: {adr_id} のリンク先 {link} のファイルがない")
        if adr_id not in adr_files:
            continue
        _path, ftitle, fdate, options = adr_files[adr_id]
        if ftitle and ftitle != title:
            problems.append(f"{adr_id}: INDEX.md の題名と、ADR の1行目の題名が違う")
        if fdate is not None:
            if DATE.match(date) and not fdate.startswith(date):
                problems.append(f"{adr_id}: 決定日が、INDEX.md（{date}）と ADR（{fdate}）で違う")
            if date == "未決定" and not fdate.startswith("未決定"):
                problems.append(f"{adr_id}: INDEX.md では未決定だが、ADR の決定日は「{fdate}」")
        if status != "提案" and not any("（採用）" in o for o in options):
            problems.append(f"{adr_id}: 採用した方法の見出しに「（採用）」がない")

    for adr_id in sorted(set(adr_files) - set(status_of)):
        problems.append(f"{adr_id}: ファイルはあるが、INDEX.md の一覧に行がない")

    deleted_ids = {r[0] for r in deleted if r and ID.match(r[0])}
    for adr_id in sorted(deleted_ids):
        if adr_id in adr_files:
            problems.append(f"{adr_id}: 削除した ADR に載っているが、ファイルが残っている")
        if adr_id in status_of:
            problems.append(f"{adr_id}: 削除した ADR に載っているが、一覧にも残っている")

    replaced = set()
    for row in relations:
        if len(row) != 4:
            problems.append(f"INDEX.md の関係: 列の数が4ではない行がある: {row}")
            continue
        src, rel, dst, _note = row
        if rel not in RELATIONS:
            problems.append(f"INDEX.md の関係: 「{rel}」は、決められた語 {sorted(RELATIONS)} ではない（{src} → {dst}）")
        for x in (src, dst):
            if x not in status_of:
                problems.append(f"INDEX.md の関係: {x} が一覧にない（{src} {rel} {dst}）")
        if rel == "置き換える":
            replaced.add(dst)
            if status_of.get(dst) not in (None, "置き換え済み"):
                problems.append(f"INDEX.md: {src} が {dst} を置き換えるのに、{dst} の状態が「置き換え済み」ではない")
    for adr_id, status in status_of.items():
        if status == "置き換え済み" and adr_id not in replaced:
            problems.append(f"INDEX.md: {adr_id} は「置き換え済み」だが、関係に「置き換える」の行がない")

    logged = set()
    for row in log:
        if len(row) != 4:
            problems.append(f"INDEX.md の更新の記録: 列の数が4ではない行がある: {row}")
            continue
        date, adr_id, kind, _content = row
        logged.add(adr_id)
        if not DATE.match(date):
            problems.append(f"INDEX.md の更新の記録: 日付「{date}」が YYYY-MM-DD の形ではない")
        if kind not in LOG_TYPES:
            problems.append(f"INDEX.md の更新の記録: 種類「{kind}」は、決められた語 {sorted(LOG_TYPES)} ではない")
    for adr_id in sorted(set(status_of) - logged):
        problems.append(f"INDEX.md の更新の記録: {adr_id} の行が1つもない")
    return problems


def is_relevant(data, adr_dir):
    """検査するかどうかと、そのきっかけ（"edit" か "bash"）を返す。"""
    tool = data.get("tool_name")
    tool_input = data.get("tool_input") or {}
    if tool in ("Edit", "Write", "MultiEdit"):
        fp = tool_input.get("file_path")
        if not fp:
            return None
        p = Path(fp)
        if not p.is_absolute():
            p = Path(data.get("cwd") or os.getcwd()) / p
        try:
            p.resolve().relative_to(adr_dir.resolve())
            return "edit"
        except ValueError:
            return None
    if tool == "Bash":
        cwd = Path(data.get("cwd") or os.getcwd())
        inside = str(cwd.resolve()).startswith(str(adr_dir.resolve()))
        if inside or BASH_HINT.search(tool_input.get("command") or ""):
            return "bash"
    return None


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd())
    adr_dir = project / ADR_RELDIR
    if not adr_dir.is_dir():
        return 0
    trigger = is_relevant(data, adr_dir)
    if not trigger:
        return 0
    problems = lint(adr_dir)
    if not problems:
        return 0

    shown = problems[:MAX_REPORT]
    more = len(problems) - len(shown)
    message = "\n".join(
        ["ADR の書式の検査（~/ROBO_NEXT/.claude/hooks/adr_lint.py）で、次の問題が見つかりました。"]
        + [f"- {p}" for p in shown]
        + ([f"- ほかに {more} 件"] if more > 0 else [])
        + [
            "直してください。書いている途中で、このあと直す予定であれば、そのまま続けてください。",
            "ユーザーや別のセッションが書いた箇所であれば、勝手に直さず、ユーザーに伝えてください。",
        ]
    )
    if trigger == "edit":
        out = {"decision": "block", "reason": message}
    else:
        out = {"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": message}}
    print(json.dumps(out, ensure_ascii=False))
    return 0


def run_cli(project_arg) -> int:
    adr_dir = Path(project_arg).expanduser().resolve() / ADR_RELDIR
    if not adr_dir.is_dir():
        print(f"{adr_dir} がありません。")
        return 2
    problems = lint(adr_dir)
    if not problems:
        print("ADR の書式の検査: 問題は見つかりませんでした。")
        return 0
    print("ADR の書式の検査: 次の問題が見つかりました。")
    for p in problems:
        print(f"- {p}")
    return 1


if __name__ == "__main__":
    if len(sys.argv) > 1:
        sys.exit(run_cli(sys.argv[1]))
    try:
        sys.exit(main())
    except Exception:
        # フックの失敗で、作業を止めない。
        sys.exit(0)
