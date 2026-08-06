#!/usr/bin/env python3
"""Build the empeo "account deactivated" email.

Outputs:
  - account-deactivated.html : self-contained preview (logo as base64 data URI)
  - account-deactivated.eml  : ready-to-send message (logo embedded via CID)

Design goals:
  - Content stays centered on every client (incl. Outlook / Word engine)
  - Responsive for both mobile and desktop
  - Full dark-mode support
  - Font order exactly as specified:
    Prompt, Inter, "Segoe UI Variable", "SF Pro Text", -apple-system,
    "system-ui", "Noto Sans Thai Looped", system-ui, sans-serif
"""

import base64
import os
from email.message import EmailMessage
from email.utils import make_msgid, formatdate

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(HERE, "assets", "empeo-logo.png")

# ---- Editable content -------------------------------------------------------
RECIPIENT_NAME = "คุณสมหมาย หมายปอง"
SUBJECT = "บัญชีของคุณถูกปิดใช้งาน"
HELP_CENTER_URL = "https://empeo.com/help"
# Exact font order requested by the user.
FONT_STACK = (
    'Prompt, Inter, "Segoe UI Variable", "SF Pro Text", -apple-system, '
    '"system-ui", "Noto Sans Thai Looped", system-ui, sans-serif'
)
# -----------------------------------------------------------------------------


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

  /* Web font for clients that honor @font-face (Apple Mail, iOS Mail) */
  @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@400;500;600;700&display=swap');

  /* ---- Palette (light) ---- */
  .bg-page   {{ background-color:#eeeef3; }}
  .bg-card   {{ background-color:#ffffff; }}
  .c-heading {{ color:#20242e; }}
  .c-body    {{ color:#5b6270; }}
  .c-note    {{ color:#9aa0ac; }}
  .c-foot    {{ color:#b7bcc6; }}
  .c-link    {{ color:#8a90a0; }}
  .divider   {{ border-top:1px solid #e8e9ee; }}

  /* ---- Responsive ---- */
  @media only screen and (max-width:620px) {{
    .container {{ width:100% !important; }}
    .card-pad  {{ padding:32px 22px !important; }}
    .h1        {{ font-size:26px !important; line-height:1.3 !important; }}
    .logo      {{ width:150px !important; height:auto !important; }}
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
      <td align="center" style="padding:32px 16px;">
        <!--[if mso]>
        <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" align="center"><tr><td>
        <![endif]-->
        <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" class="container" style="width:600px; max-width:600px; margin:0 auto;">
          <tr>
            <td align="center" class="bg-card card-pad" style="background-color:#ffffff; border-radius:22px; padding:56px 56px 44px 56px;">

              <!-- Logo -->
              <table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center" style="margin:0 auto;">
                <tr><td align="center" style="padding-bottom:34px;">
                  <img src="{logo_src}" width="176" alt="empeo" class="logo" style="display:block; width:176px; max-width:176px; height:auto; margin:0 auto;">
                </td></tr>
              </table>

              <!-- Heading -->
              <h1 class="h1 c-heading" style="margin:0 0 20px 0; font-family:{FONT_STACK}; font-size:30px; line-height:1.3; font-weight:700; color:#20242e; text-align:center;">
                {SUBJECT}
              </h1>

              <!-- Greeting -->
              <p class="body-txt c-body" style="margin:0 0 22px 0; font-family:{FONT_STACK}; font-size:17px; line-height:1.6; color:#5b6270; text-align:center;">
                เรียน <span class="c-heading" style="font-weight:600; color:#20242e;">{RECIPIENT_NAME}</span>
              </p>

              <!-- Body -->
              <p class="body-txt c-body" style="margin:0; font-family:{FONT_STACK}; font-size:17px; line-height:1.7; color:#5b6270; text-align:center;">
                ขณะนี้ สถานะของคุณบนระบบ empeo ได้ถูกเปลี่ยน<br class="dt-br">
                เป็นบุคคลที่ลาออกจากบริษัท โดยระบบได้ปิดใช้งาน<br class="dt-br">
                และย้ายบัญชีของคุณออกจากกลุ่มผู้ใช้งานภายในบริษัทเรียบร้อยแล้ว
              </p>

              <!-- Divider -->
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 auto;">
                <tr><td class="divider" style="border-top:1px solid #e8e9ee; font-size:0; line-height:0; padding-top:34px;">&nbsp;</td></tr>
              </table>

              <!-- Note -->
              <p class="c-note" style="margin:34px 0 0 0; font-family:{FONT_STACK}; font-size:15px; line-height:1.6; color:#9aa0ac; text-align:center;">
                หากพบว่าเป็นความผิดพลาด กรุณาแจ้งฝ่ายบุคคลหรือผู้ดูแลระบบของคุณได้ทันที
              </p>

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
    with open(LOGO_PATH, "rb") as f:
        logo_bytes = f.read()

    # 1) Self-contained HTML (base64 data URI) for browser preview
    b64 = base64.b64encode(logo_bytes).decode("ascii")
    data_uri = f"data:image/png;base64,{b64}"
    html_standalone = html_body(data_uri)
    with open(os.path.join(HERE, "account-deactivated.html"), "w", encoding="utf-8") as f:
        f.write(html_standalone)

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
        "โดยระบบได้ปิดใช้งาน และย้ายบัญชีของคุณออกจากกลุ่มผู้ใช้งานภายในบริษัทเรียบร้อยแล้ว\n\n"
        "หากพบว่าเป็นความผิดพลาด กรุณาแจ้งฝ่ายบุคคลหรือผู้ดูแลระบบของคุณได้ทันที\n\n"
        "Powered by empeo\n"
        "92 Central Park Offices, Unit MM3205, 32nd Floor,\n"
        "Rama 4 Road, Silom, Bang Rak, Bangkok 10500\n"
        f"Help Center: {HELP_CENTER_URL}\n"
    )
    msg.set_content(plain, subtype="plain", charset="utf-8")
    msg.add_alternative(html_email, subtype="html", charset="utf-8")

    # Attach the logo to the HTML alternative part as a related resource
    html_part = msg.get_payload()[1]
    html_part.add_related(
        logo_bytes, maintype="image", subtype="png", cid=logo_cid, filename="empeo-logo.png"
    )

    with open(os.path.join(HERE, "account-deactivated.eml"), "wb") as f:
        f.write(bytes(msg))

    print("Wrote account-deactivated.html and account-deactivated.eml")


if __name__ == "__main__":
    main()
