import json
import os
import re
from typing import Optional, Dict, Tuple, List

def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip().lower())

def _read_json_smart(path: str) -> dict:
    # Lee bytes y decide decode correcto.
    # Caso actual: JSON con BOM y/o texto con encoding legacy (cp1252) que al decodificar como utf-8 queda mojibake.
    raw = open(path, "rb").read()

    # Strip BOM utf-8 si existe
    if raw.startswith(b"\xef\xbb\xbf"):
        raw_wo_bom = raw[3:]
    else:
        raw_wo_bom = raw

    # 1) intentar utf-8 (contenido suele venir así)
    try:
        s_utf8 = raw_wo_bom.decode("utf-8")
        data_utf8 = json.loads(s_utf8)
    except Exception:
        s_cp = raw_wo_bom.decode("cp1252", errors="replace")
        return json.loads(s_cp)

    # Heurística de mojibake común
    # Si aparecen patrones típicos, preferimos cp1252
    def looks_mojibake(obj: dict) -> bool:
        try:
            verses = obj.get("verses", [])
            if not verses:
                return False
            sample = verses[0]
            t = ""
            b = ""
            if isinstance(sample, dict):
                t = str(sample.get("text", ""))
                b = str(sample.get("book_name", ""))
            bad = ("Ã" in t) or ("Ã" in b) or ("¾" in t) or ("�" in t) or ("Â" in t) or ("Ú" in b and "G" in b)
            return bad
        except Exception:
            return False

    if looks_mojibake(data_utf8):
        try:
            s_cp = raw_wo_bom.decode("cp1252", errors="replace")
            return json.loads(s_cp)
        except Exception:
            return data_utf8

    return data_utf8

class BibleReader:
    def __init__(self, base_dir: str=None, version: str="RV1909-es"):
        import os
        # Auto-detect repo root si no se pasa base_dir
        if base_dir is None:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

        self.base_dir = base_dir
        self.version = version
        self.by_bcv: Dict[Tuple[str, int, int], str] = {}
        self.books: List[str] = []
        self._load()
    def _version_path(self) -> str:
        return os.path.join(self.base_dir, "data", "versions", f"{self.version}.json")

    def _load(self) -> None:
        p = self._version_path()
        data = _read_json_smart(p)

        verses = data.get("verses", [])
        books_map: Dict[str, str] = {}

        for v in verses:
            if not isinstance(v, dict):
                continue
            bname = str(v.get("book_name", "")).strip()
            chap = int(v.get("chapter", 0) or 0)
            ver = int(v.get("verse", 0) or 0)
            txt = str(v.get("text", "")).strip()

            if not bname or chap <= 0 or ver <= 0:
                continue

            key = (_norm(bname), chap, ver)
            self.by_bcv[key] = txt
            books_map[_norm(bname)] = bname

        self.books = sorted(books_map.values(), key=lambda x: _norm(x))

    def get(self, book: str, chapter: int, verse: int) -> Optional[str]:
        key = (_norm(book), int(chapter), int(verse))
        return self.by_bcv.get(key)

