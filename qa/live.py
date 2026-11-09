import json, time, statistics, urllib.request, urllib.error, threading
import os
U = os.environ.get("QA_URL", "https://securekbgw.onrender.com")

def req(method, path, body=None, headers=None, raw=None, timeout=60):
    data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
    h = {"Content-Type": "application/json", **(headers or {})}
    r = urllib.request.Request(U + path, data=data, method=method, headers=h)
    t = time.time()
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            return resp.status, resp.read(), dict(resp.headers), time.time() - t
    except urllib.error.HTTPError as e:
        return e.code, e.read(), dict(e.headers), time.time() - t
    except Exception as e:
        return 0, repr(e).encode(), {}, time.time() - t

def js(b):
    try: return json.loads(b)
    except Exception: return None

print("== 1. what is deployed")
c, b, h, dt = req("GET", "/api/config"); print("config", c, js(b), f"{dt:.2f}s")
c, b, h, dt = req("GET", "/")
print("page", c, "CSP" if "Content-Security-Policy" in h or "content-security-policy" in h else "NO CSP",
      "| nosniff" if any(k.lower()=="x-content-type-options" for k in h) else "| NO nosniff",
      "| CORS open!" if any(k.lower()=="access-control-allow-origin" for k in h) else "| no CORS header (good)")
print("scope banner in page:", b"Public demo" in b, "| old 'synthetic' wording:", b"Everything here is synthetic" in b)

print("\n== 2. demo key issuance and limits")
keys = []
for i in range(5):
    c, b, h, dt = req("POST", "/api/demo-key")
    keys.append(js(b).get("key") if c == 200 else None)
    print(f"  request {i+1}: {c} {'key issued' if c==200 else (js(b) or {}).get('error')}")
key = next(k for k in keys if k)
A = {"Authorization": "Bearer " + key}

print("\n== 3. is the new knowledge base live")
for q in ["How many layoffs happened in Amazon in 2023?", "What happened to the S&P 500 in 2022?", "Should I buy Nvidia stock?", "What is the capital of France?"]:
    time.sleep(0.2)
    c, b, h, dt = req("POST", "/api/ask", {"question": q}, A)
    d = js(b) or {}
    print(f"  {q[:44]:<44} {c} {d.get('status')} {(d.get('answer') or d.get('reason') or '')[:75]}")

print("\n== 4. latency, 8 sequential asks (spaced past the rate limit)")
lat = []
for i in range(8):
    time.sleep(0.12)
    c, b, h, dt = req("POST", "/api/ask", {"question": "What caused the chip shortage?"}, A)
    if c == 200 and (js(b) or {}).get("status") in ("ok", "refused"): lat.append(dt)
print(f"  ok responses {len(lat)}/8  p50 {statistics.median(lat)*1000:.0f} ms  max {max(lat)*1000:.0f} ms" if lat else "  none succeeded")

print("\n== 5. concurrency: 20 threads x 5 asks on ONE key (rate limit should bite; credits must not go negative)")
res = []
def worker():
    for _ in range(5):
        c, b, h, dt = req("POST", "/api/ask", {"question": "ChatGPT release date"}, A)
        d = js(b) or {}
        res.append((c, d.get("status"), d.get("reason"), d.get("credits_left")))
th = [threading.Thread(target=worker) for _ in range(20)]
[t.start() for t in th]; [t.join() for t in th]
from collections import Counter
print("  outcomes:", dict(Counter((c, s, r) for c, s, r, _ in res)))
lefts = [x[3] for x in res if x[3] is not None]
print("  min credits_left seen:", min(lefts) if lefts else None, "(never negative)" if not lefts or min(lefts) >= 0 else "NEGATIVE!")
c, b, h, dt = req("GET", "/api/me", headers=A); print("  /api/me after:", js(b))

print("\n== 6. malformed and hostile requests (expect 4xx, never 500)")
cases = [
 ("not json", "POST", "/api/ask", dict(raw=b"{not json")),
 ("json array", "POST", "/api/ask", dict(raw=b"[1,2,3]")),
 ("null", "POST", "/api/ask", dict(raw=b"null")),
 ("question is number", "POST", "/api/ask", dict(body={"question": 12345})),
 ("question is object", "POST", "/api/ask", dict(body={"question": {"a": 1}})),
 ("empty question", "POST", "/api/ask", dict(body={"question": "   "})),
 ("501-char question", "POST", "/api/ask", dict(body={"question": "a" * 501})),
 ("5 MB body", "POST", "/api/ask", dict(raw=b"x" * 5_000_000)),
 ("emoji/unicode", "POST", "/api/ask", dict(body={"question": "☃\U0001F600 股票 nvidia"})),
 ("null byte", "POST", "/api/ask", dict(body={"question": "nvidia\u0000 value"})),
 ("wrong content-type", "POST", "/api/ask", dict(raw=b"question=nvidia", headers={"Content-Type": "text/plain"})),
 ("GET on /api/ask", "GET", "/api/ask", {}),
 ("PUT on /api/ask", "PUT", "/api/ask", dict(body={"question": "x"})),
 ("OPTIONS (CORS preflight)", "OPTIONS", "/api/ask", dict(headers={"Origin": "https://evil.example", "Access-Control-Request-Method": "POST"})),
 ("path traversal", "GET", "/../../etc/passwd", {}),
 ("encoded traversal", "GET", "/%2e%2e/%2e%2e/etc/passwd", {}),
 ("unknown path", "GET", "/nope", {}),
 ("admin w/ buyer key", "GET", "/api/admin/report", dict(headers={"X-Admin-Token": key})),
 ("admin create buyer", "POST", "/api/admin/buyers", dict(body={"name": "x", "credits": 99999})),
 ("giant URL", "GET", "/" + "a" * 20000, {}),
 ("MCP no key", "POST", "/mcp", dict(body={})),
]
bad = 0
for name, m, p, kw in cases:
    time.sleep(0.12)
    kw = dict(kw)
    if p.startswith("/api/ask") and "Authorization" not in kw.get("headers", {}):
        kw["headers"] = {**kw.get("headers", {}), **A}
    c, b, h, dt = req(m, p, **kw)
    flag = "FAIL(5xx/0)" if c >= 500 or c == 0 else "ok"
    bad += flag != "ok"
    cors = " CORS-ALLOWED!" if any(k.lower() == "access-control-allow-origin" for k in h) else ""
    print(f"  {flag:<12} {c:<4} {name}{cors}")
print("  server errors:", bad)

print("\n== 7. still healthy afterwards?")
c, b, h, dt = req("GET", "/api/config"); print("  config", c, f"{dt:.2f}s")
