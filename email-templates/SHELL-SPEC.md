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

Corner radius: **8px** everywhere — content cards and inline note boxes alike.

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

## Swapping the logo for another brand

The header is logo-agnostic in layout: centring, the 16px gap to the heading and
the flush-to-top alignment all hold whatever shape the logo is.

**Build the asset to fit the box; do not change the HTML.** Export every brand
logo onto a **256x128 transparent canvas** (2x of the 128x64 slot) with the
artwork centred. The header then needs no per-brand edit at all — the shell's own
`width="128" height="64"` keeps working.

This matters for spacing, not just sizing. The empeo asset carries about 17.5px of
transparent margin above and below its artwork at display size, and that margin is
part of the perceived gap to the heading: 16px of box spacing plus 17.5px of
padding reads as ~36px. A logo trimmed tight to its ink sits only 16px away and
looks stuck to the heading — which is exactly what happened with bangchak before
it was re-padded.

So: trim the incoming artwork to its real ink, scale it to the slot width, and
centre it on the 256x128 canvas. Measured result — empeo 36px optical gap,
bangchak 37px, both in a 128x64 box.

Two traps when preparing the artwork:

- **Trim before measuring the ratio.** bangchak.svg declares a 3.33:1 box but its
  artwork is 4.54:1 once 210px of transparent padding is removed on each side.
- **An SVG may not be vector.** bangchak.svg is a wrapper around an embedded
  4096x1231 PNG. Pull the bitmap out of the `xlink:href` data URI rather than
  rasterising the SVG box.

If you ever do keep a tightly-trimmed asset instead, the `height` attribute must
match its real ratio — `height:auto` in the stylesheet saves clients that apply
author CSS, but Outlook goes by the attributes and will stretch it.

## Non-negotiables

- **Do not wrap text in `<a>` to stop auto-linking.** Outlook mobile paints
  every link blue, and an inline `color:inherit !important` does not stop it, so
  the wrapper causes the exact problem it was meant to prevent. Three rounds
  were spent learning this: the wrappers turned the payroll period blue as well
  as the code it was protecting.

- **Break the digit run instead**, with a word joiner. Only long runs are
  detected: `12 พ.ย. 2003` was never touched, so four digits is below the
  threshold, while the eight-digit `12112003` was. Use `&#8288;` (U+2060), not
  `&#8203;` (U+200B) — a zero-width *space* is a legal line-break opportunity, so
  it let the reference number split across two lines on mobile. A word joiner is
  zero-width and non-breaking:

  ```html
  เช่น 12 พ.ย. 2003 &rarr; 1211&#8288;2003
  ```

  It stays plain text, inherits the surrounding colour in both schemes, and no
  client can repaint it because there is nothing to repaint. Reads as `12112003`
  on screen. The one cost is a stray invisible character if someone copies it —
  acceptable for an example nobody retypes verbatim, but do not use this on a
  real credential the recipient must copy.

  Leave the `format-detection` meta and the `.no-autolink` rule in place as
  backup for clients that honour them.

  Any visible run of four or more digits needs this, not just the obvious ones —
  the address unit number (`MM3205`) counts.

- **Times are a separate pattern from digit runs.** `hh:mm` is detected on its
  own: Outlook mobile linkified `13:00 - 14:00` even though no run in it exceeds
  two digits. Break each time around its colon:

  ```html
  13&#8288;:&#8288;00 - 14&#8288;:&#8288;00
  ```

  In the preheader — the inbox preview line — write the time in Thai dot form
  (`13.00 - 14.00 น.`) instead, so the preview stays readable rather than
  carrying joiners.

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
- **A rounded table needs `border-collapse:separate`.** The reset forces
  `border-collapse: collapse !important` on every table, and a collapsed table
  cannot render `border-radius` — the corners come out square whatever the value
  is. Any table carrying a radius must override it inline:

  ```html
  style="… border-radius:16px; border-collapse:separate !important; border-spacing:0;"
  ```

  This is why the card looked square at both 8px and 16px. Chromium was lenient
  enough to hide it locally, so trust the client, not the local render. A `<td>`
  with a background and a radius inside a collapsed table is the same risk; the
  file-password box happens to render rounded today, but treat it as fragile.

- **Label / value rows: pin the value column to `width="100%"`.** In a 100%-wide
  table with two auto columns the leftover width lands in the *first* column, so
  the label column inflates and shoves the value across the card. Pinning the
  value column makes it absorb the slack instead, collapsing the label column to
  its own content.

- **Cards must survive a narrow screen.** Give label cells `white-space:nowrap`
  but no fixed width — a fixed width plus nowrap cannot both hold when text
  scales up, and the value column gets squeezed to nothing. Let the label column
  size to its content, keep the gutter as `padding-right`, and both rows still
  line up because they share the column. Keep short bracketed suffixes together
  with `&nbsp;` (`(1&nbsp;วัน)`) and give the status pill `nowrap`.

- **A one-time code goes one digit per cell.** Six digits in a single text node
  is exactly what a phone detector looks for; split across six cells there is no
  contiguous run to match, so no word joiner is needed and nothing can be
  linkified. The cells carry the radius, so their table needs
  `border-collapse:separate` like any other rounded table.

- **A spacer cell collapses next to a `width:100%` column.** `font-size:0` gives
  it no min-content width, so the 100% column takes everything and the gutter
  vanishes — the step titles ran straight into their number badges. Use
  `padding-left` on the content cell for gutters in that situation.

- **A fixed-size cell needs its table sized too.** `width:24px` on a cell inside
  an auto-width table does nothing; the table shrink-wraps to the content and the
  number badge came out 7px wide instead of a 24px circle. Put the width on the
  table as well.

- **A gradient needs the HTML `background` attribute, not CSS.** A `cid:` url
  inside `background-image` is dropped by most clients, so the card arrived flat
  orange. Put `background="cid:x"` on the `<td>`, keep `bgcolor` as the fallback,
  and cut the tile to *exactly* the element's width and only a few px tall — the
  attribute tiles it down with `repeat-y` and never repeats sideways, so no
  `background-size` is involved. Outlook still shows the `bgcolor`, which is why
  the fallback has to look acceptable on its own.

- Images are inlined by CID. Run `build-eml.py <name> "<subject>"` after every
  edit to the HTML — the `.eml` is generated, never hand-edited.
