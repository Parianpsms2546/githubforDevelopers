# empeo email shell — locked values

The header, footer, typography and vertical rhythm below are fixed. Reuse them for
every new template and only change what sits between the greeting and the CTA.

`src/empeo-account-inactive.html` is the reference implementation. Start from it,
swap the content rows, and leave everything else alone.
`src/empeo-account-deletion-grayfooter.html` is the same shell with a CTA, and
`src/empeo-payslip-grayfooter.html` adds the content components — an icon-plus-label
block and an info box — on top of that.

## Type

Font stack — one canonical string, used in every cell and in the preheader:

```
'Prompt','Noto Sans Thai',Tahoma,Helvetica,Arial,sans-serif
```

The order is the point. Tahoma carries Thai glyphs, Helvetica carries none; put
Helvetica first and Thai falls through to whatever the OS picks. `'Noto Sans Thai'`
sits behind Prompt so the fallback is the email's choice, not the OS's — quote it,
it is a multi-word family name. The webfont `<link>` loads **Prompt only**: Noto
matters only when Prompt is unavailable, and a client that cannot load one webfont
will not load the other.

Outlook desktop ignores the webfont entirely and lands on Tahoma.

| Element | Size | Weight | Line height | Colour |
|---|---|---|---|---|
| Greeting label ("เรียน ", "สวัสดี ") | 18px | 500 | 24px | `#000000` |
| Greeting name | 18px | 700 | 24px | `#000000` |
| Body copy | 16px | 500 | 24px | `#1C1C22` |
| CTA label | 16px | 600 | 30px | `#FFFFFF` |
| Footer address / help line / Help Center link | 10px | 400 | 16px | `#525260` |
| Info-box label / body (payslip) | 14px | 600 / 400 | 22px | `#1C1C22` / `#525260` |

Flame (buttons, accents): `#F15A2E`. Footer band: `#F5F6F7`. Card: `#FFFFFF`.
Corner radius: **8px**, buttons and cards alike.

`.body-mobile` in the media query carries its own `line-height` — change it with the
inline value or the mobile view snaps back.

### Body copy at 24px is knowingly tight

Measured with real Prompt (Thai subset, weight 500, 16px) against the live body
lines. `headroom` is the gap between the top of the line box and the top of the ink;
negative means Outlook desktop, where `mso-line-height-rule:exactly` applies, can
shave the top of a tone mark. Browsers and webmail let the overflow pass invisibly.

| Line | ink ascent | lh 24 | lh 26 | lh 30 |
|---|---|---|---|---|
| `ขณะนี้ …` (inactive) | 17.35px | **−0.35** | +0.65 | +2.65 |
| `ปิดใช้งาน …` (inactive) | 14.00px | +3.00 | +4.00 | +6.00 |
| `ความผิดพลาด …` (inactive) | 13.00px | +4.00 | +5.00 | +7.00 |
| `คำขอการลบบัญชี …` (deletion) | 16.71px | +0.29 | +1.29 | +3.29 |
| `อย่างถาวรเรียบร้อยแล้ว …` (deletion) | 17.35px | **−0.35** | +0.65 | +2.65 |

The cost is always a *stacked* vowel-plus-tone — `นี้`, `ที่` — never a plain
consonant. **26px is the tightest value that clears every line measured.** 24px is
kept because it is the approved look; if a tone mark ever looks cut in Outlook
desktop, 26px is the one-line fix (inline value **and** `.body-mobile`).

Greeting at 18px/700 clears comfortably at 24px (+3). The CTA label at 16px/600
clears at 30px (+7) — keep the button on 30px rather than retuning it to the body
value, and see the CTA box below for how the height follows from it.

Per-template components, measured in Prompt and all clearing their current values:

| Component | Metric | Headroom |
|---|---|---|
| Payroll period label, 16px/600 | lh 24px | +3.00 |
| Payroll period date, 16px/700 — worst of the twelve months is `กุมภาพันธ์` | lh 24px | +3.00 |
| File-password note, 14px/600 and 14px/400 | lh 22px | +3.50 |

The period block is 24px rather than a guard value because its content is
**enumerable** — a fixed label and a date — so it can be measured instead of
defended. Measure the whole domain, not the string in front of you: December alone
would understate what February needs. Free-form copy keeps the shell value.

## Vertical rhythm

| Gap | Value | Where it lives |
|---|---|---|
| Top of card → logo | **0** | header band `padding:0` |
| Logo → greeting | **16px** | body band `padding-top:16px` |
| Greeting → body copy | **8px** | spacer row, `height="8"` |
| Last content row → CTA button | **48px** | `padding-top:48px` on the CTA cell |
| CTA button → footer | **80px** | body band `padding-bottom:80px` |
| Footer top / bottom | **24px** | footer band `padding:24px 0` |

Both sides of the button are padding, never a spacer row on one side and padding on
the other — clients size the two differently and the gaps drift apart.

On a template with no CTA the 80px runs from the last line of copy to the footer.

The logo's optical gap is larger than 16px on purpose: the asset carries ~17.5px of
transparent margin below its artwork, so 16px of box spacing reads as ~36px. Put
logo spacing in the asset, never in the HTML.

## The CTA box

```
padding: 7px 24px      /* 44px tall with the 30px line box */
line-height: 30px      /* the Thai clearance value */
border-radius: 8px
background: #F15A2E
```

Height is **44px** = 7 + 30 + 7, and the VML fallback carries `height:44px` so Outlook
draws the same button as everyone else. **The two are edited together, always** — a
padding change that leaves the VML behind ships two different buttons.

The vertical padding is deliberately not 24px. Padding is the CSS value, not the
optical gap: the line box is 30px while the label's ink is only 13px tall (`ดาวน์โหลด`
and `ติดต่อเรา` both measure 13px, no descender), so the 30px box already contributes
~17px of its own breathing room. Squaring the padding at 24px was tried and reverted —
it took the button to 78px, which read as oversized.

## Layout and width

- Bands are full-bleed: white body and grey footer run edge to edge. No rounded
  corners on the shell.
- Horizontal padding is **24px, front and back, at every width**. `.px-24` stays on
  the three band cells as the hook, currently a no-op in the media query.
- Body copy is centred — a left-aligned paragraph reads as off-centre between a
  centred greeting and a centred button.

Width is the one thing that must not be left to the client:

```html
<table ... class="email-container" style="width:100%; min-width:600px; max-width:100%;">
<table ... class="inner"           style="width:100%; min-width:100%; max-width:100%;">
```

```css
@media only screen and (max-width: 600px) {
  .email-container { width: 100% !important; min-width: 0 !important; margin: 0 auto !important; }
}
```

Every width in this shell is a percentage, and a percentage needs a parent with a
definite width. Outlook always has one — the Word engine's page width, plus the
`[if mso]` ghost table wrapping the container. Gmail has neither: it drops
`<html>`/`<head>`/`<body>`, which takes `html, body { width: 100% }` with them, and
it never sees the `mso` block. With no anchor left, the tables fall back to
`width:auto` and shrink-wrap to their content — `align="center"` then centres the
collapsed table, which is what a narrow Gmail render looks like. Measured: the whole
email collapsed to **176px** in a container with no definite width, grey footer band
included.

`min-width:600px` is the floor that survives that. Clients with a definite width
still fill their pane; the media query releases the floor on a viewport that really
is narrow, so mobile never scrolls sideways.

| Container | without the floor | with it |
|---|---|---|
| no definite width (Gmail-like) | 176px | 600px |
| 1000px pane | 1000px | 1000px |
| 375px viewport | 375px | 375px |

Outlook desktop ignores `min-width`, which is harmless — the ghost table already
holds it open.

## Footer structure

The footer is **one table**, not three. The logo/icons row shares its columns with
the address rows via `colspan="3"`, so a client that shrink-wraps still gives that
row the footer's real width and the social icons stay on the right edge. Both end
columns carry an explicit `width`, and the 8px between the icons is padding — a
`font-size:0` spacer has no min-content to defend itself with and collapses.

## Assets

`build-eml.py` resolves every `cid:` against `assets/<cid>.png`, so a template's
image is named by its `cid`.

**Never reference SVG from an email.** Gmail strips `<img>` pointing at `.svg` and
Outlook desktop's Word engine cannot render it — the icon becomes an empty box.
Vector sources live in `assets/` for regeneration only:

| cid | asset | source | display |
|---|---|---|---|
| `empeo-logo` | `empeo-logo.png` | — | 128×64 |
| `powered-by-empeo` | `powered-by-empeo.png` | — | 60×18 |
| `icon-facebook` | `icon-facebook.png` | `facebook.svg` | 14×14 |
| `icon-youtube` | `icon-youtube.png` | `bi_youtube.svg` | 14×14 |
| `empeo-e-payslip` | `empeo-e-payslip.png` | `empeo-e-payslip-chip.svg` | 36×42 |

Social icons are rasterised at **168px** (12× their 14px display size, matching the
density of the assets they replaced) on a transparent canvas, keeping the source
SVG's `#1C1C22`. The payslip icon is rasterised at **144px** (4× its 36px box),
keeping the source SVG's `#F05B2F`.

### The payslip icon's peach chip

`empeo-e-payslip.svg` is the artwork as delivered — the glyph alone, 24px of ink in a
36px box. The chip behind it lives in `empeo-e-payslip-chip.svg`, and that is what the
PNG is rasterised from. Same rule as the logo's margin: **the padding is in the asset,
never in the HTML**, so the markup only ever says 36×36.

Chip values, the fill and radius measured off the 80px asset it replaced so it reads
as before:

| | value | how it was measured |
|---|---|---|
| Fill | `#FDEDE8` | most common opaque colour in the old PNG |
| Corner radius | **7.2px** — 20% of the 36px width | opacity on row 0 starts 16px into an 80px asset |
| Box | **36×42** | see below |
| Glyph | **32px** — the 36px canvas scaled to 32 and centred | — |

**The chip is 36×42, not square.** The artwork is 23.73×29.81 inside its 36px canvas,
so a square chip left 6.19px of peach at the sides but only 3.09px above and below.
Growing the box to 42px and re-centring evens that out. Exact equality wants 42.1875px;
42 keeps the box on whole pixels for a quarter-pixel difference.

**The glyph then scaled from 36 to 32 inside that unchanged chip**, which lifts the
peach to 7.5px at the sides and 7.75px above and below — measured off the raster, not
computed. `translate(2,5) scale(32/36)` in the chip SVG is the whole of it; the box, the
`<img>` and every gap around the block stay where they were.

`<img>` carries `width="36" height="42"` to match, and the block is `valign="middle"`,
so the taller chip still centres against the two lines beside it.

The old asset sat its glyph at 47.5% of its box. Keeping the new glyph at native scale
fills the chip more, which is the approved look — do not shrink it back.

## Dark mode

`.card-bg` `#1F2228` · `.footer-bg` `#191B20` · `.text-charcoal` `#FFFFFF` ·
`.text-iron` `#C7CBD1` · `.text-muted` `#9AA0A8` · page `#16181D`.
`.info-bg` `#262A31` — the payslip's info box adds this pair to the shell.

Footer copy and the info box's secondary line are both `#525260` in light mode and
stay on their dark overrides — `#9AA0A8` and `#C7CBD1` — because `#525260` on
`#191B20` or `#262A31` is unreadable. Outlook mobile rewrites colours for its own
dark mode and tags what it touched with `data-ogsb` / `data-ogsc`; the CTA is pinned
back to Flame with white text there, or `#F15A2E` darkens to a muddy red.

## Building

```bash
cd email-templates
python3 build-eml.py <template-name> "<Subject line>"
```

Reads `src/<name>.html`, resolves the `cid:` references against `assets/`, writes
`<name>.eml` as `multipart/related` with `X-Unsent: 1` so it opens as an editable
draft in Outlook. Edit `src/`, never the `.eml`.
