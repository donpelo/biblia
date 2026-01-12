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
        try:
            from core.gui_reader import open_reader_gui
            ver = getattr(self, "bible_version", "RV1909-es")
            open_reader_gui(version=ver, title="Biblia Interactiva")
        except Exception as e:
            try:
                self.write_safe("[ERROR] Lector GUI: " + str(e) + "\n")
            except Exception:
                pass
    def open_daily(self):

        """

        Abre la Lectura del día en el Lector GUI.

        Usa data/devocional_calendar.json con clave MM-DD.

        Fallback: Génesis 1 si no hay match.

        """

        try:

            import os, json

            from datetime import date


            mmdd = date.today().strftime("%m-%d")


            # base_dir robusto

            base = getattr(self, "base_dir", None)

            if not base:

                try:

                    base = os.path.dirname(__file__)

                except Exception:

                    base = os.getcwd()

                self.base_dir = base


            cal_path = os.path.join(base, "data", "devocional_calendar.json")

            ref = None

            if os.path.exists(cal_path):

                try:

                    with open(cal_path, "r", encoding="utf-8") as f:

                        cal = json.load(f)

                    ref = cal.get(mmdd) or cal.get(mmdd.lstrip("0"))

                except Exception:

                    ref = None


            if not ref:

                ref = "Génesis 1"


            ver = getattr(self, "bible_version", None) or "RV1909-es"


            from core.gui_reader import open_reader_gui

            open_reader_gui(version=ver, initial_ref=ref, title="Lectura del día")


            try:

                if hasattr(self, "write_safe"):

                    self.write_safe(f"[OK] Lectura del día {mmdd}: {ref}\n")

            except Exception:

                pass


        except Exception as e:

            try:

                if hasattr(self, "write_safe"):

                    self.write_safe(f"[ERROR] open_daily: {e}\n")

            except Exception:

                pass

            try:

                from tkinter import messagebox

                messagebox.showerror("Lectura del día", str(e))

            except Exception:

                pass
    def open_settings(self):
        win = tk.Toplevel(self)
        win.title("Configuración")
        win.geometry("520x420")
        win.transient(self)

        frm = ttk.Frame(win, padding=14)
        frm.pack(fill="both", expand=True)

        cfg = dict(self.cfg) if isinstance(self.cfg, dict) else {}

        # UI language
        ttk.Label(frm, text="Idioma UI").pack(anchor="w")
        ui_lang = tk.StringVar(value=cfg.get("ui_lang","es"))
        row = ttk.Frame(frm)
        row.pack(fill="x", pady=6)
        ttk.Radiobutton(row, text="Español", variable=ui_lang, value="es").pack(side="left")
        ttk.Radiobutton(row, text="English", variable=ui_lang, value="en").pack(side="left", padx=12)

        ttk.Separator(frm, orient="horizontal").pack(fill="x", pady=10)

        # TTS settings (base values only)
        ttk.Label(frm, text="TTS rate (100-250 aprox)").pack(anchor="w")
        rate = tk.IntVar(value=int(cfg.get("tts_rate","180") or 180))
        ttk.Scale(frm, from_=80, to=300, variable=rate, orient="horizontal").pack(fill="x", pady=6)
        ttk.Label(frm, textvariable=rate).pack(anchor="w")

        ttk.Label(frm, text="TTS volume (0.0 - 1.0)").pack(anchor="w", pady=(10,0))
        vol = tk.DoubleVar(value=float(cfg.get("tts_volume","1.0") or 1.0))
        ttk.Scale(frm, from_=0.0, to=1.0, variable=vol, orient="horizontal").pack(fill="x", pady=6)
        ttk.Label(frm, textvariable=vol).pack(anchor="w")

        ttk.Label(frm, text="TTS voice (opcional, texto contiene nombre)").pack(anchor="w", pady=(10,0))
        voice = tk.StringVar(value=str(cfg.get("tts_voice","") or ""))
        ttk.Entry(frm, textvariable=voice).pack(fill="x", pady=4)

        def test_tts():
            try:
                import pyttsx3
                engine = pyttsx3.init()
                engine.setProperty("rate", int(rate.get()))
                engine.setProperty("volume", float(vol.get()))
                vn = (voice.get() or "").strip()
                if vn:
                    try:
                        for v in engine.getProperty("voices"):
                            vid = getattr(v, "id", "") or ""
                            vname = getattr(v, "name", "") or ""
                            if vn.lower() in vid.lower() or vn.lower() in vname.lower():
                                engine.setProperty("voice", vid)
                                break
                    except Exception:
                        pass
                msg = "Prueba de voz. Biblia Interactiva." if ui_lang.get()=="es" else "Voice test. Bible Interactive."
                engine.say(msg)
                engine.runAndWait()
            except Exception as e:
                messagebox.showerror("TTS", str(e))

        def save_close():
            newcfg = dict(cfg)
            newcfg["ui_lang"] = ui_lang.get()
            newcfg["tts_rate"] = str(int(rate.get()))
            newcfg["tts_volume"] = str(float(vol.get()))
            newcfg["tts_voice"] = (voice.get() or "").strip()
            newcfg["bible_version"] = self.bible_version

            self._cfg_save(newcfg)
            self.ui_lang = newcfg["ui_lang"]
            win.destroy()
            self.write_safe("[OK] Configuración guardada.\n")

        bbar = ttk.Frame(frm)
        bbar.pack(fill="x", pady=(16,0))
        ttk.Button(bbar, text="Probar voz", command=test_tts).pack(side="left")
        ttk.Button(bbar, text="Cancelar", command=win.destroy).pack(side="right")
        ttk.Button(bbar, text="Guardar", command=save_close).pack(side="right", padx=(0,8))

    # -------------------------
    # Actions / Launchers (auto)
    # -------------------------
    def write_safe(self, msg: str):
        try:
            if hasattr(self, "log") and self.log:
                self.log.insert("end", msg)
                self.log.see("end")
            else:
                print(msg, end="")
        except Exception:
            try:
                print(msg, end="")
            except Exception:
                pass

    def _repo_root(self):
        import os
        try:
            return getattr(self, "base_dir", None) or os.path.abspath(os.path.dirname(__file__))
        except Exception:
            return os.getcwd()

    def launch_console(self, rel_path: str, title: str = "Biblia"):
        import os, subprocess, sys
        root = self._repo_root()
        script = os.path.join(root, rel_path.replace("/", os.sep))
        self.write_safe(f"[INFO] {title}: {script}\n")
        if not os.path.exists(script):
            self.write_safe(f"[ERROR] No existe: {script}\n")
            return
        # abrir una consola nueva (Windows)
        try:
            subprocess.Popen([sys.executable, script], cwd=root, creationflags=0x00000010)
        except Exception as e:
            self.write_safe(f"[ERROR] launch_console: {e}\n")

    def launch_gui(self, rel_path: str, title: str = "Biblia GUI"):
        import os, subprocess, sys
        root = self._repo_root()
        script = os.path.join(root, rel_path.replace("/", os.sep))
        self.write_safe(f"[INFO] {title}: {script}\n")
        if not os.path.exists(script):
            self.write_safe(f"[ERROR] No existe: {script}\n")
            return
        try:
            subprocess.Popen([sys.executable, script], cwd=root)
        except Exception as e:
            self.write_safe(f"[ERROR] launch_gui: {e}\n")

    def open_reader_gui(self):
        # Abre el lector GUI real (core/gui_reader.py)
        try:
            from core.gui_reader import open_reader_gui
        except Exception as e:
            self.write_safe(f"[ERROR] No pude importar core.gui_reader: {e}\n")
            return

        # Resolver versión activa desde config si existe
        ver = getattr(self, "bible_version", None) or "RV1909-es"
        try:
            open_reader_gui(version=ver, initial_ref=None, title="Biblia Interactiva")
        except Exception as e:
            self.write_safe(f"[ERROR] open_reader_gui: {e}\n")

    def about(self):
        try:
            from tkinter import messagebox
            messagebox.showinfo(
                "Acerca de",
                "Biblia Interactiva\n\nLector GUI + herramientas (buscador, planes, notas, TTS).\nRepositorio: donpelo/biblia"
            )
        except Exception:
            pass

def _run_gui_entrypoint():
    _log_boot("START biblia_gui.py")
    try:
        _log_boot("ENTRYPOINT: start")
        app = BibliaMenu()
        _log_boot("ENTRYPOINT: BibliaMenu=OK")
        app.mainloop()
        _log_boot("EXIT: normal")
    except Exception as e:
        _log_boot(f"FATAL: entrypoint exception: {repr(e)}")
        _log_boot(traceback.format_exc())

    # --- PATCHED METHODS v0.1 ---
    def write_safe(self, s: str):
        try:
            self.write(s)
        except Exception:
            try:
                print(s, end="")
            except Exception:
                pass

    def about(self):
        try:
            messagebox.showinfo("Biblia", "Biblia Interactiva\nRepo: donpelo/biblia")
        except Exception:
            pass

    def _abs(self, relpath: str) -> str:
        try:
            base = getattr(self, "base_dir", None) or getattr(self, "BASE_DIR", None)
        except Exception:
            base = None
        if not base:
            try:
                base = os.path.dirname(os.path.abspath(__file__))
            except Exception:
                base = os.getcwd()
        return os.path.join(base, relpath)

    def launch_console(self, relpath: str, msg: str = ""):
        try:
            if msg:
                self.write_safe(msg + "\n")
            target = self._abs(relpath)
            if not os.path.exists(target):
                self.write_safe("[ERROR] No existe: " + target + "\n")
                return
            # consola nueva
            CREATE_NEW_CONSOLE = 0x00000010
            subprocess.Popen([sys.executable, "-u", target], cwd=os.path.dirname(target), creationflags=CREATE_NEW_CONSOLE)
        except Exception as e:
            self.write_safe("[ERROR] launch_console: " + str(e) + "\n")

    def launch_gui(self, relpath: str, msg: str = ""):
        try:
            if msg:
                self.write_safe(msg + "\n")
            target = self._abs(relpath)
            if not os.path.exists(target):
                self.write_safe("[ERROR] No existe: " + target + "\n")
                return
            subprocess.Popen([sys.executable, target], cwd=os.path.dirname(target))
        except Exception as e:
            self.write_safe("[ERROR] launch_gui: " + str(e) + "\n")

import os, sys, json, subprocess, traceback
import tkinter as tk
from tkinter import ttk, messagebox

APP_TITLE = "Biblia"
APP_VERSION = "v1.0"

def _now():
    import datetime
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

    def open_daily(self):

        """

        Abre la Lectura del día en el Lector GUI.

        Usa data/devocional_calendar.json con clave MM-DD.

        Fallback: Génesis 1 si no hay match.

        """

        try:

            import os, json

            from datetime import date


            mmdd = date.today().strftime("%m-%d")


            # base_dir robusto

            base = getattr(self, "base_dir", None)

            if not base:

                try:

                    base = os.path.dirname(__file__)

                except Exception:

                    base = os.getcwd()

                self.base_dir = base


            cal_path = os.path.join(base, "data", "devocional_calendar.json")

            ref = None

            if os.path.exists(cal_path):

                try:

                    with open(cal_path, "r", encoding="utf-8") as f:

                        cal = json.load(f)

                    ref = cal.get(mmdd) or cal.get(mmdd.lstrip("0"))

                except Exception:

                    ref = None


            if not ref:

                ref = "Génesis 1"


            ver = getattr(self, "bible_version", None) or "RV1909-es"


            from core.gui_reader import open_reader_gui

            open_reader_gui(version=ver, initial_ref=ref, title="Lectura del día")


            try:

                if hasattr(self, "write_safe"):

                    self.write_safe(f"[OK] Lectura del día {mmdd}: {ref}\n")

            except Exception:

                pass


        except Exception as e:

            try:

                if hasattr(self, "write_safe"):

                    self.write_safe(f"[ERROR] open_daily: {e}\n")

            except Exception:

                pass

            try:

                from tkinter import messagebox

                messagebox.showerror("Lectura del día", str(e))

            except Exception:

                pass
    def open_settings(self):
        win = tk.Toplevel(self)
        win.title("Configuración")
        win.geometry("520x420")
        win.transient(self)

        frm = ttk.Frame(win, padding=14)
        frm.pack(fill="both", expand=True)

        cfg = dict(self.cfg) if isinstance(self.cfg, dict) else {}

        # UI language
        ttk.Label(frm, text="Idioma UI").pack(anchor="w")
        ui_lang = tk.StringVar(value=cfg.get("ui_lang","es"))
        row = ttk.Frame(frm)
        row.pack(fill="x", pady=6)
        ttk.Radiobutton(row, text="Español", variable=ui_lang, value="es").pack(side="left")
        ttk.Radiobutton(row, text="English", variable=ui_lang, value="en").pack(side="left", padx=12)

        ttk.Separator(frm, orient="horizontal").pack(fill="x", pady=10)

        # TTS settings (base values only)
        ttk.Label(frm, text="TTS rate (100-250 aprox)").pack(anchor="w")
        rate = tk.IntVar(value=int(cfg.get("tts_rate","180") or 180))
        ttk.Scale(frm, from_=80, to=300, variable=rate, orient="horizontal").pack(fill="x", pady=6)
        ttk.Label(frm, textvariable=rate).pack(anchor="w")

        ttk.Label(frm, text="TTS volume (0.0 - 1.0)").pack(anchor="w", pady=(10,0))
        vol = tk.DoubleVar(value=float(cfg.get("tts_volume","1.0") or 1.0))
        ttk.Scale(frm, from_=0.0, to=1.0, variable=vol, orient="horizontal").pack(fill="x", pady=6)
        ttk.Label(frm, textvariable=vol).pack(anchor="w")

        ttk.Label(frm, text="TTS voice (opcional, texto contiene nombre)").pack(anchor="w", pady=(10,0))
        voice = tk.StringVar(value=str(cfg.get("tts_voice","") or ""))
        ttk.Entry(frm, textvariable=voice).pack(fill="x", pady=4)

        def test_tts():
            try:
                import pyttsx3
                engine = pyttsx3.init()
                engine.setProperty("rate", int(rate.get()))
                engine.setProperty("volume", float(vol.get()))
                vn = (voice.get() or "").strip()
                if vn:
                    try:
                        for v in engine.getProperty("voices"):
                            vid = getattr(v, "id", "") or ""
                            vname = getattr(v, "name", "") or ""
                            if vn.lower() in vid.lower() or vn.lower() in vname.lower():
                                engine.setProperty("voice", vid)
                                break
                    except Exception:
                        pass
                msg = "Prueba de voz. Biblia Interactiva." if ui_lang.get()=="es" else "Voice test. Bible Interactive."
                engine.say(msg)
                engine.runAndWait()
            except Exception as e:
                messagebox.showerror("TTS", str(e))

        def save_close():
            newcfg = dict(cfg)
            newcfg["ui_lang"] = ui_lang.get()
            newcfg["tts_rate"] = str(int(rate.get()))
            newcfg["tts_volume"] = str(float(vol.get()))
            newcfg["tts_voice"] = (voice.get() or "").strip()
            newcfg["bible_version"] = self.bible_version

            self._cfg_save(newcfg)
            self.ui_lang = newcfg["ui_lang"]
            win.destroy()
            self.write_safe("[OK] Configuración guardada.\n")

        bbar = ttk.Frame(frm)
        bbar.pack(fill="x", pady=(16,0))
        ttk.Button(bbar, text="Probar voz", command=test_tts).pack(side="left")
        ttk.Button(bbar, text="Cancelar", command=win.destroy).pack(side="right")
        ttk.Button(bbar, text="Guardar", command=save_close).pack(side="right", padx=(0,8))

    # -------------------------
    # Actions / Launchers (auto)
    # -------------------------
    def write_safe(self, msg: str):
        try:
            if hasattr(self, "log") and self.log:
                self.log.insert("end", msg)
                self.log.see("end")
            else:
                print(msg, end="")
        except Exception:
            try:
                print(msg, end="")
            except Exception:
                pass

    def _repo_root(self):
        import os
        try:
            return getattr(self, "base_dir", None) or os.path.abspath(os.path.dirname(__file__))
        except Exception:
            return os.getcwd()

    def launch_console(self, rel_path: str, title: str = "Biblia"):
        import os, subprocess, sys
        root = self._repo_root()
        script = os.path.join(root, rel_path.replace("/", os.sep))
        self.write_safe(f"[INFO] {title}: {script}\n")
        if not os.path.exists(script):
            self.write_safe(f"[ERROR] No existe: {script}\n")
            return
        # abrir una consola nueva (Windows)
        try:
            subprocess.Popen([sys.executable, script], cwd=root, creationflags=0x00000010)
        except Exception as e:
            self.write_safe(f"[ERROR] launch_console: {e}\n")

    def launch_gui(self, rel_path: str, title: str = "Biblia GUI"):
        import os, subprocess, sys
        root = self._repo_root()
        script = os.path.join(root, rel_path.replace("/", os.sep))
        self.write_safe(f"[INFO] {title}: {script}\n")
        if not os.path.exists(script):
            self.write_safe(f"[ERROR] No existe: {script}\n")
            return
        try:
            subprocess.Popen([sys.executable, script], cwd=root)
        except Exception as e:
            self.write_safe(f"[ERROR] launch_gui: {e}\n")

    def open_reader_gui(self):
        # Abre el lector GUI real (core/gui_reader.py)
        try:
            from core.gui_reader import open_reader_gui
        except Exception as e:
            self.write_safe(f"[ERROR] No pude importar core.gui_reader: {e}\n")
            return

        # Resolver versión activa desde config si existe
        ver = getattr(self, "bible_version", None) or "RV1909-es"
        try:
            open_reader_gui(version=ver, initial_ref=None, title="Biblia Interactiva")
        except Exception as e:
            self.write_safe(f"[ERROR] open_reader_gui: {e}\n")

    def about(self):
        try:
            from tkinter import messagebox
            messagebox.showinfo(
                "Acerca de",
                "Biblia Interactiva\n\nLector GUI + herramientas (buscador, planes, notas, TTS).\nRepositorio: donpelo/biblia"
            )
        except Exception:
            pass

def _run_gui_entrypoint():
    _log_boot("START biblia_gui.py")
    try:
        _log_boot("ENTRYPOINT: start")
        app = BibliaMenu()
        _log_boot("ENTRYPOINT: BibliaMenu=OK")
        app.mainloop()
        _log_boot("EXIT: normal")
    except Exception as e:
        _log_boot(f"FATAL: entrypoint exception: {repr(e)}")
        _log_boot(traceback.format_exc())

    # --- PATCHED METHODS v0.1 ---
    def write_safe(self, s: str):
        try:
            self.write(s)
        except Exception:
            try:
                print(s, end="")
            except Exception:
                pass

    def about(self):
        try:
            messagebox.showinfo("Biblia", "Biblia Interactiva\nRepo: donpelo/biblia")
        except Exception:
            pass

    def _abs(self, relpath: str) -> str:
        try:
            base = getattr(self, "base_dir", None) or getattr(self, "BASE_DIR", None)
        except Exception:
            base = None
        if not base:
            try:
                base = os.path.dirname(os.path.abspath(__file__))
            except Exception:
                base = os.getcwd()
        return os.path.join(base, relpath)

    def launch_console(self, relpath: str, msg: str = ""):
        try:
            if msg:
                self.write_safe(msg + "\n")
            target = self._abs(relpath)
            if not os.path.exists(target):
                self.write_safe("[ERROR] No existe: " + target + "\n")
                return
            # consola nueva
            CREATE_NEW_CONSOLE = 0x00000010
            subprocess.Popen([sys.executable, "-u", target], cwd=os.path.dirname(target), creationflags=CREATE_NEW_CONSOLE)
        except Exception as e:
            self.write_safe("[ERROR] launch_console: " + str(e) + "\n")

    def launch_gui(self, relpath: str, msg: str = ""):
        try:
            if msg:
                self.write_safe(msg + "\n")
            target = self._abs(relpath)
            if not os.path.exists(target):
                self.write_safe("[ERROR] No existe: " + target + "\n")
                return
            subprocess.Popen([sys.executable, target], cwd=os.path.dirname(target))
        except Exception as e:
            self.write_safe("[ERROR] launch_gui: " + str(e) + "\n")

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

    def open_daily(self):

        """

        Abre la Lectura del día en el Lector GUI.

        Usa data/devocional_calendar.json con clave MM-DD.

        Fallback: Génesis 1 si no hay match.

        """

        try:

            import os, json

            from datetime import date


            mmdd = date.today().strftime("%m-%d")


            # base_dir robusto

            base = getattr(self, "base_dir", None)

            if not base:

                try:

                    base = os.path.dirname(__file__)

                except Exception:

                    base = os.getcwd()

                self.base_dir = base


            cal_path = os.path.join(base, "data", "devocional_calendar.json")

            ref = None

            if os.path.exists(cal_path):

                try:

                    with open(cal_path, "r", encoding="utf-8") as f:

                        cal = json.load(f)

                    ref = cal.get(mmdd) or cal.get(mmdd.lstrip("0"))

                except Exception:

                    ref = None


            if not ref:

                ref = "Génesis 1"


            ver = getattr(self, "bible_version", None) or "RV1909-es"


            from core.gui_reader import open_reader_gui

            open_reader_gui(version=ver, initial_ref=ref, title="Lectura del día")


            try:

                if hasattr(self, "write_safe"):

                    self.write_safe(f"[OK] Lectura del día {mmdd}: {ref}\n")

            except Exception:

                pass


        except Exception as e:

            try:

                if hasattr(self, "write_safe"):

                    self.write_safe(f"[ERROR] open_daily: {e}\n")

            except Exception:

                pass

            try:

                from tkinter import messagebox

                messagebox.showerror("Lectura del día", str(e))

            except Exception:

                pass
    def open_settings(self):
        win = tk.Toplevel(self)
        win.title("Configuración")
        win.geometry("520x420")
        win.transient(self)

        frm = ttk.Frame(win, padding=14)
        frm.pack(fill="both", expand=True)

        cfg = dict(self.cfg) if isinstance(self.cfg, dict) else {}

        # UI language
        ttk.Label(frm, text="Idioma UI").pack(anchor="w")
        ui_lang = tk.StringVar(value=cfg.get("ui_lang","es"))
        row = ttk.Frame(frm)
        row.pack(fill="x", pady=6)
        ttk.Radiobutton(row, text="Español", variable=ui_lang, value="es").pack(side="left")
        ttk.Radiobutton(row, text="English", variable=ui_lang, value="en").pack(side="left", padx=12)

        ttk.Separator(frm, orient="horizontal").pack(fill="x", pady=10)

        # TTS settings (base values only)
        ttk.Label(frm, text="TTS rate (100-250 aprox)").pack(anchor="w")
        rate = tk.IntVar(value=int(cfg.get("tts_rate","180") or 180))
        ttk.Scale(frm, from_=80, to=300, variable=rate, orient="horizontal").pack(fill="x", pady=6)
        ttk.Label(frm, textvariable=rate).pack(anchor="w")

        ttk.Label(frm, text="TTS volume (0.0 - 1.0)").pack(anchor="w", pady=(10,0))
        vol = tk.DoubleVar(value=float(cfg.get("tts_volume","1.0") or 1.0))
        ttk.Scale(frm, from_=0.0, to=1.0, variable=vol, orient="horizontal").pack(fill="x", pady=6)
        ttk.Label(frm, textvariable=vol).pack(anchor="w")

        ttk.Label(frm, text="TTS voice (opcional, texto contiene nombre)").pack(anchor="w", pady=(10,0))
        voice = tk.StringVar(value=str(cfg.get("tts_voice","") or ""))
        ttk.Entry(frm, textvariable=voice).pack(fill="x", pady=4)

        def test_tts():
            try:
                import pyttsx3
                engine = pyttsx3.init()
                engine.setProperty("rate", int(rate.get()))
                engine.setProperty("volume", float(vol.get()))
                vn = (voice.get() or "").strip()
                if vn:
                    try:
                        for v in engine.getProperty("voices"):
                            vid = getattr(v, "id", "") or ""
                            vname = getattr(v, "name", "") or ""
                            if vn.lower() in vid.lower() or vn.lower() in vname.lower():
                                engine.setProperty("voice", vid)
                                break
                    except Exception:
                        pass
                msg = "Prueba de voz. Biblia Interactiva." if ui_lang.get()=="es" else "Voice test. Bible Interactive."
                engine.say(msg)
                engine.runAndWait()
            except Exception as e:
                messagebox.showerror("TTS", str(e))

        def save_close():
            newcfg = dict(cfg)
            newcfg["ui_lang"] = ui_lang.get()
            newcfg["tts_rate"] = str(int(rate.get()))
            newcfg["tts_volume"] = str(float(vol.get()))
            newcfg["tts_voice"] = (voice.get() or "").strip()
            newcfg["bible_version"] = self.bible_version

            self._cfg_save(newcfg)
            self.ui_lang = newcfg["ui_lang"]
            win.destroy()
            self.write_safe("[OK] Configuración guardada.\n")

        bbar = ttk.Frame(frm)
        bbar.pack(fill="x", pady=(16,0))
        ttk.Button(bbar, text="Probar voz", command=test_tts).pack(side="left")
        ttk.Button(bbar, text="Cancelar", command=win.destroy).pack(side="right")
        ttk.Button(bbar, text="Guardar", command=save_close).pack(side="right", padx=(0,8))

    # -------------------------
    # Actions / Launchers (auto)
    # -------------------------
    def write_safe(self, msg: str):
        try:
            if hasattr(self, "log") and self.log:
                self.log.insert("end", msg)
                self.log.see("end")
            else:
                print(msg, end="")
        except Exception:
            try:
                print(msg, end="")
            except Exception:
                pass

    def _repo_root(self):
        import os
        try:
            return getattr(self, "base_dir", None) or os.path.abspath(os.path.dirname(__file__))
        except Exception:
            return os.getcwd()

    def launch_console(self, rel_path: str, title: str = "Biblia"):
        import os, subprocess, sys
        root = self._repo_root()
        script = os.path.join(root, rel_path.replace("/", os.sep))
        self.write_safe(f"[INFO] {title}: {script}\n")
        if not os.path.exists(script):
            self.write_safe(f"[ERROR] No existe: {script}\n")
            return
        # abrir una consola nueva (Windows)
        try:
            subprocess.Popen([sys.executable, script], cwd=root, creationflags=0x00000010)
        except Exception as e:
            self.write_safe(f"[ERROR] launch_console: {e}\n")

    def launch_gui(self, rel_path: str, title: str = "Biblia GUI"):
        import os, subprocess, sys
        root = self._repo_root()
        script = os.path.join(root, rel_path.replace("/", os.sep))
        self.write_safe(f"[INFO] {title}: {script}\n")
        if not os.path.exists(script):
            self.write_safe(f"[ERROR] No existe: {script}\n")
            return
        try:
            subprocess.Popen([sys.executable, script], cwd=root)
        except Exception as e:
            self.write_safe(f"[ERROR] launch_gui: {e}\n")

    def open_reader_gui(self):
        # Abre el lector GUI real (core/gui_reader.py)
        try:
            from core.gui_reader import open_reader_gui
        except Exception as e:
            self.write_safe(f"[ERROR] No pude importar core.gui_reader: {e}\n")
            return

        # Resolver versión activa desde config si existe
        ver = getattr(self, "bible_version", None) or "RV1909-es"
        try:
            open_reader_gui(version=ver, initial_ref=None, title="Biblia Interactiva")
        except Exception as e:
            self.write_safe(f"[ERROR] open_reader_gui: {e}\n")

    def about(self):
        try:
            from tkinter import messagebox
            messagebox.showinfo(
                "Acerca de",
                "Biblia Interactiva\n\nLector GUI + herramientas (buscador, planes, notas, TTS).\nRepositorio: donpelo/biblia"
            )
        except Exception:
            pass

def _run_gui_entrypoint():
    _log_boot("START biblia_gui.py")
    try:
        _log_boot("ENTRYPOINT: start")
        app = BibliaMenu()
        _log_boot("ENTRYPOINT: BibliaMenu=OK")
        app.mainloop()
        _log_boot("EXIT: normal")
    except Exception as e:
        _log_boot(f"FATAL: entrypoint exception: {repr(e)}")
        _log_boot(traceback.format_exc())

    # --- PATCHED METHODS v0.1 ---
    def write_safe(self, s: str):
        try:
            self.write(s)
        except Exception:
            try:
                print(s, end="")
            except Exception:
                pass

    def about(self):
        try:
            messagebox.showinfo("Biblia", "Biblia Interactiva\nRepo: donpelo/biblia")
        except Exception:
            pass

    def _abs(self, relpath: str) -> str:
        try:
            base = getattr(self, "base_dir", None) or getattr(self, "BASE_DIR", None)
        except Exception:
            base = None
        if not base:
            try:
                base = os.path.dirname(os.path.abspath(__file__))
            except Exception:
                base = os.getcwd()
        return os.path.join(base, relpath)

    def launch_console(self, relpath: str, msg: str = ""):
        try:
            if msg:
                self.write_safe(msg + "\n")
            target = self._abs(relpath)
            if not os.path.exists(target):
                self.write_safe("[ERROR] No existe: " + target + "\n")
                return
            # consola nueva
            CREATE_NEW_CONSOLE = 0x00000010
            subprocess.Popen([sys.executable, "-u", target], cwd=os.path.dirname(target), creationflags=CREATE_NEW_CONSOLE)
        except Exception as e:
            self.write_safe("[ERROR] launch_console: " + str(e) + "\n")

    def launch_gui(self, relpath: str, msg: str = ""):
        try:
            if msg:
                self.write_safe(msg + "\n")
            target = self._abs(relpath)
            if not os.path.exists(target):
                self.write_safe("[ERROR] No existe: " + target + "\n")
                return
            subprocess.Popen([sys.executable, target], cwd=os.path.dirname(target))
        except Exception as e:
            self.write_safe("[ERROR] launch_gui: " + str(e) + "\n")

    def open_daily(self):
        # Lectura del día: MM-DD en data/devocional_calendar.json
        try:
            from datetime import date
            mmdd = date.today().strftime("%m-%d")

            cal = self._abs(r"data\devocional_calendar.json")
            ref = None
            if os.path.exists(cal):
                import json
                with open(cal, "r", encoding="utf-8-sig") as f:
                    data = json.load(f)
                ref = data.get(mmdd)

            if not ref:
                ref = "Génesis 1:1-5"

            self.launch_console(r"core\cli_reader.py", "Lectura del día: " + mmdd + " -> " + ref)

            # pasar la referencia por env var (simple y robusto)
            os.environ["BIBLIA_REF"] = ref
        except Exception as e:
            self.write_safe("[ERROR] open_daily: " + str(e) + "\n")

def _desktop_safe_run():
    """
    Garantiza que al ejecutar desde doble click el proceso no termine
    si el GUI quedó abierto pero el entrypoint retornó.
    """
    try:
        _run_gui_entrypoint()
    finally:
        try:
            import tkinter as _tk
            r = getattr(_tk, "_default_root", None)
            if r is not None:
                try:
                    r.update_idletasks()
                except Exception:
                    pass
                try:
                    r.mainloop()
                except Exception:
                    pass
        except Exception:
            pass
if __name__ == "__main__":
    try:
        import os, sys, datetime
        _base = os.path.dirname(__file__)
        _logs = os.path.join(_base, "logs")
        os.makedirs(_logs, exist_ok=True)
        _lp = os.path.join(_logs, "desktop_app.log")
        with open(_lp, "a", encoding="utf-8") as _f:
            _f.write(f"[{datetime.datetime.now().isoformat(timespec='seconds')}] START cwd={os.getcwd()} argv={sys.argv}\n")
    except Exception:
        pass

    try:
        _desktop_safe_run()
    except Exception as e:
        try:
            import os, datetime, traceback
            _base = os.path.dirname(__file__)
            _lp = os.path.join(_base, "logs", "desktop_app.log")
            with open(_lp, "a", encoding="utf-8") as _f:
                _f.write(f"[{datetime.datetime.now().isoformat(timespec='seconds')}] EXC {repr(e)}\n")
                _f.write(traceback.format_exc() + "\n")
        except Exception:
            pass
        raise
    finally:
        try:
            import os, datetime
            _base = os.path.dirname(__file__)
            _lp = os.path.join(_base, "logs", "desktop_app.log")
            with open(_lp, "a", encoding="utf-8") as _f:
                _f.write(f"[{datetime.datetime.now().isoformat(timespec='seconds')}] END\n")
        except Exception:
            pass





