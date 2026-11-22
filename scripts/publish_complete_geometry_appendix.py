"""Publish all 50 Appendix B pages, including original vector drawings."""
from pathlib import Path
from urllib.request import Request, urlopen
import fitz, re, html, json

URL="https://www.curriculumonline.ie/getmedia/6a7f1ff5-9b9e-4d71-8e1f-6d4f932191db/JC_Mathematics_Specification.pdf"
dest=Path("output/web")
dest.mkdir(parents=True,exist_ok=True)
source=Path("assets/syllabus/JC_Mathematics_Specification.pdf")
source.parent.mkdir(parents=True,exist_ok=True)
if not source.exists():
    with urlopen(Request(URL,headers={"User-Agent":"Irish School Maths reference builder"}),timeout=90) as r:
        source.write_bytes(r.read())
pdf=fitz.open(source)
if len(pdf)!=76 or "Geometry for" not in pdf[26].get_text() or "Government of Ireland" not in pdf[75].get_text():
    raise RuntimeError("Unexpected official specification version: refusing publication")
vectors=dest/"geometry-appendix-b-vectors"
vectors.mkdir(exist_ok=True)
pages=[]
entries=[]
for n in range(27,77):
    page=pdf[n-1]
    (vectors/f"{n}.svg").write_text(page.get_svg_image(text_as_path=False),encoding="utf-8")
    t=page.get_text(sort=True)
    pages.append({"n":n,"text":t})
    for match in re.finditer(r"(?im)(?:^|\n)\s*((?:Definition|Axiom|Theorem|Corollary|Converse(?:\s+of)?|Construction|Notation|Figure)\s*\d+(?:\.\d+)?)\b",t):
        entries.append((match.group(1).strip(),n))
sections=[["At a glance: Definitions, Axioms, Theorems and Corollaries",27],["1 Introduction",30],["2 The system of geometry used for the purposes of formal proofs",31],["3 Guiding Principles",31],["4 Outline of the Level 2 Account",34],["5 Terms",35],["6 The Theory",36],["6.1 Length and Distance",37],["6.2 Angles",38],["6.3 Degrees",39],["6.4 Congruent Triangles",40],["6.5 Parallels",42],["6.6 Perpendicular Lines",49],["6.7 Quadrilaterals and Parallelograms",49],["6.8 Ratios and Similarity",52],["7 Constructions",65],["8 Teaching Approaches",70],["9 JCOL Content",72],["10 Additional Content for JCHL",73],["11 Syllabus for LCFL",74],["12 Syllabus for LCOL",74],["13 Syllabus for LCHL",74],["Copyright",76]]
section_nav="".join(f'<a class="sectionlink" href="#p{n}">{html.escape(label)} <small>p. {n}</small></a>' for label,n in sections)
nav="".join(f'<a href="#p{n}">{html.escape(label)} <small>p. {n}</small></a>' for label,n in entries)
sheets="".join(f'<section class="sheet" id="p{n}"><h2>Original Appendix B · page {n}</h2><object type="image/svg+xml" data="geometry-appendix-b-vectors/{n}.svg" aria-label="Original source page {n}, all diagrams">Source page {n}</object></section>' for n in range(27,77))
css="""*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#f4f6f8;color:#232a30;font:16px/1.5 system-ui,'Segoe UI',sans-serif}header{background:white;border-bottom:2px solid #8aa8b9;padding:13px 18px;position:sticky;top:0;z-index:5;display:flex;align-items:center;gap:15px;flex-wrap:wrap}header h1{font:600 1.35rem Georgia,serif;color:#24577a;margin:0}.brand{color:#24577a}.subtitle{font-size:.8rem;color:#63768a}.layout{display:grid;grid-template-columns:270px minmax(0,1fr);gap:18px;max-width:1400px;margin:auto;padding:14px}aside{background:white;border:1px solid #d7e0e7;padding:12px;position:sticky;top:88px;height:calc(100vh - 100px);overflow:auto}aside a{display:block;padding:5px;text-decoration:none;color:#24577a;font-size:.9rem;border-bottom:1px solid #edf0f4}aside small{float:right}.sectionlink{font-weight:600;color:#204e6e;background:#f1f6f8;margin:2px 0}main{min-width:0}.sheet{max-width:890px;margin:0 auto 18px;background:#fff;border:1px solid #d6e0e7;padding:13px}.sheet h2{font-size:.83rem;font-weight:500;color:#61798a}.sheet object{display:block;width:100%;aspect-ratio:595/842}.note{background:white;border-left:3px solid #7c9cb2;padding:13px;margin-bottom:18px}#q{font:inherit;padding:8px;border:1px solid #bbc9d6;border-radius:4px}#hits a{font-size:.86rem}@media(max-width:850px){.layout{display:block}aside{height:30vh;position:relative;top:0;margin-bottom:15px}.sheet{padding:3px}}@media print{header,aside,.note,.sheet h2{display:none}.layout{display:block}.sheet{border:0;break-after:page;padding:0;margin:0}}"""
data=json.dumps(pages,ensure_ascii=False).replace("</","<\\/")
js="""const pages=DATA,q=document.getElementById('q'),hits=document.getElementById('hits');q.addEventListener('input',()=>{let s=q.value.toLocaleLowerCase().trim();if(s.length<2){hits.innerHTML='';return;}let r=pages.filter(p=>p.text.toLocaleLowerCase().includes(s));hits.innerHTML='<p>'+r.length+' pages found</p>'+r.map(p=>'<a href="#p'+p.n+'">Page '+p.n+'</a>').join('');});""".replace("DATA",data)
page=f'''<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Complete Appendix B | Irish School Maths</title><style>{css}</style></head><body><header><a class="brand" href="index.html">Irish School Maths</a><div><h1>Appendix B: Geometry for Post-primary School Mathematics</h1><span class="subtitle">Full official source · pages 27–76 · vector diagrams</span></div><input id="q" type="search" aria-label="Search all source text" placeholder="Search Appendix B"></header><div class="layout"><aside><strong>Contents — Sections 1–13</strong>{section_nav}<hr><strong>Numbered statements</strong><div id="hits"></div>{nav}</aside><main><div class="note"><strong>Full official source edition:</strong> all 50 pages and original mathematical diagrams, reproduced as selectable SVG vectors. This is a high-fidelity source reproduction. A separate semantic PreTeXt transcription is still incomplete.</div>{sheets}</main></div><script>{js}</script></body></html>'''
(dest/"geometry-appendix-b-complete.html").write_text(page,encoding="utf-8")
assert len(list(vectors.glob("*.svg")))==50
print(f"Generated complete Appendix B: 50 vector pages and {len(entries)} index entries")
