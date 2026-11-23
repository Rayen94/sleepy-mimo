"""Agent 11 — Archiviste : mémoire de la chaîne (historique de tout ce qui a été produit)."""
import json, os, datetime

PATH = "history.json"


class Memory:
    def __init__(self, path=PATH):
        self.path = path
        self.data = json.load(open(path)) if os.path.exists(path) else {"days": []}

    def recent_themes(self, days=2):
        return {d["long"]["theme"] for d in self.data["days"][-days:]}

    def recent_stories(self, days=3):
        return {d["long"].get("story") for d in self.data["days"][-days:] if d["long"].get("story")}

    def next_episode(self):
        eps = [d["long"].get("episode", 0) or 0 for d in self.data["days"]]
        return (max(eps) if eps else 0) + 1

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
        ep = entry.get("long", {}).get("episode")
        self.data["days"] = [d for d in self.data["days"]
                             if not (d["date"] == entry["date"] and d.get("long", {}).get("episode") == ep)] + [entry]
        json.dump(self.data, open(self.path, "w"), indent=1, ensure_ascii=False)
