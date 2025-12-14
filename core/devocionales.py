import json, datetime
class Devocionales:
    def __init__(self, path):
        with open(path, "r", encoding="utf-8") as f:
            self.items = json.load(f)
    def hoy(self):
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        for d in self.items:
            if d["fecha"] == today: return d
        return self.items[0]
