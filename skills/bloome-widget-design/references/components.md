# `.bw` component catalog

Every component below is defined by the auto-injected stylesheet (source of truth:
`apps/server/src/widget-bw.css`). You only write the markup — the CSS is already
there once the root has `class="bw"`. All values (type/spacing/radius/color) come
from tokens; see [`tokens.md`](./tokens.md) if you need to re-theme.

Icons: components that show an icon use [Phosphor](https://phosphoricons.com/)
(`i.ph`/`i.ph-fill` via the web font, or inline SVG with `fill="currentColor"`).
Load the Phosphor web font in the widget `<head>` if you use `<i>` icons.

---

## Header

Lead-in for the whole widget. `bw-thin` renders the split-weight (200) counterpart
for "**Bold** <thin>rest</thin>" headings.

```html
<div>
  <span class="bw-eyebrow">Quarterly review</span>
  <h1 class="bw-title">Operations <span class="bw-thin">overview</span></h1>
  <p class="bw-summary">Growth, pipeline and workload at a glance.</p>
</div>
```

- `bw-eyebrow` — body-md, uppercase, tracked, text-tertiary. Optional kicker.
- `bw-title` — display-lg (48/600). 24px below the eyebrow.
- `bw-summary` — body-lg, text-secondary. 8px below the title. Optional.

---

## Stat card

Fixed-color "island" for a headline metric. Default fill is soft-sky; `bw-stat--em`
makes it orange for the one metric that needs emphasis. Text colors are pinned
(they do NOT flip in dark) so they stay legible on the colored fill.

```html
<div class="bw-grid-4">
  <div class="bw-stat"><div class="bw-stat__label">New signups</div><div class="bw-stat__value">1,284</div><div class="bw-stat__delta">+18% WoW</div></div>
  <div class="bw-stat"><div class="bw-stat__label">Activated</div><div class="bw-stat__value">61%</div><div class="bw-stat__delta">+4 pts</div></div>
  <div class="bw-stat"><div class="bw-stat__label">Retention</div><div class="bw-stat__value">88%</div><div class="bw-stat__delta">+2 pts</div></div>
  <div class="bw-stat bw-stat--em"><div class="bw-stat__label">CAC</div><div class="bw-stat__value">$7.40</div><div class="bw-stat__delta">−$1.10</div></div>
</div>
```

- `__label` 16 text-tertiary · `__value` 32/600 · `__delta` 16/500. Radius 24.
- Put stat cards in a `bw-grid-4` (default) / `-3` / `-2`; they collapse responsively.
- Use `bw-stat--em` on **at most one** card — the focal metric.

---

## Section card

The large grouping container (muted grey, radius 32, padding 24). Its head has an
optional icon, a split-weight title, and an optional right-aligned total; a strong
divider separates head from body.

```html
<div class="bw-section">
  <div class="bw-section__head">
    <span class="bw-section__title"><b>Revenue</b> <span class="bw-thin">by segment</span></span>
    <span class="bw-section__total">$2.4M total</span>
  </div>
  <!-- body: bars / table / kv / checklist / chart … -->
</div>
```

- `__title` is subhead-sm (18/600), no icon; wrap the lead word in `<b>` and the rest
  in `bw-thin` for the split weight. `__total` is body-md, uppercase, text-tertiary.
- Nesting: a section (radius 32) may contain cards (radius 24). Don't nest a section
  inside a section.

---

## Ranking bar

Ordered list with a proportional bar. The leader gets `bw-bar--lead` (orange fill);
the rest are blue. Index badge is grey with pinned dark text.

```html
<div class="bw-bar bw-bar--lead"><span class="bw-bar__idx">01</span><span class="bw-bar__name">Enterprise</span><div class="bw-bar__track"><div class="bw-bar__fill" style="width:100%"></div></div><span class="bw-bar__value">$1.18M</span></div>
<div class="bw-bar"><span class="bw-bar__idx">02</span><span class="bw-bar__name">Mid-market</span><div class="bw-bar__track"><div class="bw-bar__fill" style="width:64%"></div></div><span class="bw-bar__value">$760K</span></div>
<div class="bw-bar"><span class="bw-bar__idx">03</span><span class="bw-bar__name">SMB</span><div class="bw-bar__track"><div class="bw-bar__fill" style="width:38%"></div></div><span class="bw-bar__value">$450K</span></div>
```

- Set the fill width inline as a percentage (relative to the max).
- Use `bw-bar--lead` on the top item only.

---

## Vote / progress bar

Taller track (40px) for polls/allocations. Name + value on one row, bar below,
optional caption. Leader = `bw-vote--lead` (orange).

```html
<div class="bw-vote bw-vote--lead">
  <div class="bw-vote__row"><span class="bw-vote__name">Option A</span><span class="bw-vote__value">62%</span></div>
  <div class="bw-vote__track"><div class="bw-vote__fill" style="width:62%"></div></div>
  <div class="bw-vote__cap">124 votes</div>
</div>
<div class="bw-vote">
  <div class="bw-vote__row"><span class="bw-vote__name">Option B</span><span class="bw-vote__value">38%</span></div>
  <div class="bw-vote__track"><div class="bw-vote__fill" style="width:38%"></div></div>
  <div class="bw-vote__cap">76 votes</div>
</div>
```

---

## List row

Ranked/numbered rows with a title, optional copy, and a trailing control (usually a
secondary button). Index is a solid black circle. Last row trims its bottom padding.

```html
<div class="bw-row">
  <span class="bw-row__idx">1</span>
  <div><div class="bw-row__title">Northwind renewal</div><div class="bw-row__copy">Contract up for renewal in 12 days.</div></div>
  <button class="bw-btn bw-btn--secondary bw-btn--sm">Open</button>
</div>
```

---

## Table

Flat table: uppercase label-size headers, tabular-nums numeric column, row dividers,
last row borderless. Right-align the last column (usually the number).

```html
<table class="bw-table">
  <thead><tr><th>Company</th><th>Plan</th><th>Status</th><th>MRR</th></tr></thead>
  <tbody>
    <tr><td>Northwind</td><td><span class="bw-badge bw-badge--gold">Enterprise</span></td><td><span class="bw-badge bw-badge--grey">Active</span></td><td class="bw-table__num">$12,400</td></tr>
    <tr><td>Acme Corp</td><td><span class="bw-badge bw-badge--gold">Enterprise</span></td><td><span class="bw-badge bw-badge--orange">At risk</span></td><td class="bw-table__num">$9,800</td></tr>
  </tbody>
</table>
```

- `bw-table__num` on numeric cells for tabular alignment.

---

## Key-value list

Label→value rows (spec sheet, order summary). Last row trims its bottom padding.

```html
<div class="bw-kv__row"><span class="bw-kv__key">Plan</span><span class="bw-kv__value">Enterprise</span></div>
<div class="bw-kv__row"><span class="bw-kv__key">Seats</span><span class="bw-kv__value">45</span></div>
<div class="bw-kv__row"><span class="bw-kv__key">Renews</span><span class="bw-kv__value">Jun 30, 2026</span></div>
```

---

## Badge

One size only: height 24, padding 0 8, label type (11/500/0.2px), full pill. Solid
fills with pinned black text (the dark variant inverts). Four variants:

```html
<span class="bw-badge bw-badge--gold">Enterprise</span>   <!-- amber #FFD15C -->
<span class="bw-badge bw-badge--grey">Active</span>       <!-- grey  #D8D8D8 -->
<span class="bw-badge bw-badge--orange">At risk</span>    <!-- orange #F36440 -->
<span class="bw-badge bw-badge--dark">New</span>          <!-- emphasis (black/white) -->
```

---

## Button

Variant (primary default / `--secondary`) × size (`--lg` / default md / `--sm`),
always a full pill. Primary = black emphasis; secondary = subtle grey fill.

```html
<button class="bw-btn">Share review</button>
<button class="bw-btn bw-btn--secondary">Export</button>
<button class="bw-btn bw-btn--lg">Primary large</button>
<button class="bw-btn bw-btn--secondary bw-btn--sm">Small secondary</button>
<button class="bw-btn" disabled>Disabled</button>
```

- Default height 40 (md, button-md). `--lg` = 48/button-lg. `--sm` = 32/button-sm.

---

## Callout

Single emphasis block: an orange accent bar + title + body on a muted card. Use for
the one insight/warning worth surfacing — not as a repeated card.

```html
<div class="bw-callout">
  <span class="bw-callout__bar"></span>
  <div>
    <div class="bw-callout__title">Paid social CAC doubled</div>
    <div class="bw-callout__body">$14.20 vs $7.10 last week while volume fell. Worth pausing the underperforming set.</div>
  </div>
</div>
```

---

## Kanban

Columns are muted cards; task cards are white with radius 12 and no shadow. WIP
columns use `bw-col--wip` (orange count + orange tag). Cards may carry an orange
accent bar (`bw-card__accent`) which tightens the left padding automatically.

```html
<div class="bw-grid-3">
  <div class="bw-col">
    <div class="bw-col__head"><span class="bw-col__name">To do</span><span class="bw-col__count">4</span></div>
    <div class="bw-card">
      <div class="bw-card__body">
        <div class="bw-card__title">Draft Q3 pricing</div>
        <div class="bw-card__meta"><span class="bw-card__tag">Pricing</span><span class="bw-avatar">AL</span></div>
      </div>
    </div>
  </div>
  <div class="bw-col bw-col--wip">
    <div class="bw-col__head"><span class="bw-col__name">In progress</span><span class="bw-col__count">2</span></div>
    <div class="bw-card">
      <span class="bw-card__accent"></span>
      <div class="bw-card__body">
        <div class="bw-card__title">Migrate billing</div>
        <div class="bw-card__meta"><span class="bw-card__tag">Backend</span><span class="bw-avatar">MK</span></div>
      </div>
    </div>
  </div>
  <div class="bw-col"><div class="bw-col__head"><span class="bw-col__name">Done</span><span class="bw-col__count">7</span></div></div>
</div>
```

- `bw-avatar` = 20px sky circle with initials.

---

## Form controls

Label is small uppercase text-tertiary. Inputs/selects/textareas are **transparent**
— only the border defines the field (radius 12, border-strong). Focus shows the
caret only (no ring). The select caret is a Phosphor chevron that flips color in dark.

```html
<div class="bw-field">
  <label class="bw-label">Full name</label>
  <input class="bw-input" placeholder="Jane Cooper" />
</div>
<div class="bw-field">
  <label class="bw-label">Plan</label>
  <select class="bw-select"><option>Starter</option><option>Pro</option><option>Enterprise</option></select>
</div>
<div class="bw-field">
  <label class="bw-label">Notes</label>
  <textarea class="bw-textarea" placeholder="Add context…"></textarea>
</div>
```

- Input/textarea text is body-md (14); label is body-sm (12). Input height 48.
- The native `<select>` popup can't be styled — for a custom dropdown use `bw-menu`.

### Checkbox / radio / toggle

```html
<span class="bw-check is-on"><i class="ph ph-check"></i></span>   <!-- square check, blue when on -->
<span class="bw-check bw-check--round is-on"></span>             <!-- circular check -->
<span class="bw-radio is-on"></span>
<span class="bw-toggle is-on"></span>
```

---

## Menu

Floating popover for context menus, custom dropdowns, and pickers (surface-card,
radius 16, soft shadow, 4px between items). Items are 40px tall; states are hover
(3%), `--selected` (6%), `--disabled`, `--danger`. Optional leading `<i>` icon (20px)
and trailing `bw-menu__check`.

```html
<div class="bw-menu">
  <div class="bw-menu__item"><span><i class="ph ph-pencil-simple"></i> Rename</span></div>
  <div class="bw-menu__item bw-menu__item--selected"><span><i class="ph ph-copy"></i> Duplicate</span><i class="ph ph-check bw-menu__check"></i></div>
  <div class="bw-menu__divider"></div>
  <div class="bw-menu__item bw-menu__item--danger"><span><i class="ph ph-trash"></i> Delete</span></div>
</div>
```

---

## Checklist

Round check (blue circle when done, grey circle when not), body-md label, done rows
get text-secondary + strikethrough. Rows are 48px; the last row trims its lower half.

```html
<div class="bw-check-row is-done"><i class="ph-fill ph-check-circle" style="font-size:20px;color:var(--bw-blue)"></i><span class="bw-check-row__label">Kickoff call</span></div>
<div class="bw-check-row"><i class="ph ph-circle" style="font-size:20px;color:var(--bw-text-4)"></i><span class="bw-check-row__label">Send proposal</span></div>
```

---

## Calendar

Bordered square-corner grid (Monday-first), day-of-week header, today = full-cell
blue square. Out-of-month days use `--mute`.

```html
<div class="bw-cal__dows">
  <span class="bw-cal__dow">Mo</span><span class="bw-cal__dow">Tu</span><span class="bw-cal__dow">We</span><span class="bw-cal__dow">Th</span><span class="bw-cal__dow">Fr</span><span class="bw-cal__dow">Sa</span><span class="bw-cal__dow">Su</span>
</div>
<div class="bw-cal__grid">
  <span class="bw-cal__day bw-cal__day--mute">30</span>
  <span class="bw-cal__day">1</span>
  <span class="bw-cal__day bw-cal__day--today">2</span>
  <!-- … -->
</div>
```

---

## Footer action bar

Top-bordered row: a caption on the left, actions on the right (secondary + primary).

```html
<div class="bw-footer">
  <span class="bw-footer__cap">Last updated · Jun 18</span>
  <span class="bw-footer__actions">
    <button class="bw-btn bw-btn--secondary">Export</button>
    <button class="bw-btn">Share review</button>
  </span>
</div>
```

---

## Empty state

Centered Phosphor icon (40, text-quaternary) + title + body + one primary action.

```html
<div class="bw-empty">
  <i class="ph ph-tray bw-empty__icon" style="font-size:40px"></i>
  <div class="bw-empty__title">No submissions yet</div>
  <div class="bw-empty__body">Share this form to start collecting responses.</div>
  <button class="bw-btn">Copy link</button>
</div>
```
