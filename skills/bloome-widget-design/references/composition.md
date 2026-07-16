# Composing a `.bw` widget

Components are the vocabulary; composition is the sentence. A widget that just stacks
every component top-to-bottom reads as generic. Compose with intent: one focal point,
a clear reading order, and grouping that matches the data.

## Layout primitives

All are plain layout classes — no visual style of their own. Gaps are 16px.

| Class | Effect |
| --- | --- |
| `bw-stack` | Vertical rhythm: 16px between direct children. Put it on the root (`<body class="bw bw-stack">`) to space the top-level blocks. |
| `bw-grid` | Auto-fit grid, min column 160px. Good for a variable number of small tiles. |
| `bw-grid-2` / `-3` / `-4` | Fixed 2 / 3 / 4 equal columns. `-4` is the default stat row. |
| `bw-split` | Asymmetric 1.6fr / 1fr two-column (main + side). |

Responsive collapse is automatic: `-4` → 2-up at ≤720px → 1-up at ≤440px; `-2`/`-3`/
`split` → single column at ≤640px. You never write the media queries.

```html
<body class="bw bw-stack">
  <div>…header…</div>          <!-- block 1 -->
  <div class="bw-grid-4">…</div> <!-- block 2: stat row -->
  <div class="bw-split">         <!-- block 3: main + side -->
    <div class="bw-section">…</div>
    <div class="bw-section">…</div>
  </div>
  <div class="bw-section">…</div> <!-- block 4 -->
  <div class="bw-footer">…</div>  <!-- block 5 -->
</body>
```

## The default reading order

A report/dashboard widget usually reads:

1. **Header** — eyebrow + split-weight title + one-line summary.
2. **Hero** — the single most important thing: one KPI row (`bw-grid-4` stats), or
   one chart (`reson-charts`), or one big number. This is the focal point.
3. **Supporting sections** — `bw-section` cards grouping related detail (ranking bars,
   a table, key-values, a chart). Use `bw-split` when a main + side pairing helps.
4. **One callout** — the single insight/warning worth emphasizing (optional).
5. **Footer** — caption + actions (optional).

Not every widget needs all five. A poll is header + votes + footer. A spec sheet is
header + one KV section. Add blocks because the content needs them, not to fill space.

## One focal point (anti-dashboard rule)

The failure mode this system exists to prevent is the "everything is equally loud"
grid — 9 identical tiles, 4 charts abreast, every section the same weight. Instead:

- Lead with **one** hero. Make exactly one thing the biggest/boldest/most-colored.
- Use `bw-stat--em` on at most one stat; `bw-bar--lead` / `bw-vote--lead` on the top
  item only; one `bw-callout` per widget.
- Orange is a scalpel, not a highlighter — one emphasis per view.
- If you have many charts, they belong in separate widgets or a scrollable report,
  not tiled 3×3. (Charts are the "genuine data" exception to keeping it calm, but the
  one-focal-point rule still applies — lead with the primary chart.)

## Nesting & concentric corners

Outer → inner, corners shrink so they stay concentric:

```
[widget root]  full-bleed bg, no frame, content capped at 860px + centered
  └ [section card]   muted grey, radius 32, padding 24
      └ [card]       stat card / kanban card, radius 24 / 12
```

- Don't wrap the whole widget in a card — the root is already the frame.
- Don't nest a `bw-section` inside a `bw-section`. One level of grouping is enough.
- A `bw-stat` or `bw-card` may sit inside a section; that's the deepest you go.

## Header pattern

```html
<div>
  <span class="bw-eyebrow">Category kicker</span>
  <h1 class="bw-title">Lead word <span class="bw-thin">rest of title</span></h1>
  <p class="bw-summary">One sentence of context.</p>
</div>
```

The split weight (`bw-thin` = 200) on the trailing words is the signature Bloome
editorial move — use it on the title and on `bw-section__title`. Wrap the emphasized
lead word in `<b>` and the remainder in `bw-thin`.

## Embedding a chart

Charts are owned by `reson-charts`, but they live **inside** a `.bw-section` so the
shell stays consistent:

```html
<div class="bw-section">
  <div class="bw-section__head"><span class="bw-section__title"><b>MRR</b> <span class="bw-thin">trend</span></span></div>
  <div id="mrr" style="height:260px"></div>
</div>
<!-- inline echarts + reson-charts.js, then: ResonChart.render('mrr', { type:'line', data:{…} }) -->
```

Don't hand-write SVG/CSS charts inside `.bw` — pick a `reson-charts` `type` instead.

## Density & whitespace

- Section inner padding is 24; top-level gaps are 16. Don't add extra ad-hoc margins
  that fight the tokens.
- Let rows breathe: list/kv/checklist rows already trim their last-child bottom so the
  bottom gap equals the card padding — don't add a trailing divider or margin.
- Prefer fewer, fuller sections over many thin ones.
