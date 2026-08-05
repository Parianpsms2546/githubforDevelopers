#!/usr/bin/env python3
"""Package empeo-new-employee-added.html as a .eml, reusing the inline images
(cid:empeo-logo, cid:powered-by-empeo, cid:icon-facebook, cid:icon-youtube)
from a source .eml so the new message renders standalone in any mail client.

    python3 build_eml.py <source.eml> [output.eml]
"""
import email
import sys
from email.message import EmailMessage
from email.utils import make_msgid
from pathlib import Path

HERE = Path(__file__).parent
HTML = HERE / "empeo-new-employee-added.html"

SUBJECT = "พนักงานใหม่ได้ถูกเพิ่มชื่อเข้าสู่ระบบ empeo เรียบร้อยแล้ว"

PLAIN = """พนักงานใหม่ได้ถูกเพิ่มชื่อเข้าสู่ระบบ empeo เรียบร้อยแล้ว

สมปอง หมายปอง
รหัสพนักงาน: EMP-00125
ตำแหน่ง: เจ้าหน้าที่ทรัพยากรบุคคล
สังกัด: ฝ่ายทรัพยากรบุคคล > แผนกสรรหาและว่าจ้าง > ทีมสรรหา
อีเมล: somphong@example.com
หัวหน้างาน: นางสาวกมลชนก ใจดี
ประเภทอัตรา: ทดแทนพนักงานเดิม
ดำเนินการเมื่อ: 5 เมษายน 2566 13:12

ดูข้อมูลพนักงาน: https://app.empeo.com/employee
"""


def collect_images(source_eml):
    """Return {content-id: (bytes, subtype, filename)} from the source message."""
    src = email.message_from_bytes(Path(source_eml).read_bytes())
    images = {}
    for part in src.walk():
        if not part.get_content_type().startswith("image/"):
            continue
        cid = (part.get("Content-ID") or "").strip("<>")
        if not cid:
            continue
        images[cid] = (
            part.get_payload(decode=True),
            part.get_content_subtype(),
            part.get_filename() or f"{cid}.png",
        )
    return images


def build(source_eml, out_path):
    images = collect_images(source_eml)
    html = HTML.read_text(encoding="utf-8")

    msg = EmailMessage()
    msg["Subject"] = SUBJECT
    msg["From"] = "empeo <no-reply@empeo.com>"
    msg["To"] = "hr@example.com"
    msg["MIME-Version"] = "1.0"

    msg.set_content(PLAIN, subtype="plain", charset="utf-8")

    # cid:<name> in the HTML has to match the Content-ID on the related part.
    # make_msgid() would give each image a unique id and break every src, so the
    # ids are kept verbatim from the source message.
    msg.add_alternative(html, subtype="html", charset="utf-8")
    html_part = msg.get_payload()[-1]

    for cid, (data, subtype, filename) in images.items():
        html_part.add_related(
            data,
            maintype="image",
            subtype=subtype,
            cid=f"<{cid}>",
            filename=filename,
        )

    Path(out_path).write_bytes(msg.as_bytes())
    print(f"wrote {out_path} ({len(msg.as_bytes())} bytes, {len(images)} inline images)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    source = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else HERE / "empeo-new-employee-added.eml"
    build(source, out)
