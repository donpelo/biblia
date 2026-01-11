# -*- coding: utf-8 -*-
import os, json, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSIONS_DIR = os.path.join(BASE, "data", "versions")

DEFAULT_VERSION = "RV1909-es"

def load_version(version=DEFAULT_VERSION):
    path = os.path.join(VERSIONS_DIR, f"{version}.json")
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    with open(path, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
    verses = data.get("verses", [])
    return verses

def books_index(verses):
    # returns: dict normalized_book -> display_book_name
    m = {}
    for v in verses:
        bn = v.get("book_name") or ""
        key = normalize_book(bn)
        if key and key not in m:
            m[key] = bn
    return m

def normalize_book(s):
    s = (s or "").strip().lower()
    s = s.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ü","u").replace("ñ","n")
    s = re.sub(r"\s+", " ", s)
    return s

def parse_ref(ref):
    # "Génesis 1:1-5" or "Salmos 1" or "Juan 1:1-14"
    ref = (ref or "").strip()
    if not ref:
        return None

    m = re.match(r"^(?P<book>.+?)\s+(?P<ch>\d+)(?::(?P<v1>\d+)(?:-(?P<v2>\d+))?)?\s*$", ref)
    if not m:
        return None

    book = m.group("book").strip()
    ch = int(m.group("ch"))
    v1 = m.group("v1")
    v2 = m.group("v2")
    if v1 is None:
        return (book, ch, None, None)
    v1 = int(v1)
    v2 = int(v2) if v2 else v1
    return (book, ch, v1, v2)

def filter_passage(verses, book, ch, v1=None, v2=None):
    nb = normalize_book(book)
    out = []
    for v in verses:
        if normalize_book(v.get("book_name")) != nb:
            continue
        if int(v.get("chapter", 0)) != int(ch):
            continue
        if v1 is None:
            out.append(v)
        else:
            vv = int(v.get("verse", 0))
            if vv >= v1 and vv <= v2:
                out.append(v)
    return out

def main():
    version = os.environ.get("BIBLIA_VERSION") or DEFAULT_VERSION
    verses = load_version(version)
    bmap = books_index(verses)

    ref = os.environ.get("BIBLIA_REF", "").strip()

    if not ref:
        print("Biblia CLI Reader")
        print(f"Version: {version}")
        print("Ejemplo ref: Génesis 1:1-5")
        ref = input("Referencia: ").strip()

    pr = parse_ref(ref)
    if not pr:
        print("No pude parsear la referencia:", ref)
        sys.exit(2)

    book, ch, v1, v2 = pr

    # intentar corregir book con índice si hay variaciones
    nb = normalize_book(book)
    if nb not in bmap:
        # match parcial
        for k, disp in bmap.items():
            if nb in k or k in nb:
                book = disp
                nb = k
                break

    passage = filter_passage(verses, book, ch, v1, v2)

    print("")
    head = ref
    print(head)
    print("=" * len(head))

    if not passage:
        print("Sin resultados.")
        sys.exit(1)

    for v in passage:
        vv = v.get("verse")
        tx = v.get("text", "")
        print(f"{vv}. {tx}")

if __name__ == "__main__":
    main()
