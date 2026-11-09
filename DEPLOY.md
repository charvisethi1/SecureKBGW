# Taking the public demo live

This deploys the **synthetic-data demo**: visitors get their own key with 15 free credits, the seller dashboard is switched off, and nothing real is stored. Do not put real company data in it. The legal scoping in `research/implementation-plan.md` has not happened.

## What the container does
`Dockerfile` runs `python -m gateway serve` with these defaults:

| Setting | Value | Why |
|---|---|---|
| `SKBGW_DEMO=1` | on | creates 120 synthetic notes on first start, enables the "Try the demo" button |
| `SKBGW_DISABLE_ADMIN=1` | on | admin routes return 404, the Seller tab is hidden |
| `SKBGW_HOME=/data` | | where the SQLite ledger and notes live |
| `PORT` | set by the host | server binds `0.0.0.0:$PORT` |
| `SKBGW_PUBLIC_URL` | **you set this** | the `https://…` address shown in connect commands |

Limits in the demo: 15 credits per visitor key, 3 keys per IP per hour, 500 keys in total, plus the normal per-company query and information limits.

## Option 1: Render (simplest)
1. Push this repo to GitHub (done).
2. On render.com: **New, Web Service**, connect the repo, **Runtime: Docker**. A free instance is fine for an MVP: it sleeps when idle, so the first visit after a quiet period loads slowly (roughly up to a minute; check Render's current free-tier notes). Tell early visitors to expect that. A paid instance removes the wait.
3. Environment: set `SKBGW_PUBLIC_URL` to the service URL Render shows (for example `https://skbgw-demo.onrender.com`). Leave the rest at their defaults.
4. Deploy. HTTPS is automatic.
5. Without a disk the ledger resets on every deploy or restart, which is fine for a demo. To keep it, add a disk mounted at `/data`.

## Option 2: Fly.io
1. Install `flyctl`, then in the repo run `fly launch --no-deploy` (accept the Dockerfile, internal port 8000).
2. `fly secrets set SKBGW_PUBLIC_URL=https://<your-app>.fly.dev`
3. `fly deploy`. HTTPS is automatic. Add `fly volumes create data` and mount it at `/data` only if you want persistence.

## Option 3: your laptop, for an hour
```bash
./skbgw serve --demo
cloudflared tunnel --url http://localhost:8000   # or: ngrok http 8000
```
Set `SKBGW_PUBLIC_URL` to the tunnel address first. The link dies when you stop.

## Smoke test after deploying
Replace `URL` with your address.
```bash
curl -s URL/api/config                      # {"demo":true,"admin":false,...}
curl -s -X POST URL/api/demo-key            # returns a key with 15 credits
curl -s -o /dev/null -w '%{http_code}\n' URL/api/admin/report   # must be 404
```
Then open `URL/` in a browser, click **Try the demo**, and ask `Main failure cause for EXP-0007`.

## Before you post the link
- [ ] The banner says "Public demo, synthetic data" (it appears automatically in demo mode).
- [ ] `/api/admin/report` returns 404.
- [ ] You looked at the page on your phone and in a dark-mode browser.
- [ ] You know how to take it down (Render: suspend the service; Fly: `fly scale count 0`).
- [ ] You are ready for people to try to extract the whole knowledge base. On synthetic data that is useful, not harmful. Write down what they find.

## Known limits of the demo
- No payments; credits are fake.
- The per-IP limit trusts the proxy's forwarded address, so a determined person can get more keys. The 500-key total still holds.
- Keys and questions are stored (hashed keys, plain questions) in the ledger on the server. The banner says questions are logged.
- State is lost on restart unless you add a volume.
- One process only. If you need more than one instance, move the ledger to a shared database first.
