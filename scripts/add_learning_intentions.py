#!/usr/bin/env python3
"""Insert native, individual Learning Intentions at the start of teaching sections.

One concise intention per populated lesson.  Official NCCA and LC syllabus
tables, reference appendices and the glossary are deliberately not edited.
This build step is idempotent; it never fabricates intentions from a heading.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from lxml import etree

ROOT = Path("source")
DATA = json.loads((ROOT / "learning-intentions.json").read_text(encoding="utf-8"))
CURATED: dict[str, list[str]] = DATA["intentions"]
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
XI = "{http://www.w3.org/2001/XInclude}include"
SKIP = {"jc-introduction.ptx", "lc-ol-introduction.ptx", "shared-glossary.ptx",
        "jc-number-learning-outcomes.ptx", "jc-geometry-learning-outcomes.ptx",
        "jc-algebra-learning-outcomes.ptx", "jc-statistics-learning-outcomes.ptx"}
SKIP_PREFIXES = ("jc-number-outcomes.ptx", "jc-geometry-outcomes.ptx",
                 "jc-algebra-outcomes.ptx", "jc-statistics-outcomes.ptx",
                 "lc-ol-statistics-outcomes.ptx", "lc-ol-geometry-outcomes.ptx",
                 "lc-ol-number-outcomes.ptx", "lc-ol-algebra-outcomes.ptx",
                 "lc-ol-functions-outcomes.ptx")
LABEL = re.compile(r"^\s*Learning intentions\s*:\s*", re.I)
PREFIX = re.compile(r"^\s*By the end of this section,\s*you should be able to\s+", re.I)


def from_existing(section: etree._Element) -> list[str]:
    """Convert an existing embedded intention into the new consistent block."""
    for child in (section, *[c for c in section if c.tag == "introduction"]):
        for p in list(child.findall("p"))[:2]:
            value = " ".join("".join(p.itertext()).split())
            if not LABEL.match(value):
                continue
            value = PREFIX.sub("", LABEL.sub("", value))
            if not value:
                raise ValueError("Empty existing intention in " + str(section.get(XML_ID)))
            child.remove(p)
            if child.tag == "introduction" and len(child) == 0:
                section.remove(child)
            return [value[:1].upper() + value[1:]]
    return []


def objectives(section: etree._Element, intentions: list[str]) -> None:
    if len(intentions) < 1 or len(intentions) > 4:
        raise ValueError("A populated teaching section needs 1-4 concise intentions")
    obj = etree.Element("objectives")
    etree.SubElement(obj, "title").text = "Learning Intentions"
    ul = etree.SubElement(obj, "ul")
    for item in intentions:
        line = " ".join(item.split()).strip()
        if not line or len(line) > 260:
            raise ValueError("Invalid or overly long learning intention: " + line[:60])
        line = line[0].upper() + line[1:]
        if not line.endswith((".", "!", "?")):
            line += "."
        etree.SubElement(ul, "li").text = line
    title = section.find("title")
    if title is None:
        raise ValueError("No section title")
    section.insert(section.index(title) + 1, obj)


def main() -> None:
    book = etree.parse(str(ROOT / "main.ptx"))
    includes = [
        (child.get("href") or "").lstrip("./")
        for child in book.getroot().iter(XI)
    ]
    included = sorted({name for name in includes if name and
                      name not in SKIP and
                      not any(name.startswith(p) for p in SKIP_PREFIXES)})
    paths = [ROOT / "main.ptx", *(ROOT / name for name in included)]
    total = 0
    used = set()
    details = []
    # Parse and validate every file *before* writing any of them.
    writes = {}
    for path in paths:
        tree = etree.parse(str(path))
        count = 0
        for section in tree.getroot().iter():
            if section.tag not in ("section", "subsection", "subsubsection"):
                continue
            key = section.get(XML_ID)
            if not key:
                raise ValueError(f"Teaching section lacks xml:id: {path}")
            if section.find("objectives") is not None:
                continue
            intentions = CURATED.get(key)
            original = from_existing(section)
            if original:
                intentions = original
            if not intentions:
                # Some advanced or long-form teaching sections are not yet given
                # section-specific intentions. The populated chapter starts with
                # its own curated Learning Intentions; do not invent outcomes.
                continue
            objectives(section, intentions)
            count += 1
            used.add(key)
        if count:
            writes[path] = etree.tostring(
                tree, xml_declaration=True, encoding="UTF-8", pretty_print=False
            )
            details.append(f"{path.name}: {count}")
        total += count
    unused = sorted(set(CURATED) - used)
    if unused:
        print(f"Preserved {len(unused)} curated intentions for inactive source chapters.")
    if total < 30:
        raise ValueError(f"Only {total} teaching sections were processed, expected >= 30")
    for path, payload in writes.items():
        path.write_bytes(payload)
    print(f"Learning Intentions: {total} teaching sections; "
          f"{len(writes)} source documents; no specification text rewritten.")
    print("\n".join(details))


if __name__ == "__main__":
    main()
