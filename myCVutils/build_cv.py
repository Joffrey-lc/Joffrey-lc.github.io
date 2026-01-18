#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CV.md -> index.html
- Only keep 3 sections: 个人简历 / 研究兴趣 / Selected Publications
- Sidebar: remove Print/Copy buttons (only keep optional PDF download)
- Publications: only PDF and BibTeX pills
- No third-party dependencies
"""

from __future__ import annotations
import os
import re
import html
from datetime import datetime
from string import Template
from typing import Dict, List, Tuple, Optional


STYLE = r"""
:root{
  --bg:#f4f6f9;
  --card:#ffffff;
  --text:#1f2937;
  --muted:#6b7280;
  --line:#e5e7eb;
  --primary:#2563eb;
  --primary-weak:#dbeafe;
  --shadow:0 10px 30px rgba(17,24,39,.08);
  --radius:16px;
  --mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  --sans: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans",
          "PingFang SC","Hiragino Sans GB","Microsoft YaHei", sans-serif;
}
*{ box-sizing:border-box; }
body{
  margin:0;
  font-family:var(--sans);
  color:var(--text);
  background: radial-gradient(1200px 500px at 10% 0%, #eef2ff 0%, transparent 60%),
              radial-gradient(1200px 500px at 90% 10%, #ecfeff 0%, transparent 60%),
              var(--bg);
  line-height:1.6;
}
a{ color:var(--primary); text-decoration:none; }
a:hover{ text-decoration:underline; }

.wrap{
  max-width:1100px;
  margin:28px auto;
  padding:0 16px 32px;
  display:grid;
  grid-template-columns: 320px 1fr;
  gap:18px;
  align-items:start;
}
.card{
  background:var(--card);
  border:1px solid var(--line);
  border-radius:var(--radius);
  box-shadow:var(--shadow);
}

/* Sidebar */
.sidebar{
  position:sticky;
  top:18px;
  padding:18px 18px 14px;
}
.profile{
  display:flex;
  gap:14px;
  align-items:center;
  padding-bottom:14px;
  border-bottom:1px solid var(--line);
}
.avatar{
  width:76px; height:76px;
  border-radius:18px;
  background:#ddd;
  overflow:hidden;
  flex:0 0 auto;
  border:1px solid var(--line);
}
.avatar img{ width:100%; height:100%; object-fit:cover; display:block; }
.name{ font-size:20px; font-weight:750; margin:0; line-height:1.2; }
.title{ margin:6px 0 0; color:var(--muted); font-size:13px; }
.tags{ margin-top:10px; display:flex; gap:8px; flex-wrap:wrap; }
.tag{ font-size:12px; padding:4px 10px; border-radius:999px; border:1px solid var(--line); background:#fafafa; color:#334155; }

.contact{
  padding:14px 0;
  border-bottom:1px solid var(--line);
}
.contact .item{
  display:flex; gap:10px; align-items:flex-start;
  padding:7px 0; font-size:14px;
}
.contact .k{ color:var(--muted); width:72px; flex:0 0 auto; }
.contact .v{ word-break:break-word; }

.actions{ padding-top:14px; display:flex; gap:10px; flex-wrap:wrap; }
.btn{
  display:inline-flex; align-items:center; gap:8px;
  padding:9px 12px; border-radius:12px;
  border:1px solid var(--line);
  background:#fff; color:var(--text);
  font-weight:650; font-size:13px;
  cursor:pointer; user-select:none;
}
.btn.primary{ background:var(--primary); border-color:var(--primary); color:#fff; }
.btn:hover{ filter:brightness(.98); }

.hint{ margin:12px 0 0; color:var(--muted); font-size:12px; }

/* Main */
.main{ padding:18px 18px 20px; }
.topbar{
  display:flex; justify-content:space-between; align-items:flex-start; gap:12px;
  padding-bottom:10px; border-bottom:1px solid var(--line); margin-bottom:14px;
}
.topbar h1{ margin:0; font-size:22px; line-height:1.25; }
.topbar .meta{
  text-align:right; color:var(--muted); font-size:12px;
  font-family:var(--mono); white-space:nowrap;
}

section{ padding:14px 0; border-bottom:1px dashed var(--line); }
section:last-child{ border-bottom:none; }
.sec-title{
  display:flex; align-items:center; gap:10px;
  margin:0 0 10px; font-size:15px; font-weight:800;
}
.dot{
  width:10px; height:10px; border-radius:999px;
  background:var(--primary);
  box-shadow:0 0 0 6px var(--primary-weak);
  flex:0 0 auto;
}
.lead{ margin:0; font-size:14px; color:#111827; }
.muted{ color:var(--muted); }

ul{ margin:8px 0 0 18px; padding:0; color:#374151; font-size:13px; }
li{ margin:6px 0; }
p{ margin:8px 0; color:#374151; font-size:13px; }

/* Publications */
.pub{
  display:flex; gap:12px;
  padding:10px 12px;
  border:1px solid var(--line);
  border-radius:14px;
  background:#fff;
  margin-top:10px;
}
.pub .idx{
  font-family:var(--mono);
  color:var(--muted);
  width:28px;
  flex:0 0 auto;
  text-align:right;
  padding-top:2px;
}
.pub .content{ flex:1; min-width:0; }
.pub .ptitle{ margin:0; font-weight:800; color:#111827; font-size:13px; }
.pub .authors{ margin:4px 0 0; font-size:12px; color:#374151; }
.pub .venue{ margin:4px 0 0; font-size:12px; color:var(--muted); }
.links{ margin-top:8px; display:flex; gap:8px; flex-wrap:wrap; }
.pill{
  font-size:12px;
  padding:5px 10px;
  border-radius:999px;
  border:1px solid var(--line);
  background:#fff;
}

.footer{ margin-top:10px; color:var(--muted); font-size:12px; text-align:center; }

@media (max-width: 940px){
  .wrap{ grid-template-columns:1fr; }
  .sidebar{ position:relative; top:auto; }
  .topbar .meta{ text-align:left; white-space:normal; }
}
"""


HTML_DOC = Template("""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>$PAGE_TITLE</title>
  <meta name="description" content="CV" />
  <style>
$STYLE
  </style>
</head>

<body>
  <div class="wrap">
    <aside class="card sidebar">
      <div class="profile">
        <div class="avatar"><img src="$AVATAR" alt="avatar" /></div>
        <div>
          <h2 class="name">$NAME</h2>
          <p class="title">$ROLE</p>
          $TAGS_BLOCK
        </div>
      </div>

      <div class="contact">
$CONTACT_BLOCK
      </div>

      <div class="actions">
$PDF_BTN
      </div>


    </aside>

    <main class="card main">
      <div class="topbar">
        <div>
          <h1>Joffrey's CV</h1>
          <div class="muted">$SUBTITLE</div>
        </div>
        <div class="meta">
          <div>Last updated: $UPDATED</div>
        </div>
      </div>

$SECTIONS

      <div class="footer">© $YEAR $NAME</div>
    </main>
  </div>
</body>
</html>
""")


def parse_front_matter(md_text: str) -> Tuple[Dict[str, object], str]:
    meta: Dict[str, object] = {}
    text = md_text.lstrip("\ufeff")

    if not text.startswith("---"):
        return meta, md_text

    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, flags=re.S)
    if not m:
        return meta, md_text

    fm, body = m.group(1), m.group(2)
    for line in fm.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        key = k.strip().lower()
        val = v.strip().strip('"').strip("'")

        if key == "tags":
            val2 = val.strip()
            if val2.startswith("[") and val2.endswith("]"):
                val2 = val2[1:-1].strip()
            meta[key] = [t.strip() for t in val2.split(",") if t.strip()]
        else:
            meta[key] = val
    return meta, body


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def render_simple_md(md: str) -> str:
    """Only paragraphs + unordered list (- item)."""
    lines = md.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    out: List[str] = []
    in_ul = False

    def close_ul():
        nonlocal in_ul
        if in_ul:
            out.append("</ul>")
            in_ul = False

    for line in lines:
        if not line.strip():
            close_ul()
            continue

        m = re.match(r"^\s*[-*]\s+(.*)$", line)
        if m:
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append("<li>{}</li>".format(esc(m.group(1).strip())))
            continue

        close_ul()
        out.append("<p>{}</p>".format(esc(line.strip())))

    close_ul()
    return "\n".join(out)


def split_sections(md: str) -> Dict[str, str]:
    """Split by '## ' headings."""
    lines = md.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    sections: Dict[str, List[str]] = {}
    cur = None
    for line in lines:
        h = re.match(r"^##\s+(.*)$", line.strip())
        if h:
            cur = h.group(1).strip()
            sections[cur] = []
        else:
            if cur is not None:
                sections[cur].append(line)
    return {k: "\n".join(v).strip() for k, v in sections.items()}


def parse_pub_line(line: str) -> Dict[str, str]:
    """
    Format:
      - Title | Authors(optional) | Venue Year(optional) | PDF: url | BibTeX: url
    """
    s = re.sub(r"^\s*[-*]\s+", "", line.strip())
    parts = [p.strip() for p in s.split("|") if p.strip()]

    title = parts[0] if parts else ""
    authors = ""
    venue_year = ""
    pdf = ""
    bib = ""

    info: List[str] = []
    for p in parts[1:]:
        pl = p.lower()
        if pl.startswith("pdf:"):
            pdf = p.split(":", 1)[1].strip()
        elif pl.startswith("bibtex:") or pl.startswith("bib:"):
            bib = p.split(":", 1)[1].strip()
        else:
            info.append(p)

    if len(info) == 1:
        venue_year = info[0]
    elif len(info) >= 2:
        authors = info[0]
        venue_year = info[1]

    # Split venue/year if possible
    venue = venue_year
    year = ""
    m = re.search(r"(19|20)\d{2}", venue_year)
    if m:
        year = m.group(0)
        venue = venue_year.replace(year, "").strip().strip("-").strip("·").strip()

    return {
        "title": title,
        "authors": authors,
        "venue": venue,
        "year": year,
        "pdf": pdf,
        "bib": bib,
    }


def render_publications(md: str) -> str:
    lines = [ln.strip() for ln in md.split("\n") if ln.strip()]
    pub_lines = [ln for ln in lines if ln.startswith("-") or ln.startswith("*")]

    pubs = [parse_pub_line(ln) for ln in pub_lines]
    blocks: List[str] = []

    for i, p in enumerate(pubs, start=1):
        links = []
        if p["pdf"]:
            links.append('<a class="pill" href="{0}" target="_blank" rel="noopener">PDF</a>'.format(esc(p["pdf"])))
        if p["bib"]:
            links.append('<a class="pill" href="{0}" target="_blank" rel="noopener">BibTeX</a>'.format(esc(p["bib"])))

        venue_text = ""
        if p["venue"] and p["year"]:
            venue_text = "{} · {}".format(p["venue"], p["year"])
        else:
            venue_text = p["venue"] or p["year"] or ""

        blocks.append(
            "\n".join([
                '<div class="pub">',
                '  <div class="idx">[{}]</div>'.format(i),
                '  <div class="content">',
                '    <p class="ptitle">{}</p>'.format(esc(p["title"])),
                ('    <p class="authors">{}</p>'.format(esc(p["authors"])) if p["authors"] else ""),
                ('    <p class="venue">{}</p>'.format(esc(venue_text)) if venue_text else ""),
                ('    <div class="links">{}</div>'.format("".join(links)) if links else ""),
                "  </div>",
                "</div>",
            ])
        )

    return "\n".join(blocks)


def section_html(title: str, inner_html: str) -> str:
    return "\n".join([
        "<section>",
        '<h3 class="sec-title"><span class="dot"></span>{}</h3>'.format(esc(title)),
        inner_html,
        "</section>",
    ])


def main():
    md_path = "CV.md"
    out_path = "index.html"

    if not os.path.exists(md_path):
        raise SystemExit("找不到 CV.md，请确认它与 build_cv.py 在同一目录。")

    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    meta, body = parse_front_matter(md_text)
    secs = split_sections(body)

    # Only keep these 3
    keep = ["个人简历", "研究兴趣", "Selected Publications"]

    sections_out: List[str] = []
    if secs.get("个人简历"):
        sections_out.append(section_html("个人简历", render_simple_md(secs["个人简历"])))
    if secs.get("研究兴趣"):
        sections_out.append(section_html("研究兴趣", render_simple_md(secs["研究兴趣"])))
    if secs.get("Selected Publications"):
        sections_out.append(section_html("Selected Publications", render_publications(secs["Selected Publications"])))

    # meta
    name = str(meta.get("name", "Your Name"))
    role = str(meta.get("role", ""))
    avatar = str(meta.get("avatar", ""))
    email = str(meta.get("email", ""))
    website = str(meta.get("website", ""))
    github = str(meta.get("github", ""))
    location = str(meta.get("location", ""))
    tags = meta.get("tags", [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]
    if not isinstance(tags, list):
        tags = []
    blogurl = str(meta.get("blogurl", ""))
    subtitle = "Personal CV"

    tags_block = ""
    if tags:
        tags_block = '<div class="tags">{}</div>'.format(
            "".join('<span class="tag">{}</span>'.format(esc(t)) for t in tags)
        )

    def contact_row(k: str, v: str, href: Optional[str] = None) -> str:
        if not v.strip():
            return ""
        if href:
            return '<div class="item"><div class="k">{}</div><div class="v"><a href="{}" target="_blank" rel="noopener">{}</a></div></div>'.format(
                esc(k), esc(href), esc(v)
            )
        return '<div class="item"><div class="k">{}</div><div class="v">{}</div></div>'.format(esc(k), esc(v))

    contact_rows = []
    if email:
        contact_rows.append(contact_row("邮箱", email, "mailto:" + email))
    if website:
        contact_rows.append(contact_row("主页", website, website))
    if github:
        show = github.replace("https://", "").replace("http://", "")
        contact_rows.append(contact_row("GitHub", show, github))
    if location:
        contact_rows.append(contact_row("所在地", location))

    contact_block = "\n".join(contact_rows) if contact_rows else ""

    pdf_btn = ""
    if blogurl:
        pdf_btn = '<a class="btn primary" href="{}" target="_blank" rel="noopener">Research Blog</a>'.format(esc(blogurl))

    now = datetime.now()
    out_html = HTML_DOC.substitute(
        PAGE_TITLE=esc(str(meta.get("title", "CV"))),
        STYLE=STYLE.strip("\n"),
        AVATAR=esc(avatar),
        NAME=esc(name),
        ROLE=esc(role),
        TAGS_BLOCK=tags_block,
        CONTACT_BLOCK=contact_block,
        PDF_BTN=pdf_btn,
        SUBTITLE=esc(subtitle),
        UPDATED=now.strftime("%Y-%m-%d"),
        YEAR=str(now.year),
        SECTIONS="\n".join(sections_out),
    )

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(out_html)

    print("✅ 生成成功：{}".format(out_path))


if __name__ == "__main__":
    main()
