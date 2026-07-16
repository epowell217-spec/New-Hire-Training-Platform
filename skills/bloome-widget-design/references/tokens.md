# `.bw` tokens & re-theming

The injected stylesheet defines a token layer under `.bw`, then builds every component
from those tokens. To restyle a widget you override tokens — you rarely touch component
rules. Source of truth: `apps/server/src/widget-bw.css` (mirrors the PC design system,
`.claude/skills/bloome-design/references/spec.md §5`).

## Token reference (light values; dark auto-derived)

**Color — text**
`--bw-text-1` #000 · `--bw-text-2` 75% · `--bw-text-3` 45% · `--bw-text-4` 30%

**Color — brand & emphasis**
`--bw-blue` #2556B6 · `--bw-orange` #F36440 · `--bw-emphasis` #000 (primary action) ·
`--bw-on-emphasis` #fff

**Color — surfaces & borders**
`--bw-bg` #fff (page) · `--bw-card` #fff · `--bw-muted` #F5F5F5 (section) ·
`--bw-border` 6% · `--bw-border-strong` 12%

**Color — supporting** (charts/badges/illustration only, never body text)
`--bw-support-sky` #ADC8E6 · `--bw-support-ochre` #F49F6A · `--bw-support-amber`
#FFD15C · `--bw-support-olive` #BAC78D · `--bw-support-purple` #7A68BF ·
`--bw-support-grey` #D8D8D8

**Typography** (`--bw-font` = Sora). role = size / weight / line-height / tracking:
- display-lg 48/600/1.1/−1.5 · display-md 40/600 · heading-md 28/600 · heading-sm 24/600
- subhead-md 20/500 · subhead-sm 18/600 (section titles) · body-lg 16/400 · body-md 14/400 (base) · body-sm 12/400
- button-lg 16/500 · button-md 14/500 · button-sm 12/500 · label 11/500/0.2 ·
  caption 12/400/0.2 · `--bw-weight-thin` 200 (split-weight headings)

**Spacing** `--bw-space-` xs4 · sm8 · md12 · lg16 (top-level gap) · xl24 · section32 ·
2xl40 · 3xl48

**Radius** `--bw-radius-` xs6 · sm8 · md12 · lg16 · xl24 · dialog32 · full9999.
Semantic: `--bw-radius-section` 24, `--bw-radius-card` 24.

**Widget layout** `--bw-pad-widget` 40 (root inset) · `--bw-max-width` 860 (content cap;
bg still bleeds full) · `--bw-pad-section` 24

**Shadow / motion** `--bw-shadow-soft` (floating surfaces only) ·
`--bw-dur-fast/base/slow` 120/180/240 · `--bw-ease`

## Dark mode

Automatic. In dark, `--bw-bg` #0F0F0F, `--bw-card` #171717, `--bw-muted` #1D1D1D,
text inverts to white at the same opacities, `--bw-emphasis` flips to white. Fixed-color
islands (stat cards, solid badges) keep pinned text so they stay legible. **Never write
your own dark-mode CSS** — override the light tokens and the dark equivalents derive, or
set `data-bw-theme="light"|"dark"` on the root to pin a mode.

## Re-theming for a user-specified style

When the user asks for a specific look, override tokens on the root. This keeps every
component's structure, spacing, and accessibility intact while changing the skin.

```html
<style>
  .bw {
    --bw-blue: #0d9488;      /* new primary */
    --bw-orange: #7c3aed;    /* new accent */
    --bw-font: 'Inter', sans-serif;
    --bw-radius-section: 12px;
    --bw-radius-card: 12px;
    --bw-muted: #0f172a;     /* darker section fill */
  }
</style>
<body class="bw bw-stack" data-bw-theme="dark"> … </body>
```

- Change **brand** with `--bw-blue` / `--bw-orange`; change **surfaces** with `--bw-bg`
  / `--bw-card` / `--bw-muted`; change **shape** with the radius tokens; change **type**
  with `--bw-font`.
- If you also re-theme charts, pass the matching palette to `ResonChart.configure({...})`
  in the `reson-charts` skill so the two layers agree.
- For a look the tokens can't express (heavy textures, custom illustration, a bespoke
  layout), hand-write CSS for that widget — but keep the hard floor below.

## Legacy base tokens (don't use for new widgets)

The server also injects an older base stylesheet (`widget-base.css`) that defines a
warm/monochrome token set — `--background`, `--foreground`, `--card`, `--primary`,
`--chart-1..5` (with green/red), etc. It stays injected so **existing** widgets that
don't use `.bw` keep working (zero regression). For any **new** widget, use the `.bw`
tokens above and don't mix the two systems — a widget is either `.bw` or legacy, not
half of each.

## Hard floor (holds under any custom style)

1. `ResonWidget` API + surface contract keep working (see `bloome/references/widget.md`).
2. Full-bleed root, no self-frame; content stays within a sane max width.
3. One focal point — never a flat grid of equal-weight tiles.
4. Contrast & readability before decoration; no tiny text on saturated fills.
5. Mobile responsive; no fixed-pixel widths or viewport-scaled body copy.
6. Data charts go through `reson-charts`, not hand-written SVG.
