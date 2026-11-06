#!/usr/bin/env python3
"""PreToolUse フック: ROBO_NEXT のコードを書き換える前に、ユーザーの確認を挟む。

2026-10-13 から、ROBO_NEXT のコードはユーザーが自分で書く方針である。
Claude がコードを書き換えようとしたら、permissionDecision "ask" を返して、確認画面を出す。
止めるのではなく、確認を挟むだけである。ユーザーが頼んだ変更なら、確認画面で許可すればよい。

社内の設定（allowManagedHooksOnly）で、ユーザーのフックが止められている間は動かない（README.md を参照）。

対象
- Edit / Write / MultiEdit / NotebookEdit で、ROBO_NEXT の中のコードのファイルを書き換えるとき
- Bash のコマンドが、ROBO_NEXT の中のコードのファイルに書き込みそうなとき
  （リダイレクト、tee、sed -i、perl -i、cp、mv、rm、touch、truncate、dd of=）
- Bash の git のコマンドが、ROBO_NEXT の作業ツリーを書き換えそうなとき
  （checkout、switch、restore、reset --hard、stash、merge、rebase、pull など）
Bash の判定は、コマンドの文字列からの推測である。すべての書き込みを見つけられるわけではない。
たとえば python -c の中での書き込みは見つけられない。

手で実行する使い方（code-edit-check スキル）
- ファイルを書き換える前: python3 code_edit_guard.py --file <ファイルの絶対パス>
- Bash のコマンドを実行する前: python3 code_edit_guard.py --command '<コマンド>' --cwd <ディレクトリ>
- 判定の結果を、いつも1行で出力する。
  - 確認が要らないとき: 「確認は要らない」と出力し、終了コード 0 で終わる。
  - 確認が要るとき: 「確認が要る: <理由>」と出力し、終了コード 1 で終わる。
  - 判定できなかったとき: 「判定できなかった: <エラー>」と出力し、終了コード 2 で終わる。
引数がないときは、フックとして動く（標準入力の JSON を読む）。フックとしての振る舞いは、変えていない。
"""
import argparse
import json
import os
import re
import shlex
import sys
from pathlib import Path

GUARDED_ROOTS = [Path.home() / "ROBO_NEXT"]
EXCLUDED_PARTS = {".claude", ".venv", "__pycache__", ".git"}
CODE_SUFFIXES = {
    ".py", ".pyi", ".pyx", ".ipynb", ".sh", ".bash", ".zsh",
    ".js", ".mjs", ".cjs", ".ts", ".tsx", ".c", ".cc", ".cpp", ".cxx", ".h", ".hpp", ".cu", ".rs", ".go",
}
CODE_NAMES = [
    re.compile(r"^Dockerfile"), re.compile(r"^Makefile$"), re.compile(r"^CMakeLists\.txt$"),
    re.compile(r"^(docker-)?compose.*\.ya?ml$"),
]
WRITE_ALL_ARGS = {"rm", "unlink", "truncate", "touch", "shred"}
COPY_LIKE = {"cp", "install", "ln", "rsync"}
WRAPPERS = {"sudo", "env", "nohup", "time", "command", "exec", "nice"}
GIT_WORKTREE = {"checkout", "switch", "restore", "stash", "merge", "rebase", "pull",
                "cherry-pick", "revert", "apply", "am", "clean", "mv", "rm"}
SEPARATORS = {";", "&&", "||", "|", "&", "|&", "(", ")"}
ASSIGN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
HEREDOC = re.compile(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")


def _is_code(p: Path) -> bool:
    return p.suffix.lower() in CODE_SUFFIXES or any(rx.match(p.name) for rx in CODE_NAMES)


def _under_root(p: Path) -> bool:
    try:
        rp = p.resolve()
    except Exception:
        return False
    for root in GUARDED_ROOTS:
        try:
            rel = rp.relative_to(root.resolve())
        except ValueError:
            continue
        return not any(part in EXCLUDED_PARTS for part in rel.parts)
    return False


def _to_path(token: str, cwd: str) -> Path:
    p = Path(os.path.expandvars(os.path.expanduser(token)))
    return p if p.is_absolute() else Path(cwd) / p


def _strip_heredocs(cmd: str) -> str:
    """ヒアドキュメントの中身を除く。中身の > などを、書き込みと取り違えないため。"""
    out, pending = [], []
    for line in cmd.split("\n"):
        if pending:
            if line.strip() == pending[0]:
                pending.pop(0)
            continue
        out.append(line)
        pending.extend(m.group(2) for m in HEREDOC.finditer(line))
    return "\n".join(out)


def _segments(cmd: str):
    """コマンドを、; && || | などで区切った単語の並びに分ける。"""
    cmd = _strip_heredocs(cmd).replace("\\\n", " ")
    for line in cmd.split("\n"):
        if not line.strip():
            continue
        lex = shlex.shlex(line, posix=True, punctuation_chars=True)
        lex.whitespace_split = True
        try:
            tokens = list(lex)
        except ValueError:
            tokens = line.split()
        seg = []
        for t in tokens:
            if t in SEPARATORS:
                if seg:
                    yield seg
                seg = []
            else:
                seg.append(t)
        if seg:
            yield seg


def _is_redirect(t: str) -> bool:
    return bool(t) and set(t) <= set("<>&|") and (">" in t or "<" in t)


def _targets_of(seg, cwd: str, found: list):
    """1つの区切りから、書き込み先の候補を found に足す。"""
    words, i = [], 0
    while i < len(seg):
        t = seg[i]
        if t.isdigit() and i + 1 < len(seg) and _is_redirect(seg[i + 1]):
            i += 1
            continue
        if _is_redirect(t):
            nxt = seg[i + 1] if i + 1 < len(seg) else ""
            # > や >> や &> の行き先は書き込み先。>&1 のような複製と、< の入力は除く。
            if ">" in t and not t.endswith("&") and not (t.startswith(">&") and nxt.isdigit()):
                found.append(("file", _to_path(nxt, cwd)))
            i += 2
            continue
        words.append(t)
        i += 1
    while words and (ASSIGN.match(words[0]) or words[0] in WRAPPERS):
        words = words[1:]
    if not words:
        return
    name, args = os.path.basename(words[0]), words[1:]
    plain = [a for a in args if not a.startswith("-")]

    if name in ("bash", "sh", "zsh") and "-c" in args:
        k = args.index("-c")
        if k + 1 < len(args):
            for inner in _segments(args[k + 1]):
                _targets_of(inner, cwd, found)
        return
    if name == "tee" or name in WRITE_ALL_ARGS:
        found.extend(("file", _to_path(a, cwd)) for a in plain)
    elif name == "sed" and any(re.match(r"^-[A-Za-z]*i", a) or a.startswith("--in-place") for a in args):
        has_script_opt = any(a in ("-e", "-f") or a.startswith("--expression") for a in args)
        files = plain if has_script_opt else plain[1:]
        found.extend(("file", _to_path(a, cwd)) for a in files)
    elif name == "perl" and any(re.match(r"^-[A-Za-z]*i", a) for a in args):
        skip, files = False, []
        for a in args:
            if skip:
                skip = False
                continue
            if a.startswith("-"):
                skip = a.endswith("e") or a.endswith("E")
                continue
            files.append(a)
        found.extend(("file", _to_path(a, cwd)) for a in files)
    elif name in COPY_LIKE or name == "mv":
        if len(plain) >= 2:
            dest = _to_path(plain[-1], cwd)
            sources = [_to_path(a, cwd) for a in plain[:-1]]
            found.append(("file", dest))
            if dest.is_dir():
                found.extend(("file", dest / s.name) for s in sources)
            if name == "mv":
                found.extend(("file", s) for s in sources)
    elif name == "dd":
        found.extend(("file", _to_path(a[3:], cwd)) for a in args if a.startswith("of="))
    elif name == "git":
        repo, k = cwd, 0
        while k < len(args):
            a = args[k]
            if a == "-C" and k + 1 < len(args):
                repo = str(_to_path(args[k + 1], cwd))
                k += 2
            elif a in ("-c", "--git-dir", "--work-tree") and k + 1 < len(args):
                k += 2
            elif a.startswith("-"):
                k += 1
            else:
                break
        if k >= len(args):
            return
        sub, rest = args[k], args[k + 1:]
        changes = sub in GIT_WORKTREE or (sub == "reset" and any(r in ("--hard", "--merge", "--keep") for r in rest))
        if sub == "stash" and rest[:1] and rest[0] in ("list", "show"):
            changes = False
        if changes and _under_root(Path(repo)):
            found.append(("git", f"git {sub}（{repo}）"))


def _decide(data: dict):
    """確認を挟む理由を返す。挟まなくてよければ None。"""
    tool = data.get("tool_name")
    ti = data.get("tool_input") or {}
    cwd = data.get("cwd") or os.getcwd()
    hits = []
    if tool in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
        fp = ti.get("file_path") or ti.get("notebook_path")
        if fp:
            p = _to_path(fp, cwd)
            if _is_code(p) and _under_root(p):
                hits.append(str(p))
    elif tool == "Bash":
        found = []
        for seg in _segments(ti.get("command") or ""):
            _targets_of(seg, cwd, found)
        for kind, x in found:
            if kind == "git":
                hits.append(x)
            elif _is_code(x) and _under_root(x):
                hits.append(str(x))
    if not hits:
        return None
    shown = "、".join(dict.fromkeys(hits[:3]))
    return (f"ROBO_NEXT のコードの変更です（{shown}）。"
            "2026-10-13 から、コードはユーザーが書く方針です。頼んだ変更であれば許可してください。")


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    reason = _decide(data)
    if reason:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": reason,
        }}, ensure_ascii=False))
    return 0


def _parse_args(argv):
    parser = argparse.ArgumentParser(
        description="ROBO_NEXT のコードの変更に、ユーザーの確認が要るかを判定する。")
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--file", help="書き換えるファイルのパス")
    target.add_argument("--command", help="実行する Bash のコマンド")
    parser.add_argument("--cwd", default=os.getcwd(), help="相対パスの基準にするディレクトリ")
    return parser.parse_args(argv)


def _check_from_args(argv) -> int:
    """手で実行したときの判定。結果を、いつも1行で出力する。"""
    args = _parse_args(argv)
    if args.file:
        data = {"tool_name": "Edit", "tool_input": {"file_path": args.file}, "cwd": args.cwd}
    else:
        data = {"tool_name": "Bash", "tool_input": {"command": args.command}, "cwd": args.cwd}
    try:
        reason = _decide(data)
    except Exception as e:
        print(f"判定できなかった: {e}")
        return 2
    if reason:
        print(f"確認が要る: {reason}")
        return 1
    print("確認は要らない")
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 手で実行したとき。判定に失敗したときは、「確認は要らない」と出力しない。
        sys.exit(_check_from_args(sys.argv[1:]))
    try:
        sys.exit(main())
    except Exception:
        # フックの失敗で、作業を止めない。ふだんの権限の確認は、そのまま働く。
        sys.exit(0)
