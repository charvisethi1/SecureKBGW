"""Turn a seller's folder of notes into the knowledge-base JSON the gateway serves."""
import json
from pathlib import Path

MAX_BYTES = 200_000  # per file; longer files should be split by the seller
EXTS = {".md", ".txt", ".json"}


def _title(text, fallback):
    for line in text.splitlines():
        line = line.strip().lstrip("#").strip()
        if line:
            return line[:120]
    return fallback


def ingest(folder):
    """Return (docs, skipped). .md/.txt become one doc per file; .json may hold a list of
    {id, title, text}. Anything else, empty or oversized is reported in `skipped`."""
    docs, skipped = [], []
    for path in sorted(Path(folder).rglob("*")):
        if not path.is_file() or path.name.startswith("."):
            continue
        if path.suffix.lower() not in EXTS:
            skipped.append((path.name, "unsupported type"))
            continue
        if path.stat().st_size > MAX_BYTES:
            skipped.append((path.name, "file too large, split it"))
            continue
        raw = path.read_text(errors="replace")
        if path.suffix.lower() == ".json":
            try:
                items = json.loads(raw)
                docs += [{"id": str(i["id"]), "title": str(i["title"]), "text": str(i["text"])} for i in items]
            except (ValueError, KeyError, TypeError):
                skipped.append((path.name, "json must be a list of {id, title, text}"))
        elif raw.strip():
            docs.append({"id": path.stem, "title": _title(raw, path.stem), "text": raw.strip()})
        else:
            skipped.append((path.name, "empty"))
    return docs, skipped
