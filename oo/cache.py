import hashlib
import json
from pathlib import Path

CACHE_DIR=Path(".cache/llm")

def _key(*parts: str) -> str:
    h=hashlib.sha256()
    for p in parts:
        h.update(p.encode("utf-8"))
        h.update(b"\x00") #separator so "ab", "c" != "a", "bc"
    return h.hexdigest()

def get(*parts: str) -> dict | None:
    path=CACHE_DIR/f"{_key(*parts)}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return None

def put(value: dict, *parts: str) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    (CACHE_DIR/f"{_key(*parts)}.json").write_text(
        json.dumps(value, indent=2), encoding="utf-8"
    )