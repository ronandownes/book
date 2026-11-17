#!/usr/bin/env python3
"""Verify and enhance all 55 native outcome/topic pages after the HTML build."""
from pathlib import Path
import json
import shutil
from lxml import etree, html

site = Path('output/web')
manifest = json.loads(Path('source/learning-outcomes-pages.json').read_text(encoding='utf-8'))
assert len(manifest['pages']) == 55
for suffix in ['js', 'css']:
    shutil.copy2(f'assets/jc-algebra-outcome-slides.{suffix}', site)

for item in manifest['pages']:
    path = site / (item['id'] + '.html')
    page = path.read_text(encoding='utf-8')
    parsed = html.fromstring(page)
    sections = parsed.xpath('//section[@id=$ident]', ident=item['id'])
    if len(sections) != 1:
        raise ValueError('Focused native section missing: ' + path.name)
    section = sections[0]
    official = section.xpath('./div[contains(concat(" ", normalize-space(@class), " "), " para ")]')
    examples = section.xpath('./article[contains(concat(" ", normalize-space(@class), " "), " remark ")]')
    if not official or len(examples) != 1 or 'Teaching example:' not in examples[0].text_content():
        raise ValueError('Official statement or teaching example missing: ' + path.name)
    if item['code'] not in section.text_content():
        raise ValueError('Wrong outcome code: ' + path.name)
    attributes = {'data-outcome-code': item['code'], 'data-outcome-course': item['course'],
                  'data-outcome-group': item['group']}
    old = '<section class="section" id="' + item['id'] + '">'
    if old not in page:
        # Retain any native classes/attributes when serialising the opening tag.
        import re
        match = re.search(r'<section\b[^>]*\bid="' + re.escape(item['id']) + r'"[^>]*>', page)
        if not match: raise ValueError('Cannot locate section opening: ' + path.name)
        old = match.group()
    addition = ''.join(' ' + key + '=' + json.dumps(value, ensure_ascii=False) for key,value in attributes.items())
    if 'data-outcome-code=' not in old:
        page = page.replace(old, old[:-1] + addition + '>', 1)
    # AF pages may already have the legacy injector. Upgrade it without adding
    # a second script or a second presentation button.
    page = page.replace('jc-algebra-outcome-slides.css?v=2', 'jc-algebra-outcome-slides.css?v=3')
    page = page.replace('jc-algebra-outcome-slides.js?v=2', 'jc-algebra-outcome-slides.js?v=3')
    if 'src="jc-algebra-outcome-slides.js?' not in page:
        css = '<link rel="stylesheet" href="jc-algebra-outcome-slides.css?v=3" data-outcome-display="1"/>'
        script = '<script defer src="jc-algebra-outcome-slides.js?v=3" data-outcome-display="1"></script>'
        page = page.replace('</head>', '  ' + css + '\n</head>', 1)
        page = page.replace('</body>', '  ' + script + '\n</body>', 1)
    path.write_text(page, encoding='utf-8')

# Verify the complete source structure, including exact-once IDs and the
# original N.3 example, before allowing deployment.
doc = etree.parse('source/main.ptx')
doc.xinclude()
ids = doc.xpath('//@xml:id', namespaces={'xml':'http://www.w3.org/XML/1998/namespace'})
if len(ids) != len(set(ids)): raise ValueError('Duplicate PreTeXt IDs')
if len(doc.xpath('//*[@xml:id="jc-number-n3-comparison"]', namespaces={'xml':'http://www.w3.org/XML/1998/namespace'})) != 1:
    raise ValueError('The approved N.3 teaching example changed or disappeared')
for item in manifest['pages']:
    if sum(ident == item['id'] for ident in ids) != 1: raise ValueError('Outcome not included in the book: ' + item['id'])
print('Verified all 55 focused pages: full official statements, labelled examples and optional presentations.')
