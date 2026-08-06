# empeo — Account Deactivated Email

HTML email + ready-to-send `.eml` for the empeo "บัญชีของคุณถูกปิดใช้งาน"
(account deactivated) notification.

## Files

| File | Purpose |
|------|---------|
| `account-deactivated.eml` | Ready-to-send message. Logo embedded via `cid:` (multipart/related) so it renders offline in every client. Import/drag into Gmail, Outlook, Apple Mail, or send via any SMTP tool. |
| `account-deactivated.html` | Self-contained HTML (logo as base64 data URI) for previewing in a browser or pasting into an ESP (Mailchimp, SendGrid, etc.). |
| `build_email.py` | Generator for both files. Edit the content block at the top and re-run. |
| `assets/empeo-logo.png` / `.svg` | Official empeo logo (people icon + wordmark). |

## Rebuild

Requires `Pillow` (the build trims the logo's transparent margin so spacing
around it is tight and predictable):

```bash
pip install pillow
python3 build_email.py
```

## Design notes

- **Official logo + flame top accent.** Uses the official empeo logo, with a
  5px flame (`#F15A2E`) accent bar that follows the card's rounded top corners.
- **Centered on every client.** Bulletproof table layout with a `600px`
  centered container, MSO conditional wrapper for Outlook (Word engine),
  and `text-align:center` throughout.
- **Responsive.** Fluid container + `@media (max-width:620px)` — the card
  fills the width with tighter padding and the desktop-only line breaks
  (`.dt-br`) collapse so text reflows naturally on mobile.
- **Dark mode.** `color-scheme: light dark` meta + `@media
  (prefers-color-scheme: dark)` plus `[data-ogsc]` overrides for clients
  that rewrite classes. Card, text, divider, and link all adapt; the orange
  logo reads on both backgrounds so no image swap is needed.
- **Font order** (exactly as specified):
  `Prompt, Inter, "Segoe UI Variable", "SF Pro Text", -apple-system,
  "system-ui", "Noto Sans Thai Looped", system-ui, sans-serif`.
  Prompt is also loaded via `@import` for clients that honor it
  (Apple Mail / iOS Mail); everything else falls back down the stack.

## Editing content

Open `build_email.py` and change `RECIPIENT_NAME`, `SUBJECT`,
`HELP_CENTER_URL`, then re-run. The recipient name is the obvious
personalization point when sending to real employees.
