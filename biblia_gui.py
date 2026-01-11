# BOOT_LOG (auto)
import traceback as _traceback
import datetime as _dt
def _boot_log(msg: str):
    try:
        import os as _os
        p = _os.path.join(_os.path.dirname(__file__), "logs")
        _os.makedirs(p, exist_ok=True)
        f = _os.path.join(p, "boot.log")
        with open(f, "a", encoding="utf-8") as _h:
            _h.write(f"[{_dt.datetime.now().isoformat(timespec='seconds')}] {msg}\n")
    except Exception:
        pass
_boot_log("START biblia_gui.py")
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
from core.bible_reader import BibleReader
import os
import json
from core.bible_loader import load_bible_json, get_verse


APP_TITLE   = "Biblia"
APP_VERSION = "v1.0"
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))

def _version_path(version_id: str) -> str:
    return os.path.join(BASE_DIR, "data", "versions", f"{version_id}.json")

def load_bible(version_id: str):
    path = _version_path(version_id)
    idx, order = load_bible_json(path)
    return idx, order, path


SETTINGS_PATH = os.path.join(BASE_DIR, "config", "gui_settings.json")

DEFAULTS = {
    "bible_version": "RVR1960",
    "tts_rate": 180,
    "tts_voice": "",
    "daily_ref": "Romanos 8:28",
    "daily_title": "Propósito",
    "daily_note": ""
}

def _safe_int(v, fallback):
    try:
        return int(v)
    except Exception:
        return fallback

def load_settings():
    s = dict(DEFAULTS)
    try:
        if os.path.exists(SETTINGS_PATH):
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                s.update({k: data.get(k, s[k]) for k in s.keys()})
    except Exception:
        pass
    s["tts_rate"] = _safe_int(s.get("tts_rate", DEFAULTS["tts_rate"]), DEFAULTS["tts_rate"])
    return s

def save_settings(s: dict):
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(s, f, ensure_ascii=False, indent=2)

def launch_python(relpath, cwd=BASE_DIR, extra_args=None):
    extra_args = extra_args or []
    target = os.path.join(BASE_DIR, relpath)
    if not os.path.exists(target):
        raise FileNotFoundError(target)
    subprocess.Popen([sys.executable, target] + extra_args, cwd=cwd)

class BibliaMenu(tk.Tk):
    def about(self):
        try:
            from tkinter import messagebox
            ver = getattr(self, 'bible_version', 'N/A')
            messagebox.showinfo('Acerca de', 'Biblia GUI\\nVersión: {0}\\nRepositorio: donpelo/biblia'.format(ver))
        except Exception as e:
            try:
                print('[WARN] about() failed: {0}'.format(e))
            except Exception:
                pass

    def write_safe(self, msg: str):
        # Fallback seguro: no depende de widgets ya creados
        try:
            target = None
            for name in ("log", "out_text", "main_text", "reader_text"):
                if hasattr(self, name):
                    target = getattr(self, name)
                    break
            if target is not None:
                try:
                    target.insert("end", msg)
                    return
                except Exception:
                    pass
        except Exception:
            pass
        try:
            print(msg, end="")
        except Exception:
            pass
        def about(self):
            try:
                from tkinter import messagebox
                ver = getattr(self, "bible_version", "N/A")
                messagebox.showinfo("Acerca de", f"Biblia GUI\nVersión: {ver}\n")
            except Exception as e:
                try:
                    print(f"[WARN] about() failed: {e}")
                except Exception:
                    pass
    def __init__(self):
        super().__init__()

        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self._log_buffer = []  # buffer para mensajes antes de crear el widget log
        self.settings = load_settings()
        
        self.bible_version = getattr(self, "bible_version", None) or "RV1909-es"
        try:
            self.bible_idx, self.books_order, self.bible_path = load_bible(self.bible_version)
            self.write(f"Versión: {self.bible_version}\n")
            self.write(f"Biblia cargada OK ({len(self.books_order)} libros)\n")
        except Exception as e:
            self.bible_idx = {}
            self.books_order = []
            self.bible_path = ""
            self.write("[ERROR] No se pudo cargar la Biblia\n")
            self.write(f"Versión: {self.bible_version}\n")
            self.write(f"Ruta esperada: {_version_path(self.bible_version)}\n")
            self.write(f"Detalle: {e}\n")


        self.title(f"{APP_TITLE} {APP_VERSION}")
        self.geometry("1200x720")
        self.minsize(1000, 600)

        root = ttk.Frame(self, padding=10)
        root.pack(fill="both", expand=True)

        left = ttk.LabelFrame(root, text="Acciones", padding=10)
        left.pack(side="left", fill="y", padx=(0,10))

        right = ttk.LabelFrame(root, text="Estado", padding=10)
        right.pack(side="right", fill="both", expand=True)

        self.log = tk.Text(right, height=25, wrap="word")

        # --- BOOTSTRAP (auto) ---

        import os as _os

        if not hasattr(self, 'base_dir'):

            try:

                self.base_dir = _os.path.dirname(__file__)

            except Exception:

                self.base_dir = _os.getcwd()


        if not hasattr(self, 'write_safe'):

            def write_safe(msg: str):

                try:

                    print(msg, end='')

                except Exception:

                    pass

            self.write_safe = write_safe


        if (not hasattr(self, 'about')) and hasattr(self, '_about'):

            self.about = self._about

        # --- END BOOTSTRAP ---

        self._load_bible_active()
        if getattr(self, "reader", None) is not None and getattr(self.reader, "books", None):
            self.reader_book['values'] = (self.reader.books if self.reader else [])
        else:
            try:
                self.reader_book['values'] = []
            except Exception:
                pass
        self.log.pack(fill="both", expand=True)

        # --- BOOTSTRAP (auto) ---

        import os as _os

        if not hasattr(self, 'base_dir'):

            try:

                self.base_dir = _os.path.dirname(__file__)

            except Exception:

                self.base_dir = _os.getcwd()


        if not hasattr(self, 'write_safe'):

            def write_safe(msg: str):

                try:

                    print(msg, end='')

                except Exception:

                    pass

            self.write_safe = write_safe


        if (not hasattr(self, 'about')) and hasattr(self, '_about'):

            self.about = self._about

        # --- END BOOTSTRAP ---

        self._load_bible_active()
        if getattr(self, "reader", None) is not None and getattr(self.reader, "books", None):
            self.reader_book['values'] = self.reader.books
        else:
            try:
                self.reader_book['values'] = []
            except Exception:
                pass
        # flush buffer a widget log
        try:
            if hasattr(self, "_log_buffer") and self._log_buffer:
                for _s in self._log_buffer:
                    self.log.insert("end", _s)
                self.log.see("end")
                self._log_buffer = []
        except Exception:
            pass
        top = ttk.Frame(root)
        top.place(relx=1.0, rely=0.0, anchor="ne")
        ttk.Button(top, text="Acerca de", command=self.about).pack()

        def btn(txt, cmd):
            b = ttk.Button(left, text=txt, command=cmd)
            b.pack(fill="x", pady=6)
            return b

        # Consola (módulos reales en /modules)
        btn("📖 Lector bíblico (consola)", lambda: self.launch_console("modules/lector_biblia.py", "Ejecutando: Lector Biblia"))
        btn("🔎 Buscador (consola)",      lambda: self.launch_console("modules/buscador.py", "Ejecutando: Buscador"))
        btn("📅 Planes de lectura (consola)", lambda: self.launch_console("modules/planes.py", "Ejecutando: Planes de lectura"))
        btn("📝 Notas y marcadores (consola)", lambda: self.launch_console("modules/notas_marcadores.py", "Ejecutando: Notas y marcadores"))
        btn("🔊 Audio Biblia TTS (consola)", lambda: self.launch_console("modules/audio_biblia.py", "Ejecutando: Audio Biblia"))

        # Lectura del día (NO abre el GUI azul)
        self.daily_btn = btn(self._daily_label(), self.open_daily)

        # Config del launcher
        btn("⚙️ Configuración", self.open_settings)

        ttk.Separator(left).pack(fill="x", pady=10)

        # GUI azul (uno solo)
        btn("🖥️ Abrir BibliaInteractiva (GUI)", lambda: self.launch_gui("gui/main.py", "Ejecutando: gui/main.py"))

        ttk.Separator(left).pack(fill="x", pady=10)
        btn("Salir", self.quit)

        self.write(
            "Listo. Selecciona un módulo.\n"
            f"Python: {sys.executable}\n"
            f"Ruta: {BASE_DIR}\n"
            f"Lectura del día: {self.settings.get('daily_ref','')}\n"
            "Menú cargado.\n"
        )

    def _daily_label(self):
        ref = self.settings.get("daily_ref", DEFAULTS["daily_ref"])
        return f"📌 Lectura del día: {ref}"
    def write(self, s):
        # seguro si self.log aún no existe
        if not hasattr(self, "log") or self.log is None:
            try:
                print(s, end="")
            except Exception:
                pass
            return
        try:
            self.log.insert("end", s)
            self.log.see("end")
        except Exception:
            try:
                print(s, end="")
            except Exception:
                pass

    def on_reader_go(self):
        try:
            book = self.book_var.get()
            chap = self.chapter_var.get()
            verse = self.verse_var.get()
            text = self.reader.get(book, chap, verse)

            if not text:
                self.write_safe(f"[WARN] No encontrado: {book} {chap}:{verse}\n")
                return

            out = f"{book} {chap}:{verse}\n\n{text}\n"
            self.write_safe(out)
            self.current_text = text

        except Exception as e:
            self.write_safe(f"[ERROR] Lector: {e}\n")

    def _version_path(self, version_name: str) -> str:
        # data/versions/<version>.json
        import os
        return os.path.join(self.base_dir, "data", "versions", f"{version_name}.json")

    def _load_bible_active(self):
        """
        Loader determinista:
        - carga RVxxxx-es desde data/versions
        - BOM-safe lo maneja BibleReader (utf-8-sig)
        """
        try:
            vp = self._version_path(self.bible_version)
            self.reader = BibleReader(vp)

            # popular UI si existen widgets
            # libros: lista de nombres
            if hasattr(self, "book_cb") and self.book_cb is not None:
                try:
                    self.book_cb["values"] = self.reader.books
                    if self.reader.books:
                        self.book_cb.set(self.reader.books[0])
                except Exception:
                    pass

            self.write_safe(f"Biblia: OK ({len(self.reader.by_bcv)} versículos)\\n")
        except Exception as e:
            self.reader = None
            self.write_safe(f"[ERROR] Loader Biblia: {e}\\n")




# END_OF_FILE
_boot_log('EOF_REACHED')
# === ENTRYPOINT_MINIMAL_FIX ===
def _ensure_logs_dir():
    try:
        import os as _os
        _p = _os.path.join(_os.path.dirname(__file__), "logs")
        _os.makedirs(_p, exist_ok=True)
        return _p
    except Exception:
        return None

def _boot_log2(msg: str):
    try:
        import os as _os
        import datetime as _dt
        _p = _ensure_logs_dir()
        if not _p:
            return
        _f = _os.path.join(_p, "boot.log")
        with open(_f, "a", encoding="utf-8") as _h:
            _h.write(f"[{_dt.datetime.now().isoformat(timespec='seconds')}] {msg}\n")
    except Exception:
        pass

def _run_gui_entrypoint():
    _boot_log2("ENTRYPOINT: start")
    try:
        cls = globals().get("BibliaMenu", None)
        _boot_log2("ENTRYPOINT: BibliaMenu=" + ("OK" if cls else "MISSING"))
        if cls is None:
            return  # no podemos arrancar si no existe la clase

        app = cls()
        _boot_log2("ENTRYPOINT: instance created")
        try:
            app.mainloop()
            _boot_log2("ENTRYPOINT: mainloop returned")
        except Exception as e:
            _boot_log2("FATAL: mainloop error: " + repr(e))
            raise
    except Exception as e:
        try:
            import traceback as _tb
            _boot_log2("FATAL: entrypoint exception: " + repr(e))
            _boot_log2(_tb.format_exc())
        except Exception:
            pass
        raise

if __name__ == "__main__":
    _run_gui_entrypoint()
# === END ENTRYPOINT_MINIMAL_FIX ===




