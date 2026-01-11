# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os

APP_TITLE = "Biblia"
APP_VERSION = "v1.0"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_py(relpath):
    py = sys.executable
    target = os.path.join(BASE_DIR, relpath)
    if not os.path.exists(target):
        messagebox.showerror(APP_TITLE, f"No existe:\n{target}")
        return
    subprocess.Popen([py, target], cwd=BASE_DIR)

class BibliaMenu(tk.Tk):
    def __init__(self):
        super().__init__()
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
        self.write(f"Listo. Selecciona un módulo.\nPython: {sys.executable}\nRuta: {BASE_DIR}\n")

        top = ttk.Frame(root)
        top.place(relx=1.0, rely=0.0, anchor="ne")
        ttk.Button(top, text="Acerca de", command=self.about).pack()

        def btn(txt, cmd):
            b = ttk.Button(left, text=txt, command=cmd)
            b.pack(fill="x", pady=6)
            return b

        btn("Leer Biblia", lambda: self.launch("gui/main.py", "Ejecutando: Leer Biblia"))
        btn("Devocional", lambda: self.launch("modules/devocional.py", "Ejecutando: Devocional"))
        btn("Planes de lectura", lambda: self.launch("modules/planes.py", "Ejecutando: Planes de lectura"))
        btn("Notas y marcadores", lambda: self.launch("modules/notas.py", "Ejecutando: Notas y marcadores"))
        btn("Audio Biblia", lambda: self.launch("modules/audio_biblia.py", "Ejecutando: Audio Biblia"))
        btn("Abrir main.py", lambda: self.launch("gui/main.py", "Ejecutando: gui/main.py"))
        btn("Salir", self.quit)

        self.write("Menú cargado.\n")

    def write(self, s):
        self.log.insert("end", s)
        self.log.see("end")

    def about(self):
        messagebox.showinfo(APP_TITLE, f"{APP_TITLE} {APP_VERSION}\nRepositorio: donpelo/biblia")

    def launch(self, relpath, msg):
        self.write(msg + "\n")
        target = os.path.join(BASE_DIR, relpath)
        if not os.path.exists(target):
            self.write(f"[ERROR] No existe: {relpath}\n")
            messagebox.showerror(APP_TITLE, f"No existe:\n{target}")
            return
        subprocess.Popen([sys.executable, target], cwd=BASE_DIR)

if __name__ == "__main__":
    app = BibliaMenu()
    app.mainloop()
