"""Hosted endpoints: the web UI, a small JSON API for it, and the MCP endpoint.

- `/`                      the web UI (static page)
- `/api/ask`, `/api/me`    buyer API, `Authorization: Bearer <buyer key>`
- `/api/admin/*`           seller API, `X-Admin-Token: <admin token>`
- `/mcp`                   MCP for agents, `Authorization: Bearer <buyer key>`, POST only

Run behind TLS for anything beyond localhost: keys and the admin token travel in clear over plain HTTP.
"""
import contextvars
import json
import re
import secrets
import time
from collections import defaultdict
from pathlib import Path

from mcp.server.mcpserver import MCPServer
from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse
from starlette.routing import Mount, Route

from .core import Gateway
from .mcp_server import INSTRUCTIONS
from .store import INJECTION, Doc, KnowledgeBase

UI = Path(__file__).with_name("ui.html")
MAX_NOTE_CHARS = 20_000
_key = contextvars.ContextVar("buyer_key", default="")


def _bearer(headers):
    """headers: a mapping with str keys (Starlette Request.headers) or an ASGI scope header list."""
    if isinstance(headers, list):
        headers = {k.decode().lower(): v.decode() for k, v in headers}
    auth = headers.get("authorization", "")
    return auth[7:].strip() if auth.lower().startswith("bearer ") else ""


class _McpAuth:
    """Guards the MCP app: POST only, valid buyer key required, key passed to the tool via a contextvar."""

    def __init__(self, app, gateway):
        self.app, self.gateway = app, gateway

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            if scope["method"] != "POST":  # stateless JSON mode needs no streams; idle GETs would hold sockets open
                resp = JSONResponse({"error": "POST only"}, status_code=405, headers={"Allow": "POST"})
                return await resp(scope, receive, send)
            key = _bearer(scope["headers"])
            if not key or self.gateway.ledger.buyer(key) is None:
                resp = JSONResponse({"error": "missing or unknown buyer key"}, status_code=401)
                return await resp(scope, receive, send)
            _key.set(key)
        await self.app(scope, receive, send)


def _result(r):
    return {"status": r.status, "answer": r.answer, "reason": r.reason, "charged": r.charged,
            "credits_left": r.credits_left, "content_type": "untrusted_seller_data"}


DEMO_CREDITS = 15
DEMO_KEYS_PER_IP_PER_HOUR = 3
DEMO_KEYS_TOTAL = 500


def build_app(gateway: Gateway, admin_token: str, kb_path: Path, public_url="http://localhost:8000",
              demo=False, admin_enabled=True):
    mcp = MCPServer("secure-kb-gateway", instructions=INSTRUCTIONS)

    @mcp.tool()
    def ask(question: str) -> str:
        """Ask one question. Returns JSON with status, answer, charged and credits_left."""
        return json.dumps(_result(gateway.query(_key.get(), question)))

    mcp_app = mcp.streamable_http_app(stateless_http=True, json_response=True)

    def buyer_key(request):
        key = _bearer(request.headers)
        return key if key and gateway.ledger.buyer(key) else None

    def is_admin(request):
        return admin_enabled and secrets.compare_digest(request.headers.get("x-admin-token", ""), admin_token)

    issued = defaultdict(list)  # ip -> timestamps of demo keys issued (in memory; resets on restart)

    def client_ip(request):
        # Behind a platform proxy the first X-Forwarded-For hop is the client. A direct caller can spoof it,
        # which only weakens the per-IP demo limit; the total cap below still holds.
        fwd = request.headers.get("fly-client-ip") or request.headers.get("x-forwarded-for", "").split(",")[0].strip()
        return fwd or (request.client.host if request.client else "unknown")

    async def body(request):
        try:
            data = await request.json()
            return data if isinstance(data, dict) else {}
        except ValueError:
            return {}

    async def home(request):
        return HTMLResponse(UI.read_text(), headers={"Content-Security-Policy": "default-src 'self'; style-src 'unsafe-inline'; script-src 'unsafe-inline'", "X-Content-Type-Options": "nosniff"})

    async def api_ask(request):
        key = buyer_key(request)
        if not key:
            return JSONResponse({"error": "missing or unknown buyer key"}, status_code=401)
        q = (await body(request)).get("question")
        if not isinstance(q, str) or not q.strip():
            return JSONResponse({"error": "question required"}, status_code=400)
        return JSONResponse(_result(gateway.query(key, q)))

    async def api_me(request):
        key = buyer_key(request)
        if not key:
            return JSONResponse({"error": "missing or unknown buyer key"}, status_code=401)
        b = gateway.ledger.buyer(key)
        return JSONResponse({"name": b["name"], "credits": b["credits"], "queries": b["queries"]})

    async def api_config(request):
        return JSONResponse({"demo": demo, "admin": admin_enabled, "demo_credits": DEMO_CREDITS})

    async def api_demo_key(request):
        if not demo:
            return JSONResponse({"error": "not found"}, status_code=404)
        ip, now = client_ip(request), time.time()
        issued[ip] = [t for t in issued[ip] if now - t < 3600]
        total = sum(1 for b in gateway.ledger.buyers() if b["name"].startswith("Demo visitor"))
        if len(issued[ip]) >= DEMO_KEYS_PER_IP_PER_HOUR or total >= DEMO_KEYS_TOTAL:
            return JSONResponse({"error": "Demo keys are limited right now. Try again later."}, status_code=429)
        issued[ip].append(now)
        key = "skb_" + secrets.token_urlsafe(24)
        gateway.ledger.add_buyer(key, "Demo visitor " + secrets.token_hex(2), DEMO_CREDITS)
        return JSONResponse({"key": key, "credits": DEMO_CREDITS})

    def admin_only(fn):
        async def wrapper(request):
            if not admin_enabled:
                return JSONResponse({"error": "not found"}, status_code=404)
            if not is_admin(request):
                return JSONResponse({"error": "admin token required"}, status_code=401)
            return await fn(request)
        return wrapper

    @admin_only
    async def admin_report(request):
        led = gateway.ledger
        return JSONResponse({
            "notes": len(gateway.kb), "quarantined": gateway.kb.quarantined,
            "revenue": sum(r["revenue"] for r in led.seller_report()),
            "buyers": led.buyers(), "report": led.seller_report(), "recent": led.recent(15),
            "mcp_url": f"{public_url}/mcp",
        })

    @admin_only
    async def admin_add_buyer(request):
        d = await body(request)
        name, credits = str(d.get("name", "")).strip()[:60], d.get("credits", 50)
        if not name or not isinstance(credits, int) or not 0 <= credits <= 10**6:
            return JSONResponse({"error": "name and integer credits (0 to 1,000,000) required"}, status_code=400)
        entity = str(d.get("entity", "")).strip()[:60] or None
        key = "skb_" + secrets.token_urlsafe(24)
        gateway.ledger.add_buyer(key, name, credits, entity)
        return JSONResponse({"key": key, "name": name, "credits": credits, "entity": entity or name,
                             "claude_code": f'claude mcp add --transport http seller-kb {public_url}/mcp '
                                            f'--header "Authorization: Bearer {key}"'})

    @admin_only
    async def admin_topup(request):
        d = await body(request)
        credits = d.get("credits")
        if not isinstance(credits, int) or not 0 < credits <= 10**6:
            return JSONResponse({"error": "positive integer credits required"}, status_code=400)
        n = gateway.ledger.topup(str(d.get("name", "")), credits)
        return JSONResponse({"updated": n}, status_code=200 if n else 404)

    @admin_only
    async def admin_add_note(request):
        d = await body(request)
        title, text = str(d.get("title", "")).strip()[:120], str(d.get("text", "")).strip()
        if not title or not text or len(text) > MAX_NOTE_CHARS:
            return JSONResponse({"error": f"title and text (max {MAX_NOTE_CHARS} chars) required"}, status_code=400)
        ids = {x.id for x in gateway.kb.docs} | set(gateway.kb.quarantined)
        base = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:40] or "note"
        nid, n = base, 1
        while nid in ids:
            n += 1
            nid = f"{base}-{n}"
        quarantined = bool(INJECTION.search(title + " " + text))
        existing = json.loads(kb_path.read_text()) if kb_path.exists() else []
        existing.append({"id": nid, "title": title, "text": text})
        kb_path.write_text(json.dumps(existing, indent=1))
        gateway.set_kb(KnowledgeBase([Doc(**x) for x in existing]))
        return JSONResponse({"id": nid, "quarantined": quarantined})

    routes = [
        Route("/", home, methods=["GET"]),
        Route("/api/ask", api_ask, methods=["POST"]),
        Route("/api/me", api_me, methods=["GET"]),
        Route("/api/config", api_config, methods=["GET"]),
        Route("/api/demo-key", api_demo_key, methods=["POST"]),
        Route("/api/admin/report", admin_report, methods=["GET"]),
        Route("/api/admin/buyers", admin_add_buyer, methods=["POST"]),
        Route("/api/admin/topup", admin_topup, methods=["POST"]),
        Route("/api/admin/notes", admin_add_note, methods=["POST"]),
        Mount("/", app=_McpAuth(mcp_app, gateway)),
    ]
    return Starlette(routes=routes, lifespan=mcp_app.router.lifespan_context)
