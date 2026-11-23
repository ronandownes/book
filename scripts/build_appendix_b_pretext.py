"""Build reusable, native PreTeXt source from official Appendix B (2018 JC specification).

No whole-page PDF images: text is transcribed into XML nodes; each geometrical
figure is a separate vector SVG made from primitive paths in its source drawing.
This is a machine-assisted first pass requiring mathematical proofreading.
"""
from __future__ import annotations
import re
import unicodedata
from pathlib import Path
from xml.etree import ElementTree as ET
import fitz
from urllib.request import Request, urlopen

PDF = Path('assets/syllabus/JC_Mathematics_Specification.pdf')
OUT = Path('source/appendix-b-native')
FIG = Path('assets/geometry-appendix-b')
XMLID = '{http://www.w3.org/XML/1998/namespace}id'
GROUPS = [
 ('at-a-glance','At a glance: Definitions, Axioms, Theorems and Corollaries'),
 ('introduction','1 Introduction'),
 ('formal-system','2 The System of Geometry'),
 ('guiding-principles','3 Guiding Principles'),
 ('level-two-account','4 Outline of the Level 2 Account'),
 ('terms','5 Terms'),
 ('theory','6 The Theory'),
 ('length-distance','6.1 Length and Distance'),
 ('angles','6.2 Angles'),
 ('degrees','6.3 Degrees'),
 ('congruent-triangles','6.4 Congruent Triangles'),
 ('parallels','6.5 Parallels'),
 ('perpendicular-lines','6.6 Perpendicular Lines'),
 ('quadrilaterals','6.7 Quadrilaterals and Parallelograms'),
 ('ratios-similarity','6.8 Ratios and Similarity'),
 ('pythagoras','6.9 Pythagoras'),
 ('area','6.10 Area'),
 ('circles','6.11 Circles'),
 ('special-triangle-points','6.12 Special Triangle Points'),
 ('constructions','7 Constructions to Study'),
 ('teaching','8 Teaching Approaches'),
 ('jcol','9 JCOL Content'),
 ('jchl','10 Additional Content for JCHL'),
 ('lcfl','11 Syllabus for LCFL'),
 ('lcol','12 Syllabus for LCOL'),
 ('lchl','13 Syllabus for LCHL'),
 ('copyright','Source copyright information'),
]
SECTION_FROM_NUMBER = {
 '1':'introduction','2':'formal-system','3':'guiding-principles',
 '4':'level-two-account','5':'terms','6':'theory','6.1':'length-distance',
 '6.2':'angles','6.3':'degrees','6.4':'congruent-triangles',
 '6.5':'parallels','6.6':'perpendicular-lines','6.7':'quadrilaterals',
 '6.8':'ratios-similarity','6.9':'pythagoras','6.10':'area',
 '6.11':'circles','6.12':'special-triangle-points',
 '7':'constructions','8':'teaching','9':'jcol','10':'jchl',
 '11':'lcfl','12':'lcol','13':'lchl',
}

LABEL = re.compile(r'^(Definition|Axiom|Theorem|Proposition|Corollary|Notation|Remark|Construction)\s+(\d+)\b\s*(?:\(([^)]*)\))?\s*[.:]?\s*(.*)$',re.I|re.S)
PROOF = re.compile(r'^(Proof|Converse)\.\s*(.*)$', re.S)
HEADING = re.compile(r'^(\d+(?:\.\d+)?)\s+([A-Z][^\n]{2,120})$')
FIGURE = re.compile(r'^Figure\s+(\d+)\.?$',re.I)
TITLE = re.compile(r'^\d+(?:\.\d+)?\s+[A-Z][^\n]{2,100}$')
MATH_TOKEN = re.compile(r"(?<![A-Za-z|])(?:∆[A-Z′']+|∠[A-Z′']+|\|(?:∠|∆)?[A-Z′']+\|(?!\|)|\b\d+◦|ℝ)")


def tidy(block: str) -> str:
    s=unicodedata.normalize('NFKC',block)
    s=s.replace('−','−').replace('∆','∆').replace('∠','∠')
    # Unwrap wrapped prose, but retain genuine hyphens in compound words.
    s=re.sub(r'(?<=\w)-\s*\n\s*(?=[a-z])','',s)
    s=re.sub(r'\s*\n\s*',' ',s)
    s=re.sub(r'\s+',' ',s).strip()
    return s


def latex_symbol(s: str) -> str:
    s=s.replace('∆',r'\triangle ').replace('∠',r'\angle ')
    s=s.replace('′',"'").replace('◦',r'^\circ').replace('ℝ',r'\mathbb{R}')
    return s


def append_text(parent: ET.Element, txt: str) -> None:
    """Embed clearly identified mathematical tokens as real PreTeXt inline maths."""
    p=ET.SubElement(parent,'p')
    pos=0; tail_to=None
    for match in MATH_TOKEN.finditer(txt):
        before=txt[pos:match.start()]
        if tail_to is None: p.text=(p.text or '')+before
        else: tail_to.tail=(tail_to.tail or '')+before
        tail_to=ET.SubElement(p,'m');tail_to.text=latex_symbol(match.group())
        pos=match.end()
    if tail_to is None: p.text=(p.text or '')+txt[pos:]
    else: tail_to.tail=(tail_to.tail or '')+txt[pos:]


def num(v): return f'{v:.2f}'.rstrip('0').rstrip('.')

def point(p):return f'{num(p.x)},{num(p.y)}'


def draw_svg(page: fitz.Page, index: int, caption_y:float) -> bool:
    """Recompose ONLY the diagram from separate vector drawing commands, not a page image."""
    items=[]; bounds=None
    for d in page.get_drawings():
        box=d['rect']
        if not(185 <=box.x0 and box.x1<=480 and caption_y-210<=box.y0 and box.y1<=caption_y-7):continue
        if box.width<0.5 or box.height<0.5:continue
        # Reject long typesetting rules, e.g. fraction bars far outside diagram.
        if box.width>180 and box.height<1:continue
        path=[]
        for part in d['items']:
            t=part[0]
            if t=='l':path.append('M '+point(part[1])+' L '+point(part[2]))
            elif t=='c':path.append('M '+point(part[1])+' C '+' '.join(point(x) for x in part[2:5]))
            elif t=='re':
                r=part[1];path.append(f'M {num(r.x0)},{num(r.y0)} H {num(r.x1)} V {num(r.y1)} H {num(r.x0)} Z')
            elif t=='qu':
                q=part[1];path.append('M '+point(q.ul)+' L '+point(q.ur)+' L '+point(q.lr)+' L '+point(q.ll)+' Z')
        if not path:continue
        stroke=d.get('color');fill=d.get('fill')
        def col(c):return 'rgb('+','.join(str(round(255*n)) for n in c)+')' if c else 'none'
        a={'d':' '.join(path),'stroke':col(stroke),'fill':col(fill),'stroke-width':num(d.get('width') or 0.5),'stroke-linecap':'round','stroke-linejoin':'round'}
        if d.get('closePath'):a['d']+=' Z'
        items.append(a)
        bounds=box if bounds is None else bounds|box
    if not items:return False
    pad=12; b=bounds+(-pad,-pad,pad,pad)
    svg=ET.Element('svg',{'xmlns':'http://www.w3.org/2000/svg','viewBox':f'{num(b.x0)} {num(b.y0)} {num(b.width)} {num(b.height)}','role':'img','aria-label':f'Geometrical diagram, Figure {index}'})
    for attrs in items:ET.SubElement(svg,'path',attrs)
    FIG.mkdir(parents=True,exist_ok=True)
    ET.ElementTree(svg).write(FIG/f'figure-{index:02d}.svg',encoding='unicode',xml_declaration=True)
    return True


def blocks_from_page(page:fitz.Page):
    for x0,y0,x1,y1,raw,*_ in page.get_text('blocks',sort=True):
        # Main column only. Exclude page numbers and repeated side matter.
        if x0<135 or y0<105 or y0>760:continue
        s=tidy(raw)
        if s:yield (x0,y0,x1,y1,s)


def produce(source_pdf:Path=PDF):
    if not source_pdf.exists():
        source_pdf.parent.mkdir(parents=True,exist_ok=True)
        url='https://www.curriculumonline.ie/getmedia/6a7f1ff5-9b9e-4d71-8e1f-6d4f932191db/JC_Mathematics_Specification.pdf'
        req=Request(url,headers={'User-Agent':'Full Cycle Maths educational reference'})
        with urlopen(req,timeout=120) as response:source_pdf.write_bytes(response.read())
    doc=fitz.open(source_pdf)
    if len(doc)==76:
        assert 'Geometry for' in doc[26].get_text(), 'Unexpected official PDF layout'
        pages=[(n,doc[n-1]) for n in range(27,77)]
    elif len(doc)==50:
        pages=[(n,doc[n-27]) for n in range(27,77)]
    else:raise ValueError('Expected 50-page appendix or 76-page specification')
    OUT.mkdir(parents=True,exist_ok=True);FIG.mkdir(parents=True,exist_ok=True)
    legacy_section_ids={'theory':'geometry-app-b-theory','length-distance':'geometry-app-b-length-distance','angles':'geometry-app-b-angles'}
    sections={slug:ET.Element('section',{XMLID:legacy_section_ids.get(slug,'geometry-b-source-'+slug)}) for slug,_ in GROUPS}
    for slug,title in GROUPS:ET.SubElement(sections[slug],'title').text=title
    current='at-a-glance'; used=set(); figures=set();count=0;words=0
    for n,pg in pages:
        if n==76:current='copyright'
        for x0,y0,x1,y1,content in blocks_from_page(pg):
            h=HEADING.match(content)
            if h and h.group(1) in SECTION_FROM_NUMBER and n>=30 and x0 < 149:
                target=SECTION_FROM_NUMBER[h.group(1)]
                # Prevent page-numbered index rows being mistaken for headings.
                if n>=30:
                    if current!=target:current=target
                    else:continue
                    continue
            sec=sections[current]
            m=FIGURE.fullmatch(content)
            if m:
                k=int(m.group(1))
                if k not in figures and draw_svg(pg,k,y0):
                    fig=ET.SubElement(sec,'figure',{XMLID:f'geometry-b-figure-{k:02d}'})
                    ET.SubElement(fig,'caption').text=f'Figure {k}. Geometry diagram.'
                    ET.SubElement(fig,'image',{'source':f'geometry-appendix-b/figure-{k:02d}.svg','width':'75%'})
                    figures.add(k)
                else:append_text(sec,content)
                continue
            match=None if current=='at-a-glance' else LABEL.match(content)
            if match and len(content)<1800:
                kind,ident,qualifier,remainder=match.groups()
                label=kind.title()+f' {ident}'+(f' ({qualifier})' if qualifier else '')
                attrs={}
                if kind.lower() in {'definition','axiom','theorem','corollary','proposition'}:
                    identifier=f'geometry-app-b-{kind.lower()}-{ident}'
                    if identifier not in used:attrs[XMLID]=identifier;used.add(identifier)
                el=ET.SubElement(sec,'paragraphs',attrs)
                ET.SubElement(el,'title').text=label
                if remainder:append_text(el,remainder)
                count+=1
            elif current!='at-a-glance' and PROOF.match(content):
                mm=PROOF.match(content)
                el=ET.SubElement(sec,'paragraphs')
                ET.SubElement(el,'title').text=mm.group(1)
                if mm.group(2):append_text(el,mm.group(2))
                count+=1
            elif h and not (current=='at-a-glance') and n>=30:
                p=ET.SubElement(sec,'p'); ET.SubElement(p,'em').text=content
            else:append_text(sec,content)
            words+=len(content.split())
    # Typeset the four term classifications as reusable native entries;
    # combine the entry broken by an original printed-page boundary.
    term_section=sections['terms']
    term_paragraphs=term_section.findall('p')
    if len(term_paragraphs)==5 and (term_paragraphs[2].text or '').endswith('reflex'):
        term_paragraphs[2].text += ' ' + (term_paragraphs[3].text or '')
        term_section.remove(term_paragraphs[3])
        term_paragraphs=term_section.findall('p')
    for item in term_paragraphs:
        raw=item.text or ''
        if ':' not in raw:continue
        heading,definition=raw.split(':',1)
        if heading not in ('Undefined Terms','Most important Defined Terms','Other Defined terms','Definable terms used without explicit definition'):continue
        location=list(term_section).index(item)
        term_section.remove(item)
        entry=ET.Element('paragraphs',{XMLID:'geometry-b-terms-'+re.sub('[^a-z0-9]+','-',heading.lower()).strip('-')})
        ET.SubElement(entry,'title').text=heading
        ET.SubElement(entry,'p').text=definition.strip()
        term_section.insert(location,entry)
    # Preserve the first three hand-typeset semantic sections from the original
    # book. They are editorially cleaner than PDF text extraction, especially
    # for the Ruler Axiom, mathematical fractions, and notes about angles.
    manual_path=Path('source/appendix-b-manual-sections.xml')
    if manual_path.is_file():
        from copy import deepcopy
        manual_root=ET.parse(manual_path).getroot()
        legacy_ids={'theory':'geometry-app-b-theory','length-distance':'geometry-app-b-length-distance','angles':'geometry-app-b-angles'}
        for slug, original_id in legacy_ids.items():
            saved=next((node for node in manual_root.findall('section') if node.get(XMLID)==original_id),None)
            if saved is None:raise RuntimeError('Missing hand-typeset section '+original_id)
            restored=deepcopy(saved)
            # Definition 12 follows the original eleven definitions in the
            # official source; keep it while retaining the hand-typeset text.
            if slug=='angles':
                for node in sections[slug].findall('paragraphs'):
                    if node.get(XMLID)=='geometry-app-b-definition-12':restored.append(deepcopy(node))
            sections[slug]=restored
    else:
        print('WARNING: manual source not present; using PDF-transcribed initial sections')
    append_text(sections['copyright'],'© 2017 Government of Ireland')
    for slug,_ in GROUPS:
        sec=sections[slug];ET.indent(sec,space='  ')
        ET.ElementTree(sec).write(OUT/f'{slug}.ptx',encoding='unicode',xml_declaration=True)
    print('Native sections:',len(GROUPS),'labelled statements:',count,'text words:',words)
    print('Reusable, isolated figures:',len(figures), sorted(figures))
    if len(figures)!=31 or words<7000:raise RuntimeError('Incomplete conversion')
    for filename in OUT.glob('*.ptx'):ET.parse(filename)

if __name__=='__main__':produce()