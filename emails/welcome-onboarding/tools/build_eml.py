#!/usr/bin/env python3
"""Assemble welcome-onboarding.html + images/ into a single .eml file.

Every image referenced as src="cid:NAME" is attached as images/NAME.png with a
matching Content-ID, so the message renders offline with no remote hosting.

    python3 tools/build_eml.py [-o out.eml]
"""

import argparse
import base64
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))

HTML = os.path.join(ROOT, 'welcome-onboarding.html')
IMAGES = os.path.join(ROOT, 'images')

FROM = 'empeo <parisa.a@gofive.co.th>'
SUBJECT = 'ยินดีต้อนรับสู่ทีม เข้าใช้งาน empeo ได้เลย'
BOUNDARY = 'empeo_boundary_5f3a1c9b'


def b64_lines(raw):
    """Base64 wrapped at 76 characters, as MIME wants it."""
    enc = base64.b64encode(raw).decode('ascii')
    return '\r\n'.join(enc[i:i + 76] for i in range(0, len(enc), 76))


def build():
    with open(HTML, 'rb') as fh:
        html = fh.read()

    cids = []
    for cid in re.findall(rb'src="cid:([^"]+)"', html):
        cid = cid.decode('ascii')
        if cid not in cids:
            cids.append(cid)

    parts = [
        'From: %s' % FROM,
        'To: ',
        'Subject: =?UTF-8?B?%s?=' % base64.b64encode(SUBJECT.encode('utf-8')).decode('ascii'),
        'X-Unsent: 1',
        'MIME-Version: 1.0',
        'Content-Type: multipart/related; boundary="%s"' % BOUNDARY,
        '',
        '--%s' % BOUNDARY,
        'Content-Type: text/html; charset="UTF-8"',
        'Content-Transfer-Encoding: base64',
        '',
        b64_lines(html),
        '',
    ]

    for cid in cids:
        path = os.path.join(IMAGES, cid + '.png')
        if not os.path.exists(path):
            raise SystemExit('missing image for cid:%s (expected %s)' % (cid, path))
        with open(path, 'rb') as fh:
            raw = fh.read()
        parts += [
            '--%s' % BOUNDARY,
            'Content-Type: image/png; name="%s.png"' % cid,
            'Content-Transfer-Encoding: base64',
            'Content-ID: <%s>' % cid,
            'Content-Disposition: inline; filename="%s.png"' % cid,
            '',
            b64_lines(raw),
            '',
        ]

    parts += ['--%s--' % BOUNDARY, '']
    return '\r\n'.join(parts), cids


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-o', '--out', default=os.path.join(ROOT, 'empeo-welcome-onboarding.eml'))
    args = ap.parse_args()

    eml, cids = build()
    with open(args.out, 'w', encoding='utf-8', newline='') as fh:
        fh.write(eml)
    print('wrote %s (%d bytes, %d inline images: %s)'
          % (args.out, len(eml), len(cids), ', '.join(cids)))
