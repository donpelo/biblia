import tkinter as tk
from gui.controlador import leer_actual, siguiente

FONT_TITLE = ("Helvetica", 16, "bold")
FONT_TEXT = ("Helvetica", 12)
FONT_BUTTON = ("Helvetica", 11)

root = tk.Tk()
root.title("Biblia Interactiva v2.0")
root.geometry("900x600")
root.configure(bg="#1e1e1e")

titulo = tk.Label(
    root,
    text="Biblia Interactiva",
    font=FONT_TITLE,
    bg="#1e1e1e",
    fg="white"
)
titulo.pack(pady=20)

texto = tk.Label(
    root,
    text="",
    font=FONT_TEXT,
    wraplength=800,
    justify="left",
    bg="#1e1e1e",
    fg="white"
)
texto.pack(pady=10)

btn = tk.Button(
    root,
    text="Siguiente",
    font=FONT_BUTTON,
    command=siguiente
)
btn.pack(pady=20)

root.mainloop()
