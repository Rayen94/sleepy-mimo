"""Saison 2 — décors en plusieurs plans (parallaxe), avec lune, rayons de lumière, brume, lucioles et feuilles.
Repère 1280x720 comme decors.py. Chaque fonction : decor(t, seed, cam) ; t boucle de 0 à 1 (16 s), cam = (cx, cy, zoom) ou None.
Les plans lointains bougent peu quand la caméra se déplace, les plans proches bougent plus : ça donne de la profondeur."""
import math, random

GROUND = 600


def _px(cam, f):
    """Décalage horizontal d'un plan selon la caméra (f = 0 plan lointain, 1 plan proche)."""
    return 0.0 if cam is None else (cam[0] - 640) * -0.32 * f


def _g(gid, stops, vertical=True, radial=False):
    s = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
    if radial:
        return f'<radialGradient id="{gid}" cx="0.5" cy="0.5" r="0.5">{s}</radialGradient>'
    xy = 'x1="0" y1="0" x2="0" y2="1"' if vertical else 'x1="0" y1="0" x2="1" y2="0"'
    return f'<linearGradient id="{gid}" {xy}>{s}</linearGradient>'


def _tree(x, base, h, w, col, crown, sway):
    top = base - h
    return (f'<g transform="rotate({sway:.2f} {x:.1f} {base:.1f})"><path d="M{x - w/2:.1f} {base} Q{x - w*0.35:.1f} {base - h*0.5:.1f} {x - w*0.18:.1f} {top} L{x + w*0.18:.1f} {top} Q{x + w*0.35:.1f} {base - h*0.5:.1f} {x + w/2:.1f} {base}Z" fill="{col}"/>'
            f'<ellipse cx="{x:.1f}" cy="{top:.1f}" rx="{w*2.2:.1f}" ry="{w*1.5:.1f}" fill="{crown}"/>'
            f'<ellipse cx="{x - w*1.1:.1f}" cy="{top + w*0.5:.1f}" rx="{w*1.5:.1f}" ry="{w*1.0:.1f}" fill="{crown}"/>'
            f'<ellipse cx="{x + w*1.2:.1f}" cy="{top + w*0.45:.1f}" rx="{w*1.5:.1f}" ry="{w*1.0:.1f}" fill="{crown}"/></g>')


def _fern(x, y, s, col, t, ph):
    sw = 4 * math.sin(2 * math.pi * t + ph)
    leaves = ""
    for k in range(-3, 4):
        a = k * 0.42
        ex, ey = x + math.sin(a) * 120 * s + sw * (1 + abs(k) * 0.3), y - math.cos(a) * 90 * s
        leaves += f'<path d="M{x:.1f} {y:.1f} Q{x + math.sin(a) * 60 * s:.1f} {y - 80 * s:.1f} {ex:.1f} {ey:.1f} Q{x + math.sin(a) * 50 * s + 9 * s:.1f} {y - 60 * s:.1f} {x:.1f} {y:.1f}Z" fill="{col}"/>'
    return leaves


def moon_glow(cx, cy, r):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r*4.2:.0f}" fill="url(#moonhalo)"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#FFF6DA"/>'
            f'<circle cx="{cx - r*0.3:.0f}" cy="{cy - r*0.15:.0f}" r="{r*0.22:.0f}" fill="#EBDDB5" opacity="0.7"/>'
            f'<circle cx="{cx + r*0.28:.0f}" cy="{cy + r*0.3:.0f}" r="{r*0.16:.0f}" fill="#EBDDB5" opacity="0.6"/>')


def rays(cx, cy, t, n=5):
    out = []
    for i in range(n):
        a = math.radians(98 + i * 11 - 22)
        w = 36 + 10 * (i % 3)
        x2, y2 = cx + math.cos(a) * 900, cy + math.sin(a) * 900
        nx, ny = -math.sin(a) * w, math.cos(a) * w
        op = 0.05 + 0.035 * math.sin(2 * math.pi * (t + i / n))
        out.append(f'<path d="M{cx:.0f} {cy:.0f} L{x2 + nx:.0f} {y2 + ny:.0f} L{x2 - nx:.0f} {y2 - ny:.0f}Z" fill="url(#rayfade)" opacity="{max(0.0, op) * 2.4:.3f}"/>')
    return "".join(out)


def mist(t, y, op, cam, f, bands=3):
    out = []
    for i in range(bands):
        x = 200 + i * 420 + 60 * math.sin(2 * math.pi * (t + i / bands)) + _px(cam, f)
        out.append(f'<ellipse cx="{x:.0f}" cy="{y + 14 * math.sin(2 * math.pi * (t * 2 + i)):.0f}" rx="420" ry="46" fill="url(#mistg)" opacity="{op}"/>')
    return "".join(out)


def fireflies(t, seed, cam, n=16):
    r = random.Random(seed * 7 + 1)
    out = []
    for i in range(n):
        x0, y0 = r.uniform(60, 1220), r.uniform(330, 640)
        ax, ay = r.uniform(30, 90), r.uniform(14, 50)
        k, ph = r.choice([1, 2]), r.uniform(0, 6.28)
        x = x0 + ax * math.sin(2 * math.pi * k * t + ph) + _px(cam, 0.8)
        y = y0 + ay * math.sin(2 * math.pi * (k + 1) * t + ph * 1.3)
        blink = 0.25 + 0.75 * max(0.0, math.sin(2 * math.pi * (2 * t + i * 0.37)))
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{16 * blink + 5:.1f}" fill="url(#ffglow)" opacity="{blink:.2f}"/>'
                   f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.4" fill="#FFFDD0" opacity="{min(1, blink + 0.3):.2f}"/>')
    return "".join(out)


def leaves(t, seed, cam):
    r = random.Random(seed * 5 + 3)
    out = []
    for i in range(9):
        x0, ph = r.uniform(0, 1280), r.uniform(0, 1)
        u = (t + ph) % 1.0
        x = (x0 + 140 * u + 30 * math.sin(2 * math.pi * (3 * u + i))) % 1280 + _px(cam, 0.9)
        y = -20 + 760 * u
        rot = 360 * u * (1 if i % 2 else -1)
        out.append(f'<g transform="translate({x:.1f} {y:.1f}) rotate({rot:.0f}) scale({0.7 + 0.5 * (i % 3) / 2:.2f})"><path d="M0 -9 Q8 0 0 9 Q-8 0 0 -9Z" fill="{["#C9A24A", "#8DBF6B", "#D9833F"][i % 3]}" opacity="0.8"/></g>')
    return "".join(out)


DEFS = ('<defs>' + _g("sky_f2", [(0, "#070E26", 1), (0.55, "#17365A", 1), (1, "#2F6A78", 1)])
        + _g("moonhalo", [(0, "#BFD8FF", 0.38), (0.35, "#8FB4F0", 0.14), (1, "#8FB4F0", 0)], radial=True)
        + _g("rayfade", [(0, "#DCEBFF", 1), (1, "#DCEBFF", 0)])
        + _g("mistg", [(0, "#BFD3EE", 0.0), (0.5, "#BFD3EE", 0.55), (1, "#BFD3EE", 0)], radial=True)
        + _g("ffglow", [(0, "#F7FF7A", 0.9), (0.4, "#C8F24A", 0.35), (1, "#C8F24A", 0)], radial=True)
        + _g("gr_f2", [(0, "#2B5A4A", 1), (0.35, "#1B3E36", 1), (1, "#0E2220", 1)])
        + _g("pool", [(0, "#BFD8FF", 0.35), (1, "#BFD8FF", 0)], radial=True)
        + '</defs>')


def forest_night(t, seed=1, cam=None):
    r = random.Random(seed)
    out = [DEFS, '<rect width="1280" height="720" fill="url(#sky_f2)"/>']
    for i in range(80):  # étoiles
        x, y = r.uniform(0, 1280), r.uniform(0, 330)
        a = 0.35 + 0.65 * abs(math.sin(2 * math.pi * t * r.choice([1, 2]) + i))
        out.append(f'<circle cx="{x + _px(cam, 0.05):.1f}" cy="{y:.1f}" r="{r.uniform(0.8, 2.2):.1f}" fill="#FFFFFF" opacity="{a:.2f}"/>')
    mx = 960 + _px(cam, 0.08)
    out.append(moon_glow(mx, 170, 62))
    # plan 1 : montagnes lointaines
    out.append(f'<g transform="translate({_px(cam, 0.12):.1f} 0)"><path d="M-80 470 L120 330 L260 410 L430 300 L610 420 L800 320 L980 430 L1160 340 L1360 460 L1360 720 L-80 720Z" fill="#14264A"/></g>')
    out.append(mist(t, 455, 0.5, cam, 0.15, 3))
    # plan 2 : grands arbres lointains
    out.append(f'<g transform="translate({_px(cam, 0.3):.1f} 0)">' + "".join(_tree(x, 520, 230 + 30 * ((x // 90) % 3), 26, "#0C1A33", "#0F2340", 1.2 * math.sin(2 * math.pi * t + x)) for x in range(-20, 1320, 135)) + '</g>')
    out.append(mist(t + 0.3, 520, 0.45, cam, 0.35, 3))
    out.append(rays(mx, 170, t))
    # plan 3 : arbres moyens
    out.append(f'<g transform="translate({_px(cam, 0.55):.1f} 0)">' + "".join(_tree(x, 585, 300 + 40 * ((x // 70) % 2), 36, "#0A1428", "#0D1D38", 1.6 * math.sin(2 * math.pi * t + x * 0.3)) for x in (60, 380, 760, 1130)) + '</g>')
    # sol : clair de lune sur l'herbe
    out.append(f'<path d="M-40 560 Q320 535 640 560 T1320 550 L1320 720 L-40 720Z" fill="url(#gr_f2)"/>')
    out.append(f'<ellipse cx="{mx - 150:.0f}" cy="640" rx="420" ry="55" fill="url(#pool)"/>')
    for i in range(34):  # brins d'herbe
        x, y = r.uniform(0, 1280), r.uniform(580, 715)
        h = 14 + (y - 580) * 0.14
        sw = 3 * math.sin(2 * math.pi * t + i)
        out.append(f'<path d="M{x:.1f} {y:.1f} q{sw / 2:.1f} {-h / 2:.1f} {sw:.1f} {-h:.1f}" stroke="#4E8C6A" stroke-width="2.2" fill="none" opacity="0.7"/>')
    for i, (x, y, c) in enumerate([(210, 640, "#9BE6FF"), (520, 690, "#FFE79B"), (910, 650, "#C7A8FF"), (1130, 700, "#9BE6FF")]):  # champignons / fleurs qui brillent
        g = 0.6 + 0.4 * math.sin(2 * math.pi * (t * 2 + i / 4))
        out.append(f'<circle cx="{x}" cy="{y - 8}" r="34" fill="url(#ffglow)" opacity="{0.55 * g:.2f}"/><rect x="{x - 2}" y="{y - 8}" width="4" height="14" fill="#CFE0D8"/><ellipse cx="{x}" cy="{y - 9}" rx="10" ry="6" fill="{c}" opacity="{0.55 + 0.4 * g:.2f}"/>')
    out.append(mist(t + 0.6, 628, 0.35, cam, 0.6, 3))
    return "".join(out)


def forest_night_front(t, seed=1, cam=None):
    """Premier plan, devant les personnages : fougères sombres, lucioles, feuilles qui tombent."""
    px = _px(cam, 1.0)
    return (fireflies(t, seed, cam) + leaves(t, seed, cam)
            + f'<g transform="translate({px:.1f} 0)">' + _fern(-10, 730, 1.5, "#0B1E1C", t, 0.0) + _fern(1290, 730, 1.6, "#0B1E1C", t, 2.0)
            + _fern(150, 745, 1.1, "#10302A", t, 1.0) + _fern(1140, 745, 1.0, "#10302A", t, 3.0) + '</g>')



# ---------------------------------------------------------------- moteur générique de paysages
def _pine(x, base, h, w, col, sway):
    tiers = ""
    for k in range(4):
        y = base - h * (0.15 + k * 0.23); ww = w * (1.5 - k * 0.28)
        tiers += f'<path d="M{x - ww:.1f} {y:.1f} L{x:.1f} {y - h * 0.32:.1f} L{x + ww:.1f} {y:.1f}Z" fill="{col}"/>'
    return (f'<g transform="rotate({sway:.2f} {x:.1f} {base:.1f})"><rect x="{x - w*0.12:.1f}" y="{base - h*0.2:.1f}" width="{w*0.24:.1f}" height="{h*0.2:.1f}" fill="{col}"/>{tiers}</g>')


def _bare(x, base, h, w, col, sway):
    d = f"M{x} {base} L{x} {base - h * 0.55}"
    for k, (dx, dy) in enumerate([(-0.5, 0.7), (0.55, 0.78), (-0.3, 0.95), (0.35, 1.0)]):
        d += f" M{x} {base - h * (0.3 + k * 0.12):.1f} L{x + dx * h * 0.45:.1f} {base - h * dy:.1f}"
    return f'<g transform="rotate({sway:.2f} {x:.1f} {base:.1f})"><path d="{d}" stroke="{col}" stroke-width="{w * 0.35:.1f}" fill="none" stroke-linecap="round"/></g>'


def _reeds(x, y, s, col, t, ph):
    d = ""
    for k in range(-2, 3):
        sw = 6 * math.sin(2 * math.pi * t + ph + k)
        d += f"M{x + k * 9 * s:.1f} {y} Q{x + k * 9 * s + sw / 2:.1f} {y - 70 * s:.1f} {x + k * 12 * s + sw:.1f} {y - 130 * s:.1f}"
    top = "".join(f'<ellipse cx="{x + k * 12 * s + 6 * math.sin(2 * math.pi * t + ph + k):.1f}" cy="{y - 128 * s:.1f}" rx="{4 * s:.1f}" ry="{14 * s:.1f}" fill="#5A3F2A"/>' for k in (-1, 1))
    return f'<path d="{d}" stroke="{col}" stroke-width="{3.2 * s:.1f}" fill="none" stroke-linecap="round"/>{top}'


def rain(t, op=0.5):
    out = []
    for i in range(70):
        x = (i * 97) % 1380 - 60 + 40 * ((t * 3) % 1)
        y = ((i * 53) % 740 + 740 * ((t * 2 + i * 0.013) % 1)) % 760 - 20
        out.append(f"M{x:.0f} {y:.0f} l-9 26")
    return f'<path d="{"".join(out)}" stroke="#B8D0F0" stroke-width="1.6" opacity="{op}" fill="none"/>'


def snow(t, seed, cam, n=70):
    r = random.Random(seed * 3 + 1); out = []
    for i in range(n):
        x0, ph, sz = r.uniform(0, 1280), r.uniform(0, 1), r.uniform(1.6, 4.2)
        u = (t * (1 + (i % 2)) + ph) % 1.0
        x = (x0 + 50 * math.sin(2 * math.pi * (t + ph)) + 90 * u) % 1280 + _px(cam, 0.9 * sz / 4)
        out.append(f'<circle cx="{x:.1f}" cy="{-10 + 740 * u:.1f}" r="{sz:.1f}" fill="#FFFFFF" opacity="{0.55 + 0.4 * (sz / 4.2):.2f}"/>')
    return "".join(out)


def _ridge(col, y, amp, seed, cam, f):
    r = random.Random(seed); d = f"M-80 720 L-80 {y}"
    x = -80
    while x < 1360:
        x += r.uniform(110, 210); d += f" L{x:.0f} {y - r.uniform(0.2, 1) * amp:.0f}"
    return f'<g transform="translate({_px(cam, f):.1f} 0)"><path d="{d} L1360 720Z" fill="{col}"/></g>'


SCENES = {
    # nom: ciel, astre, étoiles, crête lointaine, arbres (type, couleur tronc, couleur cime), sol, effets, eau, brume
    "meadow_night": dict(sky=("#0A1230", "#1E3C6A", "#5A6FA0"), moon=(900, 160, 58), stars=True, ridge="#162A52", trees=("round", "#0B1830", "#0E2040", (150, 700)),
                         ground=("#2F6A52", "#1F4A3E", "#0F2A26"), fx=("fireflies", "fireflies2"), flora="#FFE79B", ground_y=596, mist=0.4, grass="#5FA27A"),
    "river_night": dict(sky=("#08112E", "#1A3A66", "#4F78A8"), moon=(300, 150, 56), stars=True, ridge="#14284C", trees=("round", "#0A1630", "#0E1E3C", (60, 1180)),
                        ground=("#2C5A4C", "#1C4036", "#0E2622"), fx=("fireflies",), flora="#9BE6FF", ground_y=572, water=True, mist=0.45, grass="#4E8C6A", reeds=True),
    "snow_night": dict(sky=("#0B1636", "#2B4D86", "#8FB4DA"), moon=(980, 150, 54), stars=True, ridge="#2A4474", trees=("pine", "#12203C", "#16294A", (110, 430, 800, 1150)),
                       ground=("#DCE8F6", "#B9CBE6", "#8BA2C8"), fx=("snow",), flora=None, ground_y=596, mist=0.35, grass=None, snowy=True),
    "autumn_dusk": dict(sky=("#2A1A4A", "#B0506A", "#F2A65A"), moon=(220, 190, 70, "sun"), stars=False, ridge="#4A2A4E", trees=("round", "#2A1830", "#7A3A2A", (90, 420, 830, 1160)),
                        ground=("#7A5A32", "#5A3E22", "#3A2614"), fx=("leaves",), flora="#FFB45A", ground_y=596, mist=0.3, grass="#C9923F", warm=True),
    "rain_night": dict(sky=("#070B1C", "#18284A", "#33496E"), moon=None, stars=False, ridge="#0F1A36", trees=("round", "#080F22", "#0B1630", (60, 380, 760, 1130)),
                       ground=("#24493F", "#173A33", "#0C201E"), fx=("rain",), flora=None, ground_y=596, mist=0.5, grass="#3F7A60", puddles=True),
    "dawn_hills": dict(sky=("#3A3A7A", "#E27A8A", "#FFD08A"), moon=(640, 470, 90, "sun"), stars=False, ridge="#6A4A7E", trees=("round", "#3A2A5A", "#4A3A6A", (130, 1150)),
                       ground=("#6AAA6A", "#4A8A5A", "#2E6A46"), fx=("pollen",), flora="#FFE0F0", ground_y=596, mist=0.45, grass="#7CC27A", warm=True),
    "pond_night": dict(sky=("#080F2C", "#1C3C6A", "#4D7AAA"), moon=(640, 140, 56), stars=True, ridge="#12264A", trees=("round", "#0A1630", "#0E1E3C", (70, 1200)),
                       ground=("#2A5A4A", "#1B4036", "#0E2622"), fx=("fireflies",), flora="#C7A8FF", ground_y=560, water=True, mist=0.4, grass="#4E8C6A", reeds=True, lilies=True),
}


def _scene(name, t, seed, cam):
    c = SCENES[name]; r = random.Random(seed)
    out = [DEFS, f'<defs>{_g("sky_" + name, [(0, c["sky"][0], 1), (0.55, c["sky"][1], 1), (1, c["sky"][2], 1)])}'
           f'{_g("gr_" + name, [(0, c["ground"][0], 1), (0.4, c["ground"][1], 1), (1, c["ground"][2], 1)])}</defs>',
           f'<rect width="1280" height="720" fill="url(#sky_{name})"/>']
    if c["stars"]:
        for i in range(70):
            x, y = r.uniform(0, 1280), r.uniform(0, 320)
            out.append(f'<circle cx="{x + _px(cam, 0.05):.1f}" cy="{y:.1f}" r="{r.uniform(0.8, 2.1):.1f}" fill="#FFFFFF" opacity="{0.35 + 0.65 * abs(math.sin(2 * math.pi * t * r.choice([1, 2]) + i)):.2f}"/>')
    mx = my = None
    if c["moon"]:
        mx, my, mr = c["moon"][0] + _px(cam, 0.08), c["moon"][1], c["moon"][2]
        if len(c["moon"]) > 3:   # soleil
            out.append(f'<circle cx="{mx:.0f}" cy="{my}" r="{mr*3.4:.0f}" fill="url(#ffglow)" opacity="0.5"/><circle cx="{mx:.0f}" cy="{my}" r="{mr}" fill="#FFE9B0"/>')
        else:
            out.append(moon_glow(mx, my, mr))
    out.append(_ridge(c["ridge"], 470, 150, seed + 3, cam, 0.12))
    out.append(mist(t, 470, c["mist"], cam, 0.15, 3))
    kind, trunk, crown, xs = c["trees"]
    fn = {"round": lambda x, b, h, w, col, cr, sw: _tree(x, b, h, w, col, cr, sw), "pine": lambda x, b, h, w, col, cr, sw: _pine(x, b, h, w, cr, sw)}[kind]
    out.append(f'<g transform="translate({_px(cam, 0.3):.1f} 0)">' + "".join(fn(x * 1.0 + 40, 525, 200 + 40 * (i % 3), 22, trunk, crown, 1.2 * math.sin(2 * math.pi * t + x)) for i, x in enumerate(range(-40, 1320, 150))) + '</g>')
    if mx and not c.get("snowy") and c["fx"] != ("pollen",):
        out.append(rays(mx, my, t, 4))
    out.append(mist(t + 0.3, 535, c["mist"] * 0.9, cam, 0.35, 3))
    out.append(f'<g transform="translate({_px(cam, 0.55):.1f} 0)">' + "".join(fn(x, 590, 290 + 30 * (i % 2), 34, trunk, crown, 1.6 * math.sin(2 * math.pi * t + x * 0.3)) for i, x in enumerate(xs)) + '</g>')
    gy = c["ground_y"]
    if c.get("water"):
        out.append(f'<rect x="-40" y="{gy - 70}" width="1360" height="{720 - gy + 70}" fill="url(#sky_{name})"/>')
        if mx:
            out.append(f'<ellipse cx="{mx:.0f}" cy="{gy - 20}" rx="70" ry="10" fill="#FFF6DA" opacity="0.55"/>')
        for k in range(14):
            x = (k * 101 + 40 * math.sin(2 * math.pi * (t + k / 14))) % 1280
            y = gy - 62 + (k % 4) * 14
            out.append(f'<path d="M{x - 40:.0f} {y} q40 -6 80 0" stroke="#CFE2FF" stroke-width="1.8" fill="none" opacity="{0.25 + 0.2 * math.sin(2 * math.pi * (t * 2 + k)):.2f}"/>')
        out.append(f'<path d="M-40 {gy + 10} Q320 {gy - 10} 640 {gy + 6} T1320 {gy} L1320 720 L-40 720Z" fill="url(#gr_{name})"/>')
    else:
        out.append(f'<path d="M-40 {gy - 36} Q320 {gy - 62} 640 {gy - 36} T1320 {gy - 46} L1320 720 L-40 720Z" fill="url(#gr_{name})"/>')
    if c.get("snowy"):
        out.append(f'<ellipse cx="640" cy="650" rx="560" ry="60" fill="#FFFFFF" opacity="0.35"/>')
    if c["grass"]:
        for i in range(30):
            x, y = r.uniform(0, 1280), r.uniform(gy - 10, 715)
            h = 14 + (y - gy) * 0.14; sw = 3 * math.sin(2 * math.pi * t + i)
            out.append(f'<path d="M{x:.1f} {y:.1f} q{sw / 2:.1f} {-h / 2:.1f} {sw:.1f} {-h:.1f}" stroke="{c["grass"]}" stroke-width="2.2" fill="none" opacity="0.7"/>')
    if c.get("puddles"):
        for x, y, w in ((300, 660, 120), (760, 690, 160), (1100, 650, 100)):
            out.append(f'<ellipse cx="{x}" cy="{y}" rx="{w}" ry="{w * 0.14:.0f}" fill="#9CB8E0" opacity="0.28"/>')
    if c["flora"]:
        for i, (x, y) in enumerate([(210, 640), (520, 690), (910, 650), (1130, 700)]):
            g = 0.6 + 0.4 * math.sin(2 * math.pi * (t * 2 + i / 4))
            out.append(f'<circle cx="{x}" cy="{y - 8}" r="30" fill="url(#ffglow)" opacity="{0.5 * g:.2f}"/><circle cx="{x}" cy="{y - 8}" r="5" fill="{c["flora"]}" opacity="{0.6 + 0.4 * g:.2f}"/>')
    if c.get("lilies"):
        for i, (x, y) in enumerate([(380, 530), (640, 548), (900, 524), (520, 560)]):
            out.append(f'<ellipse cx="{x + 4 * math.sin(2 * math.pi * t + i):.1f}" cy="{y}" rx="34" ry="9" fill="#2F6A4A"/><circle cx="{x + 6}" cy="{y - 6}" r="8" fill="#F6B8D8"/>')
    out.append(mist(t + 0.6, 640, c["mist"] * 0.8, cam, 0.6, 3))
    return "".join(out)


def _front(name, t, seed, cam):
    c = SCENES[name]; px = _px(cam, 1.0); out = []
    fx = c["fx"]
    if "fireflies" in fx: out.append(fireflies(t, seed, cam))
    if "fireflies2" in fx: out.append(fireflies(t + 0.5, seed + 9, cam, 10))
    if "leaves" in fx: out.append(leaves(t, seed, cam))
    if "snow" in fx: out.append(snow(t, seed, cam))
    if "rain" in fx: out.append(rain(t))
    if "pollen" in fx: out.append(fireflies(t, seed + 2, cam, 22).replace("#F7FF7A", "#FFF2C0"))
    col = "#07161A" if not c.get("warm") else "#2B1A14"
    if c.get("reeds"):
        out.append(f'<g transform="translate({px:.1f} 0)">{_reeds(60, 730, 1.6, "#0B241E", t, 0)}{_reeds(1220, 730, 1.7, "#0B241E", t, 2)}{_reeds(180, 745, 1.1, "#123A30", t, 1)}</g>')
    elif c.get("snowy"):
        out.append(f'<g transform="translate({px:.1f} 0)"><ellipse cx="30" cy="740" rx="220" ry="70" fill="#E8F1FF"/><ellipse cx="1260" cy="745" rx="240" ry="80" fill="#E8F1FF"/></g>')
    else:
        out.append(f'<g transform="translate({px:.1f} 0)">{_fern(-10, 730, 1.5, col, t, 0.0)}{_fern(1290, 730, 1.6, col, t, 2.0)}{_fern(150, 745, 1.1, col, t, 1.0)}{_fern(1140, 745, 1.0, col, t, 3.0)}</g>')
    return "".join(out)


def _mk(name):
    return (lambda t, seed=1, cam=None: _scene(name, t, seed, cam)), (lambda t, seed=1, cam=None: _front(name, t, seed, cam))


def cave(t, seed=1, cam=None):
    r = random.Random(seed)
    out = [DEFS, '<defs>' + _g("cave_bg", [(0, "#0A0818", 1), (0.6, "#1B1432", 1), (1, "#2A2048", 1)]) + _g("cave_fl", [(0, "#2A2240", 1), (1, "#0F0B20", 1)]) + '</defs>',
           '<rect width="1280" height="720" fill="url(#cave_bg)"/>']
    out.append(f'<g transform="translate({_px(cam, 0.2):.1f} 0)"><path d="M-60 0 H1340 V120 " fill="#0F0B20"/>' + "".join(
        f'<path d="M{x} -10 L{x + 36} -10 L{x + 18} {80 + (x * 7) % 90} Z" fill="#171230"/>' for x in range(-40, 1320, 110)) + '</g>')
    cols = ["#7EE0FF", "#C58CFF", "#FF9AD5", "#8CFFC8"]
    for i in range(9):
        x = 90 + i * 140 + _px(cam, 0.5); y = 590 - (i * 37) % 160 + (60 if i % 2 else 0)
        c = cols[i % 4]; g = 0.65 + 0.35 * math.sin(2 * math.pi * (t * 2 + i / 9))
        out.append(f'<circle cx="{x:.0f}" cy="{y - 25}" r="70" fill="url(#ffglow)" opacity="{0.45 * g:.2f}"/>'
                   f'<path d="M{x - 14:.0f} {y} L{x - 6:.0f} {y - 58} L{x + 4:.0f} {y - 68} L{x + 14:.0f} {y - 50} L{x + 18:.0f} {y}Z" fill="{c}" opacity="{0.55 + 0.4 * g:.2f}"/>'
                   f'<path d="M{x - 6:.0f} {y - 58} L{x + 4:.0f} {y - 68} L{x + 6:.0f} {y - 30}Z" fill="#FFFFFF" opacity="0.4"/>')
    out.append('<path d="M-40 575 Q320 550 640 575 T1320 565 L1320 720 L-40 720Z" fill="url(#cave_fl)"/>')
    out.append(mist(t, 600, 0.3, cam, 0.5, 3))
    return "".join(out)


def cave_front(t, seed=1, cam=None):
    return fireflies(t, seed, cam, 12).replace("#F7FF7A", "#B8E8FF").replace("#C8F24A", "#8CC8FF").replace("#FFFDD0", "#EAF6FF")


def den(t, seed=1, cam=None):
    """Intérieur d'un tronc creux : lanterne chaude, mousse, petites lucioles."""
    fl = 0.9 + 0.1 * math.sin(2 * math.pi * (t * 3))
    out = [DEFS, '<defs>' + _g("den_bg", [(0, "#2A1A12", 1), (1, "#4A2E1C", 1)]) + _g("den_glow", [(0, "#FFD28A", 0.75), (0.5, "#FF9A4A", 0.25), (1, "#FF9A4A", 0)], radial=True) + '</defs>',
           '<rect width="1280" height="720" fill="url(#den_bg)"/>']
    for x in range(-20, 1300, 70):
        out.append(f'<path d="M{x} 0 Q{x + 20} 360 {x - 6} 720" stroke="#1E120B" stroke-width="10" fill="none" opacity="0.7"/>')
    out.append('<ellipse cx="640" cy="240" rx="240" ry="190" fill="#14243E"/><circle cx="640" cy="240" r="170" fill="#0E1B38"/>'
               f'<circle cx="560" cy="190" r="3" fill="#FFFFFF" opacity="0.8"/><circle cx="720" cy="270" r="2.4" fill="#FFFFFF" opacity="0.7"/><circle cx="690" cy="170" r="2" fill="#FFFFFF"/>'
               '<circle cx="700" cy="200" r="46" fill="#FFF3CF"/>')
    out.append(f'<circle cx="1040" cy="300" r="240" fill="url(#den_glow)" opacity="{fl:.2f}"/><rect x="1032" y="190" width="16" height="46" rx="4" fill="#6A4A2A"/>'
               f'<ellipse cx="1040" cy="270" rx="26" ry="34" fill="#FFD27A" opacity="{0.8 + 0.2 * fl:.2f}"/>')
    out.append('<path d="M-40 610 Q320 585 640 610 T1320 600 L1320 720 L-40 720Z" fill="#3E5A2E"/><path d="M-40 640 Q320 620 640 640 T1320 630 L1320 720 L-40 720Z" fill="#4F7238"/>')
    return "".join(out)


DECORS = {"forest_night": forest_night, "cave": cave, "den": den}
FRONTS = {"forest_night": forest_night_front, "cave": cave_front, "den": lambda t, seed=1, cam=None: fireflies(t, seed, cam, 8)}
for _n in SCENES:
    DECORS[_n], FRONTS[_n] = _mk(_n)
GROUND_BY = {"forest_night": 596, "cave": 586, "den": 616, **{n: c["ground_y"] + 4 for n, c in SCENES.items()}}
PLACE_NAMES = {"forest_night": "the moonlit forest", "meadow_night": "the firefly meadow", "river_night": "the silver river", "snow_night": "the snowy hills",
               "autumn_dusk": "the golden woods", "rain_night": "the rainy woods", "dawn_hills": "the dawn hills", "pond_night": "the moon pond",
               "cave": "the crystal cave", "den": "the cozy den"}
