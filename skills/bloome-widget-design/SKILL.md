---
name: bloome-widget-design
description: >-
  Design the visual shell and non-chart UI of a Bloome widget with the native
  Bloome component library (the `.bw` system — brand blue + orange, Sora,
  light + dark, auto-injected by the server; you never paste the CSS). Use
  whenever you write or restyle widget HTML/CSS: reports, dashboards, polls,
  forms, kanban, checklists, calendars, tables, stat rows, rankings, callouts,
  menus. Ships ready components (stat card, section card, ranking bar, badge,
  button, form controls, menu, table, key-value, footer, empty state) plus
  composition + token rules so widgets stop looking like generic vibe-coded UI.
  If the user asks for a specific visual style, honor it by overriding the
  tokens. Triggers: make/build a widget, report, poll, dashboard, form, kanban,
  checklist, calendar; style this widget; the widget looks bad/generic; match
  our brand. NOT for the data charts themselves (line/bar/donut/… → reson-charts).
metadata:
  type: reference
  version: '1'
---

# bloome-widget-design — the native Bloome widget component library

This skill governs the **visual shell and non-chart content** of a Bloome widget —
how it **looks**. Its companions: `reson-charts` (data charts, rendered inside a
`.bw-section`) and `bloome/references/widget.md` (how a widget **works** — the
`ResonWidget` runtime API: state, events, CAS, surface types). Read this before
writing or restyling any widget HTML/CSS.

## The `.bw` system in one paragraph

Every Bloome widget is served inside a sandboxed iframe. The server **auto-injects**
a scoped stylesheet (`<style id="reson-widget-bw">`, source of truth:
`apps/server/src/widget-bw.css`) into every widget's `<head>`. It defines a design
token layer plus a full component library, all scoped under a single `.bw` class.
**You do not paste any CSS.** You opt in by putting `class="bw"` on the root
(`<body class="bw">`) and then compose the widget from `bw-*` classes. Values are
copied 1:1 from the PC design system (brand blue `#2556B6` + orange `#F36440`,
Sora, spacing/radius/type scales), so widgets look like the product — with **zero
regression** for legacy widgets that don't set `class="bw"`.

```html
<body class="bw bw-stack">
  <div>
    <span class="bw-eyebrow">Quarterly review</span>
    <h1 class="bw-title">Operations <span class="bw-thin">overview</span></h1>
    <p class="bw-summary">Growth, pipeline and workload at a glance.</p>
  </div>

  <div class="bw-grid-4">
    <div class="bw-stat"><div class="bw-stat__label">New signups</div><div class="bw-stat__value">1,284</div><div class="bw-stat__delta">+18% WoW</div></div>
    <!-- … 3 more … -->
  </div>

  <div class="bw-section">
    <div class="bw-section__head"><span class="bw-section__title"><b>Revenue</b> <span class="bw-thin">by segment</span></span><span class="bw-section__total">$2.4M total</span></div>
    <!-- ranking bars, table, kv, checklist, … -->
  </div>
</body>
```

- Dark mode is automatic (`prefers-color-scheme`; the host bridge may force it via
  `data-bw-theme`). You never write dark-mode CSS.
- Light + dark, contrast, and mobile responsiveness are already handled by the
  tokens and component rules. Don't fight them.

## What lives where

| You need… | Read |
| --- | --- |
| The full markup for every component (stat, section, bar, badge, button, form, menu, table, kv, checklist, calendar, footer, empty…) | [`references/components.md`](./references/components.md) |
| How to arrange components — layout primitives, the header pattern, nesting/corners, the one-focal-point rule, responsive | [`references/composition.md`](./references/composition.md) |
| Token values + how to re-theme for a user-specified custom style | [`references/tokens.md`](./references/tokens.md) |
| A data chart (line, column, donut, waterfall, sankey, KPI…) | the **`reson-charts`** skill — render it inside a `.bw-section` |
| The `ResonWidget` state/event API, surface types, CAS | `bloome/references/widget.md` |

## Default vs user-specified style

- **No style requested → use `.bw` as-is.** Ordinary product words are NOT style
  requests: "make a dashboard", "create a poll", "build a kanban", "show a report",
  "make it interactive" all use the default `.bw` look. Do not ask the user to pick
  a style when the direction isn't genuinely ambiguous.
- **Style requested → honor it by overriding tokens**, not by abandoning the system.
  "make it Apple-like", "cyberpunk", "use our brand teal", "match this screenshot",
  "playful", "dark magazine" are real style requests. Re-theme by overriding the
  `--bw-*` variables on the root (see [`references/tokens.md`](./references/tokens.md)),
  or hand-write CSS for that widget — but the **hard floor below always holds**.

## Hard floor (survives any custom style)

1. **ResonWidget API is untouchable.** State, events, CAS, and the surface contract
   from `bloome/references/widget.md` must keep working regardless of visual style.
2. **Full-bleed, no self-frame.** The widget root paints the background to the iframe
   edge and adds no outer border/card of its own; `.bw` already caps content width
   (`--bw-max-width`, 860px) and centers it. Don't wrap the whole widget in a card.
3. **One focal point — not a dashboard grid.** Lead with a single hero (one number,
   one chart, one list). A 3×3 grid of equal tiles is the generic-vibe-code smell
   this skill exists to kill. Charts count as the "genuine data" exception but still
   keep one focal point.
4. **Accessibility & contrast.** Readable before decorative. Never place small body
   text on a saturated fill without checking contrast; colored `.bw` cards already
   pin their text colors for this reason.
5. **Mobile responsive.** Widgets render narrow (chat card ~380px) and wide (expanded
   window). Use the responsive primitives; never rely on a fixed pixel width or
   viewport-scaled body text.
6. **Blue + orange only** (plus neutrals). Positive/lead = blue, attention/negative =
   orange. The supporting palette (sky/olive/ochre/amber/purple/grey) is for
   charts/badges only. No green/red status colors, no AI gradients, glows, glass,
   bokeh, or multi-accent rainbows unless the user explicitly asked for that style.

## Quality checklist (before shipping)

Beyond the hard floor, these keep a widget from reading as a throwaway prototype:

- **Contrast** — text ≥ 4.5:1 against its background. Never tiny low-contrast text.
- **Mobile** — layout must work at 320px; touch targets ≥ 44×44px; body text ≥ 14px;
  don't rely on hover. The `.bw` primitives collapse responsively for you.
- **Typography** — at most two typefaces (Sora is the default); build hierarchy with
  size contrast, not with many weights/colors.
- **Motion** — optional and sparing: 1–2 transitions, 150–300ms, ease-out. Don't
  animate everything.
- **Copy** — labels concise and actionable ("Vote", not "Click here to vote"). If
  deleting 30% of the text improves it, delete it. No `Lorem ipsum`.
- **No card-in-card-in-card.** One level of grouping (section → card) is the max;
  see the nesting rule in [`references/composition.md`](./references/composition.md).

## Working pattern

1. Pick the surface type from `bloome/references/widget.md` (text vs Preview vs
   Interactive vs App/EdgeSpark). A component-heavy `.bw` layout is usually an
   Artifact or Interactive surface.
2. Write the widget HTML with `<body class="bw">` + `bw-*` components. Do not inline
   the design CSS — it is injected. Only inline chart libs (`reson-charts`) when the
   widget has charts.
3. Wire interaction/state with `ResonWidget` per `widget.md`.
4. Create/update with `widget create/update --html-file` (call the tool yourself; the
   user has no shell).
5. Sanity-check against the hard floor before shipping.
