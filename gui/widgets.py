import tkinter as tk
from gui.theme import THEME

class GoldButton(tk.Button):
    def __init__(self, master, **kw):
        super().__init__(
            master,
            bg=THEME["accent"],
            fg=THEME["fg"],
            font=THEME["font"],
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            **kw
        )
