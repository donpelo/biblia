import json

CONFIG_PATH = "config.json"
BIBLIA_PATH = "data/biblia_es.json"

def _cargar_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def _guardar_config(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

def _cargar_biblia():
    with open(BIBLIA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def obtener_actual():
    cfg = _cargar_config()
    biblia = _cargar_biblia()

    libro = cfg.get("last_book", "Ejemplo")
    cap = str(cfg.get("last_chapter", 1))
    vers = str(cfg.get("last_verse", 1))

    texto = biblia["chapters"][cap][vers]
    return f"{libro} {cap}:{vers}\n\n{texto}"

def avanzar():
    cfg = _cargar_config()
    biblia = _cargar_biblia()

    cap = str(cfg.get("last_chapter", 1))
    vers = int(cfg.get("last_verse", 1)) + 1

    if str(vers) not in biblia["chapters"][cap]:
        vers = 1
        cap = str(int(cap) + 1)

    cfg["last_chapter"] = int(cap)
    cfg["last_verse"] = vers
    _guardar_config(cfg)

    return obtener_actual()
