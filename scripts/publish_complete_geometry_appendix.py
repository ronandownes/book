"""Publish all 49 Appendix B source pages as searchable SVG vector HTML."""
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
if len(pdf)!=76 or "Geometry for" not in pdf[26].get_text():
    raise RuntimeError("Unexpected official specification version: refusing publication")
vectors=dest/"geometry-appendix-b-vectors"
vectors.mkdir(exist_ok=True)
pages=[]
entries=[]
for n in range(27,76):
    page=pdf[n-1]
    (vectors/f"{n}.svg").write_text(page.get_svg_image(text_as_path=False),encoding="utf-8")
    t=page.get_text(sort=True)
    pages.append({"n":n,"text":t})
    for match in re.finditer(r"(?im)(?:^|\n)\s*((?:Definition|Axiom|Theorem|Corollary|Converse(?:\s+of)?|Construction|Notation|Figure)\s*\d+(?:\.\d+)?)\b",t):
        entries.append((match.group(1).strip(),n))
nav="".join(f'<a href="#p{n}">{html.escape(label)} <small>p. {n}</small></a>' for label,n in entries)
sheets="".join(f'<section class="sheet" id="p{n}"><h2>Original Appendix B · page {n}</h2><object type="image/svg+xml" data="geometry-appendix-b-vectors/{n}.svg" aria-label="Original source page {n}, all diagrams">Source page {n}</object></section>' for n in range(27,76))
css="""*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#f4f6f8;color:#232a30;font:16px/1.5 system-ui,'Segoe UI',sans-serif}header{background:white;border-bottom:2px solid #8aa8b9;padding:13px 18px;position:sticky;top:0;z-index:5;display:flex;align-items:center;gap:15px;flex-wrap:wrap}header h1{font:600 1.35rem Georgia,serif;color:#24577a;margin:0}.brand{color:#24577a}.subtitle{font-size:.8rem;color:#63768a}.layout{display:grid;grid-template-columns:270px minmax(0,1fr);gap:18px;max-width:1400px;margin:auto;padding:14px}aside{background:white;border:1px solid #d7e0e7;padding:12px;position:sticky;top:88px;height:calc(100vh - 100px);overflow:auto}aside a{display:block;padding:5px;text-decoration:none;color:#24577a;font-size:.9rem;border-bottom:1px solid #edf0f4}aside small{float:right}main{min-width:0}.sheet{max-width:890px;margin:0 auto 18px;background:#fff;border:1px solid #d6e0e7;padding:13px}.sheet h2{font-size:.83rem;font-weight:500;color:#61798a}.sheet object{display:block;width:100%;aspect-ratio:595/842}.note{background:white;border-left:3px solid #7c9cb2;padding:13px;margin-bottom:18px}#q{font:inherit;padding:8px;border:1px solid #bbc9d6;border-radius:4px}#hits a{font-size:.86rem}@media(max-width:850px){.layout{display:block}aside{height:30vh;position:relative;top:0;margin-bottom:15px}.sheet{padding:3px}}@media print{header,aside,.note,.sheet h2{display:none}.layout{display:block}.sheet{border:0;break-after:page;padding:0;margin:0}}"""
data=json.dumps(pages,ensure_ascii=False).replace("</","<\\/")
js="""const pages=DATA,q=document.getElementById('q'),hits=document.getElementById('hits');q.addEventListener('input',()=>{let s=q.value.toLocaleLowerCase().trim();if(s.length<2){hits.innerHTML='';return;}let r=pages.filter(p=>p.text.toLocaleLowerCase().includes(s));hits.innerHTML='<p>'+r.length+' pages found</p>'+r.map(p=>'<a href="#p'+p.n+'">Page '+p.n+'</a>').join('');});""".replace("DATA",data)
page=f'''<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Complete Appendix B | Irish School Maths</title><style>{css}</style></head><body><header><a class="brand" href="index.html">Irish School Maths</a><div><h1>Appendix B: Geometry for Post-primary School Mathematics</h1><span class="subtitle">Full official source · pages 27–75 · vector diagrams</span></div><input id="q" type="search" aria-label="Search all source text" placeholder="Search Appendix B"></header><div class="layout"><aside><strong>Numbered statements</strong><div id="hits"></div>{nav}</aside><main><div class="note"><strong>Full official source edition:</strong> all 49 pages and original mathematical diagrams, reproduced as selectable SVG vectors. This is a high-fidelity source reproduction. A separate semantic PreTeXt transcription is still incomplete.</div>{sheets}</main></div><script>{js}</script></body></html>'''
(dest/"geometry-appendix-b-complete.html").write_text(page,encoding="utf-8")
assert len(list(vectors.glob("*.svg")))==49
print(f"Generated complete Appendix B: 49 vector pages and {len(entries)} index entries")
