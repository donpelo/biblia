import tkinter as tk
from tkinter import ttk
from core.reader import BibleReader
from core.audio import AudioReader
from core.devocionales import Devocionales

class BibliaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BibliaInteractiva")
        self.geometry("800x600")
        self.reader = BibleReader("data/biblia_demo.json")
        self.audio = AudioReader()
        self.devo = Devocionales("data/devocionales.json")

        self.text = tk.Text(self, wrap="word")
        self.text.pack(fill="both", expand=True)

        btn = ttk.Button(self, text="Leer Juan 3", command=self.show_text)
        btn.pack(pady=10)
        btn2 = ttk.Button(self, text="Audio", command=self.read_audio)
        btn2.pack()

    def show_text(self):
        txt = self.reader.get_text("Juan","3")
        self.text.delete("1.0", tk.END)
        for v, t in txt.items():
            self.text.insert(tk.END, f"{v}. {t}\n")

    def read_audio(self):
        self.audio.speak(self.text.get("1.0", tk.END))

if __name__ == "__main__":
    app = BibliaApp()
    app.mainloop()
