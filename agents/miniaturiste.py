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
    from . import style
    wild = style.s2()
    cast = (["mimo"] + [c for c in cast if c != "mimo"])[: 2 if wild else 4]
    if wild:
        decor = next((d for d in decors if d not in ("den", "cave", "rain_night")), decors[0])
    body = [D.DECORS[decor](0.2, 3)]
    xs = {1: [330], 2: [250, 470], 3: [170, 370, 570], 4: [130, 300, 470, 640]}[len(cast)]
    if wild:
        xs = {1: [380], 2: [190, 560], 3: [190, 480, 710]}[len(cast)]
    for i, (c, x) in enumerate(zip(cast, xs)):
        s = 1.25 if c == "mimo" else 1.0
        if wild:
            s = 1.85 if c == "mimo" else 1.6
        y = 300 if c in ("star", "bat") and not wild else (330 if c == "bat" else D.ground(decor) + 40 - 134 * s) if wild else (300 if c == "star" else D.GROUND + 40 - 134 * s)
        body.append(PE.draw(c, x, y, s, mouth=0.55 if c == "mimo" else 0.0, wave=1.0 if i == 0 else 0.0))
    if wild:
        body.append(D.foreground(decor, 0.2))
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
    if len(rows) > 3:                       # titre long : 4 lignes plus petites (jamais de mot coupé)
        size = 64
    step = size + 12
    top = 270 if len(rows) <= 3 else 235
    for i, r in enumerate(rows[:4]):
        body.append(I.text(1020, top + i * step, r, size, "#FFFFFF"))
    body.append(I.text(1020, 660, "Sleepy Mimo", 48, "#FFD1E8", 700))
    cairosvg.svg2png(bytestring=I.svg(W, H, "".join(body)).encode(), write_to=path)
    if wild:                                # miniature plus lumineuse et plus riche : elle doit « sortir » d'une liste claire
        _brighten(path)
    return path


def _brighten(path):
    from PIL import Image, ImageEnhance
    im = Image.open(path).convert("RGB")
    im = im.point(lambda v: int(255 * (v / 255.0) ** 0.78))          # relève les ombres
    im = ImageEnhance.Color(im).enhance(1.22)
    im = ImageEnhance.Contrast(im).enhance(1.08)
    im.save(path)
