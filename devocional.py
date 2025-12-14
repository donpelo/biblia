import random
import datetime

def versiculo_del_dia(biblia, config):
    hoy = datetime.date.today().isoformat()

    if config.get("last_devotional_date") == hoy:
        cap = str(config["last_chapter"])
        ver = str(config["last_verse"])
        return cap, ver, biblia["chapters"][cap][ver]

    cap = random.choice(list(biblia["chapters"].keys()))
    ver = random.choice(list(biblia["chapters"][cap].keys()))

    config["last_chapter"] = int(cap)
    config["last_verse"] = int(ver)
    config["last_devotional_date"] = hoy

    return cap, ver, biblia["chapters"][cap][ver]