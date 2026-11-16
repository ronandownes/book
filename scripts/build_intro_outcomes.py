#!/usr/bin/env python3
"""Produce native PreTeXt strand tables from the official curriculum sources.

Every official numbered outcome is mandatory. An unexpected source layout is an
error, not an invitation to omit material. This generates *only* LC Ordinary Level
and the four remaining Junior Cycle strands; it never imports the HL column.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from lxml import etree

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_curriculum_appendices import junior_content, leave_content

DEST = Path("source")
JUNIOR = [
    ("number", "Number", "N", 5),
    ("geometry", "Geometry and Trigonometry", "GT", 6),
    ("algebra", "Algebra and Functions", "AF", 7),
    ("statistics", "Statistics and Probability", "SP", 3),
]
LEAVING = [
    ("statistics", "Statistics and Probability", "1", 7),
    ("geometry", "Geometry and Trigonometry", "2", 4),
    ("number", "Number", "3", 4),
    ("algebra", "Algebra", "4", 4),
    ("functions", "Functions", "5", "2"),
]

# These lead sentences are checked against the printed NCCA 2018 specification,
# pp. 15-20. The website's HTML lists subparts but may omit these lead sentences.
LEADS = {
    "number": [
        "Investigate the representation of numbers and arithmetic operations so that they can:",
        "Investigate equivalent representations of rational numbers so that they can:",
        "Investigate situations involving proportionality so that they can:",
        "Analyse numerical patterns in different ways, including making out tables and graphs, and continue such patterns.",
        "Explore the concept of a set so that they can:",
    ],
    "geometry": [
        "Calculate, interpret, and apply units of measure and time.",
        "Investigate 2D shapes and 3D solids so that they can:",
        "Investigate the concept of proof through their engagement with geometry so that they can:",
        "Evaluate and use trigonometric ratios (sin, cos, and tan, defined in terms of right-angled triangles) and their inverses, involving angles between 0° and 90° at integer values and in decimal form.",
        "Investigate properties of points, lines and line segments in the co-ordinate plane so that they can:",
        "Investigate transformations of simple objects so that they can:",
    ],
    "algebra": [
        "Investigate patterns and relationships (linear, quadratic, doubling and tripling) in number, spatial patterns and real-world phenomena involving change so that they can:",
        "Investigate situations in which letters stand for quantities that are variable so that they can:",
        "Apply the properties of arithmetic operations and factorisation to generate equivalent expressions so that they can develop and use appropriate strategies to:",
        "Select and use suitable strategies (graphic, numeric, algebraic, trial and improvement, working backwards) for finding solutions to:",
        "Generate quadratic equations given integer roots.",
        "Apply the relationship between operations and an understanding of the order of operations including brackets and exponents to change the subject of a formula.",
        "Investigate functions so that they can:",
    ],
    "statistics": [
        "Investigate the outcomes of experiments so that they can:",
        "Investigate random events so that they can:",
        "Carry out a statistical investigation which includes the ability to:",
    ],
}

XML_ID = "{http://www.w3.org/XML/1998/namespace}id"

def compact(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()

def cell_with_paragraphs(texts: list[etree._Element]) -> etree._Element:
    cell = etree.Element("cell")
    for p in texts:
        cp = etree.fromstring(etree.tostring(p, encoding="utf-8"))
        cp.text = compact(cp.text or "") if cp.text else cp.text
        # Preserve inline emphasis, symbols and source text, but not PDF line breaks.
        for node in cp.iter():
            if node.text: node.text = re.sub(r"\s+", " ", node.text)
            if node.tail: node.tail = re.sub(r"\s+", " ", node.tail)
        cell.append(cp)
    return cell

def add_table(section, table_id: str, title: str, rows: list[tuple[str, str, list[etree._Element]]]):
    table = etree.SubElement(section, "table")
    table.set(XML_ID, table_id)
    etree.SubElement(table, "title").text = title
    tabular = etree.SubElement(table, "tabular")
    etree.SubElement(tabular, "col", width="25%")
    etree.SubElement(tabular, "col", width="75%")
    header = etree.SubElement(tabular, "row", header="yes")
    etree.SubElement(header, "cell").text = "Outcome"
    etree.SubElement(header, "cell").text = "Students should be able to"
    for code, heading, paragraphs in rows:
        row = etree.SubElement(tabular, "row")
        first = etree.SubElement(row, "cell")
        etree.SubElement(first, "p").text = code
        if heading:
            etree.SubElement(first, "p").text = heading
        row.append(cell_with_paragraphs(paragraphs))
    return table

def write(section: etree._Element, file_name: str):
    content = etree.tostring(section, encoding="utf-8", xml_declaration=True, pretty_print=True)
    if b"<table" not in content or b"<row" not in content:
        raise RuntimeError("Empty outcomes table: " + file_name)
    (DEST / file_name).write_bytes(content)
    print(f"Generated {file_name}: {len(content)} bytes", flush=True)

def junior():
    raw = "".join(junior_content())
    root = etree.fromstring(("<root>" + raw + "</root>").encode("utf-8"))
    for key, title, prefix, expected in JUNIOR:
        chapter = root.xpath(f"./chapter[@xml:id='jc-official-{key}']",
                             namespaces={"xml":"http://www.w3.org/XML/1998/namespace"})
        if len(chapter) != 1:
            raise RuntimeError("Missing Junior Cycle " + key)
        rows = []
        parts = chapter[0].findall("section")
        if len(parts) != expected or len(LEADS[key]) != expected:
            raise RuntimeError(f"JC {key}: source has {len(parts)} outcomes, expected {expected}")
        for number, part in enumerate(parts, 1):
            code = prefix + "." + str(number)
            paragraphs = part.findall("p")
            main = etree.Element("p")
            main.text = LEADS[key][number-1]
            # The source HTML sometimes lists the main code only after its
            # subparts and sometimes omits it entirely. Use the PDF-verified
            # main sentence, preserving every separately extracted subpart.
            extras = []
            for p in paragraphs:
                t = compact("".join(p.itertext()))
                if not t:
                    continue
                if re.search(r"\b" + re.escape(code) + r"\b", t):
                    # The numbered lead is already represented by the
                    # PDF-verified statement above. Do not print it twice.
                    continue
                extras.append(p)
            rows.append((code, compact(part.findtext("title") or ""), [main, *extras]))
        wanted = [prefix+"."+str(i) for i in range(1,expected+1)]
        actual = [r[0] for r in rows]
        if actual != wanted:
            raise RuntimeError(f"JC {key}: expected {wanted}, got {actual}. Refusing incomplete publication.")
        section = etree.Element("section")
        section.set(XML_ID, f"jc-outcomes-{key}")
        etree.SubElement(section,"title").text=title
        if key in ("number","geometry","algebra","statistics"):
            etree.SubElement(section, "p").text = ("Official learning outcomes. Higher Level-only material remains "
                "distinguished in bold where marked in the NCCA source.")
        add_table(section, f"jc-outcomes-{key}-table", f"{title}: official learning outcomes", rows)
        write(section, f"jc-{key}-outcomes.ptx")
        print(f"Junior Cycle {key}: {len(rows)} complete numbered outcomes",flush=True)

def leaving():
    raw="".join(leave_content())
    root=etree.fromstring(("<root>"+raw+"</root>").encode("utf-8"))
    for key,title,prefix,count in LEAVING:
        chapter=root.xpath(f"./chapter[@xml:id='lc-official-{key}']",
                           namespaces={"xml":"http://www.w3.org/XML/1998/namespace"})
        if len(chapter)!=1:
            raise RuntimeError("Missing LC Ordinary strand "+key)
        rows=[]
        for part in chapter[0].findall("section"):
            heading=compact(part.findtext("title") or "")
            m=re.search(r"\b"+re.escape(prefix)+r"\.(\d+)\b",heading)
            if not m: raise RuntimeError(f"Missing official topic code in {key}: {heading}")
            code=prefix+"."+m.group(1)
            paragraphs=part.findall("p")
            if not paragraphs: raise RuntimeError("Missing Ordinary Level text in "+heading)
            rows.append((code,heading,paragraphs))
        unique_codes=[]
        grouped=[]
        for row in rows:
            # On multi-page topics, append continuation to the existing row.
            if row[0] in unique_codes:
                grouped[unique_codes.index(row[0])][2].extend(row[2])
            else:
                unique_codes.append(row[0]);grouped.append((row[0],row[1],list(row[2])))
        expected=[prefix+"."+str(i) for i in range(1,int(count)+1)]
        if unique_codes!=expected:
            raise RuntimeError(f"LC OL {key}: expected {expected}, got {unique_codes}. No omissions permitted.")
        section=etree.Element("section")
        section.set(XML_ID,f"lc-ol-{key}-outcomes")
        etree.SubElement(section,"title").text=title
        etree.SubElement(section,"p").text="Ordinary Level learning outcomes only, in the order of the published 2015 syllabus."
        add_table(section,f"lc-ol-{key}-table",f"{title}: Ordinary Level learning outcomes",grouped)
        write(section,f"lc-ol-{key}-outcomes.ptx")
        print(f"Leaving Certificate Ordinary Level {key}: {len(grouped)} official topics",flush=True)

if __name__=="__main__":
    junior()
    leaving()
