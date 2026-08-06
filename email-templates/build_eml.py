#!/usr/bin/env python3
"""Build a ready-to-send .eml file from the account-deactivated HTML template.

Produces an RFC 822 message with a UTF-8 HTML body (base64-encoded so Thai text
is preserved on every mail server) and an RFC 2047 encoded Subject line.
"""
import os
from email.message import EmailMessage
from email.utils import formatdate, make_msgid

HERE = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(HERE, "account-deactivated.html")
EML_PATH = os.path.join(HERE, "account-deactivated.eml")

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

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

with open(EML_PATH, "wb") as f:
    f.write(msg.as_bytes())

print("Wrote:", EML_PATH)
