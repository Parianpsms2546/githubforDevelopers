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

- **Numeric runs must be wrapped in a bare `<a>` with inline styles.** iOS and
  the Gmail app detect codes, dates and postcodes and draw them as blue
  underlined links. The wrapper prevents detection, and the inline
  `text-decoration:none !important` beats an injected inline style. `<style>`
  rules alone are not enough — the Gmail app strips the whole block. Keep
  `color` inline *without* `!important` so dark mode still applies.
- Spacer cells carry the HTML `height` attribute plus a matching `line-height`;
  Outlook honours the attribute and can grow a cell sized only in CSS.
- Images are inlined by CID. Run `build-eml.py <name> "<subject>"` after every
  edit to the HTML — the `.eml` is generated, never hand-edited.
