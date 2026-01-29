#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CV.md -> index.html
- Only keep 3 sections: About me\关于 / Research Interests\研究兴趣 / Selected Publications\部分成果
- Sidebar: remove Print/Copy buttons (only keep optional PDF download)
- Publications: PDF / BibTeX / Code pills
- No third-party dependencies
"""

from __future__ import annotations
import os
import re
import html
import json
from datetime import datetime
from string import Template
from urllib.parse import urlparse, parse_qsl, urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from typing import Dict, List, Tuple, Optional


# Keep generated right-pane content fragments in a folder (keeps root tidy)
CONTENT_DIR = "_content"
# Author name to be highlighted in publication author lists (can be set via front matter 'highlight_author')
highlight_author = ""
# Whether to auto-generate local BibTeX files for IEEE URL-only publications
bibtex_autogen = True

# Cache IEEE metadata fetched during autofill so we can sort publications by full date
# without refetching during HTML rendering.
PUB_META_CACHE: Dict[str, Dict[str, str]] = {}

def parse_pubdate_to_tuple(s: str) -> Optional[Tuple[int, int, int]]:
    """Parse IEEE-like publicationDate into (year, month, day).

    Supports:
    - YYYY-MM-DD / YYYY/MM/DD / YYYY.MM.DD
    - '29 December 2025' / '29 Dec 2025'
    - 'December 29, 2025' / 'Dec 29, 2025'
    - 'Early Access' -> None (handled separately)
    """
    if not s:
        return None
    ss = str(s).strip()
    if not ss:
        return None
    if "early access" in ss.lower():
        return None

    # ISO-ish
    m = re.search(r"((?:19|20)\d{2})[./-](\d{1,2})[./-](\d{1,2})", ss)
    if m:
        try:
            y = int(m.group(1))
            mo = int(m.group(2))
            d = int(m.group(3))
            return (y, mo, d)
        except Exception:
            pass

    # Normalize commas and multiple spaces
    ss2 = re.sub(r"\s+", " ", ss.replace(",", " ")).strip()

    fmts = [
        "%d %B %Y",
        "%d %b %Y",
        "%B %d %Y",
        "%b %d %Y",
        "%d %B %Y %H:%M:%S",
        "%d %b %Y %H:%M:%S",
    ]
    for fmt in fmts:
        try:
            dt = datetime.strptime(ss2, fmt)
            return (dt.year, dt.month, dt.day)
        except Exception:
            continue

    # Month + year only (day=0)
    m2 = re.search(r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\b\s+((?:19|20)\d{2})", ss2, flags=re.I)
    if m2:
        try:
            dt = datetime.strptime(m2.group(0).title(), "%B %Y")
            return (dt.year, dt.month, 0)
        except Exception:
            pass

    # Fallback: any year in string
    m3 = re.search(r"(19|20)\d{2}", ss2)
    if m3:
        try:
            return (int(m3.group(0)), 0, 0)
        except Exception:
            pass

    return None
# Put auto-generated BibTeX files here
BIB_DIR = "bibtex"
# Section name to auto-fill (must match your heading)
PUB_SECTION_TITLE = "Selected Publications\部分成果"


def ieee_bibtex_export_url(doc_id: str) -> str:
    """Return an online BibTeX export URL for an IEEE Xplore document id.

    IEEE Xplore's "Download Citations" supports exporting BibTeX using:
      recordIds=<id>&citations-format=citation-only&download-format=download-bibtex
    (See an example captured request payload.)
    """
    doc_id = (doc_id or "").strip()
    if not doc_id:
        return ""
    params = {
        "recordIds": doc_id,
        "citations-format": "citation-only",
        "download-format": "download-bibtex",
    }
    return "https://ieeexplore.ieee.org/xpl/downloadCitations?" + urlencode(params)


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
html{ overflow-y:auto; scrollbar-gutter: stable; }
body{ overflow-y:auto; }
@supports not (scrollbar-gutter: stable){ html{ overflow-y: scroll; } body{ overflow-y: scroll; } }
body{
  margin:0;
  font-family:var(--sans);
  color:var(--text);
  background: radial-gradient(1200px 500px at 10% 0%, #eef2ff 0%, transparent 60%),
              radial-gradient(1200px 500px at 90% 10%, #ecfeff 0%, transparent 60%),
              var(--bg);
  line-height:1.6;
  -webkit-text-size-adjust: 100%;
}

/* Mobile hardening: ensure the CV always fits the screen width on phones/in-app browsers */
html.cv-mobile, html.cv-mobile body{ width:100%; max-width:100%; overflow-x:auto; -webkit-overflow-scrolling:touch; }
html.cv-mobile .wrap{ max-width:100%; margin:12px auto; padding:0 12px 20px; gap:14px; }
html.cv-mobile .sidebar{ position:relative; top:auto; }
html.cv-mobile .navbar{ overflow-x:auto; -webkit-overflow-scrolling:touch; }
html.cv-mobile .navbar::-webkit-scrollbar{ display:none; }
html.cv-mobile .wrap{ grid-template-columns:1fr !important; }
html.cv-mobile .main, html.cv-mobile .sidebar{ width:100%; min-width:0; }
html.cv-mobile .topbar .meta{ text-align:left; white-space:normal; }
html.cv-mobile p, html.cv-mobile li, html.cv-mobile .pub, html.cv-mobile .ext-content{ overflow-wrap:anywhere; word-break:break-word; }
html.cv-mobile .pub{ flex-direction:column; }
html.cv-mobile .pub .idx{ width:auto; text-align:left; padding-top:0; }

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
  display:flex; gap:10px; align-items:center;
  padding:7px 0; font-size:14px;
}
.contact .k{ color:var(--muted); width:72px; flex:0 0 auto; line-height:1.2; }
.contact .v{ flex:1; min-width:0; overflow-wrap:anywhere; }
.contact .v a{
  display:block;
  max-width:100%;
  overflow:hidden;
  text-overflow:ellipsis;
  white-space:nowrap;
}

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

/* WeChat QR */
.wechat{
  margin-top:14px;
  padding:12px 12px 10px;
  border:1px solid var(--line);
  border-radius:14px;
  background: linear-gradient(135deg, rgba(37,99,235,.08), rgba(245,158,11,.10));
}
.wechat .wechat-title{
  display:flex;
  align-items:center;
  gap:8px;
  font-weight:900;
  font-size:13px;
  color:#0f172a;
}
.wechat .wechat-badge{
  font-size:11px;
  font-weight:900;
  padding:2px 8px;
  border-radius:999px;
  border:1px solid rgba(37,99,235,.25);
  background: rgba(37,99,235,.10);
  color:#1e40af;
}
.wechat a{ text-decoration:none; }
.wechat img{
  width:100%;
  max-width:210px;
  display:block;
  margin:10px auto 6px;
  border-radius:14px;
  border:1px solid rgba(37,99,235,.18);
  background:#fff;
  box-shadow:0 12px 26px rgba(17,24,39,.10);
}
.wechat .wechat-name{
  text-align:center;
  font-size:12px;
  font-weight:900;
  color:#0f172a;
  margin-top:2px;
}
.wechat .wechat-hint{
  text-align:center;
  font-size:11px;
  color:var(--muted);
  margin-top:1px;
}

/* Main */
.main{ padding:18px 18px 20px; }

/* Navbar */
.navbar{
  display:flex;
  gap:10px;
  flex-wrap:wrap;
  padding:10px 12px;
  border:1px solid var(--line);
  border-radius:14px;
  background:#fff;
  margin-bottom:14px;
}
.navbar .navlink{
  display:inline-flex;
  align-items:center;
  padding:6px 10px;
  border-radius:999px;
  border:1px solid var(--line);
  background:#fff;
  color:var(--text);
  font-weight:750;
  font-size:13px;
}
.navbar .navlink:hover{
  text-decoration:none;
  filter:brightness(.98);
  border-color: rgba(37,99,235,.35);
  box-shadow:0 0 0 4px var(--primary-weak);
}

.navbar .navlink.active{
  background:var(--primary);
  border-color:var(--primary);
  color:#fff;
  text-decoration:none;
  box-shadow:0 0 0 4px var(--primary-weak);
}

.ext-content{ font-size:13px; color:#374151; }
.ext-content img{ max-width:100%; height:auto; }
.ext-content table{ border-collapse:collapse; max-width:100%; }
.ext-content th,.ext-content td{ border:1px solid var(--line); padding:6px 8px; }
.ext-content code{ font-family:var(--mono); font-size:12px; background:#f3f4f6; padding:2px 4px; border-radius:6px; }

/* Callouts */
.callout{
  margin:12px 0;
  padding:12px 14px;
  border:1px solid var(--line);
  border-left:6px solid var(--primary);
  border-radius:14px;
  background: linear-gradient(90deg, rgba(37,99,235,.12), rgba(16,185,129,.08));
}
.callout .callout-title{
  margin:0 0 6px;
  display:flex;
  align-items:center;
  gap:8px;
  font-weight:900;
  font-size:13px;
  color:#0f172a;
}
.callout .callout-body p{ margin:6px 0; }
.callout .callout-body ul{ margin-top:6px; }
.callout.recruit{
  border-left-color:#f59e0b;
  background: linear-gradient(90deg, rgba(245,158,11,.18), rgba(37,99,235,.08));
}
.callout.success{
  border-left-color:#10b981;
  background: linear-gradient(90deg, rgba(16,185,129,.16), rgba(37,99,235,.06));
}
.callout.warn{
  border-left-color:#ef4444;
  background: linear-gradient(90deg, rgba(239,68,68,.14), rgba(245,158,11,.06));
}
mark.hl{
  padding:1px 4px;
  border-radius:6px;
  background: rgba(245,158,11,.28);
}








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
.pub .meta-line{
  margin:4px 0 0;
  display:flex;
  flex-wrap:wrap;
  gap:8px;
  align-items:center;
  font-size:12px;
  color:#374151;
}
.pub .authors-text{ min-width:0; }
.pub .venue-badge{
  display:inline-flex;
  align-items:center;
  padding:2px 10px;
  border-radius:999px;
  border:1px solid rgba(37,99,235,.25);
  background: linear-gradient(90deg, rgba(37,99,235,.14), rgba(16,185,129,.10));
  color:#0f172a;
  font-weight:800;
}
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


/* Layout lock (keeps layout consistent across pages at the same zoom) */
html.cv-layout-1 .wrap{ grid-template-columns:1fr; }
html.cv-layout-1 .sidebar{ position:relative; top:auto; }
html.cv-layout-1 .topbar .meta{ text-align:left; white-space:normal; }
html.cv-layout-2 .wrap{ grid-template-columns: 320px 1fr; }
html.cv-layout-2 .sidebar{ position:sticky; top:18px; }
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
  <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=0.25, maximum-scale=5, user-scalable=yes, viewport-fit=cover" />

<script>
/* Mobile viewport fix: some host themes/in-app browsers can end up with a desktop-like viewport.
   We force a device-width viewport early and mark the page for mobile CSS hardening. */
(function(){
  var ua = navigator.userAgent || "";
  var isMobile = /Mobi|Android|iPhone|iPad|iPod|Mobile|MicroMessenger/i.test(ua);
  try{
    if (window.matchMedia){
      var hasCoarse = window.matchMedia("(any-pointer: coarse)").matches;
      var hasFine = window.matchMedia("(pointer: fine)").matches;
      if (hasCoarse && !hasFine) isMobile = true;
    }
  }catch(e){}
  if (!isMobile) return;

  var content = "width=device-width, initial-scale=1, minimum-scale=0.25, maximum-scale=5, user-scalable=yes, viewport-fit=cover";
  try{
    var metas = document.querySelectorAll('meta[name="viewport"]');
    for (var i=0;i<metas.length;i++){
      metas[i].setAttribute("content", content);
    }
  }catch(e){}
  try{
    var de = document.documentElement;
    de.classList.add("cv-mobile");
    // Clear any accidental scaling injected elsewhere
    de.style.zoom = "";
    de.style.transform = "";
    de.style.transformOrigin = "";
    de.style.width = "";
  }catch(e){}
})();
</script>
  <title>$PAGE_TITLE</title>
  <meta name="description" content="CV" />
  <!-- CV_SHELL_GENERATED -->
  <style>
$STYLE
  </style>
<script>
(function(){
  var PREFIX = "CV_ZOOM=";
  var KEY_ZOOM = "cv_zoom_desired";
  var KEY_LAYOUT = "cv_layout_mode";
  var LAYOUT_BREAKPOINT = 940;

  // --- Mobile safeguard ---
  // Mobile/touch browsers manage pinch-zoom/viewport scaling themselves.
  // This DPR-based zoom helper can make the first render look over-zoomed on mobile.
  // To keep mobile always "fit-to-screen", we disable it on mobile/touch devices.
  // Desktop behavior (including remembered zoom across navbar pages) is unchanged.
  var mq = window.matchMedia ? window.matchMedia.bind(window) : null;
  var hasFine = false, hasCoarse = false;
  try{
    if (mq){
      hasFine = mq("(pointer: fine)").matches;
      hasCoarse = mq("(any-pointer: coarse)").matches;
    }
  }catch(e){}
  var ua = (navigator.userAgent || "");
  var uaMobile = /Mobi|Android|iPhone|iPad|iPod/i.test(ua);
  var isMobile = (hasCoarse && !hasFine) || uaMobile;
  if (isMobile){
    // Avoid carrying a desktop-stored zoom value into mobile rendering.
    try{ if (window.name && window.name.indexOf(PREFIX) === 0) window.name = ""; }catch(e){}
    try{ sessionStorage.removeItem(KEY_ZOOM); sessionStorage.removeItem(KEY_LAYOUT); }catch(e){}
    return;
  }

  function ssGet(key){
    try{ return sessionStorage.getItem(key); }catch(e){}
    return null;
  }
  function ssSet(key, val){
    try{ sessionStorage.setItem(key, String(val)); }catch(e){}
  }

  function parseDesiredFromName(){
    try{
      if (window.name && window.name.indexOf(PREFIX) === 0){
        var v = parseFloat(window.name.slice(PREFIX.length));
        if (isFinite(v) && v > 0) return v;
      }
    }catch(e){}
    return null;
  }

  function readDesired(){
    var v = ssGet(KEY_ZOOM);
    if (v != null){
      var n = parseFloat(v);
      if (isFinite(n) && n > 0) return n;
    }
    return parseDesiredFromName();
  }

  function saveDesired(){
    ssSet(KEY_ZOOM, desired);
    // Keep legacy behavior if window.name is already used for CV_ZOOM.
    // Avoid overwriting other pages' window.name payloads in the same tab.
    try{
      if (!window.name || window.name.indexOf(PREFIX) === 0){
        window.name = PREFIX + String(desired);
      }
    }catch(e){}
  }

  function round6(x){
    return Math.round(x * 1000000) / 1000000;
  }

  var lastDpr = window.devicePixelRatio || 1;
  var desired = readDesired();
  if (!desired) desired = lastDpr;

  function applyZoom(){
    var cur = window.devicePixelRatio || 1;
    if (!cur) cur = 1;
    var factor = desired / cur;
    factor = round6(factor);
    if (isFinite(factor) && factor > 0.1 && factor < 10){
      var de = document.documentElement;
      if ('zoom' in de.style){
        de.style.zoom = factor;
      }else{
        de.style.transformOrigin = '0 0';
        de.style.transform = 'scale(' + factor + ')';
        de.style.width = (100 / factor) + '%';
      }
    }
  }

  // --- Layout lock ---
  function computeLayoutMode(){
    // Use clientWidth to reduce sensitivity to scrollbars.
    var w = document.documentElement.clientWidth || window.innerWidth || 0;
    return (w <= LAYOUT_BREAKPOINT) ? '1' : '2';
  }

  function applyLayoutMode(mode){
    var html = document.documentElement;
    html.classList.remove('cv-layout-1', 'cv-layout-2');
    if (mode === '1') html.classList.add('cv-layout-1');
    else html.classList.add('cv-layout-2');
    ssSet(KEY_LAYOUT, mode);
  }

  var storedLayout = ssGet(KEY_LAYOUT);
  if (storedLayout !== '1' && storedLayout !== '2') storedLayout = null;
  var layoutMode = storedLayout || computeLayoutMode();
  applyLayoutMode(layoutMode);

  var lastW = document.documentElement.clientWidth || window.innerWidth || 0;

  // Apply ASAP
  applyZoom();

  // If user changes browser zoom (devicePixelRatio changes), adopt it and avoid double scaling.
  window.addEventListener('resize', function(){
    var dpr = window.devicePixelRatio || 1;
    var w = document.documentElement.clientWidth || window.innerWidth || 0;

    // 1) Keep original zoom persistence behavior based on DPR changes
    if (Math.abs(dpr - lastDpr) > 0.001){
      desired = dpr;
      lastDpr = dpr;
      applyZoom();
      saveDesired();
      // DPR change likely alters effective width => recompute layout mode
      applyLayoutMode(computeLayoutMode());
      lastW = w;
      return;
    }

    // 2) Window resize (user resizing) can change layout; ignore tiny width changes
    if (Math.abs(w - lastW) > 60){
      lastW = w;
      applyLayoutMode(computeLayoutMode());
    }
  });

  window.addEventListener('pagehide', function(){
    saveDesired();
  });
  window.addEventListener('beforeunload', function(){
    saveDesired();
  });
})();
</script>
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
          $BANNER_BLOCK
        </div>
      </div>

      <div class="contact">
$CONTACT_BLOCK
      </div>

$WECHAT_BLOCK

      <div class="actions">
$PDF_BTN
      </div>


    </aside>

    <main class="card main">
$NAVBAR
      <div class="topbar">
        <div>
          <h1></h1>
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
    """Parse a small subset of YAML front matter.

    Supported:
      - key: value (single line)
      - tags: [a, b, c]
      - nav/nav_items/navbar: JSON array (single-line OR multi-line between [ ... ])

    (We keep it dependency-free: no PyYAML.)
    """

    meta: Dict[str, object] = {}
    text = md_text.lstrip("\ufeff")

    if not text.startswith("---"):
        return meta, md_text

    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, flags=re.S)
    if not m:
        return meta, md_text

    fm, body = m.group(1), m.group(2)
    lines = fm.splitlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith("#") or ":" not in line:
            i += 1
            continue

        k, v = line.split(":", 1)
        key = k.strip().lower()

        # For most scalar keys, keep the old behavior: strip outer quotes
        val = v.strip().strip('"').strip("'")

        if key in ("tags", "cv_tags"):
            val2 = val.strip()
            if val2.startswith("[") and val2.endswith("]"):
                val2 = val2[1:-1].strip()
            meta[key] = [t.strip() for t in val2.split(",") if t.strip()]
            i += 1
            continue

        if key in ("nav", "navbar", "nav_items"):
            # Allow:
            #   nav: [{...},{...}]
            # as well as multi-line:
            #   nav: [
            #     {...},
            #     {...}
            #   ]
            raw = v.strip()  # IMPORTANT: don't strip quotes here; keep valid JSON as-is

            if raw.startswith("[") and not raw.rstrip().endswith("]"):
                buf = [raw]
                balance = raw.count("[") - raw.count("]")
                i += 1
                while i < len(lines) and balance > 0:
                    ln = lines[i].strip()
                    buf.append(ln)
                    balance += ln.count("[") - ln.count("]")
                    i += 1
                raw = "\n".join(buf)
            else:
                i += 1

            try:
                parsed = json.loads(raw)
                meta[key] = parsed if isinstance(parsed, list) else []
            except Exception:
                meta[key] = []
            continue

        meta[key] = val
        i += 1

    return meta, body


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


_ALLOWED_URL_SCHEMES = {"http", "https", "mailto"}


def sanitize_url(u: str) -> str:
    """Return a safe URL for href, or "" if it should not be linked.

    Conservative allowlist to avoid `javascript:` / `data:` etc.
    """
    u = (u or "").strip()
    if not u:
        return ""

    # Strip common wrappers
    if u.startswith("<") and u.endswith(">"):
        u = u[1:-1].strip()
    u = u.strip().strip('"').strip("'")

    # Basic whitespace check (href cannot contain spaces safely)
    if re.search(r"\s", u):
        # Markdown links may include an optional title: (url "title").
        # In that case, keep only the first token as URL.
        u = u.split()[0].strip()
        if not u or re.search(r"\s", u):
            return ""

    p = urlparse(u)
    if p.scheme:
        if p.scheme.lower() in _ALLOWED_URL_SCHEMES:
            return u
        return ""

    # Relative / in-page links
    if u.startswith(("/", "./", "../", "#")):
        return u

    # If someone writes [text](example.com) (no scheme), treat it as https.
    if re.match(r"^[A-Za-z0-9.-]+\.[A-Za-z]{2,}(/.*)?$", u):
        return "https://" + u

    return ""


def md_inline_to_html(text: str) -> str:
    """Inline markdown (safe).

    Supported:
      - `[label](url)` links
      - bare http(s) URLs
      - `code` (backticks)
      - `**bold**` / `__bold__`
      - `==highlight==`

    Everything else is HTML-escaped.
    """
    s = text or ""
    if not s:
        return ""

    token_map = {}
    token_i = 0

    def _new_token(html_snip: str) -> str:
        nonlocal token_i
        token_i += 1
        tok = f"@@CVTOK{token_i}@@"
        token_map[tok] = html_snip
        return tok

    # 0) Inline code (protect first)
    code_pat = re.compile(r"`([^`\n]+)`")

    def _code_repl(m: re.Match) -> str:
        inner = m.group(1)
        return _new_token(f"<code>{html.escape(inner, quote=True)}</code>")

    s0 = code_pat.sub(_code_repl, s)

    # 1) Markdown links: [label](url)
    link_pat = re.compile(r"(?<!!)\[(?P<label>[^\]\n]+)\]\((?P<url>[^\)\n]+)\)")

    def _link_repl(m: re.Match) -> str:
        label = (m.group("label") or "").strip()
        raw = (m.group("url") or "").strip()
        url = raw.split()[0].strip() if raw else ""
        safe = sanitize_url(url)
        if not (label and safe):
            return m.group(0)
        href = html.escape(safe, quote=True)
        lab = html.escape(label, quote=True)
        a = f"<a href=\"{href}\" target=\"_blank\" rel=\"noopener noreferrer\">{lab}</a>"
        return _new_token(a)

    s1 = link_pat.sub(_link_repl, s0)

    # 2) Bare URLs
    url_pat = re.compile(r"(?<![A-Za-z0-9_])https?://[^ \t\r\n<>\"']+", flags=re.I)

    def _url_repl(m: re.Match) -> str:
        raw = m.group(0)
        url = raw
        trail = ""
        while url and url[-1] in ".,;:!?)]}\"'":
            trail = url[-1] + trail
            url = url[:-1]
        safe = sanitize_url(url)
        if not safe:
            return raw
        href = html.escape(safe, quote=True)
        lab = html.escape(url, quote=True)
        a = f"<a href=\"{href}\" target=\"_blank\" rel=\"noopener noreferrer\">{lab}</a>"
        return _new_token(a) + trail

    s2 = url_pat.sub(_url_repl, s1)

    # 3) Bold: **text** or __text__
    bold_pat = re.compile(r"(\*\*|__)(?P<txt>[^\n]+?)\1")

    def _bold_repl(m: re.Match) -> str:
        inner = (m.group("txt") or "").strip()
        if not inner:
            return m.group(0)
        return _new_token(f"<strong>{html.escape(inner, quote=True)}</strong>")

    s3 = bold_pat.sub(_bold_repl, s2)

    # 4) Highlight: ==text==
    hi_pat = re.compile(r"==(?P<txt>[^\n]+?)==")

    def _hi_repl(m: re.Match) -> str:
        inner = (m.group("txt") or "").strip()
        if not inner:
            return m.group(0)
        return _new_token(f"<mark class=\"hl\">{html.escape(inner, quote=True)}</mark>")

    s4 = hi_pat.sub(_hi_repl, s3)

    escaped = html.escape(s4, quote=True)
    # Restore tokens in reverse insertion order to support nesting
    for tok in reversed(list(token_map.keys())):
        escaped = escaped.replace(tok, token_map[tok])
    return escaped

def as_bool(v, default: bool = False) -> bool:
    """Parse common truthy/falsey values from front matter."""
    if v is None:
        return default
    if isinstance(v, bool):
        return v
    s = str(v).strip().lower()
    if s in {"1","true","yes","y","on"}:
        return True
    if s in {"0","false","no","n","off"}:
        return False
    return default


def render_simple_md(md: str) -> str:
    """Paragraphs + unordered lists + callouts (::: ... :::)."""
    # Fix a common Markdown formatting issue in CVs:
    #   [label](
    #     https://...
    #   )
    # When links are broken across lines, our line-based renderer would miss them.
    md = re.sub(r"\]\(\s*\n\s*(https?://[^\s\)]+)\s*\)", r"](\1)", md or "", flags=re.I)

    lines = (md or "").replace("\r\n", "\n").replace("\r", "\n").split("\n")
    out: List[str] = []
    in_ul = False

    def close_ul():
        nonlocal in_ul
        if in_ul:
            out.append("</ul>")
            in_ul = False

    def default_title(t: str) -> str:
        m = {"recruit": "Recruiting", "info": "Note", "warn": "Notice", "success": "Highlight"}
        return m.get(t, "")

    i = 0
    while i < len(lines):
        line = lines[i]
        st = line.strip()

        if not st:
            close_ul()
            i += 1
            continue

        # Callout blocks:
        #   :::recruit Title (optional)
        #   ... content ...
        #   :::
        if st.startswith(':::'):
            # Closing marker by itself
            if st == ':::':
                close_ul()
                i += 1
                continue

            # Find matching closing ':::'
            j = i + 1
            while j < len(lines) and lines[j].strip() != ':::':
                j += 1

            if j < len(lines):
                close_ul()
                header = st[3:].strip()
                parts = header.split(None, 1)
                ctype = parts[0].strip().lower() if parts else 'info'
                title = parts[1].strip() if len(parts) == 2 else ''
                # Support ':::callout recruit Title'
                if ctype == 'callout':
                    sub = title.split(None, 1)
                    ctype = sub[0].strip().lower() if sub else 'info'
                    title = sub[1].strip() if len(sub) == 2 else ''

                # Sanitize class name
                ctype = re.sub(r'[^a-z0-9_-]+', '', ctype) or 'info'
                if not title:
                    title = default_title(ctype)

                body_md = '\n'.join(lines[i+1:j]).strip('\n')
                body_html = render_simple_md(body_md) if body_md else ''
                title_html = ''
                if title:
                    title_html = '<div class="callout-title">{}</div>'.format(md_inline_to_html(title))
                out.append('<div class="callout {}">{}<div class="callout-body">{}</div></div>'.format(ctype, title_html, body_html))

                i = j + 1
                continue
            # No closing marker found: fall through and render as normal text.

        # Bullet list item (allow both '- item' and '-item')
        if st.startswith('-') or st.startswith('*'):
            after = st[1:]
            if after.startswith(' '):
                after = after[1:]
            if after.strip():
                if not in_ul:
                    out.append('<ul>')
                    in_ul = True
                out.append('<li>{}</li>'.format(md_inline_to_html(after.strip())))
                i += 1
                continue

        close_ul()
        out.append('<p>{}</p>'.format(md_inline_to_html(st)))
        i += 1

    close_ul()
    return '\n'.join(out)

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



def resolve_nav_section_map(nav_cfg, all_titles: List[str]) -> Tuple[Dict[str, List[str]], set]:
    """Resolve per-page section allocation from nav config.

    nav item can include:
      - section: "Title"
      - sections: ["Title A", "Title B", "*"]

    Special token "*":
      - Assigned ONLY once, to the first nav item (in nav order) that contains "*"
      - Expands to "all remaining section titles" (in CV.md order) not explicitly assigned elsewhere
      - If multiple pages include "*", later ones get nothing for "*"
    """
    if not isinstance(nav_cfg, list):
        return {}, set()

    # Collect raw configs by href (merge if repeated)
    raw_by_href: Dict[str, List[str]] = {}
    nav_order: List[str] = []
    for it in nav_cfg:
        if not isinstance(it, dict):
            continue
        href = str(it.get("href", "")).strip()
        if not href:
            continue
        if href.startswith(("http://", "https://")):
            continue
        if href in ("index.html", "./index.html"):
            continue
        if not href.lower().endswith(".html"):
            continue

        secs_cfg = it.get("sections", it.get("section", None))
        if secs_cfg is None:
            continue
        if isinstance(secs_cfg, str):
            secs_list = [secs_cfg]
        elif isinstance(secs_cfg, list):
            secs_list = secs_cfg
        else:
            continue
        secs_list = [str(s).strip() for s in secs_list if str(s).strip()]
        if not secs_list:
            continue

        if href not in raw_by_href:
            nav_order.append(href)
            raw_by_href[href] = []
        raw_by_href[href].extend(secs_list)

    if not raw_by_href:
        return {}, set()

    # Explicit assignments (exclude "*")
    explicit = set()
    for lst in raw_by_href.values():
        for t in lst:
            if t != "*":
                explicit.add(t)

    remaining = [t for t in all_titles if t not in explicit]

    # First wildcard page (nav order)
    wildcard_href = None
    for href in nav_order:
        if "*" in raw_by_href.get(href, []):
            wildcard_href = href
            break

    resolved: Dict[str, List[str]] = {}
    assigned: set = set()
    remaining_used = False

    for href in nav_order:
        lst = raw_by_href.get(href, [])
        out: List[str] = []
        seen = set()
        for token in lst:
            token = str(token).strip()
            if not token:
                continue
            if token == "*":
                if href == wildcard_href and (not remaining_used):
                    for t in remaining:
                        if t not in seen:
                            out.append(t)
                            seen.add(t)
                    remaining_used = True
                continue
            if token not in seen:
                out.append(token)
                seen.add(token)
        resolved[href] = out
        for t in out:
            assigned.add(t)

    return resolved, assigned



def split_front_matter_raw(md_text: str) -> Tuple[str, str]:
    """Return (front_matter_block_including_delimiters_or_empty, body)."""
    txt = md_text
    # Preserve BOM if present
    bom = "\ufeff" if txt.startswith("\ufeff") else ""
    if bom:
        txt = txt.lstrip("\ufeff")

    if not txt.startswith("---"):
        return bom, txt

    m = re.match(r"^(---\s*\n.*?\n---\s*\n)(.*)$", txt, flags=re.S)
    if not m:
        return bom, txt

    return bom + m.group(1), m.group(2)


def is_ieee_xplore_url(u: str) -> bool:
    """Return True if the URL looks like an IEEE Xplore document page."""
    u = (u or "").strip().lower()
    return ("ieeexplore.ieee.org" in u) and ("/document/" in u or "/abstract/document/" in u)


def ieee_doc_id(u: str) -> str:
    """Extract IEEE Xplore arnumber from common URL forms."""
    m = re.search(r"/(?:abstract/)?document/(\d+)", u)
    return m.group(1) if m else ""


def fetch_text(url: str, timeout: int = 20) -> str:
    """Fetch a URL as decoded text.

    Why this exists:
    - Some sites (incl. IEEE Xplore) may serve compressed content.
    - urllib does not always auto-decompress; requests usually does.

    Strategy:
    1) Prefer `requests` if installed (handles gzip/deflate transparently).
    2) Fall back to urllib + manual gzip/deflate decompress.

    Note: we *do not* advertise brotli (br) in Accept-Encoding to avoid needing extra deps.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1",
    }

    # 1) Try requests first
    try:
        import requests  # type: ignore
        r = requests.get(url, headers=headers, timeout=timeout)
        r.raise_for_status()
        # Let requests decide encoding; fallback to apparent
        if not r.encoding:
            r.encoding = r.apparent_encoding
        return r.text
    except ImportError:
        pass
    except Exception:
        # If requests is present but fails (proxy/cert/etc.), fall back to urllib.
        pass

    # 2) urllib fallback
    req = Request(url, headers=headers)
    with urlopen(req, timeout=timeout) as resp:
        data = resp.read()
        enc_hdr = (resp.headers.get("Content-Encoding") or "").lower()
        if "gzip" in enc_hdr:
            try:
                import gzip
                data = gzip.decompress(data)
            except Exception:
                pass
        elif "deflate" in enc_hdr:
            try:
                import zlib
                # Try raw deflate first, then zlib-wrapped
                try:
                    data = zlib.decompress(data, -zlib.MAX_WBITS)
                except Exception:
                    data = zlib.decompress(data)
            except Exception:
                pass

        # Guess charset
        ctype = (resp.headers.get("Content-Type") or "").lower()
        m = re.search(r"charset=([\w\-]+)", ctype)
        enc = m.group(1) if m else "utf-8"

    try:
        return data.decode(enc, errors="replace")
    except Exception:
        return data.decode("utf-8", errors="replace")


def extract_meta(html_text: str, name: str) -> List[str]:
    """Extract <meta name="..." content="..."> values (case-insensitive)."""
    if not html_text:
        return []
    # Support both single and double quotes
    pat = re.compile(
        r"<meta[^>]+name\s*=\s*(['\"]){}\1[^>]*content\s*=\s*(['\"])(.*?)\2".format(re.escape(name)),
        flags=re.I | re.S,
    )
    vals = [html.unescape(m.group(3)).strip() for m in pat.finditer(html_text)]
    return [v for v in vals if v]


def author_to_initials(full: str) -> str:
    """Convert full name to initials.

    Examples:
      - Cheng Luo -> C. Luo
      - Kai-Wei Chang -> K.-W. Chang
    """
    full = (full or "").strip()
    if not full:
        return ""
    # If the name already looks abbreviated, keep it.
    if re.search(r"\b[A-Z]\.", full):
        return full

    parts = [p for p in re.split(r"\s+", full) if p]
    if len(parts) == 1:
        return parts[0]
    last = parts[-1]
    firsts = parts[:-1]

    inits = []
    for fn in firsts:
        # Handle hyphenated given names
        sub = [x for x in fn.split("-") if x]
        if len(sub) > 1:
            inits.append("-".join([s[0].upper() + "." for s in sub if s[0].isalpha()]))
        else:
            ch = fn[0].upper() if fn[0].isalpha() else fn[0]
            inits.append(ch + ".")

    return " ".join(["".join(inits).replace("..", "."), last]).strip()


def format_authors(authors: List[str]) -> str:
    aa = [author_to_initials(a) for a in authors if a]
    aa = [a for a in aa if a]
    if not aa:
        return ""
    if len(aa) == 1:
        return aa[0]
    if len(aa) == 2:
        return aa[0] + " and " + aa[1]
    return ", ".join(aa[:-1]) + " and " + aa[-1]


def safe_bib_key(s: str) -> str:
    s = (s or "")
    s = re.sub(r"[^A-Za-z0-9]+", "", s)
    return s or "ref"


def make_bibtex(meta: Dict[str, str], key: str) -> str:
    """Make a simple BibTeX entry (good enough for CV linking)."""
    title = meta.get("title", "")
    authors = meta.get("authors_full", "")
    venue = meta.get("venue", "")
    year = meta.get("year", "")
    doi = meta.get("doi", "")
    url = meta.get("url", "")

    # Decide entry type
    entry_type = meta.get("bib_type", "article")

    fields = []
    if title:
        fields.append(("title", title))
    if authors:
        fields.append(("author", authors))
    if venue:
        # use journal by default
        fields.append(("journal" if entry_type == "article" else "booktitle", venue))
    if year:
        fields.append(("year", year))
    if doi:
        fields.append(("doi", doi))
    if url:
        fields.append(("url", url))

    body = "\n".join([f"  {k} = {{{v}}}," for k, v in fields])
    return f"@{entry_type}{{{key},\n{body}\n}}\n"


def _find_matching_brace(s: str, start: int) -> int:
    """Return index of the matching closing brace for s[start]=='{', else -1."""
    if start < 0 or start >= len(s) or s[start] != '{':
        return -1
    depth = 0
    in_str = False
    esc_next = False
    quote = ''
    for i in range(start, len(s)):
        ch = s[i]
        if in_str:
            if esc_next:
                esc_next = False
                continue
            if ch == '\\':
                esc_next = True
                continue
            if ch == quote:
                in_str = False
                quote = ''
            continue
        else:
            if ch in ('"', "'"):
                in_str = True
                quote = ch
                continue
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    return i
    return -1



def _unescape_js_str(s: str) -> str:
    """Best-effort unescape for strings extracted from JSON-ish JS blobs."""
    if not s:
        return s
    s2 = s.replace('\\/', '/').replace('\\n', ' ').replace('\\t', ' ')
    if '\\u' in s2:
        try:
            s2 = s2.encode('utf-8', errors='ignore').decode('unicode_escape', errors='ignore')
        except Exception:
            pass
    return s2

def _extract_ieee_metadata_fallback(page: str) -> Optional[dict]:
    """Fallback extractor: parse key fields from the metadata line using regex/splits."""
    if not page:
        return None
    key = 'xplGlobal.document.metadata='
    start = page.find(key)
    if start == -1:
        return None
    end = page.find('\n', start)
    if end == -1:
        end = page.find('</script>', start)
    if end == -1:
        end = min(len(page), start + 200000)
    line = page[start:end]

    def _grab(pattern: str) -> str:
        m = re.search(pattern, line)
        return _unescape_js_str(m.group(1)) if m else ''

    title = _grab(r'"formulaStrippedArticleTitle"\s*:\s*"([^"]+)"') or _grab(r'"articleTitle"\s*:\s*"([^"]+)"') or _grab(r'"title"\s*:\s*"([^"]+)"')
    venue = _grab(r'"publicationTitle"\s*:\s*"([^"]+)"') or _grab(r'"conferenceTitle"\s*:\s*"([^"]+)"')
    pubdate = _grab(r'"publicationDate"\s*:\s*"([^"]+)"') or _grab(r'"publicationYear"\s*:\s*"?((?:19|20)\d{2})"?')
    doi = _grab(r'"doi"\s*:\s*"([^"]+)"')
    ptype = _grab(r'"publicationType"\s*:\s*"([^"]+)"') or _grab(r'"contentType"\s*:\s*"([^"]+)"')
    citation = _grab(r'"citationCountPaper"\s*:\s*([0-9]+)')

    authors_blob = ''
    m = re.search(r'"authors"\s*:\s*\[(.*)\]\s*,\s*"', line)
    if m:
        authors_blob = m.group(1)
    names = re.findall(r'"name"\s*:\s*"([^"]+)"', authors_blob)
    authors = [{"name": _unescape_js_str(n)} for n in names if n.strip()]

    data = {}
    if title:
        data["formulaStrippedArticleTitle"] = title
    if authors:
        data["authors"] = authors
    if venue:
        data["publicationTitle"] = venue
    if pubdate:
        data["publicationDate"] = pubdate
    if doi:
        data["doi"] = doi
    if ptype:
        data["publicationType"] = ptype
    if citation:
        data["citationCountPaper"] = citation

    # Early Access flag (best-effort)
    try:
        m_ea = re.search(r'"isEarlyAccess"\s*:\s*(true|false|"true"|"false"|1|0)', line, flags=re.I)
        if m_ea:
            v = m_ea.group(1).strip().strip('"').lower()
            data["isEarlyAccess"] = True if v in ("true", "1", "yes") else False
    except Exception:
        pass

    return data or None

def _extract_ieee_metadata_json(page: str) -> Optional[dict]:
    """Extract the JSON object from `xplGlobal.document.metadata=...` if present."""
    if not page:
        return None
    key = 'xplGlobal.document.metadata='
    idx = page.find(key)
    if idx == -1:
        return None
    idx = page.find('{', idx)
    if idx == -1:
        return None
    end = _find_matching_brace(page, idx)
    if end == -1:
        return None
    blob = page[idx:end+1]
    try:
        return json.loads(blob)
    except Exception:
        # Some pages embed JSON with escaped sequences; try a light cleanup
        try:
            blob2 = blob.replace('\u2028', '').replace('\u2029', '')
            return json.loads(blob2)
        except Exception:
            fb = _extract_ieee_metadata_fallback(page)
            if fb is not None:
                return fb
            return None


def fetch_ieee_xplore_metadata(paper_url: str) -> Optional[Dict[str, str]]:
    """Fetch metadata from an IEEE Xplore document URL.

    Compared to the previous implementation (citation meta tags), this uses the
    `xplGlobal.document.metadata` JSON blob that IEEE Xplore pages commonly embed.

    This usually works well without downloading any PDF.
    """
    url = (paper_url or '').strip()
    if not url:
        return None

    # Normalize URL to /document/<id>
    docid = ieee_doc_id(url)
    if docid:
        url = f"https://ieeexplore.ieee.org/document/{docid}"

    try:
        page = fetch_text(url)

        # Extra: citation meta tags often include an "online date" even for Early Access.
        def _grab_meta(name: str) -> str:
            m = re.search(
                r'<meta\s+name=["\']' + re.escape(name) + r'["\']\s+content=["\']([^"\']+)["\']',
                page,
                flags=re.I,
            )
            return m.group(1).strip() if m else ""

        citation_online_date = _grab_meta("citation_online_date")
        citation_pub_date = _grab_meta("citation_publication_date")
        citation_date = _grab_meta("citation_date")

    except Exception:
        page = ''

    data = _extract_ieee_metadata_json(page)

    # Fallback: meta tags (some mirrors/old pages)
    if not data:
        try:
            title = (extract_meta(page, 'citation_title') or [''])[0]
            authors = extract_meta(page, 'citation_author')
            venue = ''
            for nm in ('citation_journal_title', 'citation_conference_title', 'citation_book_title'):
                vv = extract_meta(page, nm)
                if vv:
                    venue = vv[0]
                    break
            year = ''
            for nm in ('citation_publication_date', 'citation_date', 'citation_year'):
                vv = extract_meta(page, nm)
                if vv:
                    m = re.search(r"(19|20)\d{2}", vv[0])
                    if m:
                        year = m.group(0)
                        break
            doi = (extract_meta(page, 'citation_doi') or [''])[0]
            bib_type = 'article' if extract_meta(page, 'citation_journal_title') else 'inproceedings' if extract_meta(page, 'citation_conference_title') else 'misc'
            return {
                'title': title,
                'authors_list': authors,
                'venue': venue,
                'year': year,
                'doi': doi,
                'url': url,
                'bib_type': bib_type,
            }
        except Exception:
            return None

    # Title
    title = (data.get('formulaStrippedArticleTitle') or data.get('articleTitle') or data.get('title') or '').strip()

    # Authors
    authors_list = []
    try:
        aa = data.get('authors') or []
        if isinstance(aa, list):
            for a in aa:
                if isinstance(a, dict):
                    nm = (a.get('name') or '').strip()
                    if nm:
                        authors_list.append(nm)
                elif isinstance(a, str) and a.strip():
                    authors_list.append(a.strip())
    except Exception:
        pass

    # Venue (journal/conf name)
    venue = (data.get('publicationTitle') or data.get('conferenceTitle') or '').strip()

    # Publication date (raw, can be full date or 'Early Access')
    pubdate = ''
    for k in ('publicationDate', 'publicationYear', 'publication_date', 'publication_year'):
        v = data.get(k)
        if isinstance(v, str) and v.strip():
            pubdate = v.strip()
            break
        elif isinstance(v, int):
            pubdate = str(v)
            break

    # Prefer citation meta tag date if it provides a more specific (month/day) value.
    best_meta_date = citation_online_date or citation_pub_date or citation_date
    if best_meta_date:
        dt_meta = parse_pubdate_to_tuple(best_meta_date)
        dt_cur = parse_pubdate_to_tuple(pubdate) if pubdate else None
        if (not dt_cur) or (dt_meta and (dt_meta[1] != 0 or dt_meta[2] != 0) and (dt_cur[1] == 0 and dt_cur[2] == 0)):
            pubdate = best_meta_date

    # Early Access flag (best-effort)
    is_early_access = False
    v_ea = data.get('isEarlyAccess')
    if isinstance(v_ea, bool):
        is_early_access = v_ea
    elif isinstance(v_ea, str) and v_ea.strip().lower() in ('true', '1', 'yes'):
        is_early_access = True
    if (not is_early_access) and pubdate and ('early access' in pubdate.lower()):
        is_early_access = True
    if (not is_early_access) and ('early access' in page.lower()):
        is_early_access = True

# Year
    year = ''
    for k in ('publicationDate', 'publicationYear', 'publication_date', 'publication_year'):
        v = data.get(k)
        if isinstance(v, str):
            m = re.search(r"(19|20)\d{2}", v)
            if m:
                year = m.group(0)
                break
        elif isinstance(v, int):
            year = str(v)
            break

    # DOI
    doi = ''
    for k in ('doi', 'doiLink', 'doi_url'):
        v = data.get(k)
        if isinstance(v, str) and v.strip():
            # doiLink may be like 'https://doi.org/10....'
            m = re.search(r'10\.\d{4,9}/[^\s"<>]+', v)
            doi = m.group(0) if m else v.strip()
            break

    # Guess BibTeX type
    ptype = str(data.get('publicationType') or data.get('contentType') or '').lower()
    if 'conference' in ptype:
        bib_type = 'inproceedings'
    elif 'journal' in ptype or 'magazine' in ptype:
        bib_type = 'article'
    else:
        bib_type = 'misc'

    return {
        'title': title,
        'authors_list': authors_list,
        'venue': venue,
        'year': year,
        'doi': doi,
        'url': url,
        'bib_type': bib_type,
            'pubdate': pubdate,
        'is_early_access': 'true' if is_early_access else '',
}


def ensure_bib_file(meta: Dict[str, str]) -> str:
    """Write BibTeX file (if possible) and return the relative path (./bibtex/xxx.bib)."""
    # If local BibTeX generation is disabled, still provide an *online* BibTeX
    # export link for IEEE Xplore items (so the HTML keeps a BibTeX button).
    if not bibtex_autogen:
        doc_id = ieee_doc_id(meta.get("url", ""))
        return ieee_bibtex_export_url(doc_id) if doc_id else ""

    os.makedirs(BIB_DIR, exist_ok=True)

    authors = meta.get("authors_list") or []
    first_last = ""
    if authors:
        # Take surname of first author if possible
        parts = [p for p in re.split(r"\s+", authors[0].strip()) if p]
        first_last = parts[-1] if parts else ""

    year = meta.get("year", "")
    title = meta.get("title", "")
    first_word = ""
    if title:
        w = re.split(r"\s+", title.strip())
        first_word = w[0] if w else ""

    key = safe_bib_key(first_last) + (year or "") + safe_bib_key(first_word)
    key = key or (ieee_doc_id(meta.get("url", "")) or "ref")

    bib_rel = f"./{BIB_DIR}/{key}.bib"
    bib_path = os.path.join(BIB_DIR, f"{key}.bib")

    # Build bibtex author string in "First Last and First2 Last2" format
    authors_full = ""
    if authors:
        authors_full = " and ".join([a.strip() for a in authors if a.strip()])

    meta2 = dict(meta)
    meta2["authors_full"] = authors_full

    content = make_bibtex(meta2, key)
    # Write only if new or changed
    try:
        old = ""
        if os.path.exists(bib_path):
            with open(bib_path, "r", encoding="utf-8", errors="ignore") as f:
                old = f.read()
        if old != content:
            with open(bib_path, "w", encoding="utf-8") as f:
                f.write(content)
    except Exception:
        # If writing fails, fall back to no bib.
        return ""

    return bib_rel


def autofill_publications(md_text: str, section_title: str = PUB_SECTION_TITLE) -> Tuple[str, bool]:
    """Replace URL-only pub bullets in the Selected Publications section with filled entries.

    - If the line already contains pipes (manual format), we keep it.
    - If the line is just a URL and it's IEEE Xplore, we fetch citation meta tags and expand it.
    - For non-IEEE URL-only lines, we keep as-is (you can manually add full info).

    Returns: (new_md_text, changed)
    """
    fm, body = split_front_matter_raw(md_text)
    lines = body.splitlines()

    out = []
    in_target = False
    changed = False
    cache: Dict[str, Optional[Dict[str, str]]] = {}

    for ln in lines:
        h = re.match(r"^\s*##\s+(.*)$", ln.strip())
        if h:
            in_target = (h.group(1).strip() == section_title)
            out.append(ln)
            continue

        if in_target:
            # URL-only list item
            m = re.match(r"^(\s*[-*]\s+)(https?://\S+)\s*$", ln)
            if m:
                prefix, url = m.group(1), m.group(2).strip()
                if is_ieee_xplore_url(url):
                    if url not in cache:
                        cache[url] = fetch_ieee_xplore_metadata(url)
                    meta = cache[url]
                    if meta:
                        PUB_META_CACHE[url] = meta
                        # also cache under normalized document URL
                        _docid = ieee_doc_id(url)
                        if _docid:
                            PUB_META_CACHE[f"https://ieeexplore.ieee.org/document/{_docid}"] = meta
                    if meta and meta.get("title"):
                        authors_text = format_authors(meta.get("authors_list") or [])
                        venue = (meta.get("venue") or "").strip()
                        year = (meta.get("year") or "").strip()
                        venue_year = (venue + (" " + year if year else "")).strip()

                        bib_rel = ensure_bib_file(meta)
                        parts = [meta["title"].strip()]
                        if authors_text:
                            parts.append(authors_text)
                        if venue_year:
                            parts.append(venue_year)
                        parts.append(f"PDF: {url}")
                        if bib_rel:
                            parts.append(f"BibTeX: {bib_rel}")

                        new_line = prefix + " | ".join(parts)
                        out.append(new_line)
                        changed = True
                        continue

        out.append(ln)

    new_body = "\n".join(out)
    # Preserve trailing newline style
    if body.endswith("\n"):
        new_body += "\n"

    return fm + new_body, changed

def parse_pub_line(line: str) -> Dict[str, str]:
    """
    Format:
      - Title | Authors(optional) | Venue Year(optional) | PDF: url | BibTeX: url | Code: url
    """
    s = re.sub(r"^\s*[-*]\s+", "", line.strip())
    parts = [p.strip() for p in s.split("|") if p.strip()]

    # Allow a minimal form: '- https://...'
    # (If auto-fill failed or for non-IEEE links, we still render a usable PDF button.)
    if len(parts) == 1 and re.match(r"^https?://", parts[0], flags=re.I):
        url_only = parts[0].strip()
        return {
            "title": url_only,
            "authors": "",
            "venue": "",
            "year": "",
            "pdf": url_only,
            "bib": "",
            "code": "",
        }

    title = parts[0] if parts else ""
    authors = ""
    venue_year = ""
    pdf = ""
    bib = ""
    code = ""

    info: List[str] = []
    for p in parts[1:]:
        pl = p.lower()
        if pl.startswith("pdf:"):
            pdf = p.split(":", 1)[1].strip()
        elif pl.startswith("bibtex:") or pl.startswith("bib:"):
            bib = p.split(":", 1)[1].strip()
        elif pl.startswith("code:"):
            code = p.split(":", 1)[1].strip()
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
        "code": code,
    }



def pub_sort_key(p: Dict[str, str]) -> Tuple[int, int, int]:
    """Sort key for publications: newer first.

    Priority:
      1) If we have IEEE metadata cached for the PDF URL, use its publicationDate (year+month+day).
      2) Otherwise, fall back to year extracted from the entry itself.
      3) If marked as Early Access, push it ahead of non-early-access entries within the same year.
    Returns (year, month, day), used with reverse=True.
    """
    pdf_url = (p.get("pdf") or "").strip()

    # 1) Cached IEEE metadata
    meta = PUB_META_CACHE.get(pdf_url) if pdf_url else None
    if (not meta) and pdf_url:
        _docid = ieee_doc_id(pdf_url)
        if _docid:
            meta = PUB_META_CACHE.get(f"https://ieeexplore.ieee.org/document/{_docid}")
    if meta:
        pubdate = (meta.get("pubdate") or "").strip()
        is_ea = str(meta.get("is_early_access") or "").strip().lower() in ("true", "1", "yes")
        if (not is_ea) and pubdate and ("early access" in pubdate.lower()):
            is_ea = True

        dt = parse_pubdate_to_tuple(pubdate)
        if dt:
            y, mo, d = dt
            if is_ea:
                # Make Early Access slightly ahead within the same date bucket.
                return (y, mo, d + 1 if d < 31 else d)
            return (y, mo, d)

        # No parseable date: fall back to year but keep EA ahead
        y = 0
        m = re.search(r"(19|20)\d{2}", pubdate)
        if m:
            y = int(m.group(0))
        if y == 0:
            year_s = (p.get("year") or "").strip()
            if year_s.isdigit():
                y = int(year_s)
        if is_ea:
            return (y if y else 9999, 99, 99)
        return (y, 0, 0)

    # 2) Fallback: parse from the publication line itself
    y = 0
    mo = 0
    d = 0

    year_s = (p.get("year") or "").strip()
    if year_s.isdigit():
        y = int(year_s)

    # Try to parse a full date if the venue text contains one
    venue_text = " ".join([(p.get("venue") or ""), (p.get("year") or "")]).strip()
    dt2 = parse_pubdate_to_tuple(venue_text)
    if dt2:
        y, mo, d = dt2
    elif y == 0:
        m = re.search(r"(19|20)\d{2}", venue_text)
        if m:
            y = int(m.group(0))

    # Early Access heuristic (if it appears anywhere)
    if "early access" in venue_text.lower():
        return (y if y else 9999, 99, 99)

    return (y, mo, d)


def render_publications(md: str) -> str:
    lines = [ln.strip() for ln in md.split("\n") if ln.strip()]
    pub_lines = [ln for ln in lines if ln.startswith("-") or ln.startswith("*")]

    pubs = [parse_pub_line(ln) for ln in pub_lines]

    # Sort: newer first (stable for ties)
    pubs = sorted(pubs, key=pub_sort_key, reverse=True)

    blocks: List[str] = []

    for i, p in enumerate(pubs, start=1):
        links = []
        if p["pdf"]:
            links.append('<a class="pill" href="{0}" target="_blank" rel="noopener">PDF</a>'.format(esc(p["pdf"])))
        if p["bib"]:
            links.append('<a class="pill" href="{0}" target="_blank" rel="noopener">BibTeX</a>'.format(esc(p["bib"])))
        if p.get("code"):
            links.append('<a class="pill" href="{0}" target="_blank" rel="noopener">Code</a>'.format(esc(p["code"])))

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
                ('    <div class="meta-line">'
                 + ('<span class="authors-text">{}</span>'.format(allow_strong_only(bold_author_in_authors_str(p["authors"], highlight_author))) if p["authors"] else '')
                 + ('<span class="venue-badge">{}</span>'.format(allow_strong_only(venue_text)) if venue_text else '')
                 + '</div>'
                 if (p["authors"] or venue_text) else ''),
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

def allow_strong_only(s: str) -> str:
    # 先全部转义
    x = html.escape(s or "", quote=True)
    # 再把被转义的 <strong> 放回来（只放 strong）
    x = x.replace("&lt;strong&gt;", "<strong>").replace("&lt;/strong&gt;", "</strong>")
    return x


def bold_author_in_authors_str(authors: str, highlight: str) -> str:
    """Bold user's name in an authors string.
    - Case-insensitive
    - Works for 'C. Luo', 'Cheng Luo', 'Luo, C.', 'Luo C.' etc. by token match
    - Uses <strong>...</strong> so our renderer can safely allow it.
    """
    authors = authors or ""
    highlight = (highlight or "").strip()
    if not authors or not highlight:
        return authors

    # Normalize highlight tokens
    def norm_tokens(s: str):
        s = re.sub(r"[\.,;:()\[\]{}]", " ", s)
        s = s.replace("-", " ")
        toks = [t for t in s.split() if t]
        return toks

    h_toks = norm_tokens(highlight)
    if not h_toks:
        return authors

    # Build a few common patterns to match
    # 1) Exact substring match (case-insensitive)
    def repl(m):
        return f"<strong>{m.group(0)}</strong>"

    out = authors

    # First, try exact highlight string
    out2 = re.sub(re.escape(highlight), repl, out, flags=re.I)
    if out2 != out:
        return out2

    # Otherwise, try matching tokens in order (allow optional dots/spaces)
    # e.g., highlight "C. Luo" -> match "C. Luo", "C Luo", "C.Luo"
    # e.g., highlight "Cheng Luo" -> match "Cheng Luo"
    tok_pat = r"\s*\.?\s*".join([re.escape(t) for t in h_toks])
    tok_pat = r"\b" + tok_pat + r"\b"
    out2 = re.sub(tok_pat, repl, out, flags=re.I)
    if out2 != out:
        return out2

    # Finally, handle 'Last, F.' pattern if highlight looks like 'First Last' or 'F. Last'
    if len(h_toks) >= 2:
        first = h_toks[0]
        last = h_toks[-1]
        # Match 'Last, First' or 'Last, F'
        pat = rf"\b{re.escape(last)}\s*,\s*{re.escape(first)}\b"
        out2 = re.sub(pat, repl, out, flags=re.I)
        if out2 != out:
            return out2
        pat = rf"\b{re.escape(last)}\s*,\s*{re.escape(first[0])}\.?\b"
        out2 = re.sub(pat, repl, out, flags=re.I)
        if out2 != out:
            return out2


    # If highlight is like 'C. Luo' (initial + last), also match full first name 'Cheng Luo'
    if len(h_toks) == 2 and len(h_toks[0]) == 1:
        ini = re.escape(h_toks[0])
        last = re.escape(h_toks[1])
        pat = rf"\b{ini}[A-Za-z\-]*\s+{last}\b"
        out2 = re.sub(pat, repl, out, flags=re.I)
        if out2 != out:
            return out2
        pat = rf"\b{last}\s+{ini}[A-Za-z\-]*\b"
        out2 = re.sub(pat, repl, out, flags=re.I)
        if out2 != out:
            return out2


    return out


def main():
    md_path = "CV.md"
    out_path = "index.html"

    if not os.path.exists(md_path):
        raise SystemExit("找不到 CV.md，请确认它与 build_cv.py 在同一目录。")

    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Read front matter early so settings affect autofill/writeback
    meta0, _body0 = parse_front_matter(md_text)
    global highlight_author
    global bibtex_autogen
    highlight_author = str(meta0.get("highlight_author", "")).strip()
    writeback_backup = as_bool(meta0.get("writeback_backup", True), True)
    writeback_enabled = as_bool(meta0.get("writeback_enabled", meta0.get("writeback", meta0.get("pub_writeback", meta0.get("writeback_md", True)))), True)
    bibtex_autogen = as_bool(meta0.get("bibtex_autogen", True), True)



    # --- Auto-fill IEEE publications (URL-only bullets) and update CV.md in-place ---
    # If you wrote full info manually (with | Title | Authors | ...), we keep it as-is.
    new_md_text, changed = autofill_publications(md_text, section_title=PUB_SECTION_TITLE)
    if changed:
        md_text = new_md_text
    if changed:
            bak = None
            if writeback_enabled and writeback_backup:
                # Backup once per run
                bak = md_path + '.bak-' + datetime.now().strftime('%Y%m%d-%H%M%S')
                try:
                    with open(bak, 'w', encoding='utf-8') as f:
                        f.write(md_text)
                except Exception:
                    bak = None
            if writeback_enabled:
                try:
                    with open(md_path, 'w', encoding='utf-8') as f:
                        f.write(md_text)
                except Exception as e:
                    print('⚠️ 写回 CV.md 失败：{}'.format(e))
                else:
                    print('📝 已自动补全 Selected Publications，并写回 CV.md' + (f'（备份：{bak}）' if bak else ''))
            else:
                print('📝 已自动补全 Selected Publications（未写回 CV.md；可在 front matter 设置 writeback_enabled: true 开启）')
    meta, body = parse_front_matter(md_text)
    secs = split_sections(body)

    # Only keep these 3
    # Render all sections in order.
    # Only the publications section is treated specially (URL-only auto-fill + pills).
    
    # Render Home sections.
    # Rule:
    #   - If front matter provides home_sections (list of '##' titles), render those in that order.
    #   - Else, render all sections EXCEPT those assigned to other internal pages via nav item 'section(s)'.
    nav_cfg = []
    for _k in ("nav", "nav_items", "navbar"):
        if isinstance(meta.get(_k), list):
            nav_cfg = meta.get(_k)  # type: ignore
            break

    all_titles = list(secs.keys())
    resolved_section_map, assigned_titles = resolve_nav_section_map(nav_cfg, all_titles)

    home_sections_cfg = meta.get("home_sections", None)
    sections_out: List[str] = []

    if isinstance(home_sections_cfg, list) and home_sections_cfg:
        # Explicit list: render only those (ignore assigned_titles).
        for _t in home_sections_cfg:
            t = str(_t).strip()
            if not t:
                continue
            sec_body = secs.get(t, "")
            if not sec_body.strip():
                continue
            if t == PUB_SECTION_TITLE:
                sections_out.append(section_html(t, render_publications(sec_body)))
            else:
                sections_out.append(section_html(t, render_simple_md(sec_body)))
    else:
        # Default: render everything except what is assigned to internal pages.
        for sec_title, sec_body in secs.items():
            if not sec_body.strip():
                continue
            if sec_title.strip() in assigned_titles:
                continue
            if sec_title.strip() == PUB_SECTION_TITLE:
                sections_out.append(section_html(sec_title, render_publications(sec_body)))
            else:
                sections_out.append(section_html(sec_title, render_simple_md(sec_body)))

    # meta
    name = str(meta.get("name", "Your Name"))
    role = str(meta.get("role", ""))
    avatar = str(meta.get("avatar", ""))
    email = str(meta.get("email", ""))
    website = str(meta.get("website", ""))
    github = str(meta.get("github", ""))
    location = str(meta.get("location", ""))
    tags = meta.get("cv_tags", meta.get("tags", []))
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]
    if not isinstance(tags, list):
        tags = []
    blogurl = str(meta.get("blogurl", ""))
    subtitle = ""


    # -----------------------------
    # Navbar (simple config)
    # In CV.md front matter, add one line (JSON array):
    #   nav: [{"title":"Projects","href":"projects.html"},{"title":"Blog","href":"https://...","target":"_blank"}]
    # Optional defaults:
    #   nav_target: _self | _blank  (default: _self)
    #   nav_new_tab: true/false     (if true, default becomes _blank)
    # Each item can override:
    #   {"title":"...","href":"...","target":"_blank"}
    # or:
    #   {"title":"...","href":"...","new_tab": true}
    # -----------------------------

    def to_bool(x) -> bool:
        if isinstance(x, bool):
            return x
        if x is None:
            return False
        s = str(x).strip().lower()
        return s in ("1", "true", "yes", "y", "on")

    def normalize_target(t: str) -> str:
        tt = (t or "").strip().lower()
        if tt in ("blank", "_blank", "new", "newtab"):
            return "_blank"
        if tt in ("self", "_self", "same"):
            return "_self"
        return t

    nav_items = meta.get("nav") or meta.get("navbar") or meta.get("nav_items") or []
    if isinstance(nav_items, str):
        try:
            nav_items = json.loads(nav_items)
        except Exception:
            nav_items = []

    nav_target = normalize_target(str(meta.get("nav_target", "_self")))
    if to_bool(meta.get("nav_new_tab")):
        nav_target = "_blank"



    home_title = str(meta.get("home_title", "Home")).strip() or "Home"

    def is_external(h: str) -> bool:
        h = (h or "").strip().lower()
        return h.startswith("http://") or h.startswith("https://")

    def is_internal_html(h: str) -> bool:
        h = (h or "").strip().lower()
        return (not is_external(h)) and h.endswith(".html")

    # Build a single nav list, always including Home
    nav_all = []
    seen_home = False
    if isinstance(nav_items, list):
        for it in nav_items:
            if isinstance(it, dict) and str(it.get("href", "")).strip() in ("index.html", "./index.html"):
                seen_home = True
                break

    if not seen_home:
        nav_all.append({"title": home_title, "href": "index.html"})

    if isinstance(nav_items, list):
        for it in nav_items:
            if isinstance(it, dict):
                nav_all.append(it)

    # Collect internal pages we will generate (shell pages)
    internal_pages = []
    for it in nav_all:
        if not isinstance(it, dict):
            continue
        title = str(it.get("title", "")).strip()
        href = str(it.get("href", "")).strip()
        if not title or not href:
            continue
        if href in ("index.html", "./index.html"):
            continue
        if is_internal_html(href):
            secs_cfg = it.get("sections", it.get("section", []))
            if isinstance(secs_cfg, str):
                secs_cfg = [secs_cfg]
            elif not isinstance(secs_cfg, list):
                secs_cfg = []
            secs_cfg = [str(s).strip() for s in secs_cfg if str(s).strip()]
            internal_pages.append({"title": title, "href": href, "target": it.get("target", ""), "new_tab": it.get("new_tab", False), "sections": secs_cfg})

    def build_navbar(active_href: str) -> str:
        links = []
        for it in nav_all:
            if not isinstance(it, dict):
                continue
            title = str(it.get("title", "")).strip()
            href = str(it.get("href", "")).strip()
            if not title or not href:
                continue

            tgt = it.get("target", "")
            if to_bool(it.get("new_tab")):
                tgt = "_blank"
            tgt = normalize_target(str(tgt)) if tgt else nav_target

            # External links default to new tab unless explicitly specified
            if is_external(href) and not it.get("target") and not to_bool(it.get("new_tab")):
                tgt = "_blank"

            target_attr = f' target="{esc(tgt)}"' if tgt else ""
            rel_attr = ' rel="noopener noreferrer"' if tgt == "_blank" else ""

            css = "navlink"
            if active_href in ("index.html", "./index.html") and href in ("index.html", "./index.html"):
                css += " active"
            elif active_href == href:
                css += " active"

            links.append(f'<a class="{css}" href="{esc(href)}"{target_attr}{rel_attr}>{esc(title)}</a>')

        return '<nav class="navbar">' + ''.join(links) + '</nav>' if links else ""

    tags_block = ""
    if tags:
        tags_block = '<div class="tags">{}</div>'.format(
            "".join('<span class="tag">{}</span>'.format(esc(t)) for t in tags)
        )

    banner_text = meta.get("banner") or meta.get("announcement") or meta.get("notice") or ""
    banner_type = str(meta.get("banner_type", meta.get("announcement_type", meta.get("notice_type", "recruit"))))
    banner_title = str(meta.get("banner_title", meta.get("announcement_title", meta.get("notice_title", ""))))

    banner_block = ""
    if str(banner_text).strip():
        ctype = re.sub(r"[^a-z0-9_-]+", "", (banner_type or "recruit").strip().lower()) or "recruit"
        title = (banner_title or "").strip()
        title_html = ""
        if title:
            title_html = '<div class="callout-title">{}</div>'.format(md_inline_to_html(title))
        body_html = render_simple_md(str(banner_text))
        banner_block = '<div class="callout {}">{}<div class="callout-body">{}</div></div>'.format(ctype, title_html, body_html)

    def contact_row(k: str, v: str, href: Optional[str] = None) -> str:
        if not (v or "").strip():
            return ""
        if href:
            return (
                '<div class="item"><div class="k">{}</div>'
                '<div class="v"><a href="{}" title="{}" target="_blank" rel="noopener noreferrer">{}</a></div></div>'
            ).format(esc(k), esc(href), esc(href), esc(v))
        return '<div class="item"><div class="k">{}</div><div class="v">{}</div></div>'.format(esc(k), esc(v))

    def scholar_display_url(u: str) -> str:
        u = (u or "").strip()
        if not u:
            return ""
        # urlparse needs a scheme to properly fill netloc
        pu = urlparse(u if "://" in u else "https://" + u)
        q = dict(parse_qsl(pu.query, keep_blank_values=False))
        keep = {}
        if "user" in q:
            keep["user"] = q["user"]
        query = urlencode(keep) if keep else ""
        show = (pu.netloc + (pu.path or "")).rstrip("/")
        if query:
            show += "?" + query
        return show

    contact_rows = []
    if email:
        contact_rows.append(contact_row("E-mail", email, "mailto:" + email))
    if website:
        contact_rows.append(contact_row("Google Scholar", scholar_display_url(website), website))
    if github:
        show = github.replace("https://", "").replace("http://", "")
        contact_rows.append(contact_row("GitHub", show, github))
    if location:
        contact_rows.append(contact_row("Location", location))

    contact_block = "\n".join(contact_rows) if contact_rows else ""

    # WeChat Official Account (QR)
    wechat_qr = str(meta.get("wechat_qr", meta.get("wechat_qr_url", meta.get("wechat_mp_qr", meta.get("mp_qr", ""))))).strip()
    wechat_name = str(meta.get("wechat_name", meta.get("wechat_mp_name", meta.get("mp_name", "")))).strip()
    wechat_title = str(meta.get("wechat_title", meta.get("mp_title", "公众号"))).strip() or "公众号"
    wechat_hint = str(meta.get("wechat_hint", meta.get("mp_hint", "微信扫一扫，关注公众号"))).strip() or "微信扫一扫，关注公众号"

    def sanitize_img_src(u: str) -> str:
        u = (u or "").strip()
        if not u:
            return ""
        p = urlparse(u)
        if p.scheme:
            return u if p.scheme.lower() in {"http", "https"} else ""
        if u.startswith(("/", "./", "../")):
            return u
        return ""

    wechat_block = ""
    qr_src = sanitize_img_src(wechat_qr)
    if qr_src:
        show_name = wechat_name or "微信公众号"
        wechat_block = (
            '<div class="wechat">'
            '<div class="wechat-title">'
            '<span class="wechat-badge">WeChat</span>'
            f'<span>{esc(wechat_title)}</span>'
            '</div>'
            f'<a href="{esc(qr_src)}" target="_blank" rel="noopener noreferrer">'
            f'<img src="{esc(qr_src)}" alt="{esc(show_name)}" loading="lazy" />'
            '</a>'
            f'<div class="wechat-name">{esc(show_name)}</div>'
            f'<div class="wechat-hint">{esc(wechat_hint)}</div>'
            '</div>'
        )

    pdf_btn = ""
    if blogurl:
        pdf_btn = '<a class="btn primary" href="{}" target="_blank" rel="noopener">Research Blog</a>'.format(esc(blogurl))


    now = datetime.now()

    def content_file_for(href: str) -> str:
        # Map href (e.g. papers.html or sub/papers.html) -> _content/<...>.content.html
        base, _ext = os.path.splitext(href)
        if base.startswith('./'):
            base = base[2:]
        return os.path.join(CONTENT_DIR, base + '.content.html')

    def extract_body_inner(s: str) -> str:
        m = re.search(r'<body[^>]*>(.*?)</body>', s, flags=re.I|re.S)
        if m:
            return m.group(1).strip()
        return (s or '').strip()

    def placeholder_content(href: str, title: str) -> str:
        t = esc(title)
        cp = esc(content_file_for(href))
        hf = esc(href)
        return (
            f"<h2>{t}</h2>"
            f"<p class=\"muted\">This page is a shell. Put the right-pane content in <code>{cp}</code> (HTML fragment or full HTML).</p>"
            f"<p class=\"muted\">If you already had <code>{hf}</code>, the first run copies it into <code>{cp}</code> automatically.</p>"
        )

    def ensure_content_source(href: str, title: str) -> str:
        content_path = content_file_for(href)

        # Backward-compat: if legacy '<base>.content.html' exists in root, move it into CONTENT_DIR
        base, _ext = os.path.splitext(href)
        if base.startswith('./'):
            base = base[2:]
        legacy = base + '.content.html'
        if (not os.path.exists(content_path)) and os.path.exists(legacy):
            os.makedirs(os.path.dirname(content_path) or '.', exist_ok=True)
            try:
                os.replace(legacy, content_path)
            except OSError:
                with open(legacy, 'r', encoding='utf-8', errors='ignore') as fsrc:
                    old = fsrc.read()
                with open(content_path, 'w', encoding='utf-8') as fdst:
                    fdst.write(old)

        if os.path.exists(content_path):
            return content_path
        d = os.path.dirname(content_path)
        if d:
            os.makedirs(d, exist_ok=True)

        # If an old page file exists (and is NOT one of our generated shells), copy it into *.content.html
        if os.path.exists(href):
            with open(href, 'r', encoding='utf-8', errors='ignore') as f:
                old = f.read()
            if 'CV_SHELL_GENERATED' not in old:
                with open(content_path, 'w', encoding='utf-8') as f:
                    f.write(old)
            else:
                with open(content_path, 'w', encoding='utf-8') as f:
                    f.write(placeholder_content(href, title))
        else:
            with open(content_path, 'w', encoding='utf-8') as f:
                f.write(placeholder_content(href, title))

        return content_path

    def render_page(out_filename: str, sections_list: List[str]) -> None:
        out_dir = os.path.dirname(out_filename)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)

        out_html = HTML_DOC.safe_substitute(
            PAGE_TITLE=esc(str(meta.get('title', 'CV'))),
            STYLE=STYLE.strip('\n'),
            AVATAR=esc(avatar),
            NAME=esc(name),
            ROLE=esc(role),
            TAGS_BLOCK=tags_block,
            BANNER_BLOCK=banner_block,
            CONTACT_BLOCK=contact_block,
            WECHAT_BLOCK=wechat_block,
            PDF_BTN=pdf_btn,
            SUBTITLE=esc(subtitle),
            NAVBAR=build_navbar(out_filename),
            UPDATED=now.strftime('%Y-%m-%d'),
            YEAR=str(now.year),
            SECTIONS='\n'.join(sections_list),
        )

        with open(out_filename, 'w', encoding='utf-8') as f:
            f.write(out_html)

        print('✅ 生成成功：{}'.format(out_filename))

    # 1) Home page
    render_page(out_path, sections_out)

    
    # 2) Pages for each internal nav link (local *.html)
    # If a nav item provides 'section'/'sections', we render those CV.md sections into the page.
    # Otherwise, we keep the old behavior: treat the page as a "shell" that wraps external HTML from _content/*.content.html.
    for pg in internal_pages:
        title = str(pg.get('title', '')).strip()
        href = str(pg.get('href', '')).strip()
        raw_sections_cfg = pg.get('sections', []) or []
        configured_md_sections = isinstance(raw_sections_cfg, list) and len(raw_sections_cfg) > 0
        sections_cfg = resolved_section_map.get(href, []) if configured_md_sections else raw_sections_cfg
        if not title or not href:
            continue
        if href in ('index.html', './index.html'):
            continue

        # Mode A: CV.md-driven page
        if configured_md_sections:
            if not sections_cfg:
                page_sections = [section_html(title, '<p class="muted">（该页面已配置 sections，但未匹配到任何可渲染的标题；如果你使用了 "*"，它只会分配给 nav 中第一个包含 "*" 的页面）</p>')]
                render_page(href, page_sections)
                continue

            page_sections: List[str] = []
            for sec_title in sections_cfg:
                st = str(sec_title).strip()
                if not st:
                    continue
                sec_body = secs.get(st, "")
                if not sec_body.strip():
                    page_sections.append(section_html(st, '<p class="muted">（未在 CV.md 中找到该标题的内容）</p>'))
                    continue
                if st == PUB_SECTION_TITLE:
                    page_sections.append(section_html(st, render_publications(sec_body)))
                else:
                    page_sections.append(section_html(st, render_simple_md(sec_body)))
            if not page_sections:
                page_sections = [section_html(title, '<p class="muted">（未配置任何可渲染的标题）</p>')]
            render_page(href, page_sections)
            continue

        # Mode B: External HTML content wrapped into our style
        content_path = ensure_content_source(href, title)
        with open(content_path, 'r', encoding='utf-8', errors='ignore') as f:
            raw = f.read()
        body = extract_body_inner(raw)

        page_sections = [section_html(title, '<div class="ext-content">' + body + '</div>')]
        render_page(href, page_sections)




if __name__ == "__main__":
    main()
