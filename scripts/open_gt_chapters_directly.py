#!/usr/bin/env python3
"""Open GT.3 and GT.4 directly at their official learning outcomes.

PreTeXt normally creates a chapter landing page and a separate
Introduction page. Redirect the landing URL and rewrite navigation
links so readers reach the blue outcome immediately. No source XML
or other chapters are changed.
"""
from pathlib import Path

site = Path("output/web")
destinations = {
    "chapter-gt3-synthetic-geometry.html":
        "chapter-gt3-synthetic-geometry-2.html",
    "chapter-trigonometry.html":
        "chapter-trigonometry-2.html",
}

for old_name, new_name in destinations.items():
    old = site / old_name
    new = site / new_name
    if not old.exists() or not new.exists():
        raise SystemExit(f"Missing chapter pages: {old_name} or {new_name}")

edited = 0
for page in site.glob("*.html"):
    original = page.read_text(encoding="utf-8")
    content = original
    for old_name, new_name in destinations.items():
        content = content.replace(f'href="{old_name}"', f'href="{new_name}"')
    if content != original:
        page.write_text(content, encoding="utf-8")
        edited += 1

for old_name, new_name in destinations.items():
    old = site / old_name
    content = old.read_text(encoding="utf-8")
    marker = 'data-gt-direct-entry="1"'
    if marker not in content:
        tag = (f'<meta http-equiv="refresh" content="0;url={new_name}" '
               f'{marker} />')
        if "</head>" not in content:
            raise SystemExit(f"Invalid chapter page: {old_name}")
        old.write_text(content.replace("</head>", f"  {tag}\n</head>", 1),
                       encoding="utf-8")
    print(f"Direct entry: {old_name} → {new_name}")
print(f"Rewrote direct GT chapter links across {edited} PreTeXt pages.")
