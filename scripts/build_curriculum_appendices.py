#!/usr/bin/env python3
"""Generate native, editable PreTeXt appendices from published NCCA sources.

No iframes, PDF pages or external viewers appear in the generated textbook.
NCCA owns the text; acknowledgements are retained at the end of the part.
"""
from __future__ import annotations
import html
import re
import sys
from pathlib import Path
import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import fitz

JC_URL = "https://curriculumonline.ie/junior-cycle/junior-cycle-subjects/mathematics/expectations-for-students/"
PDF_PATH = Path("assets/syllabus/LC_Mathematics_Syllabus_2015.pdf")
OUTPUT = Path("source/appendices.ptx")

JC = [
    ("unifying", "Unifying Strand", r"unifying\s+strand"),
    ("number", "Number", r"number\s+strand"),
    ("geometry", "Geometry and Trigonometry", r"geometry\s+and\s+trigonometry\s+strand"),
    ("algebra", "Algebra and Functions", r"algebra\s+and\s+functions\s+strand"),
    ("statistics", "Statistics and Probability", r"statistics\s+and\s+probability\s+strand"),
]
LC = [
    ("statistics", "Statistics and Probability", (16, 21)),
    ("geometry", "Geometry and Trigonometry", (22, 25)),
    ("number", "Number", (26, 33)),
    ("algebra", "Algebra", (34, 39)),
    ("functions", "Functions", (40, 42)),
]

def clean(s: str) -> str:
    return re.sub(r"\\s+", " ", "".join(c for c in s if (ord(c) >= 32 or c in "\\t\\n\\r") and not (0xD800 <= ord(c) <= 0xDFFF))).strip()

def xt(s: str) -> str:
    return html.escape(s, quote=False)

def render_html(node) -> str:
    if isinstance(node, NavigableString):
        return xt(str(node))
    if not isinstance(node, Tag):
        return ""
    name = node.name.lower()
    inside = "".join(render_html(c) for c in node.children)
    if name in ("strong", "b"):
        return f"<alert>{inside}</alert>"
    if name in ("sup",):
        # Display the source's superscript explicitly; the value is not discarded.
        return f"<m>{{{clean(node.get_text())}}}</m>" if False else "^("+xt(clean(node.get_text()))+")"
    if name in ("sub",):
        return "_("+xt(clean(node.get_text()))+")"
    if name == "br":
        return " "
    return inside

def junior_content():
    response = requests.get(JC_URL, timeout=50, headers={"User-Agent":"Irish School Maths educational curriculum reader"})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    current = None
    tables = {k: [] for k, _, _ in JC}
    for element in soup.find_all(["h1", "h2", "h3", "h4", "table"]):
        if element.name != "table":
            label = clean(element.get_text(" ", strip=True)).lower()
            for key, title, pat in JC:
                if re.search(pat, label, re.I):
                    current = key
                    break
            continue
        if current in tables:
            rows = []
            for tr in element.find_all("tr"):
                cells = tr.find_all(["td", "th"], recursive=False)
                if len(cells) < 2:
                    continue
                heading = clean(cells[0].get_text(" ", strip=True))
                if heading.lower().startswith("students learn about"):
                    continue
                outcome = cells[-1]
                if heading:
                    lines = []
                    for li in outcome.find_all("li"):
                        if li.find_parent("li") is not None:
                            continue
                        raw = clean(li.get_text(" ", strip=True))
                        if raw:
                            lines.append(clean(render_html(li)))
                    if not lines:
                        raw = clean(render_html(outcome))
                        if raw:
                            lines = [raw]
                    if lines:
                        rows.append((heading, lines))
            if rows:
                tables[current].extend(rows)
    counts = {k:len(v) for k,v in tables.items()}
    print("Junior Cycle source rows:", counts, flush=True)
    if any(n == 0 for n in counts.values()):
        raise RuntimeError("Could not find all five Junior Cycle outcome tables. Refusing to publish incomplete reference.")
    out = []
    for i, (key, title, _) in enumerate(JC):
        out.append(f'<chapter xml:id="jc-official-{key}">')
        out.append(f'<title>JC {title}</title>')
        for j, (heading, outcomes) in enumerate(tables[key], 1):
            out.append(f'<section xml:id="jc-outcome-{key}-{j}">')
            out.append(f'<title>{xt(heading)}</title>')
            for statement in outcomes:
                out.append(f'<p>{statement}</p>')
            out.append("</section>")
        out.append("</chapter>")
    return out

def page_lines(page, x0, x1):
    """Read whole source lines whose *starts* lie within the selected column.

    Clipping rectangles can cut off the final letters of a word even when its
    text legitimately belongs to the column. This intentionally retains the
    full original text of each selected line, without including adjacent HL
    lines whose starts lie in the separate right-hand column.
    """
    blocks = page.get_text("dict")["blocks"]
    result = []
    for b in blocks:
        if "lines" not in b:
            continue
        for line in b["lines"]:
            begin = line["bbox"][0]
            if not (x0 - 4 <= begin < x1):
                continue
            txt = clean("".join(s.get("text", "") for s in line["spans"]))
            if txt:
                result.append((line["bbox"][1], txt))
    return sorted(result, key=lambda row: row[0])


def leave_content():
    if not PDF_PATH.exists() or PDF_PATH.stat().st_size < 100000:
        raise RuntimeError("Source LC syllabus PDF unavailable; refusing to create incomplete appendices.")
    doc = fitz.open(PDF_PATH)
    out = []
    counts = {}
    sections = {}
    for key, title, indices in LC:
        out.append(f'<chapter xml:id="lc-official-{key}">')
        out.append(f'<title>LC Ordinary Level — {xt(title)}</title>')
        bullet = []
        open_topic = False
        topic_number = None
        count = 0
        subsection_count = 0

        def flush():
            nonlocal bullet, count
            sentence = clean(" ".join(bullet))
            if sentence:
                out.append("<p>" + xt(sentence) + "</p>")
                count += 1
            bullet = []

        for idx in range(indices[0], indices[1] + 1):
            page = doc[idx]
            body = page.get_text("text")
            if not re.search(r"Students working at OL", body, re.I):
                continue
            w = page.rect.width
            raw_left = page_lines(page, .19 * w, .335 * w)
            # Determine the first HL bullet rather than assuming every
            # printed table has identical column widths. Page 43 is narrower.
            high_bullets = []
            for block in page.get_text("dict")["blocks"]:
                for ln in block.get("lines", []):
                    line_text = "".join(span.get("text", "") for span in ln["spans"]).strip()
                    if line_text.startswith("–") and ln["bbox"][0] >= .61 * w:
                        high_bullets.append(ln["bbox"][0])
            ol_right_edge = min(.645 * w, min(high_bullets) - 2 if high_bullets else .645 * w)
            ol = page_lines(page, .335 * w, ol_right_edge)
            topics = []
            for y, text in raw_left:
                if y > page.rect.height * .90:
                    continue
                match = re.match(r"^([1-5]\.\d+)\s+(.+)$", text)
                if match:
                    topics.append({"y": y, "code": match.group(1), "title": text})
                elif topics and text and (y - topics[-1]["y"]) < 150:
                    topics[-1]["title"] += " " + text

            for y, text in ol:
                if y > page.rect.height * .90:
                    continue
                if re.search(r"Students working at OL|should be able to", text, re.I):
                    continue
                if not text or re.search(r"^Leaving Certificate Mathematics", text, re.I):
                    continue
                headings = [item for item in topics if item["y"] <= y + 5]
                if headings:
                    h = headings[-1]
                    if h["code"] != topic_number:
                        flush()
                        if open_topic:
                            out.append("</section>")
                            open_topic = False
                        subsection_count += 1
                        out.append(f'<section xml:id="lc-{key}-topic-{subsection_count}">')
                        out.append("<title>" + xt(clean(h["title"])) + "</title>")
                        topic_number = h["code"]
                        open_topic = True

                # A source en-dash/bullet begins a new learning outcome.
                # Following printed lines belong to that outcome, not new paragraphs.
                if re.match(r"^\s*[–•]\s*", text):
                    flush()
                    bullet = [re.sub(r"^\s*[–•]\s*", "", text).strip()]
                elif text == "-":
                    flush()
                else:
                    if not bullet:
                        bullet = [text]
                    else:
                        bullet.append(text)
        flush()
        if open_topic:
            out.append("</section>")
        out.append("</chapter>")
        counts[key] = {"outcomes": count, "topics": subsection_count}
    print("LC Ordinary Level topics and outcomes:", counts, flush=True)
    if any(v["outcomes"] < 8 or v["topics"] < 2 for v in counts.values()):
        raise RuntimeError("LC topic extraction is incomplete; refusing to publish.")
    return out

def main():
    src = junior_content()
    lc = leave_content()
    pieces = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<part xml:id="part-official-appendices">',
        '<title>Appendices</title>',
        *src, *lc,
        Path("source/glossary.ptx").read_text(encoding="utf-8").replace('<?xml version="1.0" encoding="UTF-8"?>', '').strip(),
        '<chapter xml:id="official-curriculum-attribution">',
        '<title>Source acknowledgement</title>',
        '<p>Junior Cycle Mathematics (2018) and Leaving Certificate Mathematics Syllabus (for examination from 2015). © National Council for Curriculum and Assessment (NCCA). Reproduced with acknowledgement; copyright remains with the NCCA.</p>',
        '<p>Source: curriculumonline.ie</p>',
        '</chapter>',
        '</part>',
    ]
    OUTPUT.write_text("\n".join(pieces)+"\n", encoding="utf-8")
    print(f"Wrote {OUTPUT} ({OUTPUT.stat().st_size} bytes)", flush=True)

if __name__ == "__main__":
    main()
