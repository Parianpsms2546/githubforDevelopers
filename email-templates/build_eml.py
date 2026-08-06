#!/usr/bin/env python3
"""Build a ready-to-send .eml file from the account-deactivated HTML template.

Produces an RFC 822 message where:
  - the Subject is RFC 2047 encoded (Thai-safe)
  - the HTML body is UTF-8 (base64) so Thai text survives every mail server
  - the empeo logo (color + white) is embedded as inline CID attachments, so it
    renders reliably even in clients that block base64/remote images (Gmail).
"""
import os
from email.message import EmailMessage
from email.utils import formatdate, make_msgid

HERE = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(HERE, "account-deactivated.html")
EML_PATH = os.path.join(HERE, "account-deactivated.eml")
ASSETS = os.path.join(HERE, "assets")

# Fixed Content-IDs referenced from the HTML after rewrite.
CID_COLOR = "empeo-logo"
CID_WHITE = "empeo-logo-white"

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Point the <img> tags at the inline attachments instead of the relative files.
# Replace the white path first (it is the longer, more specific string).
html = html.replace("assets/empeo-logo-white.png", "cid:%s" % CID_WHITE)
html = html.replace("assets/empeo-logo.png", "cid:%s" % CID_COLOR)

# Plain-text fallback for clients that don't render HTML.
text = (
    "บัญชีของคุณถูกปิดใช้งาน\n\n"
    "เรียน คุณสมหมาย หมายปอง\n\n"
    "ขณะนี้ สถานะของคุณบนระบบ empeo ได้ถูกเปลี่ยนเป็นบุคคลที่ลาออกจากบริษัท "
    "โดยระบบได้ปิดใช้งานและย้ายบัญชีของคุณออกจากกลุ่มผู้ใช้งานภายในบริษัทเรียบร้อยแล้ว\n\n"
    "หากพบว่าเป็นความผิดพลาด กรุณาแจ้งฝ่ายบุคคลหรือผู้ดูแลระบบของคุณได้ทันที\n\n"
    "-----\n"
    "Powered by empeo\n"
    "92 Central Park Offices, Unit MM3205, 32nd Floor,\n"
    "Rama 4 Road, Silom, Bang Rak, Bangkok 10500\n"
    "Help Center: https://www.empeo.com/help\n"
)


def load(name):
    with open(os.path.join(ASSETS, name), "rb") as fh:
        return fh.read()


msg = EmailMessage()
msg["Subject"] = "บัญชีของคุณถูกปิดใช้งาน"          # auto RFC 2047 encoded
msg["From"] = "empeo <no-reply@empeo.com>"
msg["To"] = "คุณสมหมาย หมายปอง <employee@example.com>"
msg["Date"] = formatdate(localtime=True)
msg["Message-ID"] = make_msgid(domain="empeo.com")
msg["MIME-Version"] = "1.0"

# multipart/alternative: text first, HTML second (preferred by clients)
msg.set_content(text, subtype="plain", charset="utf-8")
msg.add_alternative(html, subtype="html", charset="utf-8")

# Attach the logos as inline (CID) images related to the HTML part. This turns
# the HTML alternative into a multipart/related container.
html_part = msg.get_payload()[1]
html_part.add_related(load("empeo-logo.png"), "image", "png",
                      cid="<%s>" % CID_COLOR, disposition="inline",
                      filename="empeo-logo.png")
html_part.add_related(load("empeo-logo-white.png"), "image", "png",
                      cid="<%s>" % CID_WHITE, disposition="inline",
                      filename="empeo-logo-white.png")

with open(EML_PATH, "wb") as f:
    f.write(msg.as_bytes())

print("Wrote:", EML_PATH)
