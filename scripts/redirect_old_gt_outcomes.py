#!/usr/bin/env python3
"""Preserve all six former GT.1–GT.6 section URLs as redirects.

Official text exists in one canonical source and appears in the overview
and chapter openings; the old individual GT sections are not regenerated.
"""
from html import escape
from pathlib import Path

site = Path("output/web")
if not (site / "jc-outcomes-geometry.html").is_file():
    raise SystemExit("Missing GT outcome overview")

chapters = {
    1: "chapter-gt1-measurement",
    2: "chapter-gt2-shapes-solids",
    3: "chapter-gt3-synthetic-geometry",
    4: "chapter-trigonometry",
    5: "chapter-gt5-coordinate-plane",
    6: "chapter-gt6-transformations",
}
for number, slug in chapters.items():
    old = site / f"jc-outcomes-geometry-gt{number}.html"
    if old.exists():
        raise SystemExit(f"Redundant individual GT page unexpectedly still exists: {old}")
    needle = f'id="jc-outcomes-geometry-gt{number}"'
    pages = [p for p in (site / f"{slug}-2.html", site / f"{slug}.html")
             if p.is_file() and needle in p.read_text(encoding="utf-8")]
    if len(pages) != 1:
        raise SystemExit(f"Cannot locate exact GT.{number} chapter learning outcome")
    url = pages[0].name + f"#jc-outcomes-geometry-gt{number}"
    label = f"GT.{number}"
    old.write_text(
        "<!doctype html>\n"
        '<html lang="en"><head><meta charset="utf-8">\n'
        f'<title>{escape(label)} learning outcome</title>\n'
        f'<meta http-equiv="refresh" content="0;url={escape(url, quote=True)}">\n'
        f'<link rel="canonical" href="{escape(url, quote=True)}">\n'
        "</head><body>\n"
        f'<p><a href="{escape(url, quote=True)}">Open {escape(label)} learning outcome</a>.</p>\n'
        "</body></html>\n",
        encoding="utf-8",
    )
    print(f"Legacy {label} link -> {url}")
