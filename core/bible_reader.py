import json
import unicodedata
from pathlib import Path

def _norm(s: str) -> str:
    s = s.lower().strip()
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c))

class BibleReader:
    def __init__(self, base_dir, version="RV1909-es"):
        self.base_dir = Path(base_dir)
        self.version = version
        self.by_bcv = {}
        self.books = []
        self._load()

    def _load(self):
        p = self.base_dir / "data" / "versions" / f"{self.version}.json"
        if not p.exists():
            raise FileNotFoundError(f"No existe {p}")

        with open(p, "r", encoding="utf-8-sig") as f:
            data = json.load(f)

        verses = data.get("verses", [])
        books = {}

        for v in verses:
            b = v.get("book_name", "")
            c = int(v.get("chapter", 1))
            n = int(v.get("verse", 1))
            t = v.get("text", "").strip()

            key = (_norm(b), c, n)
            self.by_bcv[key] = t
            books[_norm(b)] = b

        self.books = sorted(books.values(), key=lambda x: _norm(x))

    def get(self, book, chapter, verse):
        key = (_norm(book), int(chapter), int(verse))
        return self.by_bcv.get(key)
