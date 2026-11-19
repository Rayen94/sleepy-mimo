"""Agent 8 — Contrôleur qualité : vérifie techniquement chaque fichier avant publication."""
import os
from .monteur import duration, loudness


def check_video(path, expected_seconds, vertical=False, tolerance=0.1):
    problems = []
    if not os.path.exists(path):
        return [f"Fichier manquant : {path}"], {}
    d = duration(path)
    if abs(d - expected_seconds) > expected_seconds * tolerance + 3:
        problems.append(f"Durée inattendue : {d:.0f}s au lieu d'environ {expected_seconds:.0f}s.")
    if vertical and d > 180:
        problems.append("Short trop long (plus de 3 minutes).")
    mean, maxv = loudness(path)
    if mean is None or mean < -32:
        problems.append(f"Son trop faible (moyenne {mean} dB).")
    if maxv is not None and maxv > -0.5:
        problems.append(f"Son qui sature (pic {maxv} dB).")
    size = os.path.getsize(path) / 1e6
    return problems, dict(duree=round(d), volume_moyen=mean, pic=maxv, taille_mo=round(size, 1))
