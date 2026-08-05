#!/usr/bin/env python3
"""Pack leave-request-rejected.html + assets/ into a previewable .eml.

The template references its images as `cid:<name>`; this walks those
references, attaches the matching `assets/<name>.png` as a related part,
and writes an .eml that can be dropped into Outlook / Apple Mail to check
the rendering.

    python3 templates/email/build-eml.py [-o out.eml]
"""

import argparse
import mimetypes
import re
from email.message import EmailMessage
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "leave-request-rejected.html"
ASSETS = HERE / "assets"

SUBJECT = "เอกสารของคุณถูกปฏิเสธ"
FROM = "empeo <no-reply@empeo.com>"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-o", "--output", type=Path, default=HERE / "leave-request-rejected.eml")
    args = ap.parse_args()

    html = TEMPLATE.read_text(encoding="utf-8")

    msg = EmailMessage()
    msg["From"] = FROM
    msg["Subject"] = SUBJECT
    msg["X-Unsent"] = "1"
    msg.set_content("เอกสารของคุณถูกปฏิเสธ — เปิดอีเมลนี้ในโหมด HTML เพื่อดูรายละเอียด")
    msg.add_alternative(html, subtype="html")

    # Attach one related part per distinct cid: reference, in the order they
    # appear, so a template that drops an image stops shipping it too.
    seen = []
    for cid in re.findall(r'src="cid:([^"]+)"', html):
        if cid not in seen:
            seen.append(cid)

    html_part = msg.get_payload()[-1]
    for cid in seen:
        matches = sorted(ASSETS.glob(f"{cid}.*"))
        if not matches:
            raise SystemExit(f"missing asset for cid:{cid} (looked in {ASSETS})")
        asset = matches[0]
        maintype, subtype = (mimetypes.guess_type(asset.name)[0] or "application/octet-stream").split("/")
        html_part.add_related(
            asset.read_bytes(),
            maintype=maintype,
            subtype=subtype,
            cid=f"<{cid}>",
            filename=asset.name,
        )

    args.output.write_bytes(msg.as_bytes())
    print(f"wrote {args.output} ({args.output.stat().st_size:,} bytes, {len(seen)} images)")


if __name__ == "__main__":
    main()
