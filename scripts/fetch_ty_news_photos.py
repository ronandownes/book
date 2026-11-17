#!/usr/bin/env python3
"""Fetch the three openly licensed photographs attributed in the TY lesson."""
from pathlib import Path
from urllib.request import Request, urlopen
import time

FILES = {
    'deep-blue.jpg': 'https://upload.wikimedia.org/wikipedia/commons/b/be/Deep_Blue.jpg',
    'lee-sedol.jpg': 'https://upload.wikimedia.org/wikipedia/commons/9/99/Lee_Se-Dol.jpg',
    'wake-vortex.jpg': 'https://upload.wikimedia.org/wikipedia/commons/f/fe/Airplane_vortex_edit.jpg',
}
root = Path('assets/ty-news')
root.mkdir(parents=True, exist_ok=True)
for name, url in FILES.items():
    target = root / name
    if target.is_file() and target.stat().st_size > 5000:
        continue
    for attempt in range(3):
        try:
            request = Request(url, headers={'User-Agent': 'Irish School Maths educational textbook'})
            with urlopen(request, timeout=40) as response:
                data = response.read()
            if not data.startswith(b'\xff\xd8') or len(data) < 5000:
                raise ValueError('Expected a JPEG photograph: ' + name)
            target.write_bytes(data)
            print('Retrieved ' + name + ' (' + str(len(data)) + ' bytes).')
            break
        except Exception:
            if attempt == 2:
                raise
            time.sleep(1 + attempt)
