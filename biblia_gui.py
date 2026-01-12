# -*- coding: utf-8 -*-
import os, sys, json, subprocess, traceback
import tkinter as tk
from tkinter import ttk, messagebox

APP_TITLE = "Biblia"
APP_VERSION = "v1.0"

def _now():
    import datetime
    return datetime.datetime.now().isoformat(timespec="seconds")

def _ensure_dir(p):
    os.makedirs(p, exist_ok=True)
    return p

def _log_boot(msg):
    try:
        _ensure_dir(os.path.join(os.getcwd(), "logs"))
        with open(os.path.join(os.getcwd(), "logs", "boot.log"), "a", encoding="utf-8") as f:
            f.write(f"[{_now()}] {msg}\n")
    except Exception:
        pass

class BibliaStore:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.version = "RV1909-es"
        self.meta_books = None
        self.verses = None

    def version_path(self, version_name):
        return os.path.join(self.base_dir, "data", "versions", f"{version_name}.json")

    def books_meta_path(self):
        return os.path.join(self.base_dir, "data", "metadata", "books.json")

    def load_books_meta(self):
        p = self.books_meta_path()
        if not os.path.exists(p):
            return None
        with open(p, "r", encoding="utf-8-sig") as f:
            return json.load(f)

    def load_version(self, version_name):
        p = self.version_path(version_name)
        if not os.path.exists(p):
            raise FileNotFoundError(p)

        # BOM-safe
        with open(p, "r", encoding="utf-8-sig") as f:
            data = json.load(f)

        # Esperado: { metadata:..., verses:[...] }
        if isinstance(data, dict) and "verses" in data:
            verses = data.get("verses")
        else:
            verses = None

        if not isinstance(verses, list) or not verses:
            raise ValueError("JSON de Biblia no trae 'verses' como lista con contenido")

        self.version = version_name
        self.verses = verses
        self.meta_books = self.load_books_meta()
        return True

    def find_by_ref(self, book_name=None, book_num=None, chapter=None, verse=None):
        if not self.verses:
            return None
        for v in self.verses:
            try:
                if book_num is not None and int(v.get("book")) != int(book_num):
                    continue
                if book_name is not None and str(v.get("book_name","")).strip().lower() != str(book_name).strip().lower():
                    continue
                if chapter is not None and int(v.get("chapter")) != int(chapter):
                    continue
                if verse is not None and int(v.get("verse")) != int(verse):
                    continue
                return v
            except Exception:
                continue
        return None

    def pick_daily_ref(self):
        # Estrategia simple: lee devocional_calendar.json si existe con clave "MM-DD"
        from datetime import date
        mmdd = date.today().strftime("%m-%d")
        cal = os.path.join(self.base_dir, "data", "devocional_calendar.json")
        if os.path.exists(cal):
            try:
                with open(cal, "r", encoding="utf-8-sig") as f:
                    data = json.load(f)
                # soporta {"01-11":"Juan 3:16"} u objetos
                v = data.get(mmdd)
                if isinstance(v, str) and v.strip():
                    return v.strip()
                if isinstance(v, dict):
                    for key in ("ref","reference","verse","text"):
                        if isinstance(v.get(key), str) and v.get(key).strip():
                            return v.get(key).strip()
            except Exception:
                pass

        # Fallback determinista: Génesis 1:1 + día del mes como versículo si existe
        d = date.today().day
        return f"Genesis 1:{d}"

    def parse_ref(self, ref):
        # Acepta "Juan 3:16" o "Genesis 1:1"
        try:
            s = ref.strip()
            if ":" not in s:
                return None
            left, vv = s.rsplit(":", 1)
            vv = int(vv.strip())
            parts = left.strip().split()
            ch = int(parts[-1])
            book = " ".join(parts[:-1])
            return book, ch, vv
        except Exception:
            return None

class BibliaMenu(tk.Tk):
    def launch_reader_gui(self, ref: str = ""):
        try:
            from core.gui_reader import open_reader_gui
            version = getattr(self, "bible_version", "RV1909-es")
            open_reader_gui(
                version=version,
                initial_ref=(ref or ""),
                title="Biblia"
            )
        except Exception as e:
            try:
                self.write_safe("[ERROR] launch_reader_gui: " + str(e) + "\n")
            except Exception:
                pass

    def __init__(self):
        super().__init__()
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.cfg_path = os.path.join(self.base_dir, "data", "config.json")
        self.cfg = self._cfg_load()

        self.ui_lang = self.cfg.get("ui_lang","es")
        self.bible_version = self.cfg.get("bible_version","RV1909-es")

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
        self.log.pack(fill="both", expand=True)

        top = ttk.Frame(root)
        top.place(relx=1.0, rely=0.0, anchor="ne")
        ttk.Button(top, text="Acerca de", command=self.about).pack()

        def btn(txt, cmd):
            b = ttk.Button(left, text=txt, command=cmd)
            b.pack(fill="x", pady=6)
            return b

        # Store Biblia
        self.store = BibliaStore(self.base_dir)

        self.write_safe(f"Ruta: {self.base_dir}\n")
        self.write_safe(f"Python: {sys.executable}\n")
        self.write_safe(f"Versión Biblia: {self.bible_version}\n")
        self.write_safe(f"UI Lang: {self.ui_lang}\n\n")

        # Cargar Biblia al inicio (pero sin matar la app si falla)
        self._load_bible_or_warn()

        # Botones (todos con métodos reales)
        btn("📖 Leer Biblia (GUI)", lambda: self.launch_reader_gui(""))
        btn("📖 Lector bíblico (GUI)", self._open_reader_gui_action)
        btn("🔎 Buscador (consola)",      lambda: self.launch_console("modules/buscador.py", "Ejecutando: Buscador"))
        btn("📅 Planes de lectura (consola)", lambda: self.launch_console("modules/planes.py", "Ejecutando: Planes de lectura"))
        btn("📝 Notas y marcadores (consola)", lambda: self.launch_console("modules/notas_marcadores.py", "Ejecutando: Notas y marcadores"))
        btn("🔊 Audio Biblia TTS (consola)", lambda: self.launch_console("modules/audio_biblia.py", "Ejecutando: Audio Biblia TTS"))

        btn(self._daily_label(), self.open_daily)
        btn("⚙️ Configuración", self.open_settings)

        btn("🖥️ Abrir BibliaInteractiva (GUI)", lambda: self.launch_gui("gui/main.py", "Ejecutando: BibliaInteractiva GUI"))

        ttk.Separator(left, orient="horizontal").pack(fill="x", pady=8)
        self._btn_exit = btn("Salir", self._on_exit)
        try:
            self._btn_exit.bind("<ButtonRelease-1>", self._on_exit)
        except Exception:
            pass

        self.write_safe("\nMenú cargado.\n")

    def _on_exit(self, *_):
        try:
            # intentar cerrar limpio
            try:
                self.write_safe('[INFO] Salir solicitado\\n') if hasattr(self,'write_safe') else None
            except Exception:
                pass
            try:
                self.quit()
            except Exception:
                pass
            try:
                self.destroy()
            except Exception:
                pass
        except Exception:
            pass

    def write_safe(self, s):
        try:
            self.log.insert("end", s)
            self.log.see("end")
        except Exception:
            try:
                print(s, end="")
            except Exception:
                pass

    def _cfg_load(self):
        try:
            if os.path.exists(self.cfg_path):
                with open(self.cfg_path, "r", encoding="utf-8-sig") as f:
                    d = json.load(f)
                    if isinstance(d, dict):
                        return d
        except Exception:
            pass
        return {}

    def _cfg_save(self, d):
        try:
            os.makedirs(os.path.dirname(self.cfg_path), exist_ok=True)
            with open(self.cfg_path, "w", encoding="utf-8") as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
            self.cfg = d
            return True
        except Exception as e:
            self.write_safe(f"[ERROR] No pude guardar config: {e}\n")
            return False

    def _load_bible_or_warn(self):
        try:
            self.store.load_version(self.bible_version)
            self.write_safe(f"Biblia cargada OK ({len(self.store.verses)} versos)\n")
        except Exception as e:
            self.write_safe(f"[ERROR] Loader Biblia: {e}\n")
            self.write_safe("La app igual abre. Revisa que exista data/versions/<version>.json\n\n")

    def _daily_label(self):
        return "📆 Lectura del día"

    def about(self):
        messagebox.showinfo(APP_TITLE, f"{APP_TITLE} {APP_VERSION}\nRepositorio: donpelo/biblia")

    def launch_console(self, relpath, msg):
        self.write_safe(msg + "\n")
        target = os.path.join(self.base_dir, relpath)
        if not os.path.exists(target):
            self.write_safe(f"[ERROR] No existe: {relpath}\n")
            messagebox.showerror(APP_TITLE, f"No existe:\n{target}")
            return
        # Consola nueva
        try:
            subprocess.Popen([sys.executable, target], cwd=self.base_dir, creationflags=subprocess.CREATE_NEW_CONSOLE)
        except Exception:
            subprocess.Popen([sys.executable, target], cwd=self.base_dir)

    def launch_gui(self, relpath, msg):
        self.write_safe(msg + "\n")
        target = os.path.join(self.base_dir, relpath)
        if not os.path.exists(target):
            self.write_safe(f"[ERROR] No existe: {relpath}\n")
            messagebox.showerror(APP_TITLE, f"No existe:\n{target}")
            return
        subprocess.Popen([sys.executable, target], cwd=self.base_dir)

    def _open_reader_gui_action(self):
        """
        Abre el lector GUI en un proceso separado para evitar conflictos de Tk (Tk() doble / mainloop).
        Loggea traceback completo si falla.
        """
        try:
            import os, sys, subprocess, traceback
            ver = getattr(self, "bible_version", "RV1909-es")

            logs_dir = os.path.join(getattr(self, "base_dir", os.getcwd()), "logs")
            try:
                os.makedirs(logs_dir, exist_ok=True)
            except Exception:
                pass

            # Runner inline: importa y ejecuta open_reader_gui
            code = (
                "import sys; "
                "sys.path.insert(0, r'%s'); "
                "from core.gui_reader import open_reader_gui; "
                "open_reader_gui(version=r'%s', title='Biblia Interactiva')"
            ) % (getattr(self, "base_dir", os.getcwd()).replace("'", "\\'"), ver.replace("'", "\\'"))

            out_path = os.path.join(logs_dir, "reader_gui.log")
            with open(out_path, "a", encoding="utf-8") as f:
                f.write("[RUN] version=%s\n" % ver)

            # Lanzar python separado
            subprocess.Popen(
                [sys.executable, "-c", code],
                cwd=getattr(self, "base_dir", None) or os.getcwd(),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=0x00000008  # CREATE_NO_WINDOW (evita consola extra)
            )

        except Exception as e:
            try:
                import traceback, os
                logs_dir = os.path.join(getattr(self, "base_dir", os.getcwd()), "logs")
                os.makedirs(logs_dir, exist_ok=True)
                p = os.path.join(logs_dir, "desktop_app.log")
                with open(p, "a", encoding="utf-8") as f:
                    f.write("[ERROR] _open_reader_gui_action: %s\n" % str(e))
                    f.write(traceback.format_exc() + "\n")
            except Exception:
                pass
            try:
                self.write_safe("[ERROR] Lector GUI: " + str(e) + "\n")
            except Exception:
                pass
