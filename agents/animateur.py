"""Agent 15 — Animateur : une scène animée différente pour chaque comptine.
Twinkle → une étoile qui sourit ; Row Your Boat → Mimo qui rame sur la rivière ;
Are You Sleeping → la cloche qui sonne pendant que Mimo dort ; Mary Had a Little Lamb → l'agneau
qui saute la barrière ; London Bridge → le vieux pont illuminé. Toutes les boucles sont parfaites.
Les scènes sont dessinées dans un repère 1280x720 puis agrandies (Full HD)."""
import math, random
from .illustrateur import bear, zzz, mimo, draw_particles, text, FONT

SONG_SCENES = {
    "Twinkle Twinkle Little Star": "star",
    "Row Row Row Your Boat": "row",
    "Are You Sleeping (Frère Jacques)": "bell",
    "Mary Had a Little Lamb": "sheep",
    "London Bridge": "bridge",
}
SCENE_NAMES = {"star": "Twinkle Star", "row": "River Boat", "bell": "Bell Tower", "sheep": "Sleepy Lamb", "bridge": "Old Bridge"}
PALETTE = {
    "star": ("#151A4A", "#40398F"), "row": ("#0C2742", "#1D6A86"), "bell": ("#241A4D", "#5A3F86"),
    "sheep": ("#11203F", "#2E4F7A"), "bridge": ("#101836", "#33406F"),
}


def particles(scene, seed):
    r = random.Random(seed)
    parts = [("stars", r.uniform(0, 1280), r.uniform(0, 430), 1.0, r.choice([1, 2, 3]), r.uniform(0, 6.28), r.random() < 0.2)
             for _ in range(120)]
    return parts


def _star_path(cx, cy, R, r, rot=0.0, n=5):
    pts = []
    for i in range(n * 2):
        a = math.pi / n * i - math.pi / 2 + math.radians(rot)
        rad = R if i % 2 == 0 else r
        pts.append(f"{cx + rad * math.cos(a):.1f},{cy + rad * math.sin(a):.1f}")
    return "M" + " L".join(pts) + "Z"


def _sparkle(x, y, s, a):
    return (f'<path d="M{x} {y-s} Q{x} {y} {x+s} {y} Q{x} {y} {x} {y+s} Q{x} {y} {x-s} {y} Q{x} {y} {x} {y-s}Z" '
            f'fill="#FFF4C9" opacity="{a:.2f}"/>')


def _moon(x, y, r, glow=0.15):
    return (f'<circle cx="{x}" cy="{y}" r="{r*1.9:.0f}" fill="#FFE9A0" opacity="{glow:.3f}"/>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFE7A3"/>'
            f'<circle cx="{x - r*0.3:.0f}" cy="{y - r*0.2:.0f}" r="{r*0.16:.0f}" fill="#F2C24A" opacity="0.35"/>'
            f'<circle cx="{x + r*0.35:.0f}" cy="{y + r*0.3:.0f}" r="{r*0.1:.0f}" fill="#F2C24A" opacity="0.35"/>')


def _note(x, y, s, a):
    return (f'<g transform="translate({x:.1f} {y:.1f}) scale({s:.2f})" fill="#FFE9A0" opacity="{a:.2f}">'
            '<ellipse cx="0" cy="0" rx="9" ry="7" transform="rotate(-20)"/><rect x="6" y="-34" width="4" height="34"/>'
            '<path d="M10 -34 Q24 -28 20 -14 Q18 -24 10 -24Z"/></g>')


def _bear_simple(x, y, s, t, blanket=("#8FB8E8", "#B9D4F3")):
    return f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.3f})">{bear(blanket, t)}{zzz(t)}</g>'


# ---------------------------------------------------------------- Scènes
def scene_star(t, parts):
    rot = 5 * math.sin(2 * math.pi * t)
    sc = 1 + 0.04 * math.sin(2 * math.pi * 2 * t)
    glow = 0.22 + 0.1 * math.sin(2 * math.pi * 2 * t)
    cx, cy = 640, 280
    out = [f'<circle cx="{cx}" cy="{cy}" r="250" fill="url(#glow_s)" opacity="{glow:.3f}"/>',
           f'<g transform="translate({cx} {cy}) rotate({rot:.2f}) scale({sc:.3f}) translate({-cx} {-cy})">',
           f'<path d="{_star_path(cx, cy, 165, 78)}" fill="url(#star_g)" stroke="#F2B53A" stroke-width="6" stroke-linejoin="round"/>',
           f'<path d="M{cx-48} {cy-8} Q{cx-34} {cy+6} {cx-20} {cy-8}" fill="none" stroke="#7A4A1E" stroke-width="7" stroke-linecap="round"/>',
           f'<path d="M{cx+20} {cy-8} Q{cx+34} {cy+6} {cx+48} {cy-8}" fill="none" stroke="#7A4A1E" stroke-width="7" stroke-linecap="round"/>',
           f'<path d="M{cx-24} {cy+30} Q{cx} {cy+52} {cx+24} {cy+30}" fill="none" stroke="#7A4A1E" stroke-width="7" stroke-linecap="round"/>',
           f'<circle cx="{cx-62}" cy="{cy+22}" r="14" fill="#F59A8A" opacity="0.6"/><circle cx="{cx+62}" cy="{cy+22}" r="14" fill="#F59A8A" opacity="0.6"/>',
           "</g>"]
    for i, (x, y) in enumerate([(380, 150), (900, 120), (1010, 330), (290, 360), (820, 450), (470, 470)]):
        a = 0.5 + 0.5 * math.sin(2 * math.pi * (2 * t + i / 6))
        out.append(_sparkle(x, y, 14 + 6 * a, a))
    # toits endormis
    roofs = '<g fill="#0C1030">'
    for x, w, h in [(0, 170, 120), (150, 150, 160), (290, 190, 110), (900, 200, 140), (1080, 210, 180)]:
        roofs += f'<rect x="{x}" y="{720-h}" width="{w}" height="{h}"/><path d="M{x-10} {720-h} L{x+w/2} {720-h-60} L{x+w+10} {720-h}Z"/>'
    roofs += "</g>"
    out.append(roofs)
    for i, (x, y) in enumerate([(60, 640), (200, 600), (360, 650), (960, 630), (1150, 590), (1190, 650)]):
        lit = 0.55 + 0.35 * (math.sin(2 * math.pi * (t + i * 0.37)) > -0.6)
        out.append(f'<rect x="{x}" y="{y}" width="26" height="30" rx="4" fill="#FFD77A" opacity="{lit:.2f}"/>')
    out.append(f'<g transform="translate(-330 {-70 + 6*math.sin(2*math.pi*t):.1f})"><g fill="#F4F1FF"><circle cx="560" cy="640" r="40"/><circle cx="640" cy="620" r="60"/>'
               '<circle cx="730" cy="640" r="44"/><rect x="520" y="640" width="250" height="44" rx="22"/></g>'
               + _bear_simple(650, 598, 0.55, t, ("#F4A9C0", "#F9CEDB")) + "</g>")
    defs = ('<defs><radialGradient id="glow_s"><stop offset="0.4" stop-color="#FFE9A0" stop-opacity="1"/><stop offset="1" stop-color="#FFE9A0" stop-opacity="0"/></radialGradient>'
            '<radialGradient id="star_g" cx="0.45" cy="0.4" r="0.7"><stop offset="0" stop-color="#FFF6C2"/><stop offset="1" stop-color="#FFCB45"/></radialGradient></defs>')
    return defs + "".join(out)


def _waves(t, top, cols=("#174E6E", "#123F5C", "#0E3350"), amp=10):
    out = []
    for i, col in enumerate(cols):
        y0 = top + i * 38
        pts = [f"{1280*j/40:.1f},{y0 + amp*math.sin(2*math.pi*(j/8 + t*(1 if i % 2 == 0 else -1) + i*0.3)):.1f}" for j in range(41)]
        out.append(f'<path d="M0,720 L{" L".join(pts)} L1280,720Z" fill="{col}"/>')
    return "".join(out)


def scene_row(t, parts):
    out = [_moon(1040, 130, 60, 0.18)]
    # reflet de lune
    for i in range(6):
        w = 90 - i * 12 + 10 * math.sin(2 * math.pi * (2 * t + i * 0.2))
        out.append(f'<rect x="{1040 - w/2:.0f}" y="{470 + i*28}" width="{w:.0f}" height="6" rx="3" fill="#FFE7A3" opacity="{0.35 - i*0.04:.2f}"/>')
    out.append(_waves(t, 455))
    # roseaux
    for i, x in enumerate([60, 90, 120, 1180, 1210, 1240]):
        sway = 6 * math.sin(2 * math.pi * (t + i * 0.13))
        out.append(f'<path d="M{x} 720 Q{x+sway/2:.1f} 560 {x+sway:.1f} 430" stroke="#2E6B4F" stroke-width="6" fill="none"/>'
                   f'<ellipse cx="{x+sway:.1f}" cy="440" rx="8" ry="26" fill="#7A4E2E"/>')
    # barque + Mimo qui rame (8 coups de rame par boucle)
    ph = 2 * math.pi * 8 * t
    bob = 6 * math.sin(2 * math.pi * 4 * t)
    a_back = 25 * math.sin(ph)
    ripple = []
    if math.sin(ph) > 0.7:
        k = (math.sin(ph) - 0.7) / 0.3
        for x in (300, 980):
            ripple.append(f'<ellipse cx="{x}" cy="575" rx="{20+40*k:.0f}" ry="{6+8*k:.0f}" fill="none" stroke="#BFE3F2" stroke-width="3" opacity="{0.7*(1-k):.2f}"/>')
    oars = ""
    for side, px in ((-1, 470), (1, 810)):
        ang = -side * (62 + 16 * math.sin(ph))
        oars += (f'<g transform="translate({px} {470+bob:.1f}) rotate({ang:.1f})">'
                 f'<rect x="-6" y="0" width="12" height="170" rx="6" fill="#9A6A3E"/><ellipse cx="0" cy="178" rx="18" ry="34" fill="#B07A48"/></g>')
    out.append("".join(ripple) + oars)
    out.append(mimo("ocean", 640, 410 + bob, 0.95, t, 1.5 * math.sin(2 * math.pi * 2 * t)))
    out.append(_waves(t + 0.5, 572, cols=("#0E3350",), amp=8))
    return "".join(out)


def scene_bell(t, parts):
    out = [_moon(160, 120, 48, 0.15)]
    # colline et tour
    out.append('<path d="M0 600 Q320 520 700 590 T1280 560 L1280 720 L0 720Z" fill="#1A1440"/>')
    tx = 980
    out.append(f'<rect x="{tx-70}" y="260" width="140" height="360" fill="#3B2E6E"/><path d="M{tx-95} 262 L{tx} 150 L{tx+95} 262Z" fill="#5A3F86"/>'
               f'<path d="M{tx-45} 400 L{tx-45} 320 Q{tx} 270 {tx+45} 320 L{tx+45} 400Z" fill="#160F33"/>'
               f'<rect x="{tx-25}" y="470" width="50" height="70" rx="25" fill="#FFD77A" opacity="0.8"/>')
    # cloche qui se balance (4 coups par boucle)
    sw = math.sin(2 * math.pi * 4 * t)
    ang = 22 * sw
    out.append(f'<g transform="translate({tx} 318) rotate({ang:.1f})"><rect x="-3" y="0" width="6" height="18" fill="#C8963A"/>'
               '<path d="M-34 70 Q-34 18 0 16 Q34 18 34 70 L42 80 L-42 80Z" fill="url(#bell_g)" stroke="#B9822A" stroke-width="3"/>'
               '<circle cx="0" cy="86" r="8" fill="#B9822A"/></g>')
    # notes de musique qui s'envolent de la cloche
    for i in range(6):
        p = (t * 4 + i / 6) % 1.0
        out.append(_note(tx - 40 - 180 * p + 25 * math.sin(2 * math.pi * p * 2 + i), 300 - 200 * p, 0.8 + 0.6 * p, math.sin(math.pi * p) * 0.9))
    # Mimo endormi dans son lit
    out.append('<g><rect x="200" y="470" width="30" height="190" rx="10" fill="#8A5A3C"/><rect x="200" y="455" width="100" height="40" rx="20" fill="#A06A42"/>'
               '<rect x="215" y="575" width="470" height="70" rx="20" fill="#E8EEF8"/><rect x="640" y="560" width="30" height="100" rx="10" fill="#8A5A3C"/>'
               '<ellipse cx="300" cy="560" rx="75" ry="34" fill="#FFFFFF"/></g>')
    out.append(_bear_simple(390, 505, 0.95, t, ("#B79CE8", "#D9CBF6")))
    return '<defs><linearGradient id="bell_g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFE38A"/><stop offset="1" stop-color="#E5A93A"/></linearGradient></defs>' + "".join(out)


def _lamb(x, y, rot, legs):
    body = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#FFFFFF"/>' for cx, cy, r in
                   [(-40, 0, 32), (-10, -14, 36), (25, -8, 34), (45, 8, 28), (0, 16, 34), (-30, 20, 28), (30, 22, 28)])
    leg = "".join(f'<rect x="{lx}" y="30" width="12" height="{34 + legs * (1 if i % 2 else -1):.0f}" rx="6" fill="#3A3150"/>'
                  for i, lx in enumerate([-38, -14, 18, 40]))
    head = ('<ellipse cx="72" cy="-8" rx="26" ry="30" fill="#3A3150"/><ellipse cx="62" cy="-34" rx="22" ry="14" fill="#FFFFFF"/>'
            '<ellipse cx="96" cy="-14" rx="16" ry="8" fill="#3A3150" transform="rotate(30 96 -14)"/>'
            '<path d="M64 -10 Q70 -4 76 -10" stroke="#FFFFFF" stroke-width="3" fill="none" stroke-linecap="round"/>'
            '<circle cx="80" cy="6" r="5" fill="#F4A3A3" opacity="0.7"/>')
    return f'<g transform="translate({x:.1f} {y:.1f}) rotate({rot:.1f})">{leg}{body}{head}</g>'


def scene_sheep(t, parts):
    out = []
    out.append('<path d="M0 520 Q400 450 800 510 T1280 500 L1280 720 L0 720Z" fill="#1F4A3E"/>'
               '<path d="M0 600 Q500 560 1280 610 L1280 720 L0 720Z" fill="#183C33"/>')
    for i, x in enumerate(range(40, 1280, 110)):
        out.append(f'<circle cx="{x + 30*math.sin(i)}" cy="{640 + 25*math.cos(i*1.7):.0f}" r="7" fill="{["#F7D6E0", "#FFF4C9", "#CFE3FF"][i % 3]}" opacity="0.8"/>')
    # barrière
    fx = 640
    out.append('<g fill="#C79A6B">' + "".join(f'<rect x="{fx-150+i*75}" y="470" width="16" height="120" rx="6"/>' for i in range(5))
               + f'<rect x="{fx-170}" y="495" width="340" height="14" rx="7"/><rect x="{fx-170}" y="545" width="340" height="14" rx="7"/></g>')
    # l'agneau saute la barrière (4 sauts par boucle)
    p = (t * 4) % 1.0
    x = 180 + 900 * p
    y = 560 - 230 * math.sin(math.pi * p)
    rot = -18 * math.cos(math.pi * p)
    legs = 8 * math.sin(2 * math.pi * 8 * t)
    out.append(_lamb(x, y, rot, legs))
    # Mimo endormi sur la lune, en haut
    out.append(f'<g transform="translate(300 230) scale(0.55)">{mimo("moon", 0, 0, 1.0, t)}</g>')
    return "".join(out)


def scene_bridge(t, parts):
    out = [_moon(220, 120, 55, 0.16)]
    out.append('<g fill="#0B1230">' + "".join(f'<rect x="{x}" y="{330-h}" width="{w}" height="{h+200}"/>' for x, w, h in
                                           [(60, 80, 60), (150, 60, 110), (980, 90, 90), (1080, 70, 150), (1160, 100, 70)]) + "</g>")
    out.append(_waves(t, 515, cols=("#1A3360", "#152B52", "#112344"), amp=6))
    br = ['<rect x="0" y="405" width="1280" height="125" fill="#8C7A6B"/>',
          '<rect x="0" y="392" width="1280" height="18" rx="4" fill="#A39080"/>',
          '<g stroke="#7A6A5C" stroke-width="2" opacity="0.6">' + "".join(f'<line x1="{x}" y1="420" x2="{x}" y2="520"/>' for x in range(40, 1280, 80)) + "</g>"]
    for cx in (213, 640, 1067):
        br.append(f'<path d="M{cx-150} 531 L{cx-150} 500 A150 95 0 0 1 {cx+150} 500 L{cx+150} 531Z" fill="#132A50"/>')
        br.append(f'<path d="M{cx-150} 500 A150 95 0 0 1 {cx+150} 500" fill="none" stroke="#A39080" stroke-width="8"/>')
    out.append("".join(br))
    for i, x in enumerate([120, 360, 600, 840, 1080]):
        g = 0.35 + 0.2 * math.sin(2 * math.pi * (2 * t + i * 0.21))
        out.append(f'<rect x="{x-4}" y="330" width="8" height="64" fill="#3B3550"/><circle cx="{x}" cy="325" r="30" fill="#FFD77A" opacity="{g*0.45:.2f}"/>'
                   f'<circle cx="{x}" cy="325" r="11" fill="#FFE7A3"/>'
                   f'<rect x="{x-14}" y="{585 + 10*math.sin(2*math.pi*(t+i*0.3)):.1f}" width="28" height="5" rx="2" fill="#FFE7A3" opacity="{g:.2f}"/>')
    # Mimo dort dans sa barque qui passe sous le pont (1 passage par boucle)
    x = -200 + 1680 * t
    out.append(f'<g transform="translate({x:.1f} {590 + 5*math.sin(2*math.pi*4*t):.1f}) scale(0.5)">{mimo("ocean", 0, 0, 1.0, t)}</g>')
    out.append(_waves(t + 0.3, 660, cols=("#112344",), amp=5))
    return "".join(out)


SCENES = {"star": scene_star, "row": scene_row, "bell": scene_bell, "sheep": scene_sheep, "bridge": scene_bridge}


def body(scene, W, H, t, parts):
    a, b = PALETTE[scene]
    k = W / 1280
    zoom = 1 + 0.02 * (0.5 - 0.5 * math.cos(2 * math.pi * t))
    return (f'<defs><linearGradient id="sky_{scene}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>'
            f'<radialGradient id="vig_{scene}" cx="0.5" cy="0.5" r="0.75"><stop offset="0.6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.35"/></radialGradient></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#sky_{scene})"/>'
            f'<g transform="scale({k:.4f}) translate(640 360) scale({zoom:.4f}) translate(-640 -360)">'
            f'{draw_particles(parts, 1280, 720, t)}{SCENES[scene](t, parts)}</g>'
            f'<rect width="{W}" height="{H}" fill="url(#vig_{scene})"/>'
            + text(W - 30 * k, 50 * k, "Sleepy Mimo", int(26 * k), "#FFF4C9", 600, "end", False, 0.55))
