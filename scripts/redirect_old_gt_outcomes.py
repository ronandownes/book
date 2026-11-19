#!/usr/bin/env python3
"""Keep all six historic GT outcome URLs working after the navigation change.

All six statements remain in the official overview. GT.3 and GT.4 now
also occur at the top of their corresponding teaching chapters.
"""
from html import escape
from pathlib import Path

site = Path("output/web")
target = site / "jc-outcomes-geometry.html"
if not target.is_file():
    raise SystemExit("Missing Geometry outcomes overview; refusing redirects.")

for number in range(1, 7):
    old = site / f"jc-outcomes-geometry-gt{number}.html"
    if old.exists():
        raise SystemExit(f"Old page unexpectedly still exists: {old}")
    if number == 3:
        url = "chapter-gt3-synthetic-geometry.html#jc-outcomes-geometry-gt3"
    elif number == 4:
        url = "chapter-trigonometry.html#jc-outcomes-geometry-gt4"
    else:
        url = f"jc-outcomes-geometry.html#jc-geometry-overview-gt{number}"
    name = f"GT.{number}"
    old.write_text(
        "<!doctype html>\n"
        '<html lang="en"><head><meta charset="utf-8">\n'
        f'<title>{escape(name)} learning outcome</title>\n'
        f'<meta http-equiv="refresh" content="0;url={escape(url, quote=True)}">\n'
        f'<link rel="canonical" href="{escape(url, quote=True)}">\n'
        '</head><body>\n'
        f'<p>{escape(name)} has moved to the <a href="{escape(url, quote=True)}">appropriate Geometry and Trigonometry learning outcome</a>.</p>\n'
        '</body></html>\n',
        encoding="utf-8",
    )
    print(f"Redirected {old.name} to {url}")
