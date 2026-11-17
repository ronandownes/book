#!/usr/bin/env python3
"""Add classroom displays to the two native TY pages; keep their text authoritative."""
from pathlib import Path
import shutil
from lxml import html

root = Path("output/web")
pages = {"ty-news-story": 18, "ty-number-theory-projects": 20}
for stem, expected in pages.items():
    path = root / f"{stem}.html"
    source = path.read_text(encoding="utf-8")
    doc = html.fromstring(source)
    sections = doc.xpath(f'//*[@id="{stem}"]')
    if len(sections) != 1:
        raise SystemExit(f"Missing unique TY section: {stem}")
    slides = sections[0].xpath('./*[contains(concat(" ", normalize-space(@class), " "), " subsection ")]')
    if len(slides) != expected:
        raise SystemExit(f"Expected {expected} display entries on {stem}; found {len(slides)}")
    if "</head>" not in source or "</body>" not in source:
        raise SystemExit(f"Incomplete TY page: {stem}")
    if 'data-ty-display="1"' not in source:
        css = '<link rel="stylesheet" href="ty-display.css?v=2" data-ty-display="1"/>'
        js = '<script defer src="ty-display.js?v=2" data-ty-display="1"></script>'
        source = source.replace("</head>", "  " + css + "\n</head>", 1)
        source = source.replace("</body>", "  " + js + "\n</body>", 1)
        path.write_text(source, encoding="utf-8")
for name in ("ty-display.css", "ty-display.js"):
    shutil.copy2(Path("assets") / name, root / name)
print("Enabled 18 visual story slides and 20 number theory project displays.")
