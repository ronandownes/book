#!/usr/bin/env python3
"""Produce native PreTeXt strand tables from the official curriculum sources.

Every official numbered outcome is mandatory. An unexpected source layout is an
error, not an invitation to omit material. The Junior Cycle edition builds the four numbered JC strand tables;
LC Ordinary Level generator functions remain available for future editions.
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

# Concise editorial introductions: these are not part of the verbatim outcomes.
LC_STRAND_SUMMARIES = {
    "statistics": (
        "Probability develops reasoning about uncertainty through experiments, simulations and models. "
        "Statistics develops the skills to investigate data, recognise patterns, evaluate claims and communicate conclusions."
    ),
    "geometry": (
        "Geometry examines shape, space, measurement and reasoning. "
        "Trigonometry connects angles and lengths to solve mathematical and practical problems."
    ),
    "number": (
        "Number develops fluency with number systems, calculations, estimation and proportional reasoning. "
        "Students apply these ideas to quantitative situations and evaluate whether answers are reasonable."
    ),
    "algebra": (
        "Algebra uses expressions, equations and inequalities to represent relationships and solve problems. "
        "Students explain and justify the transformations they make."
    ),
    "functions": (
        "Functions describe relationships between varying quantities. "
        "Students use formulas, graphs and rates of change to interpret situations and solve problems."
    ),
}

XML_ID = "{http://www.w3.org/XML/1998/namespace}id"

def compact(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()

def tidy_outcome_sentence(p: etree._Element) -> None:
    """Make outcome sentences readable without changing their mathematical content.

    Preserve algebraic case, official subpart labels, and lead-in colons. Add
    sentence capitals and final stops to textual statements only.
    """
    if p.text:
        opening = p.text
        opening = re.sub(
            r"^(\s*(?:[a-z]|[ivx]{1,4})[.)]\s*)([a-z])",
            lambda m: m.group(1).rstrip() + " " + m.group(2).upper(),
            opening,
            count=1,
        )
        if not re.match(r"^\s*(?:[a-z]|[ivx]{1,4})[.)]", opening):
            opening = re.sub(
                r"^(\s*)([a-z])",
                lambda m: m.group(1) + m.group(2).upper(),
                opening, count=1,
            )
        p.text = opening
    # NCCA's webpage wraps subpart labels such as <alert>a)</alert>
    # separately from the verb that follows. Capitalise after the label, not
    # the label itself, and insert the previously missing inter-word space.
    if len(p) and p[0].tag in ("alert", "em"):
        label = (p[0].text or "").strip()
        if re.fullmatch(r"(?:[a-z]|[ivx]{1,4})[.)]", label):
            tail = p[0].tail or ""
            match = re.match(r"^\s*([a-z])", tail)
            if match:
                p[0].tail = " " + match.group(1).upper() + tail[match.end():]
    rendered = "".join(p.itertext()).rstrip()
    if not rendered:
        return
    # The colon introduces a sublist: do not convert it into a full stop.
    if rendered.endswith((".", "!", "?", ":", ";")):
        return
    if re.search(r"\\text\{[.!?]\}\s*$", rendered):
        return
    if len(p):
        last = p[-1]
        last.tail = (last.tail or "").rstrip() + "."
    else:
        p.text = (p.text or "").rstrip() + "."


def cell_with_paragraphs(texts: list[etree._Element]) -> etree._Element:
    cell = etree.Element("cell")
    for p in texts:
        cp = etree.fromstring(etree.tostring(p, encoding="utf-8"))
        cp.text = compact(cp.text or "") if cp.text else cp.text
        # Preserve inline emphasis, symbols and source text, but not PDF line breaks.
        for node in cp.iter():
            if node.text: node.text = re.sub(r"\s+", " ", node.text)
            if node.tail: node.tail = re.sub(r"\s+", " ", node.tail)
        tidy_outcome_sentence(cp)
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
                if re.match(r"^" + re.escape(code) + r"(?=\D|$)", t):
                    # The numbered lead is already represented by the
                    # PDF-verified statement above. Do not print it twice.
                    continue
                extras.append(p)
            if key == "number" and code == "N.1":
                extras = correct_junior_index_notation(extras)
            rows.append((code, compact(part.findtext("title") or ""), [main, *extras]))
        wanted = [prefix+"."+str(i) for i in range(1,expected+1)]
        actual = [r[0] for r in rows]
        if actual != wanted:
            raise RuntimeError(f"JC {key}: expected {wanted}, got {actual}. Refusing incomplete publication.")
        section = etree.Element("section")
        section.set(XML_ID, f"jc-outcomes-{key}")
        etree.SubElement(section,"title").text=title
        if key == "algebra":
            etree.SubElement(section, "p").text = (
                "First, scroll through the original Junior Cycle specification pages 18–19. "
                "Then use the seven-slide view to explore outcomes AF.1–AF.7."
            )
            figure = etree.SubElement(section, "figure")
            figure.set(XML_ID, "jc-algebra-original-pages")
            etree.SubElement(figure, "caption").text = (
                "Original NCCA Algebra and Functions outcomes, pages 18–19. Scroll inside the viewer."
            )
            interactive = etree.SubElement(figure, "interactive")
            interactive.set(XML_ID, "jc-algebra-original-scroll")
            interactive.set(
                "iframe",
                "https://www.curriculumonline.ie/getmedia/6a7f1ff5-9b9e-4d71-8e1f-6d4f932191db/"
                "JC_Mathematics_Specification.pdf#page=18&zoom=100",
            )
            interactive.set("width", "100%")
            interactive.set("aspect", "4:5")
            p = etree.SubElement(section, "p")
            source_link = etree.SubElement(p, "url", href=(
                "https://www.curriculumonline.ie/getmedia/6a7f1ff5-9b9e-4d71-8e1f-6d4f932191db/"
                "JC_Mathematics_Specification.pdf#page=18&zoom=100"
            ), visual="Open the original specification pages 18–19 in a new tab")
            source_link.tail = "."
        if key in ("number","geometry","algebra","statistics"):
            etree.SubElement(section, "p").text = ("Official learning outcomes. Higher Level-only material remains "
                "distinguished in bold where marked in the NCCA source.")
        add_table(section, f"jc-outcomes-{key}-table", f"{title}: official learning outcomes", rows)
        if key == "number":
            # An original teaching note, visibly distinct from official outcomes.
            note = etree.SubElement(section, "subsection")
            note.set(XML_ID, "jc-number-n3-comparison")
            etree.SubElement(note, "title").text = "N.3(a): Absolute and Relative Comparison"
            etree.SubElement(note, "p").text = (
                "An absolute comparison asks how much more or less. A relative comparison "
                "asks how many times as much, or what proportion or percentage."
            )
            example = etree.SubElement(note, "example")
            etree.SubElement(example, "title").text = "Two ways to compare"
            etree.SubElement(example, "p").text = (
                "Suppose two groups contain 12 and 8 people. The absolute difference is 4 people; "
                "the relative comparison is 12 divided by 8, or 1.5 times as many."
            )
            p = etree.SubElement(example, "p")
            p.text = "Absolute: "
            m = etree.SubElement(p, "m")
            m.text = "12-8=4"
            m.tail = ". Relative: "
            m = etree.SubElement(p, "m")
            m.text = r"\frac{12}{8}=1.5"
            m.tail = ", or 50% more, taking 8 as the reference group."
            p = etree.SubElement(note, "p")
            p.text = (
                "Addition and subtraction describe additive differences; multiplication and "
                "division describe multiplicative or proportional comparisons. "
                "The choice depends on the question."
            )

        write(section, f"jc-{key}-outcomes.ptx")
        print(f"Junior Cycle {key}: {len(rows)} complete numbered outcomes",flush=True)

def para(xml_body: str) -> etree._Element:
    return etree.fromstring(("<p>" + xml_body + "</p>").encode("utf-8"))

def correct_junior_index_notation(paragraphs: list[etree._Element]) -> list[etree._Element]:
    """Restore native maths and a genuine four-level N.1(c) hierarchy.

    The NCCA webpage collapses I-V into one HTML list item. Each roman
    statement is followed by its component equations as separate paragraphs.
    This keeps the complete syllabus text in the source table while allowing
    the browser to display one subpart or equation at a time.
    """
    fixed: list[etree._Element] = []
    replaced = False
    for p in paragraphs:
        raw = compact("".join(p.itertext())).lower()
        if not replaced and "explore numbers written as" in raw:
            fixed.extend([
                para(r"<alert>c)</alert> Explore numbers written as <m>a^b</m> (in index form) so that they can:"),
                para("i. Flexibly translate between whole numbers and index representation of numbers."),
                para("ii. Use and apply generalisations such as:"),
                para(r"<m>a^p a^q=a^{p+q}</m>;"),
                para(r"<m>\frac{a^p}{a^q}=a^{p-q}</m>;"),
                para(r"<m>(a^p)^q=a^{pq}</m>;"),
                para(r"and <m>n^{1/2}=\sqrt{n}</m>, for <m>a\in\mathbb{Z}</m>, and <m>p,q,p-q,\sqrt{n}\in\mathbb{N}</m>; and for <m>a,b,\sqrt{n}\in\mathbb{R}</m> and <m>p,q\in\mathbb{Q}</m>."),
                para("iii. <alert>Use and apply generalisations such as:</alert>"),
                para(r"<alert><m>a^0=1</m>;</alert>"),
                para(r"<alert><m>a^{p/q}=\sqrt[q]{a^p}=(\sqrt[q]{a})^p</m>;</alert>"),
                para(r"<alert><m>a^{-r}=\frac{1}{a^r}</m>;</alert>"),
                para(r"<alert><m>(ab)^r=a^rb^r</m>;</alert>"),
                para(r"<alert>and <m>\left(\frac{a}{b}\right)^r=\frac{a^r}{b^r}</m>, for <m>a,b\in\mathbb{R}</m>; <m>p,q\in\mathbb{Z}</m>; and <m>r\in\mathbb{Q}</m>.</alert>"),
                para("iv. Generalise numerical relationships involving operations involving numbers written in index form."),
                para("v. Correctly use the order of arithmetic and index operations including the use of brackets."),
            ])
            replaced = True
        else:
            fixed.append(p)
    if not replaced:
        raise RuntimeError("JC N.1 index-form outcome missing; refusing flattened maths publication.")
    # Catch accidental truncation or unexpected source text changes.
    for needle in ("i.", "ii.", "iii.", "iv.", "v."):
        if not any(compact("".join(p.itertext())).lower().startswith(needle + " ") for p in fixed):
            raise RuntimeError("JC N.1(c) missing " + needle)
    return fixed


def correct_lc_formulas(code: str, paragraphs: list[etree._Element]) -> list[etree._Element]:
    """Repair formulas that a two-dimensional PDF cannot convert to plain text.

    These particular outcomes have been checked against the source syllabus's
    printed mathematics, not guessed from the clipped extraction.
    """
    if code == "1.7":
        fixed = []
        for p in paragraphs:
            raw = compact("".join(p.itertext()))
            if "calculate the margin of error" in raw:
                fixed.append(para(r"Calculate the margin of error (<m>1/\sqrt{n}</m>) for a population proportion*."))
            else:
                fixed.append(p)
        return fixed
    if code == "3.2":
        return [
            para(r"Solve problems using the rules for indices (where <m>a,b\in\mathbb{R}</m>; <m>p,q\in\mathbb{Q}</m>; <m>a^p,a^q\in\mathbb{Q}</m>; <m>a,b\ne 0</m>):"),
            para(r"<m>a^pa^q=a^{p+q}</m>."),
            para(r"<m>\frac{a^p}{a^q}=a^{p-q}</m>."),
            para(r"<m>a^0=1</m>."),
            para(r"<m>(a^p)^q=a^{pq}</m>."),
            para(r"<m>a^{1/q}=\sqrt[q]{a}</m>, <m>q\in\mathbb{Z}</m>, <m>q\ne0</m>, <m>a\gt0</m>."),
            para(r"<m>a^{p/q}=\sqrt[q]{a^p}=(\sqrt[q]{a})^p</m>, <m>p,q\in\mathbb{Z}</m>, <m>q\ne0</m>, <m>a\gt0</m>."),
            para(r"<m>a^{-p}=\frac{1}{a^p}</m>."),
            para(r"<m>(ab)^p=a^pb^p</m>."),
            para(r"<m>\left(\frac{a}{b}\right)^p=\frac{a^p}{b^p}</m>."),
        ]
    if code == "4.1":
        return [
            para("Evaluate expressions given the value of the variables."),
            para("Expand and re-group expressions."),
            para("Factorise expressions of order 2."),
            para("Add and subtract expressions of the form:"),
            para(r"<m>(ax+by+c)\pm\cdots\pm(dx+ey+f)</m>."),
            para(r"<m>(ax^2+bx+c)\pm\cdots\pm(dx^2+ex+f)</m>, where <m>a,b,c,d,e,f\in\mathbb{Z}</m>."),
            para(r"<m>\frac{a}{bx+c}\pm\frac{p}{qx+r}</m>, where <m>a,b,c,p,q,r\in\mathbb{Z}</m>."),
            para("Use the associative and distributive properties to simplify expressions of the form:"),
            para(r"<m>a(bx\pm cy\pm d)\pm\cdots\pm e(fx\pm gy\pm h)</m>, where <m>a,b,c,d,e,f,g,h\in\mathbb{Z}</m>."),
            para(r"<m>(x\pm y)(w\pm z)</m>."),
            para("Rearrange formulae."),
        ]
    if code == "4.2":
        return [
            para("Select and use suitable strategies (graphic, numeric, algebraic, mental) for finding solutions to equations of the form:"),
            para(r"<m>f(x)=g(x)</m>, with <m>f(x)=ax+b</m>, <m>g(x)=cx+d</m>, where <m>a,b,c,d\in\mathbb{Q}</m>."),
            para(r"<m>f(x)=g(x)</m>, with <m>f(x)=\frac{a}{bx+c}\pm\frac{p}{qx+r}</m>; <m>g(x)=\frac{e}{f}</m>, where <m>a,b,c,e,f,p,q,r\in\mathbb{Z}</m>."),
            para(r"<m>f(x)=k</m>, with <m>f(x)=ax^2+bx+c</m> (and not necessarily factorisable), where <m>a,b,c\in\mathbb{Q}</m>; and interpret the results."),
            para("Select and use suitable strategies (graphic, numeric, algebraic, mental) for finding solutions to:"),
            para("Simultaneous linear equations with two unknowns, and interpret the results."),
            para("One linear equation and one equation of order 2 with two unknowns (restricted to the case where either the coefficient of x or the coefficient of y is ±1 in the linear equation), and interpret the results."),
            para("Form quadratic equations given whole number roots."),
        ]
    return paragraphs

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
            paragraphs=correct_lc_formulas(code,paragraphs)
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
        etree.SubElement(section, "p").text = LC_STRAND_SUMMARIES[key]
        etree.SubElement(section, "p").text = "The official Ordinary Level learning outcomes follow in the published syllabus order."
        add_table(section,f"lc-ol-{key}-table",f"{title}: Ordinary Level learning outcomes",grouped)
        write(section,f"lc-ol-{key}-outcomes.ptx")
        print(f"Leaving Certificate Ordinary Level {key}: {len(grouped)} official topics",flush=True)

if __name__=="__main__":
    junior()
    leaving()
