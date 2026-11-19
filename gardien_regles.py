"""Agent 9 — Gardien des règles : protège la chaîne et sa monétisation.
Il vérifie que chaque vidéo respecte les règles YouTube (contenu original, variété,
réglage « conçu pour les enfants », titres honnêtes) AVANT tout envoi.
Il ne contourne aucun contrôle : il bloque ce qui pourrait mettre la chaîne en danger."""
from .compositeur import PUBLIC_DOMAIN

BANNED_WORDS = ["guaranteed", "100%", "instantly", "cure", "medical", "doctor recommended", "cocomelon",
                "super simple", "baby shark", "disney", "pinkfong", "little baby bum"]


def check(plan, metas, memory, cfg):
    issues, notes = [], []
    used = memory.used_titles()
    for kind, m in metas:
        t = m["title"].lower(); d = m["description"].lower()
        if len(m["title"]) > 100:
            issues.append(f"{kind} : titre trop long ({len(m['title'])} caractères).")
        if m["title"] in used:
            issues.append(f"{kind} : titre déjà utilisé auparavant.")
        for w in BANNED_WORDS:
            if w in t or w in d:
                issues.append(f"{kind} : mot interdit ou trompeur « {w} » (marque d'un tiers ou promesse).")
    for tr in plan["tracks"]:
        kind, name = tr["item"]
        if kind == "pd" and name not in PUBLIC_DOMAIN:
            issues.append(f"Morceau « {name} » hors de la liste du domaine public autorisée.")
    if plan["long_theme"] in memory.recent_themes(days=2):
        if cfg["long_theme"]:
            notes.append("Décor de la vidéo longue imposé par toi et déjà utilisé récemment : varie-le de temps en temps.")
        else:
            issues.append("Le thème de la vidéo longue a déjà été utilisé ces 2 derniers jours.")
    if len({s["theme"] for s in plan["shorts"]}) < len(plan["shorts"]):
        notes.append("Certains Shorts partagent le même décor (pas assez de décors autorisés dans consignes.yml). "
                     "Plus de variété protège ta monétisation.")
    notes.append("Toutes les musiques sont soit composées par le système, soit des arrangements nouveaux de mélodies du domaine public.")
    notes.append("Réglage « conçue pour les enfants » : OUI (obligatoire pour ce contenu).")
    return issues, notes
