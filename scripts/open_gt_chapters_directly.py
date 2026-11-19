#!/usr/bin/env python3
"""Link the six GT chapter names straight to their official outcomes.

PreTeXt can generate separate chapter landing and Introduction pages.
Find the actual page containing the generated, verbatim learning outcome
instead of assuming a particular suffix. The old landing URLs redirect.
No curriculum text is rewritten.
"""
from pathlib import Path

site = Path("output/web")
chapters = {
    1: "chapter-gt1-measurement",
    2: "chapter-gt2-shapes-solids",
    3: "chapter-gt3-synthetic-geometry",
    4: "chapter-trigonometry",
    5: "chapter-gt5-coordinate-plane",
    6: "chapter-gt6-transformations",
}

destinations = {}
for number, slug in chapters.items():
    old_name = slug + ".html"
    old = site / old_name
    if not old.is_file():
        raise SystemExit("Missing GT chapter landing page: " + old_name)
    outcome_id = f'id="jc-outcomes-geometry-gt{number}"'
    candidates = [p for p in (site / f"{slug}-2.html", old)
                  if p.is_file() and outcome_id in p.read_text(encoding="utf-8")]
    if len(candidates) != 1:
        raise SystemExit(f"Cannot uniquely locate GT.{number} outcome in chapter HTML")
    destination = candidates[0].name
    if destination != old_name:
        destinations[old_name] = destination

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
            raise SystemExit("Invalid chapter landing page: " + old_name)
        old.write_text(content.replace("</head>", f"  {tag}\n</head>", 1),
                       encoding="utf-8")
    print(f"Direct GT entry: {old_name} -> {new_name}")
print(f"Updated {edited} HTML pages with direct GT chapter links.")
