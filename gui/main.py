import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from core.reader import BibleReader
from core.audio import AudioReader
from core.devocionales import Devocionales

APP_TITLE = "BibliaInteractiva"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class BibliaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1200x700")
        self.configure(bg="#142336")

        # Icono
        icon_path = os.path.join(ROOT, "assets", "icons", "biblia.ico")
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass

        # Banner
        banner_path = os.path.join(ROOT, "assets", "images", "banner.png")
        if os.path.exists(banner_path):
            img = Image.open(banner_path)
            self.banner_img = ImageTk.PhotoImage(img)
            tk.Label(self, image=self.banner_img, bg="#142336").pack(fill="x")

        # Contenedor principal
        container = tk.Frame(self, bg="#142336")
        container.pack(fill="both", expand=True, padx=10, pady=10)

        left = tk.Frame(container, bg="#142336")
        left.pack(side="left", fill="y", padx=(0,10))

        right = tk.Frame(container, bg="#142336")
        right.pack(side="right", fill="both", expand=True)

        # Reader setup
        self.reader = BibleReader(os.path.join(ROOT, "data", "biblia_demo.json"))
        self.audio = AudioReader()
        self.devo = Devocionales(os.path.join(ROOT, "data", "devocionales.json"))

        # Área de texto principal
        self.text_area = tk.Text(right, bg="#0E1A2A", fg="#FFFFFF", font=("Segoe UI", 12), wrap="word")
        self.text_area.pack(fill="both", expand=True)

        # Devocional del día
        devo_frame = tk.LabelFrame(left, text="Devocional de hoy", fg="#D4AF37", bg="#142336", labelanchor="n", font=("Segoe UI", 11, "bold"))
        devo_frame.pack(anchor="w", fill="x", pady=12)
        self.devo_text = tk.Text(devo_frame, height=12, width=36, bg="#0E1A2A", fg="#FFFFFF", wrap="word", font=("Segoe UI", 10))
        self.devo_text.pack(padx=6, pady=6)
        self.load_devo()

        # Botones principales
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", background="#D4AF37", foreground="#142336", font=("Segoe UI", 11, "bold"))
        style.map("TButton",
                  background=[("active", "#E5C158")],
                  foreground=[("active", "#000000")])

        ttk.Button(left, text="📖 Leer Juan 3", command=self.show_text).pack(anchor="w", pady=(10,4))
        ttk.Button(left, text="🔊 Audio", command=self.read_audio).pack(anchor="w")

        # Búsqueda de versículos
        search_frame = tk.LabelFrame(left, text="Buscar versículo", fg="#D4AF37", bg="#142336", font=("Segoe UI", 11, "bold"))
        search_frame.pack(anchor="w", fill="x", pady=12)
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, width=25).pack(padx=6, pady=4)
        ttk.Button(search_frame, text="Buscar", command=self.search_text).pack(pady=4)

        # Planes de lectura (demo)
        plan_frame = tk.LabelFrame(left, text="Plan de lectura", fg="#D4AF37", bg="#142336", font=("Segoe UI", 11, "bold"))
        plan_frame.pack(anchor="w", fill="x", pady=12)
        self.plan_text = tk.Text(plan_frame, height=8, width=36, bg="#0E1A2A", fg="#FFFFFF", wrap="word", font=("Segoe UI", 10))
        self.plan_text.pack(padx=6, pady=6)
        self.plan_text.insert(tk.END, "Plan demo:\nDía 1: Génesis 1\nDía 2: Juan 3")

        # Notas personales
        notes_frame = tk.LabelFrame(left, text="Notas personales", fg="#D4AF37", bg="#142336", font=("Segoe UI", 11, "bold"))
        notes_frame.pack(anchor="w", fill="x", pady=12)
        self.notes_text = tk.Text(notes_frame, height=8, width=36, bg="#0E1A2A", fg="#FFFFFF", wrap="word", font=("Segoe UI", 10))
        self.notes_text.pack(padx=6, pady=6)
        ttk.Button(notes_frame, text="Guardar notas", command=self.save_notes).pack(pady=4)

        # Status bar
        self.status = tk.StringVar(value="Listo")
        status_bar = tk.Label(self, textvariable=self.status, bg="#0E1A2A", fg="#D4AF37", font=("Segoe UI", 10))
        status_bar.pack(fill="x")

    def load_devo(self):
        d = self.devo.hoy()
        if d:
            content = f"{d['titulo']}\n{d['versiculo']}\n\n{d['texto']}\n\nAplicación:\n{d['reflexion']}"
            self.devo_text.delete("1.0", tk.END)
            self.devo_text.insert(tk.END, content)

    def show_text(self):
        txt = self.reader.get_text("Juan","3")
        self.text_area.delete("1.0", tk.END)
        for v, t in txt.items():
            self.text_area.insert(tk.END, f"{v}. {t}\n")
        self.status.set("Mostrando Juan 3")

    def read_audio(self):
        current = self.text_area.get("1.0", tk.END).strip()
        if not current:
            self.show_text()
            current = self.text_area.get("1.0", tk.END).strip()
        if not current:
            messagebox.showinfo(APP_TITLE, "No hay texto para leer.")
            return
        self.audio.speak(current)
        self.status.set("Leyendo en voz alta...")

    def search_text(self):
        query = self.search_var.get().lower()
        results = []
        for book in self.reader.get_books():
            for ch in self.reader.get_chapters(book):
                verses = self.reader.get_text(book, ch)
                for v, t in verses.items():
                    if query in t.lower():
                        results.append(f"{book} {ch}:{v} - {t}")
        self.text_area.delete("1.0", tk.END)
        if results:
            self.text_area.insert(tk.END, "\n".join(results))
            self.status.set(f"Resultados para '{query}'")
        else:
            self.text_area.insert(tk.END, "No se encontraron resultados.")
            self.status.set("Sin resultados")

    def save_notes(self):
        notes = self.notes_text.get("1.0", tk.END).strip()
        path = os.path.join(ROOT, "data", "notas.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(notes)
        self.status.set("Notas guardadas en data/notas.txt")

def main():
    app = BibliaApp()
    app.mainloop()

if __name__ == "__main__":
    main()
