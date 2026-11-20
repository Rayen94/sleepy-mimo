"""Agent 7 — Miniaturiste : crée une miniature lisible et différente pour chaque vidéo longue."""
from .illustrateur import thumbnail, THEMES

LINES = {"moon": ("MOONLIGHT", "LULLABIES"), "clouds": ("DREAMY", "LULLABIES"), "ocean": ("OCEAN", "LULLABIES"),
         "snow": ("SNOWY NIGHT", "LULLABIES"), "forest": ("FIREFLY", "LULLABIES"), "rain": ("RAINY NIGHT", "LULLABIES")}


def make(theme, minutes, path, seed):
    big = f"{minutes} MIN" if minutes < 60 else f"{minutes // 60} HOUR" + ("S" if minutes >= 120 else "")
    l1, l2 = LINES[theme]
    thumbnail(theme, big, l1, l2, path, seed)
    return path
