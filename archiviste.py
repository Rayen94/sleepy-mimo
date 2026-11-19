"""Agent 11 — Archiviste : mémoire de la chaîne (historique de tout ce qui a été produit)."""
import json, os, datetime

PATH = "history.json"


class Memory:
    def __init__(self, path=PATH):
        self.path = path
        self.data = json.load(open(path)) if os.path.exists(path) else {"days": []}

    def recent_themes(self, days=2):
        return {d["long"]["theme"] for d in self.data["days"][-days:]}

    def used_titles(self):
        out = set()
        for d in self.data["days"]:
            out.add(d["long"]["title"]); out.update(s["title"] for s in d["shorts"])
        return out

    def used_original_names(self):
        out = set()
        for d in self.data["days"]:
            out.update(d["long"].get("originals", [])); out.update(s["song"] for s in d["shorts"])
        return out

    def add_day(self, entry):
        self.data["days"] = [d for d in self.data["days"] if d["date"] != entry["date"]] + [entry]
        json.dump(self.data, open(self.path, "w"), indent=1, ensure_ascii=False)
