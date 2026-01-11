# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
import json

APP_TITLE   = "Biblia"
APP_VERSION = "v1.0"
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))

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
    def __init__(self):
        super().__init__()
        self.settings = load_settings()

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
        self.log.insert("end", s)
        self.log.see("end")

    def about(self):
        messagebox.showinfo(APP_TITLE, f"{APP_TITLE} {APP_VERSION}\nRepositorio: donpelo/biblia")

    def launch_console(self, relpath, msg):
        self.write(msg + "\n")
        try:
            launch_python(relpath)
        except FileNotFoundError:
            self.write(f"[ERROR] No existe: {relpath}\n")
            messagebox.showerror(APP_TITLE, f"No existe:\n{os.path.join(BASE_DIR, relpath)}")
        except Exception as e:
            self.write(f"[ERROR] {e}\n")
            messagebox.showerror(APP_TITLE, str(e))

    def launch_gui(self, relpath, msg):
        self.write(msg + "\n")
        try:
            # GUI sin consola: usar pythonw si está disponible
            pyw = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
            target = os.path.join(BASE_DIR, relpath)
            if not os.path.exists(target):
                raise FileNotFoundError(target)
            if os.path.exists(pyw):
                subprocess.Popen([pyw, target], cwd=BASE_DIR)
            else:
                subprocess.Popen([sys.executable, target], cwd=BASE_DIR)
        except FileNotFoundError:
            self.write(f"[ERROR] No existe: {relpath}\n")
            messagebox.showerror(APP_TITLE, f"No existe:\n{os.path.join(BASE_DIR, relpath)}")
        except Exception as e:
            self.write(f"[ERROR] {e}\n")
            messagebox.showerror(APP_TITLE, str(e))

    def open_daily(self):
        ref = self.settings.get("daily_ref", DEFAULTS["daily_ref"])
        title = self.settings.get("daily_title", "")
        note = self.settings.get("daily_note", "")
        self.write(f"Lectura del día -> {ref}\n")

        # Muestra info y (opcional) abre el lector de consola
        messagebox.showinfo(APP_TITLE, f"Lectura del día:\n{ref}\n\n{title}\n{note}".strip())

        # Intenta abrir lector bíblico de consola (si acepta args, perfecto; si no, igual abre)
        try:
            launch_python("modules/lector_biblia.py", extra_args=["--ref", ref])
        except Exception:
            # Si no soporta args, lo abrimos sin args
            try:
                launch_python("modules/lector_biblia.py")
            except Exception:
                pass

    def open_settings(self):
        win = tk.Toplevel(self)
        win.title("Configuración")
        win.geometry("560x360")
        win.resizable(False, False)

        frm = ttk.Frame(win, padding=14)
        frm.pack(fill="both", expand=True)

        s = dict(self.settings)

        # Variables
        v_bible = tk.StringVar(value=s.get("bible_version",""))
        v_rate  = tk.StringVar(value=str(s.get("tts_rate", DEFAULTS["tts_rate"])))
        v_voice = tk.StringVar(value=s.get("tts_voice",""))

        v_ref   = tk.StringVar(value=s.get("daily_ref",""))
        v_title = tk.StringVar(value=s.get("daily_title",""))
        v_note  = tk.StringVar(value=s.get("daily_note",""))

        # Layout
        ttk.Label(frm, text="Configuración", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0,10))

        ttk.Label(frm, text="Versión Biblia").grid(row=1, column=0, sticky="w")
        ttk.Entry(frm, textvariable=v_bible, width=20).grid(row=1, column=1, sticky="w")

        ttk.Label(frm, text="TTS velocidad (rate)").grid(row=2, column=0, sticky="w", pady=(6,0))
        ttk.Entry(frm, textvariable=v_rate, width=10).grid(row=2, column=1, sticky="w", pady=(6,0))

        ttk.Label(frm, text="TTS voz (id opcional)").grid(row=3, column=0, sticky="w", pady=(6,0))
        ttk.Entry(frm, textvariable=v_voice, width=40).grid(row=3, column=1, sticky="w", pady=(6,0))

        ttk.Separator(frm).grid(row=4, column=0, columnspan=2, sticky="ew", pady=10)

        ttk.Label(frm, text="Lectura del día (hoy)", font=("Segoe UI", 10, "bold")).grid(row=5, column=0, columnspan=2, sticky="w", pady=(0,6))

        ttk.Label(frm, text="Referencia").grid(row=6, column=0, sticky="w")
        ttk.Entry(frm, textvariable=v_ref, width=22).grid(row=6, column=1, sticky="w")

        ttk.Label(frm, text="Título").grid(row=7, column=0, sticky="w", pady=(6,0))
        ttk.Entry(frm, textvariable=v_title, width=40).grid(row=7, column=1, sticky="w", pady=(6,0))

        ttk.Label(frm, text="Nota").grid(row=8, column=0, sticky="w", pady=(6,0))
        ttk.Entry(frm, textvariable=v_note, width=40).grid(row=8, column=1, sticky="w", pady=(6,0))

        # Botones
        btns = ttk.Frame(frm)
        btns.grid(row=9, column=0, columnspan=2, sticky="w", pady=16)

        def on_save():
            s2 = dict(self.settings)
            s2["bible_version"] = v_bible.get().strip() or DEFAULTS["bible_version"]
            s2["tts_rate"] = _safe_int(v_rate.get().strip(), DEFAULTS["tts_rate"])
            s2["tts_voice"] = v_voice.get().strip()

            s2["daily_ref"] = v_ref.get().strip() or DEFAULTS["daily_ref"]
            s2["daily_title"] = v_title.get().strip()
            s2["daily_note"] = v_note.get().strip()

            save_settings(s2)
            self.settings = s2
            self.daily_btn.configure(text=self._daily_label())
            self.write("Configuración guardada.\n")
            win.destroy()

        ttk.Button(btns, text="Guardar", command=on_save).pack(side="left", padx=(0,10))
        ttk.Button(btns, text="Cerrar", command=win.destroy).pack(side="left")

        win.transient(self)
        win.grab_set()
        win.focus_set()

if __name__ == "__main__":
    app = BibliaMenu()
    app.mainloop()
