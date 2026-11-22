"""Generate all Appendix B source pages as PreTeXt figure sections before the book build.

The SVGs preserve original text and original diagrams. This is a source-page
facsimile within PreTeXt, NOT yet a fully semantic per-theorem transcription.
"""
from pathlib import Path
from urllib.request import Request, urlopen
import fitz
import xml.etree.ElementTree as ET

URL = "https://www.curriculumonline.ie/getmedia/6a7f1ff5-9b9e-4d71-8e1f-6d4f932191db/JC_Mathematics_Specification.pdf"
PDF = Path("assets/syllabus/JC_Mathematics_Specification.pdf")
FIGURES = Path("assets/geometry-appendix-b")
OUTPUT = Path("source/appendix-b-native")
PDF.parent.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)
OUTPUT.mkdir(parents=True, exist_ok=True)

if not PDF.exists():
    with urlopen(Request(URL, headers={"User-Agent": "Irish School Maths educational reference"}), timeout=120) as response:
        PDF.write_bytes(response.read())
doc = fitz.open(PDF)
if len(doc) != 76 or "Geometry for" not in doc[26].get_text() or "Government of Ireland" not in doc[75].get_text():
    raise SystemExit("Unexpected specification: stopping rather than publishing incorrect source")

# Pages are numbered as in the parent JC specification. Every page is included exactly once.
groups = [
    ("at-a-glance", "At a glance: definitions, axioms, theorems and corollaries", 27, 29),
    ("introduction", "1 Introduction", 30, 30),
    ("system-guiding-principles", "2–3 Formal system and guiding principles", 31, 33),
    ("level-two-account", "4 Outline of the Level 2 Account", 34, 34),
    ("terms", "5 Terms", 35, 35),
    ("theory", "6 The Theory", 36, 36),
    ("length-distance", "6.1 Length and Distance", 37, 37),
    ("angles", "6.2 Angles", 38, 38),
    ("degrees", "6.3 Degrees", 39, 39),
    ("congruent-triangles", "6.4 Congruent Triangles", 40, 41),
    ("parallels", "6.5 Parallels", 42, 48),
    ("perpendicular-quadrilaterals", "6.6–6.7 Perpendicular Lines and Quadrilaterals", 49, 51),
    ("ratios-similarity", "6.8 Ratios and Similarity", 52, 67),
    ("constructions", "7 Constructions to Study", 68, 69),
    ("teaching", "8 Teaching Approaches", 70, 71),
    ("jcol", "9 JCOL Content", 72, 72),
    ("jchl", "10 Additional Content for JCHL", 73, 73),
    ("leaving-certificate", "11–13 Leaving Certificate geometry syllabus content", 74, 75),
    ("copyright", "Source copyright information", 76, 76),
]
assert [n for _,_,a,b in groups for n in range(a,b+1)] == list(range(27,77))

for slug, title, first, last in groups:
    root = ET.Element("section", {"{http://www.w3.org/XML/1998/namespace}id": "geometry-b-source-"+slug})
    ET.SubElement(root, "title").text = title
    for n in range(first, last+1):
        page = doc[n-1]
        svg = page.get_svg_image(text_as_path=False)
        svgpath = FIGURES / f"official-page-{n}.svg"
        svgpath.write_text(svg, encoding="utf-8")
        figure = ET.SubElement(root, "figure", {"{http://www.w3.org/XML/1998/namespace}id": f"geometry-b-page-{n}"})
        ET.SubElement(figure, "caption").text = f"Official Appendix B, source page {n}"
        ET.SubElement(figure, "image", {"source": f"geometry-appendix-b/official-page-{n}.svg", "width": "100%"})
    ET.ElementTree(root).write(OUTPUT / (slug+".ptx"), encoding="unicode", xml_declaration=True)

assert len(list(FIGURES.glob("official-page-*.svg"))) == 50
assert len(list(OUTPUT.glob("*.ptx"))) == len(groups)
print("Appendix B: generated 50 vector pages in",len(groups),"native PreTeXt sections")
