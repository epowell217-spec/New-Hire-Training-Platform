# Widget / Surface Development Guide

Widgets are Bloome's conversation-native surfaces. A surface is a named, persistent UI embedded in chat: it can preview content, present an artifact, support interaction, or act as the frontend for a mini app.

Current production widgets are HTML surfaces embedded in chat messages. They support shared state, multi-user collaboration, real-time updates, and bidirectional Agent↔Widget events.

## Visual design & charts (owned elsewhere)

This file owns how a widget **works**, not how it **looks**. Do not style widgets
from here.

- **How it looks** — default style, tokens, components, composition, quality:
  read the **`bloome-widget-design`** skill. Put `class="bw"` on the root; the
  component CSS is auto-injected (you don't paste it). `.bw` is the default look.
- **Data charts** (line/bar/donut/…): the **`reson-charts`** skill, rendered
  inside a `.bw-section`.
- If the user asks for a custom visual style, honor it per `bloome-widget-design`
  (override the `--bw-*` tokens) while keeping the ResonWidget API rules in this
  file intact.

## Surface Strategy

Do not make every answer a widget. Use the lightest form that matches the user's job:

| Need                | Surface kind        | Use when                                                                                                                                              |
| ------------------- | ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| One-off answer      | Text, not widget    | The user only needs an explanation, recommendation, summary, translation, or brief answer                                                             |
| Preview             | Preview Surface     | The user asks to view/check/open/preview a file, page, PDF, PPT, HTML, Markdown, image, video, or software demo                                       |
| Structured artifact | Artifact Surface    | The result is a report, comparison matrix, timeline, plan, dashboard snapshot, scorecard, or reference sheet worth revisiting                         |
| Shared interaction  | Interactive Surface | People will vote, fill, collect, track, assign, rank, score, drag, play, or update simple shared state                                                |
| Durable mini app    | App Surface         | The surface needs backend logic, durable data, user identity, ownership, permissions, external APIs, secrets, scheduled work, or long-lived workflows |

Strong signals for creating a widget directly: **vote, form, collect, track, manage, dashboard, kanban, game, compare collaboratively, score, assign, preview, build a tool, make this interactive**.

Weak signals: **explain, summarize briefly, translate, brainstorm, rewrite, recommend**. Use text unless the user asks for a reusable or interactive surface.

When backend behavior is required, build an App Surface. Read `references/edgespark.md`, use the Bloome command `edgespark project create --alias <alias>` to create or bind an EdgeSpark backend project and scaffold `edgespark/<alias>/`, then implement/deploy that backend before creating the widget with `widget create --edgespark <alias>`. You can attach a backend later with `widget update <widgetId> --edgespark <alias>` only when migrating an existing widget. If you are using shell, the project command is `bloome-cli edgespark project create --alias <alias>`. Do not run standalone/raw `edgespark project create`; that is the official EdgeSpark CLI and can ask the human to log in instead of creating the Bloome binding.

Keep the two command surfaces separate: Bloome control-plane commands are `bloome-cli edgespark project create/list/info/verify/delete`; official EdgeSpark CLI commands are raw `edgespark pull`, `edgespark deploy`, and app implementation commands after a Bloome project exists. Create the Bloome binding before any standalone EdgeSpark CLI probing; do not start by running `which edgespark`, `edgespark --help`, or `edgespark --version`. Use the generated `edgespark/<alias>/` directory from project create; do not hand-create an empty `edgespark.toml` or move files out of `server/`. If the project status is `needs_manual_deploy`, execute the returned `nextSteps` yourself before reporting completion; run those deployment commands through `bloome_shell` when available so the temporary `bloome-cli` wrapper is on PATH. The backend metadata and binding exist, but runtime API calls will not work until the EdgeSpark bridge is deployed and `bloome-cli edgespark project verify <alias>` passes. Bloome-created EdgeSpark projects target `production`; run official EdgeSpark CLI commands from `edgespark/<alias>` with `EDGESPARK_PROJECT_ENVIRONMENT=production`, for example `EDGESPARK_PROJECT_ENVIRONMENT=production edgespark pull` and `EDGESPARK_PROJECT_ENVIRONMENT=production edgespark deploy`. Do not run `edgespark pull schema` as readiness proof before verify passes; older CLI versions can resolve that path to `staging`, while current CLI versions reject the `--environment` flag.

For EdgeSpark-backed widget frontend code, read `references/edgespark.md` and choose an access mode before writing routes. Share URLs may open without a Bloome session. Use `ResonWidget.edgespark.fetch('/api/public/...')` as the default for both anonymous-readable data and authenticated actions: the helper tries to attach identity first, but if no Bloome token is available it still sends `/api/public/*` requests anonymously. Do not hardcode the EdgeSpark host URL, and do not call bare `fetch('https://...edgespark.app/...')`; the bridge exchanges the Bloome viewer JWT for a Bloome-backed bearer token via `POST /api/public/_bloome/silent-sign-in`, sending the Bloome JWT only as `Authorization: Bearer <jwt>`, then adds the returned bearer to authenticated business API requests. Bloome-authenticated business routes must live under `/api/public/*` and call `getBloomeUser(c)` from the generated EdgeSpark bridge; keep the generated `server/src/defs/runtime.ts` because the bridge reads Bloome config from EdgeSpark secrets. `/api/*` is reserved for EdgeSpark platform auth and will reject the Bloome bearer. EdgeSpark is the only data source for that backend workflow. Do not also read/write `ResonWidget.state`, define a widget `stateSchema`, or mirror EdgeSpark rows into widget state unless the user explicitly asked for an offline/local fallback and you label it as such.

## State vs EdgeSpark

Choose this before writing code. `ResonWidget.state` is a lightweight
conversation-scoped JSON document. It is not a server replacement.

Use `ResonWidget.state` when all of these are true:

- the data is small, bounded, and naturally fits one JSON document
- conversation visibility is the only access rule
- no server secrets, external APIs, scheduled jobs, or webhooks are needed
- no backend-side queries, pagination, filtering, moderation, rate limiting, or audit trail are needed
- no user ownership rules beyond writing each user to a separate state path

Good state-backed examples: simple polls, counters, checklists, seat claiming,
lightweight game boards, bounded form snapshots, and small trackers where all
viewers see the same state.

Use EdgeSpark when any of these are true:

- the feature needs Bloome identity, author attribution, "my/all" views,
  delete/edit-own rules, likes by user, member-only data, or other permissions
- the data is a durable collection: comments, message boards, tasks, records,
  feeds, submissions, orders, logs, or anything that needs list CRUD
- the backend must validate requests, call external services, store secrets,
  run scheduled jobs, receive webhooks, apply rate limits, or expose custom routes
- the user asks for a real backend, database, persistent app, or serious
  workflow instead of a toy/shared-state widget

Default to EdgeSpark for message boards, comments, guestbooks, submissions,
feeds, and task/record lists. These are durable collections even when the
initial request sounds short. Use `ResonWidget.state` for those only when the
user explicitly asks for a simple/local/temporary state-only widget or says no
backend is needed. A purely anonymous, tiny scratchpad can use
`ResonWidget.state`, but state collections must be object maps keyed by stable
IDs and parent paths must exist before JSON Patch `add` operations.

If `edgespark project create`, `widget create --edgespark`, or `widget update
--edgespark` returns `EDGESPARK_DISABLED`, do not retry raw EdgeSpark CLI
commands or bypass Bloome. Use `ResonWidget.state` only for simple widgets; for
backend-required workflows, tell the user EdgeSpark backend support is
temporarily unavailable.

## Checklist

Before writing widget code, review these rules:

- [ ] **Right surface** — Confirm this should be Preview / Artifact / Interactive / App, not a one-off text answer
- [ ] **Backend choice** — Use `ResonWidget.state` only for small bounded shared JSON; use EdgeSpark for identity, ownership, durable collections, list CRUD, permissions, external APIs, secrets, or serious backend logic
- [ ] **Full HTML** — Write complete `<!DOCTYPE html>` with your own importmap, styles, scripts
- [ ] **Mobile-first** — Widgets are viewed on phones just as often as desktops. Use responsive layout, touch-friendly tap targets (min 44px), and test at 320px width. Avoid hover-only interactions
- [ ] **Single source of truth** — For state-backed widgets, use `ResonWidget.state` only; for verified EdgeSpark widgets, use EdgeSpark only
- [ ] **Per-user paths** — Different users write to different state paths (`votes.{userId}`, `todos.{uuid}`)
- [ ] **CAS for contention** — When paths must overlap (seat claiming, game moves), use `{ expect }`
- [ ] **Community libraries** — Import via esm.sh, don't hand-write charts/drag-drop/rich-text
- [ ] **Default design** — Read the `bloome-widget-design` skill; if the user did not specify a style, use the `.bw` default (`class="bw"` + `bw-*` components; CSS is auto-injected)
- [ ] **Visual thesis** — Decide one-sentence design direction before coding; for default widgets, keep it inside the `.bw` system
- [ ] **stateSchema** — Declare `--state-schema` only for widgets that persist data in `ResonWidget.state`
- [ ] **Backend binding** — If this is an App Surface, create/reuse an EdgeSpark alias first and pass `--edgespark <alias>` on `widget create`
- [ ] **Access mode** — For EdgeSpark App Surfaces, choose public read/authenticated mutation, authenticated read/write, anonymous read/write, or public static read/authenticated actions before writing routes
- [ ] **Single backend source** — If EdgeSpark is verified, use `ResonWidget.edgespark.fetch()` only; no `ResonWidget.state` mirror/fallback in the same code path

## Minimal Working Template

The design CSS is auto-injected, so a default widget is just `<body class="bw">` plus
`bw-*` components (full component set: the `bloome-widget-design` skill). Load the Sora
+ Phosphor webfonts, opt in with `class="bw"`, and wire state with `ResonWidget`. The
template below shows correct ResonWidget API usage — swap the content for your task:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Sora:wght@200;400;500;600&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.1/src/regular/style.css" />
  </head>
  <body class="bw bw-stack">
    <div>
      <span class="bw-eyebrow">Widget title</span>
      <h1 class="bw-title">Useful, not <span class="bw-thin">noisy</span>.</h1>
    </div>
    <div class="bw-section">
      <div id="rows"></div>
      <div class="bw-footer">
        <span class="bw-footer__cap">Shared across everyone in the chat</span>
        <span class="bw-footer__actions"><button id="increment" class="bw-btn" type="button">Add item</button></span>
      </div>
    </div>
    <script>
      const widgetState = window.ResonWidget?.state;
      const fallbackState = { count: 0 };
      const getState = () => (widgetState ? widgetState.get() || fallbackState : fallbackState);
      function setCount(next) {
        if (widgetState) widgetState.set("count", next);
        else { fallbackState.count = next; render(fallbackState); }
      }
      function render(state) {
        const count = state.count || 0;
        document.getElementById("rows").innerHTML = `
          <div class="bw-row">
            <span class="bw-row__idx">1</span>
            <div><div class="bw-row__title">Shared count</div><div class="bw-row__copy">Replace this row with task-specific content.</div></div>
            <span class="bw-badge bw-badge--dark">${count}</span>
          </div>`;
      }
      document.getElementById("increment").addEventListener("click", () => setCount((getState().count || 0) + 1));
      if (widgetState) widgetState.on("change", (state) => render(state || {}));
      render(getState());
    </script>
  </body>
</html>
```

## Architecture: Widget vs Instance

- **Widget** = code template (HTML, title, stateSchema) — `widgetId`
- **Instance** = runtime state copy — `instanceId`

First instance shares ID with widget (`instanceId = widgetId`). Forwarding can create new instances (independent state, same code).

## Editing Workflow (file-first — required)

Widget HTML is non-trivial code that lives in two places: your local working copy and the DB. To prevent drift, **always treat a local file as the source of truth and push it to DB**, never construct HTML inline as a CLI argument.

**Why:** building HTML directly inside `--html "..."` (or even `--html -` via stdin) means the "current code" only exists in your chat history. Next turn, next session, or after a tool error, you'll lose it and end up regenerating something subtly different. With a file on disk, both you and the user can re-read, diff, and resume.

**Convention:** keep working copies in `widgets/<descriptive-name>.html` under your CWD (e.g. `widgets/dashboard.html`, `widgets/voting.html`). Pick the name when you create the widget; reuse it for every update.

### Create

1. `Write` complete HTML to `widgets/<name>.html`
2. `bloome-cli widget create --title "..." --html-file widgets/<name>.html`
3. Note the returned `widgetId` — the local file remains your working copy for future updates

### Update

1. **Local file still present** → `Edit widgets/<name>.html` directly
2. **Local file lost** (new session, agent restart, switched cwd) → fetch it back first:

   ```bash
   widget read <widgetId> --html-only > widgets/<name>.html
   ```

   Then `Edit` the restored file.

3. Push: `bloome-cli widget update <widgetId> --html-file widgets/<name>.html`

### Don't

- ❌ `--html "<html>...</html>"` for anything beyond a one-line throwaway (escape hell, no working copy)
- ❌ `cat <<EOF | widget update ... --html -` (no working copy survives the call)
- ❌ Edit local file but skip `widget update` (DB stays stale, users see old version)
- ❌ Skip `widget read` when the local file is missing — that guarantees drift

The same file-first discipline applies to `--state-schema-file` (schemas with descriptions also have escape pain) and to `doc create` / `doc write` (use `--content-file`, paired with `doc read`).

## Commands

| Command                                                            | Description                                              |
| ------------------------------------------------------------------ | -------------------------------------------------------- |
| `widget create --title "T" --html-file widgets/<name>.html`        | **Preferred** — create from a local file                 |
| `widget create ... --edgespark <alias>`                            | Bind this widget to an existing EdgeSpark backend alias  |
| `widget create ... --state-schema-file widgets/<name>.schema.json` | With state schema from file                              |
| `widget create --title "T" --html "<html>..."`                     | Inline form (only for trivial one-liners)                |
| `widget read <widgetId>`                                           | Read metadata + full HTML (JSON)                         |
| `widget read <widgetId> --html-only > widgets/<name>.html`         | **Restore local working copy from DB**                   |
| `widget update <widgetId> --html-file widgets/<name>.html`         | **Preferred** — push local file to DB                    |
| `widget update <widgetId> --edgespark <alias>`                     | Attach an existing EdgeSpark backend alias               |
| `widget update <widgetId> --clear-edgespark`                       | Disable this widget's EdgeSpark runtime binding          |
| `widget update <widgetId> --html "..."`                            | Inline form (only for trivial one-liners)                |
| `widget send <widgetId>`                                           | Re-send to conversation                                  |
| `widget send <widgetId> --new`                                     | Send as new instance                                     |
| `widget info <widgetId>`                                           | Metadata-only (title, description, stateSchema, version) |
| `widget state-get <instanceId>`                                    | Read full state                                          |
| `widget state-get <instanceId> --path count`                       | Read dot-path                                            |
| `widget state-set <instanceId> --data '{"count":1}'`               | Shallow merge                                            |
| `widget state-set <instanceId> --path count --value 1`             | Dot-path set                                             |
| `widget state-set <instanceId> --patches '[...]'`                  | JSON Patch                                               |
| `widget upload <widgetId> --file <path> --name <name>`             | Upload asset                                             |
| `widget share <instanceId> --level public`                         | Make public                                              |
| `widget forward <instanceId> --to <convId> [--new]`                | Forward                                                  |
| `widget listen <instanceId> --event move`                          | Subscribe event                                          |
| `widget listen <instanceId> --state board`                         | Subscribe state path                                     |
| `widget unlisten <instanceId> --all`                               | Remove subscriptions                                     |
| `widget listeners <instanceId>`                                    | List subscriptions                                       |
| `widget emit <instanceId> --event greet --data '{}'`               | Send event to widget                                     |

## ResonWidget JavaScript API

Available via `window.ResonWidget` (alias: `window.AgentWidget`):

```javascript
ResonWidget.id       // instanceId
ResonWidget.version  // number

// User identity
const user = await ResonWidget.getUser();
// → { id, displayName, name, avatarUrl, type } | null

// State — read
ResonWidget.state.get()              // full copy
ResonWidget.state.get('count')       // dot-path
ResonWidget.state.get('board.0.1')   // deep path

// State — write
ResonWidget.state.set('count', 5)                      // dot-path
ResonWidget.state.set({ count: 5, name: 'hi' })        // shallow merge
ResonWidget.state.set('count', 5, { expect: 4 })       // CAS → Promise<boolean>

// State — subscribe
const unsub = ResonWidget.state.on('change', (snapshot, changes) => {
  // changes: [{ path, value, source: 'agent'|'user', user }]
});

// Events — emit to Agent
ResonWidget.emit('move', { x: 3, y: 5 });

// Events — listen from Agent
ResonWidget.on('greet', (data) => { ... });

// Assets
ResonWidget.asset('logo.png')  // → /api/uploads/widgets/{widgetId}/logo.png

// EdgeSpark backend binding — only present on widgets created/updated with --edgespark <alias>
await ResonWidget.edgespark.fetch('/api/public/items'); // tries identity, anonymous-falls-back for public path
await ResonWidget.edgespark.fetch('/api/public/items', { method: 'POST' }); // backend decides if identity is required
await ResonWidget.edgespark.getToken(); // Bloome-backed EdgeSpark API token, not Bloome JWT
```

Deleting an EdgeSpark project alias is not the same as clearing a widget
binding. `edgespark project delete <alias>` removes this Agent's management
binding and local API key secret only; widgets that already have
`metadata.edgespark` keep using the persisted `projectId/baseUrl`. Use `widget
update <widgetId> --clear-edgespark` when the task is to stop a widget from
receiving `ResonWidget.edgespark` at runtime.

## State Rules

Use this section only after deciding `ResonWidget.state` is the right backend
model. For identity-aware or durable app data, use EdgeSpark instead.

### CAS (Compare-And-Set)

For concurrent writes to the same path:

```javascript
const ok = await ResonWidget.state.set('seats.A1', myUserId, { expect: null });
if (!ok) alert('Seat already taken!');
```

Async — server checks `expect` matches current value. Returns `false` on 409 conflict.

### Echo Elimination

`set()` applies locally immediately (optimistic). Server broadcast of the same change is auto-suppressed via sessionId. **Rule**: In state-backed widgets, use `ResonWidget.state` as the single source of truth — don't maintain a separate `useState` for shared data.

### Multi-User State Design

Widgets in group chats have multiple users writing state simultaneously. Design state to avoid overwrites:

**Rule: Different users must write to different paths.**

```javascript
// ❌ Multiple users +1 concurrently — last write wins, earlier ones lost
state.set('voteCount', currentCount + 1);

// ✅ Each user writes to their own key — never conflicts
state.set(`votes.${user.id}`, 'optionA');
// Widget tallies votes itself: Object.values(state.votes).filter(v => v === 'optionA').length
```

```javascript
// ❌ Multiple users push to array concurrently — one side lost
state.set('todos', [...todos, newItem]);

// ✅ Use unique ID as key
state.set(`todos.${crypto.randomUUID()}`, { text, by: user.id, at: Date.now() });
```

**Pattern summary:**

| Scenario         | State structure                           | Why safe                  |
| ---------------- | ----------------------------------------- | ------------------------- |
| Voting           | `votes.{userId}: choice`                  | Each user writes own key  |
| Todo list        | `todos.{uuid}: {text, by}`                | Each item has unique path |
| Form submissions | `submissions.{userId}: data`              | Per-user namespace        |
| Seat claiming    | `seats.A1: userId` + CAS `{expect: null}` | Atomic check-and-set      |
| Game moves       | `board.{x}.{y}: playerId` + CAS           | One cell, one write       |

## Agent ↔ Widget Events

**Widget → Agent:**

```bash
# Subscribe first
widget listen <instanceId> --event move --event surrender
```

```javascript
// Widget emits
ResonWidget.emit('move', { x: 3, y: 5 });
// → Agent receives trigger
```

**Agent → Widget:**

```bash
widget emit <instanceId> --event update_board --data '{"board":[[1,0],[0,2]]}'
```

```javascript
ResonWidget.on('update_board', (data) => renderBoard(data.board));
```

**State path subscriptions:**

```bash
widget listen <instanceId> --state board --state score
# → Agent triggered when board or score changes
```

## Sharing & Forwarding

```bash
widget share <instanceId> --level public           # Anyone with link
widget forward <instanceId> --to <convId>          # Shared state
widget forward <instanceId> --to <convId> --new    # Independent state
```

Public widgets accessible at `/w/<instanceId>`. Add `?embed=true` to hide nav.

## Static Assets

```bash
widget upload <widgetId> --file ./logo.png --name logo.png
```

```javascript
const img = document.createElement('img');
img.src = ResonWidget.asset('logo.png');
```

---

## Design quality & tokens

Visual quality, the default `.bw` style, the full token set, and the component
library are all owned by the **`bloome-widget-design`** skill — read it before
writing any HTML/CSS. Data charts → the **`reson-charts`** skill. Do not restyle
from this file.

Runtime constraint (not design): `localStorage`, `sessionStorage`, and
`document.cookie` are blocked by the iframe sandbox — use `ResonWidget.state`
(state-backed) or `ResonWidget.edgespark.fetch()` (EdgeSpark-backed) instead.

## Recommended Tech Stack

Choose based on widget type — the platform has no framework preference:

| Scenario                         | Recommended                          | Why                                   |
| -------------------------------- | ------------------------------------ | ------------------------------------- |
| Data display, forms, kanban      | React 19 + HTM + Tailwind via esm.sh | Best for composition-based UI         |
| Games, animations, visualization | Canvas / Pixi.js / Three.js          | Direct pixel control, no DOM overhead |
| Simple interactions              | Vanilla HTML/CSS/JS                  | Minimal, no dependencies              |

**Prefer community libraries over hand-written code.** Import any npm package via `https://esm.sh/<package>`. Less code = fewer bugs:

| Need               | Use                                          | Not                          |
| ------------------ | -------------------------------------------- | ---------------------------- |
| Research / analytical charts | **`reson-charts` skill** — 25 native-Bloome types (waterfall, mekko, football-field, tornado, CAGR, sensitivity, bullet, treemap…), brand palette + dark mode + auto chart-selection, one `ResonChart.render(el,{type,data})` call | hand-writing chart config |
| Other charts       | `chart.js`, `recharts`, `lightweight-charts` | Hand-drawn SVG/Canvas        |
| Kanban / drag-drop | `@hello-pangea/dnd`, `sortablejs`            | Custom pointer event logic   |
| Rich text          | `tiptap`, `quill`                            | contentEditable from scratch |
| Date picker        | `date-fns` + a picker lib                    | Manual calendar grid         |
| Markdown           | `marked`, `markdown-it`                      | Regex parsing                |
| Animations         | `animejs`, `gsap`                            | Complex keyframe chains      |
| 3D / WebGL         | `three`, `pixi.js`                           | Raw WebGL shaders            |
| Confetti / effects | `canvas-confetti`, `tsparticles`             | DIY particle system          |

```javascript
// esm.sh usage — import directly, no npm install needed
import Chart from 'https://esm.sh/chart.js/auto';
import confetti from 'https://esm.sh/canvas-confetti';
import { marked } from 'https://esm.sh/marked';
import sortable from 'https://esm.sh/sortablejs';
```

---

## React + HTM Gotchas (avoid white screens)

When using `htm.bind(React.createElement)`, the children look like HTML but the prop layer is **React semantics**. Mixing the two breaks rendering.

| ❌ Wrong (HTML style)                       | ✅ Right (React/HTM)                              | Why                                                                                                               |
| ------------------------------------------- | ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `style="width: ${pct}%"`                    | `style=${{ width: `${pct}%` }}`                   | React requires `style` to be an object, not a string. **Passing a string throws React error #62 → white screen.** |
| `class="${selected ? 'a' : 'b'}"`           | `className=${selected ? 'a' : 'b'}`               | React uses `className`. `class` works in plain HTML and many JSX-like libs but logs a warning in React.           |
| `<!-- HTML comment -->` inside `html\`\`\`` | drop the comment, or use `${/* JS comment */ ''}` | htm doesn't strip HTML comments; they may end up as text children.                                                |
| `onclick=${fn}` / `onchange=${fn}`          | `onClick=${fn}` / `onChange=${fn}`                | React event names are camelCase.                                                                                  |

**Object props in htm need `${{...}}`** (the outer `${}` is the interpolation, the inner `{}` is the object literal). Same for inline event handlers, refs, etc.

### Dynamic inline style — the right way

When you need a dynamic CSS value (progress bar width, transform, computed color), build a JS object and pass it via `style=${{...}}`:

```js
// Progress bar with dynamic width
return html`
  <div class="relative h-2 bg-gray-200 rounded">
    <div
      class="absolute inset-y-0 left-0 bg-black rounded transition-all"
      style=${{ width: `${percent}%` }}
    />
  </div>
`;

// Multiple dynamic properties
const barStyle = {
  width: `${percent}%`,
  opacity: isSelected ? 1 : 0.3,
  transform: `translateX(${offset}px)`,
};
return html`<div style=${barStyle} />`;
```

If everything you need can be done with Tailwind utility classes (`w-1/2`, `opacity-50`, etc.), prefer that — fewer chances to slip back into HTML-string thinking.

---

## Complete Examples

### Voting Widget (React 19 + HTM + Tailwind)

```html
<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <script type="importmap">
      {
        "imports": {
          "react": "https://esm.sh/react@19",
          "react-dom/client": "https://esm.sh/react-dom@19/client",
          "htm": "https://esm.sh/htm@3"
        }
      }
    </script>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600&display=swap');
      body {
        margin: 0;
        font-family: 'Sora', sans-serif;
        background: #f5f5f5;
        color: #111827;
      }
      @media (prefers-color-scheme: dark) {
        body {
          background: #111318;
          color: #e5e7eb;
        }
      }
    </style>
  </head>
  <body>
    <div id="root"></div>
    <script type="module">
      import React, { useState, useEffect } from 'react';
      import { createRoot } from 'react-dom/client';
      import htm from 'htm';
      const html = htm.bind(React.createElement);

      const OPTIONS = ['Option A', 'Option B', 'Option C'];

      function App() {
        const [state, setState] = useState({});
        const [user, setUser] = useState(null);

        useEffect(() => {
          ResonWidget.getUser().then(setUser);
          setState(ResonWidget.state.get() || {});
          return ResonWidget.state.on('change', (s) => setState(s));
        }, []);

        const votes = state.votes || {};
        const totals = OPTIONS.map((_, i) => Object.values(votes).filter((v) => v === i).length);
        const total = Object.keys(votes).length;
        const myVote = user ? votes[user.id] : undefined;

        function vote(i) {
          if (!user) return;
          ResonWidget.state.set('votes.' + user.id, i);
        }

        return html`
          <div class="p-4 sm:p-6 max-w-md mx-auto">
            <h2 class="text-lg font-semibold mb-4">${state.title || 'Vote'}</h2>
            ${OPTIONS.map(
              (opt, i) => html`
                <button
                  key=${i}
                  onClick=${() => vote(i)}
                  class="w-full mb-2 min-h-[44px] px-4 py-3 rounded-lg text-left flex justify-between items-center transition-colors active:scale-[0.98]
                ${myVote === i
                    ? 'bg-black text-white dark:bg-white dark:text-black'
                    : 'bg-white dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700'}"
                >
                  <span>${opt}</span>
                  <span class="text-sm opacity-60"
                    >${total > 0 ? Math.round((totals[i] / total) * 100) + '%' : ''}</span
                  >
                </button>
              `,
            )}
            <p class="text-sm text-gray-500 mt-3">${total} vote${total !== 1 ? 's' : ''}</p>
          </div>
        `;
      }
      createRoot(document.getElementById('root')).render(html`<${App} />`);
    </script>
  </body>
</html>
```

### Board Game with CAS (Vanilla JS)

```html
<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600&display=swap');
      * {
        box-sizing: border-box;
        margin: 0;
      }
      body {
        font-family: 'Sora', sans-serif;
        background: #f5f5f5;
        color: #111827;
        padding: 16px;
      }
      @media (prefers-color-scheme: dark) {
        body {
          background: #111318;
          color: #e5e7eb;
        }
      }
      h2 {
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 12px;
      }
      .board {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 4px;
        max-width: 240px;
      }
      .cell {
        aspect-ratio: 1;
        min-height: 44px;
        border-radius: 8px;
        font-size: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        background: white;
        border: 1px solid rgba(0, 0, 0, 0.06);
        transition: background 0.15s ease-out;
        -webkit-tap-highlight-color: transparent;
      }
      .cell:hover {
        background: #f3f4f6;
      }
      .cell:active {
        background: #e5e7eb;
      }
      @media (prefers-color-scheme: dark) {
        .cell {
          background: #1a1c24;
          border-color: rgba(255, 255, 255, 0.055);
        }
        .cell:hover {
          background: #1f2128;
        }
        .cell:active {
          background: #262830;
        }
      }
      .status {
        margin-top: 12px;
        font-size: 14px;
        color: #6b7280;
      }
    </style>
  </head>
  <body>
    <h2>Tic-Tac-Toe</h2>
    <div class="board" id="board"></div>
    <p class="status" id="status"></p>
    <script>
      const MARKS = { 0: '✕', 1: '○' };
      let user = null;

      ResonWidget.getUser().then((u) => {
        user = u;
        render();
      });

      ResonWidget.state.on('change', () => render());

      function render() {
        const state = ResonWidget.state.get() || {};
        const board = state.board || {};
        const players = state.players || {};
        const turn = state.turn || 0;

        const boardEl = document.getElementById('board');
        boardEl.innerHTML = '';
        for (let r = 0; r < 3; r++) {
          for (let c = 0; c < 3; c++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            const val = board[`${r}.${c}`];
            cell.textContent = val != null ? MARKS[val] : '';
            cell.onclick = () => makeMove(r, c);
            boardEl.appendChild(cell);
          }
        }

        const playerCount = Object.keys(players).length;
        const statusEl = document.getElementById('status');
        if (playerCount < 2) statusEl.textContent = `Waiting for players (${playerCount}/2)...`;
        else statusEl.textContent = `Turn: ${MARKS[turn]}`;
      }

      async function makeMove(r, c) {
        if (!user) return;
        const state = ResonWidget.state.get() || {};
        const players = state.players || {};

        // Claim seat (CAS)
        if (!players[user.id] && Object.keys(players).length < 2) {
          const mark = Object.keys(players).length;
          await ResonWidget.state.set(`players.${user.id}`, mark, { expect: undefined });
        }

        const myMark = (ResonWidget.state.get('players') || {})[user.id];
        if (myMark == null || myMark !== (state.turn || 0)) return;

        // Place move (CAS)
        const ok = await ResonWidget.state.set(`board.${r}.${c}`, myMark, { expect: undefined });
        if (ok) ResonWidget.state.set('turn', myMark === 0 ? 1 : 0);
      }

      render();
    </script>
  </body>
</html>
```
