"""Lit le panneau de commande (consignes.yml) et traduit tes ordres pour l'équipe.
Si une consigne est mal écrite, l'équipe garde la valeur par défaut et le signale dans le rapport."""
import os, yaml

DECORS = {"lune": "moon", "nuages": "clouds", "ocean": "ocean", "océan": "ocean", "neige": "snow",
          "lucioles": "forest", "pluie": "rain"}
INSTRUMENTS = {"boite_a_musique": "box", "piano": "soft", "harpe": "harp", "clochettes": "bell"}
COMPTINES = {"twinkle": "Twinkle Twinkle Little Star", "frere_jacques": "Are You Sleeping (Frère Jacques)",
             "row_your_boat": "Row Row Row Your Boat", "brahms": "Brahms' Lullaby",
             "mary_lamb": "Mary Had a Little Lamb", "london_bridge": "London Bridge"}
OUI = {"oui", "yes", "true", True, 1, "1"}


def load(path="consignes.yml"):
    warnings = []
    raw = {}
    if os.path.exists(path):
        try:
            raw = yaml.safe_load(open(path, encoding="utf-8")) or {}
        except Exception as e:
            warnings.append(f"Le fichier consignes.yml est mal écrit ({e}). Valeurs par défaut utilisées.")

    def num(key, default, lo, hi):
        v = raw.get(key, default)
        try:
            v = float(v)
        except (TypeError, ValueError):
            warnings.append(f"« {key} » n'est pas un nombre : {default} utilisé."); return default
        if not lo <= v <= hi:
            warnings.append(f"« {key} » doit être entre {lo} et {hi} : ramené dans les limites.")
            v = min(max(v, lo), hi)
        return v

    def mapped(key, table, default):
        v = raw.get(key)
        if v is None:
            return list(default)
        out = []
        for x in (v if isinstance(v, list) else [v]):
            k = str(x).strip().lower()
            if k in table: out.append(table[k])
            else: warnings.append(f"« {x} » inconnu dans « {key} » (ignoré).")
        if not out:
            warnings.append(f"« {key} » est vide : tout est autorisé."); return list(default)
        return list(dict.fromkeys(out))

    cfg = dict(
        pause=str(raw.get("pause", "non")).lower() in OUI or raw.get("pause") is True,
        upload=(str(raw.get("envoyer_sur_youtube", "oui")).lower() in OUI) or raw.get("envoyer_sur_youtube") is True,
        auto_publish=(str(raw.get("publication_automatique", "non")).lower() in OUI) or raw.get("publication_automatique") is True,
        publish_hour=num("heure_publication", 17, 0, 23),
        long_minutes=num("duree_video_longue_minutes", 60, 5, 180),
        scene_minutes=num("changer_de_decor_toutes_les_minutes", 15, 5, 180),
        ambience=not (str(raw.get("sons_ambiance", "oui")).lower() in {"non", "no", "false"} or raw.get("sons_ambiance") is False),
        hooks=[],
        story=not (str(raw.get("histoire", "oui")).lower() in {"non", "no", "false"} or raw.get("histoire") is False),
        vocals=not (str(raw.get("voix_chantee", "oui")).lower() in {"non", "no", "false"} or raw.get("voix_chantee") is False),
        intro=not (str(raw.get("intro_sleepy_mimo", "oui")).lower() in {"non", "no", "false"} or raw.get("intro_sleepy_mimo") is False),
        short_seconds=num("duree_shorts_secondes", 45, 15, 170),
        n_shorts=int(num("nombre_shorts", 3, 0, 5)),
        themes=mapped("decors_autorises", DECORS, set(DECORS.values())),
        voices=mapped("instruments_autorises", INSTRUMENTS, INSTRUMENTS.values()),
        songs=mapped("comptines_autorisees", COMPTINES, COMPTINES.values()),
        original_pct=num("pourcentage_originales", 35, 0, 100),
        extra_tags=[str(t) for t in (raw.get("tags_en_plus") or [])][:10],
        overlays=[],
        long_theme=None,
    )
    dl = raw.get("decor_video_longue")
    if dl:
        k = str(dl).strip().lower()
        if k in DECORS: cfg["long_theme"] = DECORS[k]
        else: warnings.append(f"Décor imposé « {dl} » inconnu : le Stratège choisit.")
    for t in raw.get("textes_shorts") or []:
        if isinstance(t, list) and len(t) == 2 and all(len(str(x)) <= 22 for x in t):
            cfg["overlays"].append([str(t[0]), str(t[1])])
        else:
            warnings.append(f"Texte de Short « {t} » ignoré (il faut 2 lignes de 22 caractères maximum).")
    for t in raw.get("accroches_shorts") or []:
        if isinstance(t, list) and len(t) == 2 and all(len(str(x)) <= 18 for x in t):
            cfg["hooks"].append([str(t[0]), str(t[1])])
        else:
            warnings.append(f"Accroche « {t} » ignorée (il faut 2 lignes de 18 caractères maximum).")
    if not cfg["hooks"]:
        cfg["hooks"] = [["Shhh...", "Mimo is sleeping"], ["Play this for", "your baby"], ["Bedtime with", "Mimo"]]
    if not cfg["overlays"]:
        cfg["overlays"] = [["Sleep tight,", "little one"], ["Time to sleep,", "little star"]]
    if os.environ.get("SHORTS_OVERRIDE", "").strip().isdigit():
        cfg["n_shorts"] = max(0, min(5, int(os.environ["SHORTS_OVERRIDE"])))
    for k in ("LONG_MINUTES", "SHORT_SECONDS"):
        if os.environ.get(k):  # pour les tests uniquement
            cfg["long_minutes" if k == "LONG_MINUTES" else "short_seconds"] = float(os.environ[k])
    return cfg, warnings
