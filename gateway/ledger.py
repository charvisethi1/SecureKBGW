"""Buyer accounts, credit metering and an audit log (SQLite, stdlib)."""
import sqlite3
import time


class Ledger:
    def __init__(self, path=":memory:", clock=time.time):
        self._clock = clock
        self._db = sqlite3.connect(path, check_same_thread=False)  # callers serialize via Gateway's lock
        self._db.executescript(
            """
            CREATE TABLE IF NOT EXISTS buyers (
                key TEXT PRIMARY KEY, name TEXT, credits INTEGER, queries INTEGER DEFAULT 0,
                last_ts REAL DEFAULT 0);
            CREATE TABLE IF NOT EXISTS docs_seen (key TEXT, doc_id TEXT, PRIMARY KEY (key, doc_id));
            CREATE TABLE IF NOT EXISTS events (
                ts REAL, key TEXT, status TEXT, doc_id TEXT, chars INTEGER, charge INTEGER, question TEXT);
            """
        )

    def add_buyer(self, key, name, credits):
        self._db.execute("INSERT OR REPLACE INTO buyers (key, name, credits) VALUES (?,?,?)",
                         (key, name, credits))
        self._db.commit()

    def buyer(self, key):
        row = self._db.execute(
            "SELECT name, credits, queries, last_ts FROM buyers WHERE key=?", (key,)).fetchone()
        return None if row is None else dict(zip(("name", "credits", "queries", "last_ts"), row))

    def docs_seen(self, key):
        return {r[0] for r in self._db.execute("SELECT doc_id FROM docs_seen WHERE key=?", (key,))}

    def record(self, key, status, question, doc_id=None, chars=0, charge=0):
        now = self._clock()
        self._db.execute("UPDATE buyers SET queries=queries+1, credits=credits-?, last_ts=? WHERE key=?",
                         (charge, now, key))
        if doc_id and status == "ok":
            self._db.execute("INSERT OR IGNORE INTO docs_seen VALUES (?,?)", (key, doc_id))
        self._db.execute("INSERT INTO events VALUES (?,?,?,?,?,?,?)",
                         (now, key, status, doc_id, chars, charge, question))
        self._db.commit()

    def seller_report(self):
        rows = self._db.execute(
            """SELECT b.name, b.queries, SUM(e.charge), COUNT(DISTINCT s.doc_id)
               FROM buyers b LEFT JOIN events e ON e.key=b.key
               LEFT JOIN docs_seen s ON s.key=b.key GROUP BY b.key""").fetchall()
        return [{"buyer": n, "queries": q, "revenue": r or 0, "distinct_docs": d} for n, q, r, d in rows]
