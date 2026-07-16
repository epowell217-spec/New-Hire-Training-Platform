# Center of Family Love Training Platform

Scaffold for a training portal with:
- email invite login
- uploaded videos
- completion tracking
- CEO welcome video upload

## Current implementation
- session cookie auth
- invite acceptance flow
- login/logout
- module uploads saved locally under `public/uploads`
- progress tracking stored in Postgres via Prisma

## Next steps
1. Install dependencies
2. Set `DATABASE_URL` and `SESSION_SECRET`
3. Run `prisma migrate dev`
4. Point `NEXT_PUBLIC_APP_URL` at the deployed domain
5. Replace the mailer stub with a real provider


## Email configuration
- `SMTP_HOST` defaults to `smtp.office365.com`
- `SMTP_PORT` defaults to `587`
- `SMTP_USER` defaults to `info@cflinc.org`
- `SMTP_PASS` enables live sending; without it, invites log to the console
- `SMTP_FROM` defaults to `info@cflinc.org`


## Storage configuration
- Cloudflare R2 is the primary upload path when these are set: `R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET`
- Optional: `R2_PUBLIC_BASE_URL` if the bucket is public behind a custom domain
- If R2 env vars are missing, uploads fall back to local server storage

## SMTP sender
- Defaults to `epowell@cflinc.org`
