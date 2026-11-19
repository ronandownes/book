#!/usr/bin/env python3
"""Keep old GT.1, GT.2, GT.5, GT.6 URLs working after the navigation change.

Those outcomes are still fully reproduced in the official Geometry overview,
but their redundant individual source sections have been removed.
"""
from html import escape
from pathlib import Path

site = Path("output/web")
target = site / "jc-outcomes-geometry.html"
if not target.is_file():
    raise SystemExit("Missing Geometry outcomes overview; refusing redirects.")

for number in (1, 2, 5, 6):
    old = site / f"jc-outcomes-geometry-gt{number}.html"
    if old.exists():
        raise SystemExit(f"Old page unexpectedly still exists: {old}")
    fragment = f"jc-geometry-overview-gt{number}"
    url = f"jc-outcomes-geometry.html#{fragment}"
    name = f"GT.{number}"
    old.write_text(
        "<!doctype html>\n"
        '<html lang="en"><head><meta charset="utf-8">\n'
        f'<title>{escape(name)} learning outcome</title>\n'
        f'<meta http-equiv="refresh" content="0;url={escape(url, quote=True)}">\n'
        f'<link rel="canonical" href="{escape(url, quote=True)}">\n'
        '</head><body>\n'
        f'<p>{escape(name)} has moved to the <a href="{escape(url, quote=True)}">complete Geometry and Trigonometry learning-outcome overview</a>.</p>\n'
        '</body></html>\n',
        encoding="utf-8",
    )
    print(f"Redirected {old.name} to {url}")
