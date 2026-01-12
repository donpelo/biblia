# -*- coding: utf-8 -*-
import os, sys, json

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

print("ROOT:", ROOT)
print("PY:", sys.executable)

print("1) import biblia_gui")
import biblia_gui
print("OK biblia_gui")

print("2) import core modules")
from core.bible_loader import load_bible_version
from core.gui_reader import open_reader_gui
print("OK core imports, open_reader_gui:", callable(open_reader_gui))

print("3) load bible version")
idx, books = load_bible_version("RV1909-es", ROOT)
print("OK books:", len(books), "first:", books[0] if books else None)

print("4) daily calendar exists + json ok")
cal = os.path.join(ROOT, "data", "devocional_calendar.json")
assert os.path.exists(cal), "No existe devocional_calendar.json"
with open(cal, "r", encoding="utf-8-sig") as f:
    d = json.load(f)
assert isinstance(d, dict) and len(d) > 0, "Calendario vacío o inválido"
print("OK calendar keys:", len(d))

print("SMOKE E2E OK")
