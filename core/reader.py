import json
class BibleReader:
    def __init__(self, path):
        with open(path, "r", encoding="utf-8") as f:
            self.data = json.load(f)
    def get_books(self): return list(self.data.keys())
    def get_chapters(self, book): return list(self.data.get(book, {}).keys())
    def get_text(self, book, chapter): return self.data.get(book, {}).get(chapter, {})
