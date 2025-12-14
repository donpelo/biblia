def cargar_libro(nombre):
    with open(f"data/biblia/{nombre}.txt", encoding="utf8") as f:
        return f.read()
