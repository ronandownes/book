#!/usr/bin/env python3
"""Build navigable, source-only learning-outcome pages for JC and LC Ordinary Level.

All 55 official outcomes are retained. No slides, teaching remarks, examples,
editorial introductions or injected interactivity.
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
    """Turn a source table into a Learning Outcomes chapter and numbered sections.

    Preserve the previously published overview URL as the chapter id.
    The source table is read only; its official paragraphs are duplicated into
    an unabridged chapter overview and into each individual section.
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
        label = etree.SubElement(entry, "p")
        etree.SubElement(label, "alert").text = code + (" — " + heading if heading else "")
        append_official(entry, official)

        section = etree.SubElement(chapter, "section")
        section.set(ID, prefix + "-" + slug)
        etree.SubElement(section, "title").text = code + (" — " + heading if heading else "")
        append_official(section, official)
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
etree.SubElement(opening, "p").text = (
    "The Unifying Strand runs through every Junior Cycle mathematics topic. "
    "Rather than being a separate collection of topics, its 13 learning outcomes "
    "underpin the ideas, procedures and reasoning developed throughout the course."
)
etree.SubElement(opening, "p").text = (
    "Its six connected elements are building blocks (U.1–U.3), representation (U.4), "
    "connections (U.5–U.6), problem solving (U.7–U.10), generalisation and proof "
    "(U.11–U.12), and communication (U.13). They develop together: students can "
    "use procedures, represent ideas, explore connections, solve problems and "
    "explain their reasoning within the same task."
)
etree.SubElement(opening, "p").text = (
    "The official U.1–U.13 learning outcomes are listed individually below. "
    "Revisit these skills whenever you encounter a new topic or need to strengthen "
    "a mathematical foundation."
)
seen = []
for row in intro.findall(".//row"):
    cells = row.findall("cell")
    if len(cells) != 2:
        continue
    code = "".join(cells[0].itertext()).strip()
    if not re.fullmatch(r"U\.\d+", code):
        continue
    section = etree.SubElement(unifying, "section")
    section.set(ID, "jc-outcomes-unifying-" + code.lower().replace(".", ""))
    etree.SubElement(section, "title").text = code
    para = etree.Element("p")
    para.text = cells[1].text
    for child in cells[1]:
        para.append(deepcopy(child))
    section.append(para)
    register(section, code, "Junior Cycle", "Unifying Strand")
    seen.append(code)
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
