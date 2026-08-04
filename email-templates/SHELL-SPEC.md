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
| Body copy | 16px | 500 | **30px** |
| Card labels / values | 14px | 400 / 500 | 22px |
| Footer address | 10px | 400 | 16px |

Font stack: `'Kanit', Helvetica, Arial, sans-serif`.

**Kanit needs more headroom than Prompt did.** Its Thai upper tone marks sit
higher, and every clip measured was at the *top* of the line box — where
`mso-line-height-rule:exactly` makes Outlook cut them off rather than overflow.
Measured against the real strings, `font-size + 8` is not enough at 16px: the
worst case, "ติดตั้ง empeo บนมือถือ" at weight 600, still clipped by 0.5px at 26px
and only clears by 1.5px at **30px**. 14px is fine at 22px, 18px at 24px.

So for 16px Thai text use **line-height 30px**, and where a fixed element height
matters, take the difference out of the padding — the CTA is `padding:7px 24px`
with a 30px line box, which keeps it exactly 44px tall and matching its VML
fallback.

Helvetica and Arial carry no Thai glyphs, so on a client without Kanit the OS
picks a Thai fallback of its own. Add a named Thai fallback to the stack if that
substitution ever looks wrong.

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

**Put the spacing in the asset, not in the HTML.** Every brand logo is exported
onto a transparent canvas with a fixed margin baked in around the artwork, and the
header markup only ever changes the `cid`, the `alt`, the link and the `height`
attribute — never the spacing.

This matters for spacing, not just sizing. The empeo asset carries about 17.5px of
transparent margin above and below its artwork at display size, and that margin is
part of the perceived gap to the heading: 16px of box spacing plus 17.5px of
padding reads as ~36px. A logo trimmed tight to its ink sits only 16px away and
looks stuck to the heading — which is exactly what happened with bangchak before
it was re-padded.

The recipe, then, is about the **margin**, not the box:

1. Trim the incoming artwork to its real ink.
2. Scale it so the ink is about **29px tall** at display size — empeo's ink is
   117x29, so matching the height matches the optical weight.
3. Centre it on a transparent canvas **128px wide** with **18px of margin above and
   below**, exported at 2x. Set the `height` attribute to that canvas height.

The box height may differ per brand and that is fine — the gap comes from the
asset's bottom margin, not the box. Measured across four brands: optical gap
36-37px and top margin 17-18px for every one of them.

| Brand | Ink at display size | Canvas | `height` |
|---|---|---|---|
| empeo | 117 x 29 | 128 x 64 | 64 |
| bangchak | 128 x 28 | 128 x 64 | 64 |
| Tech-X | 105 x 29 | 128 x 65 | 65 |
| Gofive | 48 x 48 | 128 x 84 | 84 |

**A square mark is the exception to step 2.** Held to a 29px ink height, Gofive's
1:1 logo would be a 29x29 speck beside a 117px-wide wordmark, so it is scaled to
48px instead. Keeping the 18px margin means the box grows to 84 and the gap is
still 37px — the spacing survives, only the `height` attribute changes.

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

- **The footer row must never stack.** It holds a 60px logo and two 14px icons —
  about 96px of content — so it fits side by side even on a 320px screen. It used
  to carry the usual mobile-stacking kit (`.stack-column { display:block
  !important; width:100% !important }`, `[if mso]` ghost cells, `inline-block`
  wrappers), and that kit is what broke it: **a reading pane narrower than 600px
  is not a phone.** Outlook hands the message ~824px and looked right; a mail
  client in a ~435px pane tripped the `max-width:600px` query, so the two cells
  stacked and the icons centred under the logo. The row is now a plain two-cell
  table — no classes, no media query, no `inline-block`, no conditional comments
  — so there is nothing left for a client to get wrong.

  Only stack a row whose content genuinely cannot fit, and remember that the
  media query fires on the *pane* width, not the device.

- **The whole footer is one table, and that is load-bearing.** Some clients
  ignore `width:100%` and shrink-wrap every table to its own content. The
  logo/icons row holds 96px of it, so as a table of its own it collapsed to 96px
  and the icons ended up against the logo instead of on the right edge — measured
  at 96px wide in a 198px-wide footer. Keeping the row in the same table as the
  address rows (which are `colspan="3"`) forces it to the footer's real width, so
  the icons land on the right edge whatever width the client decides on. Never
  split the footer back into sibling tables.

  Both end columns carry an explicit `width` (60 and 36) so the colspan rows
  cannot squeeze them, and **the 8px gap between the icons is `padding-left`, not
  a spacer cell** — see the spacer-collapse note below; a `font-size:0` spacer
  between them collapsed to 0px and the two icons touched.

- **A fixed pixel width belongs in the attribute, never in the inline CSS.** The
  welcome card was `width="386" style="width:386px; max-width:386px"` to match its
  gradient tile, and the media query's `.cred-bg { width:100% !important }` was the
  only thing shrinking it — so a client that strips `<style>` on a narrow screen
  got a 386px card in a 320px pane and the whole email scrolled sideways. Write it
  as `width="386" style="width:100%; max-width:386px"` instead: Outlook takes the
  attribute and stays at 386, everyone else stays fluid, and nothing depends on the
  stylesheet surviving. The tile just crops on the right when the card is narrower,
  which is what already happened under the media query.

- Images are inlined by CID. Run `build-eml.py <name> "<subject>"` after every
  edit to the HTML — the `.eml` is generated, never hand-edited.
