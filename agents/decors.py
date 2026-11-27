"""Agent 18 — Décorateur : les décors colorés des histoires (repère 1280x720, sol vers y=600).
Coucher de soleil fleuri, forêt enchantée, pays des nuages et arc-en-ciel, chambre de Mimo, rivière, colline de nuit."""
import math, random

GROUND = 600
GROUND_BY = {"river": 518}


def ground(decor):
    return GROUND_BY.get(decor, GROUND)


def _grad(gid, stops, vertical=True):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    xy = 'x1="0" y1="0" x2="0" y2="1"' if vertical else 'x1="0" y1="0" x2="1" y2="0"'
    return f'<linearGradient id="{gid}" {xy}>{s}</linearGradient>'


def _cloud(x, y, s, col="#FFFFFF", op=0.95):
    return (f'<g transform="translate({x:.1f} {y:.1f}) scale({s:.2f})" fill="{col}" opacity="{op}">'
            '<circle cx="-50" cy="0" r="36"/><circle cx="0" cy="-18" r="48"/><circle cx="50" cy="0" r="36"/>'
            '<rect x="-86" y="0" width="172" height="34" rx="17"/></g>')


def _flower(x, y, col, t, ph, s=1.0):
    sw = 3 * math.sin(2 * math.pi * t + ph)
    pet = "".join(f'<circle cx="{8*math.cos(a):.1f}" cy="{8*math.sin(a):.1f}" r="7" fill="{col}"/>' for a in [i * math.pi * 2 / 5 for i in range(5)])
    return (f'<g transform="translate({x:.1f} {y:.1f}) scale({s:.2f})"><path d="M0 0 Q{sw/2:.1f} -14 {sw:.1f} -28" stroke="#4E9A5A" stroke-width="3" fill="none"/>'
            f'<g transform="translate({sw:.1f} -30)">{pet}<circle r="5" fill="#FFE37A"/></g></g>')


def _butterfly(x, y, t, col):
    f = abs(math.sin(2 * math.pi * 6 * t))
    return (f'<g transform="translate({x:.1f} {y:.1f})"><ellipse cx="-8" cy="0" rx="{10*f+2:.1f}" ry="9" fill="{col}"/>'
            f'<ellipse cx="8" cy="0" rx="{10*f+2:.1f}" ry="9" fill="{col}"/><rect x="-1.5" y="-8" width="3" height="16" rx="1.5" fill="#4A3A5A"/></g>')


def _rainbow(cx, cy, r, op=0.55):
    cols = ["#FF8A8A", "#FFB86B", "#FFE37A", "#9BE38A", "#7EC8F2", "#B59BF2"]
    return "".join(f'<path d="M{cx-r+i*14} {cy} A{r-i*14} {r-i*14} 0 0 1 {cx+r-i*14} {cy}" stroke="{c}" stroke-width="14" fill="none" opacity="{op}"/>'
                   for i, c in enumerate(cols))


def meadow(t, rng_seed=1):
    r = random.Random(rng_seed)
    sunpulse = 1 + 0.03 * math.sin(2 * math.pi * t)
    out = [f'<defs>{_grad("sky_meadow", [(0, "#FF9EC4"), (0.5, "#FFC59E"), (1, "#FFE9A8")])}</defs>',
           '<rect width="1280" height="720" fill="url(#sky_meadow)"/>',
           f'<circle cx="980" cy="330" r="{120*sunpulse:.1f}" fill="#FFE37A" opacity="0.45"/><circle cx="980" cy="330" r="85" fill="#FFD25A"/>',
           _rainbow(330, 470, 300, 0.45)]
    for i, (x, y, s) in enumerate([(200, 120, 0.9), (620, 90, 1.1), (1150, 150, 0.8)]):
        out.append(_cloud(x + 30 * math.sin(2 * math.pi * t + i), y, s))
    out.append('<path d="M0 520 Q300 430 640 500 T1280 480 L1280 720 L0 720Z" fill="#8FD27F"/>'
               '<path d="M0 580 Q420 520 820 580 T1280 570 L1280 720 L0 720Z" fill="#6CBF6A"/>')
    cols = ["#FF6F91", "#FFB347", "#B57BFF", "#5EC8F2", "#FF8AE2"]
    for i in range(26):
        x, y = r.uniform(0, 1280), r.uniform(615, 715)
        out.append(_flower(x, y, cols[i % 5], t, i, 0.9 + 0.4 * (y - 615) / 100))
    for i in range(3):
        bx = (r.uniform(0, 1280) + 1280 * t * (1 if i % 2 else -1)) % 1280
        out.append(_butterfly(bx, 300 + 80 * math.sin(2 * math.pi * (2 * t + i / 3)) + i * 60, t + i * 0.1, cols[i + 1]))
    return "".join(out)


def forest(t, rng_seed=2):
    r = random.Random(rng_seed)
    out = [f'<defs>{_grad("sky_forest", [(0, "#7FD6D6"), (0.6, "#C9B6F2"), (1, "#FFC9DE")])}</defs>',
           '<rect width="1280" height="720" fill="url(#sky_forest)"/>',
           '<path d="M0 560 Q640 500 1280 560 L1280 720 L0 720Z" fill="#7CC489"/>']
    cols = ["#5FBF7A", "#F28AB3", "#7EC8F2", "#B59BF2", "#9BD86A", "#FFB86B"]
    for i, x in enumerate([60, 220, 400, 900, 1060, 1220]):
        h = 260 + (i % 3) * 50
        sw = 4 * math.sin(2 * math.pi * t + i)
        out.append(f'<rect x="{x-14}" y="{GROUND-h+80}" width="28" height="{h}" rx="10" fill="#9A6A4A"/>'
                   f'<g transform="rotate({sw:.1f} {x} {GROUND-h+120})"><circle cx="{x}" cy="{GROUND-h+60}" r="{90 + (i%2)*20}" fill="{cols[i]}"/>'
                   f'<circle cx="{x-50}" cy="{GROUND-h+100}" r="60" fill="{cols[i]}"/><circle cx="{x+50}" cy="{GROUND-h+100}" r="60" fill="{cols[i]}"/></g>')
    for i, x in enumerate([300, 760, 1150]):
        out.append(f'<rect x="{x-8}" y="{GROUND-10}" width="16" height="30" rx="6" fill="#FFF4E0"/>'
                   f'<path d="M{x-30} {GROUND-8} Q{x} {GROUND-50} {x+30} {GROUND-8}Z" fill="#FF6F6F"/>'
                   f'<circle cx="{x-10}" cy="{GROUND-24}" r="5" fill="#FFFFFF"/><circle cx="{x+12}" cy="{GROUND-20}" r="4" fill="#FFFFFF"/>')
    for i in range(14):
        x = r.uniform(0, 1280) + 30 * math.sin(2 * math.pi * t + i)
        y = r.uniform(150, 520) + 20 * math.cos(2 * math.pi * t + i)
        a = 0.4 + 0.6 * abs(math.sin(2 * math.pi * 2 * t + i))
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="10" fill="#FFF7A8" opacity="{a*0.3:.2f}"/><circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#FFFBD0" opacity="{a:.2f}"/>')
    out.append('<rect x="0" y="640" width="1280" height="80" fill="#68B477"/>')
    return "".join(out)


def cloudland(t, rng_seed=3):
    out = [f'<defs>{_grad("sky_cloud", [(0, "#8EC5FF"), (0.6, "#D7B8FF"), (1, "#FFD1E8")])}</defs>',
           '<rect width="1280" height="720" fill="url(#sky_cloud)"/>', _rainbow(640, 520, 460, 0.6)]
    for i, (x, y, s) in enumerate([(150, 140, 1.0), (520, 90, 0.8), (1000, 120, 1.2), (1200, 300, 0.7), (80, 380, 0.8)]):
        out.append(_cloud(x + 40 * math.sin(2 * math.pi * t + i), y, s, op=0.9))
    for i, (x, y) in enumerate([(300, 260), (880, 230), (700, 380), (1100, 420)]):
        a = 0.5 + 0.5 * math.sin(2 * math.pi * (2 * t + i / 4))
        s = 12 + 6 * a
        out.append(f'<path d="M{x} {y-s} Q{x} {y} {x+s} {y} Q{x} {y} {x} {y+s} Q{x} {y} {x-s} {y} Q{x} {y} {x} {y-s}Z" fill="#FFF4C9" opacity="{0.6+0.4*a:.2f}"/>')
    out.append('<g fill="#FFFFFF"><ellipse cx="640" cy="700" rx="760" ry="120"/></g>'
               '<g fill="#F4EEFF"><circle cx="120" cy="620" r="90"/><circle cx="330" cy="600" r="110"/><circle cx="960" cy="605" r="105"/><circle cx="1180" cy="625" r="90"/></g>')
    return "".join(out)


def bedroom(t, rng_seed=4):
    out = [f'<defs>{_grad("wall", [(0, "#BFD9FF"), (1, "#E3D4FF")])}</defs>',
           '<rect width="1280" height="720" fill="url(#wall)"/>']
    for i in range(18):
        x, y = (i * 173) % 1280 + 40, (i * 97) % 380 + 30
        out.append(f'<path d="M{x} {y-9} L{x+3} {y-3} L{x+9} {y-3} L{x+4} {y+2} L{x+6} {y+9} L{x} {y+5} L{x-6} {y+9} L{x-4} {y+2} L{x-9} {y-3} L{x-3} {y-3}Z" fill="#FFFFFF" opacity="0.7"/>')
    # fenêtre avec la nuit
    out.append('<rect x="760" y="90" width="300" height="260" rx="20" fill="#2A2A6E"/>'
               f'<circle cx="980" cy="170" r="40" fill="#FFE7A3"/><circle cx="960" cy="160" r="40" fill="#2A2A6E"/>')
    for i, (x, y) in enumerate([(810, 140), (880, 220), (840, 300), (1010, 280), (930, 120)]):
        a = 0.5 + 0.5 * math.sin(2 * math.pi * (2 * t + i / 5))
        out.append(f'<circle cx="{x}" cy="{y}" r="{3+2*a:.1f}" fill="#FFF4C9"/>')
    out.append('<rect x="760" y="90" width="300" height="260" rx="20" fill="none" stroke="#FFFFFF" stroke-width="14"/>'
               '<rect x="902" y="90" width="14" height="260" fill="#FFFFFF"/><rect x="760" y="214" width="300" height="12" fill="#FFFFFF"/>'
               '<path d="M740 80 Q790 230 750 370 L720 370 L720 80Z" fill="#FF9EC4"/><path d="M1080 80 Q1030 230 1070 370 L1100 370 L1100 80Z" fill="#FF9EC4"/>')
    # sol, tapis, lit, lampe, jouets
    out.append('<rect x="0" y="560" width="1280" height="160" fill="#F2C9A8"/>'
               '<ellipse cx="640" cy="650" rx="330" ry="50" fill="#9EDBC8"/><ellipse cx="640" cy="650" rx="250" ry="34" fill="#FFE37A"/>'
               '<rect x="40" y="420" width="380" height="140" rx="30" fill="#FFFFFF"/><rect x="30" y="360" width="40" height="230" rx="14" fill="#B57BFF"/>'
               '<rect x="40" y="470" width="380" height="90" rx="30" fill="#7EC8F2"/><ellipse cx="120" cy="430" rx="70" ry="30" fill="#FFFFFF"/>')
    glow = 0.25 + 0.08 * math.sin(2 * math.pi * t)
    out.append(f'<circle cx="1180" cy="420" r="110" fill="#FFE9A0" opacity="{glow:.2f}"/><rect x="1172" y="430" width="16" height="130" fill="#B57BFF"/>'
               '<path d="M1130 430 L1230 430 L1205 370 L1155 370Z" fill="#FFD25A"/>'
               '<rect x="1040" y="520" width="50" height="50" rx="8" fill="#FF6F91"/><rect x="1095" y="520" width="50" height="50" rx="8" fill="#5EC8F2"/>'
               '<rect x="1068" y="470" width="50" height="50" rx="8" fill="#FFB347"/>')
    return "".join(out)


def river(t, rng_seed=5):
    out = [f'<defs>{_grad("sky_river", [(0, "#B9A6FF"), (0.6, "#FFB3D1"), (1, "#FFD9A8")])}</defs>',
           '<rect width="1280" height="720" fill="url(#sky_river)"/>',
           f'<circle cx="1050" cy="160" r="70" fill="#FFF0B3"/>',
           _cloud(250 + 30 * math.sin(2 * math.pi * t), 130, 0.9), _cloud(700 - 30 * math.sin(2 * math.pi * t), 90, 0.7),
           '<path d="M0 470 Q320 420 640 460 T1280 450 L1280 720 L0 720Z" fill="#8FD27F"/>']
    for i, col in enumerate(["#6FC3E8", "#5AB4DE", "#4AA3D2"]):
        y0 = 540 + i * 30
        pts = [f"{1280*j/32:.1f},{y0 + 7*math.sin(2*math.pi*(j/6 + t*(1 if i % 2 == 0 else -1))):.1f}" for j in range(33)]
        out.append(f'<path d="M0,720 L{" L".join(pts)} L1280,720Z" fill="{col}"/>')
    for i, x in enumerate([180, 460, 1000]):
        dy = 3 * math.sin(2 * math.pi * t + i)
        out.append(f'<ellipse cx="{x}" cy="{600+i*25+dy:.1f}" rx="44" ry="13" fill="#4FAE5C"/><circle cx="{x+12}" cy="{594+i*25+dy:.1f}" r="9" fill="#FF8AB8"/>')
    out.append('<rect x="0" y="470" width="1280" height="60" fill="#7CC489"/>')
    return "".join(out)


def night_hill(t, rng_seed=6):
    r = random.Random(rng_seed)
    out = [f'<defs>{_grad("sky_nh", [(0, "#2B1F6B"), (0.6, "#6A3FA0"), (1, "#E07AB8")])}</defs>',
           '<rect width="1280" height="720" fill="url(#sky_nh)"/>',
           '<circle cx="1000" cy="150" r="110" fill="#FFE7A3" opacity="0.25"/><circle cx="1000" cy="150" r="70" fill="#FFF0B3"/>']
    for i in range(70):
        x, y = r.uniform(0, 1280), r.uniform(0, 420)
        a = 0.4 + 0.6 * abs(math.sin(2 * math.pi * (t * r.choice([1, 2])) + i))
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r.uniform(1.5, 3.2):.1f}" fill="#FFFFFF" opacity="{a:.2f}"/>')
    out.append('<path d="M0 560 Q640 430 1280 560 L1280 720 L0 720Z" fill="#3F3A8C"/>')
    for i, x in enumerate([180, 380, 900, 1100]):
        g = 0.6 + 0.3 * math.sin(2 * math.pi * (2 * t + i / 4))
        out.append(f'<line x1="{x}" y1="420" x2="{x}" y2="470" stroke="#C9B6F2" stroke-width="2"/>'
                   f'<circle cx="{x}" cy="490" r="34" fill="{["#FF8AB8", "#FFD25A", "#7EC8F2", "#B59BF2"][i]}" opacity="{g*0.35:.2f}"/>'
                   f'<ellipse cx="{x}" cy="490" rx="18" ry="22" fill="{["#FF8AB8", "#FFD25A", "#7EC8F2", "#B59BF2"][i]}"/>')
    out.append('<rect x="0" y="600" width="1280" height="120" fill="#332F78"/>')
    return "".join(out)


from . import decors2 as _D2
GROUND_BY.update(_D2.GROUND_BY)
DECORS = {"meadow": meadow, "forest": forest, "clouds": cloudland, "bedroom": bedroom, "river": river, "night": night_hill}
PLACE_NAMES = {"meadow": "the flower meadow", "forest": "the rainbow forest", "clouds": "the land of clouds",
               "river": "the sparkly river", "night": "the lantern hill", "bedroom": "Mimo's room", **_D2.PLACE_NAMES}
DECORS.update(_D2.DECORS)


def water_front(t):
    """Bande d'eau devant Bubbles, pour qu'il nage à moitié dans la rivière."""
    pts = [f"{1280*j/32:.1f},{592 + 6*math.sin(2*math.pi*(j/6 + t)):.1f}" for j in range(33)]
    return (f'<path d="M0,720 L{" L".join(pts)} L1280,720Z" fill="#4AA3D2"/>'
            f'<path d="M{" L".join(pts)}" stroke="#BFE3F2" stroke-width="4" fill="none" opacity="0.7"/>')


def foreground(decor, t, cam=None):
    """Premier plan (devant les personnages) pour donner de la profondeur."""
    if decor in _D2.FRONTS:
        return _D2.FRONTS[decor](t, 1, cam)
    if decor == "meadow":
        out = []
        for i, (x, y, sc, col) in enumerate([(40, 700, 2.6, "#FF6F91"), (130, 720, 2.0, "#B57BFF"), (1200, 705, 2.4, "#FFB347"), (1110, 725, 1.9, "#5EC8F2")]):
            out.append(_flower(x, y, col, t, i * 1.3, sc))
        out.append('<path d="M0 720 Q60 650 90 720Z M70 720 Q110 640 150 720Z M1150 720 Q1190 650 1220 720Z M1210 720 Q1250 640 1280 720Z" fill="#4E9A5A"/>')
        return "".join(out)
    if decor == "forest":
        sw = 6 * math.sin(2 * math.pi * t)
        return (f'<g fill="#3E8E5A"><circle cx="-20" cy="720" r="110"/><circle cx="90" cy="740" r="80"/><circle cx="1300" cy="720" r="110"/><circle cx="1190" cy="745" r="80"/></g>'
                f'<g fill="#5FBF7A" opacity="0.9" transform="rotate({sw:.1f} 0 0)"><ellipse cx="60" cy="10" rx="120" ry="45"/><ellipse cx="0" cy="60" rx="70" ry="30"/></g>'
                f'<g fill="#F28AB3" opacity="0.9" transform="rotate({-sw:.1f} 1280 0)"><ellipse cx="1220" cy="10" rx="120" ry="45"/><ellipse cx="1280" cy="60" rx="70" ry="30"/></g>')
    if decor == "night":
        out = ['<path d="M0 720 L0 680 Q30 640 50 690 Q70 630 95 690 Q120 650 140 720Z M1280 720 L1280 680 Q1250 640 1230 690 Q1210 630 1185 690 Q1160 650 1140 720Z" fill="#221E58"/>']
        for i, (x, y) in enumerate([(90, 600), (1180, 620), (200, 660)]):
            a = 0.4 + 0.6 * abs(math.sin(2 * math.pi * (2 * t + i / 3)))
            out.append(f'<circle cx="{x}" cy="{y + 10*math.sin(2*math.pi*t + i):.1f}" r="12" fill="#FFF7A8" opacity="{a*0.3:.2f}"/>'
                       f'<circle cx="{x}" cy="{y + 10*math.sin(2*math.pi*t + i):.1f}" r="4" fill="#FFFBD0" opacity="{a:.2f}"/>')
        return "".join(out)
    if decor == "clouds":
        return ('<g fill="#FFFFFF" opacity="0.92"><circle cx="0" cy="720" r="120"/><circle cx="120" cy="745" r="90"/>'
                '<circle cx="1280" cy="720" r="120"/><circle cx="1160" cy="745" r="90"/></g>')
    if decor == "river":
        out = []
        for i, x in enumerate([20, 50, 80, 1200, 1230, 1260]):
            sw = 6 * math.sin(2 * math.pi * t + i * 0.4)
            out.append(f'<path d="M{x} 720 Q{x + sw/2:.1f} 540 {x + sw:.1f} 400" stroke="#2E6B4F" stroke-width="9" fill="none"/>'
                       f'<ellipse cx="{x + sw:.1f}" cy="410" rx="11" ry="34" fill="#7A4E2E"/>')
        return "".join(out)
    return ""
