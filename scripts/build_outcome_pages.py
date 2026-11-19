#!/usr/bin/env python3
"""Build official learning-outcome overviews and navigable reference pages.

All 55 official outcomes remain in the book, but only 51 have individual
pages: GT.1, GT.2, GT.5 and GT.6 are held in the geometry overview pending
dedicated teaching chapters. Official statements remain unchanged.
"""
from copy import deepcopy
from pathlib import Path
import json
import re
from lxml import etree

ROOT = Path("source")
ID = "{http://www.w3.org/XML/1998/namespace}id"
manifest = {"pages": [], "counts": {}}

def save(node, filename):
    (ROOT / filename).write_bytes(
        etree.tostring(node, encoding="utf-8",
                       xml_declaration=True, pretty_print=True)
    )

def register(section, code, course, group):
    if section.find("remark") is not None:
        raise ValueError("Teaching remark in official outcome: " + code)
    manifest["pages"].append({
        "id": section.get(ID), "code": code, "course": course,
        "group": group, "title": section.findtext("title")
    })

def append_official(parent, paragraphs):
    if not paragraphs:
        raise ValueError("Official outcome without statements")
    original = [etree.tostring(p, with_tail=False) for p in paragraphs]
    for paragraph in paragraphs:
        parent.append(deepcopy(paragraph))
    appended = [etree.tostring(p, with_tail=False) for p in parent.findall("p")[-len(paragraphs):]]
    if original != appended:
        raise ValueError("Official outcome transcription changed")

def chapter_from_table(path, course, group, expected, section_id):
    """Create the authoritative overview and optional individual outcome pages.

    Geometry keeps all six statements in its overview, with GT.3 and GT.4
    provided as generated sections of their *teaching* chapters instead of
    duplicating all six underneath the overview in the contents menu.
    Other strands retain their original individual outcome sections.
    """
    original = etree.parse(str(path)).getroot()
    rows = original.findall(".//tabular/row")[1:]
    if len(rows) != expected:
        raise ValueError(f"{group}: expected {expected} outcomes, got {len(rows)}")
    chapter = etree.Element("chapter")
    chapter.set(ID, section_id)
    etree.SubElement(chapter, "title").text = "Learning Outcomes"
    introduction = etree.SubElement(chapter, "introduction")
    listing = etree.SubElement(introduction, "ol")
    codes = []
    for row in rows:
        cells = row.findall("cell")
        if len(cells) != 2:
            raise ValueError("Unexpected source-table structure in " + group)
        left, right = cells
        labels = left.findall("p")
        if not labels:
            raise ValueError("Missing outcome code in " + group)
        code = "".join(labels[0].itertext()).strip()
        heading = " ".join("".join(x.itertext()).strip() for x in labels[1:])
        heading = re.sub(r"^" + re.escape(code) + r"\s*", "", heading).strip()
        slug = code.lower().replace(".", "") if course == "Junior Cycle" else code.replace(".", "-")
        prefix = section_id if course == "Junior Cycle" else section_id.removesuffix("-outcomes")
        official = right.findall("p")
        if not official:
            raise ValueError("Empty official outcome " + code)

        entry = etree.SubElement(listing, "li")
        if course == "Junior Cycle" and group == "Geometry and Trigonometry":
            entry.set(ID, "jc-geometry-overview-" + slug)
        label = etree.SubElement(entry, "p")
        etree.SubElement(label, "alert").text = code + (" — " + heading if heading else "")
        append_official(entry, official)

        # GT.1–GT.6 appear once in their complete overview. Teaching
        # chapters carry the official GT.3 and GT.4 statements as their
        # first sections, preserving the previously published section IDs.
        # The remaining GT outcomes stay in the overview until their
        # substantive teaching chapters are written.
        geometry = course == "Junior Cycle" and group == "Geometry and Trigonometry"
        if not geometry or code in ("GT.3", "GT.4"):
            section_parent = etree.Element("holder") if geometry else chapter
            section = etree.SubElement(section_parent, "section")
            section.set(ID, prefix + "-" + slug)
            etree.SubElement(section, "title").text = code + (" — " + heading if heading else "")
            append_official(section, official)
            if geometry and code == "GT.3":
                navigation = etree.SubElement(section, "p")
                navigation.text = "Geometry reference: "
                link = etree.SubElement(navigation, "xref")
                link.set("ref", "appendix-b-geometry")
                link.tail = " (definitions, axioms, theorems, corollaries and constructions)."
            if geometry:
                save(section, "jc-geometry-" + slug + "-outcome.ptx")
            register(section, code, course, group)
        codes.append(code)
    if len(codes) != expected or len(set(codes)) != expected:
        raise ValueError("Missing or duplicate outcomes in " + group)
    save(chapter, path.name)
    manifest["counts"][course + ": " + group] = len(codes)

# N.1–N.5 and AF.1–AF.7 are generated directly from the curriculum.
for key, group, count in [("number", "Number", 5), ("algebra", "Algebra and Functions", 7)]:
    path = ROOT / f"jc-{key}-outcomes.ptx"
    chapter = etree.parse(str(path)).getroot()
    sections = chapter.findall("section")
    if chapter.tag != "chapter" or len(sections) != count:
        raise ValueError("Incomplete " + key + " outcomes")
    for section in sections:
        match = re.match(r"(N|AF)\.\d+", section.findtext("title") or "")
        if not match:
            raise ValueError("Missing official code in " + key)
        register(section, match.group(), "Junior Cycle", group)
    if chapter.findall(".//remark") or chapter.findall(".//figure"):
        raise ValueError("Non-official content in " + key + " chapter")
    save(chapter, path.name)
    manifest["counts"]["Junior Cycle: " + group] = count

# The remaining Junior Cycle strands follow the same native hierarchy.
for key, group, count in [
    ("geometry", "Geometry and Trigonometry", 6),
    ("statistics", "Statistics and Probability", 3),
]:
    chapter_from_table(ROOT / f"jc-{key}-outcomes.ptx",
                       "Junior Cycle", group, count, f"jc-outcomes-{key}")

# LC Ordinary Level: each syllabus topic is individually navigable.
for key, group, count in [
    ("statistics", "Statistics and Probability", 7),
    ("geometry", "Geometry and Trigonometry", 4),
    ("number", "Number", 4),
    ("algebra", "Algebra", 4),
    ("functions", "Functions", 2),
]:
    chapter_from_table(ROOT / f"lc-ol-{key}-outcomes.ptx",
                       "Leaving Certificate Ordinary Level", group,
                       count, f"lc-ol-{key}-outcomes")

# The Unifying Strand table is the source; only its original statements are
# transcribed into the dedicated U.1–U.13 chapter.
intro = etree.parse(str(ROOT / "jc-introduction.ptx"))
unifying = etree.Element("chapter")
unifying.set(ID, "jc-outcomes-unifying")
etree.SubElement(unifying, "title").text = "Unifying Strand"
opening = etree.SubElement(unifying, "introduction")
# Source: NCCA, Junior Cycle Mathematics Specification (2018), p. 10.
# This is the introductory explanation supplied with the six elements, not
# a duplicate listing of the 13 official outcome statements.
etree.SubElement(opening, "p").text = (
    "This strand permeates all of the contextual strands and is composed of the "
    "six elements of the specification, which are shown below."
)
etree.SubElement(opening, "p").text = (
    "There is no specific content linked to this strand; rather, its learning "
    "outcomes underpin the rest of the specification. Each learning outcome in "
    "this strand is applicable to all of the activities and content of the other "
    "four strands—for example, students should be able to draw on all of their "
    "mathematical knowledge and skills to solve a problem or to communicate mathematics."
)
etree.SubElement(opening, "p").text = (
    "Furthermore, the elements of this strand are interdependent, so that "
    "students should develop the different skills associated with each element "
    "in tandem rather than in isolation—for example, engaging in problem-solving "
    "can help students improve their understanding of building blocks and their "
    "ability to make connections within mathematics."
)
# Preserve the compact six-element guide, followed by the full outcomes
# in one readable place. The same source rows also populate individual pages.
groups = etree.SubElement(opening, "ul")
groups.set(ID, "jc-unifying-elements")
for element, codes in [
    ("Building blocks", "U.1–U.3"),
    ("Representation", "U.4"),
    ("Connections", "U.5–U.6"),
    ("Problem solving", "U.7–U.10"),
    ("Generalisation and proof", "U.11–U.12"),
    ("Communication", "U.13"),
]:
    item = etree.SubElement(groups, "li")
    paragraph = etree.SubElement(item, "p")
    etree.SubElement(paragraph, "em").text = element
    paragraph[-1].tail = " — " + codes
# A full-text reading view directly after the six coloured labels.
# The curriculum source file remains unchanged; no outcome is transcribed
# manually here. Retain the individual sections and their established ids.
heading = etree.SubElement(opening, "p")
etree.SubElement(heading, "em").text = "Complete Unifying Strand learning outcomes"
etree.SubElement(opening, "p").text = (
    "All thirteen outcomes are reproduced below, grouped by the six elements. "
    "They are also available individually from the contents menu for classroom use."
)
full = etree.SubElement(opening, "ul")
full.set(ID, "jc-unifying-complete")
expected_groups = [
    ("Building blocks", ["U.1", "U.2", "U.3"]),
    ("Representation", ["U.4"]),
    ("Connections", ["U.5", "U.6"]),
    ("Problem solving", ["U.7", "U.8", "U.9", "U.10"]),
    ("Generalisation and proof", ["U.11", "U.12"]),
    ("Communication", ["U.13"]),
]
group_map = {code: (index, name) for index, (name, codes) in
             enumerate(expected_groups) for code in codes}
group_items = []
for name, _ in expected_groups:
    group = etree.SubElement(full, "li")
    title_p = etree.SubElement(group, "p")
    etree.SubElement(title_p, "em").text = name
    items = etree.SubElement(group, "ul")
    group_items.append(items)
seen = []
for row in intro.findall(".//row"):
    cells = row.findall("cell")
    if len(cells) != 2:
        continue
    code = "".join(cells[0].itertext()).strip()
    if not re.fullmatch(r"U\.\d+", code):
        continue
    if code not in group_map:
        raise ValueError("Unrecognised Unifying Strand learning outcome: " + code)
    # One canonical paragraph is copied to both reading views.
    para = etree.Element("p")
    para.text = cells[1].text
    for child in cells[1]:
        para.append(deepcopy(child))
    list_item = etree.SubElement(group_items[group_map[code][0]], "li")
    list_p = etree.SubElement(list_item, "p")
    etree.SubElement(list_p, "em").text = code
    list_p[-1].tail = " — " + (para.text or "")
    for child in para:
        list_p.append(deepcopy(child))
    section = etree.SubElement(unifying, "section")
    section.set(ID, "jc-outcomes-unifying-" + code.lower().replace(".", ""))
    etree.SubElement(section, "title").text = code
    section.append(para)
    # Exact wording check for the continuous and individual copies.
    if "".join(list_p.itertext()).removeprefix(code + " — ") != "".join(para.itertext()):
        raise ValueError("Combined U outcome differs from the individual outcome: " + code)
    register(section, code, "Junior Cycle", "Unifying Strand")
    seen.append(code)
etree.SubElement(opening, "p").text = (
    "Source: National Council for Curriculum and Assessment, "
    "Junior Cycle Mathematics Specification (2018), pp. 10–14. "
    "The source specification is authoritative."
)
if seen != [f"U.{n}" for n in range(1, 14)]:
    raise ValueError("Unifying Strand must contain U.1–U.13")
save(unifying, "jc-unifying-outcomes.ptx")
manifest["counts"]["Junior Cycle: Unifying Strand"] = 13

expected = {
    f"{prefix}.{n}"
    for prefix, count in [
        ("U", 13), ("N", 5), ("GT", 6), ("AF", 7), ("SP", 3),
        ("1", 7), ("2", 4), ("3", 4), ("4", 4), ("5", 2),
    ]
    for n in range(1, count + 1)
}
actual = [entry["code"] for entry in manifest["pages"]]
if len(actual) != 55 or set(actual) != expected or len(set(actual)) != 55:
    raise ValueError("Expected 55 distinct, source-only outcome pages")
(ROOT / "learning-outcomes-pages.json").write_text(
    json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
)
print("Generated 55 source-only outcomes in navigable chapters.")
