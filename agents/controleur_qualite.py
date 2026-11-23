"""Agent 8 — Contrôleur qualité : vérifie techniquement chaque fichier avant publication."""
import os, json, subprocess
from .monteur import duration, loudness


def video_info(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                          "-of", "json", path], capture_output=True, text=True).stdout
    st = (json.loads(out or "{}").get("streams") or [{}])[0]
    return st.get("width"), st.get("height")


def decodes(path, start, seconds=15):
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(max(0, start)), "-t", str(seconds), "-i", path, "-f", "null", "-"],
                       capture_output=True, text=True)
    return p.returncode == 0 and not p.stderr.strip()


def check_video(path, expected_seconds, vertical=False, tolerance=0.1):
    problems = []
    if not os.path.exists(path):
        return [f"Fichier manquant : {path}"], {}
    d = duration(path)
    if abs(d - expected_seconds) > expected_seconds * tolerance + 3:
        problems.append(f"Durée inattendue : {d:.0f}s au lieu d'environ {expected_seconds:.0f}s.")
    w, h = video_info(path)
    if not w:
        problems.append("Aucune image dans la vidéo.")
    elif vertical and not h > w:
        problems.append(f"Le Short n'est pas vertical ({w}x{h}).")
    elif not vertical and w < 1280:
        problems.append(f"Résolution trop basse ({w}x{h}).")
    if not (decodes(path, 0) and decodes(path, d - 15)):
        problems.append("La vidéo contient des images abîmées (début ou fin).")
    if vertical and d > 180:
        problems.append("Short trop long (plus de 3 minutes).")
    mean, maxv = loudness(path)
    if mean is None or mean < -32:
        problems.append(f"Son trop faible (moyenne {mean} dB).")
    if maxv is not None and maxv > -0.5:
        problems.append(f"Son qui sature (pic {maxv} dB).")
    size = os.path.getsize(path) / 1e6
    return problems, dict(resolution=f"{w}x{h}", duree=round(d), volume_moyen=mean, pic=maxv, taille_mo=round(size, 1))
