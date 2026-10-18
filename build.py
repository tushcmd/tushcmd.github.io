#!/usr/bin/env python3
"""Static site builder for tushdev.co. Standard library only.

    python3 build.py                       # writes ./public
    python3 -m http.server -d public 8000  # preview at http://localhost:8000

Content lives in data.py and content/. Nothing in public/ is edited by hand.
Icons live in static/icons/<name>.svg. Replace a file to change an icon.
"""
import hashlib
import json
import re
import shutil
from datetime import date, datetime, timezone
from email.utils import format_datetime
from html import escape as esc
from pathlib import Path

import data
from highlight import highlight

ROOT = Path(__file__).parent
OUT = ROOT / "public"
CONTENT = ROOT / "content"
STATIC = ROOT / "static"
SITE = data.SITE
URL = SITE["url"].rstrip("/")
YEAR = date.today().year
ASSET_V = hashlib.md5(b"".join(p.read_bytes() for p in sorted((Path(__file__).parent / "static").glob("*.[cj]s*")))).hexdigest()[:8]


# ---------- icons ----------

def icon(name):
    path = STATIC / "icons" / f"{name}.svg"
    if not path.exists():
        path = STATIC / "icons" / "link.svg"
    svg = re.sub(r"<\?xml.*?\?>", "", path.read_text(encoding="utf-8")).strip()
    return svg.replace("<svg", '<svg class="ico" aria-hidden="true" focusable="false"', 1)


def arrow(d="ne"):
    """Lucide arrow icon: ne (arrow-up-right, default), e, w or n."""
    name = {"ne": "arrow-up-right", "e": "arrow-right", "w": "arrow-left", "n": "arrow-up"}[d]
    return icon(name).replace('class="ico"', f'class="ico arr arr-{d}"', 1)


# ---------- markdown (the small subset the content uses) ----------

def inline(text):
    t = esc(text, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', t)
    return t


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def code_block(lang, code):
    return (
        '<div class="code"><div class="code-head">'
        f"<span>{esc(lang or 'text')}</span>"
        '<button class="copy" type="button">Copy</button></div>'
        f"<pre><code class=\"hl\">{highlight(lang, code)}</code></pre></div>"
    )


def markdown(text):
    lines = text.strip("\n").split("\n")
    out, i = [], 0
    block_start = re.compile(r"(```|## |> |- )")
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
        elif ln.startswith("```"):
            lang, buf = ln[3:].strip(), []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            out.append(code_block(lang, "\n".join(buf)))
        elif ln.startswith("## "):
            title = ln[3:].strip()
            out.append(f'<h2 id="{slugify(title)}">{inline(title)}</h2>')
            i += 1
        elif ln.startswith("> "):
            buf = []
            while i < len(lines) and lines[i].startswith("> "):
                buf.append(lines[i][2:])
                i += 1
            out.append(f"<blockquote>{inline(' '.join(buf))}</blockquote>")
        elif ln.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(lines[i][2:])
                i += 1
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>")
        else:
            buf = []
            while i < len(lines) and lines[i].strip() and not block_start.match(lines[i]):
                buf.append(lines[i])
                i += 1
            out.append(f"<p>{inline(' '.join(buf))}</p>")
    return "\n".join(out)


def parse_file(path):
    raw = path.read_text(encoding="utf-8")
    _, fm, body = raw.split("---", 2)
    meta = {}
    for line in fm.strip().splitlines():
        key, val = line.split(":", 1)
        meta[key.strip()] = val.strip()
    meta["slug"] = path.stem
    meta["body"] = body
    return meta


def fmt_date(iso):
    d = datetime.strptime(iso, "%Y-%m-%d")
    return f"{d.day} {d:%b %Y}"


# ---------- layout ----------

HEAD_INIT = (
    "<script>(function(){var d=document.documentElement;d.classList.add('js');"
    "try{var t=localStorage.getItem('theme');if(t)d.setAttribute('data-theme',t)}catch(e){}})()</script>"
)


def ext_attrs(href):
    external = href.startswith(("http://", "https://")) or href.endswith(".pdf")
    return ' target="_blank" rel="noopener"' if external else ""


def label_icon(label):
    l = label.lower()
    if any(k in l for k in ("live", "site", "web", "demo")):
        return "globe"
    if any(k in l for k in ("code", "git", "source", "repo")):
        return "github"
    return "link"


def link_item(label, href):
    """Lucide icon, label and arrow, used for project and case-study links."""
    return f'<a href="{href}"{ext_attrs(href)}>{icon(label_icon(label))}<span>{esc(label)}</span>{arrow()}</a>'


def link_html(label, href, ic):
    """Icon, label and an arrow icon, used for profile links in the menu and footer."""
    return f'<a href="{href}"{ext_attrs(href)}>{icon(ic)}<span>{esc(label)}</span>{arrow()}</a>'


def layout(path, title, desc, body, *, active="", article=False, og_type="website", jsonld=None, noindex=False):
    canonical = URL + path
    full_title = title if path == "/" else f"{title} | {SITE['name']}"

    menu_items = ""
    for label, href in data.NAV:
        cur = ' aria-current="page"' if href == active else ""
        menu_items += f'<li><a href="{href}"{cur}><span>{label}</span>{arrow()}</a></li>'
    links = "".join(link_html(label, href, ic) for label, href, ic in data.LINKS)
    menu_links = links
    foot_links = "".join(f"<li>{link_html(label, href, ic)}</li>" for label, href, ic in data.LINKS)
    mail = SITE["email"]
    ld = f'<script type="application/ld+json">{json.dumps(jsonld)}</script>' if jsonld else ""
    robots = '<meta name="robots" content="noindex">' if noindex else ""
    progress = '<div id="progress" aria-hidden="true"></div>' if article else ""

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
{robots}
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{esc(SITE['name'])}">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#0a0a0a">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="alternate" type="application/rss+xml" title="{esc(SITE['name'])} writing" href="/rss.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@75..125,500..900&family=Geist:wght@400;500&family=Geist+Mono:wght@400;500&display=swap">
{HEAD_INIT}
<link rel="stylesheet" href="/assets/style.css?v={ASSET_V}">
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="c bar">
    <a class="home" href="/" aria-label="{esc(SITE['name'])}, home">
      <span class="mark" aria-hidden="true">MD</span>
      <span class="home-text"><span class="home-name">{esc(SITE['name'])}</span><span class="home-sub">Software Engineer</span></span>
    </a>
    <div class="bar-actions">
      <button class="theme" id="theme" type="button" aria-label="Toggle light and dark theme">Theme</button>
      <button class="menu-btn" id="menu-btn" type="button" aria-expanded="false" aria-controls="menu" aria-label="Open menu">
        <span class="burger" aria-hidden="true"><i></i><i></i><i></i></span>
      </button>
    </div>
  </div>
  <nav class="menu" id="menu" aria-label="Main">
    <div class="c menu-in">
      <ol class="menu-list">{menu_items}</ol>
      <div class="menu-links">{menu_links}</div>
    </div>
  </nav>
</header>
{progress}
<main id="main" class="c main">
{body}
</main>
<footer class="c foot-wrap">
  <div class="foot">
    <ul class="foot-links">{foot_links}</ul>
    <div class="foot-meta">
      <span>&copy; {YEAR} {esc(SITE['name'])}. All rights reserved.</span>
      <span class="foot-right"><a href="/rss.xml">RSS</a><a class="top" href="#main"><span>Top</span>{arrow("n")}</a></span>
    </div>
  </div>
</footer>
<script src="/assets/site.js?v={ASSET_V}" defer></script>
</body>
</html>
"""


def points(items):
    if not items:
        return ""
    return '<ul class="pts">' + "".join(f"<li>{esc(x)}</li>" for x in items) + "</ul>"


def row(name, when="", pts=None, stack=None, links=None, href=None, current=False):
    n = esc(name)
    if href:
        n = f'<a href="{href}"{ext_attrs(href)}>{n}{arrow()}</a>'
    when_html = f'<span class="when">{esc(when)}</span>' if when else ""
    stack_html = f'<p class="stack">{"".join(f"<span>{esc(s)}</span>" for s in stack)}</p>' if stack else ""
    links_html = ""
    if links:
        links_html = '<p class="inline-links">' + "".join(link_item(l, h) for l, h in links) + "</p>"
    cls = ' class="now"' if current else ""
    return f'<li{cls}><div class="row"><span class="name">{n}</span>{when_html}{points(pts)}{stack_html}{links_html}</div></li>'


def project_row(p, with_links=False):
    href = f"/projects/{p['slug']}/" if p.get("slug") else None
    return row(p["name"], p.get("when", ""), p["points"], p.get("stack"), p.get("links") if with_links else None, href)


def post_item(p):
    return (
        f'<li><a class="post-link" href="/writing/{p["slug"]}/"><div>'
        f'<h2 class="post-title">{esc(p["title"])}</h2>'
        f'<p class="post-meta"><span>{fmt_date(p["date"])}</span><span>{esc(p["read"])}</span><span>{esc(p["tags"].replace(",", " /"))}</span></p>'
        f'<p class="post-dek">{esc(p["dek"])}</p>'
        f'<span class="post-more"><span>Read post</span>{arrow("e")}</span></div></a></li>'
    )


# ---------- pages ----------

def page_home(posts):
    work = "".join(
        row(w["name"], w.get("when", ""), w["points"], href=w.get("href"), current=w.get("current", False))
        for w in data.WORK
    )
    featured = "".join(project_row(p) for p in data.PROJECTS if p.get("featured"))
    latest = "".join(
        row(p["title"], fmt_date(p["date"]), [p["dek"]], href=f"/writing/{p['slug']}/") for p in posts[:3]
    )
    return f"""
<div class="hero">
  <div class="hero-head">
    <div class="hero-id">
      <p class="tag"><b>/</b> Profile</p>
      <h1>Muturi<br>David.</h1>
      <p class="role">{esc(SITE['role'])}</p>
    </div>
  </div>
  {points(SITE['bio_points'])}
  <p class="chips">
    <span class="chip"><span class="dot" aria-hidden="true"></span><span>Building &amp; shipping</span></span>
    <span class="chip">Exploring: {esc(SITE['exploring'])}</span>
  </p>
</div>
<section aria-labelledby="work"><h2 class="section" id="work">Work</h2><ul class="list">{work}</ul></section>
<section aria-labelledby="projects"><h2 class="section" id="projects">Projects</h2><ul class="list">{featured}</ul><a class="more" href="/projects/"><span>All projects</span>{arrow("e")}</a></section>
<section aria-labelledby="writing"><h2 class="section" id="writing">Writing</h2><ul class="list">{latest}</ul><a class="more" href="/writing/"><span>All writing</span>{arrow("e")}</a></section>
"""


def page_projects():
    rows = "".join(project_row(p, with_links=True) for p in data.PROJECTS)
    return f"""
<div class="page-head">
  <p class="tag"><b>/</b> Projects</p>
  <h1>Projects</h1>
  <p class="lede">Products, tools and experiments across AI, fintech and full-stack engineering. The first two have write-ups.</p>
</div>
<ul class="list">{rows}</ul>
"""


def page_case(c):
    links = "".join(
        link_item(l, h) for l, h in (pair.strip().split("|", 1) for pair in c["links"].split(";"))
    )
    return f"""
<article class="article">
  <a class="back" href="/projects/">{arrow("w")}<span>All projects</span></a>
  <header class="head">
    <p class="tag"><b>/</b> Case study</p>
    <h1 class="title">{esc(c['title'])}</h1>
    <p class="dek">{esc(c['dek'])}</p>
    <dl class="facts">
      <div><dt>Role</dt><dd>{esc(c['role'])}</dd></div>
      <div><dt>Status</dt><dd>{esc(c['status'])}</dd></div>
      <div><dt>Stack</dt><dd>{esc(c['stack'])}</dd></div>
      <div><dt>Links</dt><dd>{links}</dd></div>
    </dl>
  </header>
  <div class="prose">{markdown(c['body'])}</div>
</article>
"""


def page_writing(posts):
    items = "".join(post_item(p) for p in posts)
    return f"""
<div class="page-head">
  <p class="tag"><b>/</b> Writing</p>
  <h1>Writing</h1>
  <p class="lede">Working notes on product engineering, applied AI and lessons from practice.</p>
</div>
<ul class="list">{items}</ul>
"""


def page_post(posts, i):
    p = posts[i]
    parts = []
    aw, ae = arrow("w"), arrow("e")
    if i > 0:
        n = posts[i - 1]
        parts.append(f'<a href="/writing/{n["slug"]}/"><small class="tag">{aw}<span>Newer</span></small><span>{esc(n["title"])}</span></a>')
    if i < len(posts) - 1:
        n = posts[i + 1]
        parts.append(f'<a href="/writing/{n["slug"]}/"><small class="tag"><span>Older</span>{ae}</small><span>{esc(n["title"])}</span></a>')
    nav = f'<nav class="next" aria-label="More writing">{"".join(parts)}</nav>' if parts else ""
    return f"""
<article class="article">
  <a class="back" href="/writing/">{arrow("w")}<span>All writing</span></a>
  <header class="head">
    <div class="meta"><span class="pill">{esc(p['tags'].replace(',', ' /'))}</span><span>{fmt_date(p['date'])}</span><span>{esc(p['read'])}</span></div>
    <h1 class="title">{esc(p['title'])}</h1>
    <p class="dek">{esc(p['dek'])}</p>
    <div class="byline"><span class="mark" aria-hidden="true">MD</span><div>{esc(SITE['name'])}<small>Software engineer, {esc(SITE['location'])}</small></div></div>
  </header>
  <div class="prose">{markdown(p['body'])}</div>
  {nav}
</article>
"""


def page_stack():
    defs = "".join(f"<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k, v in data.STACK)
    learning = "".join(row(x) for x in data.LEARNING)
    return f"""
<div class="page-head">
  <p class="tag"><b>/</b> Stack</p>
  <h1>Stack</h1>
  <p class="lede">What I build with, and what I'm learning next.</p>
</div>
<dl class="defs">{defs}</dl>
<section aria-labelledby="learning"><h2 class="section" id="learning">Learning</h2><ul class="list">{learning}</ul></section>
"""


def page_now():
    defs = "".join(f"<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k, v in data.NOW["items"])
    return f"""
<div class="page-head">
  <p class="tag"><b>/</b> Now</p>
  <h1>Now</h1>
  <p class="lede">What I'm focused on at the moment. Updated {esc(data.NOW['updated'])}.</p>
</div>
<dl class="defs">{defs}</dl>
"""


def page_404():
    return f"""
<div class="nf">
  <p class="tag"><b>404</b> / Not found</p>
  <h1>Lost.</h1>
  <p class="lede">That page does not exist or has moved.</p>
  <a class="more" href="/">{arrow("w")}<span>Back home</span></a>
</div>
"""


# ---------- build ----------

def write(rel, text):
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()

    posts = sorted((parse_file(p) for p in (CONTENT / "posts").glob("*.md")), key=lambda p: p["date"], reverse=True)
    cases = {p.stem: parse_file(p) for p in (CONTENT / "projects").glob("*.md")}

    write("index.html", layout("/", f"{SITE['name']} ({SITE['handle']}), software engineer", SITE["description"], page_home(posts)))
    write("projects/index.html", layout("/projects/", "Projects", "Products, tools and experiments across AI, fintech and full-stack engineering.", page_projects(), active="/projects/"))
    for slug, c in cases.items():
        write(f"projects/{slug}/index.html", layout(f"/projects/{slug}/", c["title"], c["dek"], page_case(c), active="/projects/", article=True))
    write("writing/index.html", layout("/writing/", "Writing", "Working notes on product engineering, applied AI and lessons from practice.", page_writing(posts), active="/writing/"))
    for i, p in enumerate(posts):
        ld = {
            "@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"],
            "description": p["dek"], "datePublished": p["date"], "url": f"{URL}/writing/{p['slug']}/",
            "author": {"@type": "Person", "name": SITE["name"], "url": URL},
        }
        write(f"writing/{p['slug']}/index.html", layout(f"/writing/{p['slug']}/", p["title"], p["dek"], page_post(posts, i), active="/writing/", article=True, og_type="article", jsonld=ld))
    write("stack/index.html", layout("/stack/", "Stack", "The languages, frameworks and infrastructure I build with.", page_stack(), active="/stack/"))
    write("now/index.html", layout("/now/", "Now", "What I'm focused on at the moment.", page_now(), active="/now/"))
    write("404.html", layout("/404.html", "Not found", "Page not found.", page_404(), noindex=True))

    # static assets (icons stay in their own folder so they can be swapped)
    shutil.copytree(STATIC, OUT / "assets")
    shutil.copy(CONTENT / "Muturi_David_Resume.pdf", OUT / "assets" / "Muturi_David_Resume.pdf")

    # sitemap, robots, rss
    today = date.today().isoformat()
    urls = [("/", today), ("/projects/", today), ("/writing/", today), ("/stack/", today), ("/now/", today)]
    urls += [(f"/projects/{s}/", today) for s in cases]
    urls += [(f"/writing/{p['slug']}/", p["date"]) for p in posts]
    sm = "".join(f"<url><loc>{URL}{u}</loc><lastmod>{d}</lastmod></url>" for u, d in urls)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {URL}/sitemap.xml\n")
    items = "".join(
        f"<item><title>{esc(p['title'])}</title><link>{URL}/writing/{p['slug']}/</link>"
        f"<guid>{URL}/writing/{p['slug']}/</guid>"
        f"<pubDate>{format_datetime(datetime.strptime(p['date'], '%Y-%m-%d').replace(tzinfo=timezone.utc))}</pubDate>"
        f"<description>{esc(p['dek'])}</description></item>"
        for p in posts
    )
    write("rss.xml", (
        '<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel>'
        f"<title>{esc(SITE['name'])}: writing</title><link>{URL}/writing/</link>"
        f"<description>{esc(SITE['description'])}</description>{items}</channel></rss>\n"
    ))
    print(f"Built {len(urls) + 1} pages into {OUT}")


if __name__ == "__main__":
    main()
