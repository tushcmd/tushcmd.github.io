"""Tiny build-time syntax highlighter. Standard library only.

highlight(lang, code) returns HTML with <span class="tk-x"> tokens, or the escaped
code unchanged when the language is not supported. Colours live in static/style.css.
"""
import re
from html import escape

ALIAS = {"rs": "rust", "ts": "js", "tsx": "js", "jsx": "js", "javascript": "js", "typescript": "js",
         "mjs": "js", "py": "python", "sh": "bash", "shell": "bash", "zsh": "bash"}

KW = {
    "rust": "as async await break const continue crate dyn else enum extern false fn for if impl in let loop match mod move mut pub ref return self Self static struct super trait true type unsafe use where while",
    "js": "as async await break case catch class const continue debugger default delete do else enum export extends false finally for from function if implements import in instanceof interface let new null of private protected public readonly return static super switch this throw true try type typeof undefined var void while yield",
    "python": "and as assert async await break class continue def del elif else except False finally for from global if import in is lambda None nonlocal not or pass raise return True try while with yield",
    "bash": "if then else elif fi for while do done case esac in function return exit export local source",
    "json": "true false null",
}
NUM = r"\b(?:0x[0-9a-fA-F_]+|\d[\d_]*(?:\.\d+)?(?:[eE][+-]?\d+)?)\b"


def kw(lang):
    return r"\b(?:" + "|".join(KW[lang].split()) + r")\b"


# (css class, regex) in priority order; earlier entries win at the same position.
SPECS = {
    "rust": [("c", r"//[^\n]*|/\*.*?\*/"), ("s", r'b?"(?:\\.|[^"\\])*"'), ("a", r"#!?\[[^\]]*\]"),
             ("t", r"'[a-zA-Z_]\w*\b(?!')"), ("n", NUM), ("k", kw("rust")), ("t", r"\b[A-Z][A-Za-z0-9_]*\b"),
             ("f", r"\b[a-z_][A-Za-z0-9_]*(?=!?\()")],
    "js": [("c", r"//[^\n]*|/\*.*?\*/"), ("s", r'"(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])*\'|`(?:\\.|[^`\\])*`'),
           ("n", NUM), ("k", kw("js")), ("t", r"\b[A-Z]\w*\b"), ("f", r"\b[A-Za-z_$][\w$]*(?=\()")],
    "python": [("c", r"#[^\n]*"), ("s", r'(?:[rbfRBF]{0,2})(?:"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|"(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])*\')'),
               ("a", r"(?m:^[ \t]*@\w[\w.]*)"), ("n", NUM), ("k", kw("python")), ("t", r"\b[A-Z]\w*\b"), ("f", r"\b[A-Za-z_]\w*(?=\()")],
    "bash": [("c", r"(?<![\w$])#[^\n]*"), ("s", r'"(?:\\.|[^"\\])*"|\'[^\']*\''), ("t", r"\$\{?\w+\}?"),
             ("k", kw("bash")), ("a", r"(?<=\s)--?[A-Za-z][\w-]*"), ("n", NUM)],
    "json": [("t", r'"(?:\\.|[^"\\])*"(?=\s*:)'), ("s", r'"(?:\\.|[^"\\])*"'), ("n", NUM), ("k", kw("json"))],
}
_COMPILED = {}


def _compile(lang):
    if lang not in _COMPILED:
        spec = SPECS[lang]
        rx = re.compile("|".join(f"(?P<t{i}>{p})" for i, (_, p) in enumerate(spec)), re.S)
        _COMPILED[lang] = (rx, [c for c, _ in spec])
    return _COMPILED[lang]


def highlight(lang, code):
    lang = ALIAS.get((lang or "").lower(), (lang or "").lower())
    if lang not in SPECS:
        return escape(code, quote=False)
    rx, classes = _compile(lang)
    out, pos = [], 0
    for m in rx.finditer(code):
        if m.start() > pos:
            out.append(escape(code[pos:m.start()], quote=False))
        out.append(f'<span class="tk-{classes[int(m.lastgroup[1:])]}">{escape(m.group(), quote=False)}</span>')
        pos = m.end()
    out.append(escape(code[pos:], quote=False))
    return "".join(out)
