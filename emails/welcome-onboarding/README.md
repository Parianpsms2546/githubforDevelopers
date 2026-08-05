# empeo welcome / onboarding email

Transactional email sent to a new employee with their empeo sign-in details and
the first things to do. Subject: `ยินดีต้อนรับสู่ทีม เข้าใช้งาน empeo ได้เลย`

## Files

| Path | What it is |
|------|------------|
| `welcome-onboarding.html` | The template. Images are referenced as `cid:NAME`. |
| `images/` | Inline assets, one `NAME.png` per `cid:NAME`. |
| `empeo-welcome-onboarding.eml` | Built message — open it in a mail client to review. |
| `tools/build_eml.py` | Bundles the HTML + images into the `.eml`. |
| `tools/preview.py` | Writes `.preview.html` (cid → `images/`) for browser review. |
| `tools/make_icon_web.py` | Regenerates `images/icon-web.png`, the globe icon. |

## Build

```sh
python3 tools/build_eml.py      # -> empeo-welcome-onboarding.eml
python3 tools/preview.py        # -> .preview.html (git-ignored)
```

Nothing to install: the scripts are stdlib-only.

## Layout notes

- The body is table-based and full-bleed at `min-width:600px`, going fluid under
  600px through the media query in `<head>`.
- Copy is centred throughout: title, subtitles, step titles, step copy, buttons.
- The three store buttons (`iOS` / `Android` / `Website`) share one row and carry
  both a px width attribute (Outlook) and a percentage width (fluid clients), so
  the row divides into equal thirds instead of overflowing at narrow widths. The
  labels drop to 13px under 600px to keep `Android` on one line at 320px.
- In the credentials card, icon → label → `:` are separated by 4px each so the
  icon reads as part of the label. The label and value columns are shared by both
  rows, so the two colons and the two values stay aligned.
- Dark mode is handled with `prefers-color-scheme` plus `[data-ogsc]` /
  `[data-ogsb]` overrides for Outlook mobile.
