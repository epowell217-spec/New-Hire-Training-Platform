# Bloome Widget Design — contract

**The full design system is the `bloome-widget-design` skill** — read
`skills/bloome-widget-design/SKILL.md` (and its `references/`) for the `.bw` shell,
components, composition, tokens, and quality before writing or restyling any widget
HTML/CSS. Data charts go to the **`reson-charts`** skill, rendered inside a
`.bw-section`. This page is only the non-negotiable contract.

## How widget styling works

The server **auto-injects** the Bloome component stylesheet (scoped under `.bw`) into
every widget. You do **not** paste design CSS. Opt in by putting `class="bw"` on the
root (`<body class="bw">`) and compose from `bw-*` components (stat card, section,
ranking bar, badge, button, form controls, menu, table, key-value, checklist,
calendar, footer, empty state). Light/dark, contrast, and responsiveness are handled
by the tokens. Full markup for every component is in the `bloome-widget-design` skill.

## Default vs custom style

- **No style requested → use `.bw` as-is.** Ordinary product words ("make a
  dashboard", "create a poll", "build a kanban", "show a report", "make it
  interactive") are NOT style requests — use the default look. Don't ask the user to
  pick a style unless direction is genuinely ambiguous.
- **Style requested** ("Apple-like", "cyberpunk", "use our brand teal", "match this
  screenshot", "playful", "dark magazine") → honor it by **overriding the `--bw-*`
  tokens** (see the skill's `references/tokens.md`) or hand-writing CSS for that
  widget — the hard floor below still holds.

## Hard floor (any style)

1. **ResonWidget API untouchable** — state/events/CAS/surface contract from
   `widget.md` must keep working.
2. **Full-bleed, no self-frame** — the root paints to the iframe edge; `.bw` already
   caps and centers content. Don't wrap the whole widget in a card.
3. **One focal point** — lead with a single hero (one number / chart / list). No flat
   grid of equal-weight tiles — that is the generic-vibe-code look to avoid.
4. **Accessibility & contrast** — readable before decorative; no small text on
   saturated fills without a contrast check.
5. **Mobile responsive** — renders narrow (~380px) to wide; use the responsive
   primitives, never fixed pixel widths or viewport-scaled body text.
6. **Blue + orange only** (plus neutrals). Positive/lead = blue, attention = orange;
   supporting palette for charts/badges only. No AI gradients, glows, glass, bokeh,
   or multi-accent rainbows unless the user asked for that style.
7. **Data charts → `reson-charts` skill**, rendered inside a `.bw-section`. Do not
   hand-write SVG/CSS charts.

## Working pattern

1. Choose the surface type per `widget.md`.
2. Write the widget with `<body class="bw">` + `bw-*` components (design CSS is
   injected — don't inline it). Inline `reson-charts` only when the widget has charts.
3. Wire state/interaction with `ResonWidget`.
4. Create/update with `widget create/update --html-file` (call the tool yourself).
5. Check against the hard floor before shipping.
