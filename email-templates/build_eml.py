#!/usr/bin/env python3
"""Build ready-to-send .eml files from the empeo HTML email templates.

Each message:
  - RFC 2047 encoded Subject (Thai-safe)
  - UTF-8 (base64) HTML body so Thai text survives every mail server
  - empeo logos (color, white, powered-by) embedded as inline CID attachments
    so they render even where base64/remote images are blocked (Gmail).
"""
import os
from email.message import EmailMessage
from email.utils import formatdate, make_msgid

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

# Fixed Content-IDs referenced from the HTML after rewrite.
CID_COLOR = "empeo-logo"
CID_WHITE = "empeo-logo-white"
CID_POWERED = "powered-by-empeo"
CID_PAYSLIP = "empeo-e-payslip"

# (cid, asset filename) pairs; each is embedded only if the HTML references it.
RELATED = [
    (CID_COLOR, "empeo-logo.png"),
    (CID_WHITE, "empeo-logo-white.png"),
    (CID_POWERED, "powered-by-empeo.png"),
    (CID_PAYSLIP, "empeo-e-payslip.png"),
]


def load(name):
    with open(os.path.join(ASSETS, name), "rb") as fh:
        return fh.read()


def build(html_name, eml_name, subject, text, subs=None):
    with open(os.path.join(HERE, html_name), "r", encoding="utf-8") as f:
        html = f.read()

    # Fill in merge placeholders for the sample .eml so it renders cleanly in
    # every client (e.g. Outlook shows raw {{...}} tags otherwise). The HTML
    # template on disk keeps the placeholders for real mail-merge sending.
    for key, val in (subs or {}).items():
        html = html.replace(key, val)
        text = text.replace(key, val)

    # Point the <img> tags at the inline attachments instead of the relative
    # files. Replace the more specific paths first.
    html = html.replace("assets/empeo-e-payslip.png", "cid:%s" % CID_PAYSLIP)
    html = html.replace("assets/powered-by-empeo.png", "cid:%s" % CID_POWERED)
    html = html.replace("assets/empeo-logo-white.png", "cid:%s" % CID_WHITE)
    html = html.replace("assets/empeo-logo.png", "cid:%s" % CID_COLOR)

    msg = EmailMessage()
    msg["Subject"] = subject                       # auto RFC 2047 encoded
    msg["From"] = "empeo <no-reply@empeo.com>"
    msg["To"] = "คุณสมหมาย หมายปอง <employee@example.com>"
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="empeo.com")
    msg["MIME-Version"] = "1.0"

    # multipart/alternative: text first, HTML second (preferred by clients)
    msg.set_content(text, subtype="plain", charset="utf-8")
    msg.add_alternative(html, subtype="html", charset="utf-8")

    # Attach the images as inline (CID) attachments related to the HTML part —
    # but only the ones this template actually references.
    html_part = msg.get_payload()[1]
    for cid, fn in RELATED:
        if ("cid:%s" % cid) in html:
            html_part.add_related(load(fn), "image", "png",
                                  cid="<%s>" % cid, disposition="inline",
                                  filename=fn)

    out = os.path.join(HERE, eml_name)
    with open(out, "wb") as f:
        f.write(msg.as_bytes())
    print("Wrote:", out)


# --- Account deactivated (offboarding status change) ---
build(
    "account-deactivated.html",
    "account-deactivated.eml",
    "บัญชีของคุณถูกปิดใช้งาน",
    (
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
    ),
)

# --- Account deleted (data removed) ---
build(
    "account-deleted.html",
    "account-deleted.eml",
    "ลบบัญชีของคุณเรียบร้อยแล้ว",
    (
        "ลบบัญชีของคุณเรียบร้อยแล้ว\n\n"
        "เรียน คุณสมหมาย หมายปอง\n\n"
        "คำขอการลบบัญชีของคุณได้รับการอนุมัติ\n"
        "โดยข้อมูลทั้งหมดของคุณได้ถูกลบออกจากระบบอย่างถาวรเรียบร้อยแล้ว\n\n"
        "ติดต่อเรา: https://www.empeo.com/contact\n\n"
        "ขอขอบคุณที่ให้ความไว้วางใจเราเสมอมา :)\n\n"
        "-----\n"
        "Powered by empeo\n"
        "92 Central Park Offices, Unit MM3205, 32nd Floor,\n"
        "Rama 4 Road, Silom, Bang Rak, Bangkok 10500\n"
        "Help Center: https://www.empeo.com/help\n"
    ),
)

# --- Document rejected (leave request rejected) ---
build(
    "document-rejected.html",
    "document-rejected.eml",
    "เอกสารของคุณถูกปฏิเสธ",
    (
        "เอกสารของคุณถูกปฏิเสธ\n\n"
        "สวัสดี คุณสมหมาย หมายปอง\n\n"
        "ลาป่วย (L230200033)   [ปฏิเสธ]\n"
        "วันที่: 25 กรกฎาคม 2565 (1 วัน)\n"
        "รายละเอียด: เป็นไข้ใจ\n\n"
        "ดูเอกสาร: {{DOCUMENT_URL}}\n\n"
        "-----\n"
        "Powered by empeo\n"
        "92 Central Park Offices, Unit MM3205, 32nd Floor,\n"
        "Rama 4 Road, Silom, Bang Rak, Bangkok 10500\n"
        "Help Center: https://www.empeo.com/help\n"
    ),
    subs={"{{DOCUMENT_URL}}": "https://app.empeo.com/documents/L230200033"},
)

# --- Payslip ready (download e-payslip) ---
build(
    "payslip-ready.html",
    "payslip-ready.eml",
    "สลิปเงินเดือนของคุณพร้อมให้ดาวน์โหลดแล้ว",
    (
        "สวัสดี สมปอง หมายปอง\n\n"
        "สามารถดาวน์โหลดสลิปเงินเดือนด้านล่างได้ทันที\n\n"
        "รอบเงินเดือน: 1 – 31 ธันวาคม 2566\n"
        "รหัสผ่านในการเปิดไฟล์ของท่าน: วันเดือนปีเกิด ววดดปปปป (ค.ศ.) ของท่าน\n\n"
        "ดาวน์โหลด: {{DOWNLOAD_URL}}\n\n"
        "-----\n"
        "Powered by empeo\n"
        "92 Central Park Offices, Unit MM3205, 32nd Floor,\n"
        "Rama 4 Road, Silom, Bang Rak, Bangkok 10500\n"
        "Help Center: https://www.empeo.com/help\n"
    ),
    subs={"{{DOWNLOAD_URL}}": "https://app.empeo.com/payslip/2566-12"},
)

# --- Interview invitation ---
build(
    "interview-invitation.html",
    "interview-invitation.eml",
    "นัดสัมภาษณ์งานวันนี้",
    (
        "นัดสัมภาษณ์งานวันนี้\n\n"
        "สวัสดี อิสรีย์ สินสุขไชย\n\n"
        "คุณมีนัดสัมภาษณ์งานกับเราในตำแหน่ง Front End Developer\n\n"
        "รายละเอียดการสัมภาษณ์\n"
        "วันที่: 25 กรกฎาคม 2565 เวลา 13:00-14:00\n"
        "สถานที่: สัมภาษณ์ออนไลน์\n"
        "ข้อมูลเพิ่มเติม: Meeting ID: 435 453 627 708 / Passcode: kvuJiJ\n\n"
        "เรายินดีอย่างยิ่งที่จะได้รู้จักคุณมากขึ้น แล้วพบกัน :)\n\n"
        "เข้าร่วมสัมภาษณ์: {{INTERVIEW_URL}}\n\n"
        "-----\n"
        "Powered by empeo\n"
        "92 Central Park Offices, Unit MM3205, 32nd Floor,\n"
        "Rama 4 Road, Silom, Bang Rak, Bangkok 10500\n"
        "Help Center: https://www.empeo.com/help\n"
    ),
    subs={"{{INTERVIEW_URL}}": "https://app.empeo.com/interview/435453627708"},
)

# --- Interview invitation (v2: OTP-style date box, no frame) ---
build(
    "interview-invitation-v2.html",
    "interview-invitation-v2.eml",
    "นัดสัมภาษณ์งานวันนี้",
    (
        "นัดสัมภาษณ์งานวันนี้\n\n"
        "สวัสดี อิสรีย์ สินสุขไชย\n\n"
        "คุณมีนัดสัมภาษณ์งานกับเราในตำแหน่ง Front End Developer\n\n"
        "25 กรกฎาคม 2565 เวลา 13:00 - 14:00\n\n"
        "รายละเอียดการสัมภาษณ์\n"
        "สถานที่: ห้องประชุม Apollo อาคาร B บริษัท โกไฟว์ จำกัด\n"
        "ข้อมูลเพิ่มเติม: กรุณาแต่งกายให้สุภาพและเปิดกล้องขณะสัมภาษณ์ "
        "หากถึงที่นัดหมายแล้วกรุณาติดต่อคุณลนภา\n\n"
        "เรายินดีอย่างยิ่งที่จะได้รู้จักคุณมากขึ้น แล้วพบกัน :)\n\n"
        "เข้าร่วมสัมภาษณ์: {{INTERVIEW_URL}}\n\n"
        "-----\n"
        "Powered by empeo\n"
        "92 Central Park Offices, Unit MM3205, 32nd Floor,\n"
        "Rama 4 Road, Silom, Bang Rak, Bangkok 10500\n"
        "Help Center: https://www.empeo.com/help\n"
    ),
    subs={"{{INTERVIEW_URL}}": "https://app.empeo.com/interview/435453627708"},
)
