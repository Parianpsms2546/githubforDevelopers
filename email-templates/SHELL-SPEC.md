# empeo email shell — locked values

The header, footer and vertical rhythm below are fixed. Reuse them for every new
template and only change what sits between the greeting and the CTA.

`src/empeo-account-deletion-grayfooter.html` is the reference implementation.
Start from it, swap the content rows, and leave everything else alone.

## Vertical rhythm

| Gap | Value | Where it lives |
|---|---|---|
| Top of card → logo | **0** | header band `padding:0` |
| Logo → greeting | **16px** | body band `padding-top:16px` |
| Greeting → body copy | **8px** | spacer row, `height="8"` |
| Content → CTA button | **48px** | `padding-top:48px` on the CTA cell |
| CTA button → footer | **60px** | body band `padding-bottom:60px` |
| Footer top / bottom | **24px** | footer band `padding:24px 0` |

The CTA's 48px is padding on the CTA cell, not a spacer row, so it matches the
mechanism of the 60px below it. Clients size padding and spacer cells
differently, so mixing the two makes the two sides of the button drift apart.

## Type

| Element | Size | Weight | Line height |
|---|---|---|---|
| Greeting "สวัสดี " | 18px | 500 | 24px |
| Greeting name | 18px | 700 | 24px |
| Body copy | 16px | 500 | 24px |
| Footer address | 10px | 400 | 16px |

Font stack: `'Prompt','Noto Sans Thai',Tahoma,Arial,sans-serif`.
Flame (buttons, accents): `#F15A2E` — sampled from the logo asset.
Charcoal `#2B2D33` · Iron `#5A5F68` · Muted `#8A8F98` · Footer bg `#F5F6F7`.

## Layout

- Bands are full-bleed: the white body and the grey footer run edge to edge.
- No rounded corners anywhere.
- Each band's content sits in an `align="center"` + `margin:0 auto` table at
  full width, so if a client constrains it the leftover space still splits
  evenly instead of hugging one edge.
- Horizontal padding is 40px, dropping to 24px under 600px via `.px-24`.
- Body copy is centred. A left-aligned paragraph reads as off-centre next to a
  centred greeting and button.

At full width the email's outer left and right margins come from the client's
own container, not from the email. Outlook hands it roughly 824px with uneven
sides, and that cannot be corrected from inside the message. Reintroduce
`max-width` on the `.inner` tables if that ever becomes unacceptable.

## Non-negotiables

- **Do not wrap text in `<a>` to stop auto-linking.** Outlook mobile paints
  every link blue, and an inline `color:inherit !important` does not stop it, so
  the wrapper causes the exact problem it was meant to prevent. Three rounds
  were spent learning this: the wrappers turned the payroll period blue as well
  as the code it was protecting.

- **Break the digit run instead.** Only long runs are detected. `12 พ.ย. 2003`
  was never touched, so a four-digit run is below the threshold, while the
  eight-digit `12112003` was. A single zero-width space splits it:

  ```html
  เช่น 12 พ.ย. 2003 &rarr; 1211&#8203;2003
  ```

  It stays plain text, inherits the surrounding colour in both schemes, and no
  client can repaint it because there is nothing to repaint. Reads as `12112003`
  on screen. The one cost is a stray invisible character if someone copies it —
  acceptable for an example nobody retypes verbatim, but do not use this on a
  real credential the recipient must copy.

  Leave the `format-detection` meta and the `.no-autolink` rule in place as
  backup for clients that honour them.

- **The CTA needs the same protection.** Outlook mobile darkens `#F15A2E` to a
  muddy red in dark mode. The button cell carries `class="btn-bg"`, restored by
  the `[data-ogsb]` / `[data-ogsc]` rules Outlook keys off after it transforms a
  colour, and the label is pinned white with `color` plus
  `-webkit-text-fill-color`, both `!important`.
- Spacer cells carry the HTML `height` attribute plus a matching `line-height`;
  Outlook honours the attribute and can grow a cell sized only in CSS.
- **Never put a `{{TOKEN}}` in an `href`.** Outlook rejects an href that is not a
  valid absolute URL: it drops the link and prints the raw attribute value as
  text over the button, so the CTA reads `[{{DOWNLOAD_URL}}]ดาวน์โหลด`. Ship a
  real `https://` URL and mark the substitution point in a comment beside it.
- Images are inlined by CID. Run `build-eml.py <name> "<subject>"` after every
  edit to the HTML — the `.eml` is generated, never hand-edited.
