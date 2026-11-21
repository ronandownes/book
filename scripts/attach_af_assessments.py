#!/usr/bin/env python3
"""Attach collapsed Quiz/Test panels after teaching sections without changing any official learning-outcome text."""
from pathlib import Path
from lxml import etree
from urllib.parse import urlencode
import html
import re

ROOT = Path("output/web")
SOURCE = Path("source")
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
APP = "interactives/algebra-section-assessments.html"
if not (ROOT / APP).is_file():
    raise SystemExit("AF section assessment app is missing")

families = {
    "jc-algebra-patterns.ptx": "pattern",
    "jc-algebra-language.ptx": "vocabulary",
    "jc-algebra-substitution.ptx": "substitute",
    "jc-algebra-simplifying.ptx": "simplify",
    "jc-algebra-expanding-brackets.ptx": "quadratic",
    "jc-algebra-factorisation.ptx": "factor",
    "jc-algebra-division-fractions.ptx": "divide",
    "jc-algebra-equations-inequalities.ptx": "equations",
    "jc-algebra-changing-subject.ptx": "formula",
    "jc-algebra-polynomial-display.ptx": "polynomial",
    "jc-algebra-rational-practice.ptx": "rational",
}
overrides = {
    "algebra-words": "vocabulary", "algebra-operation-words": "law",
    "algebra-language-practice": "vocabulary",
    "expanding-principle": "distribution",
    "expanding-monomial-bracket": "monomial",
    "expanding-two-brackets": "quadratic",
    "expanding-distribution": "quadratic",
    "expanding-foil-lab": "quadratic",
    "expanding-cross-products": "quadratic",
    "expanding-place-value": "cubic",
    "expanding-homework": "quadratic",
    "expanding-scaling": "scaling",
    "expanding-zero-placeholders": "zeros",
    "expanding-language": "vocabulary",
    "expanding-hidden-maths": "quadratic",
    "expanding-beyond-school": "degree",
    "stacked-polynomials-linear": "linear",
    "stacked-polynomials-quadratic": "polynomial",
    "rational-combine-method": "rational",
    "rational-six-practice": "rational",
    "rational-equation-extension": "rationalequation",
}
# Outcome material remains exactly as written; activities are attached in the generated HTML only.
outcomes = {
    1: ("Patterns and Generalisation", "pattern"),
    2: ("Expressions, Equations and Substitution", "substitute"),
    3: ("Operations, Polynomials and Rational Expressions", "polynomial"),
    4: ("Solving Equations and Inequalities", "equations"),
    5: ("Quadratics from Integer Roots", "roots"),
    6: ("Changing the Subject of a Formula", "formula"),
    7: ("Functions", "function"),
}
targets = {}
for filename, default in families.items():
    path = SOURCE / filename
    if not path.exists():
        raise SystemExit("Missing teaching source: " + str(path))
    root = etree.parse(str(path)).getroot()
    for sec in root.iter("section"):
        ident = sec.get(XML_ID)
        if ident is None:
            continue
        if ident == "rational-interactive-checking":
            # Already embeds a distinct six-question Quiz/Test from the earlier AF3 addition.
            continue
        title = sec.findtext("title") or ident
        targets[ident] = (title, overrides.get(ident, default))
for num, (title, kind) in outcomes.items():
    targets["jc-outcomes-algebra-af" + str(num)] = ("AF." + str(num) + " — " + title, kind)
    # Some older builds generated a numeric section URL instead.
    targets["jc-outcomes-algebra-" + str(num)] = ("AF." + str(num) + " — " + title, kind)

style = """<style data-af-assessments-style="1">
details.af-assessment{border:1px solid #b8ced8;border-radius:10px;padding:.7rem 1rem;margin:1.4rem 0;background:#f5f9fb;color:#1d475c}
details.af-assessment summary{cursor:pointer;font-weight:650}
details.af-assessment p{font-size:.92rem;margin:.55rem 0}
details.af-assessment iframe{display:block;width:100%;height:790px;max-width:100%;border:1px solid #d1dfe7;border-radius:8px;background:white}
@media(max-width:650px){details.af-assessment iframe{height:860px}}
@media print{details.af-assessment{display:none}}
</style>"""

def panel(ident, title, kind):
    url = APP + "?" + urlencode({"section": ident, "skill": kind, "title": title})
    return ('<details class="af-assessment" data-af-section="' + html.escape(ident, quote=True) + '">'
        '<summary>Quiz and Test — six questions each</summary>'
        '<p>Quiz: immediate checking and worked answers. Test: submit all six before feedback.</p>'
        '<iframe title="Quiz and test: ' + html.escape(title, quote=True) + '"'
        ' loading="lazy" src="' + html.escape(url, quote=True) + '"></iframe>'
        '</details>')

def insert_after_section(document, ident, fragment):
    # Match the actual section element and its matching end tag, not an unrelated
    # nested section or a duplicate navigation link.
    m = re.search(r'<section\b[^>]*\bid=["\']' + re.escape(ident) + r'["\'][^>]*>', document)
    if m is None:
        return None
    depth = 1
    for match in re.finditer(r'</?section\b[^>]*>', document[m.end():], flags=re.I):
        token = match.group(0)
        if token.startswith("</"):
            depth -= 1
        elif not token.endswith("/>"):
            depth += 1
        if depth == 0:
            pos = m.end() + match.start()
            return document[:pos] + fragment + document[pos:]
    return None

# Index first, so sections nested on a chapter page are located correctly.
pages = sorted(ROOT.glob("*.html"))
found = {}
for page in pages:
    source = page.read_text(encoding="utf-8")
    matched = []
    for ident, (title, kind) in targets.items():
        if 'id="' + ident + '"' not in source and "id='" + ident + "'" not in source:
            continue
        if 'data-af-section="' + ident + '"' in source:
            found[ident] = page.name
            continue
        changed = insert_after_section(source, ident, panel(ident, title, kind))
        if changed is not None:
            source = changed
            matched.append(ident)
    if matched:
        if 'data-af-assessments-style="1"' not in source:
            source = source.replace("</head>", style + "\n</head>", 1)
        page.write_text(source, encoding="utf-8")
        for ident in matched:
            found[ident] = page.name

canonical = [x for x in targets if not re.match(r'jc-outcomes-algebra-\d+$', x)]
missing = [x for x in canonical if x not in found]
print(f"Inserted Quiz/Test panels into {len(found)} Algebra and Functions sections.")
if missing:
    print("Some source sections were not separate generated HTML sections:", ", ".join(missing))
# The generated outcome pages must be detectable, otherwise stop rather than
# incorrectly claiming the quiz/test is on the page being shown to students.
for num in range(1, 8):
    if not any(name in found for name in
               ("jc-outcomes-algebra-af" + str(num),
                "jc-outcomes-algebra-" + str(num))):
        raise SystemExit("AF." + str(num) + " outcome has no attached assessment")
if len(found) < 25:
    raise SystemExit("Too few Algebra assessment sections were linked")
