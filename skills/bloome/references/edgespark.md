# EdgeSpark App Surface Guide

Use this reference before creating, deploying, or debugging an EdgeSpark-backed Bloome widget.

## Required Flow

1. Create or reuse the Bloome binding first. This is a Bloome control-plane
   command, not the official EdgeSpark CLI. It also creates the local
   `edgespark/<alias>/` project scaffold:

   ```bash
   bloome-cli edgespark project create --alias <alias>
   ```

   If you have a Bloome tool instead of shell, pass only the command body:
   `edgespark project create --alias <alias>`. Do not run standalone/raw
   `edgespark project create`; that is the official EdgeSpark CLI and may ask
   the human to log in instead of creating the Bloome binding.

2. Use the generated `edgespark/<alias>/` directory. Do not hand-create a
   parallel EdgeSpark project, do not replace it with an empty `edgespark.toml`,
   and do not move files out of the generated `server/` directory.

3. Install the official EdgeSpark agent skills and CLI if `nextSteps` asks for them:

   ```bash
   npx skills add edgesparkhq/agent-skills --yes
   npm install -g @edgespark/cli@latest
   ```

4. After installing the official skills, read both installed skill files before writing EdgeSpark code:

   ```bash
   skills/building-edgespark-apps/SKILL.md
   skills/edgespark-frontend-design/SKILL.md
   ```

5. Implement the backend bridge route described below, deploy the EdgeSpark app
   with the official EdgeSpark CLI commands from `nextSteps`, then verify with
   the Bloome control-plane command:

   ```bash
   bloome-cli edgespark project verify <alias>
   ```

6. Bind the widget to the existing alias:

   ```bash
   widget create --title "T" --html-file widgets/<name>.html --edgespark <alias>
   ```

   Or attach later:

   ```bash
   widget update <widgetId> --edgespark <alias>
   ```

The `--edgespark` value is an existing Agent-local alias from the Bloome
`edgespark project create --alias <alias>` command. It does not create a new
EdgeSpark project.

`edgespark project delete <alias>` only unbinds this Agent alias and removes
the local EdgeSpark API key secret. It does not delete the external EdgeSpark
project and does not disable widgets that already have
`metadata.edgespark.{projectId,baseUrl}`. Do not use project delete as a
runtime revoke mechanism. To stop one widget from using EdgeSpark, run:

```bash
widget update <widgetId> --clear-edgespark
```

That removes the widget's `metadata.edgespark`, so future renders of that
widget and all its instances no longer receive `ResonWidget.edgespark`.

If a Bloome EdgeSpark command or `widget create/update --edgespark` returns
`EDGESPARK_DISABLED`, stop the EdgeSpark path. Do not retry raw EdgeSpark CLI
commands and do not create an untracked external EdgeSpark project. Use
`ResonWidget.state` only for simple widgets; for backend-required workflows,
tell the user EdgeSpark backend support is temporarily unavailable.

Keep command surfaces separate:

- **Bloome control-plane**: `bloome-cli edgespark project create/list/info/verify/delete`
  creates and tracks the Bloome binding.
- **Official EdgeSpark CLI**: raw `edgespark pull`, `edgespark deploy`, schema,
  type, and app implementation commands run only after the Bloome project exists
  and usually appear in the returned `nextSteps`.

## Runtime Contract

Use EdgeSpark when a widget needs real backend behavior: Bloome identity,
ownership, "my/all" views, delete/edit-own rules, durable collections, list
CRUD, queries, permissions, external APIs, secrets, scheduled jobs, webhooks,
rate limits, or moderation. Do not build those workflows on
`ResonWidget.state`; state is only for small bounded conversation-scoped JSON.
Message boards, comments, guestbooks, submissions, feeds, and task/record lists
are EdgeSpark-backed by default unless the user explicitly asks for a
simple/local/temporary state-only widget.

Widget frontend code must call:

```javascript
await ResonWidget.edgespark.fetch('/api/public/<resource>');
await ResonWidget.edgespark.fetch('/api/public/<resource>', { method: 'POST' });
```

Do not hardcode the EdgeSpark host and do not call bare `fetch('https://...edgespark.app/...')`. Bloome injects `ResonWidget.edgespark` only for widgets bound with `--edgespark <alias>`.

The injected bridge does this:

1. Holds a short-lived Bloome viewer JWT for the current widget instance.
2. Calls the EdgeSpark backend public route:

   ```text
   POST /api/public/_bloome/silent-sign-in
   ```

3. Sends the Bloome viewer JWT in the request header:

   ```text
   Authorization: Bearer <bloome-viewer-jwt>
   ```

4. Expects a JSON response containing a Bloome-backed bearer token:

   ```json
   {
     "token": "bloome-backed-bearer-token",
     "user": {},
     "bloomeUser": {},
     "expiresAt": "2026-05-07T12:00:00.000Z"
   }
   ```

5. Sends that bearer token to EdgeSpark routes when available. If no Bloome
   session exists and the target path is under `/api/public/*`, the helper
   still sends the request without a bearer. Non-public paths fail when no
   bearer can be obtained.

`ResonWidget.edgespark.getToken()` returns the Bloome-backed EdgeSpark API token, not the Bloome JWT.
`ResonWidget.edgespark.fetch(path, options)` should be the default API for
widget code. `options` is the normal `fetch` options object, with an optional
`auth` field added by the Bloome bridge. The helper tries to attach identity
first, but allows anonymous fallback only for `/api/public/*` paths. Use `auth:
"required"` only for routes that must fail before any network request when no
Bloome session exists. Use `auth: "none"` or `fetchPublic(path, options)` only
when you explicitly want to skip identity even if the user is logged in.

## Backend Route Requirements

Every Bloome-bound EdgeSpark app must expose:

```text
GET /api/public/_bloome/health
POST /api/public/_bloome/silent-sign-in
```

`silent-sign-in` must:

1. Require `Authorization: Bearer <bloome-viewer-jwt>`.
2. Do not accept JWTs from the POST body.
3. Verify the JWT with the Bloome JWKS URL from the project binding/config.
4. Require the expected issuer and audience. Audience is the EdgeSpark project id.
5. Sign a short-lived project-local bearer token for the verified Bloome participant.
6. Return that bearer token and user metadata.

Use a remote JWKS fetch such as `createRemoteJWKSet(new URL(BLOOME_JWKS_URL))`. Do not inline Bloome public keys into generated EdgeSpark apps.

The Bloome project-create command writes a starter implementation to
`edgespark/<alias>/server/src/bloome-bridge.ts` when it runs in an Agent
workspace. It also writes
`edgespark/<alias>/server/src/defs/runtime.ts` declaring the Bloome runtime
secrets. Use those generated files as the starting point and mount the bridge
from `server/src/index.ts` with `installBloomeBridge(app)`. Do not rewrite the
bridge from scratch unless the generated file is missing or EdgeSpark has
shipped a newer official server-side session API.

The bridge reads Bloome config from EdgeSpark secrets with `secret.get()`:
`BLOOME_JWKS_URL`, `BLOOME_ISSUER`, `EDGESPARK_PROJECT_ID`, and
`BLOOME_BRIDGE_SECRET`. Do not hardcode the project id in server code. The
deployment target still comes from `edgespark.toml`; the JWT audience check
comes from the `EDGESPARK_PROJECT_ID` secret in the EdgeSpark runtime.

Bloome-authenticated business routes must live under `/api/public/*` and call
`getBloomeUser(c)` from the generated bridge. Do not put these routes under
`/api/*`: EdgeSpark reserves that prefix for platform auth and will reject the
Bloome-backed bearer before your handler runs. Partition durable data by
`bloomeUser.id`, not by a display name or browser-local id.

## Access Modes

Before writing routes, choose the widget's access mode. Share URLs and public
widget URLs may open without a Bloome session, so do not assume
`ResonWidget.edgespark.fetch()` can sign in.

| Mode                                      | Use When                                                                                             | Backend Rule                                                                                       | Frontend Rule                                                                                                                                    |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| Public read, authenticated mutation       | Non-sensitive shared content where logged-out viewers should inspect state but actions need identity | Anonymous `GET /api/public/<resource>`; `POST`/`PUT`/`PATCH`/`DELETE` call `getBloomeUser(c)`      | Use `fetch` for both; helper attaches identity when possible and anonymous-falls-back for public reads. Show login/open-Bloome affordance on 401 |
| Authenticated read/write                  | Private, member-only, user-specific, or sensitive data                                               | Every business route calls `getBloomeUser(c)`                                                      | Use `fetch`; logged-out share pages show login/open-Bloome instead of a broken empty state                                                       |
| Anonymous read/write                      | User explicitly asks for anonymous participation and accepts abuse/deletion tradeoffs                | Define anonymous identity, rate limits, abuse handling, and delete permissions before writing data | Use `fetch`; do not claim per-user ownership unless you defined an anonymous identity                                                            |
| Public static read, authenticated actions | Catalogs, public status panels, event pages, docs, leaderboards, previews                            | Public/static `GET`; personalized actions call `getBloomeUser(c)`                                  | Use `fetch`; helper attaches identity when possible and anonymous-falls-back for public paths                                                    |

Default to **public read, authenticated mutation** for non-sensitive shared
content. Choose **authenticated read/write** when data is private or
conversation/member-bound. Do not choose anonymous write unless the user asked
for it explicitly.

## Data Rules

- For verified EdgeSpark widgets, EdgeSpark is the single source of truth.
- Do not mirror EdgeSpark rows into `ResonWidget.state`.
- Do not define a widget `stateSchema` for EdgeSpark-only data.
- Use `ResonWidget.state` only if the user explicitly asks for an offline/local fallback, and label that degraded behavior in your reply.
- If a feature has author attribution, "my items", delete-own behavior, likes by user, or list CRUD, model it as EdgeSpark data even when the UI is small.

## Deployment Rules

Bloome-created projects target the `production` environment. Use:

```bash
cd edgespark/<alias>
npm install
EDGESPARK_PROJECT_ENVIRONMENT=production edgespark pull
EDGESPARK_PROJECT_ENVIRONMENT=production edgespark deploy
```

If running through Bloome, wrap EdgeSpark CLI commands with the returned `secret call` command so `EDGESPARK_API_KEY` is injected.

Do not use `edgespark pull schema --environment production`; CLI versions differ and this can resolve to the wrong environment or reject the flag.

## Debugging

| Symptom                                               | Likely cause                                                                    | Fix                                                                                       |
| ----------------------------------------------------- | ------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `ResonWidget.edgespark` is missing                    | Widget is not bound with `--edgespark <alias>`                                  | Run `widget update <widgetId> --edgespark <alias>`                                        |
| `POST /api/public/_bloome/silent-sign-in` returns 404 | Backend bridge route was not deployed                                           | Add the route, deploy, then verify                                                        |
| `silent-sign-in` returns 400                          | Bloome JWT was not sent in `Authorization: Bearer <jwt>`                        | Fix the injected bridge/client; do not send JWT in POST body                              |
| `silent-sign-in` returns 401                          | Bloome JWT is expired, wrong audience, or cannot verify                         | Check JWKS URL, issuer, audience, and header value                                        |
| `silent-sign-in` returns 5xx/502                      | Bridge code threw after JWT verification                                        | Check that it does not write `es_system__auth_*` tables; system auth tables are read-only |
| `/api/*` returns 401 after silent sign-in succeeds    | Route is under EdgeSpark platform-auth prefix                                   | Move Bloome-authenticated business routes to `/api/public/*` and call `getBloomeUser(c)`  |
| Logged-out share page never calls EdgeSpark           | Target path is not under `/api/public/*`, or frontend forced `auth: "required"` | Put anonymous-readable routes under `/api/public/*` and use default `fetch`               |
| Widget still calls `/api/widgets/.../state`           | Frontend has a `ResonWidget.state` fallback or mirror                           | Remove state fallback for EdgeSpark-backed workflows                                      |
