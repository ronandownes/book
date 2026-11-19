#!/usr/bin/env python3
"""Validate official wording and independently navigable outcome pages.

All 55 official statements remain in the book. The six geometry outcomes
appear in their overview and all six dedicated GT chapter openings.
"""
from pathlib import Path
import json
from lxml import etree, html

site = Path("output/web")
manifest = json.loads(
    Path("source/learning-outcomes-pages.json").read_text(encoding="utf-8")
)
entries = manifest["pages"]
if len(entries) != 49:
    raise ValueError("Exactly 49 independent outcome pages are expected; all 55 official outcomes must remain in the book")

groups = {}
for item in entries:
    page_path = site / (item["id"] + ".html")
    if not page_path.is_file():
        raise ValueError("Missing outcome page: " + page_path.name)
    content = page_path.read_text(encoding="utf-8")
    parsed = html.fromstring(content)
    sections = parsed.xpath("//section[@id=$ident]", ident=item["id"])
    if len(sections) != 1:
        raise ValueError("Native section missing: " + page_path.name)
    section = sections[0]
    statements = section.xpath(
        './div[contains(concat(" ", normalize-space(@class), " "), " para ")]'
    )
    if not statements:
        raise ValueError("Missing official statement: " + page_path.name)
    if item["code"] not in section.text_content():
        raise ValueError("Incorrect outcome code: " + page_path.name)
    if section.xpath(".//*[contains(concat(' ', normalize-space(@class), ' '), ' remark ')]"):
        raise ValueError("Teaching remark in " + page_path.name)
    if "jc-algebra-outcome-slides" in content or 'data-outcome-display=' in content:
        raise ValueError("Outcome presentation unexpectedly present: " + page_path.name)
    groups.setdefault(item["group"] + ": " + item["course"], 0)
    groups[item["group"] + ": " + item["course"]] += 1

# Verify that outcome chapters open with the complete original wording,
# followed by *only* their numbered sections.
book = etree.parse("source/main.ptx")
book.xinclude()
ids = book.xpath(
    "//@xml:id", namespaces={"xml": "http://www.w3.org/XML/1998/namespace"}
)
if len(ids) != len(set(ids)):
    raise ValueError("Duplicate XML ids")
for item in entries:
    if ids.count(item["id"]) != 1:
        raise ValueError("Outcome missing from book: " + item["id"])

for part in book.findall(".//part"):
    for chapter in part.findall("chapter"):
        children = chapter.findall("section")
        if not children or "Learning Outcomes" not in (chapter.findtext("title") or ""):
            continue
        if any(node.tag in {"remark", "figure", "interactive"} for node in chapter.iter()):
            raise ValueError("Non-official content in " + (chapter.get("{http://www.w3.org/XML/1998/namespace}id") or "?"))
        intro = chapter.find("introduction")
        if intro is None or intro.find("ol") is None:
            raise ValueError("Missing complete-text overview in " + (chapter.get("{http://www.w3.org/XML/1998/namespace}id") or "?"))
# The GT.1–GT.6 statements occur in full in the overview, but not as six
# redundant nested pages. GT.3 and GT.4 preserve their original section ids.
geometry = book.xpath(".//chapter[@xml:id='jc-outcomes-geometry']", namespaces={"xml": "http://www.w3.org/XML/1998/namespace"})
if len(geometry) != 1:
    raise ValueError("Geometry learning-outcome overview missing")
if geometry[0].findall("section"):
    raise ValueError("Geometry overview must not repeat its six outcomes as sections")
listed = geometry[0].findall("./introduction/ol/li")
if len(listed) != 6:
    raise ValueError("All six GT outcomes must remain readable in the overview")
for code in range(1, 7):
    if f"GT.{code}" not in "".join(listed[code - 1].itertext()):
        raise ValueError(f"Missing GT.{code} official statement")
# Verify every character and inline annotation in the official statements
# is obtained from one source, with no second hand-authored transcription.
chapters = {
    1: "chapter-gt1-measurement",
    2: "chapter-gt2-shapes-solids",
    3: "chapter-gt3-synthetic-geometry",
    4: "chapter-trigonometry",
    5: "chapter-gt5-coordinate-plane",
    6: "chapter-gt6-transformations",
}

def exact_xml(element):
    return (
        etree.QName(element).localname,
        element.text,
        tuple(sorted(element.attrib.items())),
        tuple((exact_xml(child), child.tail) for child in element),
    )

for number, chapter_id in chapters.items():
    found = book.xpath(".//chapter[@xml:id=$target]", target=chapter_id,
                       namespaces={"xml": "http://www.w3.org/XML/1998/namespace"})
    if len(found) != 1:
        raise ValueError(f"Expected exactly one GT.{number} chapter")
    introduction = found[0].find("introduction")
    if introduction is None:
        raise ValueError(f"Missing GT.{number} introduction")
    blocks = [child for child in introduction if child.tag != "title"]
    if not blocks or blocks[0].tag != "blockquote":
        raise ValueError(f"GT.{number} must open with the official outcome")
    quote = blocks[0]
    if quote.get("{http://www.w3.org/XML/1998/namespace}id") != f"jc-outcomes-geometry-gt{number}":
        raise ValueError(f"Incorrect GT.{number} quotation ID")
    source_p = listed[number - 1].findall("p")[1:]
    quoted_p = quote.findall("p")[1:]
    if not source_p or list(map(exact_xml, source_p)) != list(map(exact_xml, quoted_p)):
        raise ValueError(f"GT.{number} statement differs from the overview: NOT verbatim")
    if number == 3 and any(sec.find("objectives") is None for sec in found[0].findall("section")):
        raise ValueError("GT.3 teaching section missing Learning Intentions")

print("Validated all 55 official outcomes, 49 standalone pages and six verbatim GT chapter quotations.")
