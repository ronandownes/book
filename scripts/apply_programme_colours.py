#!/usr/bin/env python3
"""Attach programme-aware sidebar colours to generated PreTeXt HTML.

Derive all chapter links from the resolved PreTeXt source: new chapters inherit
their programme palette automatically without hand-updating JavaScript.
"""
from __future__ import annotations
import json
from pathlib import Path
from lxml import etree

ROOT = Path("output/web")
SOURCE = Path("source/main.ptx")
ASSETS = Path("assets")

PARTS = {
    "part-jc-introduction": "intro",
    "part-jc-number": "number",
    "part-jc-geometry": "geometry",
    "part-jc-trigonometry": "trigonometry",
    "part-jc-algebra": "algebra",
    "part-jc-statistics": "statistics",
    "part-jc-assessment": "assessment",
    "part-transition-year": "ty",
    "part-lc-ol-introduction": "intro",
    "part-lc-ol-statistics": "lc-statistics",
    "part-lc-ol-geometry": "lc-geometry",
    "part-lc-ol-number": "lc-number",
    "part-lc-ol-algebra": "lc-algebra",
    "part-lc-ol-functions": "lc-functions",
}
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"

def main() -> None:
    doc = etree.parse(str(SOURCE))
    doc.xinclude()
    chapters: dict[str, str] = {}
    missing = []
    for part in doc.getroot().iter("part"):
        part_id = part.get(XML_ID)
        if part_id not in PARTS:
            continue
        palette = PARTS[part_id]
        for chapter in part.findall("./chapter"):
            chapter_id = chapter.get(XML_ID)
            if not chapter_id:
                raise RuntimeError(f"Chapter without xml:id in {part_id}")
            name = f"{chapter_id}.html"
            if not (ROOT / name).is_file():
                missing.append(name)
            else:
                chapters[name] = palette
    if missing:
        raise RuntimeError("Expected chapter HTML files not built: " + ", ".join(missing))
    built_parts = {part.get(XML_ID) for part in doc.getroot().iter("part")}
    if built_parts != set(PARTS):
        raise RuntimeError(f"Expected JC Unifying Strand, five Junior Cycle content Parts, assessment, TY and LC OL Parts, found: {sorted(built_parts)}")
    if len(chapters) < 10:
        raise RuntimeError(f"Unexpectedly few published teaching chapters: {len(chapters)}")

    css = (ASSETS / "programme-colours.css").read_text(encoding="utf-8")
    js = (ASSETS / "programme-colours.js").read_text(encoding="utf-8")
    marker = "__MATHS_CHAPTERS__"
    if js.count(marker) != 1:
        raise RuntimeError("Missing or repeated chapter manifest placeholder.")
    js = js.replace(marker, json.dumps(chapters, separators=(",", ":"), ensure_ascii=True))

    (ROOT / "programme-colours.css").write_text(css, encoding="utf-8")
    (ROOT / "programme-colours.js").write_text(js, encoding="utf-8")
    # Asset version changed to invalidate previously cached CSS and JavaScript.
    style_tag = '<link rel="stylesheet" href="programme-colours.css?v=4" data-maths-programme="colour"/>'
    script_tag = '<script defer src="programme-colours.js?v=3" data-maths-programme="colour"></script>'
    changed = 0
    for page in ROOT.glob("*.html"):
        text = page.read_text(encoding="utf-8")
        if "</head>" not in text or "</body>" not in text:
            continue
        # Remove any earlier version without affecting unrelated app scripts.
        import re
        text = re.sub(r'<link[^>]+data-maths-programme="colour"[^>]*>', "", text)
        text = re.sub(r'<script[^>]+data-maths-programme="colour"[^>]*></script>', "", text)
        text = text.replace("</head>", "  " + style_tag + "\n</head>", 1)
        text = text.replace("</body>", "  " + script_tag + "\n</body>", 1)
        page.write_text(text, encoding="utf-8")
        changed += 1
    if not changed:
        raise RuntimeError("No textbook HTML pages received the programme colour assets.")
    print(f"Colour mapping: {len(chapters)} chapters in {len(PARTS)} parts; annotated {changed} pages.")
    print("Part colours: saturated. Chapter colours: matching pastel. Section colours: unmodified white.")

if __name__ == "__main__":
    main()
