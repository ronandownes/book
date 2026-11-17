#!/usr/bin/env python3
"""Give every JC outcome and LC OL syllabus topic the same focused native page.

Run after build_intro_outcomes.py. Official paragraphs are copied unchanged;
illustrative teaching examples are labelled and stored separately.
"""
from copy import deepcopy
from pathlib import Path
import json
import re
from lxml import etree

ROOT = Path('source')
ID = '{http://www.w3.org/XML/1998/namespace}id'
DATA = etree.parse(str(ROOT / 'learning-outcomes-examples.xml'))
EXAMPLES = {e.get('code'): e for e in DATA.findall('example')}
manifest = {'pages': [], 'aliases': {}, 'counts': {}}

def p(parent, text):
    etree.SubElement(parent, 'p').text = text

def save(tree, filename):
    (ROOT / filename).write_bytes(etree.tostring(tree, encoding='utf-8', xml_declaration=True, pretty_print=True))

def note(section, code):
    if code not in EXAMPLES:
        raise ValueError('No curated teaching example for ' + code)
    # Preserve the N.3 example the teacher has explicitly approved.
    if code == 'N.3' and section.find('remark') is not None:
        return
    source = EXAMPLES[code]
    remark = etree.SubElement(section, 'remark')
    remark.set(ID, section.get(ID) + '-teaching-example')
    etree.SubElement(remark, 'title').text = 'Teaching example: ' + source.findtext('title')
    for paragraph in source.findall('p'):
        remark.append(deepcopy(paragraph))

def register(section, code, course, group):
    note(section, code)
    manifest['pages'].append({'id': section.get(ID), 'code': code, 'course': course,
                              'group': group, 'title': section.findtext('title')})

def chapter_from_table(path, course, group, expected, section_id):
    original = etree.parse(str(path)).getroot()
    rows = original.findall('.//tabular/row')[1:]
    if len(rows) != expected:
        raise ValueError(f'{group}: expected {expected} topics, found {len(rows)}')
    chapter = etree.Element('chapter')
    wrapper_id = (f'jc-{path.name.split("-")[1]}-learning-outcomes' if course == 'Junior Cycle'
                  else section_id.removesuffix('-outcomes') + '-learning-outcomes')
    chapter.set(ID, wrapper_id)
    etree.SubElement(chapter, 'title').text = 'Learning Outcomes'
    # Retain the existing overview page and chapter URLs, the full reference
    # table and its source citation. Focused pages are sibling sections.
    overview = deepcopy(original)
    overview.find('title').text = 'Overview — ' + group
    chapter.append(overview)
    codes = []
    for row in rows:
        left, right = row.findall('cell')
        labels = left.findall('p')
        code = ''.join(labels[0].itertext()).strip()
        heading = ' '.join(''.join(x.itertext()).strip() for x in labels[1:])
        heading = re.sub(r'^' + re.escape(code) + r'\s*', '', heading).strip()
        # A footnote printed below topic 1.4 is not part of its title.
        if code == '1.4': heading = 'Statistical reasoning'
        if code == 'GT.3': heading = 'Geometrical proof'
        slug = code.lower().replace('.', '') if course == 'Junior Cycle' else code.replace('.', '-')
        prefix = section_id if course == 'Junior Cycle' else section_id.removesuffix('-outcomes')
        section = etree.SubElement(chapter, 'section')
        section.set(ID, prefix + '-' + slug)
        etree.SubElement(section, 'title').text = code + (' — ' + heading if heading else '')
        paragraphs = right.findall('p')
        if not paragraphs: raise ValueError('Empty official outcome ' + code)
        official = [etree.tostring(x, with_tail=False) for x in paragraphs]
        for paragraph in paragraphs: section.append(deepcopy(paragraph))
        if official != [etree.tostring(x, with_tail=False) for x in section.findall('p')]:
            raise ValueError('Official wording changed in ' + code)
        register(section, code, course, group)
        codes.append(code)
    save(chapter, path.name)
    manifest['counts'][course + ': ' + group] = len(codes)
    return chapter

for key, group, count in [('number','Number',5), ('algebra','Algebra and Functions',7)]:
    path = ROOT / f'jc-{key}-outcomes.ptx'
    tree = etree.parse(str(path))
    sections = tree.findall('section')
    if len(sections) != count: raise ValueError('Incomplete ' + key)
    for section in sections:
        code = re.match(r'(N|AF)\.\d+', section.findtext('title')).group()
        register(section, code, 'Junior Cycle', group)
    save(tree, path.name)
    manifest['counts']['Junior Cycle: ' + group] = count

for key, group, count in [('geometry','Geometry and Trigonometry',6), ('statistics','Statistics and Probability',3)]:
    chapter_from_table(ROOT / f'jc-{key}-outcomes.ptx', 'Junior Cycle', group, count, f'jc-outcomes-{key}')

for key, group, count in [('statistics','Statistics and Probability',7), ('geometry','Geometry and Trigonometry',4),
                           ('number','Number',4), ('algebra','Algebra',4), ('functions','Functions',2)]:
    chapter_from_table(ROOT / f'lc-ol-{key}-outcomes.ptx', 'Leaving Certificate Ordinary Level', group, count, f'lc-ol-{key}-outcomes')

# The existing Unifying Strand reference table remains in the Introduction.
# Its exact statements are also available as individually navigable pages.
intro_source = etree.parse(str(ROOT / 'jc-introduction.ptx'))
unifying = etree.Element('chapter')
unifying.set(ID, 'jc-outcomes-unifying')
etree.SubElement(unifying, 'title').text = 'Unifying Strand Learning Outcomes'
intro = etree.SubElement(unifying, 'introduction')
p(intro, 'These outcomes are developed throughout mathematics. Each page keeps the official statement and shows an example of what it can look like in practice.')
titles = ['Understanding concepts','Applying procedures','Equality','Representations','Connections within mathematics',
          'Connections to the real world','Making sense of a problem','Solving problems','Interpreting a solution',
          'Evaluating solutions','Generalising and conjecturing','Arguments and proofs','Communicating mathematics']
seen = []
for row in intro_source.findall('.//row'):
    cells = row.findall('cell')
    if len(cells) != 2: continue
    code = ''.join(cells[0].itertext()).strip()
    if not re.fullmatch(r'U\.\d+', code): continue
    section = etree.SubElement(unifying, 'section')
    section.set(ID, 'jc-outcomes-unifying-' + code.lower().replace('.', ''))
    etree.SubElement(section, 'title').text = code + ' — ' + titles[int(code.split('.')[1])-1]
    statement = etree.SubElement(section, 'p')
    statement.text = cells[1].text
    for child in cells[1]: statement.append(deepcopy(child))
    register(section, code, 'Junior Cycle', 'Unifying Strand')
    seen.append(code)
if seen != [f'U.{n}' for n in range(1,14)]: raise ValueError('Unifying Strand must contain U.1–U.13')
save(unifying, 'jc-unifying-outcomes.ptx')
manifest['counts']['Junior Cycle: Unifying Strand'] = 13

expected = {f'{prefix}.{n}' for prefix,count in [('U',13),('N',5),('GT',6),('AF',7),('SP',3),('1',7),('2',4),('3',4),('4',4),('5',2)] for n in range(1,count+1)}
actual = [row['code'] for row in manifest['pages']]
if set(actual) != expected or len(actual) != 55 or len(set(actual)) != 55:
    raise ValueError('Every one of the 55 official outcomes/topics must have exactly one page')
if set(EXAMPLES) != expected: raise ValueError('Teaching-example inventory differs from official outcome inventory')
(ROOT / 'learning-outcomes-pages.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')
print('Generated 55 focused pages: 34 Junior Cycle outcomes and 21 LC Ordinary Level topics.')
