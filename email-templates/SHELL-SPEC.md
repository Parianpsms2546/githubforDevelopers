# empeo email shell — locked values

The header, footer, typography and vertical rhythm below are fixed. Reuse them for
every new template and only change what sits between the greeting and the CTA.

`src/empeo-account-inactive.html` is the reference implementation. Start from it,
swap the content rows, and leave everything else alone.
`src/empeo-account-deletion-grayfooter.html` is the same shell with a CTA. On top of
that, `src/empeo-payslip-grayfooter.html` adds an icon-plus-label block and an info
box, `src/empeo-password-reset.html` adds the OTP row,
`src/empeo-document-rejected.html` adds the detail card,
`src/empeo-interview-appointment.html` adds the appointment card, and
`src/empeo-welcome-onboarding.html` adds the credentials card with its numbered steps.
The interview card's own internal spacing is deliberately its own — see the rhythm
section.

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
| OTP digit (password reset) | 20px | 700 | 44px | `#F15A2E` on `#FDEDE8` |
| Reference line (password reset) | 12px | 400 | 18px | `#525260` |
| Inline link in body copy | 16px | 500 | 24px | `#F15A2E` |
| Emphasis inside body copy | 16px | 600 | 24px | inherits |
| Detail-card title (document) | 16px | 600 | 30px | `#1C1C22` |
| Detail-card label / value | 14px | 400 / 600 | 22px | `#525260` / `#1C1C22` |
| Status badge (document) | 12px | 500 | 16px | `#FFFFFF` on `#8A8F98` |
| Appointment day number | 36px | 700 | 44px | `#1C1C22` |
| Appointment month / time | 16px | 500 / 600 | 24px | `#1C1C22` / `#F15A2E` |
| Appointment mode heading | 16px | 600 | 24px | `#1C1C22` |
| Appointment label / value | 14px | 400 / 500 | 22px | `#525260` / `#1C1C22` |
| Credentials label / value (welcome) | 14px | 500 / 700 | 22px | `#FFFFFF` |
| Steps divider label (welcome) | 16px | 400 | 30px | `#1C1C22` |
| Step heading (welcome) | 16px | 600 | 30px | `#1C1C22` |
| Step description (welcome) | 16px | 400 | 24px | `#1C1C22` |
| Step number badge (welcome) | 11px | 700 | 20px | `#FFFFFF` on `#F15A2E` |
| Outlined button label (welcome) | 14px | 600 | 22px | `#1C1C22` |

Flame (buttons, accents): `#F15A2E`. Footer band: `#F5F6F7`. Card: `#FFFFFF`.
Corner radius: **8px**, buttons and cards alike.

`.body-mobile` in the media query carries its own `line-height` — change it with the
inline value or the mobile view snaps back.

**A colour change is two edits: the inline value and the class.** `.text-muted` and
`.text-iron` carry their own dark-mode overrides (`#9AA0A8`, `#C7CBD1`), so a line
recoloured to `#1C1C22` while still classed muted stays grey in dark mode while every
other charcoal line turns white. Recolour to charcoal, reclass to `text-charcoal`.

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
| Payroll period label, 16px/500 | lh 24px | +4.00 |
| Payroll period date, 16px/500 — worst of the twelve months is `กุมภาพันธ์` | lh 24px | +4.00 |
| File-password note, 14px/600 and 14px/400 | lh 22px | +3.50 |
| Reference line, 12px/400 | lh 18px | +3.00 |
| OTP digit, 20px/700 — Latin numerals, no Thai marks | lh 44px | +15.00 |
| Detail-card title, 16px/600 | lh 30px | +7.00 |
| Detail-card label 14px/400, value 14px/600 | lh 22px | +3.50 |
| Status badge, 12px/500 | lh 16px | +3.00 |
| Appointment day `25`, 36px/700 | lh 44px | +10.00 |
| Appointment month 16px/500, time 16px/600 | lh 24px | +5.00 / +6.00 |
| Appointment mode, 16px/600 | lh 24px | +4.00 |
| Appointment place 14px/500, note 14px/500 | lh 22px | +3.50 / +1.19 |
| Steps divider label, 16px/400 | lh 30px | +4.38 |
| Step headings, 16px/600 — worst is `ติดตั้ง empeo บนมือถือ` | lh 30px | +3.19 |
| Step descriptions, 16px/400 — worst is the `ที่ https://…` line | lh 24px | +0.68 |
| Step number badge, 11px/700 | lh 20px | +6.50 |
| Credentials label, 14px/500 | lh 22px | +1.19 |

The step descriptions went 13px/20px → **16px/24px**. At 16px the old 20px line box
would have cut them, and even 22px sits at −0.32px on the `ที่ https://…` line, so 24px
is the value that works — the same number the shell already uses for 16px copy.

Document-rejected is the one template whose body copy is safe at 24px: `เอกสารของคุณ
ถูกปฏิเสธ` has no stacked vowel-plus-tone, so it clears by +5px at the top and +2px
below — the descenders in `ถูก` and `ปฏิ` are what make the bottom the tighter side
there.

Password reset is the template most exposed to the 24px body value: all four of its
Thai lines — the body copy and the three closing lines — carry a stacked
vowel-plus-tone (`นี้`, `ที่นี่`, `ตั้ง`, `ต้อง`) and every one measures 17.35px of ink,
so each sits at **−0.35px** in a 24px line box. They were 30px and 28px before the
shell was applied. Same trade as the other templates: fine everywhere except Outlook
desktop, where 26px is the fix.

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

Document-rejected's detail card:

| Gap | Value | Where it lives |
|---|---|---|
| Body copy → card | **36px** | spacer row |
| Card padding | **16px 20px** | on the card's single cell |
| Title row → first detail row | **10px** | spacer row inside the card |
| Detail row → detail row | **8px** | spacer row, `colspan="2"` |
| Card → CTA button | **48px** | `padding-top:48px` on the CTA cell |

The 8px spacer carries `colspan="2"` so it cannot introduce a third column and nudge
the label column's width.

### The steps divider label

```html
<td width="49%">…rule…</td>
<td width="2%" align="center" style="width:2%; white-space:nowrap; text-align:center; padding:0 12px;">เริ่มใช้งานได้ใน 3 ขั้นตอน</td>
<td width="49%">…rule…</td>
```

Two things were wrong here, and they compounded.

**The columns were over-constrained.** The rules declared 50% each, the label declared
nothing — so the percentages claimed the entire row before the label was counted, and the
client had to invent a distribution. Chromium floors the label at its content and shrinks
the rules; Gmail handed the label the slack instead, which left the rules short with a gap
either side. Declaring all three so they total 100 — **49 / 2 / 49** — removes the guess.
`white-space:nowrap` still floors the label at its text width, so the 2% is only a hint
about where slack should *not* go: measured at 375 / 700 / 1100px panes the label cell is
203px every time (179px of ink + 24px padding) and the two rules stay equal.

**The label was left-aligned in its cell.** While the cell was oversized that read as
off-centre even though the cell itself was centred. `align="center"` plus
`text-align:center`: with the cell forced to 326px against 179px of text, the ink lands 0px
from the cell's centre, against 62px off left-aligned.

**Any cell whose width the client decides needs both its width and its alignment
declared** — never rely on a cell hugging its content, and never leave a row's percentages
adding up to more than 100.

### Pin the label column, do not let the client size it

Both cards run label / value as a two-column table. `white-space:nowrap` on the label
plus `width:100%` on the value is enough for Outlook and for every browser — the label
shrinks to its text — but **Gmail sizes those columns its own way and hands the label
roughly half the card**, which pushes the values far right and wraps them early. It is
not reproducible in Chromium: the same markup gives a 96px label column there.

So the label column carries an explicit width, as an attribute and inline, and no
distribution algorithm gets a choice:

| Card | Longest label | Prompt | Tahoma | Column |
|---|---|---|---|---|
| Interview | `ข้อมูลเพิ่มเติม:` | 84.1px | 86.0px | **100px** |
| Document | `รายละเอียด:` | 69.9px | 74.1px | **88px** |

Measured at 14px/400. Tahoma is what Outlook desktop falls back to, so it is the width
that has to fit, and the 12px `padding-right` lives inside the same box — 86 + 12 = 98,
so 100 leaves 2px of slack. Verified constant at 1100 / 675 / 375px panes.

**Re-measure if a label's text changes.** These are fixed strings today; a longer one
would wrap inside a column that no longer fits it.

The two cards also differ in the weight of their values: the document card runs them at
**600**, the appointment card at **500** with only its mode heading at 600. Both are
deliberate — do not align one to the other.

Interview-appointment's card, kept as it arrived rather than aligned to the document
card:

| Gap | Value | Where it lives |
|---|---|---|
| Body copy → card | **36px** | spacer row |
| Card padding | **24px 20px** | on the card's single cell |
| Date block → mode heading | **32px** | spacer row inside the card |
| Mode heading → first detail row | **12px** | spacer row inside the card |
| Detail row → detail row | **6px** | `padding-top` on the second row's two cells |
| Card → closing line | **24px** | spacer row |

Welcome-onboarding's blocks:

| Gap | Value | Where it lives |
|---|---|---|
| Body copy → credentials card | **36px** | spacer row |
| Credentials card padding | **20px 24px** | on the card's single cell |
| Between the two credential rows | **16px** | spacer row, `colspan="7"` |
| Credentials card → steps divider | **48px** | spacer row |
| Divider → first step | **24px** | spacer row |
| Step heading → description | **4px** | spacer row |
| Description → store buttons | **14px** | spacer row |
| Between steps | **20px + 1px rule + 20px** | three rows |
| Last step → footer | **80px** | body band `padding-bottom:80px` |

**The step number shares a row with its heading.** The badge used to sit in a
`valign="top"` column beside the whole text block, which left it floating above the first
line in Outlook — a 20px badge against a 30px line box has 10px to drift in, and Outlook
spends it differently from everyone else. Now the badge cell and the heading cell are one
row, both `valign="middle"`, so the number is tied to the line it belongs to; the
description and buttons sit in a second row indented by the same 20 + 12px. Verified: the
badge's centre and the heading's centre land within 0px in all three steps.

The badge itself is a 20x20 cell with `border-radius:10px` and an 11px digit on a 20px
line box, which centres it without a second table. The two app-store buttons are
**116px wide each**, fixed, with the padding vertical only — horizontal padding would
fight the width, so the inner table centres itself instead.

Password reset's own block, between the body copy and the closing lines:

| Gap | Value | Where it lives |
|---|---|---|
| Body copy → OTP row | **48px** | spacer row |
| OTP row → reference line | **12px** | spacer row |
| Reference line → closing lines | **48px** | spacer row |

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

**Reach 44px through the 30px line box, not through padding.** The interview template
arrived at the same 44px with `padding:11px 24px; line-height:22px`, and that label —
`คลิกเพื่อดูแผนที่`, with `พื่` and `ที่` stacked — measures 17.45px of ink, so a 22px
line box cut it by **1.45px** in Outlook desktop. Same height, same look everywhere
else, clipped only there. On the shell's 30px it clears by +2.55px.

The vertical padding is deliberately not 24px. Padding is the CSS value, not the
optical gap: the line box is 30px while the label's ink is only 13px tall (`ดาวน์โหลด`
and `ติดต่อเรา` both measure 13px, no descender), so the 30px box already contributes
~17px of its own breathing room. Squaring the padding at 24px was tried and reverted —
it took the button to 78px, which read as oversized.

## The detail card

```
background: #FFFFFF          /* white on white — the 1px border is the whole edge */
border: 1px solid #E6E8EB
border-radius: 8px
border-collapse: separate !important; border-spacing: 0
```

`border-collapse:separate` is load-bearing for the same reason as the OTP chips: the
shell's reset collapses every table, and a collapsed table drops **both** its
`border-radius` and its 1px border, leaving the card invisible.

The status badge is `#FFFFFF` on `#8A8F98` with a 10px radius and `padding:3px 12px`,
plus `white-space:nowrap` on the badge cell and its parent so a long title can never
break the word. `#8A8F98` is the one place the old muted grey survives — it is a chip
fill behind white text, not body copy, so it did not move to `#525260` with the rest.

## The credentials card

```html
<td bgcolor="#F15A2E" class="cred-cell"
    style="background-color:#F15A2E; border-radius:8px; padding:20px 24px;">
```

**Flat Flame, by decision — the gradient was dropped, not lost.** It was tried three ways
and this is what the outcome was worth:

| Path | Result |
|---|---|
| `background` attribute → `cid:` PNG | nothing, in any Outlook |
| CSS `linear-gradient` | works in Gmail / Apple Mail, stripped by the webview-based Outlook |
| VML `v:roundrect` + `v:fill type="gradient"` | only reaches a Word-engine Outlook, and the client this is checked in is not one |

The new Outlook for Windows and Outlook on the web render with a browser engine: they skip
`[if mso]` entirely, so VML never applies, and their sanitiser drops `background-image`, so
the CSS gradient never applies either. The card landed on `#F15A2E` in that client no matter
which trick was in the file. A gradient behind live text needs a Word engine, a CSS
gradient, or a downloadable image — with two of the three unavailable there, flat is the
honest answer.

What flat bought back: **one table for every client** instead of an `[if mso]` VML branch
and an `[if !mso]` branch carrying duplicate copies of the same two rows, no fixed VML
height to keep in sync with the content, and no hosted asset to keep pinned. `bg-credentials.png`
is deleted.

Do not re-add a gradient here without checking which Outlook the review happens in.

The card stays a fixed **386px** wide (`width:100%; max-width:386px`).

The VML namespaces stay on `<html>` regardless — the CTA buttons still need them:

```html
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:v="urn:schemas-microsoft-com:vml"
      xmlns:o="urn:schemas-microsoft-com:office:office" …>
```

Four templates shipped VML buttons declaring `xmlns:v` inline on the `v:roundrect` — the
fragile form — with nothing on `<html>`, and the document's own `xmlns` pointed at
`https://www.w3.org/1999/xhtml`, which is not the XHTML namespace. Both are fixed in all
seven.

## The OTP row

Six `<td>`s of `width:40px; height:44px` on `#FDEDE8` with `border-radius:8px`, and
8px spacer cells between them.

Two things are load-bearing. The wrapping table needs
`border-collapse:separate !important; border-spacing:0` — the shell's reset collapses
every table, and **a collapsed cell drops its `border-radius`**, so the chips render as
plain squares. And the 8px gaps are spacer cells with an explicit `width`, not padding
on the digit cells, so each digit stays centred in its own chip.

The chip fill is the same `#FDEDE8` as the payslip icon's chip.

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
| `icon-apple` / `icon-android` | matching PNGs | `apple.svg` / `LogoAndroid.svg` | 18×18 |
| `icon-user-white` / `icon-lock-white` | matching PNGs | — | 16×16 |
| `afs-logo` | `afs-logo.png` | `AFS_Logo.svg` | 128×64 |
| `rs-logo` | `rs-logo.png` | `RS_Logo` (WebP) | 128×64 |

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

## Brand logos and brand variants

A brand variant is **a separate template that differs in the header alone** — the `cid`,
the `alt`, the link. `src/interview-appointment-afs.html` is
`src/empeo-interview-appointment.html` with those three changed and nothing else; the grey
`powered-by-empeo` footer stays, because that is the point of it.

The header markup never changes shape: a **128×64** box, `align="center"`,
`margin:0 auto`, `height:auto` in the style so the attribute drives it.

**Put the spacing in the asset, not the HTML.** The gap to the greeting is 16px of box
spacing plus whatever transparent margin the artwork carries, and that margin is most of
what the eye reads:

| Logo | Ink | Margin top / bottom | Optical gap to greeting |
|---|---|---|---|
| `empeo-logo` | 117×29 | ~17.5px | ~36px |
| `afs-logo` | 71.6×48 | 8px | ~24px |
| `rs-logo` | 64×64 | 0px | 16px |

**RS fills the box outright**, by request: 64px of ink, diamond touching top and bottom,
no vertical margin in the asset at all. The gap to the greeting is then the 16px of box
spacing alone — less than half what the empeo logo reads — which is what a full-bleed logo
costs. Both exceptions are one number in the rasterising step.

**AFS is a deliberate exception to the 29px ink height.** Its artwork is a filled flag at
1.492:1 that fills its own canvas, and at 29px it read as too small, so it is scaled to
48px of ink inside the same 128×64 frame — bigger logo, less optical gap. One number in
the rasterising step changes it back.

**Check what a delivered brand asset actually contains before using it.** `RS` arrived as
two files: `RS.png`, 900×900 with **no alpha channel at all** — its two most common colours
are `#E7E6E6` and `#FFFFFF`, i.e. the transparency checkerboard is painted into the file,
and it is light blue — and `RS_Logo`, a WebP at 567×567 with a real transparent background
and navy `#003A6F` ink. The WebP is the one that ships. WebP itself is no use in email
(Outlook cannot read it), but it rasterises to PNG like anything else.

**`AFS_Logo.svg` ships with no `viewBox`**, and its content sits behind a
`translate(-61.85,-339.23)`, so CSS sizing crops it instead of scaling it — the first
raster came out with 0.5px of visible ink. Measured from rendered pixels the artwork fills
its declared box exactly, so inject `viewBox="0 0 576.29785 386.26526"` before scaling.
Expect the next brand logo to arrive the same way: **render it once and measure the ink
from the pixels** rather than trusting `getBBox`, which reports the group's local
coordinates and sent that first attempt off-canvas.

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
