# Python concepts behind this site

Every example below is taken from `build.py`, `highlight.py` or `data.py`. Read a concept, find it in the file, then change something and rebuild.

## The big idea: data, logic, presentation

- **Data** lives in `data.py` and `content/*.md`.
- **Logic** lives in `build.py` (read the data, decide what to write).
- **Presentation** lives in `static/style.css`.

Keeping these apart means you can edit a project without touching code, and restyle the site without touching content.

## 1. Modules and imports

```python
import json
from pathlib import Path
from html import escape as esc

import data
from highlight import highlight
```

- `import x` loads a module. `from x import y` takes one name from it. `as` renames it (`escape` becomes `esc`).
- Everything above `import data` is the **standard library**, which ships with Python. That is why the project needs no `pip install`.
- `data` and `highlight` are your own files. Any `.py` file next to `build.py` can be imported by its name.

## 2. Paths with `pathlib`

```python
ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
for p in (CONTENT / "posts").glob("*.md"): ...
path.read_text(encoding="utf-8")
p.parent.mkdir(parents=True, exist_ok=True)
```

- `__file__` is the path of the running script, so the build works from any folder.
- `/` joins paths (`ROOT / "content"`), and it works on Windows and Mac alike.
- `.glob("*.md")` finds every markdown file. `.stem` is the name without the extension (`fnewsteer.md` becomes `fnewsteer`), which is used as the page URL.
- `mkdir(parents=True, exist_ok=True)` creates a folder and its parents, and does not fail if it already exists.

## 3. Dictionaries and lists as the site's data

```python
SITE = {"name": "Muturi David", "role": "Full-stack and mobile engineer"}
PROJECTS = [{"name": "FNewsteer", "points": [...], "featured": True}, ...]

SITE["name"]            # must exist, or KeyError
p.get("featured")       # returns None if missing
```

- A **dict** holds named fields. A **list** holds ordered items. A list of dicts is a tiny database.
- `["key"]` is for fields that must exist. `.get("key")` is for optional ones.

## 4. Functions that return HTML strings

```python
def row(name, when="", pts=None, stack=None, links=None, href=None, current=False):
    ...
    return f'<li{cls}><div class="row">...</div></li>'

def layout(path, title, desc, body, *, active="", article=False): ...
```

- Arguments with `=` have **defaults**, so callers pass only what they need.
- The `*` makes everything after it **keyword-only**: you must write `active="/projects/"`, not just `"/projects/"`. That keeps long calls readable.
- Each function takes data and returns a string. They are easy to test because they do nothing else.

## 5. f-strings and templates

```python
f'<a href="{href}">{esc(label)}</a>'

return f"""
<div class="page-head">
  <h1>{esc(title)}</h1>
</div>
"""
```

- `{...}` inside an f-string is a Python expression, evaluated and inserted.
- Triple quotes allow multiple lines, which is how whole page templates are written.
- **Escaping:** `esc()` turns `<` into `&lt;` and so on. Without it, a title containing `<` would break the page, and untrusted text could inject HTML. Escape anything that is text, not markup.

## 6. Comprehensions and generators

```python
"".join(f"<li>{x}</li>" for x in items)
cases = {p.stem: parse_file(p) for p in (CONTENT / "projects").glob("*.md")}
```

- The first is a **generator expression** that produces one string per item, and `"".join(...)` glues them together. This is the loop that turns a list into markup.
- The second is a **dict comprehension**: build a dictionary from a loop in one line.

## 7. Sorting with `key=` and lambdas

```python
posts = sorted(parse_file(p) for p in files, key=lambda p: p["date"], reverse=True)
```

- `key` says what to sort by. `lambda p: p["date"]` is a tiny anonymous function. `reverse=True` puts the newest first.
- ISO dates (`2026-10-17`) sort correctly as plain text, which is why posts use that format.

## 8. Unpacking and `enumerate`

```python
for label, href, ic in data.LINKS: ...
for i, p in enumerate(posts): ...
_, fm, body = raw.split("---", 2)
```

- **Unpacking** splits a tuple or list into named variables.
- `enumerate` gives you the index and the item together, which is used so each post knows its neighbours (newer and older).
- `_` is the convention for a value you do not need.

## 9. String methods

```python
line.split(":", 1)      # split once: "title: A: B" -> ["title", " A: B"]
raw.split("---", 2)     # front matter between the first two ---
text.strip().splitlines()
ln.startswith("## ")
```

These few methods are enough to parse the post format. The `1` and `2` limit how many splits happen, which stops a colon inside a title from breaking things.

## 10. Regular expressions

```python
re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)     # **bold**
re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")       # slugify
```

- A **regex** describes a text pattern. `re.sub(pattern, replacement, text)` replaces every match.
- `( )` is a **capture group**. `\1` in the replacement means "whatever group 1 matched". That is how `**word**` becomes `<strong>word</strong>`.
- `[^*]+` means "one or more characters that are not `*`".
- Prefix patterns with `r"..."` (a raw string) so backslashes are kept as written.
- In `highlight.py`, patterns are joined with `|` into one big regex with **named groups** (`(?P<t0>...)`), and `m.lastgroup` says which group matched. That is how a single pass over the code finds comments, strings, numbers and keywords.

## 11. A tiny parser: loops with an index

```python
i = 0
while i < len(lines):
    ln = lines[i]
    if ln.startswith("```"): ... consume until the closing fence
    elif ln.startswith("## "): ... heading
    elif ln.startswith("- "): ... collect list items
    else: ... paragraph
```

- Walk the lines, look at the current one, decide what block it starts, **consume** the lines that belong to it, and move `i` forward.
- This "look, decide, consume" pattern is the core of most parsers, and the whole markdown reader is about 40 lines.

## 12. Files and folders

```python
shutil.rmtree(OUT)                     # delete the old build
shutil.copytree(STATIC, OUT / "assets")
p.write_text(text, encoding="utf-8")
```

- The build starts from a clean `public/` every time, so a deleted post can never linger.
- Always pass `encoding="utf-8"` when reading and writing text, so accents and symbols survive on every operating system.

## 13. Dates

```python
d = datetime.strptime("2026-10-17", "%Y-%m-%d")   # text -> date
f"{d.day} {d:%b %Y}"                             # date -> "17 Oct 2026"
format_datetime(...)                              # RSS wants a specific format
```

- `strptime` parses text into a date using a pattern. `%b %Y` formats it back.
- RSS needs dates in a fixed format, and the standard library already has a function for it.

## 14. Hashing for cache busting

```python
ASSET_V = hashlib.md5(b"".join(p.read_bytes() for p in sorted(...))).hexdigest()[:8]
```

- A **hash** turns any content into a short fixed-length fingerprint. Change one character in the CSS and the hash changes.
- That fingerprint goes in the URL (`style.css?v=bb10bb9d`), so browsers fetch the new file whenever it changes.
- `read_bytes()` gives raw bytes, and `b""` is an empty bytes literal to join them.

## 15. The entry-point idiom

```python
def main(): ...

if __name__ == "__main__":
    main()
```

- When you run `python3 build.py`, `__name__` is `"__main__"` and the build runs.
- When another file does `import build`, the build does **not** run. That makes the file safe to import and reuse.

## Reading order

1. `data.py` (just dicts and lists).
2. `inline()` and `slugify()` (small regex functions).
3. `markdown()` (the parser loop).
4. `row()` and `project_row()` (functions that return HTML).
5. `layout()` (how pages share a template).
6. `main()` (how everything is written to `public/`).
7. `highlight.py` (regexes with named groups).

## Exercises

1. Add a new entry to `NOW` in `data.py`, rebuild, and find where it appears.
2. Add a `## Heading` and a `- list` to a post and see which function renders each.
3. Add support for `*italic*` in `inline()` with one `re.sub` line.
4. Add a `tags` page that lists every tag from the posts (use a `set` and a loop).
5. Make `fmt_date` print `Oct 17, 2026` instead of `17 Oct 2026`.