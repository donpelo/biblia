# -*- coding: utf-8 -*-
import json
import os
from typing import Dict, Tuple, List, Any, Optional

VerseIndex = Dict[str, Dict[int, Dict[int, str]]]

# --- API estable (auto) ---
def _repo_root(base_dir=None):
    import os
    if base_dir:
        return base_dir
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def version_json_path(version_name, base_dir=None):
    import os
    root = _repo_root(base_dir)
    return os.path.join(root, "data", "versions", f"{version_name}.json")

def load_bible_version(version_name="RV1909-es", base_dir=None):
    """
    Carga una versión por nombre, por ejemplo: RV1909-es
    Retorna el dict JSON listo para BibleReader.
    """
    p = version_json_path(version_name, base_dir)
    return load_bible_json(p)
# --- END API estable ---

def _to_int(x) -> Optional[int]:
    try:
        return int(str(x).strip())
    except Exception:
        return None


def _add_verse(idx: VerseIndex, book: str, chap: int, verse: int, text: str):
    book = str(book).strip()
    if not book:
        return
    if chap <= 0 or verse <= 0:
        return
    text = (text or "").strip()
    if not text:
        return
    idx.setdefault(book, {}).setdefault(chap, {})[verse] = text


def _index_from_book_chapter_dict(data: Any) -> VerseIndex:
    # Formato típico:
    # { "Génesis": { "1": { "1": "texto", "2": "texto" }, "2": {...} }, "Éxodo": {...} }
    idx: VerseIndex = {}
    if not isinstance(data, dict):
        return idx
    for book, chapters in data.items():
        if not isinstance(chapters, dict):
            continue
        for ckey, verses in chapters.items():
            chap = _to_int(ckey)
            if chap is None:
                continue
            # verses puede ser dict { "1": "text" } o lista
            if isinstance(verses, dict):
                for vkey, text in verses.items():
                    ver = _to_int(vkey)
                    if ver is None:
                        continue
                    _add_verse(idx, book, chap, ver, str(text))
            elif isinstance(verses, list):
                # ["texto v1","texto v2"...] o [{"verse":1,"text":".."}]
                for i, item in enumerate(verses, start=1):
                    if isinstance(item, dict):
                        ver = _to_int(item.get("verse") or item.get("v") or i) or i
                        text = item.get("text") or item.get("t") or item.get("content") or ""
                        _add_verse(idx, book, chap, ver, str(text))
                    else:
                        _add_verse(idx, book, chap, i, str(item))
    return idx


def _index_from_books_list(data: Any) -> VerseIndex:
    # Formatos:
    # { "books":[{"name":"Génesis","chapters":[["v1","v2"], ...]}] }
    # o {"books":[{"book":"Genesis","chapters":{"1":{"1":"..."}}}]}
    idx: VerseIndex = {}
    if not isinstance(data, dict):
        return idx
    books = data.get("books") or data.get("Books") or data.get("bible") or data.get("Bible")
    if not isinstance(books, list):
        return idx
    for b in books:
        if not isinstance(b, dict):
            continue
        book = b.get("name") or b.get("book") or b.get("title") or b.get("id")
        if not book:
            continue
        ch = b.get("chapters") or b.get("Chapters")
        # chapters puede ser list, dict, etc.
        if isinstance(ch, dict):
            # {"1":{"1":"text"}}
            for ckey, verses in ch.items():
                chap = _to_int(ckey)
                if chap is None:
                    continue
                if isinstance(verses, dict):
                    for vkey, text in verses.items():
                        ver = _to_int(vkey)
                        if ver is None:
                            continue
                        _add_verse(idx, book, chap, ver, str(text))
                elif isinstance(verses, list):
                    for i, item in enumerate(verses, start=1):
                        _add_verse(idx, book, chap, i, str(item))
        elif isinstance(ch, list):
            # [["v1","v2"], ["v1","v2"]]
            for ci, verses in enumerate(ch, start=1):
                if isinstance(verses, list):
                    for vi, text in enumerate(verses, start=1):
                        _add_verse(idx, book, ci, vi, str(text))
                elif isinstance(verses, dict):
                    for vkey, text in verses.items():
                        ver = _to_int(vkey)
                        if ver is None:
                            continue
                        _add_verse(idx, book, ci, ver, str(text))
    return idx


def _index_from_verses_flat(data: Any) -> VerseIndex:
    # Formato flat:
    # { "verses":[{"book":"Romanos","chapter":8,"verse":28,"text":"..."}] }
    idx: VerseIndex = {}
    if not isinstance(data, dict):
        return idx
    verses = data.get("verses") or data.get("Verses") or data.get("items") or data.get("data")
    if not isinstance(verses, list):
        return idx
    for it in verses:
        if not isinstance(it, dict):
            continue
        book = it.get("book") or it.get("book_name") or it.get("b")
        chap = _to_int(it.get("chapter") or it.get("c"))
        ver  = _to_int(it.get("verse") or it.get("v"))
        text = it.get("text") or it.get("t") or it.get("content") or ""
        if book and chap and ver:
            _add_verse(idx, book, chap, ver, str(text))
    return idx


def load_bible_json(path: str) -> Tuple[VerseIndex, List[str]]:
    """
    Devuelve:
      idx[book][chapter][verse] = text
      ordered_books = lista de libros en orden (si se pudo inferir)
    """
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    with open(path, "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    # Intento 1: dict libro -> capítulos
    idx = _index_from_book_chapter_dict(data)

    # Intento 2: contenedor con lista de libros
    if not idx:
        idx = _index_from_books_list(data)

    # Intento 3: lista flat de versos
    if not idx:
        idx = _index_from_verses_flat(data)

    ordered_books = list(idx.keys())

    # Si hay metadata/books.json, úsala para ordenar cuando coincida
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        meta = os.path.join(base_dir, "data", "metadata", "books.json")
        if os.path.exists(meta):
            with open(meta, "r", encoding="utf-8-sig") as f:
                books_meta = json.load(f)
            # books_meta esperado: lista de libros con name/es/en o dict
            order = []
            if isinstance(books_meta, list):
                for b in books_meta:
                    if isinstance(b, dict):
                        nm = b.get("name") or b.get("es") or b.get("title")
                        if nm and nm in idx:
                            order.append(nm)
            elif isinstance(books_meta, dict):
                # {"books":[...]}
                bl = books_meta.get("books")
                if isinstance(bl, list):
                    for b in bl:
                        if isinstance(b, dict):
                            nm = b.get("name") or b.get("es") or b.get("title")
                            if nm and nm in idx:
                                order.append(nm)
            if order:
                ordered_books = order
    except Exception:
        pass

    return idx, ordered_books


def get_verse(idx: VerseIndex, book: str, chapter: int, verse: int) -> str:
    return idx.get(book, {}).get(int(chapter), {}).get(int(verse), "")

