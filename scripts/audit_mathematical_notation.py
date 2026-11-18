#!/usr/bin/env python3
"""Protect typographic fidelity and official outcome coverage during every build."""
import re
from pathlib import Path
from lxml import etree

ROOT = Path("source")
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
FILES = [ROOT / f"jc-{key}-outcomes.ptx" for key in ("number", "geometry", "algebra", "statistics")]
FILES += [ROOT / f"lc-ol-{key}-outcomes.ptx" for key in ("statistics", "geometry", "number", "algebra", "functions")]
errors = []
warnings = []
for path in FILES:
    book = etree.parse(str(path))
    for paragraph in book.xpath("//p"):
        label = next((str(s) for s in paragraph.iterancestors() if s.get(XML_ID)), path.name)
        # Examine text *outside* native maths, not stringified complete paragraphs.
        chunks = [part for node in paragraph.iter() if node.tag not in {"m", "me", "md"}
                  for part in [node.text or "", node.tail or ""]]
        raw = " ".join(chunks)
        if re.search(r"\^\s*\(?\d+\)?|_\s*\(?\d+\)?", raw):
            warnings.append((path.name, label, raw[:110]))
        if re.search(r"(?<![a-zA-Z])(?:[ℕℤℚℝ])", raw):
            warnings.append((path.name, label, raw[:110]))
algebra = etree.parse(str(ROOT / "jc-algebra-outcomes.ptx"))
af3 = algebra.xpath('//*[@xml:id="jc-outcomes-algebra-af3"]', namespaces={"xml":"http://www.w3.org/XML/1998/namespace"})
if len(af3) != 1:
    errors.append("AF.3 section missing")
else:
    body = etree.tostring(af3[0], encoding="unicode")
    required = [r"\frac{a}{bx+c}", r"a^2x^2-b^2y^2", r"\mathbb{Q}", r"\mathbb{Z}", "<alert>"]
    for needle in required:
        if needle not in body:
            errors.append("AF.3 missing typeset source: " + needle)
    if re.search(r"\bi\.linear|x\^\(2\)", body, re.I):
        errors.append("AF.3 still contains flattened roman numerals or exponents")
for path in FILES:
    if not path.is_file() or path.stat().st_size < 300:
        errors.append("Missing or empty outcomes: " + path.name)
print("Maths audit checked", len(FILES), "source files.")
for path, ident, raw in warnings[:40]:
    print("REVIEW mathematical typography:", path, ident, repr(raw[:95]))
print("Other potential text-only maths fragments:", len(warnings))
if errors:
    raise SystemExit("\n".join(errors))
print("AF.3 and all curriculum outcome files passed structural checks.")
