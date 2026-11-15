#!/usr/bin/env python3
"""Enable one lightweight accessible enlargement viewer on every built HTML page."""
from pathlib import Path
import re
import shutil

root = Path("output/web")
assets = Path("assets")
if not (root / "index.html").is_file():
    raise SystemExit("Missing PreTeXt HTML output.")
for name in ("diagram-zoom.js", "diagram-zoom.css"):
    shutil.copy2(assets / name, root / name)
script = '<script defer src="diagram-zoom.js?v=1" data-maths-diagram-zoom="yes"></script>'
style = '<link rel="stylesheet" href="diagram-zoom.css?v=1" data-maths-diagram-zoom="yes"/>'
count = 0
for page in root.glob("*.html"):
    html = page.read_text(encoding="utf-8")
    if "</head>" not in html or "</body>" not in html:
        continue
    html = re.sub(r'<script[^>]+data-maths-diagram-zoom="yes"[^>]*></script>', "", html)
    html = re.sub(r'<link[^>]+data-maths-diagram-zoom="yes"[^>]*>', "", html)
    html = html.replace("</head>", "  " + style + "\n</head>", 1)
    html = html.replace("</body>", "  " + script + "\n</body>", 1)
    page.write_text(html, encoding="utf-8")
    count += 1
if count < 10:
    raise SystemExit("Diagram zoom only reached " + str(count) + " pages.")
print("Enabled accessible diagram zoom on " + str(count) + " HTML pages.")
