"""skbgw: the seller's whole interface.

    skbgw demo                    one command: synthetic data, a demo buyer, ready to serve
    skbgw init ./my-notes         load a folder of .md/.txt/.json notes
    skbgw add-buyer "Acme" -c 50 [--entity acme]  create a buyer key; same entity = shared limits
    skbgw serve                   start the endpoint
    skbgw ask KEY "question"      try a query locally
    skbgw report                  who asked, who paid, how much
"""
import argparse
import json
import secrets
import sys
from pathlib import Path

from .core import Gateway
from .ingest import ingest
from .ledger import Ledger
from .policy import DEFAULT
from .store import KnowledgeBase, Doc

HOME = Path("skbgw-data")


def _kb():
    path = HOME / "kb.json"
    if not path.exists():
        sys.exit("No knowledge base yet. Run: skbgw init <folder>   (or: skbgw demo)")
    return KnowledgeBase.load(path)


def _ledger():
    HOME.mkdir(exist_ok=True)
    return Ledger(str(HOME / "ledger.db"))


def _connect_help(key, port):
    url = f"http://localhost:{port}/mcp"
    print(f"\nGive the buyer this key (shown once, only a hash is stored):\n    {key}\n")
    print("Claude Code:")
    print(f'    claude mcp add --transport http seller-kb {url} --header "Authorization: Bearer {key}"')
    print("Any MCP client that supports HTTP headers:")
    print(json.dumps({"url": url, "headers": {"Authorization": f"Bearer {key}"}}, indent=2))
    print("\nFor a buyer on another machine, serve behind HTTPS and replace localhost with your public URL.")


def cmd_init(a):
    docs, skipped = ingest(a.folder)
    if not docs:
        sys.exit(f"No usable notes found in {a.folder} (use .md, .txt or .json).")
    HOME.mkdir(exist_ok=True)
    (HOME / "kb.json").write_text(json.dumps(docs, indent=1))
    kb = KnowledgeBase([Doc(**d) for d in docs])
    print(f"Loaded {len(kb)} notes.")
    if kb.quarantined:
        print(f"Quarantined {len(kb.quarantined)} that look like prompt injection: {', '.join(kb.quarantined)}")
    for name, why in skipped:
        print(f"Skipped {name}: {why}")
    print("Next: skbgw add-buyer \"Buyer name\" --credits 50")


def cmd_add_buyer(a):
    key = "skb_" + secrets.token_urlsafe(24)
    _ledger().add_buyer(key, a.name, a.credits, a.entity)
    print(f"Created buyer '{a.name}' ({a.entity or a.name}) with {a.credits} credits.")
    _connect_help(key, a.port)


def cmd_topup(a):
    n = _ledger().topup(a.name, a.credits)
    print(f"Added {a.credits} credits to {n} buyer(s) named '{a.name}'." if n else f"No buyer named '{a.name}'.")


def cmd_serve(a):
    import uvicorn
    from .http_server import build_app

    gw = Gateway(_kb(), _ledger(), DEFAULT)
    token_file = HOME / "admin-token"
    if not token_file.exists():
        token_file.write_text(secrets.token_urlsafe(24))
        token_file.chmod(0o600)
    token = token_file.read_text().strip()
    url = f"http://localhost:{a.port}"
    print(f"Serving {len(gw.kb)} notes. (Ctrl+C to stop)")
    print(f"  Web UI:          {url}/")
    print(f"  MCP for agents:  {url}/mcp")
    print(f"  Seller dashboard admin token: {token}   (also in {token_file})")
    uvicorn.run(build_app(gw, token, HOME / "kb.json", url), host=a.host, port=a.port, log_level="warning")


def cmd_ask(a):
    r = Gateway(_kb(), _ledger(), DEFAULT).query(a.key, a.question)
    print(f"{r.status}: {r.answer or r.reason}  (charged {r.charged}, credits left {r.credits_left})")


def cmd_report(a):
    led = _ledger()
    rows = led.seller_report()
    if not rows:
        return print("No buyers yet.")
    print(f"{'buyer':<20}{'queries':>8}{'revenue':>9}{'docs seen':>10}")
    for r in rows:
        print(f"{r['buyer']:<20}{r['queries']:>8}{r['revenue']:>9}{r['distinct_docs']:>10}")
    print(f"\nTotal revenue (credits): {sum(r['revenue'] for r in rows)}")


def cmd_demo(a):
    from importlib import import_module  # synthetic data lives in scripts/, outside the package

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
    docs = import_module("make_synthetic_kb").make(120)
    HOME.mkdir(exist_ok=True)
    (HOME / "kb.json").write_text(json.dumps(docs, indent=1))
    key = "skb_" + secrets.token_urlsafe(24)
    _ledger().add_buyer(key, "demo buyer", 50)
    print("Demo ready: 120 synthetic notes and a demo buyer with 50 credits.")
    _connect_help(key, a.port)
    print("\nNow run: skbgw serve")


def main(argv=None):
    p = argparse.ArgumentParser(prog="skbgw", description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("init"); s.add_argument("folder"); s.set_defaults(fn=cmd_init)
    s = sub.add_parser("add-buyer"); s.add_argument("name"); s.add_argument("-c", "--credits", type=int, default=50)
    s.add_argument("--entity", help="buying company; keys with the same entity share limits"); s.add_argument("--port", type=int, default=8000); s.set_defaults(fn=cmd_add_buyer)
    s = sub.add_parser("topup"); s.add_argument("name"); s.add_argument("credits", type=int); s.set_defaults(fn=cmd_topup)
    s = sub.add_parser("serve"); s.add_argument("--host", default="127.0.0.1"); s.add_argument("--port", type=int, default=8000)
    s.set_defaults(fn=cmd_serve)
    s = sub.add_parser("ask"); s.add_argument("key"); s.add_argument("question"); s.set_defaults(fn=cmd_ask)
    s = sub.add_parser("report"); s.set_defaults(fn=cmd_report)
    s = sub.add_parser("demo"); s.add_argument("--port", type=int, default=8000); s.set_defaults(fn=cmd_demo)
    a = p.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
