import json
import tempfile
import unittest
from pathlib import Path

from gateway import Ledger
from gateway.ingest import ingest


class IngestTests(unittest.TestCase):
    def test_folder_ingest(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "a.md").write_text("# Batch 1 failed\nSeal leaked.")
            (d / "b.txt").write_text("Plain note about yield.")
            (d / "c.json").write_text(json.dumps([{"id": "x", "title": "T", "text": "body"}]))
            (d / "bad.json").write_text("{not a list")
            (d / "pic.png").write_bytes(b"\x89PNG")
            (d / "empty.md").write_text("  \n")
            docs, skipped = ingest(d)
        self.assertEqual(sorted(x["id"] for x in docs), ["a", "b", "x"])
        self.assertEqual(next(x for x in docs if x["id"] == "a")["title"], "Batch 1 failed")
        self.assertEqual(sorted(n for n, _ in skipped), ["bad.json", "empty.md", "pic.png"])


class LedgerTests(unittest.TestCase):
    def test_keys_are_not_stored_in_plaintext(self):
        with tempfile.TemporaryDirectory() as d:
            path = str(Path(d) / "l.db")
            led = Ledger(path)
            led.add_buyer("skb_secret", "Acme", 5)
            self.assertEqual(led.buyer("skb_secret")["name"], "Acme")
            self.assertIsNone(led.buyer("skb_other"))
            self.assertNotIn(b"skb_secret", Path(path).read_bytes())

    def test_topup(self):
        led = Ledger()
        led.add_buyer("k", "Acme", 5)
        self.assertEqual(led.topup("Acme", 10), 1)
        self.assertEqual(led.buyer("k")["credits"], 15)
        self.assertEqual(led.topup("Nobody", 10), 0)


if __name__ == "__main__":
    unittest.main()
