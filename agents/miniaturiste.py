"""Agent 7 — Miniaturiste : crée une miniature lisible et différente pour chaque vidéo longue."""
from .illustrateur import thumbnail, THEMES

LINES = {"moon": ("MOONLIGHT", "LULLABIES"), "clouds": ("DREAMY", "LULLABIES"), "ocean": ("OCEAN", "LULLABIES"),
         "snow": ("SNOWY NIGHT", "LULLABIES"), "forest": ("FIREFLY", "LULLABIES"), "rain": ("RAINY NIGHT", "LULLABIES")}


def make(theme, minutes, path, seed):
    big = f"{minutes} MIN" if minutes < 60 else f"{minutes // 60} HOUR" + ("S" if minutes >= 120 else "")
    l1, l2 = LINES[theme]
    thumbnail(theme, big, l1, l2, path, seed)
    return path



def make_episode(ep, number, path):
    """Miniature d'épisode : décor coloré, les personnages de l'épisode en grand, « EPISODE N » et le titre."""
    import cairosvg
    from . import decors as D, personnages as PE, illustrateur as I
    W, H = 1280, 720
    chap = ep["chapters"][0]
    decors = [sh["decor"] for ch in ep["chapters"] for sh in ch["story"]]
    decor = next((d for d in decors if d in ("meadow", "clouds", "forest")), decors[0])
    cast = []
    for ch in ep["chapters"]:
        for sh in ch["story"]:
            for (c, *_r) in sh["cast"]:
                if c not in cast:
                    cast.append(c)
    cast = (["mimo"] + [c for c in cast if c != "mimo"])[:4]
    body = [D.DECORS[decor](0.2, 3)]
    xs = {1: [330], 2: [250, 470], 3: [170, 370, 570], 4: [130, 300, 470, 640]}[len(cast)]
    for i, (c, x) in enumerate(zip(cast, xs)):
        s = 1.25 if c == "mimo" else 1.0
        y = 300 if c == "star" else D.GROUND + 40 - 134 * s
        body.append(PE.draw(c, x, y, s, mouth=0.55 if c == "mimo" else 0.0, wave=1.0 if i == 0 else 0.0))
    body.append('<rect x="760" y="0" width="520" height="720" fill="#1B1550" opacity="0.35"/>')
    body.append(I.text(1020, 150, f"EPISODE {number}", 70, "#FFE37A"))
    words, rows, cur = ep["title"].upper().split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > 11 and cur:
            rows.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    rows.append(cur)
    size = 92 if max(len(r) for r in rows) <= 9 else 76
    for i, r in enumerate(rows[:3]):
        body.append(I.text(1020, 290 + i * (size + 14), r, size, "#FFFFFF"))
    body.append(I.text(1020, 660, "Sleepy Mimo", 48, "#FFD1E8", 700))
    cairosvg.svg2png(bytestring=I.svg(W, H, "".join(body)).encode(), write_to=path)
    return path
