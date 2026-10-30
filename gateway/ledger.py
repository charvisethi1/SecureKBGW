"""Buyer accounts, credit metering and an audit log (SQLite, stdlib).

Keys are per buyer user, but information limits are per *entity* (the buying company): several keys
issued to one entity share one query count and one revealed-content budget.
"""
import hashlib
import sqlite3
import time


def _h(key):
    """Keys are stored as SHA-256 hashes so a leaked database does not leak buyer keys."""
    return hashlib.sha256(key.encode()).hexdigest()


class Ledger:
    def __init__(self, path=":memory:", clock=time.time):
        self._clock = clock
        self._db = sqlite3.connect(path, check_same_thread=False)  # callers serialize via Gateway's lock
        self._db.executescript(
            """
            CREATE TABLE IF NOT EXISTS buyers (
                key TEXT PRIMARY KEY, name TEXT, credits INTEGER, queries INTEGER DEFAULT 0,
                last_ts REAL DEFAULT 0, entity TEXT);
            CREATE TABLE IF NOT EXISTS docs_seen (key TEXT, doc_id TEXT, PRIMARY KEY (key, doc_id));
            CREATE TABLE IF NOT EXISTS revealed (
                entity TEXT, doc_id TEXT, idx INTEGER, chars INTEGER, PRIMARY KEY (entity, doc_id, idx));
            CREATE TABLE IF NOT EXISTS events (
                ts REAL, key TEXT, status TEXT, doc_id TEXT, chars INTEGER, charge INTEGER, question TEXT);
            """
        )
        cols = {r[1] for r in self._db.execute("PRAGMA table_info(buyers)")}
        if "entity" not in cols:  # database created before entities existed
            self._db.execute("ALTER TABLE buyers ADD COLUMN entity TEXT")
            self._db.execute("UPDATE buyers SET entity=name WHERE entity IS NULL")

    def add_buyer(self, key, name, credits, entity=None):
        self._db.execute("INSERT OR REPLACE INTO buyers (key, name, credits, entity) VALUES (?,?,?,?)",
                         (_h(key), name, credits, entity or name))
        self._db.commit()

    def topup(self, name, credits):
        cur = self._db.execute("UPDATE buyers SET credits=credits+? WHERE name=?", (credits, name))
        self._db.commit()
        return cur.rowcount

    def buyers(self):
        rows = self._db.execute("SELECT name, credits, queries, entity FROM buyers ORDER BY name").fetchall()
        return [dict(zip(("name", "credits", "queries", "entity"), r)) for r in rows]

    def buyer(self, key):
        row = self._db.execute(
            "SELECT name, credits, queries, last_ts, entity FROM buyers WHERE key=?", (_h(key),)).fetchone()
        return None if row is None else dict(zip(("name", "credits", "queries", "last_ts", "entity"), row))

    def entity_queries(self, entity):
        return self._db.execute("SELECT COALESCE(SUM(queries),0) FROM buyers WHERE entity=?", (entity,)).fetchone()[0]

    def revealed(self, entity):
        """({(doc_id, sentence_idx)}, total chars) already shown to this entity."""
        rows = self._db.execute("SELECT doc_id, idx, chars FROM revealed WHERE entity=?", (entity,)).fetchall()
        return {(d, i) for d, i, _ in rows}, sum(c for _, _, c in rows)

    def record(self, key, status, question, doc_id=None, chars=0, charge=0, new_sentences=()):
        hk, now = _h(key), self._clock()
        entity = self._db.execute("SELECT entity FROM buyers WHERE key=?", (hk,)).fetchone()[0]
        self._db.execute("UPDATE buyers SET queries=queries+1, credits=credits-?, last_ts=? WHERE key=?",
                         (charge, now, hk))
        if doc_id and status == "ok":
            self._db.execute("INSERT OR IGNORE INTO docs_seen VALUES (?,?)", (hk, doc_id))
        for idx, n in new_sentences:
            self._db.execute("INSERT OR IGNORE INTO revealed VALUES (?,?,?,?)", (entity, doc_id, idx, n))
        self._db.execute("INSERT INTO events VALUES (?,?,?,?,?,?,?)",
                         (now, hk, status, doc_id, chars, charge, question))
        self._db.commit()

    def recent(self, n=15):
        rows = self._db.execute(
            """SELECT e.ts, COALESCE(b.name,'?'), e.status, e.doc_id, e.charge, e.question
               FROM events e LEFT JOIN buyers b ON b.key=e.key ORDER BY e.ts DESC, e.rowid DESC LIMIT ?""",
            (n,)).fetchall()
        return [dict(zip(("ts", "buyer", "status", "doc_id", "charge", "question"), r)) for r in rows]

    def seller_report(self):
        rows = self._db.execute(
            """SELECT b.name, b.queries, SUM(e.charge), COUNT(DISTINCT s.doc_id)
               FROM buyers b LEFT JOIN events e ON e.key=b.key
               LEFT JOIN docs_seen s ON s.key=b.key GROUP BY b.key""").fetchall()
        return [{"buyer": n, "queries": q, "revenue": r or 0, "distinct_docs": d} for n, q, r, d in rows]
