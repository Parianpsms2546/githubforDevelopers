#!/usr/bin/env python3
"""Bundle an email template's HTML + inline images into a single .eml file.

Usage:
    python3 build-eml.py empeo-account-deletion-grayfooter "คำขอลบบัญชี empeo ของคุณได้รับการอนุมัติแล้ว"

Reads  src/<name>.html, resolves every cid: reference against assets/<cid>.png,
writes <name>.eml as a multipart/related message with X-Unsent: 1 so it opens
as an editable draft in Outlook.
"""
import base64
import re
import sys
from pathlib import Path

BOUNDARY = "empeo_boundary_5f3a1c9b"
FROM = "empeo <parisa.a@gofive.co.th>"
ROOT = Path(__file__).parent


def b64_lines(data: bytes) -> str:
    b = base64.b64encode(data).decode("ascii")
    return "\r\n".join(b[i:i + 76] for i in range(0, len(b), 76))


def build(name: str, subject: str) -> Path:
    html = (ROOT / "src" / f"{name}.html").read_text(encoding="utf-8")

    # Preserve first-seen order, drop duplicates
    cids = list(dict.fromkeys(re.findall(r'src="cid:([^"]+)"', html)))

    out = [
        f"From: {FROM}",
        "To: ",
        "Subject: =?UTF-8?B?" + base64.b64encode(subject.encode()).decode() + "?=",
        "X-Unsent: 1",
        "MIME-Version: 1.0",
        f'Content-Type: multipart/related; boundary="{BOUNDARY}"',
        "",
        f"--{BOUNDARY}",
        'Content-Type: text/html; charset="UTF-8"',
        "Content-Transfer-Encoding: base64",
        "",
        b64_lines(html.encode("utf-8")),
        "",
    ]

    for cid in cids:
        img = ROOT / "assets" / f"{cid}.png"
        if not img.exists():
            sys.exit(f"missing asset for cid:{cid} -> {img}")
        out += [
            f"--{BOUNDARY}",
            f'Content-Type: image/png; name="{img.name}"',
            "Content-Transfer-Encoding: base64",
            f"Content-ID: <{cid}>",
            f'Content-Disposition: inline; filename="{img.name}"',
            "",
            b64_lines(img.read_bytes()),
            "",
        ]

    out += [f"--{BOUNDARY}--", ""]

    dest = ROOT / f"{name}.eml"
    dest.write_text("\r\n".join(out), encoding="utf-8", newline="")
    return dest


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    print("wrote", build(sys.argv[1], sys.argv[2]))
