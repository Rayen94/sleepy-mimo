"""Fusionne la mémoire de la série : garde tous les épisodes déjà enregistrés + ceux de cette production."""
import json, sys

src, dst = sys.argv[1], sys.argv[2]


def load(p):
    try:
        return json.load(open(p)).get("days", [])
    except Exception:
        return []


key = lambda d: (d.get("date"), (d.get("long") or {}).get("episode"))
import os

run = os.environ.get("GITHUB_RUN_ID")
merged = {key(d): d for d in load(dst)}
for d in load(src):
    # on n'ajoute que ce que CETTE production a créé (pas une ancienne copie de la mémoire)
    if run is None or d.get("run") == run or key(d) not in merged:
        merged[key(d)] = d
days = sorted(merged.values(), key=lambda d: (d.get("date", ""), (d.get("long") or {}).get("episode") or 0))
json.dump({"days": days}, open(dst, "w"), indent=1, ensure_ascii=False)
