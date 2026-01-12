# -*- coding: utf-8 -*-
import os, json, re
import tkinter as tk
from tkinter import ttk, messagebox

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSIONS_DIR = os.path.join(BASE, "data", "versions")
DEFAULT_VERSION = "RV1909-es"

def _norm(s):
    s = (s or "").strip().lower()
    s = s.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ü","u").replace("ñ","n")
    s = re.sub(r"\s+", " ", s)
    return s

def _parse_ref(ref):
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

def load_version(version=DEFAULT_VERSION):
    path = os.path.join(VERSIONS_DIR, f"{version}.json")
    with open(path, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
    verses = data.get("verses", [])
    return verses

def build_index(verses):
    # book_name -> set(chapters)
    books = {}
    for v in verses:
        bn = v.get("book_name") or ""
        ch = int(v.get("chapter", 0) or 0)
        if not bn or ch <= 0:
            continue
        books.setdefault(bn, set()).add(ch)
    # sort
    book_list = sorted(books.keys(), key=lambda x: _norm(x))
    chapters = {b: sorted(list(books[b])) for b in book_list}
    return book_list, chapters

def passage_text(verses, book_name, ch, v1=None, v2=None):
    nb = _norm(book_name)
    out = []
    for v in verses:
        if _norm(v.get("book_name")) != nb:
            continue
        if int(v.get("chapter", 0) or 0) != int(ch):
            continue
        vv = int(v.get("verse", 0) or 0)
        if v1 is None:
            out.append((vv, v.get("text","")))
        else:
            if vv >= v1 and vv <= v2:
                out.append((vv, v.get("text","")))
    out.sort(key=lambda t: t[0])
    return out

def open_reader_gui(version=DEFAULT_VERSION, initial_ref=None, title="Biblia"):
    verses = load_version(version)
    books, chapters_map = build_index(verses)

    root = tk.Tk()
    root.title(f"{title} | Lector")
    root.geometry("1100x720")
    root.minsize(900, 600)

    top = ttk.Frame(root, padding=10)
    top.pack(fill="x")

    left = ttk.Frame(root, padding=10)
    left.pack(side="left", fill="y")

    right = ttk.Frame(root, padding=10)
    right.pack(side="right", fill="both", expand=True)

    ttk.Label(top, text=f"Versión: {version}").pack(side="left")

    ref_var = tk.StringVar(value=initial_ref or "")
    ttk.Label(top, text="Referencia").pack(side="left", padx=(20,6))
    ref_entry = ttk.Entry(top, textvariable=ref_var, width=40)
    ref_entry.pack(side="left")

    txt = tk.Text(right, wrap="word")
    txt.pack(fill="both", expand=True)

    book_var = tk.StringVar(value=(books[0] if books else ""))
    ch_var = tk.IntVar(value=1)

    ttk.Label(left, text="Libro").pack(anchor="w")
    cb_book = ttk.Combobox(left, textvariable=book_var, values=books, state="readonly", width=28)
    cb_book.pack(anchor="w", pady=(0,10))

    ttk.Label(left, text="Capítulo").pack(anchor="w")
    cb_ch = ttk.Combobox(left, textvariable=ch_var, values=(chapters_map.get(book_var.get(), [1])), state="readonly", width=10)
    cb_ch.pack(anchor="w", pady=(0,10))

    def _set_chapters_for_book():
        b = book_var.get()
        chs = chapters_map.get(b, [1])
        cb_ch["values"] = chs
        try:
            ch_var.set(chs[0])
        except Exception:
            ch_var.set(1)

    def _render(book, ch, v1=None, v2=None, header=None):
        txt.delete("1.0", "end")
        if header:
            txt.insert("end", header + "\n")
            txt.insert("end", ("=" * len(header)) + "\n\n")
        rows = passage_text(verses, book, ch, v1, v2)
        if not rows:
            txt.insert("end", "Sin resultados.\n")
            return
        for vv, t in rows:
            txt.insert("end", f"{vv}. {t}\n")

    def _read_selected():
        b = book_var.get()
        ch = int(ch_var.get())
        header = f"{b} {ch}"
        _render(b, ch, None, None, header)

    def _read_ref():
        pr = _parse_ref(ref_var.get())
        if not pr:
            messagebox.showerror("Referencia", "Formato esperado: Libro 1:1-5 (ej: Génesis 1:1-5) o Salmos 1")
            return
        book, ch, v1, v2 = pr

        # intento de match por normalización
        nb = _norm(book)
        bmatch = None
        for b in books:
            if _norm(b) == nb:
                bmatch = b
                break
        if not bmatch:
            for b in books:
                if nb in _norm(b) or _norm(b) in nb:
                    bmatch = b
                    break
        if bmatch:
            book = bmatch

        header = ref_var.get().strip()
        _render(book, ch, v1, v2, header)

        # sincroniza combos
        try:
            book_var.set(book)
            _set_chapters_for_book()
            ch_var.set(int(ch))
        except Exception:
            pass

    def _on_book_change(_evt=None):
        _set_chapters_for_book()

    cb_book.bind("<<ComboboxSelected>>", _on_book_change)

    btns = ttk.Frame(left)
    btns.pack(fill="x", pady=(12,0))

    ttk.Button(btns, text="Leer selección", command=_read_selected).pack(fill="x", pady=4)
    ttk.Button(btns, text="Leer referencia", command=_read_ref).pack(fill="x", pady=4)

    # auto: si hay referencia inicial
    if initial_ref:
        ref_var.set(initial_ref)
        _read_ref()
    else:
        if books:
            _set_chapters_for_book()
            _read_selected()

    root.mainloop()
