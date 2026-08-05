#!/usr/bin/env python3
"""Write .preview.html — welcome-onboarding.html with cid: refs rewritten to
images/ paths, so the template can be opened in a browser.

Build artefact, git-ignored. The .eml is the deliverable; this is for eyeballing.

    python3 tools/preview.py && open .preview.html
"""

import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))

SRC = os.path.join(ROOT, 'welcome-onboarding.html')
OUT = os.path.join(ROOT, '.preview.html')

with open(SRC, encoding='utf-8') as fh:
    html = fh.read()

html = re.sub(r'src="cid:([^"]+)"', r'src="images/\1.png"', html)

with open(OUT, 'w', encoding='utf-8') as fh:
    fh.write(html)

print('wrote', OUT)
