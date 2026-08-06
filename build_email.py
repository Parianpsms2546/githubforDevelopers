#!/usr/bin/env python3
"""Build the empeo "account deactivated" email.

Outputs:
  - account-deactivated.html : self-contained preview (logo as base64 data URI)
  - account-deactivated.eml  : ready-to-send message (logo embedded via CID)

Design goals:
  - Content stays centered on every client (incl. Outlook / Word engine)
  - Responsive for both mobile and desktop
  - Full dark-mode support
  - Flame top accent bar that follows the card's rounded corners
  - Font order exactly as specified:
    Prompt, Inter, "Segoe UI Variable", "SF Pro Text", -apple-system,
    "system-ui", "Noto Sans Thai Looped", system-ui, sans-serif
"""

import base64
import io
import os
from email.message import EmailMessage
from email.utils import make_msgid, formatdate

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(HERE, "assets", "empeo-logo.png")

# ---- Editable content -------------------------------------------------------
RECIPIENT_NAME = "คุณสมหมาย หมายปอง"
SUBJECT = "บัญชีของคุณถูกปิดใช้งาน"
HELP_CENTER_URL = "https://empeo.com/help"
FLAME = "#F15A2E"  # sampled from the official empeo logo
# Exact font order requested by the user.
FONT_STACK = (
    'Prompt, Inter, "Segoe UI Variable", "SF Pro Text", -apple-system, '
    '"system-ui", "Noto Sans Thai Looped", system-ui, sans-serif'
)
# Displayed logo width (px). The official asset is trimmed at build time so
# spacing around it is tight and predictable.
LOGO_DISPLAY_W = 150
# -----------------------------------------------------------------------------


def trimmed_logo_bytes() -> bytes:
    """Load the official logo and trim its transparent margin to a small,
    uniform padding so the logo→heading gap is controlled purely by CSS."""
    im = Image.open(LOGO_PATH).convert("RGBA")
    bbox = im.getbbox()
    if bbox:
        pad = 6  # tiny uniform breathing room
        left = max(bbox[0] - pad, 0)
        top = max(bbox[1] - pad, 0)
        right = min(bbox[2] + pad, im.width)
        bottom = min(bbox[3] + pad, im.height)
        im = im.crop((left, top, right, bottom))
    out = io.BytesIO()
    im.save(out, format="PNG")
    return out.getvalue()


def html_body(logo_src: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="th" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="color-scheme" content="light dark">
<meta name="supported-color-schemes" content="light dark">
<title>{SUBJECT}</title>
<!--[if mso]>
<noscript><xml><o:OfficeDocumentSettings><o:AllowPNG/><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml></noscript>
<![endif]-->
<style>
  /* ---- Base resets ---- */
  html, body {{ margin:0 !important; padding:0 !important; width:100% !important; }}
  * {{ -ms-text-size-adjust:100%; -webkit-text-size-adjust:100%; }}
  table, td {{ mso-table-lspace:0pt; mso-table-rspace:0pt; border-collapse:collapse; }}
  img {{ border:0; height:auto; line-height:100%; outline:none; text-decoration:none; -ms-interpolation-mode:bicubic; }}
  a {{ text-decoration:none; }}
  body, table, td, p, a, span {{ font-family:{FONT_STACK}; }}

  /* Web font for clients that honor @import (Apple Mail, iOS Mail) */
  @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@400;500;600;700&display=swap');

  /* ---- Palette (light) ---- */
  .bg-page   {{ background-color:#eeeef3; }}
  .bg-card   {{ background-color:#ffffff; }}
  .bar       {{ background-color:{FLAME}; }}
  .c-heading {{ color:#20242e; }}
  .c-body    {{ color:#5b6270; }}
  .c-note    {{ color:#9aa0ac; }}
  .c-foot    {{ color:#b7bcc6; }}
  .c-link    {{ color:#8a90a0; }}
  .divider   {{ border-top:1px solid #e8e9ee; }}

  /* ---- Responsive ---- */
  @media only screen and (max-width:620px) {{
    .container {{ width:100% !important; }}
    .card-pad  {{ padding:36px 22px 40px 22px !important; }}
    .h1        {{ font-size:26px !important; line-height:1.3 !important; }}
    .logo      {{ width:132px !important; height:auto !important; }}
    .body-txt  {{ font-size:16px !important; }}
    .dt-br     {{ display:none !important; }}
  }}

  /* ---- Dark mode ---- */
  @media (prefers-color-scheme: dark) {{
    body, .bg-page {{ background-color:#0f1116 !important; }}
    .bg-card   {{ background-color:#1c1f27 !important; }}
    .c-heading {{ color:#f4f5f8 !important; }}
    .c-body    {{ color:#c4c9d4 !important; }}
    .c-note    {{ color:#9096a2 !important; }}
    .c-foot    {{ color:#767c88 !important; }}
    .c-link    {{ color:#a7adbb !important; }}
    .divider   {{ border-top-color:#34373f !important; }}
  }}
  /* Explicit theme overrides (clients that stamp data-theme / classes) */
  [data-ogsc] .bg-page {{ background-color:#0f1116 !important; }}
  [data-ogsc] .bg-card {{ background-color:#1c1f27 !important; }}
  [data-ogsc] .c-heading {{ color:#f4f5f8 !important; }}
  [data-ogsc] .c-body {{ color:#c4c9d4 !important; }}
  [data-ogsc] .c-note {{ color:#9096a2 !important; }}
  [data-ogsc] .c-foot {{ color:#767c88 !important; }}
</style>
</head>
<body class="bg-page" style="margin:0; padding:0; width:100%; background-color:#eeeef3;">
  <!-- Preheader (hidden) -->
  <div style="display:none; max-height:0; overflow:hidden; mso-hide:all; font-size:1px; line-height:1px; color:#eeeef3; opacity:0;">
    สถานะบัญชี empeo ของคุณถูกเปลี่ยนเป็นบุคคลที่ลาออกจากบริษัท
  </div>

  <!-- Full-width centering wrapper -->
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" class="bg-page" style="background-color:#eeeef3;">
    <tr>
      <td align="center" style="padding:36px 16px;">
        <!--[if mso]>
        <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" align="center"><tr><td>
        <![endif]-->
        <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" class="container" style="width:600px; max-width:600px; margin:0 auto;">
          <!-- Card -->
          <tr>
            <td class="bg-card" style="background-color:#ffffff; border-radius:20px; overflow:hidden;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <!-- Flame top accent bar (follows the rounded top corners) -->
                <tr>
                  <td class="bar" height="5" style="height:5px; line-height:5px; font-size:0; background-color:{FLAME}; border-radius:20px 20px 0 0;">&nbsp;</td>
                </tr>
                <!-- Content -->
                <tr>
                  <td align="center" class="card-pad" style="padding:48px 56px 44px 56px;">

                    <!-- Logo -->
                    <img src="{logo_src}" width="{LOGO_DISPLAY_W}" alt="empeo" class="logo" style="display:block; width:{LOGO_DISPLAY_W}px; max-width:{LOGO_DISPLAY_W}px; height:auto; margin:0 auto 18px auto;">

                    <!-- Heading -->
                    <h1 class="h1 c-heading" style="margin:0 0 24px 0; font-family:{FONT_STACK}; font-size:30px; line-height:1.3; font-weight:700; color:#20242e; text-align:center;">
                      {SUBJECT}
                    </h1>

                    <!-- Greeting -->
                    <p class="body-txt c-body" style="margin:0 0 22px 0; font-family:{FONT_STACK}; font-size:17px; line-height:1.6; color:#5b6270; text-align:center;">
                      เรียน <span class="c-heading" style="font-weight:600; color:#20242e;">{RECIPIENT_NAME}</span>
                    </p>

                    <!-- Body (breaks are whitespace-free so mobile joins Thai text without stray spaces) -->
                    <p class="body-txt c-body" style="margin:0; font-family:{FONT_STACK}; font-size:17px; line-height:1.75; color:#5b6270; text-align:center;">ขณะนี้ สถานะของคุณบนระบบ empeo ได้ถูกเปลี่ยนเป็นบุคคล<br class="dt-br">ที่ลาออกจากบริษัท โดยระบบได้ปิดใช้งานและย้ายบัญชี<br class="dt-br">ของคุณออกจากกลุ่มผู้ใช้งานภายในบริษัทเรียบร้อยแล้ว</p>

                    <!-- Divider -->
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 auto;">
                      <tr><td class="divider" style="border-top:1px solid #e8e9ee; font-size:0; line-height:0; padding-top:38px;">&nbsp;</td></tr>
                    </table>

                    <!-- Note -->
                    <p class="c-note" style="margin:36px 0 0 0; font-family:{FONT_STACK}; font-size:15px; line-height:1.65; color:#9aa0ac; text-align:center;">
                      หากพบว่าเป็นความผิดพลาด กรุณาแจ้งฝ่ายบุคคลหรือผู้ดูแลระบบของคุณได้ทันที
                    </p>

                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td align="center" style="padding:30px 24px 8px 24px;">
              <p class="c-foot" style="margin:0 0 4px 0; font-family:{FONT_STACK}; font-size:13px; line-height:1.7; color:#b7bcc6; text-align:center;">
                Powered by empeo
              </p>
              <p class="c-foot" style="margin:0 0 4px 0; font-family:{FONT_STACK}; font-size:13px; line-height:1.7; color:#b7bcc6; text-align:center;">
                92 Central Park Offices, Unit MM3205, 32nd Floor,<br class="dt-br">
                Rama 4 Road, Silom, Bang Rak, Bangkok 10500
              </p>
              <p style="margin:8px 0 0 0; font-family:{FONT_STACK}; font-size:13px; line-height:1.7; text-align:center;">
                <a href="{HELP_CENTER_URL}" class="c-link" style="color:#8a90a0; text-decoration:underline;">Help Center</a>
              </p>
            </td>
          </tr>
        </table>
        <!--[if mso]>
        </td></tr></table>
        <![endif]-->
      </td>
    </tr>
  </table>
</body>
</html>"""


def main():
    logo_bytes = trimmed_logo_bytes()

    # 1) Self-contained HTML (base64 data URI) for browser preview
    b64 = base64.b64encode(logo_bytes).decode("ascii")
    data_uri = f"data:image/png;base64,{b64}"
    with open(os.path.join(HERE, "account-deactivated.html"), "w", encoding="utf-8") as f:
        f.write(html_body(data_uri))

    # 2) .eml with logo embedded via CID (multipart/related)
    logo_cid = make_msgid(domain="empeo.com")
    cid_ref = "cid:" + logo_cid[1:-1]  # strip angle brackets
    html_email = html_body(cid_ref)

    msg = EmailMessage()
    msg["Subject"] = SUBJECT
    msg["From"] = "empeo <no-reply@empeo.com>"
    msg["To"] = RECIPIENT_NAME + " <employee@example.com>"
    msg["Date"] = formatdate(localtime=True)
    msg["MIME-Version"] = "1.0"

    plain = (
        f"{SUBJECT}\n\n"
        f"เรียน {RECIPIENT_NAME}\n\n"
        "ขณะนี้ สถานะของคุณบนระบบ empeo ได้ถูกเปลี่ยนเป็นบุคคลที่ลาออกจากบริษัท "
        "โดยระบบได้ปิดใช้งานและย้ายบัญชีของคุณออกจากกลุ่มผู้ใช้งานภายในบริษัทเรียบร้อยแล้ว\n\n"
        "หากพบว่าเป็นความผิดพลาด กรุณาแจ้งฝ่ายบุคคลหรือผู้ดูแลระบบของคุณได้ทันที\n\n"
        "Powered by empeo\n"
        "92 Central Park Offices, Unit MM3205, 32nd Floor,\n"
        "Rama 4 Road, Silom, Bang Rak, Bangkok 10500\n"
        f"Help Center: {HELP_CENTER_URL}\n"
    )
    msg.set_content(plain, subtype="plain", charset="utf-8")
    msg.add_alternative(html_email, subtype="html", charset="utf-8")

    html_part = msg.get_payload()[1]
    html_part.add_related(
        logo_bytes, maintype="image", subtype="png", cid=logo_cid, filename="empeo-logo.png"
    )

    with open(os.path.join(HERE, "account-deactivated.eml"), "wb") as f:
        f.write(bytes(msg))

    print("Wrote account-deactivated.html and account-deactivated.eml")


if __name__ == "__main__":
    main()
