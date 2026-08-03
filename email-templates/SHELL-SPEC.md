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

- **Numeric runs must be wrapped like this**, or iOS, the Gmail app and Outlook
  mobile will detect codes, dates and postcodes and paint them as blue
  underlined links:

  ```html
  <a href="#" style="…; color:inherit !important;
     -webkit-text-fill-color:inherit !important;
     text-decoration:none !important; pointer-events:none; cursor:default;">1211</a>
  ```

  Every part earns its place:

  - **`href` is not optional.** An `<a>` with no `href` is not a link, so client
    sanitisers unwrap it and the inline styles go with it, leaving bare text for
    the detector to find.
  - **`color:inherit !important`**, not a hex. Outlook mobile repaints link text
    with its own `!important` blue, which beats a plain inline colour. Inline
    `!important` outranks any author rule and wins — but a hard-coded hex would
    then fight the client's dark-mode transform, so inherit the surrounding
    text's colour instead. That is what "looks like plain text" actually means,
    and it holds in both schemes.
  - **`-webkit-text-fill-color`** too: iOS colours links through it, and it wins
    over `color`.
  - **`pointer-events:none; cursor:default`** keep the dead link untappable.
  - `<style>` rules cannot carry any of this — the Gmail app strips the block.

  Any visible run of four or more digits needs it, not just the obvious ones.
  The address unit number (`MM3205`) counts.

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
